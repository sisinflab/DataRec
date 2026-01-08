from __future__ import annotations

from pathlib import Path
from contextlib import contextmanager
from typing import Union, Iterator, Optional
import logging
import os
import threading

from appdirs import user_cache_dir

_LOG = logging.getLogger(__name__)
_LOCK = threading.RLock()

_CACHE_DIR: Optional[Path] = None


def _default_cache_dir(app_name: str = "datarec", app_author: str = "sisinflab") -> Path:
    """
    Determine the default cache directory following the priority:
    environment variable → appdirs default.

    Args:
        app_name: Application name for appdirs.
        app_author: Application author (used on macOS/Windows).

    Output:
        Path: Absolute path to the cache directory (created if it does not exist).
    """
    env_override = os.getenv("DATAREC_CACHE_DIR")
    base = Path(env_override) if env_override else Path(user_cache_dir(app_name, app_author))
    base = base.expanduser().resolve()
    base.mkdir(parents=True, exist_ok=True)
    return base


def _check_writable(p: Path) -> None:
    """
    Ensure that the given path exists and is writable by creating and removing a temporary file.

    Args:
        p: Path to validate.

    Output:
        None

    Raises:
        PermissionError: If the path is not writable or cannot be created.
    """
    try:
        p.mkdir(parents=True, exist_ok=True)
        probe = p / ".datarec_write_test"
        with open(probe, "wb") as f:
            f.write(b"ok")
        probe.unlink(missing_ok=True)
    except Exception as e:
        raise PermissionError(f"Cache directory is not writable: {p}") from e


def cache_dir() -> Path:
    """
    Return the current cache directory (creating it if missing).

    Priority order:
      1) Directory set via `set_cache_dir()`
      2) Environment variable `DATAREC_CACHE_DIR`
      3) System default from `appdirs`

    Output:
        Path: Absolute path to the active cache directory.

    Usage:
        >>> from datarec.io.cache import cache_dir
        >>> cache_dir()
        PosixPath('/home/user/.cache/sisinflab/datarec')
    """
    with _LOCK:
        global _CACHE_DIR
        if _CACHE_DIR is None:
            _CACHE_DIR = _default_cache_dir()
        return _CACHE_DIR


def set_cache_dir(path: Union[str, Path], *, persist_env: bool = False) -> Path:
    """
    Dynamically set the cache directory (takes precedence over the environment variable).

    Args:
        path: The new cache directory path. Can include '~' or environment variables.
        persist_env: If True, updates `os.environ["DATAREC_CACHE_DIR"]` for the current process.

    Output:
        Path: Absolute path to the newly set cache directory.

    Raises:
        PermissionError: If the directory is not writable.

    Usage:
        >>> from datarec.io.cache import set_cache_dir, cache_dir
        >>> set_cache_dir("~/datasets/datarec_cache", persist_env=True)
        PosixPath('/home/user/datasets/datarec_cache')
        >>> cache_dir()
        PosixPath('/home/user/datasets/datarec_cache')
    """
    with _LOCK:
        global _CACHE_DIR
        p = Path(os.path.expandvars(os.path.expanduser(str(path)))).resolve()
        _check_writable(p)
        _CACHE_DIR = p
        if persist_env:
            os.environ["DATAREC_CACHE_DIR"] = str(p)
        _LOG.info("[DataRec] Cache directory set to: %s", _CACHE_DIR)
        return _CACHE_DIR


def reset_cache_dir() -> Path:
    """
    Reset the internal cache directory state.
    The next call to `cache_dir()` will reload it from the environment or use the default.

    Output:
        Path: The cache directory after reset.

    Usage:
        >>> from datarec.io.cache import set_cache_dir, reset_cache_dir
        >>> set_cache_dir("/tmp/datarec")
        PosixPath('/tmp/datarec')
        >>> reset_cache_dir()
        PosixPath('/home/user/.cache/sisinflab/datarec')  # if no environment variable is set
    """
    with _LOCK:
        global _CACHE_DIR
        _CACHE_DIR = None
        return cache_dir()


