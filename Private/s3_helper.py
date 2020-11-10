from __future__ import absolute_import
import logging
import dill as pickle
import boto3
from botocore.exceptions import ClientError
from .config import s3_log_level, s3_bucket_name, config_logger
from boto3.session import Session
import traceback
import base64
import io
import gzip

# Set the s3 related logging level
logging.getLogger('boto3').setLevel(s3_log_level)
logging.getLogger('botocore').setLevel(s3_log_level)
logging.getLogger('s3transfer').setLevel(s3_log_level)
logging.getLogger('urllib3').setLevel(s3_log_level)

config_logger()
logger = logging.getLogger("s3_helper")


def save_results(key, value, bucket_name=s3_bucket_name):
    """
    Saves a result set in s3
    :param key: s3 key
    :param bucket_name: s3 bucket name
    :param value: result set as a tuple
    """
    s3 = boto3.resource('s3')

    pickle_byte_obj = pickle.dumps(value)

    # Compress teh pickled object
    fgz = io.BytesIO()
    with gzip.GzipFile(mode='wb', fileobj=fgz) as gzip_obj:
        gzip_obj.write(pickle_byte_obj)

    # Base 64 encode so we can put into redis
    b64_data = base64.b64encode(fgz.getvalue())

    s3.Object(bucket_name, key).put(Body=b64_data.decode('utf-8'))


def read_results(key, bucket_name=s3_bucket_name):
    """
    Reads a result set from s3
    :param key: s3 key
    :param bucket_name: s3 bucket name
    :return: result set as a tuple
    """
    s3 = boto3.resource('s3')
    b64_data = s3.Object(bucket_name, key).get()['Body'].read()
    gzip_obj = base64.b64decode(b64_data)
    pickle_obj = gzip.decompress(gzip_obj)
    return pickle.loads(pickle_obj)


def if_exist(key, bucket_name=s3_bucket_name):
    """
    Check if key already exist in the bucket
    :param key:s3 key
    :param bucket_name: s3 bucket name
    :return:
    """
    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket_name, key).load()
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise e
    else:
        return True


def read_file(key, bucket_name=s3_bucket_name, aws_profile=None):
    """
    Reads a file set from s3
    :param key: s3 key
    :param bucket_name: s3 bucket name
    :return: result set as a tuple
    """
    logger.debug({
        'function': 'read_file',
        'bucket': bucket_name,
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
            logger.debug({
                'error': str(err),
                'traceback': traceback.format_exc()
                })
            logger.error('Error in s3 read file')
        
        return data
    else:
        s3 = boto3.resource('s3')
        return s3.Object(bucket_name, key).get()['Body'].read()


def get_matching_keys(prefix='', bucket=s3_bucket_name):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    keys = []
    kwargs = {'Bucket': bucket, 'Prefix': prefix}
    while True:
        s3 = boto3.client('s3')
        resp = s3.list_objects_v2(**kwargs)
        if 'Contents' in resp:
            for obj in resp['Contents']:
                keys.append(obj['Key'])
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break

    return keys
