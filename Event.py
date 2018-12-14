def Normal(mu, sigma, length):
  return(numpy.random.normal(mu, sigma, length))

class Event:

  def __init__(self, mydict):
    self.__dict__ = mydict

  def __repr__(self):
    return repr(self.__dict__)

  def hasField(self, fieldname):
    return fieldname in self.__dict__.keys()