def reload_cache_dir_from_env() -> Path:
    """
    Reload the cache directory from the environment variable `DATAREC_CACHE_DIR`.
    If not set, fall back to the default cache path.

    Output:
        Path: The resulting cache directory after reload.

    Usage:
        >>> from datarec.io.cache import reload_cache_dir_from_env
        >>> os.environ["DATAREC_CACHE_DIR"] = "/mnt/shared/datarec"
        >>> reload_cache_dir_from_env()
        PosixPath('/mnt/shared/datarec')
    """
    with _LOCK:
        env = os.getenv("DATAREC_CACHE_DIR")
        return set_cache_dir(env, persist_env=False) if env else reset_cache_dir()


@contextmanager
def use_cache_dir(temp_path: Union[str, Path]) -> Iterator[Path]:
    """
    Temporarily override the cache directory within a context.

    Args:
        temp_path: Temporary path to use as cache directory during the context block.

    Output:
        Iterator[Path]: The temporary cache directory used within the context.

    Usage:
        >>> from datarec.io.cache import cache_dir, use_cache_dir
        >>> base = cache_dir()
        >>> with use_cache_dir("/tmp/datarec_tests") as tmp:
        ...     assert cache_dir() == tmp
        >>> assert cache_dir() == base
    """
    previous = cache_dir()
    try:
        current = set_cache_dir(temp_path, persist_env=False)
        yield current
    finally:
        set_cache_dir(previous, persist_env=False)



from dataclasses import dataclass

@dataclass(frozen=True)
class CacheEntry:
    """Lightweight descriptor for cache listing results."""
    path: Path
    is_dir: bool
    size_bytes: int


def _human_size(n: int) -> str:
    """Format bytes into a readable string (e.g., '1.23 GB')."""
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    s = float(n)
    for u in units:
        if s < 1024.0 or u == units[-1]:
            return f"{s:.2f} {u}"
        s /= 1024.0
    return f"{n} B"


def _dir_size(p: Path) -> int:
    """Compute directory size recursively (follows files, skips symlinks)."""
    total = 0
    # Use os.scandir for performance
    for root, dirs, files in os.walk(p, followlinks=False):
        for name in files:
            fp = Path(root) / name
            try:
                if not fp.is_symlink():
                    total += fp.stat().st_size
            except OSError:
                # Ignore files that disappear mid-walk or are inaccessible
                continue
    return total


def _file_size(p: Path) -> int:
    try:
        return 0 if p.is_symlink() else p.stat().st_size
    except OSError:
        return 0


def _safe_under_cache(p: Path) -> None:
    """
    Ensure that the given path is inside the active cache directory.

    Raises:
        ValueError: If `p` is outside the cache root.
    """
    root = cache_dir().resolve()
    pr = p.resolve()
    try:
        pr.relative_to(root)
    except ValueError as e:
        raise ValueError(f"Refusing to operate outside cache root: {pr} (root={root})") from e


def list_cache_contents(subpath: Union[str, Path, None] = None,
                        *,
                        max_depth: int = 1,
                        include_sizes: bool = True,
                        human_readable: bool = True) -> list[CacheEntry]:
    """
    List cached items under the cache root (or a subfolder).

    Args:
        subpath: Optional subfolder relative (or absolute) to the cache root.
        max_depth: Directory depth to traverse (0 = only the target directory itself).
        include_sizes: If True, compute size per entry (dirs recursively).
        human_readable: Ignored in output (entries are typed); kept for future CLI formatting.

    Output:
        list[CacheEntry]: One entry per file/dir found up to `max_depth`.

    Usage:
        >>> # Top-level directories (datasets, etc.)
        >>> list_cache_contents(max_depth=1)
        >>> # Inspect a specific dataset folder
        >>> list_cache_contents("amazon_clothing/2023", max_depth=2)
    """
    with _LOCK:
        root = cache_dir()
        target = (root / subpath) if subpath else root
        target = target.expanduser().resolve()
        _safe_under_cache(target)

        results: list[CacheEntry] = []
        if not target.exists():
            return results  # empty

        # BFS-style traversal up to max_depth
        queue: list[tuple[Path, int]] = [(target, 0)]
        while queue:
            cur, depth = queue.pop(0)
            if depth > max_depth:
                continue
            try:
                with os.scandir(cur) as it:
                    for entry in it:
                        p = Path(entry.path)
                        is_dir = entry.is_dir(follow_symlinks=False)
                        size = 0
                        if include_sizes:
                            size = _dir_size(p) if is_dir else _file_size(p)
                        results.append(CacheEntry(path=p, is_dir=is_dir, size_bytes=size))
                        if is_dir and depth < max_depth:
                            queue.append((p, depth + 1))
            except NotADirectoryError:
                # If target is a file and max_depth >= 0, include it directly
                size = _file_size(cur) if include_sizes else 0
                results.append(CacheEntry(path=cur, is_dir=False, size_bytes=size))
            except FileNotFoundError:
                # Target disappeared mid-scan; ignore
                continue
        return results


