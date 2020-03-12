import io
import reprlib

import numpy
import Private.redis_helper


class RedisReference:
    redis_key = None
    display_value = None

    def __init__(self, redis_key, value, keep_existing=False):
        self.redis_key = redis_key
        if not keep_existing:
            Private.redis_helper.save_results(redis_key, value)
        self.display_value = self.get_display_value(value)

    def value(self):
        return Private.redis_helper.read_results(self.redis_key)

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



