import os
from pathlib import Path
from typing import Dict, Iterable

import requests

BASE_URL = "https://raw.githubusercontent.com/sisinflab/DataRecDatasets/refs/heads/main/"
TEMPLATE = "{FILE_FORMAT}/{FORMATTING}/{DATA}/{FORMATTING}{HEADER}{EXTENSION}"


FILE_FORMATS: Dict[str, Dict[str, Iterable[str]]] = {
    "tsv": {"inline": ["interactions", "timestamp"], "tabular": ["interactions", "ratings", "timestamp"]},
    "json": {"list": ["interactions", "ratings", "timestamp"], "user_wise": ["interactions", "ratings", "timestamp"]},
}
FILE_EXTENSIONS ={"tsv": ".tsv", "json": ".json"}


def _validate_params(file_format: str, formatting: str, data: str) -> None:
    """
    Validate the provided dataset options against the available examples.

    Args:
        file_format (str): File format of the dataset (e.g., `tsv`, `json`).
        formatting (str): Dataset layout variant for the chosen format.
        data (str): Name of the specific data file requested.

    Returns:
        None: Raises a `ValueError` when an unsupported combination is provided.
    """
    if file_format not in FILE_EXTENSIONS:
        raise ValueError(f"Unsupported file format '{file_format}'. Expected one of: {', '.join(FILE_EXTENSIONS)}")
    if formatting not in FILE_FORMATS[file_format]:
        raise ValueError(f"Unsupported formatting '{formatting}' for format '{file_format}'.")
    if data not in FILE_FORMATS[file_format][formatting]:
        raise ValueError(f"Unsupported data '{data}' for format '{file_format}' and formatting '{formatting}'.")


def example_relative_filepath(file_format: str, formatting: str, data: str, header: bool = True) -> str:
    """
    Return the relative path for the requested example dataset.

    Args:
        file_format (str): File format of the dataset (e.g., `tsv`, `json`).
        formatting (str): Dataset layout variant for the chosen format.
        data (str): Name of the specific data file requested.
        header (bool): Whether to include header information in the filename.

    Returns:
        str: Relative path to the example dataset within the repository layout.
    """
    _validate_params(file_format=file_format, formatting=formatting, data=data)
    header_field = "" if header else "_no_header"
    return TEMPLATE.format(
        FILE_FORMAT=file_format,
        FORMATTING=formatting,
        DATA=data,
        HEADER=header_field,
        EXTENSION=FILE_EXTENSIONS[file_format],
    )


def find_url(file_format: str, formatting: str, data: str, header: bool = True) -> str:
    """
    Return the absolute URL for the requested example dataset.

    Args:
        file_format (str): File format of the dataset (e.g., `tsv`, `json`).
        formatting (str): Dataset layout variant for the chosen format.
        data (str): Name of the specific data file requested.
        header (bool): Whether to include header information in the filename.

    Returns:
        str: Absolute URL pointing to the example dataset in the remote repository.
    """
    return BASE_URL + example_relative_filepath(file_format=file_format, formatting=formatting, data=data, header=header)


def download_example(output_folder: str, file_format: str, formatting: str, data: str, header: bool = True) -> None:
    """
    Download an example dataset into the given output directory.

    Args:
        output_folder (str): Local folder where the dataset should be stored.
        file_format (str): File format of the dataset (e.g., `tsv`, `json`).
        formatting (str): Dataset layout variant for the chosen format.
        data (str): Name of the specific data file requested.
        header (bool): Whether to include header information in the filename.

    Returns:
        None: Writes the requested example dataset to `output_folder`.
    """
    output_dir = Path(output_folder)
    if not output_dir.exists():
        raise NotADirectoryError(f"Output directory not found at '{output_folder}'")

    url = find_url(file_format=file_format, formatting=formatting, data=data, header=header)
    relative_path = example_relative_filepath(file_format=file_format, formatting=formatting, data=data, header=header)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total = int(response.headers.get("content-length", 0))
    chunk_size = 8192
    downloaded = 0

    filename = url.split("/")[-1]
    output_path = output_dir / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading example dataset from {url}")
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if not chunk:
                continue
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                percent = int(downloaded * 100 / total)
                print(f"\r{filename}: {percent}% ({downloaded}/{total} bytes)", end="", flush=True)
            else:
                print(f"\r{filename}: {downloaded} bytes downloaded", end="", flush=True)

    print()
    print(f"{filename} downloaded from {url} stored at \'{output_path}\'")


def download_example_by_url(output_folder: str, filename: str, url: str) -> None:
    """
    Download an example dataset from an explicit URL into the given output directory.

    Args:
        output_folder (str): Local folder where the dataset should be stored.
        filename (str): Target filename (including subdirectories if desired).
        url (str): Full URL of the dataset to download.

    Returns:
        None: Writes the dataset to `output_folder/filename`.
    """
    output_dir = Path(output_folder)
    if not output_dir.exists():
        raise NotADirectoryError(f"Output directory not found at '{output_folder}'")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total = int(response.headers.get("content-length", 0))
    chunk_size = 8192
    downloaded = 0

    output_path = output_dir / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading example dataset from {url}")
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if not chunk:
                continue
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                percent = int(downloaded * 100 / total)
                print(f"\r{filename}: {percent}% ({downloaded}/{total} bytes)", end="", flush=True)
            else:
                print(f"\r{filename}: {downloaded} bytes downloaded", end="", flush=True)

    print()
    print(f"{filename} downloaded from {url} stored at \'{output_path}\'")
