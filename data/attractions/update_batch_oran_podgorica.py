import json
import os

attractions_data = {
    "oran": [
        {"rank": 1, "name": "Santa Cruz Fort & Chapel", "postcode": "31000", "distanceKmFromAirport": 29, "description": "Spanish fortress on Murdjadjo Mountain overlooking the city and bay", "distance": 3.0, "URL": ""},
        {"rank": 2, "name": "Bey's Palace (Regency Palace)", "postcode": "31000", "distanceKmFromAirport": 27, "description": "18th-century Ottoman-Andalusian palace with the best example of Moorish tilework in Algeria", "distance": 1.0, "URL": ""},
        {"rank": 3, "name": "City Hall (Mairie d'Oran)", "postcode": "31000", "distanceKmFromAirport": 27, "description": "Magnificent French colonial town hall from 1886", "distance": 0.5, "URL": ""},
        {"rank": 4, "name": "Musee National Ahmed Zabana", "postcode": "31000", "distanceKmFromAirport": 28, "description": "Oran's main museum with prehistoric rock art and colonial history", "distance": 2.0, "URL": ""},
        {"rank": 5, "name": "Place du 1er Novembre (Place Joffre)", "postcode": "31000", "distanceKmFromAirport": 27, "description": "Grand French colonial square with the Palais des Rais and Oran Cathedral", "distance": 0.5, "URL": ""},
        {"rank": 6, "name": "Port of Oran", "postcode": "31000", "distanceKmFromAirport": 28, "description": "Historic Mediterranean port that inspired Albert Camus's novel The Plague", "distance": 2.0, "URL": ""},
        {"rank": 7, "name": "Oran Cathedral (Sacred Heart)", "postcode": "31000", "distanceKmFromAirport": 27, "description": "Neoclassical French colonial cathedral - now a public library", "distance": 1.0, "URL": ""},
        {"rank": 8, "name": "Tlemcen Day Trip", "postcode": "13000", "distanceKmFromAirport": 155, "description": "The pearl of the Maghreb - UNESCO-listed medina with Almoravid and Merinid ruins", "distance": 140.0, "URL": "https://whc.unesco.org/en/list/153"},
        {"rank": 9, "name": "Plage des Andalouses", "postcode": "31340", "distanceKmFromAirport": 30, "description": "Oran's most popular Mediterranean beach", "distance": 15.0, "URL": ""},
        {"rank": 10, "name": "Rai Music Bars", "postcode": "31000", "distanceKmFromAirport": 27, "description": "Oran is the home of Rai - North African pop fusion now popular worldwide", "distance": 1.0, "URL": ""},
    ],
    "ouagadougou": [
        {"rank": 1, "name": "FESPACO African Film Festival", "postcode": "12000", "distanceKmFromAirport": 6, "description": "Africa's largest cinema festival held every two years in February", "distance": 3.0, "URL": "https://www.fespaco.bf/"},
        {"rank": 2, "name": "National Museum of Burkina Faso", "postcode": "12000", "distanceKmFromAirport": 5, "description": "Traditional masks, bronze castings and daily life objects of the Mossi and Lobi", "distance": 2.0, "URL": ""},
        {"rank": 3, "name": "Central Market (Grand Marche)", "postcode": "12000", "distanceKmFromAirport": 4, "description": "Ouaga's main market with Burkinabe woven fabric, leather goods and food", "distance": 1.0, "URL": ""},
        {"rank": 4, "name": "Mossi Royal Court", "postcode": "12000", "distanceKmFromAirport": 5, "description": "Audience with the Mogho Naaba - the Mossi Emperor who still holds traditional power", "distance": 2.0, "URL": ""},
        {"rank": 5, "name": "Maison du Peuple Cultural Centre", "postcode": "12000", "distanceKmFromAirport": 4, "description": "Government arts centre hosting concerts and exhibitions", "distance": 1.0, "URL": ""},
        {"rank": 6, "name": "Village Artisanal de Ouagadougou", "postcode": "12000", "distanceKmFromAirport": 6, "description": "Bronze casting, leatherwork and weaving workshops in a craft village", "distance": 3.0, "URL": ""},
        {"rank": 7, "name": "Laongo Sculpture Symposium", "postcode": "11000", "distanceKmFromAirport": 38, "description": "Outdoor granite sculpture park 35km from the city", "distance": 35.0, "URL": ""},
        {"rank": 8, "name": "Bangr-Weogo Urban Nature Reserve", "postcode": "12000", "distanceKmFromAirport": 8, "description": "Urban nature park with gazelles and a botanical garden", "distance": 5.0, "URL": ""},
        {"rank": 9, "name": "Temple of Enlightenment", "postcode": "12000", "distanceKmFromAirport": 8, "description": "Syncretic temple built by a visionary with local stone and recycled materials", "distance": 5.0, "URL": ""},
        {"rank": 10, "name": "Riz Gras (Fat Rice)", "postcode": "12000", "distanceKmFromAirport": 4, "description": "Burkina Faso's most popular dish - rice cooked in meat stock with vegetables", "distance": 1.0, "URL": ""},
    ],
    "palermo": [
        {"rank": 1, "name": "Capuchin Catacombs", "postcode": "90129", "distanceKmFromAirport": 32, "description": "Macabre corridors with 8,000 mummified monks and citizens in poses of life", "distance": 3.0, "URL": "https://www.catacombepalermo.it/"},
        {"rank": 2, "name": "Palazzo dei Normanni", "postcode": "90134", "distanceKmFromAirport": 31, "description": "Norman Palace housing the dazzling Palatine Chapel, a UNESCO World Heritage site", "distance": 1.0, "URL": "https://www.federicosecondo.org/"},
        {"rank": 3, "name": "Ballarò Market", "postcode": "90134", "distanceKmFromAirport": 31, "description": "Palermo's oldest and most vibrant street market, the beating heart of the city", "distance": 1.0, "URL": ""},
        {"rank": 4, "name": "Quattro Canti", "postcode": "90133", "distanceKmFromAirport": 31, "description": "Baroque octagonal piazza where the four historic districts of the city intersect", "distance": 0.5, "URL": ""},
        {"rank": 5, "name": "Palermo Cathedral", "postcode": "90134", "distanceKmFromAirport": 31, "description": "Arab-Norman UNESCO masterpiece with royal tombs including Emperor Frederick II", "distance": 1.0, "URL": "https://www.cattedrale.palermo.it/"},
        {"rank": 6, "name": "La Martorana Church", "postcode": "90133", "distanceKmFromAirport": 31, "description": "12th-century Byzantine church with original golden mosaics", "distance": 0.5, "URL": ""},
        {"rank": 7, "name": "Teatro Massimo", "postcode": "90138", "distanceKmFromAirport": 31, "description": "Italy's largest opera house, used for the baptism scene in The Godfather Part III", "distance": 1.0, "URL": "https://www.teatromassimo.it/"},
        {"rank": 8, "name": "Mondello Beach", "postcode": "90151", "distanceKmFromAirport": 40, "description": "Palermo's favourite beach resort with a picturesque Liberty-style bathing establishment", "distance": 11.0, "URL": ""},
        {"rank": 9, "name": "Orto Botanico", "postcode": "90123", "distanceKmFromAirport": 32, "description": "18th-century botanical garden with rare plants from around the Mediterranean", "distance": 2.0, "URL": "https://www.ortobotanico.unipa.it/"},
        {"rank": 10, "name": "Cefalù", "postcode": "90015", "distanceKmFromAirport": 70, "description": "Stunning medieval town with Norman cathedral and beaches just 70km from Palermo", "distance": 70.0, "URL": "https://www.cefaluweb.com/"},
    ],
    "palma": [
        {"rank": 1, "name": "Palma Cathedral (La Seu)", "postcode": "07001", "distanceKmFromAirport": 9, "description": "Dramatic Gothic cathedral rising above the sea with Gaudi's interior modifications", "distance": 1.0, "URL": "https://catedraldemallorca.org/"},
        {"rank": 2, "name": "Bellver Castle", "postcode": "07015", "distanceKmFromAirport": 10, "description": "Unique circular 14th-century Gothic castle on a hill with panoramic bay views", "distance": 3.0, "URL": "https://www.palma.cat/portal/PALMA/"},
        {"rank": 3, "name": "Old Town Palma", "postcode": "07001", "distanceKmFromAirport": 9, "description": "Winding medieval streets with Arab baths, Renaissance palaces and tapas bars", "distance": 0.5, "URL": "https://visitpalma.cat/"},
        {"rank": 4, "name": "Es Baluard Museum", "postcode": "07001", "distanceKmFromAirport": 9, "description": "Contemporary art museum in a 16th-century bastion with sea views", "distance": 1.0, "URL": "https://www.esbaluard.org/"},
        {"rank": 5, "name": "Arab Baths", "postcode": "07001", "distanceKmFromAirport": 9, "description": "Remarkably preserved 10th-century Moorish hammam in the old town", "distance": 1.0, "URL": "https://www.banysdel.com/"},
        {"rank": 6, "name": "Fundacio Pilar i Joan Miro", "postcode": "07015", "distanceKmFromAirport": 11, "description": "Joan Miro's studio complex preserved as it was when he died, surrounded by his work", "distance": 4.0, "URL": "https://www.miromallorca.com/"},
        {"rank": 7, "name": "Passeig des Born", "postcode": "07012", "distanceKmFromAirport": 9, "description": "Elegant tree-lined promenade with 16th-century fountain and Art Nouveau mansions", "distance": 0.5, "URL": ""},
        {"rank": 8, "name": "Parc de la Mar", "postcode": "07001", "distanceKmFromAirport": 9, "description": "Waterfront park with an artificial lake reflecting the cathedral facade", "distance": 1.0, "URL": ""},
        {"rank": 9, "name": "Palma Aquarium", "postcode": "07609", "distanceKmFromAirport": 3, "description": "Impressive aquarium with Mediterranean and tropical ecosystems", "distance": 9.0, "URL": "https://www.palmaaquarium.com/"},
        {"rank": 10, "name": "Mallorcan Villages", "postcode": "07170", "distanceKmFromAirport": 25, "description": "Day trips to Soller, Deia, Valldemossa and Sineu's famous Wednesday market", "distance": 20.0, "URL": "https://www.infomallorca.net/"},
    ],
    "panama_city": [
        {"rank": 1, "name": "Panama Canal (Miraflores Locks)", "postcode": "0816", "distanceKmFromAirport": 50, "description": "Watch container ships pass through one of the world's greatest engineering achievements", "distance": 15.0, "URL": "https://micanaldepanama.com/"},
        {"rank": 2, "name": "Casco Viejo (Old Quarter)", "postcode": "0843", "distanceKmFromAirport": 37, "description": "UNESCO World Heritage Spanish colonial quarter with French and American architecture", "distance": 2.0, "URL": "https://www.cascoviejo.org/"},
        {"rank": 3, "name": "San Blas Islands (Guna Yala)", "postcode": "0000", "distanceKmFromAirport": 80, "description": "370 palm-fringed islands governed by the Guna indigenous people with perfect beaches", "distance": 100.0, "URL": "https://www.gunayala.gob.pa/"},
        {"rank": 4, "name": "Metropolitan Natural Park", "postcode": "0816", "distanceKmFromAirport": 40, "description": "Tropical forest within the city limits with sloths, toucans and anteaters", "distance": 5.0, "URL": "https://www.parquemetropolitano.org/"},
        {"rank": 5, "name": "Biomuseo", "postcode": "0843", "distanceKmFromAirport": 42, "description": "Frank Gehry-designed museum on the continental divide and Panama's biodiversity", "distance": 7.0, "URL": "https://www.biomuseopanama.org/"},
        {"rank": 6, "name": "Panama Viejo Archaeological Site", "postcode": "0801", "distanceKmFromAirport": 30, "description": "Ruins of the first European city on the Pacific, razed by pirate Henry Morgan in 1671", "distance": 5.0, "URL": "https://www.panamaviejo.org/"},
        {"rank": 7, "name": "Amador Causeway", "postcode": "0843", "distanceKmFromAirport": 43, "description": "3km causeway of islands connected to the city with restaurants and the new Biomuseo", "distance": 8.0, "URL": "https://www.calzadadeamador.com/"},
        {"rank": 8, "name": "Gamboa Rainforest & Monkey Island", "postcode": "0816", "distanceKmFromAirport": 55, "description": "Boat trip on Gatun Lake to Monkey Island teeming with howler, capuchin and spider monkeys", "distance": 28.0, "URL": "https://www.gamboaresort.com/"},
        {"rank": 9, "name": "Miraflores Visitors Centre", "postcode": "0816", "distanceKmFromAirport": 50, "description": "Best view of the Canal locks with a museum and 3D IMAX film", "distance": 15.0, "URL": "https://micanaldepanama.com/"},
        {"rank": 10, "name": "Mercado de Mariscos (Fish Market)", "postcode": "0843", "distanceKmFromAirport": 36, "description": "Ceviche and fresh seafood directly from the Pacific at the historic fish market", "distance": 1.0, "URL": ""},
    ],
    "paramaribo": [
        {"rank": 1, "name": "Historic Inner City (Paramaribo Old Town)", "postcode": "0000", "distanceKmFromAirport": 46, "description": "UNESCO World Heritage Dutch colonial city with a unique Caribbean wooden architecture", "distance": 0.5, "URL": "https://www.surinametourism.sr/"},
        {"rank": 2, "name": "Saint Peter and Paul Cathedral", "postcode": "0000", "distanceKmFromAirport": 46, "description": "One of the largest wooden structures in the Western Hemisphere built by Dutch Redemptorists", "distance": 0.5, "URL": ""},
        {"rank": 3, "name": "Central Market (Centrale Markt)", "postcode": "0000", "distanceKmFromAirport": 46, "description": "Multi-ethnic market reflecting Suriname's extraordinary diversity - Creole, Javanese, Chinese", "distance": 0.5, "URL": ""},
        {"rank": 4, "name": "Joden Savanne Jewish Cemetery", "postcode": "0000", "distanceKmFromAirport": 95, "description": "Ruins of the oldest synagogue in the Western Hemisphere built by Sephardic Jews in 1671", "distance": 50.0, "URL": ""},
        {"rank": 5, "name": "Fort Zeelandia Museum", "postcode": "0000", "distanceKmFromAirport": 46, "description": "17th-century Dutch fort on the Suriname River now housing historical collections", "distance": 0.5, "URL": "https://www.surinamemuseum.sr/"},
        {"rank": 6, "name": "Brownsberg Nature Park", "postcode": "0000", "distanceKmFromAirport": 165, "description": "Rainforest park above the Brokopondo reservoir with howler monkeys and toucans", "distance": 120.0, "URL": "https://www.stinasu.sr/"},
        {"rank": 7, "name": "Neveh Shalom Synagogue", "postcode": "0000", "distanceKmFromAirport": 46, "description": "Active 1834 synagogue with a sand floor - oldest in continuous use in the Americas", "distance": 0.5, "URL": ""},
        {"rank": 8, "name": "Commewijne District Plantation Cruise", "postcode": "0000", "distanceKmFromAirport": 55, "description": "River boat to former Dutch coffee and sugar plantations with dolphins", "distance": 10.0, "URL": ""},
        {"rank": 9, "name": "Central Suriname Nature Reserve", "postcode": "0000", "distanceKmFromAirport": 245, "description": "UNESCO World Heritage 1.6 million hectares of pristine Amazon rainforest", "distance": 200.0, "URL": ""},
        {"rank": 10, "name": "Pom Cassava & Chicken Dish", "postcode": "0000", "distanceKmFromAirport": 45, "description": "Suriname's national dish - pomtajer root with chicken, lemon and spices", "distance": 1.0, "URL": ""},
    ],
    "paro": [
        {"rank": 1, "name": "Taktsang Monastery (Tiger's Nest)", "postcode": "12001", "distanceKmFromAirport": 16, "description": "Bhutan's most iconic image - a monastery clinging to a 900m cliff above Paro Valley", "distance": 10.0, "URL": "https://www.tourism.gov.bt/"},
        {"rank": 2, "name": "Rinpung Dzong", "postcode": "12001", "distanceKmFromAirport": 9, "description": "16th-century fortified monastery housing the monk body and district administration", "distance": 0.5, "URL": "https://www.tourism.gov.bt/"},
        {"rank": 3, "name": "National Museum of Bhutan", "postcode": "12001", "distanceKmFromAirport": 9, "description": "Inside the 17th-century Ta Dzong watchtower with Bhutan's finest cultural collection", "distance": 1.0, "URL": "https://www.nationalmuseumbhutan.gov.bt/"},
        {"rank": 4, "name": "Kyichu Lhakhang", "postcode": "12001", "distanceKmFromAirport": 9, "description": "7th-century temple built by King Songtsen Gampo - one of the oldest in Bhutan", "distance": 3.0, "URL": "https://www.tourism.gov.bt/"},
        {"rank": 5, "name": "Paro Valley Walk", "postcode": "12001", "distanceKmFromAirport": 10, "description": "Walk through rice fields, apple orchards and traditional farmhouses in the valley", "distance": 2.0, "URL": "https://www.tourism.gov.bt/"},
        {"rank": 6, "name": "Dochula Pass & 108 Memorial Chortens", "postcode": "11001", "distanceKmFromAirport": 55, "description": "Mountain pass at 3,100m with 108 chortens and Himalayan panorama to Tibet", "distance": 50.0, "URL": "https://www.tourism.gov.bt/"},
        {"rank": 7, "name": "Punakha Dzong", "postcode": "13001", "distanceKmFromAirport": 80, "description": "17th-century dzong at the confluence of two rivers - Bhutan's most beautiful", "distance": 75.0, "URL": "https://www.tourism.gov.bt/"},
        {"rank": 8, "name": "Thimphu Tashichho Dzong", "postcode": "11001", "distanceKmFromAirport": 62, "description": "Bhutan's 13th century capital fortress monastery and seat of the government", "distance": 55.0, "URL": "https://www.tourism.gov.bt/"},
        {"rank": 9, "name": "Bhutan International Festival (Tsechu)", "postcode": "12001", "distanceKmFromAirport": 8, "description": "Ancient tantric mask dances performed by monks - dates vary by monastery", "distance": 0.5, "URL": "https://www.tourism.gov.bt/"},
        {"rank": 10, "name": "Ema Datshi (Chilli Cheese)", "postcode": "12001", "distanceKmFromAirport": 8, "description": "Bhutan's national dish - whole red and green chillies cooked in fresh yak cheese sauce", "distance": 1.0, "URL": ""},
    ],
    "phnom_penh": [
        {"rank": 1, "name": "Royal Palace & Silver Pagoda", "postcode": "12301", "distanceKmFromAirport": 11, "description": "The royal residence with the Silver Pagoda housing a life-sized gold Buddha encrusted with diamonds", "distance": 1.0, "URL": "https://www.royalpalace.gov.kh/"},
        {"rank": 2, "name": "Tuol Sleng Genocide Museum (S-21)", "postcode": "12304", "distanceKmFromAirport": 12, "description": "Former Khmer Rouge prison where 17,000 were tortured - essential and harrowing history", "distance": 2.0, "URL": "https://tuolsleng.gov.kh/"},
        {"rank": 3, "name": "Choeung Ek Killing Fields", "postcode": "12101", "distanceKmFromAirport": 25, "description": "Memorial to the 17,000 victims executed here during the Khmer Rouge genocide", "distance": 15.0, "URL": "https://www.killingfieldsmuseum.com/"},
        {"rank": 4, "name": "National Museum of Cambodia", "postcode": "12202", "distanceKmFromAirport": 11, "description": "World's finest collection of Khmer art with sculptures from Angkor Wat", "distance": 1.0, "URL": "https://www.cambodiamuseum.info/"},
        {"rank": 5, "name": "Riverside Promenade (Sisowath Quay)", "postcode": "12201", "distanceKmFromAirport": 10, "description": "Sunset drinks on the promenade where the Mekong and Tonle Sap rivers merge", "distance": 0.5, "URL": ""},
        {"rank": 6, "name": "Central Market (Phsar Thmei)", "postcode": "12210", "distanceKmFromAirport": 11, "description": "1930s Art Deco market with a distinctive yellow dome selling gold, gems and souvenirs", "distance": 1.0, "URL": ""},
        {"rank": 7, "name": "Russian Market (Phsar Toul Tom Poung)", "postcode": "12303", "distanceKmFromAirport": 13, "description": "Best local market for handicrafts, silk, Buddha statues and cheap street food", "distance": 2.5, "URL": ""},
        {"rank": 8, "name": "Wat Phnom", "postcode": "12202", "distanceKmFromAirport": 11, "description": "Hill temple that gave the city its name, with a reclining Buddha and resident monkeys", "distance": 1.0, "URL": ""},
        {"rank": 9, "name": "Cambodian Living Arts Performance", "postcode": "12202", "distanceKmFromAirport": 11, "description": "Traditional apsara dance and classical Khmer music performed by genocide survivors", "distance": 1.0, "URL": "https://www.cambodianlivingarts.org/"},
        {"rank": 10, "name": "Mekong River Sunset Cruise", "postcode": "12201", "distanceKmFromAirport": 10, "description": "Sunset boat cruise on the great river with Angkor beer and views of the Royal Palace", "distance": 0.5, "URL": ""},
    ],
    "pisa": [
        {"rank": 1, "name": "Leaning Tower of Pisa", "postcode": "56126", "distanceKmFromAirport": 4, "description": "World-famous 56-metre white marble bell tower that began leaning during construction", "distance": 1.0, "URL": "https://www.opapisa.it/"},
        {"rank": 2, "name": "Piazza dei Miracoli", "postcode": "56126", "distanceKmFromAirport": 4, "description": "UNESCO World Heritage square containing the cathedral, baptistery, tower and camposanto", "distance": 1.0, "URL": "https://www.opapisa.it/"},
        {"rank": 3, "name": "Pisa Cathedral", "postcode": "56126", "distanceKmFromAirport": 4, "description": "Masterpiece of Romanesque architecture housing Galileo's lamp and Giovanni Pisano's pulpit", "distance": 1.0, "URL": "https://www.opapisa.it/"},
        {"rank": 4, "name": "Baptistery", "postcode": "56126", "distanceKmFromAirport": 4, "description": "Largest baptistery in Italy with remarkable acoustics demonstrated by the guardian", "distance": 1.0, "URL": "https://www.opapisa.it/"},
        {"rank": 5, "name": "Camposanto Monumentale", "postcode": "56126", "distanceKmFromAirport": 4, "description": "Monumental cemetery with ancient sarcophagi and rare medieval frescoes", "distance": 1.0, "URL": "https://www.opapisa.it/"},
        {"rank": 6, "name": "Piazza dei Cavalieri", "postcode": "56126", "distanceKmFromAirport": 3, "description": "Second most important square with Palazzo della Carovana and the Scuola Normale Superiore", "distance": 0.5, "URL": ""},
        {"rank": 7, "name": "Lungarni Promenade", "postcode": "56125", "distanceKmFromAirport": 3, "description": "Elegant riverside walkway along the Arno with palaces and the iconic Luminara festival", "distance": 0.5, "URL": ""},
        {"rank": 8, "name": "Palazzo Blu", "postcode": "56125", "distanceKmFromAirport": 3, "description": "Blue-facade palace hosting major art exhibitions on the Lungarno", "distance": 0.5, "URL": "https://www.palazzoblu.it/"},
        {"rank": 9, "name": "Museo Nazionale di Pisa", "postcode": "56126", "distanceKmFromAirport": 4, "description": "Major art collection in the Museo Nazionale di San Matteo with medieval Pisan sculpture", "distance": 1.0, "URL": "https://www.museodipisasanmatteo.it/"},
        {"rank": 10, "name": "Certosa di Pisa", "postcode": "56011", "distanceKmFromAirport": 14, "description": "Stunning 14th-century Carthusian monastery with remarkable cloister and Natural History Museum", "distance": 12.0, "URL": "https://www.certosadipisa.it/"},
    ],
    "podgorica": [
        {"rank": 1, "name": "Millennium Bridge", "postcode": "81000", "distanceKmFromAirport": 13, "description": "Distinctive cable-stayed bridge over the Moraca river, symbol of modern Podgorica", "distance": 1.0, "URL": ""},
        {"rank": 2, "name": "Ostrog Monastery", "postcode": "81400", "distanceKmFromAirport": 87, "description": "Extraordinary 17th-century monastery built into a sheer cliff face, Montenegro's holiest site", "distance": 75.0, "URL": "https://manastir-ostrog.com/"},
        {"rank": 3, "name": "Stara Varos (Old Town)", "postcode": "81000", "distanceKmFromAirport": 13, "description": "Ottoman old town with mosques, hammam ruins and the Sahat-Kula clock tower", "distance": 1.0, "URL": ""},
        {"rank": 4, "name": "Cathedral of Christ's Resurrection", "postcode": "81000", "distanceKmFromAirport": 13, "description": "Imposing modern Orthodox cathedral completed in 2014 with remarkable frescoes", "distance": 1.0, "URL": ""},
        {"rank": 5, "name": "Skadar Lake National Park", "postcode": "81305", "distanceKmFromAirport": 22, "description": "Largest lake in the Balkans, a bird sanctuary with pelicans and medieval monasteries", "distance": 25.0, "URL": "https://nparkovi.me/destinacije/nacionalni-park-skadarsko-jezero/"},
        {"rank": 6, "name": "Moraca River Canyon", "postcode": "81400", "distanceKmFromAirport": 32, "description": "Dramatic gorge downstream from the city with crystal-clear turquoise water", "distance": 20.0, "URL": ""},
        {"rank": 7, "name": "Gorica Hill", "postcode": "81000", "distanceKmFromAirport": 14, "description": "Green hill park above the city with forest walks and views over Podgorica", "distance": 2.0, "URL": ""},
        {"rank": 8, "name": "Ribnica River Confluence", "postcode": "81000", "distanceKmFromAirport": 13, "description": "Point where Ribnica meets Moraca with the ruins of a medieval Ribnica fortress", "distance": 1.0, "URL": ""},
        {"rank": 9, "name": "Duklja Roman Ruins", "postcode": "81000", "distanceKmFromAirport": 17, "description": "Excavated remains of the Roman city of Docleatae on the outskirts of Podgorica", "distance": 5.0, "URL": ""},
        {"rank": 10, "name": "Natural History Museum", "postcode": "81000", "distanceKmFromAirport": 13, "description": "Montenegro's natural world and geology in a neoclassical building", "distance": 1.0, "URL": "https://www.pmcg.co.me/"},
    ],
}

base_path = r"c:\Users\junkp\MagicMirror\modules\MMM-iAmGoingThere\data\attractions"

for city, attractions in attractions_data.items():
    file_path = os.path.join(base_path, f"{city}.json")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data['things'] = attractions
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Updated {city}.json")

print("\nAll files have been successfully updated!")
