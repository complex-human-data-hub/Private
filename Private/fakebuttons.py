from __future__ import print_function
from __future__ import absolute_import
from .fakedata import FakeEvent

from .demo_events import data

users = set([e["UserId"] for e in data])

print(users)


