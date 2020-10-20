from __future__ import absolute_import
from Private.demo_events import data
from Private.event import Event
from Private.reference import Reference
from Private import redis_helper

import multiprocessing as mp


class Source:
    """ 
        Class to handle retrieval of Source data for private 
        To demonstrate it's use we load moke data from demo_event.py
        To create your own source file, duplicate this file and change the 
        get_events function to load your events.

        If you customise this class, it needs all of these methods:
            get_events()
            get_demo_events()
            get_user_ids()
            load_cache()

    """
    events = None
    project_id = "999-999-999"
    shell_id = "shared"
    include_demo_events = True


    def __init__(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])


    def get_events(self):
        if self.events:
            return self.events

        # caste data items into Private Events
        self.events = list(map(Event, data)) 
        return self.events


    def get_demo_events(self):
        return self.events


    def get_user_ids(self):
        events = self.get_events()
        if not events:
            events = self.get_events()
        self.user_ids = list(set(e.UserId for e in events))
        return self.user_ids


    def load_cache(self):
        """
        Load events into cache from Source
        Private needs to have N+1 copies of the data to do privacy calculations
        For example, if we 10 participants data, then we need
        1 full copy of the data ("All")
        10 partial copies of the data for each participant

        A participant's partial copy of the data holds out they own data,
        but contains all data from the other participants
        
        """
       
        users = self.get_user_ids()
        if not 'All' in users:
            users.append('All')

        events_array = ['Events']
        if self.include_demo_events:
            events_array.append("DemoEvents")

        jobs = []
        for event_type in events_array:
            for user in users:
                opts = {
                    'user': user,
                    'events': self.events,
                    'project_id': self.project_id,
                    'shell_id': self.shell_id,
                    'event_type': event_type
                }
                jobs.append(opts)
       
        print("Number of jobs", len(jobs))
        pool = mp.Pool(processes=6)
        parallel_results = pool.map(store_cache, jobs)
        pool.close()
        pool.join()
       


def store_cache(opts):
    user = opts['user']
    user_events = opts['events']
    if user != 'All':
        user_events = [e for e in user_events if e.UserId != user]

    rk_events = redis_helper.get_redis_key(
            opts['user'],
            opts['event_type'],
            project_id=opts['project_id'],
            shell_id=opts['shell_id'])
    r = Reference(rk_events, user_events, keep_existing=False)
    print(rk_events)
    return None


if __name__ == "__main__":
    source = Source()
    user_ids = source.get_user_ids()
    print(user_ids)

    source.load_cache()



