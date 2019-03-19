import dill as pickle
import boto3

# s3 config
from botocore.exceptions import ClientError

s3_bucket_name = 'chdhprivate'


def save_results_s3(key, value):
    """
    Saves a result set in s3
    :param key: s3 key
    :param value: result set as a tuple
    """
    s3 = boto3.resource('s3')
    pickle_byte_obj = pickle.dumps(value)
    s3.Object(s3_bucket_name, key).put(Body=pickle_byte_obj)


def read_results_s3(key):
    """
    Reads a result set from s3
    :param key: s3 key
    :return: result set as a tuple
    """
    s3 = boto3.resource('s3')
    return pickle.loads(s3.Object(s3_bucket_name, key).get()['Body'].read())


def if_exist(key):
    """
    Check if key already exist in the bucket
    :param key:
    :return:
    """
    s3 = boto3.resource('s3')
    try:
        s3.Object(s3_bucket_name, key).load()
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise e
    else:
        return True
