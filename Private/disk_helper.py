import os

import dill as pickle
from .config import data_location
import base64
import io
import gzip
from pathlib import Path


def save_results(key, value, location=data_location):
    """
    Saves a result set in disk

    :param key: redis key
    :param value: result set as a tuple
    :param location: location of data in disk
    """
    pickle_byte_obj = pickle.dumps(value)

    # Compress teh pickled object
    fgz = io.BytesIO()
    with gzip.GzipFile(mode='wb', fileobj=fgz) as gzip_obj:
        gzip_obj.write(pickle_byte_obj)

    # Base 64 encode so we can put into redis
    b64_data = base64.b64encode(fgz.getvalue())

    # Save data to disk
    folder = '/'.join((location + key).split('/')[:-1])
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(location + key, 'w+') as f:
        f.write(b64_data.decode('utf-8'))


def read_results(key, location=data_location):
    """
    Reads a result set from disk

    :param key: redis key
    :param location: location of data in disk
    :return: result set as a tuple
    """
    with open(location + key, 'r+', encoding="utf-8") as f:
        b64_data = f.read()
    gzip_obj = base64.b64decode(b64_data)
    pickle_obj = gzip.decompress(gzip_obj)
    return pickle.loads(pickle_obj)


def get_matching_keys(prefix='', location=data_location):
    """
    list all the files in the folder.

    :param prefix: Only fetch keys that start with this prefix (optional).
    :param location: location of data in disk
    """
    directory = location + prefix
    file_names = []

    for root, directories, files in os.walk(directory):
        for file_name in files:
            filepath = os.path.join(root, file_name)
            file_names.append(filepath[len(location):])

    return file_names

