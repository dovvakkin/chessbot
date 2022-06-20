"""Module for system dependent sockfish download."""

import os
from os import listdir
from os.path import isfile, join
import platform
import shutil
import stat
from tempfile import mkdtemp
from zipfile import ZipFile

import requests

from tqdm.auto import tqdm

LINUX_BIN = 'https://stockfishchess.org/files/stockfish_15_linux_x64_avx2.zip'
WINDOWS_BIN = 'https://stockfishchess.org/files/stockfish_15_win_x64_avx2.zip'
MACOS_BIN = 'http://macchess.internetcontact.be/downloads/stockfish-14.1-mac.zip'

STOCKFISH_EXECUTABLE = 'chessbot/bin/stockfish.exe'


def download(url, target):
    """Download file from url to target with fancy progress bar."""
    with requests.get(url, stream=True) as r: # pylint: disable=invalid-name
        total_length = int(r.headers.get("Content-Length"))
        with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
            with open(target, 'wb') as output:
                shutil.copyfileobj(raw, output)


def create_bin_according_to_os(system_name):
    """Create stockfish bin for current os."""
    if isfile(STOCKFISH_EXECUTABLE):
        return

    tmp_dir = mkdtemp()
    stockfish_archive = f"{tmp_dir}/sockfish.zip"

    if system_name == 'Windows':
        download(WINDOWS_BIN, stockfish_archive)
    elif system_name == 'Linux':
        download(LINUX_BIN, stockfish_archive)
    elif system_name == 'Darwin':
        download(MACOS_BIN, stockfish_archive)
    else:
        raise RuntimeError('Unknown platform')

    with ZipFile(stockfish_archive, 'r') as zip_obj:
        zip_obj.extractall(tmp_dir)

    os.remove(stockfish_archive)
    onlyfiles = [f for f in listdir(tmp_dir) if isfile(join(tmp_dir, f))]

    if len(onlyfiles) > 1:
        raise RuntimeError('Bad stockfish archive content')

    os.makedirs(os.path.dirname(STOCKFISH_EXECUTABLE), exist_ok=True)
    shutil.move(join(tmp_dir, onlyfiles[0]), STOCKFISH_EXECUTABLE)
    os.chmod(STOCKFISH_EXECUTABLE, 0o775)

    shutil.rmtree(tmp_dir)


def main():
    """Create stockfish bin for current os."""
    create_bin_according_to_os(platform.system())


if __name__ == '__main__':
    main()
