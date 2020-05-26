from __future__ import print_function
from faker import Faker
from random import choice, randint, gauss, uniform, shuffle, expovariate
from datetime import timedelta, date, datetime
from pprint import PrettyPrinter


def season(date_time):
    var_month = date_time.month
    if 2 <= var_month <= 4:
        return "Autumn"
    elif 5 <= var_month <= 7:
        return "Winter"
    elif 8 <= var_month <= 10:
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
        self.id = FakeEvent.fake.uuid4()
        start_date_time_local = self.StartDateTimeLocal

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
            self.Name = None
            self.BatteryDataFiles = [
                {
                    "type": "localfs",
                    "filepath": "/data/battery_20190616140000Z_ffc4284d-7aa3-415e-a3dd-b9125c556388.csv"
                }],
            self.StreetViewThumbnail = "https://s3-us-west-1.amazonaws.com/unforgettable-dev-usw1/userhome/" \
                 "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/2019/06/08/streetview_thumb_4a28b74a-1608-448b-b8e4-7831b6d5f858.jpeg"
            self.hasAudioProcessedDataFiles = True
            self.AudioProcessedDataFiles = [
                {
                    "type": "localfs",
                    "filepath": "/data/audio_20190616141007Z_28868a90-f7bd-4ad5-9264-e35c9b36e109.mfcc"
                },
                {
                    "type": "localfs",
                    "filepath": "/data/audio_20190616142007Z_53f62074-5bc5-4902-9f5e-841d25e3684f.mfcc"
                },
                {
                    "type": "localfs",
                    "filepath": "/data/audio_20190616143008Z_020d149b-8e99-485f-9337-7b43d9096169.mfcc"
                }]
            self.hasAccelerometryDataFiles = True
            self.AccelerometryDataFiles = [
                {
                    "type": "localfs",
                    "filepath": "/data/accel_20190616141000Z_b3944396-b87e-4b29-9acc-a05d00ed868f.bin"
                },
                {
                    "type": "localfs",
                    "filepath": "/data/accel_20190616142000Z_0983b4e0-8cab-4d29-bd78-e33278c0095f.bin"
                },
                {
                    "type": "localfs",
                    "filepath": "/data/accel_20190616143001Z_1503e036-bd86-4a29-87e3-b1ff73ec7929.bin"
                }]
            self.StreetViewImage = "https://s3-us-west-1.amazonaws.com/unforgettable-dev-usw1/userhome/" \
                "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/2019/06/08/streetview_full_4a28b74a-1608-448b-b8e4-7831b6d5f858.jpeg"
            self.UserImages = []
            self.hasGpsLocations = True
            self.GpsLocations = [
                {
                    "lat": -37.7929697,
                    "time_local": "2019-06-17 00:01:25",
                    "lon": 144.9888915,
                    "time": "2019-06-16 14:01:25Z"
                },
                {
                    "lat": -37.7929776,
                    "time_local": "2019-06-17 00:12:15",
                    "lon": 144.988879,
                    "time": "2019-06-16 14:12:15Z"
                },
                {
                    "lat": -37.792762010358274,
                    "time_local": "2019-06-17 00:22:17",
                    "lon": 144.98914819210768,
                    "time": "2019-06-16 14:22:17Z"
                },
                {
                    "lat": -37.7930073,
                    "time_local": "2019-06-17 00:32:12",
                    "lon": 144.9889067,
                    "time": "2019-06-16 14:32:12Z"
                },
                {
                    "lat": -37.7929881,
                    "time_local": "2019-06-17 00:42:15",
                    "lon": 144.9889107,
                    "time": "2019-06-16 14:42:15Z"
                },
                {
                    "lat": -37.7929881,
                    "time_local": "2019-06-17 00:52:13",
                    "lon": 144.9889107,
                    "time": "2019-06-16 14:52:13Z"
                }]
            self.GpsDataFiles = [
                {
                    "type": "localfs",
                    "filepath": "/data/location_ffc4284d-7aa3-415e-a3dd-b9125c556388.csv"
                }]
            self.Suggestions = []
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
            expired = randint(1, 3) == 1
            created_ts = start_date_time_local + timedelta(minutes=randint(1, 110))
            completed_ts = start_date_time_local + timedelta(hours=2)

            if sema_participant_id:
                self.ParticipantId = sema_participant_id
            else:
                self.ParticipantId = "".join([str(randint(1, 9))] + [str(randint(0, 9)) for _ in range(8)])
            self.ParticipantTz = "Australia/Melbourne"
            self.ExportTz = "Australia/Melbourne"

            self.StudyName = "DemoStudy"
            self.StudyId = "WKjsuNhsa"
            self.StudyVersion = 1
            self.SurveyName = "Personal Experience Sampling Study"
            self.SurveyId = "n8_i_jUrMl"
            self.Trigger = "scheduled"

            self.ScheduledTs = str(start_date_time_local)
            self.ScheduledUtcTs = str(to_utc(start_date_time_local))

            self.StartDateTimeLocal = str(created_ts)
            self.StartDateTime = str(to_utc(created_ts))

            self.EndDateTimeLocal = str(completed_ts)
            self.EndDateTime = str(to_utc(completed_ts))

            self.keywords = []
            self.keywords.append("SEMA")
            self.keywords.append(self.StudyName)
            self.keywords.append(self.SurveyName)
            self.keywords.append(FakeEvent.months[start_date_time_local.month - 1])
            self.keywords.append(FakeEvent.days[start_date_time_local.weekday()])
            self.keywords.append(start_date_time_local.year)
            self.keywords.append(season(start_date_time_local))

            if expired:
                self.keywords.append("Expired")
                self.keywords.append("uncompleted")

                self.ExpiredTs = str(completed_ts)
                self.ExpiredUtcTs = str(to_utc(completed_ts))
            else:
                self.keywords.append("Completed")

                self.CreatedTs = str(created_ts)
                self.CreatedUtcTs = str(to_utc(created_ts))

                self.StartedTs = str(created_ts)
                self.StartedUtcTs = str(to_utc(created_ts))

                self.CompletedTs = str(completed_ts)
                self.CompletedUtcTs = str(to_utc(completed_ts))

                self.UploadedTs = str(completed_ts)
                self.UploadedUtcTs = str(to_utc(completed_ts))

                self.TotalRt = randint(1, 100000)
                self.Happy = randint(1, 10)
                self.Relaxed = randint(1, 10)
                self.HappyRt = randint(100, 10000)
                self.RelaxedRt = randint(100, 10000)
                self.Confident = randint(1, 10)
                self.ConfidentRt = randint(100, 10000)
                self.Excited = randint(1, 10)
                self.ExcitedRt = randint(100, 10000)
                self.Content = randint(1, 10)
                self.ContentRt = randint(100, 10000)
                self.Sad = randint(1, 10)
                self.SadRt = randint(100, 10000)
                self.Anxious = randint(1, 10)
                self.AnxiousRt = randint(100, 10000)
                self.Angry = randint(1, 10)
                self.AngryRt = randint(100, 10000)
                self.Bored = randint(1, 10)
                self.BoredRt = randint(100, 10000)
                self.Disappointed = randint(1, 10)
                self.DisappointedRt = randint(100, 10000)
                self.Irritable = randint(1, 10)
                self.IrritableRt = randint(100, 10000)
                self.Location = randint(1, 100)
                self.LocationRt = randint(1000, 100000)
                # Special Patterns
                if "Saturday" in self.keywords or "Sunday" in self.keywords:
                    self.Happy = randint(7, 10)
                    self.Relaxed = randint(7, 10)
                    self.Bored = randint(5, 10)
                if "Wednesday" in self.keywords or "Thursday" in self.keywords:
                    self.Anxious = randint(7, 10)
                if "Monday" in self.keywords or "Tuesday" in self.keywords:
                    self.Sad = randint(5, 10)
                    self.Angry = randint(5, 10)

                self.Suggestions = []

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
        return FakeEvent.pp.pformat(self.__dict__)

    def has_field(self, field):
        return field in self.__dict__.keys()


