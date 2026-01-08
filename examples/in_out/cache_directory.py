"""
DataRec cache usage example.

What this script shows:
  1) Inspect the current cache directory
  2) Print a human-friendly cache summary
  3) Measure total cache size
  4) List top-level cache contents
  5) Temporarily override the cache directory (context manager)
  6) Permanently set and then reset the cache directory
  7) Preview what would be cleared (dry run, no deletion)
  8) Create and then clear a *dummy* dataset safely

Run:
    python -m datarec.usages.cache
"""

from __future__ import annotations

from pathlib import Path

from datarec.io.cache import (
    cache_dir,
    set_cache_dir,
    reset_cache_dir,
    use_cache_dir,
    cache_size,
    list_cache_contents,
    cache_summary,
    clear_cache,
)


def _hr(bytes_val: int) -> str:
    """Human readable size (e.g., 1.23 GB)."""
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    s = float(bytes_val)
    for u in units:
        if s < 1024.0 or u == units[-1]:
            return f"{s:.2f} {u}"
        s /= 1024.0
    return f"{bytes_val} B"


if __name__ == "__main__":
    print("\n=== DataRec Cache — Usage Examples ===\n")

    # 1) Show the current cache directory
    print("1) Current cache directory:")
    print(f"   {cache_dir()}\n")

    # 2) Print a human-friendly summary (top-level only)
    print("2) Cache summary (top-level):")
    print(cache_summary())
    print()

    # 3) Show total cache size
    print("3) Total cache size:")
    print(f"   {cache_size(human_readable=True)}\n")

    # 4) List top-level contents (first level only)
    print("4) Top-level cache contents:")
    entries = list_cache_contents(max_depth=1, include_sizes=True)
    if not entries:
        print("   (empty)")
    else:
        for e in entries:
            kind = "DIR " if e.is_dir else "FILE"
            print(f"   {kind} {e.path.name:<30} {_hr(e.size_bytes)}")
    print()

    # 5) Temporarily override cache directory using a context (safe)
    print("5) Temporary cache directory override (context manager):")
    tmp_dir = Path("/tmp/datarec_temp_cache")
    with use_cache_dir(tmp_dir) as active:
        print(f"   Inside context:  {cache_dir()}")
        # Create a tiny marker file (in the temp cache) just to demonstrate
        marker = active / "example_marker.txt"
        marker.write_text("temporary cache content\n")
        print(f"   Wrote:           {marker}")
    print(f"   Outside context: {cache_dir()}  (restored)\n")

    # 6) Permanently set a custom cache dir, then reset to default
    print("6) Set and reset cache directory:")
    new_dir = Path.home() / "datarec_cache_example"
    set_cache_dir(new_dir, persist_env=True)
    print(f"   Set to:   {cache_dir()}")
    print(f"   Reset to: {reset_cache_dir()}\n")

    # 7) Preview what would be cleared (dry run → no deletion)
    print("7) Preview cache clearing (dry run):")
    preview = clear_cache(force=False)  # will only preview; no deletion
    print(f"   {len(preview['preview'])} path(s) would be removed.\n")

    # 8) Create and then clear a *dummy* dataset safely
    print("8) Create and clear a dummy dataset (safe example):")
    root = cache_dir()
    demo_ds = root / "demo_dataset"
    demo_ds.mkdir(parents=True, exist_ok=True)
    (demo_ds / "dummy.txt").write_text("temporary cache file\n" * 1000)  # ~ small file
    raw = demo_ds / "raw"
    raw.mkdir(exist_ok=True)
    (raw / "blob.bin").write_bytes(b"\x00" * 256 * 1024)  # 256 KB

    print(f"   Dummy dataset path: {demo_ds}")
    print(f"   Size before clear:  {cache_size(subpath='demo_dataset', human_readable=True)}")

    # Now actually clear ONLY the dummy dataset we just created
    result = clear_cache("demo_dataset", force=True)
    print(f"   Removed:            {len(result['removed'])} path(s)")
    print(f"   Freed:              {_hr(result['bytes_freed'])}")
    print(f"   Exists after?       {demo_ds.exists()}\n")

    print("✅ Done.\n")