import io
import reprlib
import numpy
from Private.cache_helper import CacheHelperFactory
from Private.graph_constants import cache_type_redis, cache_type_s3


class Reference:
    """
    This is the generic reference object that need to be extended to different data sources
    """
    key = None
    display_value = None
    helper = None

    def __init__(self, ref_type, key, value, keep_existing, keep_value=False):
        self.key = key
        self.ori_value = None
        self.helper = CacheHelperFactory.get_helper(ref_type)
        if keep_value:
            self.ori_value = value
        if not keep_existing:
            self.helper.save_results(key, value)
        self.display_value = self.get_display_value(value)

    def empty_value(self):
        self.ori_value = None

    def value(self):
        if not self.ori_value:
            self.ori_value = self.helper.read_results(self.key)
        return self.ori_value

    @staticmethod
    def get_display_value(value):
        formatter_string = "%%.%sf" % 3
        if type(value) == io.BytesIO:
            return "[PNG Image]"
        elif type(value) == numpy.ndarray:
            s = value.shape
            return "[" * len(s) + formatter_string % value.ravel()[
                0] + " ... " + formatter_string % value.ravel()[-1] + "]" * len(s)
        elif type(value) == float or type(value) == numpy.float64:
            return str((formatter_string % value))
        else:
            return reprlib.repr(value).replace('\n', '')


class S3Reference(Reference):
    def __init__(self, key, value, keep_existing=False, keep_value=False):
        super().__init__(cache_type_s3, key, value, keep_existing, keep_value)


class RedisReference(Reference):
    def __init__(self, key, value, keep_existing=False, keep_value=False):
        super().__init__(cache_type_redis, key, value, keep_existing, keep_value)


class ReferenceFactory:
    @staticmethod
    def get_reference(ref_type, key, value, keep_existing=False, keep_value=False):
        if ref_type == cache_type_redis:
            return RedisReference(key, value, keep_existing, keep_value)
        elif ref_type == cache_type_s3:
            return S3Reference(key, value, keep_existing, keep_value)


