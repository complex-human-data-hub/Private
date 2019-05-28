from datetime import datetime
import os

import s3_helper


class FileIterator:
    """
    Return a file iterator for given list of s3 keys. This will return the raw file content on the next call
    """
    def __init__(self, datafile_list):
        self.file_id = -1
        self.file_list = datafile_list
        self.file_list.sort()

    def __iter__(self):
        return self

    def next(self):
        if self.file_id < len(self.file_list) - 1:
            self.file_id += 1
            return s3_helper.read_file(self.file_list[self.file_id])
        else:
            raise StopIteration

    def get_file_count(self):
        return len(self.file_list)

    def get_file_datetime(self, file_id = 0):
        """
        Return the time information in the file under the given file ID. by default this will return the datetime of
        the first file of the sorted file list.

        :return: datetime
        """
        file_name = os.path.basename(self.file_list[file_id])
        file_name_parts = file_name.split('_')
        return datetime.strptime(file_name_parts[1], '%Y%m%d%H%M%SZ')