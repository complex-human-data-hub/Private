from datetime import datetime
import os

import s3_helper
SOURCE_TYPE_S3 = 's3'


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

    def __init__(self, datafile_obj_list):
        self.file_id = -1
        self.file_obj_list = datafile_obj_list

    def __iter__(self):
        return self

    def next(self):
        if self.file_id < len(self.file_obj_list) - 1:
            self.file_id += 1
            file_object = self.file_obj_list[self.file_id]
            if file_object['type'] == SOURCE_TYPE_S3:
                return s3_helper.read_file(file_object['key'], file_object['bucket'])
            else:
                raise Exception('Unknown data source type')
        else:
            raise StopIteration

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