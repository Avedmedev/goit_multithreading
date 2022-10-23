import shutil
import threading
from pathlib import Path
from typing import List
from concurrent.futures import ThreadPoolExecutor

from logger import get_logger

logger = get_logger(__name__)


def sort_folder(target_dir: Path, files: List[str]):

    logger.info(f'thread {threading.get_native_id()} started - {target_dir}')

    # get set of file extensions in target directory
    ext_set = set(map(lambda file_name: Path(file_name).suffix, files))

    # make directories named by file extension
    [(target_dir / ext.upper()).mkdir(exist_ok=True, parents=True) for ext in ext_set]

    # move files to directory with own name
    for file in files:
        if Path(file).suffix:
            shutil.move((target_dir / file), target_dir / Path(file).suffix.upper())

    logger.info(f'thread {threading.get_native_id()} finished - {target_dir}')


def folder_walk(target_folder_: Path):
    files = []

    [files.append(el) if el.is_file() else folder_walk(el) for el in target_folder_.iterdir()]

    if files:
        threading.Thread(target=sort_folder, args=(target_folder_, files)).start()


def folders_pool_walk(target_folder_: Path):
    logger.info(f'folders_pool_walk {target_folder_.name} started')

    files = []
    folders = []

    [files.append(el) if el.is_file() else folders.append(el) for el in target_folder_.iterdir()]

    if folders:
        with ThreadPoolExecutor(max_workers=len(folders)) as executor:
            executor.map(folders_pool_walk, folders)
    if files:
        threading.Thread(target=sort_folder, args=(target_folder_, files)).start()


if __name__ == '__main__':

    while True:
        target_folder = input("insert trash folder path or type 'exit': ")

        if target_folder == 'exit':
            break
        else:
            # folder_walk(Path(target_folder))  # walk by tree, push file list to Thread
            folders_pool_walk(Path(target_folder))   # walk by tree, push subfolders to ThreadPoolExecutor and push files to thread

        [thread.join() for thread in threading.enumerate() if thread is not threading.main_thread()]
