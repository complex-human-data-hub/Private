from __future__ import absolute_import
import dill as pickle
from .config import redis_server_ip
import redis
import base64
import io
import gzip


def get_project_id(key):
    """
    Get project id from a key, this assumes the key is created using get_redis_key function
    :param key: redis key
    :return: project_id (String)
    """
    project_id = key.split("/")[0]
    return project_id


def get_redis_key(user_id, variable_name, project_id="proj1", shell_id="shell1"):
    """
    Returns the redis key based on a agreed format, should use this method whenever we need to build a redis key

    :param user_id: user_id, in data
    :param variable_name: variable name
    :param project_id: project id
    :param shell_id: shell id
    :return: redis key (String)
    """
    return f"{project_id}/{shell_id}/{user_id}_{variable_name}"


def save_results(key, value, server_ip=redis_server_ip):
    """
    Saves a result set in redis

    :param key: redis key
    :param value: result set as a tuple
    :param server_ip: redis server IP
    """
    pickle_byte_obj = pickle.dumps(value)

    # Compress teh pickled object
    fgz = io.BytesIO()
    with gzip.GzipFile(mode='wb', fileobj=fgz) as gzip_obj:
        gzip_obj.write(pickle_byte_obj)

    # Base 64 encode so we can put into redis
    b64_data = base64.b64encode(fgz.getvalue())

    # Add key/value to redis
    r = redis.Redis(host=server_ip)
    r.set(key, b64_data.decode('utf-8'))

    # Add project and key to lookup table used by get_matching_keys()
    project_id = get_project_id(key)
    r.sadd(project_id, key)


def read_results(key, server_ip=redis_server_ip):
    """
    Reads a result set from redis

    :param key: redis key
    :param server_ip: redis server IP
    :return: result set as a tuple
    """
    r = redis.Redis(host=server_ip)
    b64_data = r.get(key).decode('utf-8')
    gzip_obj = base64.b64decode(b64_data)
    pickle_obj = gzip.decompress(gzip_obj)
    return pickle.loads(pickle_obj)


def if_exist(key, server_ip=redis_server_ip):
    """
    Check if key already exist in the store

    :param key:redis key
    :param server_ip: redis server IP
    :return:
    """
    r = redis.Redis(host=server_ip)
    return r.exists(key)


def get_matching_keys(prefix='', server_ip=redis_server_ip):
    """
    Generate the keys in an S3 bucket.

    :param prefix: Only fetch keys that start with this prefix (optional).
    :param server_ip: redis server IP
    """
    r = redis.Redis(host=server_ip)
    return list(map(lambda x: x.decode('utf-8'), r.smembers(prefix)))


def delete_user_keys(project_id, shell_id, server_ip=redis_server_ip):
    """
    Delete the redis keys under a given prefix

    :param project_id: redis key prefix
    :param shell_id: shell id
    :param server_ip: redis server IP
    """
    r = redis.Redis(host=server_ip)
    for key in r.scan_iter(f"{project_id}/{shell_id}/*"):
        r.delete(key)
