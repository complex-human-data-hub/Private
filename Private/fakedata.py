from __future__ import print_function
from faker import Faker
from random import choice, randint, gauss, uniform, shuffle, expovariate
from datetime import timedelta, date
from pprint import PrettyPrinter


def season(date_time):
    month = date_time.month
    if 2 <= month <= 4:
        return "Autumn"
    elif 5 <= month <= 7:
        return "Winter"
    elif 8 <= month <= 10:
        return "Spring"
    else:
        return "Summer"


class FakeEvent:
    fake = Faker()
    eventTypes = ["__App__", "__SEMA__", "Button", "Gmail", "SMS", "PhoneCall"]
    placeType = ["church", "cafe"]
    weatherType = ["clear", "overcast", "cloudy", "rain"]
    moonPhaseType = ["waning_gibbous", "waxing_gibbous"]
    audioClassType = ["audio_voice", "audio_home", "audio_street", "audio_car", "audio_home"]
    seasonType = ["summer", "winter", "autumn", "spring"]
    buttonType = ["Happy", "Excited", "Tired", "Depressed"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    pp = PrettyPrinter(indent=2)

    @classmethod
    def set_locale(cls, locale):
        FakeEvent.fake = Faker(locale)

    def __init__(self, event_type=None, user_id=None, sema_participant_id=None, latitude=None, longitude=None,
                 button_type=None, date_time=None):
        if not event_type:
            event_type = choice(FakeEvent.eventTypes)
        self.type = event_type
        if user_id:
            self.UserId = user_id
        else:
            self.UserId = FakeEvent.fake.uuid4()
        if date_time:
            self.StartDateTimeLocal = date_time
        else:
            self.StartDateTimeLocal = FakeEvent.fake.date_this_decade(before_today=True,
                                                                      after_today=False)  # type: date

        if event_type == "__App__":
            self.StartDateTime = self.StartDateTimeLocal - timedelta(hours=11)
            self.EndDateTime = str(self.StartDateTime + timedelta(hours=1))
            self.StartDateTime = str(self.StartDateTime)
            self.EndDateTimeLocal = str(self.StartDateTimeLocal + timedelta(hours=1))
            self.keywords = []
            self.keywords.append(FakeEvent.months[self.StartDateTimeLocal.month - 1])
            self.keywords.append(FakeEvent.days[self.StartDateTimeLocal.weekday()])
            self.keywords.append(self.StartDateTimeLocal.year)
            self.keywords.append(season(self.StartDateTimeLocal))
            self.StartDateTimeLocal = str(self.StartDateTimeLocal)
            self.AccelerometryCount = randint(1, 12)
            self.AudioProcessedCount = randint(1, 12)

            self.BatteryCount = randint(1, 12)
            self.BatteryLevel = randint(1, 100)
            t = min(int(expovariate(1.)) + 1, len(FakeEvent.audioClassType))
            shuffle(FakeEvent.audioClassType)

            for i in range(t):
                self.keywords.append(FakeEvent.audioClassType[i])

            if randint(0, 10) != 0:  # add a few events that don't have location information
                self.Kilometers = expovariate(1.)
                self.LocationCount = randint(1, 12)
                if latitude:
                    self.latitude = latitude + gauss(0, 1)
                else:
                    self.latitude = float(FakeEvent.fake.latitude())
                if longitude:
                    self.longitude = longitude + gauss(0, 1)
                else:
                    self.longitude = float(FakeEvent.fake.longitude())
                self.address = FakeEvent.fake.address()
                self.MoonIllumination = uniform(0., 1.)
                self.MoonAge = uniform(0.0, 30.0)
                if "Summer" in self.keywords:
                    self.Temperature = gauss(28, 5)
                elif "Winter" in self.keywords:
                    self.Temperature = gauss(15, 5)
                else:
                    self.Temperature = gauss(20, 5)
                self.Weather = choice(FakeEvent.weatherType)
                self.keywords.append(self.Weather)
                self.keywords.append(choice(FakeEvent.moonPhaseType))
                if randint(0, 6) == 0:
                    self.keywords.append(choice(FakeEvent.placeType))

        elif event_type == "__SEMA__":
            self.keywords = []
            self.keywords.append("SEMA")
            if sema_participant_id:
                self.ParticipantId = sema_participant_id
            else:
                self.ParticipantId = "".join([str(randint(1, 9))] + [str(randint(0, 9)) for _ in range(8)])
            self.ParticipantTz = "Australia/Melbourne"
            self.StudyName = "DemoStudy"
            self.keywords.append(self.StudyName)
            self.StudyVersion = 1
            self.SurveyName = "Personal Experience Sampling Study"
            self.keywords.append(self.SurveyName)
            self.Trigger = "scheduled"
            expired = randint(1, 3) == 1
            if expired:
                self.keywords.append("Expired")
                self.ScheduledTs = str(self.StartDateTimeLocal)
                self.StartDateTimeLocal = self.StartDateTimeLocal + timedelta(minutes=randint(1, 110))
                self.StartDateTime = self.StartDateTimeLocal - timedelta(hours=11)
                self.StartDateTime = str(self.StartDateTime)
                self.EndDateTimeLocal = self.StartDateTimeLocal + timedelta(hours=2)
                self.EndDateTime = str(self.EndDateTimeLocal - timedelta(hours=11))
                self.EndDateTimeLocal = str(self.EndDateTimeLocal)
            else:
                self.keywords.append("Completed")
                self.ScheduledTs = str(self.StartDateTimeLocal)
                self.StartDateTimeLocal = self.StartDateTimeLocal + timedelta(minutes=randint(1, 110))
                self.StartDateTime = self.StartDateTimeLocal - timedelta(hours=11)
                self.EndDateTimeLocal = self.StartDateTimeLocal + timedelta(minutes=randint(4, 40))
                self.EndDateTime = str(self.StartDateTime - timedelta(hours=11))
                self.EndDateTimeLocal = str(self.EndDateTimeLocal)
                self.StartDateTime = str(self.StartDateTime)

                self.TotalRt = randint(1, 100000)
                if "Saturday" in self.keywords or "Sunday" in self.keywords:
                    self.Happy = randint(7, 10)
                else:
                    self.Happy = randint(1, 10)
                self.HappyRt = randint(100, 10000)
                if "Saturday" in self.keywords or "Sunday" in self.keywords:
                    self.Relaxed = randint(7, 10)
                else:
                    self.Relaxed = randint(1, 10)
                self.RelaxedRt = randint(100, 10000)
                self.Confident = randint(1, 10)
                self.ConfidentRt = randint(100, 10000)
                self.Excited = randint(1, 10)
                self.ExcitedRt = randint(100, 10000)
                self.Content = randint(1, 10)
                self.ContentRt = randint(100, 10000)
                self.Sad = randint(1, 10)
                self.SadRt = randint(100, 10000)
                if "Wednesday" in self.keywords or "Thursday" in self.keywords:
                    self.Anxious = randint(7, 10)
                else:
                    self.Anxious = randint(1, 10)
                self.AnxiousRt = randint(100, 10000)
                self.Angry = randint(1, 10)
                self.AngryRt = randint(100, 10000)
                self.Bored = randint(1, 10)
                self.BoredRt = randint(100, 10000)
                self.Disappointed = randint(1, 10)
                self.DisappointedRt = randint(100, 10000)
            self.keywords.append(FakeEvent.months[self.StartDateTimeLocal.month - 1])
            self.keywords.append(FakeEvent.days[self.StartDateTimeLocal.weekday()])
            self.keywords.append(self.StartDateTimeLocal.year)
            self.keywords.append(season(self.StartDateTimeLocal))
            self.StartDateTimeLocal = str(self.StartDateTimeLocal)

        elif event_type == "Gmail":
            self.StartDateTime = self.StartDateTimeLocal - timedelta(hours=11)
            self.EndDateTime = str(self.StartDateTime)
            self.StartDateTime = str(self.StartDateTime)
            self.EndDateTimeLocal = str(self.StartDateTimeLocal)
            self.keywords = []
            self.keywords.append(FakeEvent.months[self.StartDateTimeLocal.month - 1])
            self.keywords.append(FakeEvent.days[self.StartDateTimeLocal.weekday()])
            self.keywords.append(self.StartDateTimeLocal.year)
            self.keywords.append(season(self.StartDateTimeLocal))
            self.StartDateTimeLocal = str(self.StartDateTimeLocal)
            self.keywords.append("Gmail")
            self.Subject = FakeEvent.fake.text(20)
            self.Message = FakeEvent.fake.text(400)
            if randint(0, 1) == 0:
                self.keywords.append("Received")
                self.From = FakeEvent.fake.email()
            else:
                self.keywords.append("Sent")
                self.To = FakeEvent.fake.email()

        elif event_type == "SMS":
            self.StartDateTime = self.StartDateTimeLocal - timedelta(hours=11)
            self.EndDateTime = str(self.StartDateTime)
            self.StartDateTime = str(self.StartDateTime)
            self.EndDateTimeLocal = str(self.StartDateTimeLocal)
            self.keywords = []
            self.keywords.append(FakeEvent.months[self.StartDateTimeLocal.month - 1])
            self.keywords.append(FakeEvent.days[self.StartDateTimeLocal.weekday()])
            self.keywords.append(self.StartDateTimeLocal.year)
            self.keywords.append(season(self.StartDateTimeLocal))
            self.StartDateTimeLocal = str(self.StartDateTimeLocal)
            self.keywords.append("SMS")
            self.Text = FakeEvent.fake.text(30)
            self.Name = FakeEvent.fake.name()
            self.Number = FakeEvent.fake.phone_number()
            if randint(0, 1) == 0:
                self.keywords.append("Received")
            else:
                self.keywords.append("Sent")

        elif event_type == "Call":
            self.StartDateTime = self.StartDateTimeLocal - timedelta(hours=11)
            self.EndDateTime = str(self.StartDateTime)
            self.StartDateTime = str(self.StartDateTime)
            self.EndDateTimeLocal = str(self.StartDateTimeLocal)
            self.keywords = []
            self.keywords.append(FakeEvent.months[self.StartDateTimeLocal.month - 1])
            self.keywords.append(FakeEvent.days[self.StartDateTimeLocal.weekday()])
            self.keywords.append(self.StartDateTimeLocal.year)
            self.keywords.append(season(self.StartDateTimeLocal))
            self.StartDateTimeLocal = str(self.StartDateTimeLocal)
            self.keywords.append("Call")
            self.Duration = int(expovariate(1. / 120.))
            self.Name = FakeEvent.fake.name()
            self.Number = FakeEvent.fake.phone_number()
            if randint(0, 1) == 0:
                self.keywords.append("Received")
            else:
                self.keywords.append("Sent")

        elif event_type == "Button":
            self.StartDateTime = self.StartDateTimeLocal - timedelta(hours=11)
            self.EndDateTime = str(self.StartDateTime)
            self.StartDateTime = str(self.StartDateTime)
            self.EndDateTimeLocal = str(self.StartDateTimeLocal)
            self.keywords = []
            self.keywords.append(FakeEvent.months[self.StartDateTimeLocal.month - 1])
            self.keywords.append(FakeEvent.days[self.StartDateTimeLocal.weekday()])
            self.keywords.append(self.StartDateTimeLocal.year)
            self.keywords.append(season(self.StartDateTimeLocal))
            self.StartDateTimeLocal = str(self.StartDateTimeLocal)
            self.keywords.append("Button")
            if button_type:
                self.keywords.append(button_type)
            else:
                self.keywords.append(choice(FakeEvent.buttonType))
            self.keywords.append("Button")
            if randint(0, 10) != 0:  # add a few events that don't have location information
                if latitude:
                    self.latitude = latitude + gauss(0, 1)
                else:
                    self.latitude = float(FakeEvent.fake.latitude())
                if longitude:
                    self.longitude = longitude + gauss(0, 1)
                else:
                    self.longitude = float(FakeEvent.fake.longitude())

    def __repr__(self):
        return (FakeEvent.pp.pformat(self.__dict__))

    def hasField(self, field):
        return (field in self.__dict__.keys())


if __name__ == "__main__":
    # print "Set the locale to Australia"
    FakeEvent.set_locale(
        "en_AU")  # set the locale to Australia - this affects the kinds of values filled in for many fields (e.g. address, name ...)
    # print
    print(FakeEvent("SEMA"))
    # for eventType in FakeEvent.eventTypes:
    #  print eventType + " Event"
    #  print
    #  print FakeEvent(eventType)
    #  print

    # using list comprehensions to filter events ala examples from paper

    # someEvents = [FakeEvent() for _ in range(50)]
    # print [e.latitude for e in someEvents if e.type == "App" and e.hasField("latitude")]

    # generate many events for a small set of users

    # events = []
    # for user in range(10):
    #    i = randint(5,10)
    #    ev = FakeEvent()
    #    userid = ev.UserId
    #    RainProb = 0.3
    #    if user == 0:
    #        RainProb = 0.5
    #    events.extend([FakeEvent("App", UserId=userid, Latitude = -37.79, Longitude = 144.9, RainProb=RainProb) for _ in range(i)])
    # print events

    # NumUsers = 10
    # users = [FakeEvent.fake.uuid4() for _ in range(NumUsers)]
    #
    # Events = []
    # for user in users:
    #   SEMAParticipantId = "".join([str(randint(1,9))] + [str(randint(0,9)) for _ in range(8)])
    #   month = randint(1,12)
    #   firstday = randint(1,20)
    #   for day in range(firstday,firstday+7):
    #     for hour in range(0,24):
    #         lat = gauss(-37.814, 1.)
    #         long = gauss(144.96332, 1.5)
    #         eApp = FakeEvent(eventType="App", UserId=user, DateTime = datetime(2019, month, day, hour), Latitude=lat, Longitude=long)
    #         Events.append(eApp)
    #         if randint(0,1+abs(hour-12)) == 0:
    #             e = FakeEvent(eventType="Gmail", UserId=user, DateTime = datetime(2019, month, day, hour), Latitude=lat, Longitude=long)
    #             Events.append(e)
    #         if randint(0,4+abs(hour-12)) == 0:
    #             e = FakeEvent(eventType="SMS", UserId=user, DateTime = datetime(2019, month, day, hour), Latitude=lat, Longitude=long)
    #             Events.append(e)
    #         if randint(0,6+abs(hour-12)) == 0:
    #             e = FakeEvent(eventType="Call", UserId=user, DateTime = datetime(2019, month, day, hour), Latitude=lat, Longitude=long)
    #             Events.append(e)
    #         if randint(0,9+abs(hour-12)) == 0:
    #             if "Saturday" in eApp.keywords or "Sunday" in eApp.keywords:
    #                 e = FakeEvent(eventType="Button", buttonType = "Happy", UserId=user, DateTime = datetime(2019, month, day, hour), Latitude=lat, Longitude=long)
    #             else:
    #                 e = FakeEvent(eventType="Button", UserId=user, DateTime = datetime(2019, month, day, hour), Latitude=lat, Longitude=long)
    #             Events.append(e)
    #
    #     # SEMA data
    #
    #     semahours = [randint(9,12), randint(13,16), randint(17, 20)]
    #     for semahour in semahours:
    #         e = FakeEvent(eventType="SEMA", UserId=user, SEMAParticipantId = SEMAParticipantId, DateTime = datetime(2019, month, day, semahour), Latitude=lat, Longitude=long)
    #         Events.append(e)

    # print(Events)
