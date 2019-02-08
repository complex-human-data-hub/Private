from event import Event

data = [{ 'AccelerometryCount': 3,
  'AudioProcessedCount': 7,
  'BatteryCount': 9,
  'BatteryLevel': 43,
  'EndDateTime': '2016-11-14',
  'Kilometers': 2.5696762096240664,
  'LocationCount': 2,
  'MoonAge': 16.65677569622446,
  'MoonIllumination': 0.31864295121020203,
  'StartDateTime': '2016-11-14',
  'Temperature': 17.042919489100292,
  'UserId': '1a579b64-a77e-4087-a3b4-d30ddf534348',
  'Weather': 'overcast',
  'address': u'Unit 94\n 784 Hensley Port\nSouth Kimberly, SA, 2658',
  'keywords': [ 'November',
                'Monday',
                '2010',
                'summer',
                'audio_car',
                'overcast',
                'waning_gibbous'],
  'latitude': -40.198690642459965,
  'longitude': 145.17861031042898,
  'type': 'App'}, { 'AccelerometryCount': 2,
  'AudioProcessedCount': 7,
  'BatteryCount': 8,
  'BatteryLevel': 14,
  'EndDateTime': '2013-03-14',
  'Kilometers': 2.35520051107455,
  'LocationCount': 4,
  'MoonAge': 2.1973401186553874,
  'MoonIllumination': 0.38383528676966583,
  'StartDateTime': '2013-03-14',
  'Temperature': 9.13981255125622,
  'UserId': '1a579b64-a77e-4087-a3b4-d30ddf534348',
  'Weather': 'overcast',
  'address': u'Flat 14\n 9 Hall Nook\nVelazquezside, NT, 2565',
  'keywords': [ 'August',
                'Thursday',
                '1983',
                'summer',
                'audio_home',
                'overcast',
                'waxing_gibbous',
                'cafe'],
  'latitude': -39.03689423023596,
  'longitude': 144.32534760995784,
  'type': 'App'}, { 'AccelerometryCount': 11,
  'AudioProcessedCount': 3,
  'BatteryCount': 4,
  'BatteryLevel': 25,
  'EndDateTime': '2017-02-07',
  'Kilometers': 1.2391193768143063,
  'LocationCount': 10,
  'MoonAge': 26.236006416890703,
  'MoonIllumination': 0.6750754951700502,
  'StartDateTime': '2017-02-07',
  'Temperature': 29.684222318053816,
  'UserId': '1a579b64-a77e-4087-a3b4-d30ddf534348',
  'Weather': 'clear',
  'address': u'9 /\n 0 Jones Quays\nKaylastad, WA, 2925',
  'keywords': [ 'July',
                'Friday',
                '1982',
                'autumn',
                'audio_home',
                'clear',
                'waning_gibbous'],
  'latitude': -39.216966580756676,
  'longitude': 143.00999741684043,
  'type': 'App'}, { 'AccelerometryCount': 11,
  'AudioProcessedCount': 1,
  'BatteryCount': 9,
  'BatteryLevel': 7,
  'EndDateTime': '2018-12-10',
  'Kilometers': 0.6398597333310044,
  'LocationCount': 11,
  'MoonAge': 21.345884180040862,
  'MoonIllumination': 0.11472006113433186,
  'StartDateTime': '2018-12-10',
  'Temperature': 8.155740613849009,
  'UserId': '1a579b64-a77e-4087-a3b4-d30ddf534348',
  'Weather': 'rain',
  'address': u'Level 7\n 2 Wolfe Port\nTerrichester, QLD, 2984',
  'keywords': [ 'August',
                'Monday',
                '1997',
                'summer',
                'audio_home',
                'rain',
                'waning_gibbous'],
  'latitude': -36.157373938854285,
  'longitude': 145.61586023947572,
  'type': 'App'}, { 'AccelerometryCount': 10,
  'AudioProcessedCount': 10,
  'BatteryCount': 10,
  'BatteryLevel': 76,
  'EndDateTime': '2010-10-16',
  'Kilometers': 0.26791628657890276,
  'LocationCount': 8,
  'MoonAge': 22.991097032065408,
  'MoonIllumination': 0.3932845038314968,
  'StartDateTime': '2010-10-16',
  'Temperature': 10.3936148724047,
  'UserId': '1a579b64-a77e-4087-a3b4-d30ddf534348',
  'Weather': 'rain',
  'address': u'Suite 398\n 191 Amy Deviation\nWest Heidi, QLD, 2392',
  'keywords': [ 'March',
                'Tuesday',
                '1997',
                'spring',
                'audio_home',
                'rain',
                'waxing_gibbous',
                'church'],
  'latitude': -36.966501646575324,
  'longitude': 143.77583800494668,
  'type': 'App'}, { 'AccelerometryCount': 4,
  'AudioProcessedCount': 2,
  'BatteryCount': 8,
  'BatteryLevel': 9,
  'EndDateTime': '2012-08-05',
  'StartDateTime': '2012-08-05',
  'UserId': '1a579b64-a77e-4087-a3b4-d30ddf534348',
  'keywords': ['January', 'Wednesday', '2016', 'spring', 'audio_street'],
  'type': 'App'}, { 'AccelerometryCount': 10,
  'AudioProcessedCount': 10,
  'BatteryCount': 7,
  'BatteryLevel': 54,
  'EndDateTime': '2015-09-24',
  'StartDateTime': '2015-09-24',
  'UserId': 'f32cf42b-45d9-49cb-96af-09f51a140888',
  'keywords': ['January', 'Tuesday', '1976', 'spring', 'audio_home'],
  'type': 'App'}, { 'AccelerometryCount': 2,
  'AudioProcessedCount': 4,
  'BatteryCount': 8,
  'BatteryLevel': 69,
  'EndDateTime': '2018-11-05',
  'Kilometers': 1.1913593883808407,
  'LocationCount': 1,
  'MoonAge': 2.6165121991229965,
  'MoonIllumination': 0.6429039761084253,
  'StartDateTime': '2018-11-05',
  'Temperature': 24.239060916012356,
  'UserId': 'f32cf42b-45d9-49cb-96af-09f51a140888',
  'Weather': 'overcast',
  'address': u'Flat 41\n 315 Williams Mew\nYoungfort, SA, 2693',
  'keywords': [ 'June',
                'Friday',
                '1997',
                'autumn',
                'audio_car',
                'overcast',
                'waning_gibbous'],
  'latitude': -37.913803137740096,
  'longitude': 145.90188325141057,
  'type': 'App'}, { 'AccelerometryCount': 9,
  'AudioProcessedCount': 5,
  'BatteryCount': 7,
  'BatteryLevel': 97,
  'EndDateTime': '2016-09-11',
  'StartDateTime': '2016-09-11',
  'UserId': 'f32cf42b-45d9-49cb-96af-09f51a140888',
  'keywords': ['August', 'Saturday', '2004', 'spring', 'audio_home'],
  'type': 'App'}, { 'AccelerometryCount': 5,
  'AudioProcessedCount': 12,
  'BatteryCount': 10,
  'BatteryLevel': 87,
  'EndDateTime': '2013-03-08',
  'Kilometers': 1.2317138043115905,
  'LocationCount': 8,
  'MoonAge': 14.97208349570932,
  'MoonIllumination': 0.3784670726515499,
  'StartDateTime': '2013-03-08',
  'Temperature': 8.970262799100073,
  'UserId': 'f32cf42b-45d9-49cb-96af-09f51a140888',
  'Weather': 'rain',
  'address': u'437 /\n 924 Stuart Firetrail\nMorenoborough, VIC, 2933',
  'keywords': [ 'March',
                'Sunday',
                '1984',
                'winter',
                'audio_street',
                'rain',
                'waxing_gibbous'],
  'latitude': -38.977990976060994,
  'longitude': 144.86427986415464,
  'type': 'App'}, { 'AccelerometryCount': 4,
  'AudioProcessedCount': 11,
  'BatteryCount': 6,
  'BatteryLevel': 39,
  'EndDateTime': '2015-09-01',
  'Kilometers': 0.16068192330357625,
  'LocationCount': 6,
  'MoonAge': 13.776865535361125,
  'MoonIllumination': 0.5914240148364442,
  'StartDateTime': '2015-09-01',
  'Temperature': 29.76913724289956,
  'UserId': 'f32cf42b-45d9-49cb-96af-09f51a140888',
  'Weather': 'rain',
  'address': u'9 Johnson Entrance\nConwaymouth, NT, 2904',
  'keywords': [ 'June',
                'Sunday',
                '2009',
                'winter',
                'audio_home',
                'rain',
                'waxing_gibbous'],
  'latitude': -37.30960378164955,
  'longitude': 144.83652790401624,
  'type': 'App'}, { 'AccelerometryCount': 6,
  'AudioProcessedCount': 11,
  'BatteryCount': 8,
  'BatteryLevel': 85,
  'EndDateTime': '2016-09-20',
  'Kilometers': 0.6570723110889157,
  'LocationCount': 2,
  'MoonAge': 22.84363316001355,
  'MoonIllumination': 0.13628734111461482,
  'StartDateTime': '2016-09-20',
  'Temperature': 27.873097748331638,
  'UserId': 'f32cf42b-45d9-49cb-96af-09f51a140888',
  'Weather': 'overcast',
  'address': u'Level 0\n 424 Shawn Avenue\nSt. Jessicaville, VIC, 5183',
  'keywords': [ 'February',
                'Wednesday',
                '2016',
                'winter',
                'audio_voice',
                'overcast',
                'waxing_gibbous'],
  'latitude': -36.88499669354035,
  'longitude': 144.48226787706287,
  'type': 'App'}, { 'AccelerometryCount': 1,
  'AudioProcessedCount': 7,
  'BatteryCount': 1,
  'BatteryLevel': 52,
  'EndDateTime': '2010-11-29',
  'Kilometers': 0.08263488721004394,
  'LocationCount': 5,
  'MoonAge': 25.201534572204704,
  'MoonIllumination': 0.6234772629806182,
  'StartDateTime': '2010-11-29',
  'Temperature': 1.4326330866226957,
  'UserId': 'f32cf42b-45d9-49cb-96af-09f51a140888',
  'Weather': 'overcast',
  'address': u'Flat 12\n 73 Paul Approach\nWalkerside, VIC, 2212',
  'keywords': [ 'March',
                'Tuesday',
                '2007',
                'spring',
                'audio_home',
                'audio_street',
                'overcast',
                'waning_gibbous'],
  'latitude': -37.95552870246483,
  'longitude': 143.24313075367812,
  'type': 'App'}, { 'AccelerometryCount': 10,
  'AudioProcessedCount': 5,
  'BatteryCount': 11,
  'BatteryLevel': 75,
  'EndDateTime': '2013-07-26',
  'Kilometers': 1.212688885270516,
  'LocationCount': 6,
  'MoonAge': 28.256551157599013,
  'MoonIllumination': 0.39253937697314756,
  'StartDateTime': '2013-07-26',
  'Temperature': 10.570302728987917,
  'UserId': 'f32cf42b-45d9-49cb-96af-09f51a140888',
  'Weather': 'clear',
  'address': u'97 James Road\nJenningsberg, VIC, 2492',
  'keywords': [ 'February',
                'Friday',
                '1998',
                'summer',
                'audio_home',
                'audio_home',
                'clear',
                'waxing_gibbous'],
  'latitude': -38.35387383555743,
  'longitude': 145.37882968005812,
  'type': 'App'}, { 'AccelerometryCount': 12,
  'AudioProcessedCount': 8,
  'BatteryCount': 5,
  'BatteryLevel': 62,
  'EndDateTime': '2017-06-29',
  'Kilometers': 0.18969003055135397,
  'LocationCount': 2,
  'MoonAge': 2.1501081841388903,
  'MoonIllumination': 0.42356359655664744,
  'StartDateTime': '2017-06-29',
  'Temperature': 15.612791023184487,
  'UserId': 'f32cf42b-45d9-49cb-96af-09f51a140888',
  'Weather': 'rain',
  'address': u'Apt. 971\n 61 Stevens Amble\nNorth Danielchester, NT, 2596',
  'keywords': [ 'January',
                'Wednesday',
                '1999',
                'summer',
                'audio_car',
                'audio_home',
                'rain',
                'waxing_gibbous'],
  'latitude': -38.52295623856186,
  'longitude': 145.1031528106771,
  'type': 'App'}, { 'AccelerometryCount': 6,
  'AudioProcessedCount': 10,
  'BatteryCount': 8,
  'BatteryLevel': 87,
  'EndDateTime': '2012-10-16',
  'Kilometers': 0.551274773724955,
  'LocationCount': 6,
  'MoonAge': 23.854101817585565,
  'MoonIllumination': 0.19716626192081999,
  'StartDateTime': '2012-10-16',
  'Temperature': 12.99298247119834,
  'UserId': 'f32cf42b-45d9-49cb-96af-09f51a140888',
  'Weather': 'rain',
  'address': u'696 Michele Expressway\nWest Melissaborough, QLD, 2667',
  'keywords': [ 'February',
                'Tuesday',
                '2017',
                'summer',
                'audio_voice',
                'rain',
                'waxing_gibbous'],
  'latitude': -37.50980591480495,
  'longitude': 144.07419843822993,
  'type': 'App'}, { 'AccelerometryCount': 12,
  'AudioProcessedCount': 9,
  'BatteryCount': 8,
  'BatteryLevel': 5,
  'EndDateTime': '2012-03-16',
  'Kilometers': 0.44609346575608216,
  'LocationCount': 11,
  'MoonAge': 8.227127257730727,
  'MoonIllumination': 0.00350411216630786,
  'StartDateTime': '2012-03-16',
  'Temperature': 14.569966384339658,
  'UserId': 'dd7f1efb-e741-4633-9192-f3c5bebb04d3',
  'Weather': 'rain',
  'address': u'Flat 20\n 560 Maldonado Circle\nSt. Michellemouth, ACT, 2915',
  'keywords': [ 'October',
                'Monday',
                '2016',
                'autumn',
                'audio_car',
                'audio_street',
                'audio_home',
                'rain',
                'waning_gibbous'],
  'latitude': -38.308047057961616,
  'longitude': 145.90905219888157,
  'type': 'App'}, { 'AccelerometryCount': 7,
  'AudioProcessedCount': 4,
  'BatteryCount': 11,
  'BatteryLevel': 14,
  'EndDateTime': '2017-01-29',
  'StartDateTime': '2017-01-29',
  'UserId': 'dd7f1efb-e741-4633-9192-f3c5bebb04d3',
  'keywords': ['August', 'Tuesday', '1974', 'autumn', 'audio_home'],
  'type': 'App'}, { 'AccelerometryCount': 7,
  'AudioProcessedCount': 7,
  'BatteryCount': 4,
  'BatteryLevel': 59,
  'EndDateTime': '2013-06-22',
  'Kilometers': 0.45838737864812473,
  'LocationCount': 10,
  'MoonAge': 5.233160811702088,
  'MoonIllumination': 0.5362242551347338,
  'StartDateTime': '2013-06-22',
  'Temperature': 19.86642525944445,
  'UserId': 'dd7f1efb-e741-4633-9192-f3c5bebb04d3',
  'Weather': 'clear',
  'address': u'Unit 86\n 10 Pamela Quays\nSouth Steven, NT, 2482',
  'keywords': [ 'July',
                'Thursday',
                '1984',
                'autumn',
                'audio_car',
                'clear',
                'waxing_gibbous',
                'church'],
  'latitude': -38.621772604948774,
  'longitude': 144.44880928857455,
  'type': 'App'}, { 'AccelerometryCount': 8,
  'AudioProcessedCount': 9,
  'BatteryCount': 6,
  'BatteryLevel': 66,
  'EndDateTime': '2017-06-17',
  'Kilometers': 0.948471284039566,
  'LocationCount': 8,
  'MoonAge': 11.125924386541715,
  'MoonIllumination': 0.414707865737159,
  'StartDateTime': '2017-06-17',
  'Temperature': 26.32395990542856,
  'UserId': 'dd7f1efb-e741-4633-9192-f3c5bebb04d3',
  'Weather': 'cloudy',
  'address': u'Unit 35\n 015 Levi Hill\nWest Emma, QLD, 2912',
  'keywords': [ 'October',
                'Thursday',
                '1975',
                'spring',
                'audio_home',
                'cloudy',
                'waning_gibbous'],
  'latitude': -38.238133723475976,
  'longitude': 145.5281473950043,
  'type': 'App'}, { 'AccelerometryCount': 6,
  'AudioProcessedCount': 8,
  'BatteryCount': 6,
  'BatteryLevel': 82,
  'EndDateTime': '2011-10-09',
  'Kilometers': 0.14829514534435098,
  'LocationCount': 2,
  'MoonAge': 6.9224921421995464,
  'MoonIllumination': 0.3303525557841235,
  'StartDateTime': '2011-10-09',
  'Temperature': 26.075559685835152,
  'UserId': 'dd7f1efb-e741-4633-9192-f3c5bebb04d3',
  'Weather': 'rain',
  'address': u'21 Lisa Hill\nSt. Kathleen, SA, 2222',
  'keywords': [ 'December',
                'Monday',
                '2006',
                'spring',
                'audio_home',
                'audio_street',
                'rain',
                'waxing_gibbous'],
  'latitude': -37.41800983229789,
  'longitude': 142.82565114722303,
  'type': 'App'}, { 'AccelerometryCount': 12,
  'AudioProcessedCount': 1,
  'BatteryCount': 6,
  'BatteryLevel': 31,
  'EndDateTime': '2018-12-16',
  'Kilometers': 0.30814929654289636,
  'LocationCount': 11,
  'MoonAge': 2.265027492717243,
  'MoonIllumination': 0.6142144987106299,
  'StartDateTime': '2018-12-16',
  'Temperature': -3.3382947364523865,
  'UserId': 'dd7f1efb-e741-4633-9192-f3c5bebb04d3',
  'Weather': 'overcast',
  'address': u'2 Amanda Wade\nAndersonmouth, SA, 5984',
  'keywords': [ 'July',
                'Monday',
                '1997',
                'spring',
                'audio_street',
                'audio_home',
                'audio_car',
                'overcast',
                'waning_gibbous'],
  'latitude': -38.62980040888183,
  'longitude': 144.37265452503246,
  'type': 'App'}, { 'AccelerometryCount': 10,
  'AudioProcessedCount': 7,
  'BatteryCount': 1,
  'BatteryLevel': 25,
  'EndDateTime': '2011-07-25',
  'StartDateTime': '2011-07-25',
  'UserId': 'dd7f1efb-e741-4633-9192-f3c5bebb04d3',
  'keywords': [ 'November',
                'Monday',
                '1976',
                'spring',
                'audio_street',
                'audio_car',
                'audio_home',
                'audio_voice'],
  'type': 'App'}]
Events = [Event(d) for d in data]
DemoEvents = Events

