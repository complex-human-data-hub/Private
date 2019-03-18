import pickle
import boto3

# s3 config
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