from graph import depGraph
import datetime

data = [{ 'EndDateTime': '2015-02-13',\
  'StartDateTime': '2015-02-13',\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'keywords': ['July', 'Wednesday', '1995', 'Depressed'],\
  'latitude': -69.2492515,\
  'longitude': 173.966435,\
  'type': 'Button'}, { 'Duration': 23,\
  'EndDateTime': '2012-07-25',\
  'Name': u'Richard Huber',\
  'Number': u'+61 8 8411 9324',\
  'StartDateTime': '2012-07-25',\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'keywords': ['May', 'Saturday', '2003', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2010-08-03',\
  'StartDateTime': '2010-08-03',\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'keywords': ['June', 'Saturday', '1971', 'Depressed'],\
  'latitude': 27.1414945,\
  'longitude': -3.089708,\
  'type': 'Button'}, { 'EndDateTime': '2012-10-10',\
  'Name': u'Kevin Carter',\
  'Number': u'+61-2-7644-3864',\
  'StartDateTime': '2012-10-10',\
  'Text': u'Quasi non qui quasi numquam.',\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'keywords': ['December', 'Monday', '2007', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'AccelerometryCount': 4,\
  'AudioProcessedCount': 5,\
  'BatteryCount': 1,\
  'BatteryLevel': 13,\
  'EndDateTime': '2016-01-20',\
  'Kilometers': 0.7599383412711663,\
  'LocationCount': 10,\
  'MoonAge': 2.6435062652652586,\
  'MoonIllumination': 0.7395869048962413,\
  'StartDateTime': '2016-01-20',\
  'Temperature': 23.082639702001117,\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'Weather': 'rain',\
  'address': u'65 Hickman Cruiseway\nNathanshire, QLD, 2985',\
  'keywords': [ 'April',\
                'Sunday',\
                '1999',\
                'autumn',\
                'audio_voice',\
                'rain',\
                'waning_gibbous'],\
  'latitude': -19.5369225,\
  'longitude': 175.672064,\
  'type': 'App'}, { 'Duration': 31,\
  'EndDateTime': '2013-02-15',\
  'Name': u'David Avery',\
  'Number': u'02.0863.2626',\
  'StartDateTime': '2013-02-15',\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'keywords': ['March', 'Monday', '2017', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 2,\
  'AudioProcessedCount': 1,\
  'BatteryCount': 10,\
  'BatteryLevel': 54,\
  'EndDateTime': '2011-10-23',\
  'Kilometers': 1.389555785898355,\
  'LocationCount': 12,\
  'MoonAge': 14.380146678358015,\
  'MoonIllumination': 0.7111892963373782,\
  'StartDateTime': '2011-10-23',\
  'Temperature': 23.537372240122753,\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'Weather': 'overcast',\
  'address': u'Suite 411\n 6 Smith Mount\nNorth Stuart, TAS, 2920',\
  'keywords': [ 'April',\
                'Sunday',\
                '2007',\
                'summer',\
                'audio_car',\
                'overcast',\
                'waxing_gibbous'],\
  'latitude': -40.6210135,\
  'longitude': 125.934819,\
  'type': 'App'}, { 'AccelerometryCount': 12,\
  'AudioProcessedCount': 3,\
  'BatteryCount': 9,\
  'BatteryLevel': 86,\
  'EndDateTime': '2015-03-31',\
  'Kilometers': 0.9784885910507192,\
  'LocationCount': 10,\
  'MoonAge': 12.416443796102156,\
  'MoonIllumination': 0.3943898541077435,\
  'StartDateTime': '2015-03-31',\
  'Temperature': 35.943094601951074,\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'Weather': 'rain',\
  'address': u'27 Jackson Link\nNorth Leviville, NSW, 2821',\
  'keywords': [ 'September',\
                'Sunday',\
                '1974',\
                'spring',\
                'audio_street',\
                'audio_car',\
                'rain',\
                'waxing_gibbous'],\
  'latitude': 0.846724,\
  'longitude': -88.568127,\
  'type': 'App'}, { 'EndDateTime': '2010-12-01',\
  'Name': u'Kellie Holland',\
  'Number': u'0492-865-718',\
  'StartDateTime': '2010-12-01',\
  'Text': u'Laudantium quos quia dicta.',\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'keywords': ['August', 'Thursday', '1984', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2011-03-14',\
  'StartDateTime': '2011-03-14',\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'keywords': ['September', 'Saturday', '1997', 'Happy'],\
  'latitude': 72.838334,\
  'longitude': -12.2246,\
  'type': 'Button'}, { 'EndDateTime': '2012-01-17',\
  'StartDateTime': '2012-01-17',\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'keywords': ['January', 'Wednesday', '1977', 'Tired'],\
  'latitude': -31.435795,\
  'longitude': -60.190644,\
  'type': 'Button'}, { 'Duration': 18,\
  'EndDateTime': '2013-10-01',\
  'Name': u'Johnathan Watts',\
  'Number': u'+61 3 9683 4147',\
  'StartDateTime': '2013-10-01',\
  'UserId': 'f1ff5f31-055b-4037-9f2b-c1de65cfb3a3',\
  'keywords': ['August', 'Monday', '2001', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2016-02-02',\
  'StartDateTime': '2016-02-02',\
  'UserId': '75007c40-c1e3-4c00-8361-4152d437dfd4',\
  'keywords': ['March', 'Friday', '1981', 'Excited'],\
  'latitude': -84.5771995,\
  'longitude': 132.553418,\
  'type': 'Button'}, { 'EndDateTime': '2018-03-13',\
  'StartDateTime': '2018-03-13',\
  'UserId': '75007c40-c1e3-4c00-8361-4152d437dfd4',\
  'keywords': ['July', 'Monday', '2011', 'Excited'],\
  'latitude': 59.408222,\
  'longitude': 136.587303,\
  'type': 'Button'}, { 'Duration': 196,\
  'EndDateTime': '2018-05-06',\
  'Name': u'Kelsey Smith',\
  'Number': u'+61-483-940-557',\
  'StartDateTime': '2018-05-06',\
  'UserId': '75007c40-c1e3-4c00-8361-4152d437dfd4',\
  'keywords': ['June', 'Thursday', '1974', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'Duration': 166,\
  'EndDateTime': '2012-05-23',\
  'Name': u'Kristen Conway',\
  'Number': u'(07)62329748',\
  'StartDateTime': '2012-05-23',\
  'UserId': '75007c40-c1e3-4c00-8361-4152d437dfd4',\
  'keywords': ['April', 'Tuesday', '1989', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 6,\
  'AudioProcessedCount': 11,\
  'BatteryCount': 8,\
  'BatteryLevel': 98,\
  'EndDateTime': '2016-07-23',\
  'Kilometers': 0.006787677978210564,\
  'LocationCount': 1,\
  'MoonAge': 2.073988530567398,\
  'MoonIllumination': 0.4690346483388076,\
  'StartDateTime': '2016-07-23',\
  'Temperature': 17.36280160327512,\
  'UserId': '75007c40-c1e3-4c00-8361-4152d437dfd4',\
  'Weather': 'clear',\
  'address': u'096 /\n 031 Patrick Strand\nHannahborough, QLD, 2920',\
  'keywords': [ 'July',\
                'Friday',\
                '1998',\
                'summer',\
                'audio_street',\
                'clear',\
                'waning_gibbous'],\
  'latitude': -49.1707115,\
  'longitude': 123.160315,\
  'type': 'App'}, { 'EndDateTime': '2011-01-28',\
  'StartDateTime': '2011-01-28',\
  'UserId': '75007c40-c1e3-4c00-8361-4152d437dfd4',\
  'keywords': ['July', 'Thursday', '2008', 'Happy'],\
  'latitude': -74.404759,\
  'longitude': -68.305062,\
  'type': 'Button'}, { 'AccelerometryCount': 8,\
  'AudioProcessedCount': 3,\
  'BatteryCount': 7,\
  'BatteryLevel': 23,\
  'EndDateTime': '2017-02-03',\
  'Kilometers': 0.13207523937652363,\
  'LocationCount': 12,\
  'MoonAge': 11.082800215867994,\
  'MoonIllumination': 0.21280283791250987,\
  'StartDateTime': '2017-02-03',\
  'Temperature': 9.534929326422613,\
  'UserId': '75007c40-c1e3-4c00-8361-4152d437dfd4',\
  'Weather': 'clear',\
  'address': u'88 Aguilar Court\nSt. Brian, SA, 2677',\
  'keywords': [ 'August',\
                'Thursday',\
                '1985',\
                'winter',\
                'audio_car',\
                'clear',\
                'waxing_gibbous'],\
  'latitude': -55.349562,\
  'longitude': -139.886791,\
  'type': 'App'}, { 'EndDateTime': '2012-02-22',\
  'Name': u'Chelsey Garcia',\
  'Number': u'+61-433-140-112',\
  'StartDateTime': '2012-02-22',\
  'Text': u'Error adipisci harum eum.',\
  'UserId': '75007c40-c1e3-4c00-8361-4152d437dfd4',\
  'keywords': ['September', 'Saturday', '1971', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2018-07-02',\
  'Name': u'Eugene Acosta',\
  'Number': u'29552616',\
  'StartDateTime': '2018-07-02',\
  'Text': u'Veritatis aperiam non est ut.',\
  'UserId': '75007c40-c1e3-4c00-8361-4152d437dfd4',\
  'keywords': ['March', 'Tuesday', '1990', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2018-04-21',\
  'StartDateTime': '2018-04-21',\
  'UserId': '75007c40-c1e3-4c00-8361-4152d437dfd4',\
  'keywords': ['October', 'Monday', '2003', 'Depressed'],\
  'latitude': -33.279136,\
  'longitude': 40.367053,\
  'type': 'Button'}, { 'Duration': 172,\
  'EndDateTime': '2010-08-15',\
  'Name': u'Michelle Stuart',\
  'Number': u'+61 3 7918 3225',\
  'StartDateTime': '2010-08-15',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['May', 'Sunday', '1993', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2013-09-05',\
  'Name': u'Timothy Horne',\
  'Number': u'+61.2.2556.5661',\
  'StartDateTime': '2013-09-05',\
  'Text': u'Ex eum fuga quidem.',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['March', 'Sunday', '1985', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2013-05-21',\
  'Name': u'Shaun Guzman',\
  'Number': u'(07)35288257',\
  'StartDateTime': '2013-05-21',\
  'Text': u'Suscipit quidem alias.',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['May', 'Sunday', '2011', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'AccelerometryCount': 6,\
  'AudioProcessedCount': 2,\
  'BatteryCount': 9,\
  'BatteryLevel': 33,\
  'EndDateTime': '2018-08-07',\
  'Kilometers': 3.6948755079843227,\
  'LocationCount': 8,\
  'MoonAge': 4.116963213053011,\
  'MoonIllumination': 0.9907700752787726,\
  'StartDateTime': '2018-08-07',\
  'Temperature': 6.796437389637363,\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'Weather': 'clear',\
  'address': u'Suite 120\n 0 Karen Green\nLake Johnside, VIC, 2920',\
  'keywords': [ 'December',\
                'Thursday',\
                '1981',\
                'winter',\
                'audio_voice',\
                'audio_home',\
                'clear',\
                'waning_gibbous',\
                'church'],\
  'latitude': -55.103314,\
  'longitude': 37.986689,\
  'type': 'App'}, { 'EndDateTime': '2011-03-31',\
  'From': u'alexandra95@conner.com.au',\
  'Message': u'Iste nesciunt tempore aperiam voluptates. Enim praesentium odit quis culpa dignissimos.\nDucimus excepturi nihil adipisci veritatis delectus facilis. Iste fugit quasi labore voluptas reiciendis.\nInventore aliquid vitae impedit. Nam perspiciatis facilis deleniti cupiditate voluptas porro. Autem occaecati amet nobis nam corrupti id.',\
  'StartDateTime': '2011-03-31',\
  'Subject': u'Distinctio rerum.',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['March', 'Thursday', '1997', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2017-11-13',\
  'Name': u'Kathleen Hunter',\
  'Number': u'+61-486-657-140',\
  'StartDateTime': '2017-11-13',\
  'Text': u'Dolores optio sint iusto.',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['August', 'Thursday', '1972', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2015-04-12',\
  'StartDateTime': '2015-04-12',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['March', 'Thursday', '2007', 'Excited'],\
  'latitude': -33.0660485,\
  'longitude': 7.961256,\
  'type': 'Button'}, { 'EndDateTime': '2012-11-14',\
  'From': u'david69@yahoo.com',\
  'Message': u'Incidunt totam vero iste nam. Distinctio suscipit voluptate delectus ducimus recusandae impedit non.\nNon veniam earum earum architecto aspernatur. Repudiandae suscipit deserunt amet quasi. Dicta excepturi placeat commodi autem.\nQuasi asperiores esse porro quia. Voluptatum atque praesentium blanditiis ratione. Nobis in nemo itaque soluta quod molestias. Repellat nulla ut harum.',\
  'StartDateTime': '2012-11-14',\
  'Subject': u'Laborum eveniet.',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['September', 'Saturday', '2004', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 8,\
  'AudioProcessedCount': 2,\
  'BatteryCount': 1,\
  'BatteryLevel': 88,\
  'EndDateTime': '2012-12-12',\
  'Kilometers': 0.06324990955028616,\
  'LocationCount': 9,\
  'MoonAge': 6.090916339266071,\
  'MoonIllumination': 0.7627928393957139,\
  'StartDateTime': '2012-12-12',\
  'Temperature': 17.091423624216755,\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'Weather': 'overcast',\
  'address': u'4 /\n 00 Carter Dip\nPort Kathleenfort, SA, 2975',\
  'keywords': [ 'August',\
                'Saturday',\
                '1973',\
                'spring',\
                'audio_home',\
                'overcast',\
                'waxing_gibbous'],\
  'latitude': -66.756477,\
  'longitude': -76.903033,\
  'type': 'App'}, { 'Duration': 64,\
  'EndDateTime': '2010-07-16',\
  'Name': u'Jeffery Myers',\
  'Number': u'+61.419.643.769',\
  'StartDateTime': '2010-07-16',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['June', 'Monday', '2004', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2015-08-07',\
  'Message': u'Enim exercitationem pariatur sed. Dicta natus voluptate facilis odit et. Recusandae ut voluptate iusto. Vero blanditiis quod quisquam deserunt.\nSequi labore occaecati optio. Quod corrupti soluta ratione quam quidem.\nBeatae nostrum tempora consequuntur adipisci. Provident ullam inventore labore quaerat.\nPorro velit temporibus.',\
  'StartDateTime': '2015-08-07',\
  'Subject': u'Temporibus maxime.',\
  'To': u'connor63@miller.org',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['June', 'Friday', '2017', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 5,\
  'AudioProcessedCount': 4,\
  'BatteryCount': 12,\
  'BatteryLevel': 96,\
  'EndDateTime': '2015-05-15',\
  'Kilometers': 1.1252532047630612,\
  'LocationCount': 8,\
  'MoonAge': 1.4782798936335773,\
  'MoonIllumination': 0.5964381164952606,\
  'StartDateTime': '2015-05-15',\
  'Temperature': -2.419253864972859,\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'Weather': 'cloudy',\
  'address': u'38 Michael Sound\nLake Courtney, WA, 2698',\
  'keywords': [ 'March',\
                'Saturday',\
                '1976',\
                'summer',\
                'audio_home',\
                'audio_voice',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': 41.3326315,\
  'longitude': 139.090451,\
  'type': 'App'}, { 'EndDateTime': '2013-10-17',\
  'Name': u'Casey Hernandez DVM',\
  'Number': u'+61-499-837-038',\
  'StartDateTime': '2013-10-17',\
  'Text': u'Numquam cupiditate ad sint.',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['January', 'Sunday', '1996', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2014-03-07',\
  'StartDateTime': '2014-03-07',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['March', 'Wednesday', '1990', 'Depressed'],\
  'latitude': -34.903382,\
  'longitude': 107.025918,\
  'type': 'Button'}, { 'EndDateTime': '2012-05-05',\
  'StartDateTime': '2012-05-05',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['September', 'Friday', '2003', 'Happy'],\
  'latitude': 27.490582,\
  'longitude': -148.230973,\
  'type': 'Button'}, { 'Duration': 186,\
  'EndDateTime': '2017-03-06',\
  'Name': u'Joseph Davis',\
  'Number': u'07 3965 1324',\
  'StartDateTime': '2017-03-06',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['August', 'Thursday', '2016', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2018-11-14',\
  'Name': u'Sherry Pacheco',\
  'Number': u'+61.417.031.364',\
  'StartDateTime': '2018-11-14',\
  'Text': u'Eos aliquam nobis provident.',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['May', 'Wednesday', '1972', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2017-07-30',\
  'From': u'jasminesimmons@winters-ortiz.com',\
  'Message': u'Provident dolores quisquam tempore cumque saepe officiis deleniti. Consectetur nostrum nemo saepe quaerat iusto. Natus magni praesentium.\nIn sunt in sint soluta cumque. Adipisci eveniet totam at necessitatibus veniam vitae.\nSunt voluptas voluptate nisi.\nDebitis rem aut quidem. Distinctio voluptates officiis. Accusamus qui facilis dolores deserunt quidem perspiciatis.',\
  'StartDateTime': '2017-07-30',\
  'Subject': u'Exercitationem.',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['March', 'Sunday', '2002', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'Duration': 158,\
  'EndDateTime': '2013-09-12',\
  'Name': u'Joseph Lopez',\
  'Number': u'0829520396',\
  'StartDateTime': '2013-09-12',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['February', 'Friday', '1983', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'Duration': 295,\
  'EndDateTime': '2011-04-04',\
  'Name': u'Joshua Adams',\
  'Number': u'08-6140-3644',\
  'StartDateTime': '2011-04-04',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['January', 'Friday', '2015', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2018-09-24',\
  'From': u'laura00@boyle-barker.org.au',\
  'Message': u'Voluptas laboriosam dolores possimus voluptates placeat voluptatibus. Quod amet corporis perferendis laborum.\nAt cum ducimus similique sapiente. Ratione facilis ratione deleniti voluptas esse. Architecto tenetur laudantium voluptate laudantium.\nEarum minima provident facilis. Minima sunt blanditiis architecto modi quod placeat consectetur. Natus fugit aperiam aliquid molestiae omnis architecto.',\
  'StartDateTime': '2018-09-24',\
  'Subject': u'Magnam libero.',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['August', 'Thursday', '1987', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 11,\
  'AudioProcessedCount': 9,\
  'BatteryCount': 2,\
  'BatteryLevel': 21,\
  'EndDateTime': '2018-09-15',\
  'Kilometers': 0.37272658538981096,\
  'LocationCount': 12,\
  'MoonAge': 2.7689324419511827,\
  'MoonIllumination': 0.3280219763852802,\
  'StartDateTime': '2018-09-15',\
  'Temperature': 21.813384279023786,\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'Weather': 'clear',\
  'address': u'0 Darius Close\nPooleberg, ACT, 6960',\
  'keywords': [ 'April',\
                'Tuesday',\
                '2001',\
                'summer',\
                'audio_home',\
                'clear',\
                'waxing_gibbous',\
                'church'],\
  'latitude': -17.549622,\
  'longitude': -148.319661,\
  'type': 'App'}, { 'AccelerometryCount': 5,\
  'AudioProcessedCount': 1,\
  'BatteryCount': 4,\
  'BatteryLevel': 86,\
  'EndDateTime': '2014-05-22',\
  'Kilometers': 1.0267193749481394,\
  'LocationCount': 1,\
  'MoonAge': 25.332864920286667,\
  'MoonIllumination': 0.2805274643534671,\
  'StartDateTime': '2014-05-22',\
  'Temperature': -0.56440301691147,\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'Weather': 'overcast',\
  'address': u'99 Craig Landing\nThomaschester, NSW, 0812',\
  'keywords': [ 'April',\
                'Tuesday',\
                '1996',\
                'autumn',\
                'audio_street',\
                'overcast',\
                'waning_gibbous'],\
  'latitude': -89.113853,\
  'longitude': -57.737094,\
  'type': 'App'}, { 'Duration': 39,\
  'EndDateTime': '2013-08-24',\
  'Name': u'Oscar Bridges',\
  'Number': u'7704-0201',\
  'StartDateTime': '2013-08-24',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['June', 'Friday', '1999', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2017-06-24',\
  'Name': u'Katie Todd',\
  'Number': u'9247-3153',\
  'StartDateTime': '2017-06-24',\
  'Text': u'Consequuntur autem est enim.',\
  'UserId': 'a1a8ce23-1911-4411-88e4-df49b8488106',\
  'keywords': ['October', 'Saturday', '2005', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2013-01-17',\
  'From': u'vargasjeanette@yahoo.com.au',\
  'Message': u'Architecto voluptatem nobis ipsam suscipit ullam possimus. Velit sint officiis blanditiis in atque reiciendis.\nLabore fugit nihil rem. Eveniet sapiente quas non similique illum. Magni enim pariatur laudantium amet.\nSed quos saepe ab eos. Reprehenderit dolore in neque. Commodi dolores autem non voluptatem quas. Atque perferendis quia quibusdam dolorum omnis.',\
  'StartDateTime': '2013-01-17',\
  'Subject': u'Possimus laborum.',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['April', 'Friday', '1983', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 1,\
  'AudioProcessedCount': 10,\
  'BatteryCount': 3,\
  'BatteryLevel': 21,\
  'EndDateTime': '2014-12-11',\
  'Kilometers': 0.3010014600947741,\
  'LocationCount': 7,\
  'MoonAge': 29.196141641460553,\
  'MoonIllumination': 0.02066648175141761,\
  'StartDateTime': '2014-12-11',\
  'Temperature': 10.5060912015267,\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'Weather': 'overcast',\
  'address': u'Flat 40\n 2 Kennedy Court\nDouglasville, TAS, 9716',\
  'keywords': [ 'May',\
                'Monday',\
                '1995',\
                'summer',\
                'audio_car',\
                'overcast',\
                'waning_gibbous'],\
  'latitude': 86.3684675,\
  'longitude': -100.146929,\
  'type': 'App'}, { 'EndDateTime': '2016-10-23',\
  'From': u'christopherjimenez@gmail.com',\
  'Message': u'Odit iusto nihil numquam blanditiis saepe esse. Maxime nobis sed odit.\nPossimus non quibusdam in. Non possimus autem ipsam laboriosam. Unde ipsum dicta magnam.\nDucimus dignissimos perspiciatis qui excepturi. Assumenda sapiente nihil. Deserunt veritatis et suscipit. Harum nostrum adipisci voluptas asperiores.',\
  'StartDateTime': '2016-10-23',\
  'Subject': u'Voluptate quasi.',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['August', 'Wednesday', '1978', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'Duration': 87,\
  'EndDateTime': '2017-10-28',\
  'Name': u'Thomas Miller',\
  'Number': u'9875-6149',\
  'StartDateTime': '2017-10-28',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['August', 'Monday', '1992', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 5,\
  'AudioProcessedCount': 11,\
  'BatteryCount': 7,\
  'BatteryLevel': 100,\
  'EndDateTime': '2012-11-28',\
  'Kilometers': 1.0987233908807439,\
  'LocationCount': 3,\
  'MoonAge': 1.1096540189990323,\
  'MoonIllumination': 0.8298065028354916,\
  'StartDateTime': '2012-11-28',\
  'Temperature': 13.846449488990094,\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'Weather': 'rain',\
  'address': u'Flat 00\n 9 Joseph Park\nEast Meredith, TAS, 2567',\
  'keywords': [ 'March',\
                'Saturday',\
                '1978',\
                'spring',\
                'audio_home',\
                'audio_home',\
                'rain',\
                'waxing_gibbous'],\
  'latitude': 43.6814385,\
  'longitude': 82.906326,\
  'type': 'App'}, { 'EndDateTime': '2011-09-09',\
  'StartDateTime': '2011-09-09',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['September', 'Wednesday', '2009', 'Tired'],\
  'latitude': 26.638706,\
  'longitude': -38.805659,\
  'type': 'Button'}, { 'EndDateTime': '2016-08-04',\
  'From': u'pmyers@hanson-webster.edu',\
  'Message': u'In nam et quia nisi voluptatum. Minus reiciendis autem omnis. Facilis quibusdam eveniet id hic.\nCorrupti reiciendis quod fugiat. Cumque repudiandae iste ratione illum. Vel quaerat amet qui quas fugiat sed ipsa. Soluta soluta aspernatur recusandae eaque optio molestiae.\nIpsam veritatis nulla odit. Provident ratione natus nam labore consequuntur.',\
  'StartDateTime': '2016-08-04',\
  'Subject': u'Mollitia.',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['May', 'Saturday', '2012', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2014-04-07',\
  'Name': u'Christopher Morris',\
  'Number': u'(02)-3549-0522',\
  'StartDateTime': '2014-04-07',\
  'Text': u'Nostrum dolores a non.',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['July', 'Wednesday', '1989', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2010-09-28',\
  'From': u'carmenjohnson@palmer-morgan.com.au',\
  'Message': u'Nam quos quidem sit quos. Praesentium et esse sapiente occaecati nobis. Voluptatibus rem culpa aliquid id modi quod.\nNobis molestias architecto. Perferendis dolores repellat expedita. Quam repudiandae dolore ipsum nesciunt corrupti id. Nam amet impedit dolorem modi deserunt nihil odio.\nDoloribus occaecati molestiae. Quae rem ipsam aut.',\
  'StartDateTime': '2010-09-28',\
  'Subject': u'In pariatur ipsa.',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['August', 'Thursday', '1995', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'Duration': 127,\
  'EndDateTime': '2016-06-15',\
  'Name': u'Jesse Morrow',\
  'Number': u'0453-805-521',\
  'StartDateTime': '2016-06-15',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['September', 'Friday', '2011', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2011-03-17',\
  'StartDateTime': '2011-03-17',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['April', 'Wednesday', '2001', 'Depressed'],\
  'latitude': -66.2760915,\
  'longitude': -36.246246,\
  'type': 'Button'}, { 'EndDateTime': '2013-12-01',\
  'Name': u'Kenneth Rocha',\
  'Number': u'07-4114-1522',\
  'StartDateTime': '2013-12-01',\
  'Text': u'Illo doloribus quibusdam.',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['May', 'Thursday', '2013', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'Duration': 133,\
  'EndDateTime': '2016-10-27',\
  'Name': u'Rachel Randall',\
  'Number': u'(03)73962703',\
  'StartDateTime': '2016-10-27',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['August', 'Saturday', '1990', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2016-05-14',\
  'StartDateTime': '2016-05-14',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['May', 'Sunday', '2002', 'Depressed'],\
  'latitude': 21.428655,\
  'longitude': 74.309381,\
  'type': 'Button'}, { 'EndDateTime': '2013-12-07',\
  'Name': u'Jennifer Pham',\
  'Number': u'02.5257.1274',\
  'StartDateTime': '2013-12-07',\
  'Text': u'Qui ratione iure ratione.',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['April', 'Monday', '1990', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'Duration': 11,\
  'EndDateTime': '2010-07-24',\
  'Name': u'Cindy Hendrix',\
  'Number': u'0425.083.738',\
  'StartDateTime': '2010-07-24',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['October', 'Tuesday', '1971', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 7,\
  'AudioProcessedCount': 6,\
  'BatteryCount': 11,\
  'BatteryLevel': 21,\
  'EndDateTime': '2016-11-29',\
  'Kilometers': 1.068441340477178,\
  'LocationCount': 10,\
  'MoonAge': 6.597840835690877,\
  'MoonIllumination': 0.3442680213076843,\
  'StartDateTime': '2016-11-29',\
  'Temperature': 32.555713347618955,\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'Weather': 'rain',\
  'address': u'328 /\n 6 Victor Parade\nWest Tracy, WA, 2944',\
  'keywords': [ 'October',\
                'Saturday',\
                '1973',\
                'autumn',\
                'audio_voice',\
                'audio_car',\
                'rain',\
                'waning_gibbous'],\
  'latitude': 7.1619795,\
  'longitude': -48.146417,\
  'type': 'App'}, { 'AccelerometryCount': 8,\
  'AudioProcessedCount': 8,\
  'BatteryCount': 10,\
  'BatteryLevel': 94,\
  'EndDateTime': '2016-05-04',\
  'Kilometers': 0.6494744682906973,\
  'LocationCount': 3,\
  'MoonAge': 20.639334106142343,\
  'MoonIllumination': 0.7019938350290456,\
  'StartDateTime': '2016-05-04',\
  'Temperature': 23.694706319535793,\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'Weather': 'clear',\
  'address': u'823 Tammy Foreshore\nRussellville, TAS, 5664',\
  'keywords': [ 'January',\
                'Friday',\
                '2006',\
                'autumn',\
                'audio_home',\
                'clear',\
                'waning_gibbous'],\
  'latitude': -20.508877,\
  'longitude': 93.083684,\
  'type': 'App'}, { 'EndDateTime': '2012-07-29',\
  'StartDateTime': '2012-07-29',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['December', 'Thursday', '1985', 'Depressed'],\
  'latitude': 85.943748,\
  'longitude': 8.430734,\
  'type': 'Button'}, { 'EndDateTime': '2012-06-20',\
  'Message': u'Neque iure neque magni exercitationem voluptas. A saepe eaque ab voluptatibus est animi.\nModi illo enim dolorem vitae. Est ratione vitae. Sapiente quod illum eos deleniti aut omnis. Perferendis repellendus praesentium tempora esse consectetur.',\
  'StartDateTime': '2012-06-20',\
  'Subject': u'Et officiis ipsum.',\
  'To': u'allenlynch@yahoo.com',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['September', 'Saturday', '1981', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 10,\
  'AudioProcessedCount': 6,\
  'BatteryCount': 2,\
  'BatteryLevel': 61,\
  'EndDateTime': '2014-01-08',\
  'Kilometers': 0.9646242211059584,\
  'LocationCount': 7,\
  'MoonAge': 0.9633501797757937,\
  'MoonIllumination': 0.46162356515839065,\
  'StartDateTime': '2014-01-08',\
  'Temperature': 13.460429435410122,\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'Weather': 'cloudy',\
  'address': u'635 Griffith Lookout\nSmithhaven, QLD, 0233',\
  'keywords': [ 'July',\
                'Tuesday',\
                '1995',\
                'summer',\
                'audio_home',\
                'audio_voice',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': 67.2695315,\
  'longitude': -149.262033,\
  'type': 'App'}, { 'EndDateTime': '2016-07-18',\
  'StartDateTime': '2016-07-18',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['August', 'Saturday', '1976', 'Happy'],\
  'type': 'Button'}, { 'EndDateTime': '2015-03-19',\
  'StartDateTime': '2015-03-19',\
  'UserId': '7fa05124-ca58-4a9f-b54c-a65f137905b7',\
  'keywords': ['November', 'Tuesday', '1977', 'Happy'],\
  'latitude': 59.6199045,\
  'longitude': -87.302272,\
  'type': 'Button'}, { 'Duration': 293,\
  'EndDateTime': '2018-03-29',\
  'Name': u'Richard Roberts',\
  'Number': u'+61.466.809.468',\
  'StartDateTime': '2018-03-29',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['January', 'Saturday', '2012', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'Duration': 60,\
  'EndDateTime': '2010-11-30',\
  'Name': u'Diana Whitney',\
  'Number': u'(08) 1209 7113',\
  'StartDateTime': '2010-11-30',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['July', 'Saturday', '1975', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 6,\
  'AudioProcessedCount': 7,\
  'BatteryCount': 2,\
  'BatteryLevel': 4,\
  'EndDateTime': '2016-03-18',\
  'Kilometers': 0.7157284769100377,\
  'LocationCount': 11,\
  'MoonAge': 6.442355799003936,\
  'MoonIllumination': 0.5086120605963209,\
  'StartDateTime': '2016-03-18',\
  'Temperature': 24.150437622983,\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'Weather': 'clear',\
  'address': u'629 Katherine Bridge\nWilliechester, NSW, 2668',\
  'keywords': [ 'August',\
                'Wednesday',\
                '1983',\
                'autumn',\
                'audio_home',\
                'clear',\
                'waxing_gibbous'],\
  'latitude': 71.858007,\
  'longitude': 175.887354,\
  'type': 'App'}, { 'EndDateTime': '2017-04-06',\
  'Name': u'Amanda Romero',\
  'Number': u'0880785755',\
  'StartDateTime': '2017-04-06',\
  'Text': u'Porro voluptatum harum.',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['February', 'Saturday', '1983', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2017-11-14',\
  'Name': u'Jonathan Walton',\
  'Number': u'0474-572-389',\
  'StartDateTime': '2017-11-14',\
  'Text': u'Quaerat maxime eum similique.',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['April', 'Thursday', '1973', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'Duration': 22,\
  'EndDateTime': '2013-04-29',\
  'Name': u'Karen Mendoza',\
  'Number': u'2895 5531',\
  'StartDateTime': '2013-04-29',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['October', 'Wednesday', '1991', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2015-03-15',\
  'Name': u'Hannah Smith',\
  'Number': u'0438-235-871',\
  'StartDateTime': '2015-03-15',\
  'Text': u'Illum odit fugiat.',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['May', 'Friday', '1972', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2014-05-18',\
  'StartDateTime': '2014-05-18',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['December', 'Sunday', '1991', 'Tired'],\
  'latitude': -15.472293,\
  'longitude': -119.013169,\
  'type': 'Button'}, { 'EndDateTime': '2012-11-17',\
  'StartDateTime': '2012-11-17',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['April', 'Wednesday', '2015', 'Depressed'],\
  'latitude': -66.3184375,\
  'longitude': -144.802618,\
  'type': 'Button'}, { 'EndDateTime': '2011-03-09',\
  'Name': u'Colleen Contreras',\
  'Number': u'(08)-5193-5018',\
  'StartDateTime': '2011-03-09',\
  'Text': u'Omnis voluptatum qui aut aut.',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['April', 'Monday', '1985', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2011-08-20',\
  'Name': u'Stephen Chen',\
  'Number': u'9123-9171',\
  'StartDateTime': '2011-08-20',\
  'Text': u'Maxime cum nemo.',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['March', 'Thursday', '1987', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'Duration': 24,\
  'EndDateTime': '2015-10-05',\
  'Name': u'Patrick Hernandez',\
  'Number': u'+61-7-4452-8789',\
  'StartDateTime': '2015-10-05',\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'keywords': ['September', 'Friday', '1971', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 10,\
  'AudioProcessedCount': 10,\
  'BatteryCount': 7,\
  'BatteryLevel': 48,\
  'EndDateTime': '2016-06-20',\
  'Kilometers': 0.6812017558971871,\
  'LocationCount': 6,\
  'MoonAge': 8.509793598090535,\
  'MoonIllumination': 0.6903601453496996,\
  'StartDateTime': '2016-06-20',\
  'Temperature': 3.7263865509032392,\
  'UserId': 'ab4dd600-2d74-4147-b963-710e56c42089',\
  'Weather': 'rain',\
  'address': u'586 Little Quays\nPort Jacob, QLD, 2636',\
  'keywords': [ 'March',\
                'Monday',\
                '2014',\
                'winter',\
                'audio_home',\
                'audio_home',\
                'audio_street',\
                'rain',\
                'waning_gibbous',\
                'church'],\
  'latitude': 33.5329355,\
  'longitude': -85.546789,\
  'type': 'App'}, { 'EndDateTime': '2012-03-12',\
  'StartDateTime': '2012-03-12',\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'keywords': ['January', 'Monday', '1997', 'Tired'],\
  'latitude': -10.3664605,\
  'longitude': -158.056195,\
  'type': 'Button'}, { 'AccelerometryCount': 10,\
  'AudioProcessedCount': 11,\
  'BatteryCount': 6,\
  'BatteryLevel': 90,\
  'EndDateTime': '2016-07-21',\
  'Kilometers': 0.45179534112467307,\
  'LocationCount': 9,\
  'MoonAge': 22.77515614182604,\
  'MoonIllumination': 0.24222077967814926,\
  'StartDateTime': '2016-07-21',\
  'Temperature': 34.5616877625842,\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'Weather': 'overcast',\
  'address': u'Apt. 877\n 878 Eric Byway\nNicolemouth, VIC, 2661',\
  'keywords': [ 'March',\
                'Sunday',\
                '2001',\
                'winter',\
                'audio_home',\
                'audio_street',\
                'overcast',\
                'waning_gibbous'],\
  'latitude': 67.500942,\
  'longitude': -129.446196,\
  'type': 'App'}, { 'EndDateTime': '2015-07-10',\
  'StartDateTime': '2015-07-10',\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'keywords': ['July', 'Saturday', '2005', 'Happy'],\
  'latitude': 1.4064885,\
  'longitude': 92.10175,\
  'type': 'Button'}, { 'EndDateTime': '2018-02-25',\
  'Name': u'Charles Villarreal',\
  'Number': u'+61-3-0831-9704',\
  'StartDateTime': '2018-02-25',\
  'Text': u'Enim nam itaque dolorum nam.',\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'keywords': ['July', 'Tuesday', '2012', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'AccelerometryCount': 5,\
  'AudioProcessedCount': 12,\
  'BatteryCount': 3,\
  'BatteryLevel': 14,\
  'EndDateTime': '2010-11-14',\
  'Kilometers': 0.007955684824998718,\
  'LocationCount': 12,\
  'MoonAge': 23.76190712194256,\
  'MoonIllumination': 0.4116991670030795,\
  'StartDateTime': '2010-11-14',\
  'Temperature': 17.1266482840623,\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'Weather': 'rain',\
  'address': u'Suite 446\n 04 Michelle Frontage\nNew Annamouth, NT, 2744',\
  'keywords': [ 'May',\
                'Saturday',\
                '1984',\
                'summer',\
                'audio_car',\
                'rain',\
                'waning_gibbous'],\
  'latitude': -8.917936,\
  'longitude': 94.020107,\
  'type': 'App'}, { 'Duration': 20,\
  'EndDateTime': '2018-09-07',\
  'Name': u'Kristin Hoover',\
  'Number': u'4496 5992',\
  'StartDateTime': '2018-09-07',\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'keywords': ['March', 'Monday', '1973', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2011-03-16',\
  'From': u'tbuckley@holmes-barrett.edu',\
  'Message': u'Veritatis laudantium ea. Quisquam amet nesciunt nulla mollitia qui impedit. Id ea tempore eos quo fugiat.\nAt similique illum sed ad expedita. Cupiditate suscipit harum repellat perspiciatis minus voluptatum officia. Dignissimos asperiores deserunt.\nAperiam aspernatur facere unde quas assumenda laborum. Officiis natus quisquam sint nihil quis blanditiis.',\
  'StartDateTime': '2011-03-16',\
  'Subject': u'Quod cupiditate.',\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'keywords': ['April', 'Friday', '1972', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2014-10-15',\
  'StartDateTime': '2014-10-15',\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'keywords': ['July', 'Thursday', '1982', 'Tired'],\
  'latitude': 29.9588595,\
  'longitude': 101.274715,\
  'type': 'Button'}, { 'EndDateTime': '2012-01-10',\
  'Message': u'Eius animi nihil. Maiores hic maiores. Dolorem cum consequatur.\nIste et corporis aut voluptatum. Aut nisi reprehenderit cupiditate quia. Debitis reprehenderit officiis laboriosam.\nAssumenda maxime nam.\nEveniet suscipit dolorum. At nemo animi quisquam explicabo. Itaque eos autem doloribus quos beatae.\nSit eum doloremque debitis. Similique velit saepe labore sapiente nulla. Sunt officia veritatis.',\
  'StartDateTime': '2012-01-10',\
  'Subject': u'Voluptates facilis.',\
  'To': u'richardsondavid@gmail.com',\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'keywords': ['June', 'Thursday', '1984', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2015-09-09',\
  'Message': u'Sunt ab odit. Similique quisquam perferendis eaque nostrum. Doloribus suscipit rem dolorem ex numquam.\nSint nostrum nihil. Nulla deserunt quibusdam quam.\nRem deleniti impedit fugit consequatur dicta. Quis labore numquam. Provident aspernatur et placeat esse nihil vero.',\
  'StartDateTime': '2015-09-09',\
  'Subject': u'Ex nemo quaerat.',\
  'To': u'aaron41@hotmail.com.au',\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'keywords': ['January', 'Friday', '1991', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2017-08-25',\
  'Name': u'Lisa Dickson',\
  'Number': u'2765-7156',\
  'StartDateTime': '2017-08-25',\
  'Text': u'Nostrum mollitia maiores.',\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'keywords': ['December', 'Saturday', '2000', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2016-11-06',\
  'From': u'rebecca59@gmail.com',\
  'Message': u'Veritatis neque cumque consequatur. Enim nemo explicabo maiores ut doloribus. Impedit nulla accusamus nemo dolorum sequi.\nIpsum a eaque optio commodi recusandae aliquam omnis. Porro nobis ex consequuntur esse veritatis architecto. Voluptate cum mollitia expedita adipisci aut.',\
  'StartDateTime': '2016-11-06',\
  'Subject': u'Natus quae itaque.',\
  'UserId': 'dabefd67-add2-42fb-a7e0-97501fb23b59',\
  'keywords': ['August', 'Monday', '1978', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'Duration': 82,\
  'EndDateTime': '2010-02-04',\
  'Name': u'Alexander Moon',\
  'Number': u'+61.498.856.880',\
  'StartDateTime': '2010-02-04',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['February', 'Monday', '1994', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'Duration': 150,\
  'EndDateTime': '2012-06-20',\
  'Name': u'Rebecca Kirk',\
  'Number': u'(08)-6583-2165',\
  'StartDateTime': '2012-06-20',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['August', 'Saturday', '1970', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2015-01-06',\
  'Name': u'Margaret Snyder',\
  'Number': u'+61-408-591-095',\
  'StartDateTime': '2015-01-06',\
  'Text': u'Delectus at placeat qui.',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['August', 'Saturday', '1981', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2013-09-06',\
  'StartDateTime': '2013-09-06',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['October', 'Tuesday', '1994', 'Happy'],\
  'type': 'Button'}, { 'EndDateTime': '2018-02-15',\
  'Message': u'Repudiandae cupiditate quod consectetur sapiente quia ab. Dicta aperiam voluptas. Nostrum vel natus rerum commodi.\nDebitis molestias alias exercitationem similique corporis. Vero distinctio nesciunt adipisci.\nQuisquam nam officia voluptatum fuga. Est quisquam minus excepturi. Nam explicabo voluptatem magnam at laboriosam nam.',\
  'StartDateTime': '2018-02-15',\
  'Subject': u'Deleniti.',\
  'To': u'ujones@hawkins-fuentes.edu',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['December', 'Wednesday', '1991', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2013-09-10',\
  'Message': u'Natus alias corrupti iusto voluptatibus. Modi nulla quam deleniti quaerat. Voluptatum consequatur voluptatum illum ducimus earum.\nEa necessitatibus aperiam adipisci vitae similique quo. Facere sed temporibus expedita autem distinctio. Facilis labore corporis.\nPariatur labore laboriosam iure eos laborum atque quasi. Est molestiae expedita distinctio quod.',\
  'StartDateTime': '2013-09-10',\
  'Subject': u'Aliquid autem fugit.',\
  'To': u'jamieduran@yahoo.com',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['October', 'Tuesday', '2017', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2018-08-28',\
  'Name': u'Daniel Gomez',\
  'Number': u'+61 3 3123 8829',\
  'StartDateTime': '2018-08-28',\
  'Text': u'Maiores ipsa nam.',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['March', 'Friday', '1982', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2017-11-06',\
  'StartDateTime': '2017-11-06',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['January', 'Tuesday', '2011', 'Depressed'],\
  'latitude': -56.3447665,\
  'longitude': 179.112934,\
  'type': 'Button'}, { 'EndDateTime': '2013-04-28',\
  'From': u'christophergarza@henderson.edu',\
  'Message': u'Sint aliquid at eos. Ad dicta facere accusamus.\nQuo occaecati soluta sunt. Consectetur iure distinctio dolores id cum.\nCupiditate aliquam saepe quis reprehenderit alias. Quae enim omnis illo.\nDoloremque eius debitis tenetur. Optio corporis voluptate voluptates. Odio in dolores impedit repellat quis placeat.\nRepellendus temporibus cumque. Laborum sit veniam provident unde ratione architecto.',\
  'StartDateTime': '2013-04-28',\
  'Subject': u'Dolorem adipisci.',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['January', 'Saturday', '2013', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'Duration': 32,\
  'EndDateTime': '2018-01-13',\
  'Name': u'Richard Banks',\
  'Number': u'0400-071-017',\
  'StartDateTime': '2018-01-13',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['September', 'Wednesday', '1987', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 2,\
  'AudioProcessedCount': 7,\
  'BatteryCount': 8,\
  'BatteryLevel': 50,\
  'EndDateTime': '2012-01-01',\
  'Kilometers': 1.341591256574151,\
  'LocationCount': 11,\
  'MoonAge': 3.1525501859600036,\
  'MoonIllumination': 0.6035655571809329,\
  'StartDateTime': '2012-01-01',\
  'Temperature': 10.384045845637857,\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'Weather': 'cloudy',\
  'address': u'93 Mathis Broadway\nHoffmanchester, SA, 2685',\
  'keywords': [ 'June',\
                'Wednesday',\
                '1997',\
                'autumn',\
                'audio_voice',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': -55.2908735,\
  'longitude': -17.502356,\
  'type': 'App'}, { 'Duration': 157,\
  'EndDateTime': '2013-03-03',\
  'Name': u'Peter Weeks',\
  'Number': u'0886440091',\
  'StartDateTime': '2013-03-03',\
  'UserId': '9b7d53eb-d605-427c-84bc-2ccf4c3ca6db',\
  'keywords': ['November', 'Saturday', '1989', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 8,\
  'AudioProcessedCount': 2,\
  'BatteryCount': 11,\
  'BatteryLevel': 46,\
  'EndDateTime': '2011-09-05',\
  'Kilometers': 0.5266123288125109,\
  'LocationCount': 7,\
  'MoonAge': 24.995292700463423,\
  'MoonIllumination': 0.7198093104259032,\
  'StartDateTime': '2011-09-05',\
  'Temperature': 21.71027135757653,\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'Weather': 'overcast',\
  'address': u'319 Andrew Dip\nMichelleberg, NSW, 2619',\
  'keywords': [ 'January',\
                'Friday',\
                '1970',\
                'autumn',\
                'audio_voice',\
                'audio_home',\
                'audio_street',\
                'audio_home',\
                'audio_car',\
                'overcast',\
                'waxing_gibbous'],\
  'latitude': -7.6462705,\
  'longitude': 145.288537,\
  'type': 'App'}, { 'EndDateTime': '2018-10-10',\
  'From': u'angelica89@walker.edu',\
  'Message': u'Dignissimos quaerat debitis itaque. Cum ut quae facere ut.\nNihil aliquid aspernatur eveniet ipsa nostrum quos tenetur. Fuga non deleniti earum amet maiores. Porro reiciendis quo voluptate praesentium adipisci vitae.\nQuia eligendi laudantium repellat sapiente iure. Occaecati ipsam explicabo animi. Tempora harum nobis accusantium animi quod voluptatem.\nConsequuntur eum vero hic saepe commodi.',\
  'StartDateTime': '2018-10-10',\
  'Subject': u'Pariatur natus.',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['June', 'Saturday', '1984', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 5,\
  'AudioProcessedCount': 9,\
  'BatteryCount': 8,\
  'BatteryLevel': 98,\
  'EndDateTime': '2017-07-18',\
  'Kilometers': 0.1070094215874796,\
  'LocationCount': 9,\
  'MoonAge': 2.429677254150157,\
  'MoonIllumination': 0.7367018194101568,\
  'StartDateTime': '2017-07-18',\
  'Temperature': 24.63894405810067,\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'Weather': 'clear',\
  'address': u'Flat 89\n 3 Camacho Towers\nEast George, WA, 0271',\
  'keywords': [ 'September',\
                'Friday',\
                '1987',\
                'winter',\
                'audio_home',\
                'audio_car',\
                'clear',\
                'waning_gibbous'],\
  'latitude': 89.622431,\
  'longitude': -29.664608,\
  'type': 'App'}, { 'EndDateTime': '2016-09-02',\
  'Message': u'Vero dolore porro. Deserunt deleniti expedita vitae nesciunt. Nam repudiandae modi.\nVoluptate saepe dicta consequuntur sint atque corporis. Repudiandae ipsa cum fugit unde labore. Impedit voluptatum nam tempore excepturi provident.\nBeatae maxime libero quis ullam nostrum dignissimos. Deleniti perferendis itaque deleniti veniam nam.',\
  'StartDateTime': '2016-09-02',\
  'Subject': u'Voluptatibus ipsum.',\
  'To': u'sharonwilliams@gmail.com',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['April', 'Friday', '1986', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'Duration': 209,\
  'EndDateTime': '2014-05-09',\
  'Name': u'Luis Crosby',\
  'Number': u'8953 9049',\
  'StartDateTime': '2014-05-09',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['December', 'Monday', '1975', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2013-07-24',\
  'Name': u'Matthew Rodriguez',\
  'Number': u'(02)-1975-7946',\
  'StartDateTime': '2013-07-24',\
  'Text': u'Unde amet sunt.',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['July', 'Monday', '1990', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2013-03-05',\
  'StartDateTime': '2013-03-05',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['August', 'Saturday', '2016', 'Happy'],\
  'latitude': 64.861575,\
  'longitude': 64.259311,\
  'type': 'Button'}, { 'Duration': 230,\
  'EndDateTime': '2016-12-13',\
  'Name': u'Kimberly Villegas',\
  'Number': u'0883 5489',\
  'StartDateTime': '2016-12-13',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['April', 'Tuesday', '2012', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2018-05-25',\
  'Name': u'Kelly Hunt',\
  'Number': u'+61253887310',\
  'StartDateTime': '2018-05-25',\
  'Text': u'Rem iusto quisquam qui.',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['February', 'Thursday', '2001', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'AccelerometryCount': 2,\
  'AudioProcessedCount': 12,\
  'BatteryCount': 2,\
  'BatteryLevel': 76,\
  'EndDateTime': '2010-05-01',\
  'StartDateTime': '2010-05-01',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['June', 'Friday', '1995', 'spring', 'audio_voice'],\
  'type': 'App'}, { 'Duration': 89,\
  'EndDateTime': '2017-12-09',\
  'Name': u'Joseph Silva',\
  'Number': u'+61.487.716.725',\
  'StartDateTime': '2017-12-09',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['July', 'Thursday', '1975', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2011-03-25',\
  'Name': u'Elizabeth Smith',\
  'Number': u'+61-488-997-895',\
  'StartDateTime': '2011-03-25',\
  'Text': u'Similique ullam earum.',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['July', 'Friday', '2015', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'AccelerometryCount': 9,\
  'AudioProcessedCount': 12,\
  'BatteryCount': 2,\
  'BatteryLevel': 59,\
  'EndDateTime': '2014-08-17',\
  'Kilometers': 0.755169451115481,\
  'LocationCount': 1,\
  'MoonAge': 3.701644370296999,\
  'MoonIllumination': 0.8169325187737803,\
  'StartDateTime': '2014-08-17',\
  'Temperature': 23.60924288127185,\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'Weather': 'rain',\
  'address': u'9 Garcia Track\nWebbbury, QLD, 4308',\
  'keywords': [ 'January',\
                'Friday',\
                '1996',\
                'spring',\
                'audio_voice',\
                'rain',\
                'waning_gibbous'],\
  'latitude': 50.3559195,\
  'longitude': -23.033461,\
  'type': 'App'}, { 'AccelerometryCount': 10,\
  'AudioProcessedCount': 8,\
  'BatteryCount': 3,\
  'BatteryLevel': 81,\
  'EndDateTime': '2015-04-05',\
  'Kilometers': 0.3861894806571407,\
  'LocationCount': 5,\
  'MoonAge': 3.1593650395379793,\
  'MoonIllumination': 0.9711487557401628,\
  'StartDateTime': '2015-04-05',\
  'Temperature': 18.795957524688962,\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'Weather': 'overcast',\
  'address': u'61 Kaitlyn Crescent\nNavarrobury, ACT, 2619',\
  'keywords': [ 'February',\
                'Saturday',\
                '2000',\
                'autumn',\
                'audio_home',\
                'overcast',\
                'waxing_gibbous'],\
  'latitude': 52.268653,\
  'longitude': 22.375472,\
  'type': 'App'}, { 'EndDateTime': '2016-08-13',\
  'StartDateTime': '2016-08-13',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['September', 'Sunday', '2010', 'Happy'],\
  'latitude': 89.2369285,\
  'longitude': 59.273725,\
  'type': 'Button'}, { 'EndDateTime': '2015-12-10',\
  'From': u'mjohnson@yahoo.com',\
  'Message': u'Nihil ipsa repudiandae eligendi id numquam. Minus minus nisi molestias. Hic quis at.\nVeniam voluptate architecto vel voluptatem beatae accusamus ad. Itaque expedita quae repellat. A deleniti minus veritatis.\nVero ad quasi voluptatem perferendis quia laborum. Ab voluptatum cum dolore unde voluptatibus est. Commodi dolores qui quibusdam doloribus necessitatibus debitis. Autem nemo ratione.',\
  'StartDateTime': '2015-12-10',\
  'Subject': u'Fugiat odit sint.',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['February', 'Sunday', '1995', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 9,\
  'AudioProcessedCount': 5,\
  'BatteryCount': 1,\
  'BatteryLevel': 87,\
  'EndDateTime': '2010-03-22',\
  'Kilometers': 4.18447917484531,\
  'LocationCount': 7,\
  'MoonAge': 0.05689286043939368,\
  'MoonIllumination': 0.012269907892275,\
  'StartDateTime': '2010-03-22',\
  'Temperature': 24.1949147551314,\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'Weather': 'rain',\
  'address': u'123 Alexander Riverway\nCarolyntown, SA, 2361',\
  'keywords': [ 'April',\
                'Sunday',\
                '1976',\
                'winter',\
                'audio_home',\
                'rain',\
                'waxing_gibbous'],\
  'latitude': -22.428295,\
  'longitude': -94.843754,\
  'type': 'App'}, { 'EndDateTime': '2010-11-04',\
  'From': u'townsendjasmine@hotmail.com.au',\
  'Message': u'Nam quo suscipit nostrum. Ad quibusdam nihil asperiores ab cupiditate blanditiis aliquam.\nDolorem nobis porro. Repellendus odio eum ipsa.\nBeatae quidem deleniti neque maiores at. Assumenda assumenda corrupti quae ipsam dicta autem.\nDebitis mollitia distinctio explicabo consectetur ex.\nQuas sed modi soluta doloremque. Molestias occaecati illum nesciunt asperiores corporis totam.',\
  'StartDateTime': '2010-11-04',\
  'Subject': u'Sit voluptate.',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['March', 'Friday', '1997', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2010-02-05',\
  'Name': u'Misty Reeves',\
  'Number': u'+61.431.528.917',\
  'StartDateTime': '2010-02-05',\
  'Text': u'Omnis magnam vel veniam.',\
  'UserId': '00d1ebe7-0ad6-4d97-8529-94c6ee77fc4e',\
  'keywords': ['October', 'Saturday', '2003', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2012-10-03',\
  'From': u'yhall@yahoo.com',\
  'Message': u'Libero odio omnis.\nAb autem doloribus omnis. Laborum numquam distinctio nobis libero. Molestias sit ad expedita autem.\nRem ducimus distinctio similique omnis voluptatem. Rerum eveniet ratione recusandae aperiam alias aperiam officiis. Totam incidunt nisi maxime et.\nNeque illo tempore aliquid ipsam odio. Libero ipsam unde repellendus veniam impedit temporibus. Illo sequi perspiciatis.',\
  'StartDateTime': '2012-10-03',\
  'Subject': u'Veritatis hic earum.',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['January', 'Wednesday', '2004', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2014-05-03',\
  'StartDateTime': '2014-05-03',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['January', 'Sunday', '1998', 'Happy'],\
  'latitude': -4.004671,\
  'longitude': -107.770361,\
  'type': 'Button'}, { 'Duration': 71,\
  'EndDateTime': '2015-03-24',\
  'Name': u'Samantha Mitchell',\
  'Number': u'03-1441-3608',\
  'StartDateTime': '2015-03-24',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['June', 'Wednesday', '1985', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'Duration': 190,\
  'EndDateTime': '2010-12-25',\
  'Name': u'Brian May',\
  'Number': u'(02) 0781 2538',\
  'StartDateTime': '2010-12-25',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['November', 'Monday', '2002', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'Duration': 0,\
  'EndDateTime': '2011-07-03',\
  'Name': u'Sean King MD',\
  'Number': u'(02)27465385',\
  'StartDateTime': '2011-07-03',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['March', 'Tuesday', '1976', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2013-10-21',\
  'Message': u'Eligendi consequatur vitae repellendus unde necessitatibus. Nemo porro iste non dolorum modi rem sapiente. Nesciunt deserunt saepe enim.\nOmnis blanditiis officiis sint alias fugit fugit. Tempora expedita vel delectus illo ut. Et iste aperiam architecto id.',\
  'StartDateTime': '2013-10-21',\
  'Subject': u'Pariatur porro.',\
  'To': u'jennaford@hotmail.com.au',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['February', 'Wednesday', '1996', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2018-10-14',\
  'Message': u'Quibusdam quae cumque ullam maxime labore. Nisi nisi dolorum libero. Numquam delectus ad quaerat voluptates.\nVel ullam expedita.\nDolore suscipit ex voluptate velit fuga. Accusamus dolore quibusdam sint quia.\nCulpa expedita minima laboriosam dicta asperiores libero. Eum tenetur fugiat soluta porro optio. Ex voluptates vero vel.\nExercitationem molestias ad corrupti nostrum.',\
  'StartDateTime': '2018-10-14',\
  'Subject': u'Maiores perferendis.',\
  'To': u'jessicadillon@yahoo.com.au',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['October', 'Sunday', '1974', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 1,\
  'AudioProcessedCount': 11,\
  'BatteryCount': 10,\
  'BatteryLevel': 93,\
  'EndDateTime': '2012-12-01',\
  'Kilometers': 0.09173101741299865,\
  'LocationCount': 4,\
  'MoonAge': 26.146021450373134,\
  'MoonIllumination': 0.7404096869827962,\
  'StartDateTime': '2012-12-01',\
  'Temperature': 2.946558155326718,\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'Weather': 'cloudy',\
  'address': u'Apt. 166\n 93 Stephanie Service Way\nPort Williestad, ACT, 7263',\
  'keywords': [ 'March',\
                'Saturday',\
                '1980',\
                'spring',\
                'audio_voice',\
                'cloudy',\
                'waxing_gibbous'],\
  'latitude': -12.3589105,\
  'longitude': 134.439857,\
  'type': 'App'}, { 'EndDateTime': '2015-03-28',\
  'From': u'samuel54@yang.org',\
  'Message': u'Soluta placeat deleniti animi perferendis nam consectetur ipsa. Officiis beatae iusto illo exercitationem.\nDebitis quas natus ex quibusdam. Autem dolorem ad ratione inventore.\nDelectus eveniet quaerat aliquid quo. Minima omnis sed quod ipsa est explicabo.',\
  'StartDateTime': '2015-03-28',\
  'Subject': u'Debitis mollitia.',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['April', 'Sunday', '1994', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'Duration': 234,\
  'EndDateTime': '2018-03-18',\
  'Name': u'Brian Ford',\
  'Number': u'3186 6204',\
  'StartDateTime': '2018-03-18',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['September', 'Monday', '1982', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2011-08-16',\
  'Message': u'Quisquam itaque quis totam cumque accusantium voluptatum voluptate. Reprehenderit labore alias voluptates veritatis occaecati placeat.\nEveniet repellat earum. Rem perspiciatis libero. Soluta adipisci sed itaque dicta eaque. Dignissimos ut iure modi iure nihil.\nOccaecati temporibus at voluptatibus necessitatibus. Deserunt nam labore ratione saepe. Cupiditate ipsa nostrum sequi.',\
  'StartDateTime': '2011-08-16',\
  'Subject': u'Nesciunt cupiditate.',\
  'To': u'joseph30@gmail.com',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['July', 'Friday', '1990', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2014-12-23',\
  'Name': u'Sarah Palmer',\
  'Number': u'+61 408 093 536',\
  'StartDateTime': '2014-12-23',\
  'Text': u'Voluptates cumque eaque eos.',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['April', 'Thursday', '2006', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2013-08-09',\
  'From': u'amanda34@hotmail.com',\
  'Message': u'Dicta dignissimos hic quibusdam ad excepturi deleniti. Dolorum doloribus asperiores.\nPlaceat delectus nulla laborum. Nemo perspiciatis animi recusandae voluptatibus reprehenderit facilis adipisci. Provident atque molestiae ipsum.\nSoluta ducimus optio ad. Porro libero ullam maxime magnam laborum dolore.\nIpsa dignissimos fugiat maiores asperiores cum iste. Saepe ipsam recusandae accusantium.',\
  'StartDateTime': '2013-08-09',\
  'Subject': u'Sint amet.',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['May', 'Friday', '1992', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2014-10-21',\
  'StartDateTime': '2014-10-21',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['September', 'Sunday', '2016', 'Happy'],\
  'latitude': 73.849729,\
  'longitude': 25.951263,\
  'type': 'Button'}, { 'EndDateTime': '2014-10-13',\
  'Name': u'Daniel Wilson',\
  'Number': u'03 6681 6746',\
  'StartDateTime': '2014-10-13',\
  'Text': u'Nobis mollitia amet veniam.',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['July', 'Monday', '1995', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'Duration': 22,\
  'EndDateTime': '2016-01-19',\
  'Name': u'Craig Maddox',\
  'Number': u'6079.4871',\
  'StartDateTime': '2016-01-19',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['May', 'Wednesday', '1989', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2013-12-20',\
  'From': u'rebeccaware@hotmail.com.au',\
  'Message': u'Quam velit neque animi voluptatibus excepturi iusto. Neque ipsam eum neque voluptatum quisquam. Explicabo accusantium eveniet quisquam molestiae commodi temporibus.\nTenetur voluptate fugiat alias accusamus. Sed perspiciatis illo est nesciunt eligendi qui. Eius corrupti placeat aliquam cupiditate itaque nihil.\nPlaceat voluptas a laudantium nihil. Dolorem ea aspernatur eum quasi voluptates.',\
  'StartDateTime': '2013-12-20',\
  'Subject': u'Rerum iusto.',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['March', 'Tuesday', '2017', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2013-03-01',\
  'Name': u'Caleb Sharp',\
  'Number': u'(07).3370.0776',\
  'StartDateTime': '2013-03-01',\
  'Text': u'Reprehenderit nulla magnam.',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['November', 'Thursday', '1994', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2016-12-04',\
  'StartDateTime': '2016-12-04',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['May', 'Tuesday', '1976', 'Excited'],\
  'latitude': 76.8109835,\
  'longitude': 149.858472,\
  'type': 'Button'}, { 'AccelerometryCount': 5,\
  'AudioProcessedCount': 2,\
  'BatteryCount': 4,\
  'BatteryLevel': 23,\
  'EndDateTime': '2015-10-30',\
  'StartDateTime': '2015-10-30',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': [ 'March',\
                'Friday',\
                '1978',\
                'autumn',\
                'audio_street',\
                'audio_voice'],\
  'type': 'App'}, { 'EndDateTime': '2017-06-10',\
  'Name': u'Grace Martinez',\
  'Number': u'02.9271.9569',\
  'StartDateTime': '2017-06-10',\
  'Text': u'Odio fuga nostrum quia.',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['March', 'Tuesday', '1977', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'AccelerometryCount': 7,\
  'AudioProcessedCount': 10,\
  'BatteryCount': 1,\
  'BatteryLevel': 4,\
  'EndDateTime': '2010-06-23',\
  'Kilometers': 0.7725353582593237,\
  'LocationCount': 2,\
  'MoonAge': 0.6050048615346615,\
  'MoonIllumination': 0.27883499445067406,\
  'StartDateTime': '2010-06-23',\
  'Temperature': 23.840782683939977,\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'Weather': 'rain',\
  'address': u'063 Robinson Lookout\nPotterfurt, QLD, 2058',\
  'keywords': [ 'July',\
                'Wednesday',\
                '1974',\
                'winter',\
                'audio_car',\
                'audio_voice',\
                'rain',\
                'waxing_gibbous'],\
  'latitude': 18.827169,\
  'longitude': 93.789238,\
  'type': 'App'}, { 'EndDateTime': '2017-04-07',\
  'StartDateTime': '2017-04-07',\
  'UserId': 'aa6fc8db-a5c8-4415-9c9d-3bb94b496c3a',\
  'keywords': ['December', 'Wednesday', '2016', 'Happy'],\
  'latitude': 7.63836,\
  'longitude': -108.632142,\
  'type': 'Button'}, { 'AccelerometryCount': 9,\
  'AudioProcessedCount': 5,\
  'BatteryCount': 7,\
  'BatteryLevel': 40,\
  'EndDateTime': '2014-02-17',\
  'Kilometers': 0.33827392460795547,\
  'LocationCount': 10,\
  'MoonAge': 1.838434710386222,\
  'MoonIllumination': 0.2402056860852395,\
  'StartDateTime': '2014-02-17',\
  'Temperature': 15.085701300351044,\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'Weather': 'overcast',\
  'address': u'Apt. 632\n 8 Foster Anchorage\nSouth Davidmouth, VIC, 2920',\
  'keywords': [ 'December',\
                'Saturday',\
                '2008',\
                'summer',\
                'audio_car',\
                'overcast',\
                'waning_gibbous',\
                'church'],\
  'latitude': -45.4238765,\
  'longitude': 173.589012,\
  'type': 'App'}, { 'Duration': 7,\
  'EndDateTime': '2012-06-30',\
  'Name': u'David Lee',\
  'Number': u'0415-013-908',\
  'StartDateTime': '2012-06-30',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['December', 'Monday', '2016', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2017-11-07',\
  'From': u'james66@yahoo.com.au',\
  'Message': u'Dolor voluptate suscipit ad modi minus quo. Ullam rerum quos nihil non at.\nDolorum nesciunt quae exercitationem deleniti nesciunt eligendi. Voluptatibus officia nesciunt sint molestiae fugiat.\nMaiores ipsam architecto voluptates quo sunt quae. Quasi iure non illo quo.\nVoluptatem quaerat suscipit blanditiis explicabo architecto non cumque. Necessitatibus consequatur similique voluptatibus.',\
  'StartDateTime': '2017-11-07',\
  'Subject': u'Qui aperiam quidem.',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['November', 'Thursday', '2018', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'Duration': 1,\
  'EndDateTime': '2018-08-07',\
  'Name': u'Nicholas Velez',\
  'Number': u'03 0943 4419',\
  'StartDateTime': '2018-08-07',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['September', 'Tuesday', '1973', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 2,\
  'AudioProcessedCount': 12,\
  'BatteryCount': 1,\
  'BatteryLevel': 16,\
  'EndDateTime': '2012-02-05',\
  'Kilometers': 0.42256989074512336,\
  'LocationCount': 2,\
  'MoonAge': 22.299960332214347,\
  'MoonIllumination': 0.7282364662289609,\
  'StartDateTime': '2012-02-05',\
  'Temperature': 14.343905508708955,\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'Weather': 'clear',\
  'address': u'417 Watson Retreat\nTurnerchester, QLD, 2636',\
  'keywords': [ 'July',\
                'Friday',\
                '2013',\
                'winter',\
                'audio_street',\
                'clear',\
                'waning_gibbous'],\
  'latitude': -82.4293265,\
  'longitude': -13.105132,\
  'type': 'App'}, { 'EndDateTime': '2014-02-07',\
  'Name': u'David Massey',\
  'Number': u'+61-400-659-689',\
  'StartDateTime': '2014-02-07',\
  'Text': u'Vero nobis officia occaecati.',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['January', 'Tuesday', '2007', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2014-11-01',\
  'From': u'james94@gmail.com',\
  'Message': u'Earum occaecati debitis. Voluptatem modi consequuntur voluptate similique expedita ipsa.\nRepudiandae eaque nulla alias tempore molestiae neque numquam. Ipsam eveniet facilis in repellat accusantium et. Illum id cumque nam dolore soluta.\nTempore id maxime inventore. Ipsum laudantium delectus unde voluptatem eius quibusdam.',\
  'StartDateTime': '2014-11-01',\
  'Subject': u'Blanditiis corrupti.',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['July', 'Monday', '1978', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 6,\
  'AudioProcessedCount': 12,\
  'BatteryCount': 5,\
  'BatteryLevel': 92,\
  'EndDateTime': '2015-08-10',\
  'Kilometers': 0.2952425762631851,\
  'LocationCount': 6,\
  'MoonAge': 6.111514413589961,\
  'MoonIllumination': 0.6992955330711368,\
  'StartDateTime': '2015-08-10',\
  'Temperature': 20.220188775071076,\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'Weather': 'cloudy',\
  'address': u'7 Smith Flat\nNorth Deborah, ACT, 2691',\
  'keywords': [ 'November',\
                'Sunday',\
                '1992',\
                'summer',\
                'audio_car',\
                'audio_home',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': 26.299329,\
  'longitude': -120.903419,\
  'type': 'App'}, { 'EndDateTime': '2016-04-12',\
  'Name': u'Donald Cox',\
  'Number': u'(08)20525121',\
  'StartDateTime': '2016-04-12',\
  'Text': u'Rem ad exercitationem.',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['March', 'Tuesday', '1986', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'Duration': 14,\
  'EndDateTime': '2013-10-19',\
  'Name': u'Rachael Chase',\
  'Number': u'9638 0302',\
  'StartDateTime': '2013-10-19',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['July', 'Friday', '1987', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'Duration': 42,\
  'EndDateTime': '2010-10-11',\
  'Name': u'Alexander Chaney',\
  'Number': u'44626569',\
  'StartDateTime': '2010-10-11',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['January', 'Friday', '2003', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2016-12-24',\
  'Message': u'Minus officiis sapiente soluta eaque reiciendis nobis saepe. Impedit dicta fugit ullam dolor. Corrupti ducimus maiores quibusdam earum quibusdam consequuntur.\nQuo repellendus ad rem. Distinctio ex dolor assumenda vitae mollitia aliquid. Fuga ad hic at numquam numquam.',\
  'StartDateTime': '2016-12-24',\
  'Subject': u'In asperiores.',\
  'To': u'brittanybrown@clark.info',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['May', 'Saturday', '2017', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'Duration': 357,\
  'EndDateTime': '2012-07-29',\
  'Name': u'Timothy Ramos',\
  'Number': u'0460-933-096',\
  'StartDateTime': '2012-07-29',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['June', 'Monday', '1984', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 1,\
  'AudioProcessedCount': 3,\
  'BatteryCount': 12,\
  'BatteryLevel': 60,\
  'EndDateTime': '2010-04-08',\
  'Kilometers': 0.12916963506616916,\
  'LocationCount': 6,\
  'MoonAge': 0.09672500999793665,\
  'MoonIllumination': 0.3902711186759218,\
  'StartDateTime': '2010-04-08',\
  'Temperature': 27.392446628162638,\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'Weather': 'cloudy',\
  'address': u'2 Ramirez Wynd\nPort Derek, SA, 2945',\
  'keywords': [ 'October',\
                'Monday',\
                '1995',\
                'summer',\
                'audio_voice',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': 57.2129275,\
  'longitude': -8.894742,\
  'type': 'App'}, { 'EndDateTime': '2010-04-05',\
  'StartDateTime': '2010-04-05',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['November', 'Saturday', '1976', 'Tired'],\
  'latitude': 12.978343,\
  'longitude': -65.233604,\
  'type': 'Button'}, { 'EndDateTime': '2016-08-22',\
  'StartDateTime': '2016-08-22',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['May', 'Saturday', '1978', 'Depressed'],\
  'latitude': -20.2999605,\
  'longitude': 40.091934,\
  'type': 'Button'}, { 'EndDateTime': '2017-07-08',\
  'StartDateTime': '2017-07-08',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['October', 'Friday', '1997', 'Depressed'],\
  'latitude': 42.5254565,\
  'longitude': -112.681907,\
  'type': 'Button'}, { 'EndDateTime': '2015-10-07',\
  'From': u'denisecooper@michael-harrison.org',\
  'Message': u'Cupiditate esse deleniti delectus ratione libero omnis. Enim tempora sed maiores sit sit. Reiciendis repellendus cumque distinctio beatae quis velit blanditiis.\nSuscipit odio modi tenetur. Quos laborum harum quisquam.\nAtque ipsam vel rem. Tempora autem necessitatibus consequuntur aliquid.',\
  'StartDateTime': '2015-10-07',\
  'Subject': u'Veniam fugit facere.',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['December', 'Tuesday', '1988', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2010-07-29',\
  'From': u'brendaholland@hotmail.com',\
  'Message': u'Neque molestias officiis molestias distinctio nam. Iure suscipit soluta numquam commodi dolores beatae. Alias assumenda deserunt similique magnam accusantium. Nihil tempore quibusdam corrupti unde.\nNulla natus impedit iusto sunt ipsum voluptate. Assumenda sit recusandae nihil itaque. Omnis quod aspernatur deserunt impedit reprehenderit sapiente.',\
  'StartDateTime': '2010-07-29',\
  'Subject': u'Perferendis optio.',\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'keywords': ['February', 'Friday', '1995', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 3,\
  'AudioProcessedCount': 4,\
  'BatteryCount': 11,\
  'BatteryLevel': 31,\
  'EndDateTime': '2010-07-22',\
  'Kilometers': 0.643969909778758,\
  'LocationCount': 10,\
  'MoonAge': 16.513476754863856,\
  'MoonIllumination': 0.24939660838090116,\
  'StartDateTime': '2010-07-22',\
  'Temperature': 14.886915226014633,\
  'UserId': 'b7a4590f-45a4-4247-bb5a-53b5b40f6cac',\
  'Weather': 'overcast',\
  'address': u'058 Tonya Flat\nPort Andreastad, QLD, 2610',\
  'keywords': [ 'May',\
                'Sunday',\
                '2005',\
                'autumn',\
                'audio_car',\
                'audio_home',\
                'overcast',\
                'waxing_gibbous'],\
  'latitude': -30.849749,\
  'longitude': 73.234921,\
  'type': 'App'}, { 'EndDateTime': '2014-11-15',\
  'StartDateTime': '2014-11-15',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['January', 'Monday', '2003', 'Tired'],\
  'latitude': -13.8750905,\
  'longitude': -177.40682,\
  'type': 'Button'}, { 'EndDateTime': '2014-03-10',\
  'Name': u'Steven Ortiz',\
  'Number': u'0483 469 328',\
  'StartDateTime': '2014-03-10',\
  'Text': u'Ratione commodi eligendi ea.',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['September', 'Friday', '1991', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2015-02-18',\
  'StartDateTime': '2015-02-18',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['April', 'Saturday', '2005', 'Tired'],\
  'latitude': 67.741881,\
  'longitude': -145.591981,\
  'type': 'Button'}, { 'EndDateTime': '2012-12-24',\
  'Name': u'Joseph Davis',\
  'Number': u'0228613370',\
  'StartDateTime': '2012-12-24',\
  'Text': u'Natus corporis laborum minus.',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['October', 'Sunday', '2016', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'Duration': 15,\
  'EndDateTime': '2010-02-07',\
  'Name': u'Norma Paul',\
  'Number': u'08.4206.5245',\
  'StartDateTime': '2010-02-07',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['November', 'Thursday', '1996', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2016-06-14',\
  'From': u'victorwalker@yahoo.com',\
  'Message': u'Quis maiores soluta esse quasi maxime. Similique inventore tenetur consectetur officia.\nAliquid ex asperiores in esse libero. Odio at ea assumenda hic aspernatur iure.\nUllam laudantium ipsum perspiciatis. Magni voluptas nobis asperiores quaerat consequatur doloremque. Deserunt dignissimos consequatur vero temporibus.',\
  'StartDateTime': '2016-06-14',\
  'Subject': u'Perferendis labore.',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['November', 'Wednesday', '1998', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'Duration': 38,\
  'EndDateTime': '2014-07-06',\
  'Name': u'Emily Lee',\
  'Number': u'2686 9635',\
  'StartDateTime': '2014-07-06',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['November', 'Tuesday', '1993', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2016-10-14',\
  'Name': u'Leslie Vaughan',\
  'Number': u'2457.8846',\
  'StartDateTime': '2016-10-14',\
  'Text': u'Labore ullam veritatis quod.',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['January', 'Tuesday', '2005', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'Duration': 96,\
  'EndDateTime': '2015-02-02',\
  'Name': u'Luke Garza',\
  'Number': u'+61 8 9887 6569',\
  'StartDateTime': '2015-02-02',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['January', 'Thursday', '1970', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2016-08-16',\
  'From': u'eroberts@olsen-fowler.org.au',\
  'Message': u'Nam necessitatibus perspiciatis corrupti quibusdam totam iure. Aliquid excepturi voluptatum aspernatur eos rem perferendis voluptatum.\nLaborum officia occaecati optio. Nesciunt impedit sapiente ratione facilis. Dicta provident odit quis.\nFacilis placeat autem voluptatum. Ut rem harum natus. Culpa vero quos optio. Expedita nobis voluptas corporis neque asperiores.',\
  'StartDateTime': '2016-08-16',\
  'Subject': u'Est quaerat.',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['August', 'Thursday', '1980', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 6,\
  'AudioProcessedCount': 10,\
  'BatteryCount': 3,\
  'BatteryLevel': 87,\
  'EndDateTime': '2012-10-30',\
  'Kilometers': 0.8777750387271577,\
  'LocationCount': 9,\
  'MoonAge': 5.378328237738124,\
  'MoonIllumination': 0.2532869798150763,\
  'StartDateTime': '2012-10-30',\
  'Temperature': 12.661824865276737,\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'Weather': 'rain',\
  'address': u'58 Smith Boulevard\nLake Robert, WA, 2598',\
  'keywords': [ 'August',\
                'Saturday',\
                '1999',\
                'summer',\
                'audio_home',\
                'audio_street',\
                'rain',\
                'waxing_gibbous'],\
  'latitude': -81.934917,\
  'longitude': 165.670073,\
  'type': 'App'}, { 'EndDateTime': '2012-08-26',\
  'From': u'ethan15@brown-martinez.edu',\
  'Message': u'Ipsa expedita dicta qui. Minima nulla eius dignissimos ex. Nesciunt minima magnam omnis molestias nisi tenetur.\nEst nisi vel ut aperiam voluptatem delectus. Fugiat ducimus quisquam facilis placeat. Distinctio magni veniam commodi quisquam at quae.\nConsequatur inventore eveniet. Aperiam totam unde odio voluptate minima. Molestias iste eos at soluta quae in.',\
  'StartDateTime': '2012-08-26',\
  'Subject': u'Molestiae nesciunt.',\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'keywords': ['April', 'Friday', '2013', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 11,\
  'AudioProcessedCount': 6,\
  'BatteryCount': 4,\
  'BatteryLevel': 6,\
  'EndDateTime': '2012-11-14',\
  'Kilometers': 0.08699487724829241,\
  'LocationCount': 10,\
  'MoonAge': 23.27144691582733,\
  'MoonIllumination': 0.19952991540552223,\
  'StartDateTime': '2012-11-14',\
  'Temperature': 16.84533046024643,\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'Weather': 'rain',\
  'address': u'9 /\n 7 Fisher Promenade\nWest Heidi, QLD, 2949',\
  'keywords': [ 'January',\
                'Friday',\
                '1970',\
                'summer',\
                'audio_street',\
                'audio_car',\
                'rain',\
                'waning_gibbous',\
                'cafe'],\
  'latitude': 40.52534,\
  'longitude': -91.667748,\
  'type': 'App'}, { 'AccelerometryCount': 3,\
  'AudioProcessedCount': 2,\
  'BatteryCount': 11,\
  'BatteryLevel': 93,\
  'EndDateTime': '2017-04-12',\
  'Kilometers': 1.1989865701676907,\
  'LocationCount': 6,\
  'MoonAge': 6.805957909676903,\
  'MoonIllumination': 0.1193340835105563,\
  'StartDateTime': '2017-04-12',\
  'Temperature': 5.017628629602958,\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'Weather': 'overcast',\
  'address': u'782 Tami Part\nTerryville, SA, 2373',\
  'keywords': [ 'May',\
                'Friday',\
                '1999',\
                'summer',\
                'audio_car',\
                'audio_home',\
                'overcast',\
                'waxing_gibbous'],\
  'latitude': -45.469404,\
  'longitude': -3.240605,\
  'type': 'App'}, { 'AccelerometryCount': 8,\
  'AudioProcessedCount': 5,\
  'BatteryCount': 7,\
  'BatteryLevel': 17,\
  'EndDateTime': '2012-02-24',\
  'Kilometers': 0.28843088878573925,\
  'LocationCount': 7,\
  'MoonAge': 29.350939998882936,\
  'MoonIllumination': 0.8631908992564248,\
  'StartDateTime': '2012-02-24',\
  'Temperature': 32.27508693394626,\
  'UserId': '1c26bef3-3a6d-4abc-8cc1-553eb7ac2883',\
  'Weather': 'rain',\
  'address': u'2 Berry Upper\nPort Williammouth, SA, 2576',\
  'keywords': [ 'February',\
                'Monday',\
                '2013',\
                'spring',\
                'audio_home',\
                'rain',\
                'waning_gibbous'],\
  'latitude': 36.211055,\
  'longitude': -49.229847,\
  'type': 'App'}, { 'Duration': 15,\
  'EndDateTime': '2017-05-20',\
  'Name': u'Maria Ball',\
  'Number': u'+61-3-5109-4671',\
  'StartDateTime': '2017-05-20',\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'keywords': ['September', 'Friday', '2017', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'Duration': 103,\
  'EndDateTime': '2016-02-11',\
  'Name': u'Corey Gonzalez',\
  'Number': u'+61.443.573.724',\
  'StartDateTime': '2016-02-11',\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'keywords': ['June', 'Wednesday', '1978', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2016-01-08',\
  'Name': u'Maria Mathews',\
  'Number': u'(08).1275.0133',\
  'StartDateTime': '2016-01-08',\
  'Text': u'Nisi inventore quas.',\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'keywords': ['July', 'Wednesday', '1975', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'AccelerometryCount': 9,\
  'AudioProcessedCount': 12,\
  'BatteryCount': 8,\
  'BatteryLevel': 90,\
  'EndDateTime': '2013-06-06',\
  'Kilometers': 3.3604953010593475,\
  'LocationCount': 3,\
  'MoonAge': 10.65254292755829,\
  'MoonIllumination': 0.39300315840423883,\
  'StartDateTime': '2013-06-06',\
  'Temperature': 7.880517966988727,\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'Weather': 'clear',\
  'address': u'17 Cathy Ramp\nLake Stacy, ACT, 3450',\
  'keywords': [ 'November',\
                'Thursday',\
                '1992',\
                'winter',\
                'audio_home',\
                'clear',\
                'waxing_gibbous'],\
  'latitude': -89.7713785,\
  'longitude': 86.515018,\
  'type': 'App'}, { 'EndDateTime': '2011-08-14',\
  'StartDateTime': '2011-08-14',\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'keywords': ['December', 'Tuesday', '2012', 'Happy'],\
  'latitude': -31.4759755,\
  'longitude': 164.363034,\
  'type': 'Button'}, { 'EndDateTime': '2013-03-21',\
  'StartDateTime': '2013-03-21',\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'keywords': ['December', 'Tuesday', '2004', 'Excited'],\
  'latitude': -59.171095,\
  'longitude': -34.088078,\
  'type': 'Button'}, { 'EndDateTime': '2017-03-26',\
  'Name': u'Kimberly Miller',\
  'Number': u'9058-3179',\
  'StartDateTime': '2017-03-26',\
  'Text': u'Nobis ut quas eligendi.',\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'keywords': ['July', 'Tuesday', '1990', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'Duration': 421,\
  'EndDateTime': '2012-08-12',\
  'Name': u'Tony Griffin',\
  'Number': u'+61709653140',\
  'StartDateTime': '2012-08-12',\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'keywords': ['May', 'Wednesday', '1973', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2010-06-10',\
  'From': u'christinachan@morgan-campos.org.au',\
  'Message': u'Omnis laboriosam assumenda amet assumenda voluptas error. Eligendi laudantium ea cum enim error recusandae. A cupiditate doloribus.\nVoluptatibus illum enim sapiente assumenda excepturi. Eveniet saepe ab consequatur beatae suscipit deserunt.\nInventore dicta id laudantium reprehenderit. Optio rerum repellendus aspernatur.',\
  'StartDateTime': '2010-06-10',\
  'Subject': u'Nobis nihil nemo.',\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'keywords': ['July', 'Tuesday', '1988', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2010-08-14',\
  'Message': u'Unde aspernatur molestias tempore quidem illum dolorem. Quos nesciunt consequatur iste veritatis ducimus nulla. Dolorem quaerat architecto.\nDolores voluptatibus odit cum. Placeat vitae modi velit at. Magni suscipit molestias. Iste explicabo deserunt nulla iusto temporibus.\nLibero facilis nihil. In beatae dolore voluptates iure ex quibusdam fuga.',\
  'StartDateTime': '2010-08-14',\
  'Subject': u'Eos qui esse facere.',\
  'To': u'angela79@ramsey.biz',\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'keywords': ['June', 'Wednesday', '1998', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 12,\
  'AudioProcessedCount': 1,\
  'BatteryCount': 3,\
  'BatteryLevel': 88,\
  'EndDateTime': '2016-09-18',\
  'Kilometers': 1.0587599935513867,\
  'LocationCount': 12,\
  'MoonAge': 8.290462307919986,\
  'MoonIllumination': 0.995313068590835,\
  'StartDateTime': '2016-09-18',\
  'Temperature': 12.953533412477476,\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'Weather': 'rain',\
  'address': u'98 /\n 94 Lane Alley\nNorth Robert, VIC, 8154',\
  'keywords': [ 'August',\
                'Sunday',\
                '1981',\
                'spring',\
                'audio_home',\
                'audio_street',\
                'rain',\
                'waxing_gibbous'],\
  'latitude': 85.1545065,\
  'longitude': -36.615133,\
  'type': 'App'}, { 'EndDateTime': '2018-05-29',\
  'Name': u'Carl Harris',\
  'Number': u'0219213721',\
  'StartDateTime': '2018-05-29',\
  'Text': u'Deserunt deleniti facere in.',\
  'UserId': '3f1bedbd-b90c-43bd-9904-edc7efe2950b',\
  'keywords': ['May', 'Monday', '1996', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'AccelerometryCount': 5,\
  'AudioProcessedCount': 6,\
  'BatteryCount': 1,\
  'BatteryLevel': 89,\
  'EndDateTime': '2016-07-19',\
  'Kilometers': 0.2474337306313863,\
  'LocationCount': 10,\
  'MoonAge': 15.407672277054637,\
  'MoonIllumination': 0.756000105625289,\
  'StartDateTime': '2016-07-19',\
  'Temperature': 26.380969386359503,\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'Weather': 'overcast',\
  'address': u'361 Callahan Gully\nJohnsonmouth, WA, 2914',\
  'keywords': [ 'November',\
                'Wednesday',\
                '2005',\
                'winter',\
                'audio_car',\
                'overcast',\
                'waning_gibbous'],\
  'latitude': 16.7004555,\
  'longitude': -22.833703,\
  'type': 'App'}, { 'EndDateTime': '2010-11-14',\
  'StartDateTime': '2010-11-14',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['November', 'Monday', '1989', 'Happy'],\
  'latitude': 69.0253155,\
  'longitude': 175.223121,\
  'type': 'Button'}, { 'EndDateTime': '2018-09-06',\
  'StartDateTime': '2018-09-06',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['October', 'Saturday', '1985', 'Depressed'],\
  'latitude': 61.7392895,\
  'longitude': -97.575067,\
  'type': 'Button'}, { 'EndDateTime': '2012-01-05',\
  'StartDateTime': '2012-01-05',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['February', 'Friday', '1996', 'Depressed'],\
  'type': 'Button'}, { 'Duration': 151,\
  'EndDateTime': '2012-07-14',\
  'Name': u'Kathryn Jones',\
  'Number': u'+61.2.3067.3549',\
  'StartDateTime': '2012-07-14',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['August', 'Thursday', '2001', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2012-10-17',\
  'From': u'odavis@oneal-carr.org',\
  'Message': u'Quos ducimus nostrum ab.\nSoluta cum illo voluptatibus.\nNihil eligendi optio quas. Id ab enim voluptas quam. Ab ipsum ullam tempore porro.\nEos hic sit saepe velit non repellat. Natus accusantium enim soluta commodi rerum. Expedita quasi facilis facilis sed sapiente molestias.\nEnim nostrum quidem eius magnam delectus. Error nesciunt laudantium consectetur iste deserunt amet.',\
  'StartDateTime': '2012-10-17',\
  'Subject': u'Debitis fugit.',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['September', 'Monday', '2000', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2018-01-11',\
  'Message': u'Porro dolore numquam voluptatem doloribus iste inventore. Explicabo ea cumque sapiente quaerat consectetur nesciunt. Minima vitae atque quasi.\nFacere asperiores necessitatibus accusantium pariatur corporis repellat optio. Similique reprehenderit nulla earum provident.\nNeque iste vitae adipisci. Sed nemo omnis iure. Inventore exercitationem quasi voluptate earum.',\
  'StartDateTime': '2018-01-11',\
  'Subject': u'Sunt natus quae.',\
  'To': u'dglass@yahoo.com.au',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['July', 'Tuesday', '2016', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2018-01-18',\
  'StartDateTime': '2018-01-18',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['May', 'Monday', '2000', 'Happy'],\
  'latitude': 1.310979,\
  'longitude': 163.114757,\
  'type': 'Button'}, { 'EndDateTime': '2015-09-15',\
  'Name': u'Priscilla Stephens',\
  'Number': u'50258135',\
  'StartDateTime': '2015-09-15',\
  'Text': u'Nobis dignissimos harum.',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['July', 'Thursday', '2015', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2015-03-06',\
  'Name': u'Jasmine Jones',\
  'Number': u'7410-7076',\
  'StartDateTime': '2015-03-06',\
  'Text': u'Delectus sed animi aliquam.',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['April', 'Wednesday', '2014', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'AccelerometryCount': 10,\
  'AudioProcessedCount': 3,\
  'BatteryCount': 11,\
  'BatteryLevel': 16,\
  'EndDateTime': '2013-03-05',\
  'StartDateTime': '2013-03-05',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['June', 'Saturday', '2000', 'autumn', 'audio_home'],\
  'type': 'App'}, { 'EndDateTime': '2018-06-23',\
  'Name': u'Miranda Lang',\
  'Number': u'(02) 1462 7410',\
  'StartDateTime': '2018-06-23',\
  'Text': u'Cupiditate enim illo.',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['November', 'Monday', '1991', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2010-01-20',\
  'StartDateTime': '2010-01-20',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['August', 'Thursday', '1974', 'Happy'],\
  'latitude': -30.017493,\
  'longitude': -141.190685,\
  'type': 'Button'}, { 'Duration': 151,\
  'EndDateTime': '2015-10-31',\
  'Name': u'Sara Wade',\
  'Number': u'(08) 0606 8404',\
  'StartDateTime': '2015-10-31',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['June', 'Monday', '1991', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2017-06-07',\
  'Message': u'Quisquam quibusdam sunt perspiciatis atque nemo corporis. Rem tenetur porro vero molestias id beatae natus. Repudiandae nemo veritatis blanditiis.\nNatus ipsam optio suscipit. Et excepturi autem minus laboriosam aspernatur.\nDignissimos corrupti sint. Laudantium dolore quae voluptate. Temporibus doloremque repellendus esse ullam accusantium.',\
  'StartDateTime': '2017-06-07',\
  'Subject': u'Sint quidem.',\
  'To': u'mfrank@lewis.info',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['August', 'Friday', '1985', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2013-06-10',\
  'Message': u'Doloribus error ea nesciunt. Veritatis commodi eligendi ab. Quibusdam ipsum reprehenderit consectetur labore perspiciatis.\nModi dicta facere possimus tempora. Quae voluptas vel dolorum tempora aperiam ut.\nAd voluptatem ipsa nisi. Delectus impedit officia aspernatur incidunt.\nNumquam eligendi blanditiis. Rem magni non eos saepe maiores quia ut. Doloremque ullam quod quam.',\
  'StartDateTime': '2013-06-10',\
  'Subject': u'Hic assumenda.',\
  'To': u'raymond00@yahoo.com.au',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['December', 'Monday', '2016', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2018-09-29',\
  'Name': u'Jason Hernandez',\
  'Number': u'(03)39176633',\
  'StartDateTime': '2018-09-29',\
  'Text': u'Ad quaerat numquam modi.',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['February', 'Saturday', '2002', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2013-02-17',\
  'Message': u'Beatae nihil harum explicabo. Quia ex modi excepturi ullam similique fuga ea.\nEum sequi ea impedit. Quibusdam quas et magnam totam accusamus cumque. Atque fugit nemo quia temporibus esse.\nPerspiciatis quasi vel dolores porro. Consequuntur esse dolores iure consequatur.\nSaepe perspiciatis non eligendi facilis rem error modi. Maxime deserunt ullam distinctio maxime porro.',\
  'StartDateTime': '2013-02-17',\
  'Subject': u'Aspernatur odio.',\
  'To': u'sullivanmadeline@hotmail.com',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['June', 'Thursday', '1987', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'Duration': 20,\
  'EndDateTime': '2010-12-08',\
  'Name': u'Heather Underwood',\
  'Number': u'(02)-4722-4948',\
  'StartDateTime': '2010-12-08',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['March', 'Thursday', '2011', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'Duration': 91,\
  'EndDateTime': '2014-10-04',\
  'Name': u'Christopher Bryant',\
  'Number': u'7164 8387',\
  'StartDateTime': '2014-10-04',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['April', 'Thursday', '1983', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2011-08-24',\
  'Name': u'Jonathon Bradley',\
  'Number': u'9303-1237',\
  'StartDateTime': '2011-08-24',\
  'Text': u'Minus atque iste fugiat quam.',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['September', 'Friday', '1980', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2018-02-09',\
  'Message': u'Tenetur vitae aut sequi laborum consectetur. Occaecati excepturi cupiditate sint.\nDolores sint nesciunt dignissimos rerum culpa. Rerum voluptatem esse impedit quasi architecto. Accusamus earum officiis error perferendis.\nPerspiciatis recusandae molestiae. Autem magni dolores veritatis fuga natus consequuntur.\nDolores totam magnam itaque. Dolores vitae architecto error minima.',\
  'StartDateTime': '2018-02-09',\
  'Subject': u'Voluptas quod magni.',\
  'To': u'mayerin@hotmail.com',\
  'UserId': '382ec4c1-1bf5-4bfa-95a6-008ef0a5d029',\
  'keywords': ['March', 'Saturday', '2012', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2015-02-13',\
  'StartDateTime': '2015-02-13',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['June', 'Friday', '1971', 'Depressed'],\
  'latitude': -16.378731,\
  'longitude': 147.887572,\
  'type': 'Button'}, { 'EndDateTime': '2010-08-03',\
  'StartDateTime': '2010-08-03',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['January', 'Sunday', '2001', 'Excited'],\
  'type': 'Button'}, { 'EndDateTime': '2015-04-29',\
  'StartDateTime': '2015-04-29',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['October', 'Saturday', '1978', 'Depressed'],\
  'latitude': -59.682326,\
  'longitude': -119.365709,\
  'type': 'Button'}, { 'EndDateTime': '2013-09-03',\
  'From': u'bruce33@gmail.com',\
  'Message': u'Et asperiores odio ex assumenda sunt. Ab sunt non provident. Quas quae placeat accusantium iusto.\nFugit incidunt necessitatibus doloremque consequatur animi. Impedit delectus aliquam iusto.\nVeniam molestias autem sapiente. Illo consequuntur sunt architecto maxime ipsam architecto soluta. Quae beatae consequuntur.',\
  'StartDateTime': '2013-09-03',\
  'Subject': u'Tempora quod.',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['January', 'Sunday', '1989', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2010-03-17',\
  'StartDateTime': '2010-03-17',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['January', 'Friday', '2015', 'Tired'],\
  'latitude': -50.812625,\
  'longitude': -92.39973,\
  'type': 'Button'}, { 'EndDateTime': '2010-02-25',\
  'Name': u'Stephanie Haynes',\
  'Number': u'+61.3.2138.5450',\
  'StartDateTime': '2010-02-25',\
  'Text': u'Eaque eos at modi esse.',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['January', 'Thursday', '1985', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2017-09-28',\
  'StartDateTime': '2017-09-28',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['July', 'Monday', '1975', 'Excited'],\
  'latitude': 40.781514,\
  'longitude': 68.856532,\
  'type': 'Button'}, { 'EndDateTime': '2016-06-09',\
  'StartDateTime': '2016-06-09',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['March', 'Wednesday', '1979', 'Depressed'],\
  'latitude': -3.247263,\
  'longitude': 72.227407,\
  'type': 'Button'}, { 'EndDateTime': '2015-08-17',\
  'StartDateTime': '2015-08-17',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['June', 'Saturday', '1995', 'Excited'],\
  'latitude': -58.8887075,\
  'longitude': -11.741766,\
  'type': 'Button'}, { 'AccelerometryCount': 8,\
  'AudioProcessedCount': 11,\
  'BatteryCount': 9,\
  'BatteryLevel': 56,\
  'EndDateTime': '2018-10-06',\
  'Kilometers': 1.0326576871560509,\
  'LocationCount': 3,\
  'MoonAge': 19.023095683291796,\
  'MoonIllumination': 0.8575556107701946,\
  'StartDateTime': '2018-10-06',\
  'Temperature': 20.92355187689899,\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'Weather': 'rain',\
  'address': u'Unit 26\n 529 Andrea Plateau\nPort Kenneth, SA, 2651',\
  'keywords': [ 'March',\
                'Saturday',\
                '2009',\
                'spring',\
                'audio_street',\
                'audio_voice',\
                'rain',\
                'waning_gibbous'],\
  'latitude': 59.2324655,\
  'longitude': 89.911749,\
  'type': 'App'}, { 'EndDateTime': '2013-06-29',\
  'Message': u'Sint mollitia fuga ut dolor voluptatum. Sint rerum debitis numquam velit unde nihil asperiores.\nDistinctio nemo nulla ab dolore accusamus adipisci modi. Occaecati repellat dolores placeat beatae. Illo animi enim quibusdam quos fugit minus. Atque perspiciatis accusamus dolores necessitatibus.\nNisi quisquam adipisci fuga iste a. Accusantium iste sint inventore. Beatae facere delectus.',\
  'StartDateTime': '2013-06-29',\
  'Subject': u'Corrupti doloremque.',\
  'To': u'steven29@turner.edu.au',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['May', 'Sunday', '1989', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2017-04-26',\
  'StartDateTime': '2017-04-26',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['February', 'Thursday', '1973', 'Depressed'],\
  'latitude': -56.855771,\
  'longitude': -102.695798,\
  'type': 'Button'}, { 'EndDateTime': '2014-07-13',\
  'Name': u'Michelle Watson',\
  'Number': u'03-9625-4167',\
  'StartDateTime': '2014-07-13',\
  'Text': u'Alias ipsum tempora.',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['March', 'Friday', '1980', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2011-03-19',\
  'StartDateTime': '2011-03-19',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['September', 'Friday', '1977', 'Tired'],\
  'latitude': 34.1063065,\
  'longitude': 86.753536,\
  'type': 'Button'}, { 'Duration': 171,\
  'EndDateTime': '2011-04-24',\
  'Name': u'Eric Oneill',\
  'Number': u'0411-232-930',\
  'StartDateTime': '2011-04-24',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['May', 'Thursday', '1980', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2015-08-04',\
  'StartDateTime': '2015-08-04',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['March', 'Friday', '2008', 'Depressed'],\
  'latitude': 50.4042995,\
  'longitude': 174.319809,\
  'type': 'Button'}, { 'Duration': 219,\
  'EndDateTime': '2013-07-13',\
  'Name': u'Lisa Berry',\
  'Number': u'+61 7 9116 3154',\
  'StartDateTime': '2013-07-13',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['February', 'Saturday', '2000', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 7,\
  'AudioProcessedCount': 1,\
  'BatteryCount': 5,\
  'BatteryLevel': 12,\
  'EndDateTime': '2015-05-20',\
  'Kilometers': 0.5616693213281005,\
  'LocationCount': 3,\
  'MoonAge': 5.482258692366621,\
  'MoonIllumination': 0.5894765291414523,\
  'StartDateTime': '2015-05-20',\
  'Temperature': 10.352481722992575,\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'Weather': 'cloudy',\
  'address': u'393 /\n 9 Pineda Ridge\nSouth Haley, NT, 2618',\
  'keywords': [ 'May',\
                'Friday',\
                '2016',\
                'autumn',\
                'audio_home',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': -46.0141205,\
  'longitude': -61.775284,\
  'type': 'App'}, { 'EndDateTime': '2018-06-03',\
  'StartDateTime': '2018-06-03',\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'keywords': ['April', 'Thursday', '2009', 'Depressed'],\
  'latitude': -59.538578,\
  'longitude': 96.8897,\
  'type': 'Button'}, { 'AccelerometryCount': 12,\
  'AudioProcessedCount': 9,\
  'BatteryCount': 6,\
  'BatteryLevel': 15,\
  'EndDateTime': '2012-07-13',\
  'Kilometers': 3.6771400744514593,\
  'LocationCount': 4,\
  'MoonAge': 25.368342483348645,\
  'MoonIllumination': 0.3994579838477267,\
  'StartDateTime': '2012-07-13',\
  'Temperature': 17.876640391572543,\
  'UserId': '42c875aa-b7c9-4662-bd85-4a604c71545e',\
  'Weather': 'rain',\
  'address': u'19 /\n 95 Victoria Dell\nPort Jasonside, TAS, 2920',\
  'keywords': [ 'December',\
                'Tuesday',\
                '1971',\
                'winter',\
                'audio_car',\
                'rain',\
                'waning_gibbous'],\
  'latitude': -44.130729,\
  'longitude': 8.545191,\
  'type': 'App'}, { 'EndDateTime': '2010-06-23',\
  'StartDateTime': '2010-06-23',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['July', 'Wednesday', '2003', 'Depressed'],\
  'type': 'Button'}, { 'AccelerometryCount': 12,\
  'AudioProcessedCount': 6,\
  'BatteryCount': 5,\
  'BatteryLevel': 5,\
  'EndDateTime': '2012-04-08',\
  'Kilometers': 0.6588397100590552,\
  'LocationCount': 1,\
  'MoonAge': 10.383092317321417,\
  'MoonIllumination': 0.19983084179681676,\
  'StartDateTime': '2012-04-08',\
  'Temperature': 5.503252855639987,\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'Weather': 'clear',\
  'address': u'919 /\n 2 Gardner Estate\nMeganshire, SA, 2918',\
  'keywords': [ 'July',\
                'Saturday',\
                '2018',\
                'winter',\
                'audio_car',\
                'audio_voice',\
                'clear',\
                'waxing_gibbous'],\
  'latitude': 39.476589,\
  'longitude': -64.030381,\
  'type': 'App'}, { 'Duration': 3,\
  'EndDateTime': '2014-02-15',\
  'Name': u'John Bernard',\
  'Number': u'+61.425.621.710',\
  'StartDateTime': '2014-02-15',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['April', 'Tuesday', '2006', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2015-07-10',\
  'Message': u'Sint maxime tempora architecto dicta.\nSequi quaerat amet consequatur. Eius aliquid occaecati iusto sit distinctio.\nEarum assumenda quod blanditiis. Iure nisi eos sed corporis quia distinctio eos. Adipisci expedita nulla laborum.\nFacere ad doloremque quisquam quas autem unde. Eum corporis pariatur rem sunt.',\
  'StartDateTime': '2015-07-10',\
  'Subject': u'Soluta deleniti eum.',\
  'To': u'michael79@gmail.com',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['May', 'Tuesday', '2000', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2014-03-31',\
  'StartDateTime': '2014-03-31',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['May', 'Friday', '1993', 'Tired'],\
  'latitude': -11.4683235,\
  'longitude': 170.971646,\
  'type': 'Button'}, { 'AccelerometryCount': 8,\
  'AudioProcessedCount': 12,\
  'BatteryCount': 1,\
  'BatteryLevel': 62,\
  'EndDateTime': '2010-09-09',\
  'Kilometers': 0.2759538560206055,\
  'LocationCount': 9,\
  'MoonAge': 17.91763417737084,\
  'MoonIllumination': 0.3457577955175126,\
  'StartDateTime': '2010-09-09',\
  'Temperature': 14.098404373788748,\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'Weather': 'rain',\
  'address': u'Suite 426\n 05 Vasquez Round\nEast Timothybury, VIC, 2642',\
  'keywords': [ 'February',\
                'Monday',\
                '1971',\
                'autumn',\
                'audio_home',\
                'audio_home',\
                'audio_car',\
                'rain',\
                'waning_gibbous'],\
  'latitude': -58.5456245,\
  'longitude': 126.328465,\
  'type': 'App'}, { 'EndDateTime': '2012-06-01',\
  'Message': u'Dicta repudiandae temporibus consequatur blanditiis excepturi suscipit eveniet. Deleniti ratione adipisci est cumque alias earum. Explicabo eum aspernatur exercitationem possimus labore.\nUllam aut et aliquam omnis esse. Mollitia corporis atque vel ut hic.\nProvident ipsum dolores expedita. Tempora cumque perferendis. Cupiditate deserunt minima.',\
  'StartDateTime': '2012-06-01',\
  'Subject': u'Molestias optio.',\
  'To': u'alexanderrobin@ramirez.com.au',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['February', 'Wednesday', '2017', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2016-10-07',\
  'From': u'qburgess@fisher.info',\
  'Message': u'Exercitationem deleniti aliquam necessitatibus saepe. Suscipit mollitia repudiandae.\nExcepturi voluptatibus dolorum perferendis. Doloremque distinctio sunt eius magnam omnis excepturi perspiciatis.\nPerspiciatis odio similique dolorem. Facere ea praesentium repellendus.',\
  'StartDateTime': '2016-10-07',\
  'Subject': u'Ullam quos quasi.',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['January', 'Wednesday', '1994', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2017-11-15',\
  'StartDateTime': '2017-11-15',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['May', 'Thursday', '1980', 'Tired'],\
  'latitude': -47.502841,\
  'longitude': 156.730839,\
  'type': 'Button'}, { 'Duration': 249,\
  'EndDateTime': '2015-02-25',\
  'Name': u'Robert Smith',\
  'Number': u'03-7141-6243',\
  'StartDateTime': '2015-02-25',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['February', 'Monday', '1986', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 6,\
  'AudioProcessedCount': 10,\
  'BatteryCount': 9,\
  'BatteryLevel': 9,\
  'EndDateTime': '2015-06-09',\
  'Kilometers': 3.0042615444360568,\
  'LocationCount': 8,\
  'MoonAge': 17.689762639261726,\
  'MoonIllumination': 0.5976602239033408,\
  'StartDateTime': '2015-06-09',\
  'Temperature': 17.96739016972223,\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'Weather': 'cloudy',\
  'address': u'14 Trujillo Walk\nNorth Markfurt, QLD, 2658',\
  'keywords': [ 'April',\
                'Sunday',\
                '1978',\
                'summer',\
                'audio_voice',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': 42.6115765,\
  'longitude': 43.395562,\
  'type': 'App'}, { 'AccelerometryCount': 5,\
  'AudioProcessedCount': 3,\
  'BatteryCount': 10,\
  'BatteryLevel': 28,\
  'EndDateTime': '2010-02-22',\
  'Kilometers': 0.8205950630059535,\
  'LocationCount': 11,\
  'MoonAge': 21.15612625153645,\
  'MoonIllumination': 0.121212788287829,\
  'StartDateTime': '2010-02-22',\
  'Temperature': 7.329522710976379,\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'Weather': 'cloudy',\
  'address': u'7 /\n 708 Lynch Gully\nBrownborough, VIC, 2689',\
  'keywords': [ 'May',\
                'Monday',\
                '1992',\
                'autumn',\
                'audio_home',\
                'audio_car',\
                'audio_street',\
                'audio_home',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': 24.9821475,\
  'longitude': 37.539222,\
  'type': 'App'}, { 'EndDateTime': '2017-11-08',\
  'StartDateTime': '2017-11-08',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['August', 'Friday', '2003', 'Happy'],\
  'latitude': -55.05845,\
  'longitude': -165.0043,\
  'type': 'Button'}, { 'AccelerometryCount': 3,\
  'AudioProcessedCount': 8,\
  'BatteryCount': 10,\
  'BatteryLevel': 94,\
  'EndDateTime': '2012-05-30',\
  'StartDateTime': '2012-05-30',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['May', 'Sunday', '1998', 'autumn', 'audio_car', 'audio_street'],\
  'type': 'App'}, { 'Duration': 31,\
  'EndDateTime': '2011-06-09',\
  'Name': u'Dr. Bruce Scott',\
  'Number': u'80384570',\
  'StartDateTime': '2011-06-09',\
  'UserId': '39f30772-bf47-45d2-ba3b-68255d51fc29',\
  'keywords': ['August', 'Friday', '1982', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2013-01-21',\
  'Message': u'Voluptatem aliquid autem explicabo quam dolor soluta asperiores. Quae dolorem dolor aut. Ut asperiores beatae sequi atque consequuntur. Quis vitae dignissimos.\nIllum iure totam corporis nostrum adipisci doloribus. Similique dolor fugiat officiis distinctio. Maiores harum deleniti fugit.\nNemo expedita nulla quidem at officiis. Soluta excepturi quidem minus.',\
  'StartDateTime': '2013-01-21',\
  'Subject': u'Accusamus deleniti.',\
  'To': u'christinaferguson@hill.com.au',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['October', 'Monday', '2014', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 9,\
  'AudioProcessedCount': 4,\
  'BatteryCount': 4,\
  'BatteryLevel': 93,\
  'EndDateTime': '2014-07-29',\
  'Kilometers': 0.020833996642346562,\
  'LocationCount': 2,\
  'MoonAge': 10.753391010316257,\
  'MoonIllumination': 0.7023731491037811,\
  'StartDateTime': '2014-07-29',\
  'Temperature': 6.5936334808682435,\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'Weather': 'clear',\
  'address': u'596 /\n 733 Perkins River\nOrrstad, ACT, 3983',\
  'keywords': [ 'March',\
                'Monday',\
                '1986',\
                'summer',\
                'audio_home',\
                'clear',\
                'waxing_gibbous'],\
  'latitude': -21.466242,\
  'longitude': 136.883496,\
  'type': 'App'}, { 'Duration': 175,\
  'EndDateTime': '2018-04-14',\
  'Name': u'Angela Cross',\
  'Number': u'0461.700.807',\
  'StartDateTime': '2018-04-14',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['February', 'Sunday', '1978', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2014-01-23',\
  'From': u'dawn18@stevens.org.au',\
  'Message': u'Nemo amet totam qui consequuntur. Alias quas cum debitis.\nEaque expedita eligendi possimus vero aliquid suscipit. Error earum molestiae asperiores. Occaecati aspernatur porro odio aliquid quis incidunt.\nEx nostrum placeat saepe. Autem vitae quis voluptatum minima molestiae repellat.\nNeque fugiat iure. Eaque odit error iusto accusamus delectus. Voluptas consequuntur in beatae vitae.',\
  'StartDateTime': '2014-01-23',\
  'Subject': u'Nostrum recusandae.',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['February', 'Tuesday', '1992', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2012-10-08',\
  'StartDateTime': '2012-10-08',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['July', 'Saturday', '1979', 'Tired'],\
  'latitude': -48.990154,\
  'longitude': 123.075434,\
  'type': 'Button'}, { 'EndDateTime': '2016-02-01',\
  'StartDateTime': '2016-02-01',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['January', 'Monday', '1990', 'Happy'],\
  'latitude': 88.435106,\
  'longitude': 43.794227,\
  'type': 'Button'}, { 'EndDateTime': '2013-11-05',\
  'Message': u'Recusandae reprehenderit non inventore dignissimos fugit. Veniam mollitia facere aliquid esse dolore doloribus. Expedita nostrum veniam totam fugiat doloribus.\nEa ducimus odio sint veniam. Distinctio consectetur quibusdam.\nVoluptatem corrupti sunt deleniti praesentium officiis voluptatum. Libero quis praesentium quam facere expedita.',\
  'StartDateTime': '2013-11-05',\
  'Subject': u'Ipsa libero tenetur.',\
  'To': u'lwalters@walker-mitchell.org.au',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['July', 'Friday', '1975', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'Duration': 15,\
  'EndDateTime': '2011-11-16',\
  'Name': u'Robert Hicks',\
  'Number': u'+61-2-1280-5235',\
  'StartDateTime': '2011-11-16',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['November', 'Friday', '1986', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 3,\
  'AudioProcessedCount': 12,\
  'BatteryCount': 3,\
  'BatteryLevel': 90,\
  'EndDateTime': '2013-08-18',\
  'Kilometers': 2.6997914415497837,\
  'LocationCount': 12,\
  'MoonAge': 20.093996700565356,\
  'MoonIllumination': 0.08491617941217677,\
  'StartDateTime': '2013-08-18',\
  'Temperature': -2.24640067841948,\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'Weather': 'rain',\
  'address': u'429 Robert Path\nWest Michellemouth, QLD, 2142',\
  'keywords': [ 'July',\
                'Wednesday',\
                '2008',\
                'autumn',\
                'audio_street',\
                'rain',\
                'waxing_gibbous'],\
  'latitude': 60.291751,\
  'longitude': 161.357435,\
  'type': 'App'}, { 'AccelerometryCount': 10,\
  'AudioProcessedCount': 12,\
  'BatteryCount': 5,\
  'BatteryLevel': 93,\
  'EndDateTime': '2018-03-24',\
  'Kilometers': 1.4256550781667379,\
  'LocationCount': 4,\
  'MoonAge': 0.5166195372321125,\
  'MoonIllumination': 0.7141916088546861,\
  'StartDateTime': '2018-03-24',\
  'Temperature': 21.445330538535455,\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'Weather': 'rain',\
  'address': u'Level 9\n 99 Jackson Vista\nHeatherview, SA, 5572',\
  'keywords': [ 'November',\
                'Tuesday',\
                '1987',\
                'autumn',\
                'audio_car',\
                'audio_street',\
                'audio_home',\
                'audio_voice',\
                'rain',\
                'waxing_gibbous'],\
  'latitude': -33.207906,\
  'longitude': 45.320467,\
  'type': 'App'}, { 'EndDateTime': '2012-10-18',\
  'Name': u'Lindsey Mccoy',\
  'Number': u'+61-413-373-715',\
  'StartDateTime': '2012-10-18',\
  'Text': u'Id officiis a corporis.',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['October', 'Friday', '1987', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2017-09-16',\
  'Name': u'Marc Donaldson',\
  'Number': u'0389720689',\
  'StartDateTime': '2017-09-16',\
  'Text': u'Velit minus facere eos earum.',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['November', 'Sunday', '1974', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'Duration': 92,\
  'EndDateTime': '2015-04-01',\
  'Name': u'Carl Evans',\
  'Number': u'+61 418 037 382',\
  'StartDateTime': '2015-04-01',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['October', 'Wednesday', '1976', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'Duration': 184,\
  'EndDateTime': '2015-07-01',\
  'Name': u'Isaac Dunn',\
  'Number': u'02.1528.8632',\
  'StartDateTime': '2015-07-01',\
  'UserId': '5b2a7460-66a4-4fb7-be73-7925e6d708db',\
  'keywords': ['October', 'Thursday', '2005', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2010-02-26',\
  'Name': u'Jessica Cameron',\
  'Number': u'+61.8.6954.0782',\
  'StartDateTime': '2010-02-26',\
  'Text': u'Culpa neque dolores.',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['August', 'Friday', '1996', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'Duration': 37,\
  'EndDateTime': '2015-10-12',\
  'Name': u'Matthew Adams',\
  'Number': u'8485-6825',\
  'StartDateTime': '2015-10-12',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['January', 'Saturday', '1973', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2014-05-23',\
  'Message': u'Exercitationem ex eius exercitationem perferendis at fugiat. Laudantium dicta suscipit ipsam.\nAlias veniam quam officiis vel explicabo. Sed beatae fuga cupiditate.\nOdio perferendis consequatur aut voluptatum natus. Aliquid officiis in veniam dolorem. Eos harum dolores maxime.',\
  'StartDateTime': '2014-05-23',\
  'Subject': u'Eaque magnam ipsa.',\
  'To': u'perezkelly@morgan-jones.info',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['September', 'Monday', '1998', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'Duration': 33,\
  'EndDateTime': '2017-09-05',\
  'Name': u'Ryan Kennedy',\
  'Number': u'(08)87795508',\
  'StartDateTime': '2017-09-05',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['September', 'Saturday', '2016', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 12,\
  'AudioProcessedCount': 4,\
  'BatteryCount': 1,\
  'BatteryLevel': 91,\
  'EndDateTime': '2014-04-21',\
  'Kilometers': 1.3958449478861503,\
  'LocationCount': 4,\
  'MoonAge': 22.451250432584587,\
  'MoonIllumination': 0.5999176721866829,\
  'StartDateTime': '2014-04-21',\
  'Temperature': 5.8822900923727826,\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'Weather': 'cloudy',\
  'address': u'7 Shannon Grange\nNorth Jamestown, NT, 8834',\
  'keywords': [ 'March',\
                'Wednesday',\
                '2004',\
                'winter',\
                'audio_home',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': -75.127074,\
  'longitude': -102.134518,\
  'type': 'App'}, { 'EndDateTime': '2010-02-13',\
  'Name': u'Kara Mendoza',\
  'Number': u'(02) 4460 3161',\
  'StartDateTime': '2010-02-13',\
  'Text': u'Eius sint qui ducimus harum.',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['October', 'Thursday', '2001', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2017-01-05',\
  'Message': u'A voluptatum iusto libero incidunt. Minima ipsa debitis. Culpa quae dolore nobis iure.\nAssumenda tenetur omnis non tempora debitis magnam mollitia. Soluta unde asperiores velit accusamus.\nImpedit alias nihil numquam est sit. Voluptatibus sit reprehenderit ducimus. Ipsa delectus pariatur.\nIure suscipit eum excepturi voluptatem ducimus praesentium.',\
  'StartDateTime': '2017-01-05',\
  'Subject': u'Iste necessitatibus.',\
  'To': u'karenwelch@gentry.com.au',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['December', 'Wednesday', '1978', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'Duration': 37,\
  'EndDateTime': '2015-12-17',\
  'Name': u'Matthew Andrews',\
  'Number': u'02.3357.7022',\
  'StartDateTime': '2015-12-17',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['March', 'Friday', '1980', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2018-05-12',\
  'Name': u'Joseph Huff',\
  'Number': u'+61-437-377-501',\
  'StartDateTime': '2018-05-12',\
  'Text': u'Vitae rerum ullam ducimus.',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['June', 'Monday', '2004', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2012-03-29',\
  'From': u'ronald01@yahoo.com.au',\
  'Message': u'Nam vel maxime quas magnam voluptatem aliquam expedita. Aut animi modi laudantium similique officia.\nAb porro perferendis. Accusamus eum nulla corporis dolorum reiciendis. Velit praesentium recusandae aperiam possimus ducimus.\nA maxime nostrum delectus est voluptate odit aspernatur. Assumenda eius autem dicta nemo.',\
  'StartDateTime': '2012-03-29',\
  'Subject': u'Sunt recusandae.',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['December', 'Tuesday', '2008', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2018-09-17',\
  'From': u'kathleen42@smith-erickson.com',\
  'Message': u'Magnam sequi error eius nobis incidunt tempora. Vero enim quas dolor.\nInventore repellendus laborum iste voluptatem odit sunt. Dignissimos cupiditate totam non quas. Nesciunt sunt cupiditate qui hic enim.\nNam autem corrupti earum. Aliquam maxime quos. Natus vel pariatur temporibus praesentium soluta.\nVeniam distinctio optio tempore consequatur. Rem dolores exercitationem similique quae rerum rem.',\
  'StartDateTime': '2018-09-17',\
  'Subject': u'Adipisci quibusdam.',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['November', 'Friday', '1989', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'Duration': 106,\
  'EndDateTime': '2016-02-11',\
  'Name': u'Nancy Miranda',\
  'Number': u'(02).1201.9211',\
  'StartDateTime': '2016-02-11',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['November', 'Wednesday', '2010', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2010-12-29',\
  'StartDateTime': '2010-12-29',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['January', 'Saturday', '1991', 'Depressed'],\
  'latitude': 59.1101295,\
  'longitude': 128.141794,\
  'type': 'Button'}, { 'EndDateTime': '2012-04-06',\
  'StartDateTime': '2012-04-06',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['November', 'Tuesday', '1970', 'Happy'],\
  'type': 'Button'}, { 'Duration': 239,\
  'EndDateTime': '2018-03-02',\
  'Name': u'Terrence Hamilton',\
  'Number': u'07 1978 1229',\
  'StartDateTime': '2018-03-02',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['July', 'Saturday', '1987', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 1,\
  'AudioProcessedCount': 7,\
  'BatteryCount': 5,\
  'BatteryLevel': 81,\
  'EndDateTime': '2011-11-18',\
  'Kilometers': 0.08886049474461885,\
  'LocationCount': 6,\
  'MoonAge': 17.67217015020688,\
  'MoonIllumination': 0.24405979832437374,\
  'StartDateTime': '2011-11-18',\
  'Temperature': 5.93667751949075,\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'Weather': 'overcast',\
  'address': u'5 Yates River\nMcknightmouth, TAS, 7426',\
  'keywords': [ 'September',\
                'Thursday',\
                '2006',\
                'spring',\
                'audio_voice',\
                'audio_car',\
                'overcast',\
                'waning_gibbous'],\
  'latitude': -13.8753875,\
  'longitude': 170.572401,\
  'type': 'App'}, { 'EndDateTime': '2010-07-05',\
  'StartDateTime': '2010-07-05',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['September', 'Sunday', '2016', 'Excited'],\
  'latitude': 74.6361825,\
  'longitude': 74.730727,\
  'type': 'Button'}, { 'Duration': 49,\
  'EndDateTime': '2013-03-22',\
  'Name': u'William Shields DDS',\
  'Number': u'+61-411-747-598',\
  'StartDateTime': '2013-03-22',\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'keywords': ['August', 'Tuesday', '2007', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 10,\
  'AudioProcessedCount': 5,\
  'BatteryCount': 9,\
  'BatteryLevel': 94,\
  'EndDateTime': '2017-05-04',\
  'Kilometers': 0.1785403088302102,\
  'LocationCount': 9,\
  'MoonAge': 6.30373089917382,\
  'MoonIllumination': 0.7258095824297766,\
  'StartDateTime': '2017-05-04',\
  'Temperature': 35.42076353813706,\
  'UserId': '3d22a45a-680b-4fcb-9ccb-b16ffa3d572e',\
  'Weather': 'cloudy',\
  'address': u'Suite 574\n 46 King Expressway\nAlexanderburgh, WA, 0895',\
  'keywords': [ 'October',\
                'Thursday',\
                '1976',\
                'winter',\
                'audio_home',\
                'cloudy',\
                'waxing_gibbous'],\
  'latitude': -43.7814265,\
  'longitude': 4.830886,\
  'type': 'App'}, { 'EndDateTime': '2018-02-24',\
  'Message': u'Ab ab fugit nemo nostrum at expedita. Dolorum mollitia facilis distinctio officiis eaque facilis. Voluptatibus fugiat fuga porro.\nDeserunt nostrum cum. Vel rem nam incidunt deserunt repellat repellendus cupiditate.\nIncidunt reprehenderit a aut ipsam. Quas nam corrupti quod quis ut.',\
  'StartDateTime': '2018-02-24',\
  'Subject': u'Vel minima beatae.',\
  'To': u'matthew90@hotmail.com',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['January', 'Tuesday', '1983', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 9,\
  'AudioProcessedCount': 4,\
  'BatteryCount': 3,\
  'BatteryLevel': 50,\
  'EndDateTime': '2016-10-20',\
  'Kilometers': 1.2844527789551683,\
  'LocationCount': 10,\
  'MoonAge': 10.78140943832626,\
  'MoonIllumination': 0.6301570613415879,\
  'StartDateTime': '2016-10-20',\
  'Temperature': 5.4901268030828945,\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'Weather': 'rain',\
  'address': u'66 Shelton Plaza\nNorth Kristinberg, QLD, 2963',\
  'keywords': [ 'April',\
                'Sunday',\
                '2014',\
                'winter',\
                'audio_car',\
                'audio_home',\
                'audio_home',\
                'audio_street',\
                'rain',\
                'waxing_gibbous'],\
  'latitude': -63.065785,\
  'longitude': 0.95756,\
  'type': 'App'}, { 'EndDateTime': '2012-08-17',\
  'StartDateTime': '2012-08-17',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['January', 'Monday', '2013', 'Excited'],\
  'type': 'Button'}, { 'EndDateTime': '2015-01-07',\
  'Name': u'Frank Miller',\
  'Number': u'(08) 5734 7081',\
  'StartDateTime': '2015-01-07',\
  'Text': u'Enim atque numquam.',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['October', 'Sunday', '1994', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2015-11-04',\
  'StartDateTime': '2015-11-04',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['November', 'Thursday', '1987', 'Happy'],\
  'latitude': 52.8719445,\
  'longitude': -142.880241,\
  'type': 'Button'}, { 'Duration': 685,\
  'EndDateTime': '2012-12-09',\
  'Name': u'Stephanie Ramirez',\
  'Number': u'5479-9315',\
  'StartDateTime': '2012-12-09',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['February', 'Sunday', '1978', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2014-08-17',\
  'Name': u'Kenneth Vargas',\
  'Number': u'0484 962 296',\
  'StartDateTime': '2014-08-17',\
  'Text': u'Ea itaque repellat.',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['April', 'Tuesday', '1983', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'EndDateTime': '2016-09-16',\
  'From': u'johnsondawn@yahoo.com',\
  'Message': u'Quidem possimus harum quasi omnis magnam. Quam sapiente natus corporis consequatur doloremque.\nPraesentium doloribus velit aut dolorem quae.\nMinus numquam quos porro id suscipit voluptas praesentium. Sint numquam doloremque asperiores facilis. Amet veniam adipisci enim illum.',\
  'StartDateTime': '2016-09-16',\
  'Subject': u'Natus occaecati.',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['September', 'Thursday', '2009', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2013-01-09',\
  'From': u'jessica19@gmail.com',\
  'Message': u'Natus iusto quos ab. Natus consectetur numquam cumque error velit magni.\nArchitecto similique veniam optio cumque ratione. Quibusdam perferendis quod earum eligendi labore dolores maxime.\nEst omnis accusamus iure omnis amet doloribus. Nobis totam culpa totam. Ratione laudantium omnis neque.',\
  'StartDateTime': '2013-01-09',\
  'Subject': u'Asperiores omnis ea.',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['May', 'Monday', '1987', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 2,\
  'AudioProcessedCount': 6,\
  'BatteryCount': 2,\
  'BatteryLevel': 36,\
  'EndDateTime': '2017-02-01',\
  'StartDateTime': '2017-02-01',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['January', 'Monday', '2007', 'spring', 'audio_home'],\
  'type': 'App'}, { 'EndDateTime': '2013-07-24',\
  'From': u'watkinsbill@lopez-briggs.net.au',\
  'Message': u'Vero voluptatum beatae. Architecto earum quae in libero doloremque.\nVero nesciunt pariatur molestias nemo vero. Pariatur non iusto harum cumque vitae. Praesentium fugiat aliquid facere.\nConsectetur quae itaque libero consequuntur assumenda. Quidem ipsam neque sed ex architecto quae.',\
  'StartDateTime': '2013-07-24',\
  'Subject': u'Aliquam perferendis.',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['July', 'Saturday', '1970', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2011-11-24',\
  'StartDateTime': '2011-11-24',\
  'UserId': '06a9e1b3-95ec-4fe8-881d-f9396e27dbf4',\
  'keywords': ['June', 'Thursday', '1994', 'Excited'],\
  'latitude': 15.634376,\
  'longitude': -164.450888,\
  'type': 'Button'}, { 'EndDateTime': '2014-07-06',\
  'From': u'hannah45@berry.org',\
  'Message': u'Repellat quidem sequi quo dicta.\nBlanditiis ratione veniam earum. Perspiciatis eos doloribus sed. Nihil architecto quae est.\nMagnam minima corporis quas. Debitis officia minima nobis.\nQuod perferendis eos rem iure placeat ullam. Inventore voluptates sequi fugit odit. Soluta nesciunt vero non.\nDicta voluptatem illo. Repellat facere eos laudantium dolorum soluta officia.',\
  'StartDateTime': '2014-07-06',\
  'Subject': u'Rem mollitia.',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['January', 'Monday', '1975', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'AccelerometryCount': 12,\
  'AudioProcessedCount': 2,\
  'BatteryCount': 4,\
  'BatteryLevel': 95,\
  'EndDateTime': '2016-04-18',\
  'Kilometers': 0.09486830889522135,\
  'LocationCount': 12,\
  'MoonAge': 9.271524689620916,\
  'MoonIllumination': 0.4431155511183861,\
  'StartDateTime': '2016-04-18',\
  'Temperature': 30.638507326342634,\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'Weather': 'cloudy',\
  'address': u'612 Tracy Stairs\nNew Danielle, TAS, 9164',\
  'keywords': [ 'September',\
                'Friday',\
                '2013',\
                'winter',\
                'audio_home',\
                'audio_voice',\
                'audio_street',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': 58.2005935,\
  'longitude': -150.283983,\
  'type': 'App'}, { 'EndDateTime': '2016-03-03',\
  'Name': u'Joseph Smith',\
  'Number': u'03-1710-7503',\
  'StartDateTime': '2016-03-03',\
  'Text': u'Quasi alias rem quaerat est.',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['January', 'Tuesday', '2004', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2012-09-07',\
  'Name': u'Cody Leach',\
  'Number': u'07-7717-6132',\
  'StartDateTime': '2012-09-07',\
  'Text': u'Et natus ut id occaecati.',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['October', 'Tuesday', '2012', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'Duration': 584,\
  'EndDateTime': '2014-09-20',\
  'Name': u'Nicole Zhang',\
  'Number': u'0070 7768',\
  'StartDateTime': '2014-09-20',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['August', 'Monday', '1978', 'SMS', 'Received'],\
  'type': 'PhoneCall'}, { 'Duration': 68,\
  'EndDateTime': '2011-04-11',\
  'Name': u'Charlotte Roberts',\
  'Number': u'0407 444 214',\
  'StartDateTime': '2011-04-11',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['February', 'Sunday', '1979', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 3,\
  'AudioProcessedCount': 7,\
  'BatteryCount': 2,\
  'BatteryLevel': 81,\
  'EndDateTime': '2013-10-19',\
  'Kilometers': 1.4996849541446395,\
  'LocationCount': 9,\
  'MoonAge': 14.422895374186407,\
  'MoonIllumination': 0.8735797415346266,\
  'StartDateTime': '2013-10-19',\
  'Temperature': 3.4208375536629863,\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'Weather': 'clear',\
  'address': u'Apt. 947\n 751 Joseph Nook\nNguyenfort, NSW, 2907',\
  'keywords': [ 'July',\
                'Friday',\
                '2009',\
                'spring',\
                'audio_voice',\
                'clear',\
                'waning_gibbous'],\
  'latitude': -87.0033295,\
  'longitude': -77.633492,\
  'type': 'App'}, { 'EndDateTime': '2013-04-11',\
  'Name': u'Norman Dudley',\
  'Number': u'08-0014-3754',\
  'StartDateTime': '2013-04-11',\
  'Text': u'Dolore consequuntur odit.',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['May', 'Saturday', '1976', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'AccelerometryCount': 9,\
  'AudioProcessedCount': 11,\
  'BatteryCount': 12,\
  'BatteryLevel': 76,\
  'EndDateTime': '2013-09-30',\
  'Kilometers': 1.3357088629554823,\
  'LocationCount': 11,\
  'MoonAge': 13.34522311565086,\
  'MoonIllumination': 0.32353012756443966,\
  'StartDateTime': '2013-09-30',\
  'Temperature': 14.014828919946876,\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'Weather': 'rain',\
  'address': u'44 /\n 6 Peter Highway\nKellyhaven, WA, 2619',\
  'keywords': [ 'August',\
                'Thursday',\
                '2015',\
                'spring',\
                'audio_home',\
                'rain',\
                'waning_gibbous'],\
  'latitude': -44.9011105,\
  'longitude': -32.908242,\
  'type': 'App'}, { 'EndDateTime': '2014-09-15',\
  'Message': u'Ullam earum vel inventore id. Nostrum debitis harum labore quasi consequuntur. Sequi debitis voluptates quis adipisci fuga error.\nQuaerat ab provident excepturi dolorum quidem cumque. Exercitationem harum eveniet ea molestias cum.\nVoluptas rerum exercitationem tenetur culpa illum consequatur expedita. Excepturi iusto esse in eligendi modi dolorem.',\
  'StartDateTime': '2014-09-15',\
  'Subject': u'Qui harum illo.',\
  'To': u'harrismelissa@yahoo.com.au',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['June', 'Tuesday', '1982', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2015-04-18',\
  'From': u'fford@aguilar.net',\
  'Message': u'Eaque doloribus suscipit blanditiis earum numquam fugit architecto. Blanditiis et adipisci odio numquam consequuntur quam in. Cum adipisci labore odit optio quam.\nIpsum maxime libero enim alias delectus voluptates.\nArchitecto consequuntur nulla praesentium odit pariatur. Earum esse quisquam nihil illo eos.',\
  'StartDateTime': '2015-04-18',\
  'Subject': u'Accusamus corporis.',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['February', 'Tuesday', '2012', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2016-09-09',\
  'Name': u'Thomas Weber',\
  'Number': u'(07)62619478',\
  'StartDateTime': '2016-09-09',\
  'Text': u'Animi assumenda similique.',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['April', 'Thursday', '1994', 'SMS', 'Received'],\
  'type': 'SMS'}, { 'Duration': 57,\
  'EndDateTime': '2014-01-30',\
  'Name': u'Patricia Mckinney',\
  'Number': u'(02) 3691 3771',\
  'StartDateTime': '2014-01-30',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['April', 'Monday', '1994', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'AccelerometryCount': 9,\
  'AudioProcessedCount': 12,\
  'BatteryCount': 9,\
  'BatteryLevel': 80,\
  'EndDateTime': '2014-09-10',\
  'Kilometers': 1.845623184806436,\
  'LocationCount': 6,\
  'MoonAge': 15.958593130325978,\
  'MoonIllumination': 0.9801319847574277,\
  'StartDateTime': '2014-09-10',\
  'Temperature': 7.557880261108984,\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'Weather': 'overcast',\
  'address': u'204 /\n 06 Alexandra Dip\nGrantbury, TAS, 2619',\
  'keywords': [ 'October',\
                'Friday',\
                '2003',\
                'autumn',\
                'audio_street',\
                'overcast',\
                'waxing_gibbous'],\
  'latitude': 37.298759,\
  'longitude': -54.186624,\
  'type': 'App'}, { 'EndDateTime': '2015-07-03',\
  'From': u'uthompson@yahoo.com.au',\
  'Message': u'Suscipit tempora necessitatibus placeat. Odio voluptatibus distinctio facere perferendis facere.\nFuga ipsam minus amet aspernatur labore nulla voluptatem. Dolorem aperiam voluptatibus voluptates molestias aut facilis. Porro facere animi beatae expedita fugit.\nId cum vitae quod neque saepe architecto. Eos iste totam minima id tempora eveniet.',\
  'StartDateTime': '2015-07-03',\
  'Subject': u'Facere a commodi.',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['August', 'Friday', '1981', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2011-06-29',\
  'From': u'gnash@scott.net.au',\
  'Message': u'Perspiciatis similique veniam sequi. Laboriosam rerum inventore.\nIn voluptatem placeat eligendi corporis amet dolorem. Impedit sint aliquam velit consequuntur asperiores debitis.\nDucimus nostrum adipisci sequi impedit. Necessitatibus magnam nesciunt nam. Accusantium voluptas iste.\nIncidunt dolores inventore neque est laboriosam placeat dolorem. Maxime tenetur sequi optio excepturi debitis unde.',\
  'StartDateTime': '2011-06-29',\
  'Subject': u'Saepe quisquam.',\
  'UserId': '5811fbc0-9da9-452e-914a-8e76fdc728c7',\
  'keywords': ['October', 'Saturday', '1975', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2011-04-20',\
  'From': u'qrobertson@gmail.com',\
  'Message': u'Non assumenda laudantium iste hic officiis. Excepturi sit ipsam eius minus eius culpa.\nNostrum cumque consequatur accusamus.\nTemporibus fugiat culpa officiis. Enim soluta hic dicta laborum.\nNon dolor hic rem. Non cupiditate adipisci magni libero cumque fugiat. Quisquam fuga sint est impedit magnam modi.\nIpsam debitis quae nesciunt non similique.',\
  'StartDateTime': '2011-04-20',\
  'Subject': u'Expedita molestiae.',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['March', 'Saturday', '2003', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'Duration': 46,\
  'EndDateTime': '2014-01-12',\
  'Name': u'William Durham',\
  'Number': u'+61.400.675.801',\
  'StartDateTime': '2014-01-12',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['November', 'Friday', '1982', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2011-03-21',\
  'StartDateTime': '2011-03-21',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['July', 'Wednesday', '2013', 'Depressed'],\
  'latitude': -61.6109675,\
  'longitude': 68.154335,\
  'type': 'Button'}, { 'AccelerometryCount': 12,\
  'AudioProcessedCount': 7,\
  'BatteryCount': 11,\
  'BatteryLevel': 69,\
  'EndDateTime': '2010-12-21',\
  'Kilometers': 1.8035681398429042,\
  'LocationCount': 9,\
  'MoonAge': 28.563926676979484,\
  'MoonIllumination': 0.29880251833773386,\
  'StartDateTime': '2010-12-21',\
  'Temperature': 18.60294752272254,\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'Weather': 'overcast',\
  'address': u'0 Gould Bend\nWalkershire, NT, 2950',\
  'keywords': [ 'January',\
                'Thursday',\
                '1977',\
                'summer',\
                'audio_car',\
                'overcast',\
                'waxing_gibbous',\
                'cafe'],\
  'latitude': 86.1099575,\
  'longitude': -66.516197,\
  'type': 'App'}, { 'Duration': 169,\
  'EndDateTime': '2014-10-01',\
  'Name': u'Patrick Pennington',\
  'Number': u'+61-427-314-292',\
  'StartDateTime': '2014-10-01',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['March', 'Sunday', '2012', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2013-07-04',\
  'Message': u'Dolores alias consequatur fuga. Officiis saepe fugiat optio iure delectus voluptas quaerat. Enim omnis asperiores voluptas.\nFugit saepe animi fugit ullam reprehenderit ad. Vitae nemo tenetur recusandae consequatur modi voluptatibus. Sapiente cupiditate quod quod cupiditate.\nProvident dicta vero sit eius esse. Eligendi magni ipsam saepe quasi.',\
  'StartDateTime': '2013-07-04',\
  'Subject': u'Iure possimus.',\
  'To': u'scott83@black.edu',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['June', 'Saturday', '2017', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2018-10-18',\
  'Message': u'Suscipit deserunt architecto fugiat voluptates ex reiciendis. Magnam voluptatum inventore sed id veniam.\nEsse consequuntur error dignissimos minima voluptas molestiae perferendis. Nulla doloremque quasi accusamus debitis qui. Dolore atque beatae autem quam sed eveniet itaque.\nBlanditiis reiciendis molestiae deleniti modi nostrum. Mollitia quam cum quos quod minus similique magnam.',\
  'StartDateTime': '2018-10-18',\
  'Subject': u'Expedita odio.',\
  'To': u'matthewwoods@hernandez.net',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['February', 'Saturday', '1999', 'Gmail', 'Sent'],\
  'type': 'Gmail'}, { 'EndDateTime': '2013-09-16',\
  'From': u'fcarter@hotmail.com.au',\
  'Message': u'Suscipit architecto odio blanditiis aspernatur. Nisi quod fugiat maxime itaque occaecati.\nEa corporis nostrum deleniti consequatur. Accusamus quidem maiores architecto illo necessitatibus ab. Autem recusandae porro delectus.',\
  'StartDateTime': '2013-09-16',\
  'Subject': u'Nulla.',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['March', 'Friday', '1993', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2015-05-25',\
  'StartDateTime': '2015-05-25',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['August', 'Tuesday', '2018', 'Excited'],\
  'latitude': 29.9540525,\
  'longitude': 1.510854,\
  'type': 'Button'}, { 'AccelerometryCount': 3,\
  'AudioProcessedCount': 11,\
  'BatteryCount': 8,\
  'BatteryLevel': 45,\
  'EndDateTime': '2017-06-13',\
  'Kilometers': 0.2867842336018282,\
  'LocationCount': 12,\
  'MoonAge': 6.73538755635421,\
  'MoonIllumination': 0.8214669824871582,\
  'StartDateTime': '2017-06-13',\
  'Temperature': 7.551623945788906,\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'Weather': 'overcast',\
  'address': u'9 Martinez Amble\nNorth Davidville, TAS, 0228',\
  'keywords': [ 'September',\
                'Tuesday',\
                '1987',\
                'winter',\
                'audio_home',\
                'audio_car',\
                'overcast',\
                'waxing_gibbous',\
                'church'],\
  'latitude': -52.3390855,\
  'longitude': -73.921808,\
  'type': 'App'}, { 'EndDateTime': '2016-01-27',\
  'StartDateTime': '2016-01-27',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['December', 'Friday', '2017', 'Happy'],\
  'latitude': -43.244469,\
  'longitude': 3.776264,\
  'type': 'Button'}, { 'EndDateTime': '2017-12-12',\
  'StartDateTime': '2017-12-12',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['May', 'Friday', '1981', 'Depressed'],\
  'latitude': -36.55332,\
  'longitude': -111.670349,\
  'type': 'Button'}, { 'EndDateTime': '2011-02-24',\
  'From': u'nicholashood@rosales.org.au',\
  'Message': u'Sequi ad dolores reiciendis nisi maxime minima voluptatum.\nVoluptatem harum praesentium amet soluta quis ipsum vel. Ex ipsam occaecati praesentium officiis cum. Necessitatibus unde nesciunt eligendi. Fugit placeat quibusdam dolorem voluptatum numquam deleniti similique.',\
  'StartDateTime': '2011-02-24',\
  'Subject': u'Fugit ipsum sit.',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['June', 'Saturday', '1978', 'Gmail', 'Received'],\
  'type': 'Gmail'}, { 'EndDateTime': '2013-11-19',\
  'StartDateTime': '2013-11-19',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['July', 'Friday', '1997', 'Tired'],\
  'type': 'Button'}, { 'EndDateTime': '2017-04-29',\
  'StartDateTime': '2017-04-29',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['June', 'Friday', '1983', 'Happy'],\
  'latitude': -9.853524,\
  'longitude': -138.573423,\
  'type': 'Button'}, { 'Duration': 132,\
  'EndDateTime': '2014-01-10',\
  'Name': u'Robert Clark',\
  'Number': u'+61-8-4159-8165',\
  'StartDateTime': '2014-01-10',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['March', 'Saturday', '1980', 'SMS', 'Sent'],\
  'type': 'PhoneCall'}, { 'EndDateTime': '2012-03-10',\
  'Name': u'Rachel Norris',\
  'Number': u'03-5287-8367',\
  'StartDateTime': '2012-03-10',\
  'Text': u'Amet ut odit provident.',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['December', 'Thursday', '1977', 'SMS', 'Sent'],\
  'type': 'SMS'}, { 'EndDateTime': '2012-06-26',\
  'StartDateTime': '2012-06-26',\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'keywords': ['May', 'Monday', '1985', 'Excited'],\
  'latitude': 22.3092505,\
  'longitude': -155.225176,\
  'type': 'Button'}, { 'AccelerometryCount': 7,\
  'AudioProcessedCount': 7,\
  'BatteryCount': 4,\
  'BatteryLevel': 50,\
  'EndDateTime': '2014-04-30',\
  'Kilometers': 0.21164846398965054,\
  'LocationCount': 2,\
  'MoonAge': 7.648335983415616,\
  'MoonIllumination': 0.49717366938156715,\
  'StartDateTime': '2014-04-30',\
  'Temperature': 20.740930050243705,\
  'UserId': 'd352b1ed-3791-4f5d-b7ca-b756c41cdb1d',\
  'Weather': 'cloudy',\
  'address': u'Suite 021\n 7 Tracy Point\nMillerbury, VIC, 2997',\
  'keywords': [ 'July',\
                'Friday',\
                '2007',\
                'winter',\
                'audio_street',\
                'cloudy',\
                'waning_gibbous'],\
  'latitude': 77.9044055,\
  'longitude': 31.700652,\
  'type': 'App'}]


code = "[Event(d) for d in %s]" % str(data)
depGraph.define("DemoEvents", code, private=False)
depGraph.define("DemoEventsPrivate", code, private=True)
