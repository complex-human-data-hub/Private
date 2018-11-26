from event import Event

data = [{ 'AccelerometryCount': 5, \
  'AudioProcessedCount': 2, \
  'BatteryCount': 1, \
  'BatteryLevel': 38, \
  'EndDateTime': '2018-07-01', \
  'Kilometers': 2.3042819927342455, \
  'LocationCount': 8, \
  'MoonAge': 23.46621009833171, \
  'MoonIllumination': 0.518660389048138, \
  'StartDateTime': '2018-07-01', \
  'Temperature': 11.016170376090706, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'clear', \
  'address': u'4 William Path\nPort Nicholas, TAS, 2693', \
  'keywords': [ 'July', \
                'Wednesday', \
                '2014', \
                'winter', \
                'audio_car', \
                'clear', \
                'waning_gibbous'], \
  'latitude': -38.67369247090188, \
  'longitude': 143.3055711756974, \
  'type': 'App'}, { 'AccelerometryCount': 12, \
  'AudioProcessedCount': 6, \
  'BatteryCount': 2, \
  'BatteryLevel': 2, \
  'EndDateTime': '2016-12-29', \
  'Kilometers': 3.988685280237546, \
  'LocationCount': 9, \
  'MoonAge': 9.939608198676849, \
  'MoonIllumination': 0.3033848573024327, \
  'StartDateTime': '2016-12-29', \
  'Temperature': 23.111855145835115, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'overcast', \
  'address': u'40 Wendy Vale\nEast Ashleyton, VIC, 2655', \
  'keywords': [ 'March', \
                'Wednesday', \
                '2010', \
                'summer', \
                'audio_voice', \
                'overcast', \
                'waning_gibbous', \
                'cafe'], \
  'latitude': -39.451563764351924, \
  'longitude': 145.1358558132345, \
  'type': 'App'}, { 'AccelerometryCount': 6, \
  'AudioProcessedCount': 5, \
  'BatteryCount': 8, \
  'BatteryLevel': 75, \
  'EndDateTime': '2012-05-28', \
  'Kilometers': 0.8467397692828945, \
  'LocationCount': 3, \
  'MoonAge': 16.749398115137247, \
  'MoonIllumination': 0.4844550081262008, \
  'StartDateTime': '2012-05-28', \
  'Temperature': 18.51173778353623, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'overcast', \
  'address': u'Flat 54\n 58 Austin Reach\nDeckerview, SA, 1951', \
  'keywords': [ 'June', \
                'Wednesday', \
                '1995', \
                'spring', \
                'audio_home', \
                'overcast', \
                'waning_gibbous'], \
  'latitude': -38.5091766084715, \
  'longitude': 144.78730437823455, \
  'type': 'App'}, { 'AccelerometryCount': 4, \
  'AudioProcessedCount': 7, \
  'BatteryCount': 5, \
  'BatteryLevel': 40, \
  'EndDateTime': '2013-07-13', \
  'Kilometers': 1.0449284421719145, \
  'LocationCount': 2, \
  'MoonAge': 11.455915115916312, \
  'MoonIllumination': 0.5068121490425598, \
  'StartDateTime': '2013-07-13', \
  'Temperature': 39.394269684548924, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'rain', \
  'address': u'Suite 838\n 519 Moon Ring\nSouth Ronald, SA, 2998', \
  'keywords': [ 'July', \
                'Monday', \
                '2014', \
                'summer', \
                'audio_home', \
                'rain', \
                'waning_gibbous', \
                'church'], \
  'latitude': -37.032689785973766, \
  'longitude': 144.21517229185002, \
  'type': 'App'}, { 'AccelerometryCount': 7, \
  'AudioProcessedCount': 8, \
  'BatteryCount': 6, \
  'BatteryLevel': 35, \
  'EndDateTime': '2010-07-02', \
  'Kilometers': 0.1951308201404873, \
  'LocationCount': 11, \
  'MoonAge': 27.187293322701834, \
  'MoonIllumination': 0.7620675634685448, \
  'StartDateTime': '2010-07-02', \
  'Temperature': 20.69952972554985, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'overcast', \
  'address': u'9 Adrian Formation\nAimeeton, QLD, 2909', \
  'keywords': [ 'June', \
                'Wednesday', \
                '1988', \
                'autumn', \
                'audio_voice', \
                'overcast', \
                'waning_gibbous'], \
  'latitude': -36.344322215628374, \
  'longitude': 143.5420262039886, \
  'type': 'App'}, { 'AccelerometryCount': 12, \
  'AudioProcessedCount': 3, \
  'BatteryCount': 1, \
  'BatteryLevel': 50, \
  'EndDateTime': '2015-12-20', \
  'Kilometers': 0.4353195203255296, \
  'LocationCount': 3, \
  'MoonAge': 24.06064048896967, \
  'MoonIllumination': 0.7999201669788973, \
  'StartDateTime': '2015-12-20', \
  'Temperature': 15.029233104278944, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'clear', \
  'address': u'794 Wilkinson Close\nEast Erikbury, VIC, 6611', \
  'keywords': [ 'August', \
                'Sunday', \
                '1977', \
                'spring', \
                'audio_car', \
                'clear', \
                'waxing_gibbous', \
                'cafe'], \
  'latitude': -38.985989291877516, \
  'longitude': 144.7552368671828, \
  'type': 'App'}, { 'AccelerometryCount': 1, \
  'AudioProcessedCount': 4, \
  'BatteryCount': 2, \
  'BatteryLevel': 15, \
  'EndDateTime': '2012-10-25', \
  'Kilometers': 1.2612841983880394, \
  'LocationCount': 5, \
  'MoonAge': 20.243144147041846, \
  'MoonIllumination': 0.5988504852563101, \
  'StartDateTime': '2012-10-25', \
  'Temperature': 15.442075685711888, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'clear', \
  'address': u'Suite 397\n 4 Stacy Pathway\nWalshfort, SA, 5209', \
  'keywords': [ 'January', \
                'Saturday', \
                '2013', \
                'winter', \
                'audio_car', \
                'clear', \
                'waxing_gibbous'], \
  'latitude': -38.04387322097976, \
  'longitude': 144.96837785145374, \
  'type': 'App'}, { 'AccelerometryCount': 5, \
  'AudioProcessedCount': 1, \
  'BatteryCount': 12, \
  'BatteryLevel': 51, \
  'EndDateTime': '2015-06-13', \
  'Kilometers': 0.3488012278134759, \
  'LocationCount': 2, \
  'MoonAge': 21.31503059790072, \
  'MoonIllumination': 0.8913169180253401, \
  'StartDateTime': '2015-06-13', \
  'Temperature': 26.268584555017554, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'overcast', \
  'address': u'Unit 82\n 2 Wong Subway\nBrittneyland, NSW, 2920', \
  'keywords': [ 'January', \
                'Sunday', \
                '1970', \
                'spring', \
                'audio_home', \
                'audio_home', \
                'overcast', \
                'waxing_gibbous'], \
  'latitude': -38.61668308195461, \
  'longitude': 146.58122905532557, \
  'type': 'App'}, { 'AccelerometryCount': 1, \
  'AudioProcessedCount': 11, \
  'BatteryCount': 12, \
  'BatteryLevel': 67, \
  'EndDateTime': '2010-09-26', \
  'Kilometers': 0.006202116328042672, \
  'LocationCount': 10, \
  'MoonAge': 4.7799574062366466, \
  'MoonIllumination': 0.029261139971911154, \
  'StartDateTime': '2010-09-26', \
  'Temperature': 16.88965554066266, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'cloudy', \
  'address': u'2 Maureen Rest\nMelanieshire, WA, 5092', \
  'keywords': [ 'March', \
                'Wednesday', \
                '2013', \
                'autumn', \
                'audio_home', \
                'audio_street', \
                'audio_car', \
                'cloudy', \
                'waning_gibbous', \
                'church'], \
  'latitude': -38.95027602640882, \
  'longitude': 144.6608987444805, \
  'type': 'App'}, { 'AccelerometryCount': 10, \
  'AudioProcessedCount': 4, \
  'BatteryCount': 7, \
  'BatteryLevel': 2, \
  'EndDateTime': '2014-09-26', \
  'Kilometers': 0.20332137427066693, \
  'LocationCount': 9, \
  'MoonAge': 27.322314659515992, \
  'MoonIllumination': 0.052353349188621, \
  'StartDateTime': '2014-09-26', \
  'Temperature': 8.799573610458673, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'overcast', \
  'address': u'277 Kevin Way\nWest Briannachester, VIC, 2566', \
  'keywords': [ 'September', \
                'Sunday', \
                '1971', \
                'summer', \
                'audio_voice', \
                'overcast', \
                'waning_gibbous'], \
  'latitude': -37.075418577826, \
  'longitude': 144.91838807607786, \
  'type': 'App'}, { 'AccelerometryCount': 9, \
  'AudioProcessedCount': 8, \
  'BatteryCount': 3, \
  'BatteryLevel': 69, \
  'EndDateTime': '2014-06-04', \
  'Kilometers': 0.1948995868377653, \
  'LocationCount': 6, \
  'MoonAge': 26.243771183524153, \
  'MoonIllumination': 0.5883010700711541, \
  'StartDateTime': '2014-06-04', \
  'Temperature': 33.81009761607972, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'rain', \
  'address': u'15 Brooke Frontage\nBlackwellburgh, ACT, 2635', \
  'keywords': [ 'May', \
                'Sunday', \
                '2005', \
                'spring', \
                'audio_home', \
                'audio_home', \
                'rain', \
                'waning_gibbous'], \
  'latitude': -39.6943128952132, \
  'longitude': 147.89460968066848, \
  'type': 'App'}, { 'AccelerometryCount': 1, \
  'AudioProcessedCount': 6, \
  'BatteryCount': 8, \
  'BatteryLevel': 92, \
  'EndDateTime': '2013-04-02', \
  'Kilometers': 0.4606598574611403, \
  'LocationCount': 8, \
  'MoonAge': 1.0418127231748509, \
  'MoonIllumination': 0.31567083617814795, \
  'StartDateTime': '2013-04-02', \
  'Temperature': 24.390188154140873, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'clear', \
  'address': u'349 /\n 04 Robertson Retreat\nLake Ricardofurt, WA, 9365', \
  'keywords': [ 'May', \
                'Tuesday', \
                '1990', \
                'winter', \
                'audio_home', \
                'clear', \
                'waxing_gibbous'], \
  'latitude': -37.225967836386175, \
  'longitude': 145.95845517840957, \
  'type': 'App'}, { 'AccelerometryCount': 7, \
  'AudioProcessedCount': 7, \
  'BatteryCount': 9, \
  'BatteryLevel': 86, \
  'EndDateTime': '2011-11-19', \
  'Kilometers': 1.31098626091625, \
  'LocationCount': 10, \
  'MoonAge': 18.904022674194806, \
  'MoonIllumination': 0.47728651133162026, \
  'StartDateTime': '2011-11-19', \
  'Temperature': 15.468338291602368, \
  'UserId': '70c669ee-325d-4c7c-b7a9-353c39624839', \
  'Weather': 'cloudy', \
  'address': u'14 Lisa Follow\nPort Kelly, SA, 7327', \
  'keywords': [ 'March', \
                'Tuesday', \
                '1975', \
                'autumn', \
                'audio_home', \
                'cloudy', \
                'waning_gibbous'], \
  'latitude': -37.18205774297304, \
  'longitude': 143.60000040561425, \
  'type': 'App'}, { 'AccelerometryCount': 3, \
  'AudioProcessedCount': 10, \
  'BatteryCount': 2, \
  'BatteryLevel': 61, \
  'EndDateTime': '2012-12-14', \
  'Kilometers': 0.624450591770048, \
  'LocationCount': 4, \
  'MoonAge': 0.5179927083566271, \
  'MoonIllumination': 0.41169974415460286, \
  'StartDateTime': '2012-12-14', \
  'Temperature': 31.836971246545076, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'rain', \
  'address': u'9 Hamilton Rest\nAllisonfort, SA, 2653', \
  'keywords': [ 'May', \
                'Thursday', \
                '2007', \
                'spring', \
                'audio_home', \
                'rain', \
                'waxing_gibbous'], \
  'latitude': -37.82221624751518, \
  'longitude': 144.12333174931658, \
  'type': 'App'}, { 'AccelerometryCount': 9, \
  'AudioProcessedCount': 11, \
  'BatteryCount': 9, \
  'BatteryLevel': 96, \
  'EndDateTime': '2012-01-02', \
  'StartDateTime': '2012-01-02', \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'keywords': [ 'December', \
                'Sunday', \
                '2002', \
                'winter', \
                'audio_home', \
                'audio_street', \
                'audio_car'], \
  'type': 'App'}, { 'AccelerometryCount': 11, \
  'AudioProcessedCount': 2, \
  'BatteryCount': 7, \
  'BatteryLevel': 70, \
  'EndDateTime': '2010-07-17', \
  'Kilometers': 0.4014611609306304, \
  'LocationCount': 5, \
  'MoonAge': 3.5359185230628465, \
  'MoonIllumination': 0.9628736036787228, \
  'StartDateTime': '2010-07-17', \
  'Temperature': 20.796370281637742, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'clear', \
  'address': u'9 David Plaza\nKarenfort, TAS, 2120', \
  'keywords': [ 'September', \
                'Monday', \
                '1974', \
                'spring', \
                'audio_street', \
                'clear', \
                'waxing_gibbous'], \
  'latitude': -38.009548919672376, \
  'longitude': 144.1534607668369, \
  'type': 'App'}, { 'AccelerometryCount': 11, \
  'AudioProcessedCount': 8, \
  'BatteryCount': 5, \
  'BatteryLevel': 44, \
  'EndDateTime': '2018-02-03', \
  'Kilometers': 1.3005353513483529, \
  'LocationCount': 9, \
  'MoonAge': 4.723703033594263, \
  'MoonIllumination': 0.7345777323339067, \
  'StartDateTime': '2018-02-03', \
  'Temperature': 7.980794039900463, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'cloudy', \
  'address': u'285 Timothy Turn\nJacquelineburgh, VIC, 5487', \
  'keywords': [ 'November', \
                'Wednesday', \
                '1975', \
                'autumn', \
                'audio_home', \
                'cloudy', \
                'waxing_gibbous'], \
  'latitude': -38.347012258736484, \
  'longitude': 145.6746396689485, \
  'type': 'App'}, { 'AccelerometryCount': 11, \
  'AudioProcessedCount': 9, \
  'BatteryCount': 4, \
  'BatteryLevel': 91, \
  'EndDateTime': '2016-07-21', \
  'Kilometers': 2.68208025750609, \
  'LocationCount': 10, \
  'MoonAge': 3.935940574199929, \
  'MoonIllumination': 0.5497437116720884, \
  'StartDateTime': '2016-07-21', \
  'Temperature': 19.07700291251358, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'clear', \
  'address': u'87 Miller Parklands\nNew Sarahland, TAS, 2812', \
  'keywords': [ 'March', \
                'Monday', \
                '1970', \
                'autumn', \
                'audio_home', \
                'clear', \
                'waxing_gibbous'], \
  'latitude': -37.05540455496199, \
  'longitude': 144.30941226356384, \
  'type': 'App'}, { 'AccelerometryCount': 7, \
  'AudioProcessedCount': 7, \
  'BatteryCount': 11, \
  'BatteryLevel': 63, \
  'EndDateTime': '2018-11-15', \
  'Kilometers': 0.734584314558446, \
  'LocationCount': 4, \
  'MoonAge': 10.574267723643612, \
  'MoonIllumination': 0.46649899193669164, \
  'StartDateTime': '2018-11-15', \
  'Temperature': -3.89846043226585, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'rain', \
  'address': u'72 Emily Deviation\nLake Madisonmouth, QLD, 5109', \
  'keywords': [ 'July', \
                'Saturday', \
                '1974', \
                'spring', \
                'audio_street', \
                'rain', \
                'waxing_gibbous'], \
  'latitude': -38.35056265880536, \
  'longitude': 145.80279123783248, \
  'type': 'App'}, { 'AccelerometryCount': 4, \
  'AudioProcessedCount': 8, \
  'BatteryCount': 2, \
  'BatteryLevel': 59, \
  'EndDateTime': '2016-05-18', \
  'Kilometers': 0.22250938392179254, \
  'LocationCount': 8, \
  'MoonAge': 17.49861807869579, \
  'MoonIllumination': 0.8668519720454576, \
  'StartDateTime': '2016-05-18', \
  'Temperature': 5.184014290432664, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'cloudy', \
  'address': u'Flat 13\n 4 Martinez Riverway\nNorth Brenda, WA, 5823', \
  'keywords': [ 'April', \
                'Friday', \
                '1994', \
                'spring', \
                'audio_home', \
                'audio_street', \
                'audio_car', \
                'audio_home', \
                'cloudy', \
                'waxing_gibbous'], \
  'latitude': -38.84717074207787, \
  'longitude': 143.89545988687038, \
  'type': 'App'}, { 'AccelerometryCount': 12, \
  'AudioProcessedCount': 6, \
  'BatteryCount': 4, \
  'BatteryLevel': 81, \
  'EndDateTime': '2018-01-22', \
  'Kilometers': 0.6959353573761176, \
  'LocationCount': 2, \
  'MoonAge': 27.416424424010607, \
  'MoonIllumination': 0.3306967290466363, \
  'StartDateTime': '2018-01-22', \
  'Temperature': 13.160946930597209, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'rain', \
  'address': u'Apt. 788\n 018 Jeffrey Ground\nEast Alexandra, NT, 2166', \
  'keywords': [ 'July', \
                'Saturday', \
                '1987', \
                'winter', \
                'audio_street', \
                'rain', \
                'waning_gibbous'], \
  'latitude': -36.37187087511672, \
  'longitude': 144.10714606305675, \
  'type': 'App'}, { 'AccelerometryCount': 4, \
  'AudioProcessedCount': 9, \
  'BatteryCount': 8, \
  'BatteryLevel': 80, \
  'EndDateTime': '2013-04-06', \
  'Kilometers': 0.21652595052140236, \
  'LocationCount': 4, \
  'MoonAge': 29.368718369494605, \
  'MoonIllumination': 0.9604125598863185, \
  'StartDateTime': '2013-04-06', \
  'Temperature': 16.234809582681983, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'overcast', \
  'address': u'530 /\n 0 Dana Laneway\nLisaborough, TAS, 2851', \
  'keywords': [ 'January', \
                'Friday', \
                '2016', \
                'autumn', \
                'audio_home', \
                'audio_car', \
                'audio_home', \
                'overcast', \
                'waxing_gibbous'], \
  'latitude': -39.27807666746985, \
  'longitude': 145.73637911417774, \
  'type': 'App'}, { 'AccelerometryCount': 11, \
  'AudioProcessedCount': 1, \
  'BatteryCount': 4, \
  'BatteryLevel': 84, \
  'EndDateTime': '2010-02-24', \
  'Kilometers': 0.024335451167485943, \
  'LocationCount': 9, \
  'MoonAge': 26.355735996229615, \
  'MoonIllumination': 0.7103335020498781, \
  'StartDateTime': '2010-02-24', \
  'Temperature': 9.638280234206842, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'overcast', \
  'address': u'0 Johnson Terrace\nEast Daniel, ACT, 0863', \
  'keywords': [ 'April', \
                'Tuesday', \
                '1974', \
                'autumn', \
                'audio_voice', \
                'overcast', \
                'waxing_gibbous'], \
  'latitude': -38.06609765653208, \
  'longitude': 145.24140850789746, \
  'type': 'App'}, { 'AccelerometryCount': 7, \
  'AudioProcessedCount': 11, \
  'BatteryCount': 8, \
  'BatteryLevel': 54, \
  'EndDateTime': '2014-03-06', \
  'StartDateTime': '2014-03-06', \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'keywords': [ 'December', \
                'Wednesday', \
                '1979', \
                'summer', \
                'audio_car', \
                'audio_home'], \
  'type': 'App'}, { 'AccelerometryCount': 11, \
  'AudioProcessedCount': 3, \
  'BatteryCount': 4, \
  'BatteryLevel': 99, \
  'EndDateTime': '2015-06-07', \
  'Kilometers': 2.375486457273549, \
  'LocationCount': 5, \
  'MoonAge': 9.154079565640147, \
  'MoonIllumination': 0.7742814959211132, \
  'StartDateTime': '2015-06-07', \
  'Temperature': 8.054856403652106, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'cloudy', \
  'address': u'43 William Quad\nDavidland, VIC, 2851', \
  'keywords': [ 'February', \
                'Monday', \
                '1988', \
                'summer', \
                'audio_voice', \
                'audio_home', \
                'audio_street', \
                'cloudy', \
                'waning_gibbous', \
                'church'], \
  'latitude': -37.90122210770134, \
  'longitude': 145.01280928387348, \
  'type': 'App'}, { 'AccelerometryCount': 1, \
  'AudioProcessedCount': 8, \
  'BatteryCount': 12, \
  'BatteryLevel': 53, \
  'EndDateTime': '2014-05-31', \
  'Kilometers': 0.18095531702850812, \
  'LocationCount': 9, \
  'MoonAge': 18.730156245964075, \
  'MoonIllumination': 0.2783270740223437, \
  'StartDateTime': '2014-05-31', \
  'Temperature': 20.449286130101186, \
  'UserId': 'd193b85f-009f-4dfe-a9ec-b0a5cbf8b26b', \
  'Weather': 'overcast', \
  'address': u'4 Mejia Trunkway\nBryantown, SA, 8656', \
  'keywords': [ 'June', \
                'Wednesday', \
                '1973', \
                'summer', \
                'audio_home', \
                'audio_car', \
                'overcast', \
                'waxing_gibbous'], \
  'latitude': -39.04123307219, \
  'longitude': 144.8691811520059, \
  'type': 'App'}, { 'AccelerometryCount': 8, \
  'AudioProcessedCount': 2, \
  'BatteryCount': 10, \
  'BatteryLevel': 32, \
  'EndDateTime': '2017-09-15', \
  'Kilometers': 0.5657083876714307, \
  'LocationCount': 9, \
  'MoonAge': 25.949875811241807, \
  'MoonIllumination': 0.5536085538493658, \
  'StartDateTime': '2017-09-15', \
  'Temperature': 21.707552604725954, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'overcast', \
  'address': u'Apt. 109\n 32 Taylor Common\nLongchester, NSW, 2670', \
  'keywords': [ 'January', \
                'Tuesday', \
                '2017', \
                'spring', \
                'audio_street', \
                'audio_home', \
                'overcast', \
                'waxing_gibbous'], \
  'latitude': -38.75845236287482, \
  'longitude': 144.65297627002917, \
  'type': 'App'}, { 'AccelerometryCount': 5, \
  'AudioProcessedCount': 9, \
  'BatteryCount': 4, \
  'BatteryLevel': 35, \
  'EndDateTime': '2013-07-03', \
  'Kilometers': 3.223388054982133, \
  'LocationCount': 4, \
  'MoonAge': 22.450743538835557, \
  'MoonIllumination': 0.6828523933679187, \
  'StartDateTime': '2013-07-03', \
  'Temperature': 21.453282394113717, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'rain', \
  'address': u'8 /\n 36 Welch Crossroad\nPort Matthew, SA, 2696', \
  'keywords': [ 'January', \
                'Friday', \
                '1986', \
                'summer', \
                'audio_home', \
                'rain', \
                'waxing_gibbous'], \
  'latitude': -37.6109534846908, \
  'longitude': 145.5413185269537, \
  'type': 'App'}, { 'AccelerometryCount': 12, \
  'AudioProcessedCount': 4, \
  'BatteryCount': 7, \
  'BatteryLevel': 34, \
  'EndDateTime': '2017-07-04', \
  'Kilometers': 0.21272306273272612, \
  'LocationCount': 10, \
  'MoonAge': 2.4844328075752955, \
  'MoonIllumination': 0.2591070203074939, \
  'StartDateTime': '2017-07-04', \
  'Temperature': 4.2773221438622215, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'rain', \
  'address': u'986 Wells Fire Track\nLake Marc, ACT, 2489', \
  'keywords': [ 'February', \
                'Thursday', \
                '1983', \
                'winter', \
                'audio_home', \
                'audio_street', \
                'audio_car', \
                'audio_home', \
                'rain', \
                'waning_gibbous'], \
  'latitude': -37.22529372858696, \
  'longitude': 145.8606938813122, \
  'type': 'App'}, { 'AccelerometryCount': 7, \
  'AudioProcessedCount': 5, \
  'BatteryCount': 12, \
  'BatteryLevel': 9, \
  'EndDateTime': '2010-08-25', \
  'Kilometers': 1.0161905592960898, \
  'LocationCount': 4, \
  'MoonAge': 16.013128079209483, \
  'MoonIllumination': 0.5695611005603824, \
  'StartDateTime': '2010-08-25', \
  'Temperature': 41.749981873732594, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'clear', \
  'address': u'2 /\n 154 Moody Corso\nShelleyfort, QLD, 6202', \
  'keywords': [ 'April', \
                'Friday', \
                '1978', \
                'summer', \
                'audio_car', \
                'audio_home', \
                'clear', \
                'waning_gibbous'], \
  'latitude': -39.01040124554501, \
  'longitude': 143.6751478843177, \
  'type': 'App'}, { 'AccelerometryCount': 2, \
  'AudioProcessedCount': 1, \
  'BatteryCount': 2, \
  'BatteryLevel': 36, \
  'EndDateTime': '2012-02-06', \
  'Kilometers': 0.3121306404224755, \
  'LocationCount': 4, \
  'MoonAge': 28.841720986950914, \
  'MoonIllumination': 0.549912238071871, \
  'StartDateTime': '2012-02-06', \
  'Temperature': -2.717126325580363, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'clear', \
  'address': u'578 /\n 9 Moore Common\nNew Stephenstad, WA, 2935', \
  'keywords': [ 'March', \
                'Friday', \
                '1997', \
                'autumn', \
                'audio_street', \
                'audio_home', \
                'audio_car', \
                'clear', \
                'waning_gibbous'], \
  'latitude': -37.481579088229005, \
  'longitude': 145.1346426710026, \
  'type': 'App'}, { 'AccelerometryCount': 11, \
  'AudioProcessedCount': 2, \
  'BatteryCount': 5, \
  'BatteryLevel': 88, \
  'EndDateTime': '2018-10-30', \
  'Kilometers': 0.34899119817603697, \
  'LocationCount': 8, \
  'MoonAge': 2.654234868658616, \
  'MoonIllumination': 0.6073721610580668, \
  'StartDateTime': '2018-10-30', \
  'Temperature': -6.905397247861732, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'clear', \
  'address': u'9 Williams Tollway\nNorth Laurieburgh, ACT, 2624', \
  'keywords': [ 'July', \
                'Monday', \
                '1993', \
                'spring', \
                'audio_street', \
                'clear', \
                'waning_gibbous'], \
  'latitude': -36.65255288493431, \
  'longitude': 145.27714711419574, \
  'type': 'App'}, { 'AccelerometryCount': 12, \
  'AudioProcessedCount': 8, \
  'BatteryCount': 10, \
  'BatteryLevel': 95, \
  'EndDateTime': '2015-07-28', \
  'Kilometers': 0.05326329637440035, \
  'LocationCount': 2, \
  'MoonAge': 27.588333313308617, \
  'MoonIllumination': 0.063012282819365, \
  'StartDateTime': '2015-07-28', \
  'Temperature': 7.088266829914685, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'clear', \
  'address': u'Suite 842\n 9 Moore Roadway\nEast Andrea, TAS, 2122', \
  'keywords': [ 'February', \
                'Tuesday', \
                '2007', \
                'autumn', \
                'audio_home', \
                'clear', \
                'waxing_gibbous'], \
  'latitude': -36.77477379838005, \
  'longitude': 144.0806781831104, \
  'type': 'App'}, { 'AccelerometryCount': 12, \
  'AudioProcessedCount': 7, \
  'BatteryCount': 9, \
  'BatteryLevel': 79, \
  'EndDateTime': '2015-05-17', \
  'StartDateTime': '2015-05-17', \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'keywords': ['February', 'Thursday', '2009', 'autumn', 'audio_home'], \
  'type': 'App'}, { 'AccelerometryCount': 8, \
  'AudioProcessedCount': 5, \
  'BatteryCount': 1, \
  'BatteryLevel': 76, \
  'EndDateTime': '2014-11-15', \
  'Kilometers': 0.3137550117855374, \
  'LocationCount': 6, \
  'MoonAge': 4.477603745379134, \
  'MoonIllumination': 0.42373689348828003, \
  'StartDateTime': '2014-11-15', \
  'Temperature': 25.974010270311986, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'rain', \
  'address': u'1 Fleming Mew\nSouth Daniel, VIC, 2920', \
  'keywords': [ 'November', \
                'Thursday', \
                '2009', \
                'winter', \
                'audio_home', \
                'rain', \
                'waning_gibbous'], \
  'latitude': -37.28899418332061, \
  'longitude': 145.07311711035416, \
  'type': 'App'}, { 'AccelerometryCount': 3, \
  'AudioProcessedCount': 3, \
  'BatteryCount': 9, \
  'BatteryLevel': 70, \
  'EndDateTime': '2015-02-10', \
  'Kilometers': 1.094400919490475, \
  'LocationCount': 4, \
  'MoonAge': 15.679833523375542, \
  'MoonIllumination': 0.4576335860518066, \
  'StartDateTime': '2015-02-10', \
  'Temperature': 20.92161413335754, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'rain', \
  'address': u'045 Michael Follow\nPort Susanland, NT, 4308', \
  'keywords': [ 'January', \
                'Saturday', \
                '2016', \
                'winter', \
                'audio_car', \
                'audio_home', \
                'rain', \
                'waning_gibbous'], \
  'latitude': -38.740931013599784, \
  'longitude': 145.8403659121897, \
  'type': 'App'}, { 'AccelerometryCount': 5, \
  'AudioProcessedCount': 5, \
  'BatteryCount': 10, \
  'BatteryLevel': 63, \
  'EndDateTime': '2018-09-03', \
  'Kilometers': 0.7095301095887605, \
  'LocationCount': 3, \
  'MoonAge': 7.936335850538815, \
  'MoonIllumination': 0.6438456003443969, \
  'StartDateTime': '2018-09-03', \
  'Temperature': 15.876597550775838, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'rain', \
  'address': u'434 Vega Wade\nRichardsonside, ACT, 2083', \
  'keywords': [ 'April', \
                'Tuesday', \
                '1996', \
                'summer', \
                'audio_home', \
                'rain', \
                'waning_gibbous'], \
  'latitude': -37.603997737335, \
  'longitude': 144.3276780269499, \
  'type': 'App'}, { 'AccelerometryCount': 2, \
  'AudioProcessedCount': 12, \
  'BatteryCount': 6, \
  'BatteryLevel': 97, \
  'EndDateTime': '2012-07-27', \
  'Kilometers': 0.5824890330826783, \
  'LocationCount': 2, \
  'MoonAge': 10.414874332109349, \
  'MoonIllumination': 0.5763629176952272, \
  'StartDateTime': '2012-07-27', \
  'Temperature': 32.87361342379758, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'rain', \
  'address': u'650 /\n 56 May Range\nNorth Lisashire, TAS, 5940', \
  'keywords': [ 'April', \
                'Friday', \
                '1987', \
                'winter', \
                'audio_home', \
                'rain', \
                'waxing_gibbous'], \
  'latitude': -36.87863933165809, \
  'longitude': 145.8312055303064, \
  'type': 'App'}, { 'AccelerometryCount': 5, \
  'AudioProcessedCount': 5, \
  'BatteryCount': 11, \
  'BatteryLevel': 99, \
  'EndDateTime': '2016-07-13', \
  'Kilometers': 0.1729330712984412, \
  'LocationCount': 1, \
  'MoonAge': 12.648502059164638, \
  'MoonIllumination': 2.178797601226634e-07, \
  'StartDateTime': '2016-07-13', \
  'Temperature': 5.170156412483442, \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'Weather': 'rain', \
  'address': u'6 Ryan Port\nWilliammouth, SA, 2896', \
  'keywords': [ 'January', \
                'Wednesday', \
                '2003', \
                'spring', \
                'audio_car', \
                'audio_street', \
                'rain', \
                'waning_gibbous'], \
  'latitude': -38.294920282090175, \
  'longitude': 145.74802169715232, \
  'type': 'App'}, { 'AccelerometryCount': 9, \
  'AudioProcessedCount': 2, \
  'BatteryCount': 10, \
  'BatteryLevel': 57, \
  'EndDateTime': '2015-09-10', \
  'StartDateTime': '2015-09-10', \
  'UserId': 'e34fc8b4-4040-479e-923f-8c49bec679a6', \
  'keywords': ['October', 'Saturday', '1977', 'summer', 'audio_home'], \
  'type': 'App'}, { 'AccelerometryCount': 4, \
  'AudioProcessedCount': 5, \
  'BatteryCount': 9, \
  'BatteryLevel': 20, \
  'EndDateTime': '2011-11-27', \
  'Kilometers': 1.79783467718011, \
  'LocationCount': 1, \
  'MoonAge': 11.426808943411316, \
  'MoonIllumination': 0.0751577230942494, \
  'StartDateTime': '2011-11-27', \
  'Temperature': 1.066543229537901, \
  'UserId': '2eafb6d7-fb41-4830-b97b-bf0e1023da16', \
  'Weather': 'rain', \
  'address': u'2 Darrell Plateau\nSmithland, QLD, 2973', \
  'keywords': [ 'May', \
                'Tuesday', \
                '2018', \
                'winter', \
                'audio_car', \
                'audio_street', \
                'rain', \
                'waning_gibbous'], \
  'latitude': -38.486284900953585, \
  'longitude': 145.45037241134793, \
  'type': 'App'}, { 'AccelerometryCount': 10, \
  'AudioProcessedCount': 11, \
  'BatteryCount': 10, \
  'BatteryLevel': 67, \
  'EndDateTime': '2010-08-24', \
  'Kilometers': 0.5651266855169107, \
  'LocationCount': 1, \
  'MoonAge': 0.07407916705533313, \
  'MoonIllumination': 0.8715796091526479, \
  'StartDateTime': '2010-08-24', \
  'Temperature': 21.029738039364847, \
  'UserId': '2eafb6d7-fb41-4830-b97b-bf0e1023da16', \
  'Weather': 'rain', \
  'address': u'987 Espinoza Brow\nEast Leah, SA, 2656', \
  'keywords': [ 'January', \
                'Wednesday', \
                '1976', \
                'autumn', \
                'audio_voice', \
                'audio_car', \
                'audio_street', \
                'audio_home', \
                'audio_home', \
                'rain', \
                'waning_gibbous'], \
  'latitude': -37.966474278947786, \
  'longitude': 145.1689062846299, \
  'type': 'App'}, { 'AccelerometryCount': 9, \
  'AudioProcessedCount': 6, \
  'BatteryCount': 8, \
  'BatteryLevel': 66, \
  'EndDateTime': '2016-10-26', \
  'StartDateTime': '2016-10-26', \
  'UserId': '2eafb6d7-fb41-4830-b97b-bf0e1023da16', \
  'keywords': [ 'August', \
                'Friday', \
                '1995', \
                'summer', \
                'audio_home', \
                'audio_street', \
                'audio_home', \
                'audio_car', \
                'audio_voice'], \
  'type': 'App'}, { 'AccelerometryCount': 8, \
  'AudioProcessedCount': 3, \
  'BatteryCount': 2, \
  'BatteryLevel': 43, \
  'EndDateTime': '2015-06-26', \
  'Kilometers': 1.3696095899467875, \
  'LocationCount': 5, \
  'MoonAge': 8.798297719634302, \
  'MoonIllumination': 0.6908562336300403, \
  'StartDateTime': '2015-06-26', \
  'Temperature': 9.787721316913213, \
  'UserId': '2eafb6d7-fb41-4830-b97b-bf0e1023da16', \
  'Weather': 'cloudy', \
  'address': u'Apt. 075\n 466 Harris Amble\nRobersonville, SA, 0970', \
  'keywords': [ 'November', \
                'Friday', \
                '2008', \
                'winter', \
                'audio_street', \
                'audio_voice', \
                'cloudy', \
                'waning_gibbous', \
                'cafe'], \
  'latitude': -35.97832436583084, \
  'longitude': 145.4342865697288, \
  'type': 'App'}, { 'AccelerometryCount': 10, \
  'AudioProcessedCount': 6, \
  'BatteryCount': 5, \
  'BatteryLevel': 19, \
  'EndDateTime': '2012-06-26', \
  'StartDateTime': '2012-06-26', \
  'UserId': '2eafb6d7-fb41-4830-b97b-bf0e1023da16', \
  'keywords': ['May', 'Monday', '2015', 'winter', 'audio_street'], \
  'type': 'App'}, { 'AccelerometryCount': 2, \
  'AudioProcessedCount': 11, \
  'BatteryCount': 7, \
  'BatteryLevel': 56, \
  'EndDateTime': '2012-05-01', \
  'StartDateTime': '2012-05-01', \
  'UserId': '2eafb6d7-fb41-4830-b97b-bf0e1023da16', \
  'keywords': ['October', 'Saturday', '2014', 'autumn', 'audio_home'], \
  'type': 'App'}, { 'AccelerometryCount': 7, \
  'AudioProcessedCount': 11, \
  'BatteryCount': 11, \
  'BatteryLevel': 4, \
  'EndDateTime': '2012-09-02', \
  'Kilometers': 0.06721417569948736, \
  'LocationCount': 3, \
  'MoonAge': 25.696105690940417, \
  'MoonIllumination': 0.35991011840436415, \
  'StartDateTime': '2012-09-02', \
  'Temperature': 27.782783778039278, \
  'UserId': '2eafb6d7-fb41-4830-b97b-bf0e1023da16', \
  'Weather': 'cloudy', \
  'address': u'936 /\n 0 Diana Tor\nCharlesport, NSW, 2910', \
  'keywords': [ 'September', \
                'Monday', \
                '1999', \
                'spring', \
                'audio_home', \
                'audio_car', \
                'cloudy', \
                'waxing_gibbous'], \
  'latitude': -38.538285134819574, \
  'longitude': 143.8530648063553, \
  'type': 'App'}, { 'AccelerometryCount': 3, \
  'AudioProcessedCount': 2, \
  'BatteryCount': 5, \
  'BatteryLevel': 16, \
  'EndDateTime': '2016-11-11', \
  'Kilometers': 0.21678011800456917, \
  'LocationCount': 3, \
  'MoonAge': 7.323742827627605, \
  'MoonIllumination': 0.5583157391131924, \
  'StartDateTime': '2016-11-11', \
  'Temperature': 18.223247021575958, \
  'UserId': '2eafb6d7-fb41-4830-b97b-bf0e1023da16', \
  'Weather': 'rain', \
  'address': u'60 Cynthia Piazza\nPort Carol, VIC, 2999', \
  'keywords': [ 'September', \
                'Friday', \
                '1986', \
                'spring', \
                'audio_street', \
                'rain', \
                'waxing_gibbous'], \
  'latitude': -39.37098058890374, \
  'longitude': 142.61842930803047, \
  'type': 'App'}, { 'AccelerometryCount': 10, \
  'AudioProcessedCount': 11, \
  'BatteryCount': 8, \
  'BatteryLevel': 60, \
  'EndDateTime': '2013-05-19', \
  'StartDateTime': '2013-05-19', \
  'UserId': '2eafb6d7-fb41-4830-b97b-bf0e1023da16', \
  'keywords': ['February', 'Wednesday', '1996', 'summer', 'audio_home'], \
  'type': 'App'}, { 'AccelerometryCount': 1, \
  'AudioProcessedCount': 1, \
  'BatteryCount': 9, \
  'BatteryLevel': 28, \
  'EndDateTime': '2017-01-20', \
  'Kilometers': 0.9688815864149494, \
  'LocationCount': 12, \
  'MoonAge': 14.949266860896067, \
  'MoonIllumination': 0.24853825061872625, \
  'StartDateTime': '2017-01-20', \
  'Temperature': 19.5827159225934, \
  'UserId': '2eafb6d7-fb41-4830-b97b-bf0e1023da16', \
  'Weather': 'overcast', \
  'address': u'Level 4\n 50 Elizabeth Quadrangle\nWest Zachary, WA, 2949', \
  'keywords': [ 'November', \
                'Friday', \
                '2008', \
                'summer', \
                'audio_home', \
                'overcast', \
                'waxing_gibbous', \
                'cafe'], \
  'latitude': -37.345959840186296, \
  'longitude': 145.35408116539864, \
  'type': 'App'}, { 'AccelerometryCount': 10, \
  'AudioProcessedCount': 10, \
  'BatteryCount': 11, \
  'BatteryLevel': 80, \
  'EndDateTime': '2015-04-14', \
  'Kilometers': 0.5577642672218468, \
  'LocationCount': 6, \
  'MoonAge': 21.866383342859983, \
  'MoonIllumination': 0.26856002932444845, \
  'StartDateTime': '2015-04-14', \
  'Temperature': 17.25148589021851, \
  'UserId': '10dac7d9-b3ee-4a99-860a-24895806a032', \
  'Weather': 'rain', \
  'address': u'Suite 281\n 259 Davis Byway\nCoopertown, WA, 5945', \
  'keywords': [ 'March', \
                'Thursday', \
                '2001', \
                'winter', \
                'audio_street', \
                'audio_home', \
                'rain', \
                'waning_gibbous'], \
  'latitude': -38.04926522087483, \
  'longitude': 145.8405289562623, \
  'type': 'App'}, { 'AccelerometryCount': 12, \
  'AudioProcessedCount': 5, \
  'BatteryCount': 5, \
  'BatteryLevel': 24, \
  'EndDateTime': '2010-02-07', \
  'Kilometers': 1.031750523928769, \
  'LocationCount': 11, \
  'MoonAge': 28.53762171419499, \
  'MoonIllumination': 0.16661074636724527, \
  'StartDateTime': '2010-02-07', \
  'Temperature': 19.488904823749287, \
  'UserId': '10dac7d9-b3ee-4a99-860a-24895806a032', \
  'Weather': 'cloudy', \
  'address': u'69 Luis Corso\nSt. Cassandramouth, NSW, 2909', \
  'keywords': [ 'July', \
                'Saturday', \
                '1979', \
                'winter', \
                'audio_street', \
                'audio_home', \
                'audio_voice', \
                'cloudy', \
                'waning_gibbous'], \
  'latitude': -38.269216437473595, \
  'longitude': 144.81439527510784, \
  'type': 'App'}, { 'AccelerometryCount': 2, \
  'AudioProcessedCount': 3, \
  'BatteryCount': 8, \
  'BatteryLevel': 61, \
  'EndDateTime': '2011-10-06', \
  'Kilometers': 0.7319298390292647, \
  'LocationCount': 4, \
  'MoonAge': 13.987846319030572, \
  'MoonIllumination': 0.28465379457774553, \
  'StartDateTime': '2011-10-06', \
  'Temperature': 29.777841424377776, \
  'UserId': '10dac7d9-b3ee-4a99-860a-24895806a032', \
  'Weather': 'clear', \
  'address': u'94 Michael Causeway\nWhitefurt, SA, 2992', \
  'keywords': [ 'December', \
                'Sunday', \
                '1989', \
                'spring', \
                'audio_street', \
                'audio_voice', \
                'audio_home', \
                'clear', \
                'waning_gibbous'], \
  'latitude': -39.664499255923985, \
  'longitude': 143.9684337093626, \
  'type': 'App'}, { 'AccelerometryCount': 10, \
  'AudioProcessedCount': 5, \
  'BatteryCount': 6, \
  'BatteryLevel': 3, \
  'EndDateTime': '2017-09-29', \
  'Kilometers': 0.25277438042717315, \
  'LocationCount': 9, \
  'MoonAge': 9.890901606188544, \
  'MoonIllumination': 0.39344491371017487, \
  'StartDateTime': '2017-09-29', \
  'Temperature': 20.333972337302832, \
  'UserId': '10dac7d9-b3ee-4a99-860a-24895806a032', \
  'Weather': 'overcast', \
  'address': u'0 /\n 9 Cody Square\nNorth Kimberlyborough, SA, 3162', \
  'keywords': [ 'September', \
                'Monday', \
                '1987', \
                'winter', \
                'audio_car', \
                'overcast', \
                'waxing_gibbous'], \
  'latitude': -38.62138185226698, \
  'longitude': 143.9469983958724, \
  'type': 'App'}, { 'AccelerometryCount': 5, \
  'AudioProcessedCount': 5, \
  'BatteryCount': 4, \
  'BatteryLevel': 96, \
  'EndDateTime': '2012-01-19', \
  'Kilometers': 4.78206186351646, \
  'LocationCount': 10, \
  'MoonAge': 9.641475736566811, \
  'MoonIllumination': 0.12407543010070043, \
  'StartDateTime': '2012-01-19', \
  'Temperature': 9.404031418053018, \
  'UserId': '10dac7d9-b3ee-4a99-860a-24895806a032', \
  'Weather': 'cloudy', \
  'address': u'Suite 865\n 3 Ethan Ronde\nSmithfurt, QLD, 2987', \
  'keywords': [ 'December', \
                'Saturday', \
                '1998', \
                'summer', \
                'audio_car', \
                'cloudy', \
                'waning_gibbous'], \
  'latitude': -38.361233757905275, \
  'longitude': 145.5178337200036, \
  'type': 'App'}, { 'AccelerometryCount': 8, \
  'AudioProcessedCount': 1, \
  'BatteryCount': 6, \
  'BatteryLevel': 53, \
  'EndDateTime': '2014-09-27', \
  'Kilometers': 1.935944321058681, \
  'LocationCount': 3, \
  'MoonAge': 21.61094848067285, \
  'MoonIllumination': 0.10907076161329365, \
  'StartDateTime': '2014-09-27', \
  'Temperature': 27.631687711082456, \
  'UserId': '10dac7d9-b3ee-4a99-860a-24895806a032', \
  'Weather': 'cloudy', \
  'address': u'142 Leonard Road\nLake Loriburgh, WA, 2037', \
  'keywords': [ 'January', \
                'Sunday', \
                '2003', \
                'winter', \
                'audio_voice', \
                'audio_car', \
                'cloudy', \
                'waxing_gibbous'], \
  'latitude': -37.51215436031478, \
  'longitude': 146.21366939521212, \
  'type': 'App'}, { 'AccelerometryCount': 8, \
  'AudioProcessedCount': 2, \
  'BatteryCount': 9, \
  'BatteryLevel': 2, \
  'EndDateTime': '2012-09-07', \
  'Kilometers': 1.2776226866667637, \
  'LocationCount': 5, \
  'MoonAge': 15.346159290488938, \
  'MoonIllumination': 0.6775248132018616, \
  'StartDateTime': '2012-09-07', \
  'Temperature': 10.183798822005365, \
  'UserId': '10dac7d9-b3ee-4a99-860a-24895806a032', \
  'Weather': 'cloudy', \
  'address': u'880 /\n 82 Timothy Fairway\nSandersberg, QLD, 2612', \
  'keywords': [ 'September', \
                'Monday', \
                '1993', \
                'summer', \
                'audio_street', \
                'cloudy', \
                'waning_gibbous'], \
  'latitude': -37.06459195363852, \
  'longitude': 145.9799895235096, \
  'type': 'App'}, { 'AccelerometryCount': 6, \
  'AudioProcessedCount': 6, \
  'BatteryCount': 10, \
  'BatteryLevel': 78, \
  'EndDateTime': '2018-02-13', \
  'Kilometers': 0.9559059371959108, \
  'LocationCount': 10, \
  'MoonAge': 14.797448655221343, \
  'MoonIllumination': 0.5197753949208793, \
  'StartDateTime': '2018-02-13', \
  'Temperature': 17.868792456394637, \
  'UserId': '10dac7d9-b3ee-4a99-860a-24895806a032', \
  'Weather': 'cloudy', \
  'address': u'524 Marshall Intersection\nWest Michaeltown, QLD, 2626', \
  'keywords': [ 'April', \
                'Wednesday', \
                '1985', \
                'winter', \
                'audio_car', \
                'cloudy', \
                'waxing_gibbous'], \
  'latitude': -38.5363626603198, \
  'longitude': 145.27998494150216, \
  'type': 'App'}, { 'AccelerometryCount': 1, \
  'AudioProcessedCount': 7, \
  'BatteryCount': 5, \
  'BatteryLevel': 7, \
  'EndDateTime': '2013-05-23', \
  'Kilometers': 0.9419611681874849, \
  'LocationCount': 8, \
  'MoonAge': 27.649589834311026, \
  'MoonIllumination': 0.42058774316728464, \
  'StartDateTime': '2013-05-23', \
  'Temperature': 35.4797243105823, \
  'UserId': '10dac7d9-b3ee-4a99-860a-24895806a032', \
  'Weather': 'cloudy', \
  'address': u'92 Vazquez Grove\nNorth Melissa, VIC, 2967', \
  'keywords': [ 'May', \
                'Wednesday', \
                '1982', \
                'winter', \
                'audio_street', \
                'audio_voice', \
                'cloudy', \
                'waning_gibbous', \
                'cafe'], \
  'latitude': -37.61011220208231, \
  'longitude': 143.4746138851298, \
  'type': 'App'}, { 'AccelerometryCount': 1, \
  'AudioProcessedCount': 9, \
  'BatteryCount': 9, \
  'BatteryLevel': 13, \
  'EndDateTime': '2012-05-21', \
  'Kilometers': 0.3795230369353105, \
  'LocationCount': 9, \
  'MoonAge': 23.475742009055942, \
  'MoonIllumination': 0.07079928503457822, \
  'StartDateTime': '2012-05-21', \
  'Temperature': 2.8803555918947072, \
  'UserId': '10dac7d9-b3ee-4a99-860a-24895806a032', \
  'Weather': 'rain', \
  'address': u'Level 6\n 94 Ritter Roadside\nPort Stephanie, QLD, 2434', \
  'keywords': [ 'January', \
                'Saturday', \
                '1976', \
                'summer', \
                'audio_home', \
                'audio_street', \
                'rain', \
                'waxing_gibbous'], \
  'latitude': -39.12135149340159, \
  'longitude': 146.35657408735688, \
  'type': 'App'}]


Events = [Event(d) for d in data]
DemoEvents = Events

