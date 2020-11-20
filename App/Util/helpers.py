import json
import random
import uuid
import time
from datetime import datetime
from typing import Any, Dict, List
from numpy.random import permutation
from App.Util.constants import DATE_FORMAT


def str_to_timestamp(date: str):
    date_formats = (DATE_FORMAT, DATE_FORMAT.replace('-', '/'), DATE_FORMAT.replace('-', '.'))
    for fmt in date_formats:
        try:
            dt_object = datetime.strptime(date, fmt).timetuple()
            return time.mktime(dt_object)
        except ValueError:
            pass
        raise ValueError(f"No valid date format found. Use the next format: '{DATE_FORMAT}'.")


def timestamp_to_str(timestamp: int):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime(DATE_FORMAT)


def datetime_to_str(date: datetime):
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