def cache_size(subpath: Union[str, Path, None] = None,
               *,
               human_readable: bool = False) -> Union[int, str]:
    """
    Compute the total size of the cache (or a subfolder).

    Args:
        subpath: Optional subfolder relative (or absolute) to the cache root.
        human_readable: If True, return a string like '1.23 GB'; otherwise number of bytes.

    Output:
        int | str: Size in bytes (int) or human-readable string.

    Usage:
        >>> cache_size()
        123456789
        >>> cache_size("amazon_clothing/2023", human_readable=True)
        '2.34 GB'
    """
    with _LOCK:
        root = cache_dir()
        target = (root / subpath) if subpath else root
        target = target.expanduser().resolve()
        _safe_under_cache(target)

        if not target.exists():
            return "0 B" if human_readable else 0
        total = _dir_size(target) if target.is_dir() else _file_size(target)
        return _human_size(total) if human_readable else total


def clear_cache(target: Union[str, Path, None] = None,
                *,
                patterns: Optional[list[str]] = None,
                force: bool = False) -> dict:
    """
    Safely delete cached elements (never outside the cache root).

    Behavior:
      - If `force=True`, delete immediately (no prompt).
      - Else, show a preview and ask 'Proceed? [y/N]'. Only 'y'/'yes' proceeds.
      - Refuses to wipe the entire cache root unless `force=True` or user confirms.

    Args:
        target: Relative/absolute path under the cache root. If None, operates on the root.
        patterns: Optional glob patterns (e.g., ['**/*.tmp', '*/raw/*']).
        force: Keyword-only. If True, perform deletion without interactive prompt.

    Output:
        dict: {'removed': [Path], 'skipped': [Path], 'bytes_freed': int,
               'forced': bool, 'confirmed': bool, 'aborted': bool, 'preview': [Path]}
    """
    import sys, shutil

    # Defensive: catch accidental old-style calls like clear_cache(True, "lastfm")
    if isinstance(target, bool):
        raise TypeError(
            "clear_cache() now expects `target` first and `force` as keyword-only.\n"
            "Use: clear_cache('lastfm', force=True)"
        )

    root = cache_dir()
    base = (root / target) if target else root
    base = base.expanduser().resolve()
    _safe_under_cache(base)

    # Build candidate list (read-only)
    if patterns:
        cands: list[Path] = []
        for pat in patterns:
            cands.extend(base.glob(pat))
        candidates = sorted({p.resolve() for p in cands})
    else:
        candidates = [base]

    # Preview existing paths + size estimation
    preview: list[Path] = []
    est_bytes = 0
    for p in candidates:
        try:
            _safe_under_cache(p)
            if p.exists():
                preview.append(p)
                est_bytes += _dir_size(p) if p.is_dir() else _file_size(p)
        except Exception:
            continue

    if not preview:
        return {"removed": [], "skipped": [], "bytes_freed": 0,
                "forced": force, "confirmed": False, "aborted": False, "preview": []}

    # If target is cache root and not forced, require explicit confirmation
    confirmed = force
    if not force:
        if not sys.stdin.isatty():
            # Non-interactive env: safer to abort
            return {"removed": [], "skipped": [], "bytes_freed": 0,
                    "forced": False, "confirmed": False, "aborted": True, "preview": preview}

        # Human-readable preview (limit lines)
        print("The following paths will be removed:")
        limit = 50
        for i, p in enumerate(preview[:limit], 1):
            label = "(dir)" if p.is_dir() else "(file)"
            try:
                sz = _dir_size(p) if p.is_dir() else _file_size(p)
            except Exception:
                sz = 0
            print(f"  {i:>4}. {p} {label}  {_human_size(sz)}")
        if len(preview) > limit:
            print(f"  ... and {len(preview) - limit} more")
        print(f"\nEstimated space to be freed: {_human_size(est_bytes)}")

        # Extra safety: if wiping root with no patterns, make user explicitly confirm
        if base == root and not patterns:
            print("WARNING: you are about to clear the ENTIRE DataRec cache root.")

        ans = input("Proceed? [y/N]: ").strip().lower()
        confirmed = ans in ("y", "yes")
        if not confirmed:
            return {"removed": [], "skipped": [], "bytes_freed": 0,
                    "forced": False, "confirmed": False, "aborted": True, "preview": preview}

    # Mutating phase under lock
    removed: list[Path] = []
    skipped: list[Path] = []
    freed = 0
    with _LOCK:
        for p in preview:
            try:
                _safe_under_cache(p)
                if p.is_dir():
                    sz = _dir_size(p)
                    shutil.rmtree(p, ignore_errors=False)
                    freed += sz
                    removed.append(p)
                elif p.exists():
                    sz = _file_size(p)
                    p.unlink(missing_ok=False)
                    freed += sz
                    removed.append(p)
                else:
                    skipped.append(p)
            except Exception:
                skipped.append(p)

    return {"removed": removed, "skipped": skipped, "bytes_freed": freed,
            "forced": force, "confirmed": confirmed, "aborted": False, "preview": preview}


