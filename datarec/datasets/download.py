import os

import requests
from tqdm import tqdm
import gzip
import shutil
import tarfile
import zipfile

def download_url(url, local_filepath) -> None:
    """
    Download a file from the given URL and save it
    :param url: url to download
    :param local_filepath: path to save
    :return:
    """
    r = requests.get(url)
    r.raise_for_status()
    with open(local_filepath, 'wb') as file:
        with tqdm(unit='byte', unit_scale=True) as progress_bar:
            for chunk in r.iter_content(chunk_size=1024):
                file.write(chunk)
                progress_bar.update(len(chunk))
                print(f"File downloaded successfully and saved as {local_filepath}")

def download_compressed_file(url, local_filepath):
    # Make a GET request to the URL
    response = requests.get(url, stream=True)
    # Check if the request was successful
    if response.status_code == 200:
        # Save the response content to a file
        with open(local_filepath, 'wb') as f:
            with tqdm(unit='byte', unit_scale=True) as progress_bar:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    progress_bar.update(len(chunk))
            print(f"File downloaded successfully and saved as {local_filepath}")
        return local_filepath
    else:
        print(f"Failed to download the file: {response.status_code}")
        return None


def decompress_gz(input_file, output_file):
    print(f'Decompress: \'{input_file}\'')
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f'File decompressed: \'{output_file}\'')
    return output_file


def decompress_tar_file(input_file, output_dir):
    print(f'Decompress: \'{input_file}\'')
    with tarfile.open(input_file, 'r') as tar:
        tar.extractall(path=output_dir)
        print(f'File decompressed in \'{output_dir}\'')
    return os.listdir(output_dir)


def decompress_zip_file(input_file, output_dir):
    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
        print(f'File decompressed in \'{output_dir}\'')
    return os.listdir(output_dir)

