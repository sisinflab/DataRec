"""
Provides utility functions for downloading and decompressing dataset files.

This module contains a set of helper functions used internally by the dataset
builder classes (e.g., `MovieLens1M`, `Yelp_v1`) to handle the fetching of
raw data from web sources and the extraction of various archive formats
like .zip, .gz, .tar, and .7z.

These functions are not typically called directly by the end-user but are
fundamental to the automatic data preparation process of the library.
"""
import os
import requests
from tqdm import tqdm
import gzip
import shutil
import tarfile
import zipfile
import py7zr


def download_url(url, local_filepath) -> None:
    """
    Downloads a file from a URL and saves it to a local path.

    Note: This is a basic downloader. For large files or more robust handling,
    `download_file` is generally preferred within this library.

    Args:
        url (str): The URL of the file to download.
        local_filepath (str): The local path where the file will be saved.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returned an
            unsuccessful status code.
    """
    r = requests.get(url)
    r.raise_for_status()
    with open(local_filepath, 'wb') as file:
        with tqdm(unit='byte', unit_scale=True) as progress_bar:
            for chunk in r.iter_content(chunk_size=1024):
                file.write(chunk)
                progress_bar.update(len(chunk))
                print(f"File downloaded successfully and saved as {local_filepath}")


def download_file(url, local_filepath, size=None):
    """
    Downloads a file by streaming its content, with a progress bar.

    This is the primary download function used for most datasets. It streams the
    response, making it suitable for large files. It attempts to infer the file
    size from response headers for the progress bar, but an expected size can also
    be provided.

    Args:
        url (str): The URL of the file to download.
        local_filepath (str): The local path where the file will be saved.
        size (int, optional): The expected file size in bytes. Used for the
            progress bar if the 'Content-Length' header is not available.
            Defaults to None.

    Returns:
        (str): The local file path if the download was successful, otherwise None.
    """
    # Make a GET request to the URL
    response = requests.get(url, stream=True)
    # Check if the request was successful
    if response.status_code == 200:
        # try to infer the total size
        try:
            size = int(response.headers.get('Content-Length', 0))
        except:
            size = size
        # Save the response content to a file
        with open(local_filepath, 'wb') as f:
            with tqdm(unit='byte', unit_scale=True, total=size) as progress_bar:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    progress_bar.update(len(chunk))
            print(f"File downloaded successfully and saved at \'{local_filepath}\'")
        return local_filepath
    else:

        print(f"Failed to download the file. Response status code: {response.status_code}")
        return None


def download_browser(url, local_filepath, headers=None, chunk_size=8192):
    """
    Downloads a file by mimicking a web browser request.

    This function is used for sources that may block simple scripted requests.
    It includes a default 'User-Agent' header to appear as a standard browser,
    which is necessary for some datasets (e.g., Yelp).

    Args:
        url (str): The URL of the file to download.
        local_filepath (str): The local path where the file will be saved.
        headers (dict, optional): Custom headers to use for the request. If None,
            a default browser User-Agent is used. Defaults to None.
        chunk_size (int, optional): The size of chunks to download in bytes.
            Defaults to 8192.

    Returns:
        (str): The local file path if the download was successful, otherwise None.
    """
    # Default headers, or a custom one if provided
    if headers is None:
        headers = {'User-Agent': 'Mozilla/5.0...'}
    response = requests.get(url, stream=True, headers=headers)
    if response.status_code == 200:
        total_size = int(response.headers.get('Content-Length', 0))
        with open(local_filepath, 'wb') as f:
            with tqdm(total=total_size, unit='iB', unit_scale=True) as progress_bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))
        print(f"Downloaded to '{local_filepath}'")
        return local_filepath
    return None


def decompress_gz(input_file, output_dir, output_file=None, **kwargs):
    """
    Decompresses a .gz file.

    Args:
        input_file (str): The path to the input .gz file.
        output_dir (str): The path to the output decompressed file.
        output_file (str, optional): The name of the output file. If None,

    Returns:
        (str): The path to the decompressed output file.
    """
    print(f'Decompress: \'{input_file}\'')
    if output_file is None:
        output_file = os.path.join(output_dir, os.path.basename(input_file).replace('.gz', ''))
    else:
        output_file = os.path.join(output_dir, output_file)
    assert input_file != output_file, "Input and output file paths must be different."
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f'File decompressed: \'{output_file}\'')
    return output_file


def decompress_tar_file(input_file, output_dir, **kwargs):
    """
    Decompresses a .tar archive.

    Args:
        input_file (str): The path to the input .tar file.
        output_dir (str): The directory where the contents will be extracted.

    Returns:
        (list): A list of the names of the extracted files and directories.
    """

    print(f'Decompress: \'{input_file}\'')
    with tarfile.open(input_file, 'r') as tar:
        tar.extractall(path=output_dir)

        print(f'File decompressed in \'{output_dir}\'')
    return os.listdir(output_dir)


def decompress_zip_file(input_file, output_dir, allowZip64=False, **kwargs):
    """
    Decompresses a .zip archive.

    Args:
        input_file (str): The path to the input .zip file.
        output_dir (str): The directory where the contents will be extracted.
        allowZip64 (bool): Whether to allow the Zip64 extension (for archives
            larger than 2 GB). Defaults to False, but should be True for large files.

    Returns:
        (list): A list of the names of the extracted files and directories.
    """
    with zipfile.ZipFile(input_file, 'r', allowZip64=allowZip64) as zip_ref:
        zip_ref.extractall(output_dir)
        print(f'File decompressed in \'{output_dir}\'')
    return os.listdir(output_dir)


def decompress_7z_file(input_file, output_dir, **kwargs):
    """
    Decompresses a .7z archive.

    This function is used for datasets distributed in the 7-Zip format, such as
    the Alibaba-iFashion dataset.

    Args:
        input_file (str): The path to the input .7z file.
        output_dir (str): The directory where the contents will be extracted.

    Returns:
        (str): The path to the output directory.
    """
    print(f"Decompressing: {input_file}")
    with py7zr.SevenZipFile(input_file, mode='r') as archive:
        archive.extractall(path=output_dir)
    print(f"File decompressed in '{output_dir}'")
    return output_dir

def decompress_file(input_file, output_dir, archive_type, **kwargs):
    """
    Decompresses a file based on its archive type.

    This function serves as a dispatcher to call the appropriate decompression
    function based on the specified archive type.

    Args:
        input_file (str): The path to the input archive file.
        output_dir (str): The directory where the contents will be extracted.
        archive_type (str): The type of the archive ('gz', 'tar', 'zip', '7z').

    Returns:
        (str or list): The path to the decompressed file or a list of extracted
            files/directories, depending on the archive type.

    Raises:
        ValueError: If an unsupported archive type is provided.
    """
    archive_type = archive_type.lower()
    archive_types = ('gz', 'tar', 'zip', '7z')
    if archive_type not in archive_types:
        raise ValueError(f"Unsupported archive type: {archive_type}. Supported types are: {archive_types}")
    if archive_type == 'gz':
        return decompress_gz(input_file, output_dir, **kwargs)
    elif archive_type == 'tar':
        return decompress_tar_file(input_file, output_dir, **kwargs)
    elif archive_type == 'zip':
        return decompress_zip_file(input_file, output_dir, **kwargs)
    elif archive_type == '7z':
        return decompress_7z_file(input_file, output_dir, **kwargs)
    else:
        raise ValueError(f"Unsupported archive type: {archive_type}")
