from os import listdir
from os.path import isfile, join, splitext
from typing import List
import requests

UPLOAD_MENUS_FLAG = False
UPLOAD_REGISTERS_FLAG = True
TRANSFORM_MENUS_FILES_URL = "http://0.0.0.0:5050/dataset_creation/menu/transform_file"
UPLOAD_MENUS_URL = "http://0.0.0.0:5050/dataset_creation/menu/insert"
TRANSFORM_REGISTERS_FILES_URL = "http://0.0.0.0:5050/dataset_creation/register/transform_file"
UPLOAD_REGISTERS_URL = "http://0.0.0.0:5050/dataset_creation/register/insert"
MENUS_PATH = './data/MENU/'
MENUS_EXTENSION = ['.csv', '.tsv']
REGISTERS_PATH = './data/REGISTERS/'
REGISTERS_EXTENSION = ['.xlsx']


def get_list_of_files(path: str, extensions: List[str] = []):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    if len(extensions) > 0:
        return [file for file in files if splitext(file.lower())[1] in extensions]
    return files


# Main
if UPLOAD_MENUS_FLAG:
    print("Uploading Menus...")
    menu_files = get_list_of_files(MENUS_PATH, MENUS_EXTENSION)
    num_files = len(menu_files)
    for idx, file in enumerate(menu_files):
        with open(f"{MENUS_PATH}{file}", "rb") as a_file:
            print(f"{idx}/{num_files} -> File: {file}", end=' ')
            file_dict = {"file": a_file}
            transform_response = requests.post(TRANSFORM_MENUS_FILES_URL, files=file_dict)
            response = requests.post(UPLOAD_MENUS_URL, json=transform_response.json())
            print(response)

if UPLOAD_REGISTERS_FLAG:
    print("Uploading Registers...")
    register_files = get_list_of_files(REGISTERS_PATH, REGISTERS_EXTENSION)
    num_files = len(register_files)
    for idx, file in enumerate(register_files):
        with open(f"{REGISTERS_PATH}{file}", "rb") as a_file:
            print(f"{idx+1}/{num_files} -> File: {file}", end=' ')
            file_dict = {"file": a_file}
            transform_response = requests.post(TRANSFORM_REGISTERS_FILES_URL, files=file_dict)
            response = requests.post(UPLOAD_REGISTERS_URL, json=transform_response.json())
            print(response)

