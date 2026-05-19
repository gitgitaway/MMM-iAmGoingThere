#!/usr/bin/env python3
import json
from pathlib import Path

data = {
    "nadi": {
        "city": "Nadi",
        "country": "Fiji",
        "airportPostcode": "685",
        "airportDistanceKm": 2,
        "things": [
            {"rank": 1, "name": "Mamanuca Islands", "postcode": "685", "distanceKmFromAirport": 22, "description": "Picture-perfect island archipelago off Nadi with white sand, coral reefs and resorts", "distance": 20.0, "URL": "https://www.fiji.travel/place/mamanuca-islands"},
            {"rank": 2, "name": "Sri Siva Subramaniya Temple", "postcode": "680", "distanceKmFromAirport": 3, "description": "South Pacific's largest Hindu temple with vivid Dravidian-style painted gopuram", "distance": 0.5, "URL": "https://www.srisiva.org/"},
            {"rank": 3, "name": "Garden of the Sleeping Giant", "postcode": "680", "distanceKmFromAirport": 7, "description": "Orchid gardens established by Raymond Burr with hundreds of exotic orchid varieties", "distance": 5.0, "URL": "https://www.gardensleepinggiant.com/"},
            {"rank": 4, "name": "Yasawa Islands", "postcode": "679", "distanceKmFromAirport": 122, "description": "Remote volcanic island chain with crystal water, caves and the Blue Lagoon", "distance": 120.0, "URL": "https://www.fiji.travel/place/yasawa-islands"},
            {"rank": 5, "name": "Nadi Municipal Market", "postcode": "680", "distanceKmFromAirport": 3, "description": "Colourful local market with tropical fruits, kava root, spices and Fijian produce", "distance": 0.5, "URL": ""},
            {"rank": 6, "name": "Sawa-i-Lau Limestone Caves", "postcode": "679", "distanceKmFromAirport": 162, "description": "Sacred limestone sea caves in the Yasawas with an inner swimming chamber", "distance": 160.0, "URL": "https://www.fiji.travel/place/sawa-i-lau-caves"},
            {"rank": 7, "name": "Zip Fiji Canopy Tour", "postcode": "680", "distanceKmFromAirport": 10, "description": "Ziplining through tropical rainforest in the Sabeto Mountains above Nadi", "distance": 8.0, "URL": "https://www.zipfiji.com/"},
            {"rank": 8, "name": "Sabeto Hot Springs & Mud Pool", "postcode": "680", "distanceKmFromAirport": 11, "description": "Natural volcanic mud pools and hot spring pools at the foot of the Sabeto Mountains", "distance": 9.0, "URL": "https://www.sabetohotsprings.com/"},
            {"rank": 9, "name": "Port Denarau Marina", "postcode": "675", "distanceKmFromAirport": 7, "description": "Hub for island cruises, sunset sails and ferries to the Mamanuca and Yasawa islands", "distance": 5.0, "URL": "https://www.portdenarau.com.fj/"},
            {"rank": 10, "name": "Sigatoka Sand Dunes National Park", "postcode": "670", "distanceKmFromAirport": 62, "description": "Fiji's first national park with 60m Pacific sand dunes and archaeological finds", "distance": 60.0, "URL": "https://fijiparks.org.fj/"},
        ]
    },
    "nanjing": {
        "city": "Nanjing",
        "country": "China",
        "airportPostcode": "211131",
        "airportDistanceKm": 37,
        "things": [
            {"rank": 1, "name": "Sun Yat-sen Mausoleum", "postcode": "210014", "distanceKmFromAirport": 42, "description": "Imposing hilltop mausoleum of the Father of Modern China with 392-step climb", "distance": 5.0, "URL": "http://www.zschina.org.cn/"},
            {"rank": 2, "name": "Nanjing Massacre Memorial", "postcode": "210007", "distanceKmFromAirport": 41, "description": "Sobering memorial to the 300,000 killed by Japanese troops in December 1937", "distance": 4.0, "URL": "https://www.nj1937.org/"},
            {"rank": 3, "name": "Ming Xiaoling Mausoleum", "postcode": "210014", "distanceKmFromAirport": 43, "description": "UNESCO World Heritage tomb of the first Ming Emperor in a magnificent sacred way", "distance": 6.0, "URL": "https://www.mingling.org.cn/"},
            {"rank": 4, "name": "Confucius Temple (Fuzimiao)", "postcode": "210001", "distanceKmFromAirport": 39, "description": "Qinhuai River waterfront with a lively night market of Nanjing's famous snacks", "distance": 2.0, "URL": "https://www.njfzmq.com/"},
            {"rank": 5, "name": "City Wall", "postcode": "210001", "distanceKmFromAirport": 38, "description": "Best-preserved city wall in China at 35km - cycle the top with mountain views", "distance": 1.0, "URL": "https://www.njcitywall.com/"},
            {"rank": 6, "name": "Presidential Palace (Zongtongfu)", "postcode": "210018", "distanceKmFromAirport": 39, "description": "Former seat of the Chinese republican government with extensive museum", "distance": 2.0, "URL": "https://www.njztf.cn/"},
            {"rank": 7, "name": "Purple Mountain Scenic Area", "postcode": "210014", "distanceKmFromAirport": 42, "description": "Cable car to Zijin Mountain with ancient tombs, temples and walking trails", "distance": 5.0, "URL": "https://www.zijinshan.org/"},
            {"rank": 8, "name": "Zhongshan Botanical Garden", "postcode": "210014", "distanceKmFromAirport": 43, "description": "China's most comprehensive botanical garden on the slopes of Purple Mountain", "distance": 6.0, "URL": "https://www.cnbg.net/"},
            {"rank": 9, "name": "Nanjing Museum", "postcode": "210014", "distanceKmFromAirport": 41, "description": "China's second largest museum with imperial bronzes and porcelain", "distance": 4.0, "URL": "https://www.njmuseum.com/"},
            {"rank": 10, "name": "Nanjing Salted Duck (Yan Shui Ya)", "postcode": "210001", "distanceKmFromAirport": 38, "description": "Nanjing's most famous dish - osmanthus-cured salted duck with aromatic spices", "distance": 1.0, "URL": ""},
        ]
    },
    "nha_trang": {
        "city": "Nha Trang",
        "country": "Vietnam",
        "airportPostcode": "650000",
        "airportDistanceKm": 35,
        "things": [
            {"rank": 1, "name": "Po Nagar Cham Towers", "postcode": "650000", "distanceKmFromAirport": 33, "description": "8th-century Cham Hindu temple towers on a hilltop above the mouth of the Cai River", "distance": 2.0, "URL": "https://ponagar.vn/"},
            {"rank": 2, "name": "Nha Trang Bay Island Hopping", "postcode": "650000", "distanceKmFromAirport": 40, "description": "Boat trip to offshore islands with snorkelling, beach time and seafood lunch", "distance": 5.0, "URL": ""},
            {"rank": 3, "name": "Nha Trang Beach", "postcode": "650000", "distanceKmFromAirport": 36, "description": "6km white-sand beach curving around the bay with a vibrant cafe scene", "distance": 1.0, "URL": ""},
            {"rank": 4, "name": "VinWonders Theme Park (Vinpearl)", "postcode": "650000", "distanceKmFromAirport": 40, "description": "Cable car to the island amusement park across Nha Trang Bay", "distance": 5.0, "URL": "https://vinwonders.com/en/vinwonders-nha-trang/"},
            {"rank": 5, "name": "Ba Ho Waterfalls", "postcode": "650000", "distanceKmFromAirport": 20, "description": "Three mountain waterfall pools accessible by motorbike and jungle trek", "distance": 20.0, "URL": ""},
            {"rank": 6, "name": "Hot Spring Mud Bath", "postcode": "650000", "distanceKmFromAirport": 25, "description": "Volcanic mud baths in private tubs - popular Nha Trang spa experience", "distance": 10.0, "URL": "https://i-resort.vn/"},
            {"rank": 7, "name": "Long Son Pagoda", "postcode": "650000", "distanceKmFromAirport": 36, "description": "Buddhist pagoda with a giant white Buddha on the hillside above the city", "distance": 1.0, "URL": ""},
            {"rank": 8, "name": "Pasteur Institute Museum", "postcode": "650000", "distanceKmFromAirport": 36, "description": "Former research institute of Alexandre Yersin who discovered plague", "distance": 1.0, "URL": ""},
            {"rank": 9, "name": "Scuba Diving in Nha Trang", "postcode": "650000", "distanceKmFromAirport": 25, "description": "Over 25 dive sites in the marine protected area around the bay islands", "distance": 10.0, "URL": ""},
            {"rank": 10, "name": "Bun Ca (Fish Noodle Soup)", "postcode": "650000", "distanceKmFromAirport": 36, "description": "Nha Trang's signature breakfast soup with fresh fish, pineapple and herbs", "distance": 1.0, "URL": ""},
        ]
    },
    "niamey": {
        "city": "Niamey",
        "country": "Niger",
        "airportPostcode": "BP 10099",
        "airportDistanceKm": 12,
        "things": [
            {"rank": 1, "name": "National Museum of Niger", "postcode": "BP 248", "distanceKmFromAirport": 13, "description": "World-class outdoor museum with dinosaur fossils, traditional crafts and a zoo", "distance": 2.0, "URL": ""},
            {"rank": 2, "name": "Grand Marche", "postcode": "BP 10000", "distanceKmFromAirport": 12, "description": "West African market with Tuareg silverwork, leather goods and indigo cloth", "distance": 1.0, "URL": ""},
            {"rank": 3, "name": "Niger River Pirogue Cruise", "postcode": "BP 10000", "distanceKmFromAirport": 13, "description": "Sunset boat on the Niger with hippos and pelicans", "distance": 2.0, "URL": ""},
            {"rank": 4, "name": "Agadez (Day Trip)", "postcode": "BP 142", "distanceKmFromAirport": 912, "description": "UNESCO World Heritage Tuareg city in the Sahara with the famous mud-brick minaret", "distance": 900.0, "URL": "https://whc.unesco.org/en/list/1268"},
            {"rank": 5, "name": "Village Artisanal", "postcode": "BP 10000", "distanceKmFromAirport": 14, "description": "Craft village with Tuareg silversmiths making the famous Agadez Cross pendants", "distance": 3.0, "URL": ""},
            {"rank": 6, "name": "Kennedy Bridge", "postcode": "BP 10000", "distanceKmFromAirport": 13, "description": "Main bridge over the Niger river with views of the capital", "distance": 2.0, "URL": ""},
            {"rank": 7, "name": "Palais de Justice Cultural Events", "postcode": "BP 10000", "distanceKmFromAirport": 12, "description": "Colonial courts building hosting festivals and cultural performances", "distance": 1.0, "URL": ""},
            {"rank": 8, "name": "Wadata Market", "postcode": "BP 10000", "distanceKmFromAirport": 14, "description": "Traditional market in the Hausa quarter with kola nuts, dried goods and spices", "distance": 3.0, "URL": ""},
            {"rank": 9, "name": "Musee de la BCEAO", "postcode": "BP 10000", "distanceKmFromAirport": 13, "description": "Economic history of the West African franc zone in a modern museum", "distance": 2.0, "URL": "https://www.bceao.int/"},
            {"rank": 10, "name": "Djerma Millet Porridge", "postcode": "BP 10000", "distanceKmFromAirport": 12, "description": "Traditional Nigerien breakfast - millet porridge with sour milk and sugar", "distance": 1.0, "URL": ""},
        ]
    },
    "nis": {
        "city": "Nis",
        "country": "Serbia",
        "airportPostcode": "18210",
        "airportDistanceKm": 3,
        "things": [
            {"rank": 1, "name": "Nis Fortress", "postcode": "18000", "distanceKmFromAirport": 3, "description": "Impressive 18th-century Ottoman fortress on the Nisava river with four gates and towers", "distance": 0.5, "URL": "https://turistickinis.rs/"},
            {"rank": 2, "name": "Skull Tower (Cele Kula)", "postcode": "18000", "distanceKmFromAirport": 5, "description": "Chilling Ottoman tower built from the skulls of Serbian rebels after the 1809 Battle of Cegar", "distance": 1.5, "URL": ""},
            {"rank": 3, "name": "Naissus Archaeological Site", "postcode": "18000", "distanceKmFromAirport": 6, "description": "Birthplace of Emperor Constantine the Great with Roman ruins and basilicas", "distance": 3.0, "URL": ""},
            {"rank": 4, "name": "Nis Concentration Camp Memorial", "postcode": "18000", "distanceKmFromAirport": 5, "description": "WWII Nazi camp where 10,000 people were executed, now a solemn memorial", "distance": 2.0, "URL": ""},
            {"rank": 5, "name": "Cegar Hill Memorial", "postcode": "18204", "distanceKmFromAirport": 10, "description": "Site of the Battle of Cegar with a memorial chapel on the hillside", "distance": 8.0, "URL": ""},
            {"rank": 6, "name": "Main Pedestrian Zone (Zona)", "postcode": "18000", "distanceKmFromAirport": 3, "description": "Lively city centre promenade with restaurants, cafes and evening atmosphere", "distance": 0.5, "URL": ""},
            {"rank": 7, "name": "Mediana Roman Complex", "postcode": "18000", "distanceKmFromAirport": 6, "description": "4th-century Roman villa complex near the fortress with mosaic floors", "distance": 3.0, "URL": "http://www.mediana.org.rs/"},
            {"rank": 8, "name": "Suva Planina Mountain", "postcode": "18220", "distanceKmFromAirport": 32, "description": "National park with dramatic Sicevo Gorge and hiking in the Balkan highlands", "distance": 30.0, "URL": ""},
            {"rank": 9, "name": "Sicevo Gorge", "postcode": "18220", "distanceKmFromAirport": 22, "description": "Spectacular limestone gorge carved by the Nisava river with walking trails", "distance": 20.0, "URL": ""},
            {"rank": 10, "name": "Nis Thermal Spa", "postcode": "18211", "distanceKmFromAirport": 12, "description": "Natural thermal springs at the Niska Banja spa resort just 10km from the city", "distance": 10.0, "URL": "https://www.niska-banja.org/"},
        ]
    },
    "nottingham": {
        "city": "Nottingham",
        "country": "United Kingdom",
        "airportPostcode": "DE74 2SA",
        "airportDistanceKm": 25,
        "things": [
            {"rank": 1, "name": "Nottingham Castle", "postcode": "NG1 6EL", "distanceKmFromAirport": 25, "description": "Historic castle and museum on a sandstone rock with views over the city", "distance": 0.5, "URL": "https://www.nottinghamcastle.org.uk/"},
            {"rank": 2, "name": "Sherwood Forest", "postcode": "NG21 9HN", "distanceKmFromAirport": 40, "description": "Ancient royal forest famous as the home of Robin Hood with 1,000-year-old Major Oak", "distance": 22.0, "URL": "https://www.sherwoodforest.org.uk/"},
            {"rank": 3, "name": "City of Caves", "postcode": "NG1 7LS", "distanceKmFromAirport": 25, "description": "Network of 500+ sandstone caves beneath the city streets with fascinating history", "distance": 0.5, "URL": "https://www.cityofcaves.com/"},
            {"rank": 4, "name": "Wollaton Hall", "postcode": "NG8 2AE", "distanceKmFromAirport": 28, "description": "Spectacular Elizabethan mansion in a deer park, used as Wayne Manor in The Dark Knight Rises", "distance": 5.0, "URL": "https://www.wollatonhall.org.uk/"},
            {"rank": 5, "name": "Old Market Square", "postcode": "NG1 2BY", "distanceKmFromAirport": 25, "description": "One of the largest market squares in England, lined with cafes and hosting events year-round", "distance": 0.3, "URL": ""},
            {"rank": 6, "name": "Nottingham Contemporary", "postcode": "NG1 1NB", "distanceKmFromAirport": 25, "description": "Largest contemporary art gallery in the East Midlands with changing exhibitions", "distance": 0.5, "URL": "https://www.nottinghamcontemporary.org/"},
            {"rank": 7, "name": "Green's Windmill", "postcode": "NG2 4QB", "distanceKmFromAirport": 26, "description": "Restored 19th-century tower mill where mathematician George Green was born and worked", "distance": 2.0, "URL": "https://www.greensmill.org.uk/"},
            {"rank": 8, "name": "National Ice Centre", "postcode": "NG1 1LA", "distanceKmFromAirport": 25, "description": "Home to the Nottingham Panthers and Britain's largest twin-pad indoor ice facility", "distance": 0.5, "URL": "https://www.national-ice-centre.com/"},
            {"rank": 9, "name": "Nottingham Arboretum", "postcode": "NG1 4JB", "distanceKmFromAirport": 26, "description": "Victorian park and one of the oldest public parks in England", "distance": 1.5, "URL": ""},
            {"rank": 10, "name": "Tales of Robin Hood", "postcode": "NG1 7LD", "distanceKmFromAirport": 25, "description": "Interactive attraction bringing the Robin Hood legend vividly to life", "distance": 0.5, "URL": ""},
        ]
    },
    "nouakchott": {
        "city": "Nouakchott",
        "country": "Mauritania",
        "airportPostcode": "BP 1014",
        "airportDistanceKm": 4,
        "things": [
            {"rank": 1, "name": "Camel Market (Marche au Chameau)", "postcode": "BP 1000", "distanceKmFromAirport": 8, "description": "Hundreds of camels auctioned weekly on the edge of the Sahara Desert", "distance": 5.0, "URL": ""},
            {"rank": 2, "name": "Banc d'Arguin National Park", "postcode": "BP 5", "distanceKmFromAirport": 124, "description": "UNESCO World Heritage tidal flats - the world's most important migratory bird staging post", "distance": 120.0, "URL": "https://whc.unesco.org/en/list/506"},
            {"rank": 3, "name": "Iron Ore Train (Mauritania Railway)", "postcode": "BP 1", "distanceKmFromAirport": 504, "description": "Ride the world's longest and heaviest freight train - 3km of iron ore wagons across the Sahara", "distance": 500.0, "URL": ""},
            {"rank": 4, "name": "Nouakchott Fishing Port (Port de Peche)", "postcode": "BP 1000", "distanceKmFromAirport": 7, "description": "Hundreds of painted pirogues land their catch - the biggest artisanal fishing port in the world", "distance": 3.0, "URL": ""},
            {"rank": 5, "name": "Marche Capitale", "postcode": "BP 1000", "distanceKmFromAirport": 5, "description": "Main city market with Tuareg silverwork, indigo cloth and Saharan crafts", "distance": 1.0, "URL": ""},
            {"rank": 6, "name": "Musee National de Mauritanie", "postcode": "BP 1000", "distanceKmFromAirport": 6, "description": "Mauritanian prehistory, Islamic manuscripts and Moorish silver jewellery", "distance": 2.0, "URL": ""},
            {"rank": 7, "name": "Chinguetti Ancient Libraries", "postcode": "BP 1", "distanceKmFromAirport": 464, "description": "UNESCO World Heritage holy city with medieval Islamic manuscript libraries", "distance": 460.0, "URL": "https://whc.unesco.org/en/list/750"},
            {"rank": 8, "name": "Atar & Adrar Plateau", "postcode": "BP 1", "distanceKmFromAirport": 464, "description": "Dramatic sandstone plateau with palm-lined gorges and ancient caravan towns", "distance": 460.0, "URL": ""},
            {"rank": 9, "name": "Atlantic Ocean Beaches", "postcode": "BP 1000", "distanceKmFromAirport": 6, "description": "Huge empty Atlantic beaches stretching for hundreds of kilometres", "distance": 2.0, "URL": ""},
            {"rank": 10, "name": "Thieboudienne (Rice and Fish)", "postcode": "BP 1000", "distanceKmFromAirport": 5, "description": "Shared from Senegal - the definitive West African dish of rice cooked in fish stock with vegetables", "distance": 1.0, "URL": ""},
        ]
    },
    "novosibirsk": {
        "city": "Novosibirsk",
        "country": "Russia",
        "airportPostcode": "633109",
        "airportDistanceKm": 17,
        "things": [
            {"rank": 1, "name": "Novosibirsk Opera and Ballet Theatre", "postcode": "630099", "distanceKmFromAirport": 17, "description": "Russia's largest opera and ballet theatre in a striking neo-Classical building", "distance": 0.5, "URL": "https://novat.nsk.ru/"},
            {"rank": 2, "name": "Novosibirsk Zoo", "postcode": "630007", "distanceKmFromAirport": 18, "description": "One of Russia's top zoos with 700+ species including the famous white tigers and snow leopards", "distance": 2.0, "URL": "https://zoonovosib.ru/"},
            {"rank": 3, "name": "Akademgorodok (Science City)", "postcode": "630090", "distanceKmFromAirport": 35, "description": "Soviet-era academic city in the taiga forest, home to the Siberian Branch of the Russian Academy of Sciences", "distance": 25.0, "URL": "https://www.sbras.ru/"},
            {"rank": 4, "name": "Novosibirsk State Art Museum", "postcode": "630007", "distanceKmFromAirport": 17, "description": "Regional art collection with Russian academic painting and Siberian folk art", "distance": 1.0, "URL": "https://artmuseum.ru/"},
            {"rank": 5, "name": "Trans-Siberian Railway Museum", "postcode": "630004", "distanceKmFromAirport": 18, "description": "Museum at the original 1897 Novosibirsk station on the world's longest railway", "distance": 2.0, "URL": ""},
            {"rank": 6, "name": "Ob Sea Beach", "postcode": "630003", "distanceKmFromAirport": 22, "description": "Vast man-made Ob reservoir beach known as the 'Siberian Sea' for summer swimming", "distance": 15.0, "URL": ""},
            {"rank": 7, "name": "Chapel of St Nicholas", "postcode": "630099", "distanceKmFromAirport": 17, "description": "Restored chapel marking the geographical centre of Russia at the foot of the main bridge", "distance": 0.5, "URL": ""},
            {"rank": 8, "name": "Lenin Square", "postcode": "630099", "distanceKmFromAirport": 17, "description": "Central Soviet-era square with the Stalin-era regional government building and the Novosibirsk banner", "distance": 0.5, "URL": ""},
            {"rank": 9, "name": "Museum of the Sun", "postcode": "630000", "distanceKmFromAirport": 19, "description": "Unique private collection of sun symbols from cultures around the world", "distance": 3.0, "URL": "https://www.muzeysolnca.ru/"},
            {"rank": 10, "name": "Berdsk Beach & Ob Forests", "postcode": "633004", "distanceKmFromAirport": 35, "description": "Sandy pine forest beaches south of the city on the Ob reservoir", "distance": 35.0, "URL": ""},
        ]
    },
    "nukualofa": {
        "city": "Nuku'alofa",
        "country": "Tonga",
        "airportPostcode": "676",
        "airportDistanceKm": 21,
        "things": [
            {"rank": 1, "name": "Humpback Whale Swimming (July-October)", "postcode": "676", "distanceKmFromAirport": 30, "description": "Tonga is the only place in the world to legally swim with humpback whales", "distance": 20.0, "URL": "https://www.tongaholiday.com/"},
            {"rank": 2, "name": "Royal Palace of Tonga", "postcode": "676", "distanceKmFromAirport": 21, "description": "Victorian wooden palace of the Tongan royal family surrounded by Norfolk pines", "distance": 1.0, "URL": ""},
            {"rank": 3, "name": "Ha'amonga 'a Maui Trilithon", "postcode": "676", "distanceKmFromAirport": 25, "description": "13th-century coral stone trilithon - Tonga's Stonehenge - aligned with the solstice", "distance": 35.0, "URL": ""},
            {"rank": 4, "name": "Blowholes of Houma", "postcode": "676", "distanceKmFromAirport": 28, "description": "Natural limestone blowholes shooting water 30m into the air on the south coast", "distance": 16.0, "URL": ""},
            {"rank": 5, "name": "Anahulu Cave", "postcode": "676", "distanceKmFromAirport": 20, "description": "Swimming in a freshwater limestone cave with stalactites and natural ceiling opening", "distance": 22.0, "URL": ""},
            {"rank": 6, "name": "Flea Market & Talamahu Market", "postcode": "676", "distanceKmFromAirport": 21, "description": "Tapa cloth, woven mats, vanilla beans and fresh tropical produce", "distance": 0.5, "URL": ""},
            {"rank": 7, "name": "Royal Tombs (Mala'e Kula)", "postcode": "676", "distanceKmFromAirport": 21, "description": "Burial ground of the Tongan royal family since the 11th century", "distance": 1.0, "URL": ""},
            {"rank": 8, "name": "Ha'apai Islands Getaway", "postcode": "676", "distanceKmFromAirport": 185, "description": "Pristine uninhabited island beaches and magnificent whale-watching", "distance": 170.0, "URL": "https://www.haapai.to/"},
            {"rank": 9, "name": "Tongan Feast (Ufi Puna)", "postcode": "676", "distanceKmFromAirport": 22, "description": "Underground earth oven feast with suckling pig, taro and lu sipi (mutton flaps in coconut)", "distance": 2.0, "URL": ""},
            {"rank": 10, "name": "Sunday Church Singing", "postcode": "676", "distanceKmFromAirport": 21, "description": "Tonga's extraordinary choral church singing every Sunday morning", "distance": 1.0, "URL": ""},
        ]
    },
    "odessa": {
        "city": "Odessa",
        "country": "Ukraine",
        "airportPostcode": "65003",
        "airportDistanceKm": 10,
        "things": [
            {"rank": 1, "name": "Potemkin Stairs", "postcode": "65026", "distanceKmFromAirport": 10, "description": "Iconic 192-step stairway from the city to the port, immortalised in Eisenstein's 1925 film", "distance": 1.0, "URL": ""},
            {"rank": 2, "name": "Opera and Ballet Theatre", "postcode": "65011", "distanceKmFromAirport": 10, "description": "1887 Neo-Baroque opera house - one of the most beautiful in Europe with a stunning interior", "distance": 1.0, "URL": "https://opera.odessa.ua/"},
            {"rank": 3, "name": "Deribasivska Street", "postcode": "65014", "distanceKmFromAirport": 10, "description": "Odessa's pedestrian main street with 19th-century architecture, cafes and restaurants", "distance": 0.5, "URL": ""},
            {"rank": 4, "name": "Odessa Catacombs", "postcode": "65000", "distanceKmFromAirport": 20, "description": "2,500km network of underground tunnels used by partisans in WWII - the world's largest catacomb", "distance": 15.0, "URL": "https://catacombs.ua/"},
            {"rank": 5, "name": "Arcadia Beach", "postcode": "65009", "distanceKmFromAirport": 14, "description": "Odessa's most popular beach and entertainment district with clubs and seaside restaurants", "distance": 5.0, "URL": ""},
            {"rank": 6, "name": "Vorontsov Palace", "postcode": "65026", "distanceKmFromAirport": 10, "description": "Elegant Neoclassical governor's palace with colonnaded loggia overlooking the sea", "distance": 1.0, "URL": ""},
            {"rank": 7, "name": "Odessa Fine Arts Museum", "postcode": "65011", "distanceKmFromAirport": 10, "description": "Classicist palace housing masterworks including Caravaggio, Rubens and Russian masters", "distance": 1.0, "URL": "https://ofam.com.ua/"},
            {"rank": 8, "name": "Privoz Market", "postcode": "65026", "distanceKmFromAirport": 11, "description": "Vast open-air market with the freshest Black Sea fish, produce and local street food", "distance": 1.5, "URL": ""},
            {"rank": 9, "name": "Lanzheron Beach & Spa", "postcode": "65045", "distanceKmFromAirport": 12, "description": "City beach with a saltwater spa, beach clubs and great views of the Odessa skyline", "distance": 3.0, "URL": ""},
            {"rank": 10, "name": "Plague Column (Chumna Kolona)", "postcode": "65011", "distanceKmFromAirport": 10, "description": "1827 column erected to give thanks for deliverance from the 1812-1814 plague epidemic", "distance": 1.0, "URL": ""},
        ]
    }
}

output_dir = r"c:\Users\junkp\MagicMirror\modules\MMM-iAmGoingThere\data\attractions"

for city_key, city_data in data.items():
    output_file = f"{output_dir}\\{city_key}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(city_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] {city_key}.json")

print("\nAll files updated successfully!")
