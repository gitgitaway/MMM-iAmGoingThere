import json, os

base = os.path.dirname(os.path.abspath(__file__))

data = {
  'panama_city': {
    'things': [
      {'rank':1,'name':'Panama Canal (Miraflores Locks)','postcode':'0816','distanceKmFromAirport':50,'description':'Watch container ships pass through one of the world\'s greatest engineering achievements','distance':15.0,'URL':'https://micanaldepanama.com/'},
      {'rank':2,'name':'Casco Viejo (Old Quarter)','postcode':'0843','distanceKmFromAirport':37,'description':'UNESCO World Heritage Spanish colonial quarter with French and American architecture','distance':2.0,'URL':'https://www.cascoviejo.org/'},
      {'rank':3,'name':'San Blas Islands (Guna Yala)','postcode':'0000','distanceKmFromAirport':80,'description':'370 palm-fringed islands governed by the Guna indigenous people with perfect beaches','distance':100.0,'URL':'https://www.gunayala.gob.pa/'},
      {'rank':4,'name':'Metropolitan Natural Park','postcode':'0816','distanceKmFromAirport':40,'description':'Tropical forest within the city limits with sloths, toucans and anteaters','distance':5.0,'URL':'https://www.parquemetropolitano.org/'},
      {'rank':5,'name':'Biomuseo','postcode':'0843','distanceKmFromAirport':42,'description':'Frank Gehry-designed museum on the continental divide and Panama\'s biodiversity','distance':7.0,'URL':'https://www.biomuseopanama.org/'},
      {'rank':6,'name':'Panama Viejo Archaeological Site','postcode':'0801','distanceKmFromAirport':30,'description':'Ruins of the first European city on the Pacific, razed by pirate Henry Morgan in 1671','distance':5.0,'URL':'https://www.panamaviejo.org/'},
      {'rank':7,'name':'Amador Causeway','postcode':'0843','distanceKmFromAirport':43,'description':'3km causeway of islands connected to the city with restaurants and the new Biomuseo','distance':8.0,'URL':'https://www.calzadadeamador.com/'},
      {'rank':8,'name':'Gamboa Rainforest & Monkey Island','postcode':'0816','distanceKmFromAirport':55,'description':'Boat trip on Gatun Lake to Monkey Island teeming with howler, capuchin and spider monkeys','distance':28.0,'URL':'https://www.gamboaresort.com/'},
      {'rank':9,'name':'Miraflores Visitors Centre','postcode':'0816','distanceKmFromAirport':50,'description':'Best view of the Canal locks with a museum and 3D IMAX film','distance':15.0,'URL':'https://micanaldepanama.com/'},
      {'rank':10,'name':'Mercado de Mariscos (Fish Market)','postcode':'0843','distanceKmFromAirport':36,'description':'Ceviche and fresh seafood directly from the Pacific at the historic fish market','distance':1.0,'URL':''},
    ]
  },
  'paphos': {
    'things': [
      {'rank':1,'name':'Paphos Archaeological Park','postcode':'8010','distanceKmFromAirport':8,'description':'UNESCO World Heritage site with extraordinary Roman floor mosaics of Dionysus, Theseus and Orpheus','distance':1.0,'URL':'https://www.mcw.gov.cy/'},
      {'rank':2,'name':'Tombs of the Kings','postcode':'8010','distanceKmFromAirport':9,'description':'UNESCO-listed underground rock-cut tombs used by Ptolemaic aristocracy from the 4th century BC','distance':3.0,'URL':'https://www.mcw.gov.cy/'},
      {'rank':3,'name':'Aphrodite\'s Rock (Petra tou Romiou)','postcode':'8510','distanceKmFromAirport':17,'description':'Legendary birthplace of Aphrodite - a spectacular sea stack on the coastal road','distance':15.0,'URL':'https://www.visitcyprus.com/'},
      {'rank':4,'name':'Paphos Castle','postcode':'8010','distanceKmFromAirport':8,'description':'Medieval Byzantine castle at the harbour entrance, converted into a wine store by the Ottomans','distance':1.0,'URL':'https://www.mcw.gov.cy/'},
      {'rank':5,'name':'Kato Paphos Harbour','postcode':'8010','distanceKmFromAirport':8,'description':'Picturesque old harbour with fishing boats, fish restaurants and the castle','distance':1.0,'URL':'https://www.visitpafos.org.cy/'},
      {'rank':6,'name':'Akamas Peninsula National Park','postcode':'8830','distanceKmFromAirport':40,'description':'Wild headland with the Aphrodite Trail, Blue Lagoon at Agios Georgios and sea turtles','distance':35.0,'URL':'https://www.visitcyprus.com/'},
      {'rank':7,'name':'Kouklia (Old Paphos)','postcode':'8500','distanceKmFromAirport':14,'description':'Site of the great Sanctuary of Aphrodite and the Lusignan manor house museum','distance':14.0,'URL':'https://www.mcw.gov.cy/'},
      {'rank':8,'name':'Coral Bay Beach','postcode':'8099','distanceKmFromAirport':18,'description':'Excellent sandy beach north of Paphos with watersports and beach clubs','distance':12.0,'URL':'https://www.visitpafos.org.cy/'},
      {'rank':9,'name':'St Neophytos Monastery','postcode':'8040','distanceKmFromAirport':14,'description':'12th-century monastery carved into a cliff with remarkable Byzantine frescoes','distance':9.0,'URL':'https://www.neophytosmonastery.com/'},
      {'rank':10,'name':'Troodos Mountains & Kykkos Monastery','postcode':'4820','distanceKmFromAirport':67,'description':'Day trip to Cyprus\'s highest peaks with Byzantine painted churches and the richest monastery','distance':60.0,'URL':'https://www.kykkos-museum.cy.net/'},
    ]
  },
  'paramaribo': {
    'things': [
      {'rank':1,'name':'Historic Inner City (Paramaribo Old Town)','postcode':'','distanceKmFromAirport':46,'description':'UNESCO World Heritage Dutch colonial city with a unique Caribbean wooden architecture','distance':0.5,'URL':'https://www.surinametourism.sr/'},
      {'rank':2,'name':'Saint Peter and Paul Cathedral','postcode':'','distanceKmFromAirport':46,'description':'One of the largest wooden structures in the Western Hemisphere built by Dutch Redemptorists','distance':0.5,'URL':''},
      {'rank':3,'name':'Central Market (Centrale Markt)','postcode':'','distanceKmFromAirport':46,'description':'Multi-ethnic market reflecting Suriname\'s extraordinary diversity - Creole, Javanese, Chinese','distance':0.5,'URL':''},
      {'rank':4,'name':'Joden Savanne Jewish Cemetery','postcode':'','distanceKmFromAirport':95,'description':'Ruins of the oldest synagogue in the Western Hemisphere built by Sephardic Jews in 1671','distance':50.0,'URL':''},
      {'rank':5,'name':'Fort Zeelandia Museum','postcode':'','distanceKmFromAirport':46,'description':'17th-century Dutch fort on the Suriname River now housing historical collections','distance':0.5,'URL':'https://www.surinamemuseum.sr/'},
      {'rank':6,'name':'Brownsberg Nature Park','postcode':'','distanceKmFromAirport':165,'description':'Rainforest park above the Brokopondo reservoir with howler monkeys and toucans','distance':120.0,'URL':'https://www.stinasu.sr/'},
      {'rank':7,'name':'Neveh Shalom Synagogue','postcode':'','distanceKmFromAirport':46,'description':'Active 1834 synagogue with a sand floor - oldest in continuous use in the Americas','distance':0.5,'URL':''},
      {'rank':8,'name':'Commewijne District Plantation Cruise','postcode':'','distanceKmFromAirport':55,'description':'River boat to former Dutch coffee and sugar plantations with dolphins','distance':10.0,'URL':''},
      {'rank':9,'name':'Central Suriname Nature Reserve','postcode':'','distanceKmFromAirport':245,'description':'UNESCO World Heritage 1.6 million hectares of pristine Amazon rainforest','distance':200.0,'URL':''},
      {'rank':10,'name':'Pom Cassava & Chicken Dish','postcode':'','distanceKmFromAirport':45,'description':'Suriname\'s national dish - pomtajer root with chicken, lemon and spices','distance':1.0,'URL':''},
    ]
  },
  'paro': {
    'things': [
      {'rank':1,'name':'Taktsang Monastery (Tiger\'s Nest)','postcode':'12001','distanceKmFromAirport':16,'description':'Bhutan\'s most iconic image - a monastery clinging to a 900m cliff above Paro Valley','distance':10.0,'URL':'https://www.tourism.gov.bt/'},
      {'rank':2,'name':'Rinpung Dzong','postcode':'12001','distanceKmFromAirport':9,'description':'16th-century fortified monastery housing the monk body and district administration','distance':0.5,'URL':'https://www.tourism.gov.bt/'},
      {'rank':3,'name':'National Museum of Bhutan','postcode':'12001','distanceKmFromAirport':9,'description':'Inside the 17th-century Ta Dzong watchtower with Bhutan\'s finest cultural collection','distance':1.0,'URL':'https://www.nationalmuseumbhutan.gov.bt/'},
      {'rank':4,'name':'Kyichu Lhakhang','postcode':'12001','distanceKmFromAirport':9,'description':'7th-century temple built by King Songtsen Gampo - one of the oldest in Bhutan','distance':3.0,'URL':'https://www.tourism.gov.bt/'},
      {'rank':5,'name':'Paro Valley Walk','postcode':'12001','distanceKmFromAirport':10,'description':'Walk through rice fields, apple orchards and traditional farmhouses in the valley','distance':2.0,'URL':'https://www.tourism.gov.bt/'},
      {'rank':6,'name':'Dochula Pass & 108 Memorial Chortens','postcode':'11001','distanceKmFromAirport':55,'description':'Mountain pass at 3,100m with 108 chortens and Himalayan panorama to Tibet','distance':50.0,'URL':'https://www.tourism.gov.bt/'},
      {'rank':7,'name':'Punakha Dzong','postcode':'13001','distanceKmFromAirport':80,'description':'17th-century dzong at the confluence of two rivers - Bhutan\'s most beautiful','distance':75.0,'URL':'https://www.tourism.gov.bt/'},
      {'rank':8,'name':'Thimphu Tashichho Dzong','postcode':'11001','distanceKmFromAirport':62,'description':'Bhutan\'s 13th century capital fortress monastery and seat of the government','distance':55.0,'URL':'https://www.tourism.gov.bt/'},
      {'rank':9,'name':'Bhutan International Festival (Tsechu)','postcode':'12001','distanceKmFromAirport':8,'description':'Ancient tantric mask dances performed by monks - dates vary by monastery','distance':0.5,'URL':'https://www.tourism.gov.bt/'},
      {'rank':10,'name':'Ema Datshi (Chilli Cheese)','postcode':'12001','distanceKmFromAirport':8,'description':'Bhutan\'s national dish - whole red and green chillies cooked in fresh yak cheese sauce','distance':1.0,'URL':''},
    ]
  },
  'penang': {
    'things': [
      {'rank':1,'name':'George Town Historic District','postcode':'10000','distanceKmFromAirport':17,'description':'UNESCO World Heritage colonial city with the finest collection of pre-war buildings in Asia','distance':1.0,'URL':'https://gtwhi.com.my/'},
      {'rank':2,'name':'Penang Street Art','postcode':'10000','distanceKmFromAirport':17,'description':'Ironwork sculptures and painted murals by Ernest Zacharevic throughout George Town','distance':1.0,'URL':'https://www.penangstreetart.com/'},
      {'rank':3,'name':'Penang Hill (Bukit Bendera)','postcode':'10350','distanceKmFromAirport':22,'description':'Cable car to the summit with colonial bungalows, an owl museum and cooler temperatures','distance':6.0,'URL':'https://www.penanghill.gov.my/'},
      {'rank':4,'name':'Kek Lok Si Temple','postcode':'10460','distanceKmFromAirport':23,'description':'Southeast Asia\'s largest Buddhist temple complex with a 36m bronze Kuan Yin statue','distance':7.0,'URL':'https://kekloksitemple.com/'},
      {'rank':5,'name':'Penang National Park','postcode':'11050','distanceKmFromAirport':40,'description':'Smallest national park in Malaysia with pristine beaches and a turtle sanctuary','distance':25.0,'URL':'https://www.forestry.gov.my/'},
      {'rank':6,'name':'Clan Jetties','postcode':'10050','distanceKmFromAirport':17,'description':'Chinese clan house villages built on stilts over the water - unique heritage communities','distance':1.5,'URL':'https://www.visitpenang.gov.my/'},
      {'rank':7,'name':'Penang Food Trail','postcode':'10000','distanceKmFromAirport':17,'description':'Char kway teow, assam laksa, cendol and rojak - Penang is Malaysia\'s food capital','distance':1.0,'URL':'https://www.visitpenang.gov.my/'},
      {'rank':8,'name':'Little India (Brickfields)','postcode':'10050','distanceKmFromAirport':17,'description':'Bustling Indian quarter with temples, sari shops and the best roti canai on the island','distance':1.0,'URL':'https://www.visitpenang.gov.my/'},
      {'rank':9,'name':'Cheong Fatt Tze Mansion (Blue Mansion)','postcode':'10050','distanceKmFromAirport':17,'description':'UNESCO-award winning 38-room indigo blue Victorian mansion open for tours','distance':1.0,'URL':'https://cheongfatttzemansion.com/'},
      {'rank':10,'name':'Batu Ferringhi Beach','postcode':'11100','distanceKmFromAirport':30,'description':'North coast resort beach with a famous night market and watersports','distance':15.0,'URL':'https://www.visitpenang.gov.my/'},
    ]
  },
  'perth': {
    'things': [
      {'rank':1,'name':'Kings Park & Botanic Garden','postcode':'WA 6005','distanceKmFromAirport':20,'description':'One of the world\'s largest city parks with wildflower displays above the Swan River','distance':2.0,'URL':'https://www.bgpa.wa.gov.au/kings-park'},
      {'rank':2,'name':'Rottnest Island','postcode':'WA 6161','distanceKmFromAirport':37,'description':'Quokka-filled island paradise with car-free beaches, snorkelling and cycling','distance':19.0,'URL':'https://www.rottnestisland.com/'},
      {'rank':3,'name':'Fremantle','postcode':'WA 6160','distanceKmFromAirport':32,'description':'Maritime heritage port city with the Fremantle Prison, markets and craft beer scene','distance':20.0,'URL':'https://www.visitfremantle.com.au/'},
      {'rank':4,'name':'Cottesloe Beach','postcode':'WA 6011','distanceKmFromAirport':27,'description':'Perth\'s premier white-sand surf beach with the Indiana Tea House and coral reef','distance':12.0,'URL':'https://www.cottesloe.wa.gov.au/'},
      {'rank':5,'name':'Swan Valley Wine Region','postcode':'WA 6055','distanceKmFromAirport':16,'description':'Perth\'s oldest wine region with cellar doors, chocolate factories and cheese farms','distance':25.0,'URL':'https://www.swanvalley.com.au/'},
      {'rank':6,'name':'Northbridge','postcode':'WA 6003','distanceKmFromAirport':19,'description':'Cultural precinct with the Art Gallery of WA, WA Museum and Perth\'s best nightlife','distance':1.0,'URL':'https://northbridge.com.au/'},
      {'rank':7,'name':'Pinnacles Desert','postcode':'WA 6522','distanceKmFromAirport':250,'description':'Extraordinary limestone pillars rising from yellow sand in Nambung National Park','distance':245.0,'URL':'https://parks.dpaw.wa.gov.au/park/nambung'},
      {'rank':8,'name':'Perth Zoo','postcode':'WA 6151','distanceKmFromAirport':21,'description':'Compact zoo with Australian wildlife, African savannah and orangutans','distance':3.0,'URL':'https://www.perthzoo.wa.gov.au/'},
      {'rank':9,'name':'Yanchep National Park','postcode':'WA 6035','distanceKmFromAirport':58,'description':'Koalas in the wild, ancient caves and beautiful bushland north of the city','distance':51.0,'URL':'https://parks.dpaw.wa.gov.au/park/yanchep'},
      {'rank':10,'name':'Elizabeth Quay','postcode':'WA 6000','distanceKmFromAirport':19,'description':'Waterfront precinct on the Swan River with restaurants, art and the Bell Tower','distance':1.0,'URL':'https://elizabethquay.com.au/'},
    ]
  },
  'phnom_penh': {
    'things': [
      {'rank':1,'name':'Royal Palace & Silver Pagoda','postcode':'12301','distanceKmFromAirport':11,'description':'The royal residence with the Silver Pagoda housing a life-sized gold Buddha encrusted with diamonds','distance':1.0,'URL':'https://www.royalpalace.gov.kh/'},
      {'rank':2,'name':'Tuol Sleng Genocide Museum (S-21)','postcode':'12304','distanceKmFromAirport':12,'description':'Former Khmer Rouge prison where 17,000 were tortured - essential and harrowing history','distance':2.0,'URL':'https://tuolsleng.gov.kh/'},
      {'rank':3,'name':'Choeung Ek Killing Fields','postcode':'12101','distanceKmFromAirport':25,'description':'Memorial to the 17,000 victims executed here during the Khmer Rouge genocide','distance':15.0,'URL':'https://www.killingfieldsmuseum.com/'},
      {'rank':4,'name':'National Museum of Cambodia','postcode':'12202','distanceKmFromAirport':11,'description':'World\'s finest collection of Khmer art with sculptures from Angkor Wat','distance':1.0,'URL':'https://www.cambodiamuseum.info/'},
      {'rank':5,'name':'Riverside Promenade (Sisowath Quay)','postcode':'12201','distanceKmFromAirport':10,'description':'Sunset drinks on the promenade where the Mekong and Tonle Sap rivers merge','distance':0.5,'URL':''},
      {'rank':6,'name':'Central Market (Phsar Thmei)','postcode':'12210','distanceKmFromAirport':11,'description':'1930s Art Deco market with a distinctive yellow dome selling gold, gems and souvenirs','distance':1.0,'URL':''},
      {'rank':7,'name':'Russian Market (Phsar Toul Tom Poung)','postcode':'12303','distanceKmFromAirport':13,'description':'Best local market for handicrafts, silk, Buddha statues and cheap street food','distance':2.5,'URL':''},
      {'rank':8,'name':'Wat Phnom','postcode':'12202','distanceKmFromAirport':11,'description':'Hill temple that gave the city its name, with a reclining Buddha and resident monkeys','distance':1.0,'URL':''},
      {'rank':9,'name':'Cambodian Living Arts Performance','postcode':'12202','distanceKmFromAirport':11,'description':'Traditional apsara dance and classical Khmer music performed by genocide survivors','distance':1.0,'URL':'https://www.cambodianlivingarts.org/'},
      {'rank':10,'name':'Mekong River Sunset Cruise','postcode':'12201','distanceKmFromAirport':10,'description':'Sunset boat cruise on the great river with Angkor beer and views of the Royal Palace','distance':0.5,'URL':''},
    ]
  },
  'phuket': {
    'things': [
      {'rank':1,'name':'Phi Phi Islands Day Trip','postcode':'81000','distanceKmFromAirport':75,'description':'Speedboat day trip to stunning limestone islands - snorkel Maya Bay from The Beach film','distance':45.0,'URL':'https://www.phi-phi.com/'},
      {'rank':2,'name':'Patong Beach','postcode':'83150','distanceKmFromAirport':42,'description':'Phuket\'s most famous and lively beach with watersports, beach clubs and Bangla Road nightlife','distance':15.0,'URL':'https://www.tourismthailand.org/'},
      {'rank':3,'name':'Big Buddha Phuket','postcode':'83130','distanceKmFromAirport':37,'description':'45m white marble Buddha on Nakkerd Hill visible from across the island','distance':8.0,'URL':'https://www.bigbuddha.co/'},
      {'rank':4,'name':'Phuket Old Town','postcode':'83000','distanceKmFromAirport':33,'description':'Sino-Portuguese shophouses, temples and art cafes in Phuket\'s historic centre','distance':1.0,'URL':'https://www.phuketoldtown.com/'},
      {'rank':5,'name':'Phang Nga Bay (James Bond Island)','postcode':'82000','distanceKmFromAirport':52,'description':'Limestone karst islands including Khao Phing Kan from The Man with the Golden Gun','distance':70.0,'URL':'https://www.tourismthailand.org/'},
      {'rank':6,'name':'Kata & Karon Beaches','postcode':'83100','distanceKmFromAirport':47,'description':'Long sandy beaches south of Patong with cleaner water and calmer atmosphere','distance':18.0,'URL':'https://www.tourismthailand.org/'},
      {'rank':7,'name':'Simon Cabaret Show','postcode':'83150','distanceKmFromAirport':44,'description':'Phuket\'s famous ladyboy cabaret performance - spectacular costumes and entertainment','distance':15.0,'URL':'https://www.simoncabaret.com/'},
      {'rank':8,'name':'Khao Sok National Park Day Trip','postcode':'84250','distanceKmFromAirport':85,'description':'Jungle safari with ancient rainforest, giant Rafflesia flowers and kayaking on Cheow Lan Lake','distance':100.0,'URL':'https://www.khaosok.com/'},
      {'rank':9,'name':'Thai Cooking Class','postcode':'83000','distanceKmFromAirport':34,'description':'Market visit and cooking class learning to make tom yum, green curry and pad thai','distance':2.0,'URL':'https://www.tourismthailand.org/'},
      {'rank':10,'name':'Elephant Sanctuary Visit','postcode':'83110','distanceKmFromAirport':25,'description':'Ethical elephant sanctuary in the hills where rescued elephants roam freely','distance':15.0,'URL':'https://www.elephantjungle.com/'},
    ]
  },
  'pisa': {
    'things': [
      {'rank':1,'name':'Leaning Tower of Pisa','postcode':'56126','distanceKmFromAirport':4,'description':'World-famous 56-metre white marble bell tower that began leaning during construction','distance':1.0,'URL':'https://www.opapisa.it/'},
      {'rank':2,'name':'Piazza dei Miracoli','postcode':'56126','distanceKmFromAirport':4,'description':'UNESCO World Heritage square containing the cathedral, baptistery, tower and camposanto','distance':1.0,'URL':'https://www.opapisa.it/'},
      {'rank':3,'name':'Pisa Cathedral','postcode':'56126','distanceKmFromAirport':4,'description':'Masterpiece of Romanesque architecture housing Galileo\'s lamp and Giovanni Pisano\'s pulpit','distance':1.0,'URL':'https://www.opapisa.it/'},
      {'rank':4,'name':'Baptistery','postcode':'56126','distanceKmFromAirport':4,'description':'Largest baptistery in Italy with remarkable acoustics demonstrated by the guardian','distance':1.0,'URL':'https://www.opapisa.it/'},
      {'rank':5,'name':'Camposanto Monumentale','postcode':'56126','distanceKmFromAirport':4,'description':'Monumental cemetery with ancient sarcophagi and rare medieval frescoes','distance':1.0,'URL':'https://www.opapisa.it/'},
      {'rank':6,'name':'Piazza dei Cavalieri','postcode':'56126','distanceKmFromAirport':3,'description':'Second most important square with Palazzo della Carovana and the Scuola Normale Superiore','distance':0.5,'URL':''},
      {'rank':7,'name':'Lungarni Promenade','postcode':'56125','distanceKmFromAirport':3,'description':'Elegant riverside walkway along the Arno with palaces and the iconic Luminara festival','distance':0.5,'URL':''},
      {'rank':8,'name':'Palazzo Blu','postcode':'56125','distanceKmFromAirport':3,'description':'Blue-facade palace hosting major art exhibitions on the Lungarno','distance':0.5,'URL':'https://www.palazzoblu.it/'},
      {'rank':9,'name':'Museo Nazionale di Pisa','postcode':'56126','distanceKmFromAirport':4,'description':'Major art collection in the Museo Nazionale di San Matteo with medieval Pisan sculpture','distance':1.0,'URL':'https://www.museodipisasanmatteo.it/'},
      {'rank':10,'name':'Certosa di Pisa','postcode':'56011','distanceKmFromAirport':14,'description':'Stunning 14th-century Carthusian monastery with remarkable cloister and Natural History Museum','distance':12.0,'URL':'https://www.certosadipisa.it/'},
    ]
  },
  'podgorica': {
    'things': [
      {'rank':1,'name':'Millennium Bridge','postcode':'81000','distanceKmFromAirport':13,'description':'Distinctive cable-stayed bridge over the Moraca river, symbol of modern Podgorica','distance':1.0,'URL':''},
      {'rank':2,'name':'Ostrog Monastery','postcode':'81400','distanceKmFromAirport':87,'description':'Extraordinary 17th-century monastery built into a sheer cliff face, Montenegro\'s holiest site','distance':75.0,'URL':'https://manastir-ostrog.com/'},
      {'rank':3,'name':'Stara Varos (Old Town)','postcode':'81000','distanceKmFromAirport':13,'description':'Ottoman old town with mosques, hammam ruins and the Sahat-Kula clock tower','distance':1.0,'URL':''},
      {'rank':4,'name':'Cathedral of Christ\'s Resurrection','postcode':'81000','distanceKmFromAirport':13,'description':'Imposing modern Orthodox cathedral completed in 2014 with remarkable frescoes','distance':1.0,'URL':''},
      {'rank':5,'name':'Skadar Lake National Park','postcode':'81305','distanceKmFromAirport':22,'description':'Largest lake in the Balkans, a bird sanctuary with pelicans and medieval monasteries','distance':25.0,'URL':'https://nparkovi.me/destinacije/nacionalni-park-skadarsko-jezero/'},
      {'rank':6,'name':'Moraca River Canyon','postcode':'81400','distanceKmFromAirport':32,'description':'Dramatic gorge downstream from the city with crystal-clear turquoise water','distance':20.0,'URL':''},
      {'rank':7,'name':'Gorica Hill','postcode':'81000','distanceKmFromAirport':14,'description':'Green hill park above the city with forest walks and views over Podgorica','distance':2.0,'URL':''},
      {'rank':8,'name':'Ribnica River Confluence','postcode':'81000','distanceKmFromAirport':13,'description':'Point where Ribnica meets Moraca with the ruins of a medieval Ribnica fortress','distance':1.0,'URL':''},
      {'rank':9,'name':'Duklja Roman Ruins','postcode':'81000','distanceKmFromAirport':17,'description':'Excavated remains of the Roman city of Docleatae on the outskirts of Podgorica','distance':5.0,'URL':''},
      {'rank':10,'name':'Natural History Museum','postcode':'81000','distanceKmFromAirport':13,'description':'Montenegro\'s natural world and geology in a neoclassical building','distance':1.0,'URL':'https://www.pmcg.co.me/'},
    ]
  },
  'pohnpei': {
    'things': [
      {'rank':1,'name':'Nan Madol Ruins','postcode':'96941','distanceKmFromAirport':13,'description':'UNESCO World Heritage megalithic city built on artificial islands - the Venice of the Pacific','distance':10.0,'URL':'https://www.visit-micronesia.fm/'},
      {'rank':2,'name':'Kepirohi Waterfall','postcode':'96941','distanceKmFromAirport':13,'description':'Largest waterfall in Micronesia plunging into a black lava swimming hole','distance':10.0,'URL':''},
      {'rank':3,'name':'Sokehs Ridge Hike','postcode':'96941','distanceKmFromAirport':8,'description':'Volcanic basalt ridge with WWII Japanese gun emplacements and panoramic views','distance':5.0,'URL':''},
      {'rank':4,'name':'Mangrove Kayaking','postcode':'96941','distanceKmFromAirport':8,'description':'Paddle through pristine mangrove forest teeming with black tip reef sharks','distance':5.0,'URL':''},
      {'rank':5,'name':'Pohnpei Surf Break (Palikir Pass)','postcode':'96941','distanceKmFromAirport':11,'description':'World-class left-hand surf break on the outer reef','distance':8.0,'URL':''},
      {'rank':6,'name':'Village of Kolonia','postcode':'96941','distanceKmFromAirport':4,'description':'Former German and Japanese colonial capital with ruins of the old stone wall','distance':1.0,'URL':''},
      {'rank':7,'name':'Liduduhniap Waterfall','postcode':'96941','distanceKmFromAirport':15,'description':'Twin waterfalls accessible by a jungle hike with swimming pools','distance':12.0,'URL':''},
      {'rank':8,'name':'Sakau (Kava) Ceremony','postcode':'96941','distanceKmFromAirport':5,'description':'Traditional Pohnpeian drink made from pepper plant roots - central to social life','distance':2.0,'URL':''},
      {'rank':9,'name':'Pohnpei State Museum','postcode':'96941','distanceKmFromAirport':4,'description':'Cultural artefacts and natural history of the Caroline Islands','distance':1.0,'URL':''},
      {'rank':10,'name':'Fishing in the Pacific','postcode':'96941','distanceKmFromAirport':8,'description':'Deep sea fishing for marlin, wahoo and mahi-mahi in Pohnpei\'s pristine waters','distance':5.0,'URL':''},
    ]
  },
  'port_au_prince': {
    'things': [
      {'rank':1,'name':'Citadelle Laferriere','postcode':'HT1510','distanceKmFromAirport':185,'description':'UNESCO World Heritage Haiti\'s greatest monument - a mountaintop fortress built after independence','distance':175.0,'URL':'https://www.haiticulture.ch/Citadelle.html'},
      {'rank':2,'name':'Sans-Souci Palace','postcode':'HT1510','distanceKmFromAirport':185,'description':'UNESCO World Heritage ruined palace of King Henri Christophe - the Versailles of the Caribbean','distance':175.0,'URL':''},
      {'rank':3,'name':'Musee du Pantheon National Haiti (MUPANAH)','postcode':'HT6112','distanceKmFromAirport':10,'description':'Haiti\'s national museum with the anchor from Columbus\'s Santa Maria','distance':1.0,'URL':'https://mupanah.gouv.ht/'},
      {'rank':4,'name':'Iron Market (Marche en Fer)','postcode':'HT6112','distanceKmFromAirport':10,'description':'Restored 1891 Victorian iron market - Port-au-Prince\'s most iconic landmark','distance':1.0,'URL':''},
      {'rank':5,'name':'Petion-Ville Art Galleries','postcode':'HT6140','distanceKmFromAirport':19,'description':'Haiti\'s extraordinary naif painting tradition - some of the Caribbean\'s finest art','distance':10.0,'URL':''},
      {'rank':6,'name':'Labadee Private Beach (Royal Caribbean)','postcode':'HT1510','distanceKmFromAirport':185,'description':'Beautiful north coast beach leased to Royal Caribbean ships','distance':175.0,'URL':'https://www.royalcaribbean.com/destinations/labadee'},
      {'rank':7,'name':'Holy Trinity Cathedral Murals','postcode':'HT6112','distanceKmFromAirport':10,'description':'Earthquake-damaged cathedral with extraordinary Haitian naif murals in the remaining walls','distance':1.0,'URL':''},
      {'rank':8,'name':'Jacmel Carnival','postcode':'HT8110','distanceKmFromAirport':89,'description':'Haiti\'s most creative carnival with papier-mache masks and traditional rara bands','distance':80.0,'URL':''},
      {'rank':9,'name':'Bassin Bleu Waterfall','postcode':'HT8110','distanceKmFromAirport':94,'description':'Three-tiered swimming holes near Jacmel accessible by horseback','distance':85.0,'URL':''},
      {'rank':10,'name':'Griot Pork with Pikliz','postcode':'HT6112','distanceKmFromAirport':10,'description':'Haiti\'s national dish - fried pork chunks with vinegary pickled vegetable relish','distance':1.0,'URL':''},
    ]
  },
  'port_harcourt': {
    'things': [
      {'rank':1,'name':'Port Harcourt Pleasure Park','postcode':'500001','distanceKmFromAirport':27,'description':'Riverside amusement park with gardens and the largest Ferris wheel in Nigeria','distance':2.0,'URL':''},
      {'rank':2,'name':'Isaac Boro Garden Park','postcode':'500001','distanceKmFromAirport':27,'description':'Botanical garden and recreation area named after the Niger Delta activist','distance':2.0,'URL':''},
      {'rank':3,'name':'Bonny Island Excursion','postcode':'500001','distanceKmFromAirport':70,'description':'Historic slave trade island with colonial-era buildings in the Niger Delta','distance':60.0,'URL':''},
      {'rank':4,'name':'Trans Amadi Area & Oil Industry','postcode':'500001','distanceKmFromAirport':28,'description':'Hub of Nigeria\'s oil industry - driving through the industrial heart of African oil','distance':5.0,'URL':''},
      {'rank':5,'name':'Opobo Town Day Trip','postcode':'524001','distanceKmFromAirport':112,'description':'Historic town founded by King Ja Ja - one of Nigeria\'s greatest trade empire builders','distance':90.0,'URL':''},
      {'rank':6,'name':'Port Harcourt Zoo','postcode':'500001','distanceKmFromAirport':28,'description':'Zoo with West African wildlife including pygmy hippos','distance':3.0,'URL':''},
      {'rank':7,'name':'Rivers State Museum','postcode':'500001','distanceKmFromAirport':27,'description':'Ijaw, Ogoni and Ikwerre culture of the Niger Delta peoples','distance':2.0,'URL':''},
      {'rank':8,'name':'Rumuola & GRA Market','postcode':'500001','distanceKmFromAirport':24,'description':'City markets with fresh Niger Delta produce and street food','distance':5.0,'URL':''},
      {'rank':9,'name':'Live Music at Port Harcourt','postcode':'500001','distanceKmFromAirport':27,'description':'The Niger Delta has a rich music tradition - highlife and Afrobeats bars','distance':2.0,'URL':''},
      {'rank':10,'name':'Bole and Fish','postcode':'500001','distanceKmFromAirport':26,'description':'Port Harcourt\'s definitive street food - grilled plantain with smoked fish and pepper sauce','distance':1.0,'URL':''},
    ]
  },
  'port_louis': {
    'things': [
      {'rank':1,'name':'Le Morne Brabant','postcode':'90425','distanceKmFromAirport':82,'description':'UNESCO World Heritage basalt peninsula - symbol of slave resistance with stunning lagoon','distance':50.0,'URL':'https://www.tourism-mauritius.mu/'},
      {'rank':2,'name':'Aapravasi Ghat','postcode':'11324','distanceKmFromAirport':48,'description':'UNESCO World Heritage immigration depot where 500,000 indentured labourers arrived','distance':0.5,'URL':'https://www.aapravasighat.org/'},
      {'rank':3,'name':'Port Louis Market (Central Market)','postcode':'11314','distanceKmFromAirport':48,'description':'Spice, textile and street food market in an 1886 Victorian iron-frame market hall','distance':0.5,'URL':''},
      {'rank':4,'name':'Caudan Waterfront','postcode':'11307','distanceKmFromAirport':48,'description':'Renovated waterfront with restaurants, the Blue Penny Museum and a casino','distance':0.5,'URL':'https://www.caudan.com/'},
      {'rank':5,'name':'Blue Penny Museum','postcode':'11307','distanceKmFromAirport':48,'description':'Two of the world\'s rarest stamps - the original 1847 \'Post Office\' Mauritius issues','distance':0.5,'URL':'https://www.bluepennymuseum.com/'},
      {'rank':6,'name':'Natural History Museum','postcode':'11302','distanceKmFromAirport':48,'description':'Skeleton of the dodo bird - the extinct flightless bird endemic to Mauritius','distance':0.5,'URL':''},
      {'rank':7,'name':'Pamplemousses Botanical Garden','postcode':'30501','distanceKmFromAirport':55,'description':'One of the oldest botanical gardens in the Southern Hemisphere with giant Victoria water lilies','distance':11.0,'URL':'https://www.npcs.mu/'},
      {'rank':8,'name':'Chamarel Coloured Earths','postcode':'91401','distanceKmFromAirport':98,'description':'Seven-coloured volcanic earth landscape with the highest waterfall on the island','distance':55.0,'URL':'https://www.chamarelcolouredearths.com/'},
      {'rank':9,'name':'Dolphin Watching at Tamarin Bay','postcode':'90521','distanceKmFromAirport':80,'description':'Swim with wild spinner dolphins in the warm turquoise waters off the west coast','distance':40.0,'URL':''},
      {'rank':10,'name':'Dholl Puri','postcode':'11314','distanceKmFromAirport':49,'description':'Mauritius\'s most popular street food - split pea flatbread with rougaille sauce','distance':1.0,'URL':''},
    ]
  },
  'port_moresby': {
    'things': [
      {'rank':1,'name':'National Museum & Art Gallery','postcode':'121','distanceKmFromAirport':11,'description':'Masks, ceremonial objects and artefacts from Papua New Guinea\'s 800+ tribes','distance':2.0,'URL':'https://www.nmag.gov.pg/'},
      {'rank':2,'name':'Kokoda Track (Historical Trail)','postcode':'122','distanceKmFromAirport':69,'description':'WWII jungle track 96km over the Owen Stanley Ranges - one of history\'s greatest battles','distance':60.0,'URL':'https://www.kokodatrackauthority.org/'},
      {'rank':3,'name':'Parliament House','postcode':'121','distanceKmFromAirport':12,'description':'Spectacular 1984 building combining traditional Sepik haus tambaran with modern architecture','distance':3.0,'URL':'https://www.parliament.gov.pg/'},
      {'rank':4,'name':'Port Moresby Nature Park','postcode':'121','distanceKmFromAirport':14,'description':'Tree kangaroos, birds of paradise and cassowaries in a natural conservation park','distance':5.0,'URL':'https://www.pmnaturepark.org/'},
      {'rank':5,'name':'Bird of Paradise Watching','postcode':'122','distanceKmFromAirport':49,'description':'PNG has 38 of the world\'s 42 bird of paradise species - the most spectacular birds on Earth','distance':40.0,'URL':'https://www.pngtourism.org.pg/'},
      {'rank':6,'name':'Ela Beach','postcode':'121','distanceKmFromAirport':10,'description':'Popular city beach with the Ela Beach Hotel and afternoon market','distance':1.0,'URL':''},
      {'rank':7,'name':'Bomana War Cemetery','postcode':'124','distanceKmFromAirport':14,'description':'Commonwealth War Graves for the 3,824 Allied soldiers who fell defending Port Moresby','distance':20.0,'URL':'https://www.cwgc.org/'},
      {'rank':8,'name':'Varirata National Park','postcode':'121','distanceKmFromAirport':49,'description':'Rainforest 40km from the city with birds of paradise and magnificent coastal views','distance':40.0,'URL':'https://www.cepa.gov.pg/'},
      {'rank':9,'name':'Goroka Show Day Trip','postcode':'441','distanceKmFromAirport':439,'description':'Highlands tribal gathering with 100+ tribes in traditional sing-sing dress','distance':430.0,'URL':'https://www.gorokashow.com/'},
      {'rank':10,'name':'Betel Nut (Buai) Market Experience','postcode':'121','distanceKmFromAirport':10,'description':'Papua New Guinea\'s favourite chew - the red-staining nut sold everywhere','distance':1.0,'URL':''},
    ]
  },
}

field_order = ['rank', 'name', 'postcode', 'distanceKmFromAirport', 'description', 'distance', 'URL']

for city_key, city_data in data.items():
    filepath = os.path.join(base, city_key + '.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        original = json.load(f)

    lookup = {t['name']: t for t in city_data['things']}

    new_things = []
    for thing in original['things']:
        name = thing['name']
        if name in lookup:
            new_t = lookup[name]
            ordered = {k: new_t[k] for k in field_order}
        else:
            ordered = thing
        new_things.append(ordered)

    original['things'] = new_things

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(original, f, indent=2, ensure_ascii=False)

    print(f'Updated {city_key}.json')

print('Done.')
