import s3_helper


class FileIterator:
    def __init__(self, datafile_list):
        self.file_id = -1
        self.file_list = datafile_list

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

