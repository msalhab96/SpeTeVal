from .exceptions import FileNotExist
from functools import wraps
import os


def check_file_existance(func):
    @wraps(func)
    def wrapper(file_path, *args, **kwargs):
        assert os.path.exists(file_path), FileNotExist(file_path)
        return func(file_path, *args, **kwargs)
    return wrapper
