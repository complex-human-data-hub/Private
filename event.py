import pprint

pp = pprint.PrettyPrinter()

class Event:

  def __init__(self, mydict):
    self.__dict__ = mydict

  def __repr__(self):
    return pp.pformat(self.__dict__)

  def hasField(self, fieldname):
    return fieldname in self.__dict__.keys()

  def __str__(self):
    return pp.pformat(self.__dict__)

