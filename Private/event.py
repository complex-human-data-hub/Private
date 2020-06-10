from __future__ import absolute_import
import pprint
from .file_iterator import FileIterator

pp = pprint.PrettyPrinter()


class Event:
    aws_profile = None

    def __init__(self, mydict, aws_profile=None):
        self.__dict__ = mydict
        self.convert_data_files(aws_profile)

    def __repr__(self):
        return pp.pformat(self.__dict__)

    def hasField(self, fieldname):
        return fieldname in self.__dict__.keys()

    def __str__(self):
        return pp.pformat(self.__dict__)

    def convert_data_files(self, aws_profile):
        for key in list(self.__dict__):
            if key.endswith("DataFiles") and not key.startswith('has'):
                self.__dict__[key + "Itr"] = FileIterator(self.__dict__[key], aws_profile=aws_profile)
                del self.__dict__[key]

    def __getitem__(self, item):
        return getattr(self, item)
