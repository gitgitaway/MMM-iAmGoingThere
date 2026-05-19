#!/usr/bin/env python3
import json
import os

cities_data = {
    "luang_prabang": {
        "city": "Luang Prabang",
        "country": "Laos",
        "airportPostcode": "0600",
        "airportDistanceKm": 4,
        "things": [
            {
                "rank": 1,
                "name": "Tak Bat (Almsgiving Ceremony)",
                "postcode": "06000",
                "distanceKmFromAirport": 5,
                "description": "Dawn procession of orange-robed monks collecting alms - deeply spiritual and moving",
                "distance": 0.5,
                "URL": "https://www.tourismlaos.org/"
            },
            {
                "rank": 2,
                "name": "Kuang Si Waterfalls",
                "postcode": "06270",
                "distanceKmFromAirport": 33,
                "description": "Turquoise travertine pools and a 50m main waterfall with a bear rescue sanctuary",
                "distance": 29.0,
                "URL": "https://www.kuangsifalls.com/"
            },
            {
                "rank": 3,
                "name": "Royal Palace Museum",
                "postcode": "06000",
                "distanceKmFromAirport": 4,
                "description": "Last royal palace of the Kingdom of Laos with the sacred Pha Bang gold Buddha",
                "distance": 0.2,
                "URL": "https://www.tourismlaos.org/"
            },
            {
                "rank": 4,
                "name": "Wat Xieng Thong",
                "postcode": "06000",
                "distanceKmFromAirport": 5,
                "description": "Finest temple in Laos with a sweeping multi-tiered roof and mosaics of the tree of life",
                "distance": 0.8,
                "URL": "https://www.tourismlaos.org/"
            },
            {
                "rank": 5,
                "name": "Mount Phousi",
                "postcode": "06000",
                "distanceKmFromAirport": 4,
                "description": "Hilltop stupa with 360-degree sunset views over the Mekong and Nam Khan rivers",
                "distance": 0.3,
                "URL": "https://www.tourismlaos.org/"
            },
            {
                "rank": 6,
                "name": "Mekong River Slow Boat",
                "postcode": "06000",
                "distanceKmFromAirport": 5,
                "description": "Two-day slow boat journey down the Mekong through spectacular jungle scenery",
                "distance": 0.5,
                "URL": "https://www.tourismlaos.org/"
            },
            {
                "rank": 7,
                "name": "Night Market",
                "postcode": "06000",
                "distanceKmFromAirport": 4,
                "description": "Nightly textile market with indigo-dyed fabrics, silver jewellery and local handicrafts",
                "distance": 0.3,
                "URL": "https://www.tourismlaos.org/"
            },
            {
                "rank": 8,
                "name": "Old Town Walking Tour",
                "postcode": "06000",
                "distanceKmFromAirport": 4,
                "description": "UNESCO World Heritage peninsula with 33 temples between the Mekong and Nam Khan",
                "distance": 0.3,
                "URL": "https://www.tourismlaos.org/"
            },
            {
                "rank": 9,
                "name": "Pak Ou Caves",
                "postcode": "06270",
                "distanceKmFromAirport": 21,
                "description": "River-mouth caves crammed with thousands of Buddha images - accessible by boat",
                "distance": 25.0,
                "URL": "https://www.tourismlaos.org/"
            },
            {
                "rank": 10,
                "name": "Tad Sae Waterfall",
                "postcode": "06270",
                "distanceKmFromAirport": 19,
                "description": "Accessible by boat and elephant - beautiful tiered waterfall for swimming",
                "distance": 15.0,
                "URL": "https://www.tourismlaos.org/"
            }
        ]
    },
    "lucknow": {
        "city": "Lucknow",
        "country": "India",
        "airportPostcode": "226021",
        "airportDistanceKm": 18,
        "things": [
            {
                "rank": 1,
                "name": "Bara Imambara",
                "postcode": "226003",
                "distanceKmFromAirport": 19,
                "description": "1784 Nawabi complex with the remarkable Bhulbhuliya labyrinth maze of passages",
                "distance": 1.0,
                "URL": "https://uptourism.gov.in/"
            },
            {
                "rank": 2,
                "name": "Chota Imambara (Husainabad)",
                "postcode": "226003",
                "distanceKmFromAirport": 19,
                "description": "Nawab Muhammad Ali Shah's 1838 imambara with chandeliers and gilded interior",
                "distance": 1.2,
                "URL": "https://uptourism.gov.in/"
            },
            {
                "rank": 3,
                "name": "Rumi Darwaza",
                "postcode": "226003",
                "distanceKmFromAirport": 19,
                "description": "Imposing 18m gateway built in 1784 modelled after a gate in Constantinople",
                "distance": 1.0,
                "URL": "https://uptourism.gov.in/"
            },
            {
                "rank": 4,
                "name": "British Residency",
                "postcode": "226001",
                "distanceKmFromAirport": 20,
                "description": "Ruins of the British Residency besieged for 87 days during the 1857 Uprising",
                "distance": 1.5,
                "URL": "https://asi.nic.in/"
            },
            {
                "rank": 5,
                "name": "Chattar Manzil (Umbrella Palace)",
                "postcode": "226001",
                "distanceKmFromAirport": 19,
                "description": "Nawabi palace on the Gomti riverbank now housing research institutes",
                "distance": 1.0,
                "URL": "https://uptourism.gov.in/"
            },
            {
                "rank": 6,
                "name": "Chowk Heritage Walk",
                "postcode": "226003",
                "distanceKmFromAirport": 20,
                "description": "Old city market streets with Lucknawi chikankari embroidery workshops",
                "distance": 1.5,
                "URL": "https://uptourism.gov.in/"
            },
            {
                "rank": 7,
                "name": "Lucknow Zoo & Safari",
                "postcode": "226001",
                "distanceKmFromAirport": 22,
                "description": "One of India's finest zoos featuring tigers, white tigers and gharial crocodiles",
                "distance": 3.5,
                "URL": "https://www.lucknowzoo.com/"
            },
            {
                "rank": 8,
                "name": "Nawab Wajid Ali Shah Planetarium",
                "postcode": "226001",
                "distanceKmFromAirport": 21,
                "description": "Cultural centre celebrating the last Nawab of Awadh's arts and culture",
                "distance": 3.0,
                "URL": "https://uptourism.gov.in/"
            },
            {
                "rank": 9,
                "name": "Chikankari Embroidery Shopping",
                "postcode": "226003",
                "distanceKmFromAirport": 19,
                "description": "Lucknow's delicate white-on-white needlework embroidery - India's most refined craft",
                "distance": 1.0,
                "URL": "https://uptourism.gov.in/"
            },
            {
                "rank": 10,
                "name": "Tunday Kebabi Restaurant (1905)",
                "postcode": "226003",
                "distanceKmFromAirport": 20,
                "description": "The world's finest kebabs - galouti kebab so soft it melts on your tongue",
                "distance": 1.5,
                "URL": "https://uptourism.gov.in/"
            }
        ]
    },
    "luton": {
        "city": "Luton",
        "country": "United Kingdom",
        "airportPostcode": "LU2 9LY",
        "airportDistanceKm": 50,
        "things": [
            {
                "rank": 1,
                "name": "Whipsnade Zoo",
                "postcode": "LU6 2LF",
                "distanceKmFromAirport": 10,
                "description": "Europe's largest zoo covering 600 acres with over 3,600 animals",
                "distance": 8.0,
                "URL": "https://www.zsl.org/whipsnade-zoo"
            },
            {
                "rank": 2,
                "name": "Woburn Abbey & Safari Park",
                "postcode": "MK17 9WA",
                "distanceKmFromAirport": 20,
                "description": "Ancestral home of the Dukes of Bedford with a renowned drive-through safari park",
                "distance": 18.0,
                "URL": "https://www.woburnabbey.co.uk/"
            },
            {
                "rank": 3,
                "name": "Luton Hoo Estate",
                "postcode": "LU1 3TQ",
                "distanceKmFromAirport": 5,
                "description": "Grand country house in a Capability Brown landscape with luxury hotel",
                "distance": 3.0,
                "URL": "https://www.lutonhoo.com/"
            },
            {
                "rank": 4,
                "name": "Dunstable Downs",
                "postcode": "LU6 2GY",
                "distanceKmFromAirport": 12,
                "description": "Chalk escarpment popular for kite flying with stunning views over the vale",
                "distance": 10.0,
                "URL": "https://www.nationaltrust.org.uk/dunstable-downs-and-whipsnade-estate"
            },
            {
                "rank": 5,
                "name": "Stockwood Discovery Centre",
                "postcode": "LU1 4LX",
                "distanceKmFromAirport": 5,
                "description": "Museum of local history with period gardens and craft museum",
                "distance": 3.5,
                "URL": "https://www.lutonculture.com/stockwood/"
            },
            {
                "rank": 6,
                "name": "Wardown Museum",
                "postcode": "LU2 7HA",
                "distanceKmFromAirport": 4,
                "description": "Victorian park museum with local lace collection and social history",
                "distance": 1.5,
                "URL": "https://www.lutonculture.com/wardown/"
            },
            {
                "rank": 7,
                "name": "Dunstable Priory",
                "postcode": "LU5 4RS",
                "distanceKmFromAirport": 11,
                "description": "Historic 12th-century Augustinian priory where Henry VIII's marriage to Catherine was annulled",
                "distance": 9.0,
                "URL": "https://www.historicengland.org.uk/"
            },
            {
                "rank": 8,
                "name": "Chiltern Hills AONB",
                "postcode": "HP4 1NX",
                "distanceKmFromAirport": 15,
                "description": "Beautiful chalk hills with villages, ancient woodland and the Ridgeway path",
                "distance": 15.0,
                "URL": "https://www.chilternsaonb.org/"
            },
            {
                "rank": 9,
                "name": "Knebworth House",
                "postcode": "SG3 6PY",
                "distanceKmFromAirport": 30,
                "description": "Gothic stately home with gardens, maze and legendary open-air concert venue",
                "distance": 28.0,
                "URL": "https://www.knebworthhouse.com/"
            },
            {
                "rank": 10,
                "name": "De Havilland Aircraft Museum",
                "postcode": "AL2 1EX",
                "distanceKmFromAirport": 24,
                "description": "Britain's oldest aircraft museum housing the world's only surviving Mosquito prototype",
                "distance": 24.0,
                "URL": "https://www.dehavillandmuseum.co.uk/"
            }
        ]
    },
    "luxembourg_city": {
        "city": "Luxembourg City",
        "country": "Luxembourg",
        "airportPostcode": "2987",
        "airportDistanceKm": 6,
        "things": [
            {
                "rank": 1,
                "name": "Bock Casemates",
                "postcode": "L-1468",
                "distanceKmFromAirport": 7,
                "description": "UNESCO World Heritage 17km network of underground tunnels carved into the rock over 400 years",
                "distance": 0.5,
                "URL": "https://www.luxembourg-city.com/en/place/bock-casemates"
            },
            {
                "rank": 2,
                "name": "Grand Ducal Palace",
                "postcode": "L-1017",
                "distanceKmFromAirport": 6,
                "description": "Late Renaissance palace in the heart of the old town, official residence of the Grand Duke",
                "distance": 0.2,
                "URL": "https://monarchie.lu/"
            },
            {
                "rank": 3,
                "name": "Notre-Dame Cathedral",
                "postcode": "L-2240",
                "distanceKmFromAirport": 6,
                "description": "Early Baroque cathedral with the revered Our Lady of Luxembourg statue",
                "distance": 0.3,
                "URL": "https://www.cathol.lu/"
            },
            {
                "rank": 4,
                "name": "Adolphe Bridge",
                "postcode": "L-1114",
                "distanceKmFromAirport": 7,
                "description": "Elegant 1903 arch bridge spanning the Petrusse valley with views of the old town",
                "distance": 0.8,
                "URL": "https://www.luxembourg-city.com/"
            },
            {
                "rank": 5,
                "name": "MUDAM Luxembourg",
                "postcode": "L-2090",
                "distanceKmFromAirport": 8,
                "description": "Grand Duke Jean Museum of Modern Art in a striking I.M. Pei building",
                "distance": 1.5,
                "URL": "https://www.mudam.com/"
            },
            {
                "rank": 6,
                "name": "Chemin de la Corniche",
                "postcode": "L-1344",
                "distanceKmFromAirport": 7,
                "description": "Panoramic clifftop promenade dubbed 'Europe's most beautiful balcony'",
                "distance": 0.5,
                "URL": "https://www.luxembourg-city.com/"
            },
            {
                "rank": 7,
                "name": "Pfaffenthal Elevator",
                "postcode": "L-1629",
                "distanceKmFromAirport": 7,
                "description": "Free public panoramic elevator connecting the upper and lower city",
                "distance": 0.7,
                "URL": "https://www.luxembourg-city.com/"
            },
            {
                "rank": 8,
                "name": "Grund District",
                "postcode": "L-1645",
                "distanceKmFromAirport": 7,
                "description": "Picturesque lower town along the Alzette river with bars and riverside walks",
                "distance": 1.0,
                "URL": "https://www.luxembourg-city.com/"
            },
            {
                "rank": 9,
                "name": "National Museum of History and Art",
                "postcode": "L-1468",
                "distanceKmFromAirport": 6,
                "description": "Archaeology, decorative arts and fine art from Gallo-Roman times to today",
                "distance": 0.3,
                "URL": "https://mnha.lu/"
            },
            {
                "rank": 10,
                "name": "Vianden Castle",
                "postcode": "L-9408",
                "distanceKmFromAirport": 46,
                "description": "Day trip to one of Europe's finest Gothic-Romanesque castles above the Our river",
                "distance": 40.0,
                "URL": "https://www.vianden-castle.lu/"
            }
        ]
    },
    "lviv": {
        "city": "Lviv",
        "country": "Ukraine",
        "airportPostcode": "79019",
        "airportDistanceKm": 7,
        "things": [
            {
                "rank": 1,
                "name": "Lviv Historic Centre",
                "postcode": "79000",
                "distanceKmFromAirport": 8,
                "description": "UNESCO World Heritage old town with Renaissance, Baroque and Gothic architecture",
                "distance": 0.5,
                "URL": "https://lviv.travel/"
            },
            {
                "rank": 2,
                "name": "High Castle Hill (Vysokyi Zamok)",
                "postcode": "79008",
                "distanceKmFromAirport": 8,
                "description": "Hilltop park with panoramic views over the old town and Lviv's rooftops",
                "distance": 1.2,
                "URL": "https://lviv.travel/"
            },
            {
                "rank": 3,
                "name": "Rynok Square (Market Square)",
                "postcode": "79000",
                "distanceKmFromAirport": 7,
                "description": "Historic market square surrounded by colourful merchant houses and the 16th-century Town Hall",
                "distance": 0.2,
                "URL": "https://lviv.travel/"
            },
            {
                "rank": 4,
                "name": "Lviv Coffee Culture",
                "postcode": "79000",
                "distanceKmFromAirport": 7,
                "description": "Lviv claims to have introduced coffee to Europe - explore the coffee mine and themed cafes",
                "distance": 0.3,
                "URL": "https://lviv.travel/"
            },
            {
                "rank": 5,
                "name": "Dormition Church (Uspenska)",
                "postcode": "79000",
                "distanceKmFromAirport": 7,
                "description": "Renaissance ensemble with a three-apse church, the Korniakt Tower and the Chapel of the Three Saints",
                "distance": 0.4,
                "URL": "https://lviv.travel/"
            },
            {
                "rank": 6,
                "name": "Lychakiv Cemetery",
                "postcode": "79010",
                "distanceKmFromAirport": 10,
                "description": "Romantic 19th-century cemetery with elaborate sculptures and the graves of Ukrainian heroes",
                "distance": 2.5,
                "URL": "https://lychakiv.org/"
            },
            {
                "rank": 7,
                "name": "Armenian Cathedral of the Assumption",
                "postcode": "79000",
                "distanceKmFromAirport": 7,
                "description": "14th-century Armenian cathedral with unique courtyard and 17th-century frescoes",
                "distance": 0.4,
                "URL": "https://lviv.travel/"
            },
            {
                "rank": 8,
                "name": "Pharmacy Museum",
                "postcode": "79000",
                "distanceKmFromAirport": 7,
                "description": "19th-century pharmacy with original fittings, the oldest operating pharmacy in Ukraine",
                "distance": 0.3,
                "URL": "https://lviv.travel/"
            },
            {
                "rank": 9,
                "name": "Shevchenkivskyi Hai Open-Air Museum",
                "postcode": "79013",
                "distanceKmFromAirport": 10,
                "description": "Folk architecture park with 120 original wooden buildings from the Carpathian region",
                "distance": 3.0,
                "URL": "https://skansen.lviv.ua/"
            },
            {
                "rank": 10,
                "name": "Lviv Chocolate Workshop",
                "postcode": "79000",
                "distanceKmFromAirport": 7,
                "description": "Famous chocolate workshops making the city's renowned handmade truffles and pralines",
                "distance": 0.3,
                "URL": "https://chocolate.lviv.ua/"
            }
        ]
    },
    "majuro": {
        "city": "Majuro",
        "country": "Marshall Islands",
        "airportPostcode": "96960",
        "airportDistanceKm": 3,
        "things": [
            {
                "rank": 1,
                "name": "Bikini Atoll Day Trip",
                "postcode": "96940",
                "distanceKmFromAirport": 1500,
                "description": "UNESCO World Heritage nuclear test site - extraordinary diving on sunken US and Japanese warships",
                "distance": 1500.0,
                "URL": "https://whc.unesco.org/en/list/1339"
            },
            {
                "rank": 2,
                "name": "Alele Museum & Public Library",
                "postcode": "96960",
                "distanceKmFromAirport": 4,
                "description": "Marshallese history, navigation stick charts and WWII and nuclear test era",
                "distance": 1.0,
                "URL": "https://www.visitmajuro.com/"
            },
            {
                "rank": 3,
                "name": "WWII Relics (Eniwetok)",
                "postcode": "96940",
                "distanceKmFromAirport": 1200,
                "description": "Remains of WWII battles and nuclear test infrastructure",
                "distance": 1200.0,
                "URL": "https://www.visitmajuro.com/"
            },
            {
                "rank": 4,
                "name": "Majuro Atoll Lagoon Sailing",
                "postcode": "96960",
                "distanceKmFromAirport": 4,
                "description": "Sail a traditional outrigger canoe on the world's largest atoll lagoon",
                "distance": 0.5,
                "URL": "https://www.visitmajuro.com/"
            },
            {
                "rank": 5,
                "name": "Traditional Navigation Stick Charts",
                "postcode": "96960",
                "distanceKmFromAirport": 4,
                "description": "Learn to read the traditional Marshallese wave and island navigation charts",
                "distance": 1.0,
                "URL": "https://www.visitmajuro.com/"
            },
            {
                "rank": 6,
                "name": "Laura Beach",
                "postcode": "96960",
                "distanceKmFromAirport": 37,
                "description": "Finest beach on Majuro at the far western end of the atoll",
                "distance": 34.0,
                "URL": "https://www.visitmajuro.com/"
            },
            {
                "rank": 7,
                "name": "Marshallese Canoe Building",
                "postcode": "96960",
                "distanceKmFromAirport": 4,
                "description": "Traditional outrigger canoe construction using traditional methods",
                "distance": 1.0,
                "URL": "https://www.visitmajuro.com/"
            },
            {
                "rank": 8,
                "name": "Sunrise Market",
                "postcode": "96960",
                "distanceKmFromAirport": 4,
                "description": "Fresh fish, breadfruit, pandanus and local produce at the main market",
                "distance": 0.5,
                "URL": "https://www.visitmajuro.com/"
            },
            {
                "rank": 9,
                "name": "Giant Clam Research Farm",
                "postcode": "96960",
                "distanceKmFromAirport": 8,
                "description": "Visit the MIMRA Giant Clam Research Facility restocking reefs",
                "distance": 5.0,
                "URL": "https://www.visitmajuro.com/"
            },
            {
                "rank": 10,
                "name": "Pandanus Weaving",
                "postcode": "96960",
                "distanceKmFromAirport": 4,
                "description": "Watch and learn traditional Marshallese pandanus leaf weaving",
                "distance": 1.0,
                "URL": "https://www.visitmajuro.com/"
            }
        ]
    },
    "makassar": {
        "city": "Makassar",
        "country": "Indonesia",
        "airportPostcode": "90553",
        "airportDistanceKm": 18,
        "things": [
            {
                "rank": 1,
                "name": "Fort Rotterdam",
                "postcode": "90111",
                "distanceKmFromAirport": 19,
                "description": "1607 Dutch colonial fort with two museums of South Sulawesi history and ethnography",
                "distance": 0.5,
                "URL": "https://makassar.go.id/"
            },
            {
                "rank": 2,
                "name": "Tana Toraja Funeral Ceremonies",
                "postcode": "91811",
                "distanceKmFromAirport": 338,
                "description": "8-hour drive to Tana Toraja - extraordinary cliff graves and elaborate funeral rites",
                "distance": 320.0,
                "URL": "https://www.indonesia.travel/"
            },
            {
                "rank": 3,
                "name": "Losari Beach Sunset",
                "postcode": "90114",
                "distanceKmFromAirport": 20,
                "description": "Iconic sunset promenade with the floating mosque and traditional Makassar seafood",
                "distance": 1.5,
                "URL": "https://makassar.go.id/"
            },
            {
                "rank": 4,
                "name": "Bugis Schooner Port (Pelabuhan Paotere)",
                "postcode": "90131",
                "distanceKmFromAirport": 20,
                "description": "Traditional wooden Bugis Phinisi ships - the world's last working wooden cargo fleet",
                "distance": 2.0,
                "URL": "https://makassar.go.id/"
            },
            {
                "rank": 5,
                "name": "Sulawesi Exhibition at Balla Lompoa Palace",
                "postcode": "92111",
                "distanceKmFromAirport": 26,
                "description": "Gowa Kingdom royal regalia including the magnificent royal crown",
                "distance": 8.0,
                "URL": "https://makassar.go.id/"
            },
            {
                "rank": 6,
                "name": "Bantimurung Waterfall",
                "postcode": "90561",
                "distanceKmFromAirport": 60,
                "description": "Karst limestone waterfall park where Alfred Russel Wallace collected butterflies",
                "distance": 42.0,
                "URL": "https://www.indonesia.travel/"
            },
            {
                "rank": 7,
                "name": "Samalona Island Day Trip",
                "postcode": "90000",
                "distanceKmFromAirport": 28,
                "description": "Snorkelling on the coral reef 10km offshore",
                "distance": 10.0,
                "URL": "https://makassar.go.id/"
            },
            {
                "rank": 8,
                "name": "Leang-Leang Cave Paintings",
                "postcode": "90561",
                "distanceKmFromAirport": 58,
                "description": "35,000-year-old cave paintings - possibly the world's oldest figurative art",
                "distance": 40.0,
                "URL": "https://www.indonesia.travel/"
            },
            {
                "rank": 9,
                "name": "Karebosi Square",
                "postcode": "90111",
                "distanceKmFromAirport": 18,
                "description": "Central public square with views of the Makassar cityscape",
                "distance": 0.3,
                "URL": "https://makassar.go.id/"
            },
            {
                "rank": 10,
                "name": "Coto Makassar (Beef Offal Soup)",
                "postcode": "90111",
                "distanceKmFromAirport": 19,
                "description": "Makassar's famous spiced offal soup eaten with ketupat rice cake",
                "distance": 1.0,
                "URL": "https://makassar.go.id/"
            }
        ]
    },
    "malabo": {
        "city": "Malabo",
        "country": "Equatorial Guinea",
        "airportPostcode": "BP 745",
        "airportDistanceKm": 7,
        "things": [
            {
                "rank": 1,
                "name": "Catedral de Santa Isabel",
                "postcode": "GQ-LB",
                "distanceKmFromAirport": 7,
                "description": "Neo-Gothic Spanish colonial cathedral from 1916 - the most striking landmark in Malabo",
                "distance": 0.2,
                "URL": "https://www.equatorial-guinea-tourism.com/"
            },
            {
                "rank": 2,
                "name": "Plaza de la Independencia",
                "postcode": "GQ-LB",
                "distanceKmFromAirport": 7,
                "description": "Central colonial square surrounded by government buildings and the Presidential Palace",
                "distance": 0.1,
                "URL": "https://www.equatorial-guinea-tourism.com/"
            },
            {
                "rank": 3,
                "name": "Malabo National Park",
                "postcode": "GQ-LB",
                "distanceKmFromAirport": 10,
                "description": "Tropical forest surrounding the city with drill monkeys and forest elephants",
                "distance": 3.0,
                "URL": "https://www.equatorial-guinea-tourism.com/"
            },
            {
                "rank": 4,
                "name": "Market & Artisans District",
                "postcode": "GQ-LB",
                "distanceKmFromAirport": 8,
                "description": "Local crafts and Fang and Bubi tribal art",
                "distance": 0.5,
                "URL": "https://www.equatorial-guinea-tourism.com/"
            },
            {
                "rank": 5,
                "name": "Pico Basile National Park",
                "postcode": "GQ-LB",
                "distanceKmFromAirport": 19,
                "description": "Hike to the 3,011m summit - the highest point in Equatorial Guinea",
                "distance": 12.0,
                "URL": "https://www.equatorial-guinea-tourism.com/"
            },
            {
                "rank": 6,
                "name": "Bioko Island Beaches",
                "postcode": "GQ-BS",
                "distanceKmFromAirport": 39,
                "description": "Turtle nesting beaches at Arena Blanca on one of Africa's most unspoilt islands",
                "distance": 32.0,
                "URL": "https://www.equatorial-guinea-tourism.com/"
            },
            {
                "rank": 7,
                "name": "Waterfall at Ureka",
                "postcode": "GQ-KS",
                "distanceKmFromAirport": 67,
                "description": "Dramatic rainforest waterfall in the wet southern tip of Bioko Island",
                "distance": 60.0,
                "URL": "https://www.equatorial-guinea-tourism.com/"
            },
            {
                "rank": 8,
                "name": "Luba Gorilla Sanctuary",
                "postcode": "GQ-LB",
                "distanceKmFromAirport": 49,
                "description": "Rescued western lowland gorillas",
                "distance": 42.0,
                "URL": "https://www.equatorial-guinea-tourism.com/"
            },
            {
                "rank": 9,
                "name": "Malabo Port",
                "postcode": "GQ-LB",
                "distanceKmFromAirport": 8,
                "description": "Historic port where Spanish colonial trade and the modern oil industry converge",
                "distance": 0.5,
                "URL": "https://www.equatorial-guinea-tourism.com/"
            },
            {
                "rank": 10,
                "name": "Sopa de Poyo (Chicken Soup)",
                "postcode": "GQ-LB",
                "distanceKmFromAirport": 8,
                "description": "Equatorial Guinean specialty - chicken and vegetable soup with plantains",
                "distance": 0.5,
                "URL": "https://www.equatorial-guinea-tourism.com/"
            }
        ]
    },
    "male": {
        "city": "Male",
        "country": "Maldives",
        "airportPostcode": "20076",
        "airportDistanceKm": 2,
        "things": [
            {
                "rank": 1,
                "name": "Overwater Bungalow Resort Stay",
                "postcode": "20026",
                "distanceKmFromAirport": 22,
                "description": "Stay in a glass-floor overwater villa above the turquoise Indian Ocean lagoon",
                "distance": 20.0,
                "URL": "https://www.visitmaldives.com/"
            },
            {
                "rank": 2,
                "name": "Manta Ray & Whale Shark Snorkelling",
                "postcode": "07020",
                "distanceKmFromAirport": 122,
                "description": "Hanifaru Bay UNESCO Biosphere Reserve - snorkel with hundreds of manta rays feeding",
                "distance": 120.0,
                "URL": "https://www.visitmaldives.com/"
            },
            {
                "rank": 3,
                "name": "Coral Reef Diving & Snorkelling",
                "postcode": "20026",
                "distanceKmFromAirport": 12,
                "description": "UNESCO-protected reefs with sea turtles, reef sharks, napoleonfish and hard corals",
                "distance": 10.0,
                "URL": "https://www.visitmaldives.com/"
            },
            {
                "rank": 4,
                "name": "Male Friday Mosque (Hukuru Miskiy)",
                "postcode": "20026",
                "distanceKmFromAirport": 2,
                "description": "17th-century coral stone mosque with intricate Arabic calligraphy and lacquer carvings",
                "distance": 0.2,
                "URL": "https://www.visitmaldives.com/"
            },
            {
                "rank": 5,
                "name": "National Museum of Maldives",
                "postcode": "20375",
                "distanceKmFromAirport": 2,
                "description": "Pre-Islamic artefacts, royal regalia and Buddhist coral stone sculptures",
                "distance": 0.3,
                "URL": "https://museum.gov.mv/"
            },
            {
                "rank": 6,
                "name": "Malé Fish Market (Local Market)",
                "postcode": "20026",
                "distanceKmFromAirport": 2,
                "description": "Dawn tuna market where fishermen bring in their catch - the heartbeat of Maldivian life",
                "distance": 0.3,
                "URL": "https://www.visitmaldives.com/"
            },
            {
                "rank": 7,
                "name": "Bioluminescent Beach",
                "postcode": "20026",
                "distanceKmFromAirport": 52,
                "description": "Night swimming where plankton light up the water with electric blue bioluminescence",
                "distance": 50.0,
                "URL": "https://www.visitmaldives.com/"
            },
            {
                "rank": 8,
                "name": "Sandbank Picnic",
                "postcode": "20026",
                "distanceKmFromAirport": 17,
                "description": "Uninhabited sandbanks only centimetres above sea level - ultimate isolation",
                "distance": 15.0,
                "URL": "https://www.visitmaldives.com/"
            },
            {
                "rank": 9,
                "name": "Sunset Dolphin Cruise",
                "postcode": "20026",
                "distanceKmFromAirport": 3,
                "description": "Spinner dolphins somersault beside the boat as the sun sets over the Indian Ocean",
                "distance": 0.5,
                "URL": "https://www.visitmaldives.com/"
            },
            {
                "rank": 10,
                "name": "Mas Huni (Tuna & Coconut Breakfast)",
                "postcode": "20026",
                "distanceKmFromAirport": 2,
                "description": "Traditional Maldivian breakfast - shredded tuna with coconut, onion and chilli on flatbread",
                "distance": 0.3,
                "URL": "https://www.visitmaldives.com/"
            }
        ]
    },
    "malmo": {
        "city": "Malmo",
        "country": "Sweden",
        "airportPostcode": "230 32",
        "airportDistanceKm": 30,
        "things": [
            {
                "rank": 1,
                "name": "Turning Torso",
                "postcode": "211 15",
                "distanceKmFromAirport": 32,
                "description": "Scandinavia's tallest building, Santiago Calatrava's iconic twisted skyscraper",
                "distance": 1.5,
                "URL": "https://www.hsvab.se/en/turning-torso/"
            },
            {
                "rank": 2,
                "name": "Western Harbour (Vastra Hamnen)",
                "postcode": "211 19",
                "distanceKmFromAirport": 32,
                "description": "Sustainable urban development showcase with striking modern architecture",
                "distance": 1.5,
                "URL": "https://malmo.se/"
            },
            {
                "rank": 3,
                "name": "Malmo Castle (Malmohus)",
                "postcode": "211 18",
                "distanceKmFromAirport": 31,
                "description": "15th-century castle housing history, art and natural history museums",
                "distance": 1.0,
                "URL": "https://malmo.se/Uppleva-och-gora/Museer-och-utstallningar/Malmo-Museum.html"
            },
            {
                "rank": 4,
                "name": "Old Town (Gamla Staden)",
                "postcode": "211 22",
                "distanceKmFromAirport": 31,
                "description": "Charming medieval core with Stortorget square and the beautifully preserved Lilla Torg",
                "distance": 0.5,
                "URL": "https://malmo.se/"
            },
            {
                "rank": 5,
                "name": "Oresund Bridge",
                "postcode": "230 32",
                "distanceKmFromAirport": 24,
                "description": "Iconic 8km bridge-tunnel connecting Malmo to Copenhagen over the Oresund strait",
                "distance": 6.0,
                "URL": "https://www.oresundsbron.com/"
            },
            {
                "rank": 6,
                "name": "Moderna Museet Malmo",
                "postcode": "211 24",
                "distanceKmFromAirport": 31,
                "description": "Satellite of Stockholm's Moderna Museet in a renovated power station",
                "distance": 1.0,
                "URL": "https://www.modernamuseet.se/malmo/en/"
            },
            {
                "rank": 7,
                "name": "Stortorget",
                "postcode": "211 22",
                "distanceKmFromAirport": 30,
                "description": "Vast market square with the statue of King Karl X Gustav and City Hall",
                "distance": 0.3,
                "URL": "https://malmo.se/"
            },
            {
                "rank": 8,
                "name": "Pildammsparken",
                "postcode": "214 21",
                "distanceKmFromAirport": 32,
                "description": "Large city park with a theatre, sculpture garden and lake",
                "distance": 2.0,
                "URL": "https://malmo.se/"
            },
            {
                "rank": 9,
                "name": "St Peter's Church",
                "postcode": "211 34",
                "distanceKmFromAirport": 30,
                "description": "Magnificent 14th-century brick Gothic church with medieval frescoes",
                "distance": 0.3,
                "URL": "https://petrikyrkan.se/"
            },
            {
                "rank": 10,
                "name": "Malmo Food Hall (Saluhallen)",
                "postcode": "211 24",
                "distanceKmFromAirport": 31,
                "description": "Historic covered market with the best of Swedish and Mediterranean produce",
                "distance": 1.0,
                "URL": "https://malmo.se/"
            }
        ]
    }
}

base_path = r"c:\Users\junkp\MagicMirror\modules\MMM-iAmGoingThere\data\attractions"

for city_file, city_data in cities_data.items():
    file_path = os.path.join(base_path, f"{city_file}.json")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(city_data, f, indent=2, ensure_ascii=False)
    
    print(f"Updated {city_file}.json")

print("\nAll cities updated successfully!")