def to_utc(date_time):
    return date_time - timedelta(hours=11)


def write_file(events):
    with open('test-events.py', 'w') as fp:
        fp.write(str(events))


if __name__ == "__main__":
    # set the locale to Australia - this affects the kinds of values filled in for many fields (e.g. address, name ...)
    FakeEvent.set_locale("en_AU")

    NumUsers = 10
    users = [FakeEvent.fake.uuid4() for _ in range(NumUsers)]

    Events = []
    for user in users:
        SEMAParticipantId = "".join([str(randint(1, 9))] + [str(randint(0, 9)) for _ in range(8)])
        month = randint(1, 12)
        first_day = randint(1, 20)
        for day in range(first_day, first_day + 7):
            for hour in range(0, 24):
                lat = gauss(-37.814, 1.)
                long = gauss(144.96332, 1.5)
                eApp = FakeEvent(event_type="__App__", user_id=user, date_time=datetime(2019, month, day, hour),
                                 latitude=lat, longitude=long)
                Events.append(eApp)
                if randint(0, 1 + abs(hour - 12)) == 0:
                    e = FakeEvent(event_type="Gmail", user_id=user, date_time=datetime(2019, month, day, hour),
                                  latitude=lat, longitude=long)
                    Events.append(e)
                if randint(0, 4 + abs(hour - 12)) == 0:
                    e = FakeEvent(event_type="SMS", user_id=user, date_time=datetime(2019, month, day, hour),
                                  latitude=lat, longitude=long)
                    Events.append(e)
                if randint(0, 6 + abs(hour - 12)) == 0:
                    e = FakeEvent(event_type="Call", user_id=user, date_time=datetime(2019, month, day, hour),
                                  latitude=lat, longitude=long)
                    Events.append(e)
                if randint(0, 9 + abs(hour - 12)) == 0:
                    if "Saturday" in eApp.keywords or "Sunday" in eApp.keywords:
                        e = FakeEvent(event_type="Button", button_type="Happy", user_id=user,
                                      date_time=datetime(2019, month, day, hour), latitude=lat, longitude=long)
                    else:
                        e = FakeEvent(event_type="Button", user_id=user, date_time=datetime(2019, month, day, hour),
                                      latitude=lat, longitude=long)
                    Events.append(e)

            # SEMA data
            sema_hours = [randint(9, 12), randint(13, 16), randint(17, 20)]
            for sema_hour in sema_hours:
                lat = gauss(-37.814, 1.)
                long = gauss(144.96332, 1.5)
                e = FakeEvent(event_type="__SEMA__", user_id=user, sema_participant_id=SEMAParticipantId,
                              date_time=datetime(2019, month, day, sema_hour), latitude=lat, longitude=long)
                Events.append(e)

    write_file(Events)
