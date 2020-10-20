import io
import reprlib

import numpy
import Private.redis_helper
import Private.disk_helper
import Private.s3_helper
from Private.config import s3_integration


class Reference:
    key = None
    display_value = None
    helper = Private.s3_helper if s3_integration else Private.disk_helper

    def __init__(self, key, value, keep_existing=False):
        self.key = key
        if not keep_existing:
            self.helper.save_results(self.key, value)
            # invalidate cache
            Private.redis_helper.delete_results(self.key)
        self.display_value = self.get_display_value(value)

    def value(self):
        if Private.redis_helper.if_exist(self.key):
            return Private.redis_helper.read_results(self.key)
        else:
            value = self.helper.read_results(self.key)
            Private.redis_helper.save_results(self.key, value)
            return value

    @staticmethod
    def get_display_value(value):
        formatter_string = "%%.%sf" % 3
        if type(value) == io.BytesIO:  # write image to file
            return "[PNG Image]"
        elif type(value) == numpy.ndarray:
            s = value.shape
            return "[" * len(s) + formatter_string % value.ravel()[
                0] + " ... " + formatter_string % value.ravel()[-1] + "]" * len(s)
        elif type(value) == float or type(value) == numpy.float64:
            return str((formatter_string % value))
        else:
            return reprlib.repr(value).replace('\n', '')



