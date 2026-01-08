import os
from pathlib import Path
from typing import List, Dict, Any

import yaml

from datarec.data.resource import load_dataset_config
from datarec.io.paths import (
    REGISTRY_DATASETS_FOLDER,
    registry_dataset_filepath,
    registry_metrics_filepath,
    registry_version_filepath,
)


def available_datasets() -> List[str]:
    return sorted([d.replace(".yml", "") for d in os.listdir(REGISTRY_DATASETS_FOLDER)])


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _md_table(rows: List[List[str]], header: List[str]) -> str:
    lines = []
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "|".join(["---"] * len(header)) + "|")
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def _code_block(text: str, lang: str = "") -> str:
    text = (text or "").rstrip()
    return f"```{lang}\n{text}\n```"


def _build_dataset_markdown(meta: Dict[str, Any], version_cfg: Dict[str, Any], computed: Dict[str, Any]) -> str:
    dataset_name = meta.get("dataset_name", meta.get("name", "Unknown"))
    latest_version = meta.get("latest_version")
    versions = meta.get("versions", [])
    source = meta.get("source")
    description = (meta.get("description") or "").strip()
    citation = (meta.get("citation") or "").strip()

    version = version_cfg.get("version", "unknown")
    sources = version_cfg.get("sources", {}) or {}
    resources = version_cfg.get("resources", {}) or {}

    computed_at = computed.get("computed_at")
    characteristics = (computed.get("characteristics") or {})

    md = []
    md.append(f"# {dataset_name}")
    md.append("")
    md.append("## Overview")
    md.append("")
    md.append(f"**Dataset name:** {dataset_name}  ")
    if latest_version:
        md.append(f"**Latest version:** {latest_version}  ")
    if versions:
        md.append(f"**Available versions:** {', '.join(str(v) for v in versions)}  ")
    if source:
        md.append(f"**Source:** {source}")
    md.append("")
    if description:
        md.append(description)
        md.append("")
    md.append("---")
    md.append("")
    md.append("## Citation")
    md.append("")
    if citation:
        md.append(_code_block(citation, "bibtex"))
    else:
        md.append("_No citation provided._")
    md.append("")
    md.append("---")
    md.append("")
    md.append(f"## Version: {version}")
    md.append("")

    md.append("### Data Sources")
    md.append("")
    if sources:
        rows = []
        for src_name, src in sources.items():
            src_type = str(src.get("source_type", ""))
            args = src.get("args", {}) or {}
            url = str(args.get("url", ""))
            archive = str(args.get("archive", ""))
            checksum = str(args.get("checksum", ""))
            algo = str(args.get("checksum_algorithm", ""))
            rows.append([src_name, src_type, archive, url, f"{algo}:{checksum}" if checksum else ""])
        md.append(_md_table(rows, header=["Name", "Source type", "Archive", "URL", "Checksum"]))
    else:
        md.append("_No sources declared._")
    md.append("")
    md.append("---")
    md.append("")

    md.append("### Resources")
    md.append("")
    if resources:
        for res_name, res in resources.items():
            md.append(f"#### {res_name}")
            md.append("")
            md.append(f"- **Type:** {res.get('type', '')}")
            if res.get("format"):
                md.append(f"- **Format:** `{res.get('format')}`")
            if "required" in res:
                md.append(f"- **Required:** {'yes' if res.get('required') else 'no'}")
            if res.get("source_name"):
                md.append(f"- **Source:** `{res.get('source_name')}`")
            if res.get("filename"):
                md.append(f"- **Filename:** `{res.get('filename')}`")
            if res.get("about"):
                md.append(f"- **About:** {res.get('about')}")
            md.append("")
            schema = res.get("schema")
            if schema:
                md.append("**Schema**")
                md.append("")
                md.append(_code_block(yaml.safe_dump(schema, sort_keys=False).rstrip(), "yaml"))
                md.append("")
    else:
        md.append("_No resources declared._")
        md.append("")

    md.append("---")
    md.append("")
    md.append("## Dataset Characteristics")
    md.append("")
    if computed_at:
        md.append(f"Computed at: **{str(computed_at)[:10]}**")
        md.append("")
    if characteristics:
        rows = [[k, str(v)] for k, v in characteristics.items()]
        md.append(_md_table(rows, header=["Metric", "Value"]))
    else:
        md.append("_No computed characteristics available._")

    md.append("")
    md.append("---")
    md.append("")
    md.append("## License & Usage")
    md.append("")
    md.append("Please refer to the official dataset page for licensing and usage restrictions.")
    if source:
        md.append(source)

    return "\n".join(md).rstrip() + "\n"


def generate_dataset_markdown(dataset_name: str,
                              version: str,
                              output_dir: str = "docs/src/assets/pages/datasets") -> str:
    meta_path = Path(registry_dataset_filepath(dataset_name))
    version_path = Path(registry_version_filepath(dataset_name, version))
    metrics_path = Path(registry_metrics_filepath(dataset_name, version))

    meta = _load_yaml(meta_path)
    version_cfg = _load_yaml(version_path)
    computed = _load_yaml(metrics_path)

    md_text = _build_dataset_markdown(meta, version_cfg, computed)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{dataset_name}_{version}.md"
    out_path.write_text(md_text, encoding="utf-8")
    print(f"Wrote dataset page: {out_path}")
    return str(out_path)


def generate_all_dataset_markdowns(output_dir: str = "docs/src/assets/pages/datasets") -> None:
    for ds_name in available_datasets():
        conf = load_dataset_config(ds_name)
        versions = conf.get("versions", [])
        if isinstance(versions, dict):
            versions = list(versions.keys())
        for version in versions:
            try:
                generate_dataset_markdown(ds_name, version, output_dir=output_dir)
            except Exception as exc:  # noqa: BLE001
                print(f"Failed to generate markdown for {ds_name} {version}: {exc}")


if __name__ == "__main__":
    generate_all_dataset_markdowns()
