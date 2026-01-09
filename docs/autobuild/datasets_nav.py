import os
import shutil
from typing import Iterable

import yaml

from datarec.io.paths import DOCS_FOLDER, REGISTRY_DATASETS_FOLDER

INTRO = """DataRec includes several commonly used recommendation datasets to facilitate reproducibility and standardization. These datasets have been carefully curated, with traceable sources and versioning information maintained whenever possible.
For each dataset, DataRec provides metadata such as the number of users, items, and interactions and data characteristics known to impact recommendation performance (e.g., sparsity and user/item distribution shifts).
The dataset collection in DataRec is continuously updated to include more recent and widely used datasets from the recommendation systems literature. The most recent and widely used version is included when the original data source is unavailable to ensure backward compatibility.

The following datasets are currently included in DataRec:
"""

ASSETS_PAGES_SRC = os.path.join(DOCS_FOLDER, "assets", "pages", "datasets")
ASSETS_PAGES_DST = os.path.join(DOCS_FOLDER, "src", "assets", "pages", "datasets")


def _load_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def _list_dataset_configs() -> Iterable[str]:
    for filename in sorted(os.listdir(REGISTRY_DATASETS_FOLDER)):
        if filename.endswith(".yml"):
            yield os.path.join(REGISTRY_DATASETS_FOLDER, filename)


def _versions_from_config(config: dict) -> list[str]:
    versions = config.get("versions", [])
    if isinstance(versions, dict):
        return sorted(versions.keys())
    if isinstance(versions, list):
        return sorted(str(v) for v in versions)
    return []


def _ensure_assets_pages() -> None:
    if not os.path.isdir(ASSETS_PAGES_SRC):
        return
    os.makedirs(ASSETS_PAGES_DST, exist_ok=True)
    for filename in os.listdir(ASSETS_PAGES_SRC):
        if filename.endswith(".md"):
            src = os.path.join(ASSETS_PAGES_SRC, filename)
            dst = os.path.join(ASSETS_PAGES_DST, filename)
            shutil.copy2(src, dst)


def build_datasets_nav() -> str:
    dataset_nav_path = os.path.join(DOCS_FOLDER, "src", "datasets_nav.md")
    _ensure_assets_pages()

    lines = [
        INTRO,
        "",
        '<div class="datasets-table">',
        '<table>',
        "<thead>",
        "<tr><th>Dataset</th><th>Version</th><th>Dataset Page</th></tr>",
        "</thead>",
        "<tbody>",
    ]

    for config_path in _list_dataset_configs():
        config = _load_yaml(config_path)
        dataset_file_stem = os.path.splitext(os.path.basename(config_path))[0]
        dataset_display = config.get("dataset_name", dataset_file_stem)
        versions = _versions_from_config(config)

        if not versions:
            versions = ["-"]

        row_span = len(versions)
        for idx, version in enumerate(versions):
            page_name = f"{dataset_file_stem}_{version}.md"
            page_rel = f"../assets/pages/datasets/{dataset_file_stem}_{version}/"
            page_path = os.path.join(ASSETS_PAGES_DST, page_name)
            page_cell = f'<a href="{page_rel}">page</a>' if os.path.exists(page_path) else "—"
            if idx == 0:
                dataset_cell = f'<td rowspan="{row_span}">{dataset_display}</td>'
            else:
                dataset_cell = ""
            lines.append(f"<tr>{dataset_cell}<td>{version}</td><td>{page_cell}</td></tr>")

    lines.append("</tbody>")
    lines.append("</table>")
    lines.append("</div>")

    with open(dataset_nav_path, "w") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    print(f"Generated '{dataset_nav_path}'")
    return dataset_nav_path


if __name__ == "__main__":
    build_datasets_nav()
