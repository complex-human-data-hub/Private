from __future__ import absolute_import
import json
from . import s3_helper
from .event import Event


class EventsIterator:
    """
    Returns the event iterator for given list of s3 keys (files). This assumes that the file are in the JSON format
    """

    def __init__(self, datafile_list):
        self.i = -1
        self.file_id = 0
        self.file_list = datafile_list
        self.data = s3_helper.read_file(self.file_list[self.file_id])
        self.objects = json.loads(self.data)

    def __iter__(self):
        return self

    def next(self):
        self.i += 1
        if self.i < len(self.objects):
            event = Event(self.objects[self.i])
        else:
            if self.file_id < len(self.file_list) - 1:
                self.file_id += 1
                self.data = s3_helper.read_file(self.file_list[self.file_id])
                self.objects = json.loads(self.data)
                self.i = 0
                event = Event(self.objects[self.i])
            else:
                raise StopIteration
        return event
