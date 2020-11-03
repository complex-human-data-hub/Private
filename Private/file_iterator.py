from __future__ import absolute_import
from datetime import datetime
import os
import hashlib
from . import s3_helper
import logging
_log = logging.getLogger("Private")

SOURCE_TYPE_S3 = 's3'
SOURCE_TYPE_LOCAL_FILE_SYSTEM = 'localfs'
SOURCE_LOCAL_FILE_PATH_KEY = 'filepath'


class PrivateFileException(Exception):
    """
    Allows us to separate private exceptions from more generic exceptions
    """
    pass


class FileIterator:
    """
    Return a file iterator for given list of file objects. This will return the raw file content on the next call
    Ex List:
    "AudioProcessedDataFiles": [
    {
        "type": "s3"
        "bucket": "bucket_name",
        "key": "s3 key"
    },
    {
        "type": "s3"
        "bucket": "bucket_name",
        "key": "s3 key"
    }
    ]
    """

    def __init__(self, datafile_obj_list, aws_profile=None, check_files=False):
        self.file_id = -1
        if check_files:
            self.file_obj_list = self.check_files(datafile_obj_list)
        else:
            self.file_obj_list = datafile_obj_list
        self.aws_profile = aws_profile


    def __iter__(self):
        return self

    def __len__(self):
        return len(self.file_obj_list)
    
    def __next__(self):
        if self.file_id < len(self.file_obj_list) - 1:
            self.file_id += 1
            file_object = self.file_obj_list[self.file_id]
            if file_object['type'] == SOURCE_TYPE_S3:
                return s3_helper.read_file(file_object['key'], bucket_name=file_object['bucket'], aws_profile=self.aws_profile)
            elif file_object['type'] == SOURCE_TYPE_LOCAL_FILE_SYSTEM:
                try:
                    with open(file_object[SOURCE_LOCAL_FILE_PATH_KEY], 'rb') as file:
                        byte_file = file.read()
                        return byte_file
                except IOError:
                    raise PrivateFileException('Issue when reading local file ' + file_object[SOURCE_LOCAL_FILE_PATH_KEY])

            else:
                raise PrivateFileException('Unknown data source type')
        else:
            raise StopIteration

    def check_files(self, datafile_obj_list):
        file_obj_list = [] 
        print("list", type(datafile_obj_list))

        # A tuple is sometimes being sent through
        # Need to find from where
        # This is a patch, needs to be FIXED

        if isinstance(datafile_obj_list, tuple) and isinstance(datafile_obj_list[0], list):
            _log.warning("Tuple sent to FileIterator instead of list")
            datafile_obj_list = datafile_obj_list[0]

        for x in datafile_obj_list:
            if x.get('type') == 'localfs':
                if not os.path.isfile(x.get('filepath')):
                    _log.warning('Removing missing local file from FileIterator: {}'.format(x.get('filepath')))
                    continue
                elif os.path.getsize(x.get('filepath')) == 0:
                    _log.warning('Removing empty local file from FileIterator: {}'.format(x.get('filepath')))
                    continue
            file_obj_list.append(x)
        return file_obj_list


    def reset(self):
        self.file_id = -1

    def get_file_count(self):
        return len(self.file_obj_list)

    def get_file_datetime(self, file_id = 0):
        """
        Return the time information in the file under the given file ID. by default this will return the datetime of
        the first file of the sorted file list.

        :return: datetime
        """
        file_name = os.path.basename(self.file_obj_list[file_id]['key'])
        file_name_parts = file_name.split('_')
        return datetime.strptime(file_name_parts[1], '%Y%m%d%H%M%SZ')

    def get_iter_id(self):
        return hashlib.sha224(str(self.file_obj_list).encode('utf-8')).hexdigest()
