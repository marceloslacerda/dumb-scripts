#!/usr/bin/env python3

import mimetypes
import pathlib
import sys
import subprocess
import zipfile


def main(file):
    print(f"Processing {file}")
    ftype=mimetypes.guess_type(file)[0]
    if "zip" in ftype:
        print("Guessed type to be zip")
        zip = zipfile.ZipFile(file)
        filenames = zip.namelist()
        if all('/' in file for file in filenames):
            root = min(filenames)
            print(f"All files are contained in a directory, extracting to {root}")
            zip.extractall()
        else:
            print(f"Some files are not contained in a directory, extracting to {file.stem}")
            zip.extractall(file.stem)
    elif "rar" in ftype:
        print("Guessed type to be rar")
        filenames = subprocess.run(["unrar", "l"], encoding="utf-8", check=True).split("\n")
        if all('/' in file for file in filenames):
            root = min(filenames)
            print(f"All files are contained in a directory, extracting to {root}")
            subprocess.run(["unrar", "e"], check=True)
        else:
            subdir = file.stem
            print(f"Some files are not contained in a directory, extracting to {subdir}")
            pathlib.Path(subdir).mkdir()
            subprocess.run(["unrar", "e"], check=True, cwd=file.stem)
    elif "lzma" in ftype:
        print("Guessed type to be 7zip")
        filenames = subprocess.run(["7z", "l"], encoding="utf-8", check=True).split("\n")
        if all('/' in file for file in filenames):
            root = min(filenames)
            print(f"All files are contained in a directory, extracting to {root}")
            subprocess.run(["7z", "x"], check=True)
        else:
            subdir = file.stem
            print(f"Some files are not contained in a directory, extracting to {subdir}")
            pathlib.Path(subdir).mkdir()
            subprocess.run(["7z", "x"], check=True, cwd=file.stem)
    else:
        print(f"I don't know how to extract {ftype}")
        exit(1)
    print("All files successfully extracted")


if __name__ == '__main__':
    main(pathlib.Path(sys.argv[1]))
