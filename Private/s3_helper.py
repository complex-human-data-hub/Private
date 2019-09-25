import logging
import dill as pickle
import boto3
from botocore.exceptions import ClientError
from config import s3_log_level, s3_bucket_name
from boto3.session import Session
import json 
from datetime import datetime

# Set the s3 related logging level
logging.getLogger('boto3').setLevel(s3_log_level)
logging.getLogger('botocore').setLevel(s3_log_level)
logging.getLogger('s3transfer').setLevel(s3_log_level)
logging.getLogger('urllib3').setLevel(s3_log_level)

def _debug(msg):
    with open('/tmp/s3-debug.log', 'a') as fp:
        if not isinstance(msg, basestring):
            msg = json.dumps(msg, indent=4, sort_keys=True, default=str)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        fp.write("[{}][{}] {}\n".format(timestamp, os.getpid(), msg ))


def save_results_s3(key, value, bucket_name=s3_bucket_name):
    """
    Saves a result set in s3
    :param key: s3 key
    :param bucket_name: s3 bucket name
    :param value: result set as a tuple
    """
    s3 = boto3.resource('s3')
    pickle_byte_obj = pickle.dumps(value)
    s3.Object(bucket_name, key).put(Body=pickle_byte_obj)


def read_results_s3(key, bucket_name=s3_bucket_name):
    """
    Reads a result set from s3
    :param key: s3 key
    :param bucket_name: s3 bucket name
    :return: result set as a tuple
    """
    s3 = boto3.resource('s3')
    return pickle.loads(s3.Object(bucket_name, key).get()['Body'].read())


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
    _debug({
        'function': 'read_file',
        'bucket': bucket_name,
        'aws_profile': aws_profile
        })
    if aws_profile:
        session = Session(
               profile_name=aws_profile.get('name'),
               region_name=aws_profile.get('region_name'))
        client = session.client('s3')
        return client.get_object(Bucket=bucket_name, Key=key).get('Body').read()
        
    else:
        s3 = boto3.resource('s3')
        return s3.Object(bucket_name, key).get()['Body'].read()
