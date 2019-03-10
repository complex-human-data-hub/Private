from fakedata import FakeEvent

from demo_events import data

users = set([e["UserId"] for e in data])

print users


