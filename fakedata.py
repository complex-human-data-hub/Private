from faker import Faker
from random import choice, randint, gauss, uniform, shuffle, expovariate
from datetime import timedelta
from pprint import PrettyPrinter

class FakeEvent:

  fake = Faker()
  eventTypes = ["App", "Button", "Gmail", "SMS", "PhoneCall"]
  placeType = ["church", "cafe"]
  weatherType = ["clear", "overcast", "cloudy", "rain"]
  moonPhaseType = ["waning_gibbous", "waxing_gibbous"]
  audioClassType = ["audio_voice", "audio_home", "audio_street", "audio_car", "audio_home"]
  seasonType = ["summer", "winter", "autumn", "spring"]
  buttonType = ["Happy", "Excited", "Tired", "Depressed"]
  pp = PrettyPrinter(indent=2)


  @classmethod
  def setLocale(cls, locale):
    FakeEvent.fake = Faker(locale)

  def __init__(self, eventType = None, UserId = None):
    if not eventType:
      eventType = choice(FakeEvent.eventTypes)
    self.type = eventType
    if UserId:
      self.UserId = UserId
    else:
      self.UserId = FakeEvent.fake.uuid4()
    if eventType == "App":
      self.StartDateTime = FakeEvent.fake.date_this_decade(before_today=True, after_today=False)
      self.EndDateTime = str(self.StartDateTime + timedelta(hours=1))
      self.StartDateTime = str(self.StartDateTime)
      self.keywords = []
      self.keywords.append(FakeEvent.fake.month_name())
      self.keywords.append(FakeEvent.fake.day_of_week())
      self.keywords.append(FakeEvent.fake.year())
      self.keywords.append(choice(FakeEvent.seasonType))
      self.AccelerometryCount = randint(1,12)
      self.AudioProcessedCount = randint(1,12)

      self.BatteryCount = randint(1,12)
      self.BatteryLevel = randint(1,100)
      t = min(int(expovariate(1.))+1, len(FakeEvent.audioClassType))
      shuffle(FakeEvent.audioClassType)

      for i in xrange(t):
        self.keywords.append(FakeEvent.audioClassType[i])

      if randint(0, 10) != 0: # add a few events that don't have location information
        self.Kilometers = expovariate(1.)
        self.LocationCount = randint(1,12)
        self.latitude = float(FakeEvent.fake.latitude())
        self.longitude = float(FakeEvent.fake.longitude())
        self.address = FakeEvent.fake.address()
        self.MoonIllumination = uniform(0., 1.)
        self.MoonAge = uniform(0.0, 30.0)
        self.Weather = choice(FakeEvent.weatherType) 
        self.Temperature = gauss(16, 10)
        self.keywords.append(self.Weather)
        self.keywords.append(choice(FakeEvent.moonPhaseType))
        if randint(0,6) == 0:
          self.keywords.append(choice(FakeEvent.placeType))

    elif eventType == "Gmail":
      self.StartDateTime = str(FakeEvent.fake.date_this_decade(before_today=True, after_today=False))
      self.EndDateTime = self.StartDateTime 
      self.keywords = []
      self.keywords.append(FakeEvent.fake.month_name())
      self.keywords.append(FakeEvent.fake.day_of_week())
      self.keywords.append(FakeEvent.fake.year())
      self.keywords.append("Gmail")
      self.Subject = FakeEvent.fake.text(20)
      self.Message = FakeEvent.fake.text(400)
      if randint(0,1) == 0:
        self.keywords.append("Received")
        self.From = FakeEvent.fake.email()
      else:
        self.keywords.append("Sent")
        self.To = FakeEvent.fake.email()

    elif eventType == "SMS":
      self.StartDateTime = str(FakeEvent.fake.date_this_decade(before_today=True, after_today=False))
      self.EndDateTime = self.StartDateTime 
      self.keywords = []
      self.keywords.append(FakeEvent.fake.month_name())
      self.keywords.append(FakeEvent.fake.day_of_week())
      self.keywords.append(FakeEvent.fake.year())
      self.keywords.append("SMS")
      self.Text = FakeEvent.fake.text(30)
      self.Name = FakeEvent.fake.name()
      self.Number = FakeEvent.fake.phone_number()
      if randint(0,1) == 0:
        self.keywords.append("Received")
      else:
        self.keywords.append("Sent")

    elif eventType == "PhoneCall":
      self.StartDateTime = str(FakeEvent.fake.date_this_decade(before_today=True, after_today=False))
      self.EndDateTime = self.StartDateTime 
      self.keywords = []
      self.keywords.append(FakeEvent.fake.month_name())
      self.keywords.append(FakeEvent.fake.day_of_week())
      self.keywords.append(FakeEvent.fake.year())
      self.keywords.append("SMS")
      self.Duration = int(expovariate(1./120.))
      self.Name = FakeEvent.fake.name()
      self.Number = FakeEvent.fake.phone_number()
      if randint(0,1) == 0:
        self.keywords.append("Received")
      else:
        self.keywords.append("Sent")

    elif eventType == "Button":
      self.StartDateTime = str(FakeEvent.fake.date_this_decade(before_today=True, after_today=False))
      self.EndDateTime = self.StartDateTime 
      self.keywords = []
      self.keywords.append(FakeEvent.fake.month_name())
      self.keywords.append(FakeEvent.fake.day_of_week())
      self.keywords.append(FakeEvent.fake.year())
      self.keywords.append(choice(FakeEvent.buttonType))
      if randint(0, 10) != 0: # add a few events that don't have location information
        self.latitude = float(FakeEvent.fake.latitude())
        self.longitude = float(FakeEvent.fake.longitude())

  def __repr__(self):
    return(FakeEvent.pp.pformat(self.__dict__))

  def hasField(self, field):
    return(field in self.__dict__.keys())



if __name__ == "__main__":
  print "Set the locale to Australia"
  FakeEvent.setLocale("en_AU")   # set the locale to Australia - this affects the kinds of values filled in for many fields (e.g. address, name ...)
  print 

  #for eventType in FakeEvent.eventTypes:
  #  print eventType + " Event"
  #  print
  #  print FakeEvent(eventType)
  #  print

  # using list comprehensions to filter events ala examples from paper

  someEvents = [FakeEvent() for _ in xrange(50)]
  #print [e.latitude for e in someEvents if e.type == "App" and e.hasField("latitude")]

  # generate many events for a small set of users

  events = []
  for user in xrange(20):
    i = randint(10,25)
    ev = FakeEvent()
    userid = ev.UserId
    events.extend([FakeEvent(UserId=userid) for _ in xrange(i)])
  print events
 

