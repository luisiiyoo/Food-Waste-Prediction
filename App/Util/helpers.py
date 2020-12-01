import pickle
import os
import json
import random
import uuid
import time
from datetime import datetime
from typing import Any, Dict, List
from numpy.random import permutation
from App.Util.constants import DATE_FORMAT


def read_object_from_pkl_file(full_file_path: str) -> Any:
    """
    Reads an object from a pkl file

    Args:
        full_file_path (str): Complete path and file name where will be saved the file

    Returns:
        Any: Object from the pkl read file
    """
    if not os.path.exists(full_file_path) or not os.path.isfile(full_file_path):
        raise Exception(f"'{full_file_path}' file does not exist.")
    with open(full_file_path, 'rb', pickle.HIGHEST_PROTOCOL) as f:
        obj: Any = pickle.load(f)
    return obj


def save_object_to_pkl_file(obj: Any, full_file_path: str) -> None:
    """
    Saves an object in a pkl file

    Args:
        obj (Any): Object to save in a pkl file
        full_file_path (str): Complete path and file name where will be saved the file

    Returns:
        None
    """
    print(f'\nSaving variables on {full_file_path}')
    output_path, output_file = os.path.split(full_file_path)

    if output_path and not os.path.isdir(output_path):
        try:
            os.makedirs(output_path)  # os.mkdir for one directory only
        except OSError:
            print("Creation of the directory %s failed" % output_path)
        else:
            print("Successfully created the directory %s " % output_path)
    with open(full_file_path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def str_to_timestamp(date: str) -> int:
    """
    Converts a string to a timestamp integer

    Args:
        date (str): Date as a string

    Returns:
        int: Timestamp integer
    """
    date_formats = (DATE_FORMAT, DATE_FORMAT.replace('-', '/'), DATE_FORMAT.replace('-', '.'))
    for fmt in date_formats:
        try:
            dt_object = datetime.strptime(date, fmt).timetuple()
            return int(time.mktime(dt_object))
        except ValueError:
            pass
        raise ValueError(f"No valid date format found. Use the next format: '{DATE_FORMAT}'.")


def timestamp_to_str(timestamp: int) -> str:
    """
    Converts a timestamp integer to a string

    Args:
        timestamp (int): Timestamp integer

    Returns:
        str: Date as a string
    """
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime(DATE_FORMAT)


def datetime_to_str(date: datetime) -> str:
    """
    Converts a datetime_to_str instance to a string

    Args:
        date (datetime): Instance of datetime

    Returns:
        str: Date as a string
    """
    return date.strftime(DATE_FORMAT)


def str_to_bool(cad: str) -> bool:
    """
    Converts an string to boolean

    Args:
        cad (str): string

    Returns:
        bool: string converted to boolean
    """
    return not (cad.lower() in ['false', '0'])


def to_dict(obj: Any) -> Dict:
    """
    Converts an instance to a dictionary

    Args:
        obj (Any): Object instance

    Returns:
        Dict: Instance converted to a dictionary
    """
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


def get_random_string(len_str: int = 12) -> str:
    """
    Returns a random string

    Args:
        len_str (int): Random string length desired (Default: 12)

    Returns:
        random_str (str): Random string
    """
    random_str = str(uuid.uuid4()).replace('-', '')
    return random_str[-len_str:]


def get_random_num_in_range(start, stop) -> int:
    """
    Returns a random integer between a range

    Args:
        start (int): Star range
        stop (int): Stop range

    Returns:
        random_int (int): Random integer
    """
    return random.randint(start, stop)


def get_random_indexes(size_perm: int, num_idx: int) -> List[int]:
    """
    Returns a list of n-random indexes

    Args:
        size_perm (int): Last possible index (starting in 0)
        num_idx (int): Number of random indexes wanted

    Returns:
        list_indexes (int): List of n-random indexes
      """
    return list(permutation(size_perm))[0:num_idx]
