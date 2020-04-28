from __future__ import absolute_import
import logging
import dill as pickle
import boto3
from botocore.exceptions import ClientError
from .config import s3_log_level, s3_bucket_name, redis_server_ip
from boto3.session import Session
import json 
from datetime import datetime
import os 
import traceback 
import redis 
import base64
import io
import gzip

# Set the s3 related logging level
logging.getLogger('boto3').setLevel(s3_log_level)
logging.getLogger('botocore').setLevel(s3_log_level)
logging.getLogger('redis').setLevel(s3_log_level)
logging.getLogger('urllib3').setLevel(s3_log_level)

def _debug(msg):
    with open('/tmp/redis-debug.log', 'a') as fp:
        if not isinstance(msg, str):
            msg = json.dumps(msg, indent=4, sort_keys=True, default=str)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        fp.write("[{}][{}] {}\n".format(timestamp, os.getpid(), msg ))

def get_project_id(key):
    project_id = key.split("/")[0]
    return project_id


def get_redis_key(user_id, variable_name, project_id="proj1", shell_id="shell1"):
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
    :param host_ip: redis server ip
    :return: result set as a tuple
    """
    r = redis.Redis(host=server_ip)
    b64_data = r.get(key).decode('utf-8')
    gzip_obj = base64.b64decode(b64_data)
    pickle_obj = gzip.decompress(gzip_obj)
    return pickle.loads(pickle_obj)

    
    s3 = boto3.resource('s3')
    return pickle.loads(s3.Object(bucket_name, key).get()['Body'].read())


def if_exist(key, server_ip=redis_server_ip):
    """
    Check if key already exist in the store
    :param key:redis key
    :param server_ip: redis server IP
    :return:
    """
    r = redis.Redis(host=server_ip)
    return r.exists(key)


def read_file(key, bucket_name=s3_bucket_name, aws_profile=None):
    """
    Reads a file set from s3
    :param key: s3 key
    :param bucket_name: s3 bucket name
    :return: result set as a tuple
    """
    aws_profile = {
        'name': 'ume', 
        'region_name': 'us-west-1'
            }
    
    _debug({
        'function': 'read_file',
        'bucket': bucket_name,
        'key': key,
        'aws_profile': aws_profile
        })
    if aws_profile:
        data = None
        try:
            session = Session(
                   profile_name=aws_profile.get('name'),
                   region_name=aws_profile.get('region_name'))
            client = session.client('s3')
            theobject = client.get_object(Bucket=bucket_name, Key=key)
            body = theobject["Body"]
            data = body.read()
        except Exception as err:
            _debug({
                'error': str(err),
                'traceback': traceback.format_exc()
                })
        
        return data
    else:
        s3 = boto3.resource('s3')
        return s3.Object(bucket_name, key).get()['Body'].read()



def get_matching_keys(prefix='', server_ip=redis_server_ip):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    r = redis.Redis(host=server_ip) 
    return list(map(lambda x: x.decode('utf-8'), r.smembers(prefix)))

