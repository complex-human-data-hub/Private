from __future__ import absolute_import

import boto3
import redis
import base64
import io
import gzip
import dill as pickle
from botocore.exceptions import ClientError
from .config import redis_server_ip, s3_bucket_name, s3_log_level
from boto3.session import Session
from Private.graph_constants import cache_type_redis, cache_type_s3

import logging
from abc import abstractmethod


class CacheHelper:

    @staticmethod
    def get_project_id(key):
        """
        Get project id from a key, this assumes the key is created using get_redis_key function
        :param key: redis key
        :return: project_id (String)
        """
        project_id = key.split("/")[0]
        return project_id

    @staticmethod
    def get_key(user_id, variable_name, project_id="proj1", shell_id="shell1"):
        """
        Returns the redis key based on a agreed format, should use this method whenever we need to build a redis key

        :param user_id: user_id, in data
        :param variable_name: variable name
        :param project_id: project id
        :param shell_id: shell id
        :return: key (String)
        """
        return f"{project_id}/{shell_id}/{user_id}_{variable_name}"

    @abstractmethod
    def save_results(self, key, value):
        pass

    @abstractmethod
    def read_results(self, key):
        pass

    @abstractmethod
    def if_exist(self, key):
        pass

    @abstractmethod
    def get_matching_keys(self, prefix=''):
        pass


class RedisHelper(CacheHelper):
    server_ip = None

    def __init__(self, server_ip):
        super().__init__()
        self.server_ip = server_ip

    def save_results(self, key, value):
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
        r = redis.Redis(host=self.server_ip)
        r.set(key, b64_data.decode('utf-8'))

        # Add project and key to lookup table used by get_matching_keys()
        project_id = self.get_project_id(key)
        r.sadd(project_id, key)

    def read_results(self, key):
        """
        Reads a result set from redis

        :param key: redis key
        :param server_ip: redis server IP
        :return: result set as a tuple
        """
        r = redis.Redis(host=self.server_ip)
        b64_data = r.get(key).decode('utf-8')
        gzip_obj = base64.b64decode(b64_data)
        pickle_obj = gzip.decompress(gzip_obj)
        return pickle.loads(pickle_obj)

    def if_exist(self, key):
        """
        Check if key already exist in the store

        :param key:redis key
        :param server_ip: redis server IP
        :return:
        """
        r = redis.Redis(host=self.server_ip)
        return r.exists(key)

    def get_matching_keys(self, prefix=''):
        """
        Generate the keys in an S3 bucket.

        :param prefix: Only fetch keys that start with this prefix (optional).
        :param server_ip: redis server IP
        """
        r = redis.Redis(host=self.server_ip)
        return list(map(lambda x: x.decode('utf-8'), r.smembers(prefix)))

    def delete_user_keys(self, project_id, shell_id):
        """
        Delete the redis keys under a given prefix

        :param project_id: redis key prefix
        :param shell_id: shell id
        :param server_ip: redis server IP
        """
        r = redis.Redis(host=self.server_ip)
        for key in r.scan_iter(f"{project_id}/{shell_id}/*"):
            r.delete(key)


class S3Helper(CacheHelper):
    bucket_name = None

    def __init__(self, bucket_name):
        super().__init__()
        logging.getLogger('boto3').setLevel(s3_log_level)
        logging.getLogger('botocore').setLevel(s3_log_level)
        logging.getLogger('s3transfer').setLevel(s3_log_level)
        logging.getLogger('urllib3').setLevel(s3_log_level)
        self.bucket_name = bucket_name

    def save_results(self, key, value):
        """
        Saves a result set in s3
        :param key: s3 key
        :param bucket_name: s3 bucket name
        :param value: result set as a tuple
        """
        s3 = boto3.resource('s3')
        pickle_byte_obj = pickle.dumps(value)
        s3.Object(self.bucket_name, key).put(Body=pickle_byte_obj)

    def read_results(self, key):
        """
        Reads a result set from s3
        :param key: s3 key
        :param bucket_name: s3 bucket name
        :return: result set as a tuple
        """
        s3 = boto3.resource('s3')
        return pickle.loads(s3.Object(self.bucket_name, key).get()['Body'].read())

    def if_exist(self, key, bucket_name=s3_bucket_name):
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

    def read_file(self, key, aws_profile=None):
        """
        Reads a file set from s3
        :param key: s3 key
        :param aws_profile: aws profile
        :return: result set as a tuple
        """
        if aws_profile:
            data = None
            try:
                session = Session(
                    profile_name=aws_profile.get('name'),
                    region_name=aws_profile.get('region_name'))
                client = session.client('s3')
                theobject = client.get_object(Bucket=self.bucket_name, Key=key)
                body = theobject["Body"]
                data = body.read()
            except Exception as err:
                return err

            return data
        else:
            s3 = boto3.resource('s3')
            return s3.Object(self.bucket_name, key).get()['Body'].read()

    def get_all_s3_keys(self):
        """Get a list of all keys in an S3 bucket."""
        keys = []

        kwargs = {'Bucket': self.bucket_name}
        while True:
            s3 = boto3.client('s3')
            resp = s3.list_objects_v2(**kwargs)
            for obj in resp['Contents']:
                keys.append(obj['Key'])

            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

        return keys

    def get_matching_keys(self, prefix=''):
        """
        Generate the keys in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param prefix: Only fetch keys that start with this prefix (optional).
        :param suffix: Only fetch keys that end with this suffix (optional).
        """
        keys = []
        kwargs = {'Bucket': self.bucket_name, 'Prefix': prefix}
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



class CacheHelperFactory:
    @staticmethod
    def get_helper(ref_type):
        if ref_type == cache_type_redis:
            return RedisHelper(redis_server_ip)
        elif ref_type == cache_type_s3:
            return S3Helper(s3_bucket_name)

