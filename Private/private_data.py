from __future__ import absolute_import
from .demo_events import Events, DemoEvents

class Source:
    """ 
        Class to handle retrieval of data for private 
        If you customise this class, it should have both of these methods:
            get_events(opts)

            get_demo_events(opts)

    """

    def __init__(*args, **kwargs):
        pass

    def get_events(self, opts=None):
        return Events

    def get_demo_events(self, opts=None):
        return DemoEvents


