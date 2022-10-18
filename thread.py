import os
import shutil
import threading
from typing import List
from concurrent.futures import ThreadPoolExecutor

from logger import get_logger

logger = get_logger(__name__)


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

    logger.info(f'thread {threading.get_native_id()} started - {target_dir}')

    make_ext_folders(target_dir, get_ext_set(files))
    move_files_to_folder(target_dir, files)

    logger.info(f'tread {threading.get_native_id()} finished - {target_dir}')


def folder_walk(target_folder_):
    for folder, _, files in os.walk(target_folder_):
        if files:
            threading.Thread(target=sort_folder, args=(folder, files)).start()


def folders_walk(target_folder_):
    logger.info(f'folders_walk {target_folder_} started')
    parent_folder, folders, files = next(os.walk(target_folder_))
    if folders:
        for folder in folders:
            threading.Thread(target=folders_walk, args=(parent_folder + "\\" + folder, )).start()
    if files:
        threading.Thread(target=sort_folder, args=(parent_folder, files)).start()


def folders_pool_walk(target_folder_):
    logger.info(f'folders_pool_walk {target_folder_} started')
    parent_folder, folders, files = next(os.walk(target_folder_))
    if folders:
        with ThreadPoolExecutor(max_workers=len(folders)) as executor:
            executor.map(lambda fld: folders_pool_walk(parent_folder + "\\" + fld), folders)
    if files:
        threading.Thread(target=sort_folder, args=(parent_folder, files)).start()


if __name__ == '__main__':

    while True:
        target_folder = input("insert trash folder path or type 'exit': ")

        if target_folder == 'exit':
            break
        else:
            # folder_walk(target_folder)  # walk by tree, push files to Thread
            # folders_walk(target_folder)  # walk by tree, push subfolders to Threads and push files to Thread
            folders_pool_walk(target_folder)   # walk by tree, push subfolders to ThreadPoolExecutor and push files to thread

        for thread in threading.enumerate():
            if thread is not threading.main_thread():
                thread.join()