def cache_summary(max_items: int = 20,
                  *,
                  sort_by: str = "size",
                  descending: bool = True,
                  human_readable: bool = True) -> str:
    """
    Produce a concise, human-friendly summary of the cache root,
    considering only *top-level entries* (datasets or files directly
    under the cache root). Subfolders are NOT included recursively.

    Args:
        max_items: Maximum number of top-level entries to show (after sorting).
        sort_by: 'size' or 'name'.
        descending: Sort direction (relevant for 'size' and 'name').
        human_readable: If True, format sizes like '1.23 GB'.

    Output:
        str: A formatted table-like string.

    Example:
        >>> print(cache_summary(max_items=10))
        DATASET                          SIZE
        -----------------------------------------
        Alibaba                       21.49 GB
        yelp                          16.75 GB
        amazon_clothing                4.81 GB
        ...
    """
    with _LOCK:
        root = cache_dir()
        rows = {}

        # Walk only top-level entries
        for entry in os.scandir(root):
            if entry.name.startswith("."):  # ignore hidden/system files
                continue
            path = Path(entry.path)
            if entry.is_file(follow_symlinks=False):
                size = _file_size(path)
            elif entry.is_dir(follow_symlinks=False):
                # compute recursively
                size = _dir_size(path)
            else:
                size = 0

            rows[entry.name] = size

        # Sort
        items = list(rows.items())
        if sort_by == "name":
            items.sort(key=lambda x: x[0].lower(), reverse=descending)
        else:
            items.sort(key=lambda x: x[1], reverse=descending)

        if max_items and max_items > 0:
            items = items[:max_items]

        # Pretty print
        name_w = max([len("DATASET")] + [len(k) for k, _ in items]) if items else len("DATASET")
        lines = [f'{"DATASET".ljust(name_w)}  SIZE', "-" * (name_w + 7)]

        for k, v in items:
            size_str = _human_size(v) if human_readable else str(v)
            lines.append(f'{k.ljust(name_w)}  {size_str}')

        total = sum(v for _, v in rows.items())
        total_str = _human_size(total) if human_readable else str(total)
        lines.append("")
        lines.append(f"Total cache size (non-recursive): {total_str}")

        return "\n".join(lines)