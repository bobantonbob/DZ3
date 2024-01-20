
import argparse
from pathlib import Path
from shutil import copyfile
from concurrent.futures import ThreadPoolExecutor
import logging
import time

"""
py main.py --source -s picture
py main.py --output -o dist
"""

def grab_folders(path: Path, folders_list):
    for el in path.iterdir():
        if el.is_dir():
            folders_list.append(el)
            grab_folders(el, folders_list)


def sort_file(src_path: Path, output_path: Path):
    start_time = time.time()

    for el in src_path.iterdir():
        if el.is_file():
            ext = el.suffix
            new_path = output_path / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                destination_file = new_path / el.name
                if not destination_file.exists():
                    copyfile(el, destination_file)
                else:
                    logging.warning(f"File {el.name} already exists in {new_path}")
            except OSError as e:
                logging.error(e)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Processing {src_path} took {elapsed_time:.2f} seconds")


def main(source_folder, output_folder):
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    base_folder = Path(source_folder)
    output_folder = Path(output_folder)

    folders = [base_folder]
    grab_folders(base_folder, folders)
    print(folders)

    with ThreadPoolExecutor() as executor:
        for folder in folders:
            executor.submit(sort_file, folder, output_folder)

    print('Всі файли відсортовано. Можна видалити початкову папку.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='App for sorting folder')
    parser.add_argument('-s', '--source', help="Source folder", required=True)
    parser.add_argument('-o', '--output', default='dist')
    args = parser.parse_args()

    main(args.source, args.output)
