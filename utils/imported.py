import importlib
import os


def import_packages(filename=None, filepath=None) -> None:
    full_file_path = os.path.join(filepath, filename)
    assert os.path.exists(full_file_path), f" File <{full_file_path}> is not found ... "
    return importlib.import_module(f'{filepath}.' + filename).__dict__[filename]

