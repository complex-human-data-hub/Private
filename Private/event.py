import pprint
from file_iterator import FileIterator

pp = pprint.PrettyPrinter()

class Event:
    aws_profile = None
    def __init__(self, mydict, aws_profile=None):
        self.__dict__ = mydict
        self.convert_data_files()
        self.aws_profile = aws_profile

    def __repr__(self):
        return pp.pformat(self.__dict__)

    def hasField(self, fieldname):
        return fieldname in self.__dict__.keys()

    def __str__(self):
        return pp.pformat(self.__dict__)

    def convert_data_files(self):
        for key in self.__dict__.keys():
            if key.endswith("DataFiles"):
                self.__dict__[key + "Itr"] = FileIterator(self.__dict__[key], aws_profile=self.aws_profile)
