import os
import shutil
import threading
from typing import List
from concurrent.futures import ThreadPoolExecutor

from logger import get_logger

logger = get_logger(__name__)


def get_file_lib(target_folder_) -> dict:
    file_lib_ = dict()

    for folder, _, files in os.walk(target_folder_):
        if files:
            file_lib_[folder] = files

    return file_lib_


def get_ext_set(file_list: List) -> List:
    ext_set = set(map(lambda file_name: file_name.split('.')[-1], file_list))
    return list(ext_set)


def make_ext_folders(target_dir: str, ext_set: List[str]) -> None:
    for ext in ext_set:
        try:
            os.mkdir(target_dir + '\\' + ext.upper())
        except FileExistsError:
            continue
        except FileNotFoundError:
            raise Exception('Check Target_dir in make_ext_folders')


def move_files_to_folder(target_dir: str, files: List[str]) -> None:
    for file in files:
        shutil.move(target_dir + '\\' + file, target_dir + '\\' + file.split('.')[-1].upper())


def sort_folder(target_dir: str, files: List[str]):

    logger.info(f'{threading.get_native_id()} - {target_dir}')

    make_ext_folders(target_dir, get_ext_set(files))
    move_files_to_folder(target_dir, files)


if __name__ == '__main__':

    while True:
        target_folder = input("insert trash folder path or type 'exit': ")

        if target_folder == 'exit':
            break

        file_lib = get_file_lib(target_folder)
        if file_lib:
            with ThreadPoolExecutor(max_workers=len(file_lib)) as executor:
                executor.map(lambda item: sort_folder(*item), file_lib.items())
        else:
            print(f'trash folder {target_folder} was not found, try another.')
