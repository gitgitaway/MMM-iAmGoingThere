import json
import os

base = r"C:\Users\junkp\MagicMirror\modules\MMM-iAmGoingThere\data\attractions"

cities = {
    "tampere": {
        "things": [
            {"rank": 1, "name": "Tampere Cathedral", "postcode": "33100", "distance": 0.5, "distanceKmFromAirport": 17, "URL": "https://tampereenseurakunnat.fi/"},
            {"rank": 2, "name": "Vapriikki Museum Centre", "postcode": "33210", "distance": 0.8, "distanceKmFromAirport": 17, "URL": "https://vapriikki.fi/"},
            {"rank": 3, "name": "Tampere Hall", "postcode": "33100", "distance": 1.0, "distanceKmFromAirport": 17, "URL": "https://tampere-talo.fi/"},
            {"rank": 4, "name": "Nasinneula Observation Tower", "postcode": "33230", "distance": 1.5, "distanceKmFromAirport": 18, "URL": "https://sarkanniemi.fi/nasinneula/"},
            {"rank": 5, "name": "Sarkanniemi Amusement Park", "postcode": "33230", "distance": 1.5, "distanceKmFromAirport": 18, "URL": "https://sarkanniemi.fi/"},
            {"rank": 6, "name": "Pyynikki Ridge & Observation Tower", "postcode": "33230", "distance": 2.0, "distanceKmFromAirport": 18, "URL": "https://pyynikintorni.fi/"},
            {"rank": 7, "name": "Moomin Museum", "postcode": "33100", "distance": 0.5, "distanceKmFromAirport": 17, "URL": "https://www.muumimuseo.fi/"},
            {"rank": 8, "name": "Lenin Museum", "postcode": "33200", "distance": 0.3, "distanceKmFromAirport": 16, "URL": "https://www.leninmuseo.fi/"},
            {"rank": 9, "name": "Finlayson Factory Area", "postcode": "33210", "distance": 0.5, "distanceKmFromAirport": 16, "URL": "https://finlayson.fi/"},
            {"rank": 10, "name": "Laukontori Harbour", "postcode": "33200", "distance": 1.0, "distanceKmFromAirport": 17, "URL": "https://www.tampere.fi/"},
        ]
    },
    "tangier": {
        "things": [
            {"rank": 1, "name": "Kasbah Museum (Dar al Makhzen)", "postcode": "90000", "distance": 0.3, "distanceKmFromAirport": 15, "URL": "https://www.moroccanmuseums.ma/"},
            {"rank": 2, "name": "Cap Spartel & Hercules Cave", "postcode": "90000", "distance": 13.0, "distanceKmFromAirport": 20, "URL": ""},
            {"rank": 3, "name": "Grand Socco & Petit Socco", "postcode": "90000", "distance": 0.2, "distanceKmFromAirport": 15, "URL": ""},
            {"rank": 4, "name": "Medina Walking Tour", "postcode": "90000", "distance": 0.3, "distanceKmFromAirport": 15, "URL": ""},
            {"rank": 5, "name": "American Legation Museum", "postcode": "90000", "distance": 0.4, "distanceKmFromAirport": 15, "URL": "https://www.legation.org/"},
            {"rank": 6, "name": "Cafe Hafa (1921)", "postcode": "90000", "distance": 1.5, "distanceKmFromAirport": 16, "URL": ""},
            {"rank": 7, "name": "Museum of Contemporary Art of Tangier", "postcode": "90000", "distance": 0.5, "distanceKmFromAirport": 15, "URL": ""},
            {"rank": 8, "name": "Ferry to Spain (Algeciras/Tarifa)", "postcode": "90000", "distance": 2.0, "distanceKmFromAirport": 14, "URL": "https://www.frs.es/"},
            {"rank": 9, "name": "Chefchaouen Day Trip", "postcode": "91000", "distance": 115.0, "distanceKmFromAirport": 120, "URL": ""},
            {"rank": 10, "name": "Tagine at Dar Nour", "postcode": "90000", "distance": 0.3, "distanceKmFromAirport": 15, "URL": "https://www.darnour.com/"},
        ]
    },
    "tarawa": {
        "things": [
            {"rank": 1, "name": "Battle of Tarawa WWII Sites", "postcode": "", "distance": 3.0, "distanceKmFromAirport": 4, "URL": ""},
            {"rank": 2, "name": "Betio WWII Museum", "postcode": "", "distance": 4.0, "distanceKmFromAirport": 5, "URL": ""},
            {"rank": 3, "name": "Ambo Island Causeway Drive", "postcode": "", "distance": 5.0, "distanceKmFromAirport": 6, "URL": ""},
            {"rank": 4, "name": "Traditional Maneaba Meeting House", "postcode": "", "distance": 1.0, "distanceKmFromAirport": 2, "URL": ""},
            {"rank": 5, "name": "Lagoon Fishing", "postcode": "", "distance": 1.0, "distanceKmFromAirport": 2, "URL": ""},
            {"rank": 6, "name": "Te Umanibong Museum", "postcode": "", "distance": 2.0, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 7, "name": "Bairiki National Stadium", "postcode": "", "distance": 1.0, "distanceKmFromAirport": 2, "URL": ""},
            {"rank": 8, "name": "Buota Village Traditional Fishing", "postcode": "", "distance": 8.0, "distanceKmFromAirport": 9, "URL": ""},
            {"rank": 9, "name": "Nanikai Beach", "postcode": "", "distance": 3.0, "distanceKmFromAirport": 4, "URL": ""},
            {"rank": 10, "name": "Toddy (Palm Wine) Tapping", "postcode": "", "distance": 2.0, "distanceKmFromAirport": 3, "URL": ""},
        ]
    },
    "tashkent": {
        "things": [
            {"rank": 1, "name": "Khast Imam Complex (Hazrati Imam)", "postcode": "100011", "distance": 1.5, "distanceKmFromAirport": 14, "URL": "https://hastimom.uz/"},
            {"rank": 2, "name": "Chorsu Bazaar", "postcode": "100017", "distance": 1.0, "distanceKmFromAirport": 14, "URL": ""},
            {"rank": 3, "name": "Independence Square (Mustaqillik Maydoni)", "postcode": "100029", "distance": 0.5, "distanceKmFromAirport": 13, "URL": ""},
            {"rank": 4, "name": "Museum of Applied Arts", "postcode": "100047", "distance": 1.5, "distanceKmFromAirport": 14, "URL": ""},
            {"rank": 5, "name": "Amir Timur Museum", "postcode": "100029", "distance": 0.3, "distanceKmFromAirport": 13, "URL": "https://amirtimurmuseum.uz/"},
            {"rank": 6, "name": "Tashkent Metro", "postcode": "100000", "distance": 0.0, "distanceKmFromAirport": 13, "URL": "https://metro.tashkent.uz/"},
            {"rank": 7, "name": "Old City (Eski Shahar)", "postcode": "100017", "distance": 1.0, "distanceKmFromAirport": 14, "URL": ""},
            {"rank": 8, "name": "Samarkand Day Trip", "postcode": "140100", "distance": 270.0, "distanceKmFromAirport": 275, "URL": "https://samarkandtourism.uz/"},
            {"rank": 9, "name": "Alisher Navoi Opera Theatre", "postcode": "100047", "distance": 0.5, "distanceKmFromAirport": 13, "URL": "https://gabt.uz/"},
            {"rank": 10, "name": "Tashkentland Amusement Park", "postcode": "100029", "distance": 1.5, "distanceKmFromAirport": 14, "URL": ""},
        ]
    },
    "tbilisi": {
        "things": [
            {"rank": 1, "name": "Old Town (Abanotubani Sulphur Baths)", "postcode": "0105", "distance": 1.0, "distanceKmFromAirport": 19, "URL": "https://www.tbilisi.gov.ge/"},
            {"rank": 2, "name": "Narikala Fortress", "postcode": "0105", "distance": 1.2, "distanceKmFromAirport": 19, "URL": ""},
            {"rank": 3, "name": "Mtatsminda Park & Funicular", "postcode": "0179", "distance": 1.5, "distanceKmFromAirport": 19, "URL": "https://funicular.ge/"},
            {"rank": 4, "name": "Georgian National Museum", "postcode": "0108", "distance": 0.8, "distanceKmFromAirport": 19, "URL": "https://museum.ge/"},
            {"rank": 5, "name": "Sioni Cathedral", "postcode": "0105", "distance": 0.5, "distanceKmFromAirport": 18, "URL": ""},
            {"rank": 6, "name": "Rustaveli Avenue", "postcode": "0108", "distance": 0.5, "distanceKmFromAirport": 18, "URL": ""},
            {"rank": 7, "name": "Kazbegi National Park Day Trip", "postcode": "4700", "distance": 148.0, "distanceKmFromAirport": 155, "URL": "https://apa.gov.ge/"},
            {"rank": 8, "name": "Georgian Wine & Qvevri Wine Tourism", "postcode": "1200", "distance": 80.0, "distanceKmFromAirport": 90, "URL": "https://gnta.ge/"},
            {"rank": 9, "name": "Peace Bridge", "postcode": "0105", "distance": 0.3, "distanceKmFromAirport": 18, "URL": ""},
            {"rank": 10, "name": "Fabrika", "postcode": "0102", "distance": 1.0, "distanceKmFromAirport": 18, "URL": "https://fabrika.ge/"},
        ]
    },
    "tegucigalpa": {
        "things": [
            {"rank": 1, "name": "Copan Ruins", "postcode": "70600", "distance": 220.0, "distanceKmFromAirport": 225, "URL": "https://www.copanhonduras.org/"},
            {"rank": 2, "name": "Valle de Angeles Craft Village", "postcode": "11201", "distance": 22.0, "distanceKmFromAirport": 25, "URL": ""},
            {"rank": 3, "name": "National Museum of Honduras", "postcode": "11101", "distance": 0.5, "distanceKmFromAirport": 6, "URL": "https://www.iahcula.edu.hn/"},
            {"rank": 4, "name": "La Tigra Cloud Forest", "postcode": "11101", "distance": 22.0, "distanceKmFromAirport": 25, "URL": ""},
            {"rank": 5, "name": "Parque La Leona", "postcode": "11101", "distance": 1.0, "distanceKmFromAirport": 7, "URL": ""},
            {"rank": 6, "name": "Virgen de Suyapa Basilica", "postcode": "11101", "distance": 4.5, "distanceKmFromAirport": 8, "URL": ""},
            {"rank": 7, "name": "Central Park & Cathedral", "postcode": "11101", "distance": 0.2, "distanceKmFromAirport": 6, "URL": ""},
            {"rank": 8, "name": "Bay Islands Diving (Roatan)", "postcode": "34201", "distance": 300.0, "distanceKmFromAirport": 300, "URL": "https://www.roatanonline.com/"},
            {"rank": 9, "name": "Mercado San Isidro", "postcode": "11101", "distance": 0.8, "distanceKmFromAirport": 6, "URL": ""},
            {"rank": 10, "name": "Baleada", "postcode": "11101", "distance": 0.0, "distanceKmFromAirport": 6, "URL": ""},
        ]
    },
    "tehran": {
        "things": [
            {"rank": 1, "name": "Golestan Palace", "postcode": "1114913321", "distance": 1.0, "distanceKmFromAirport": 36, "URL": "https://golestanpalace.ir/"},
            {"rank": 2, "name": "National Museum of Iran", "postcode": "1136613111", "distance": 1.2, "distanceKmFromAirport": 36, "URL": "https://www.irannationalmuseum.ir/"},
            {"rank": 3, "name": "Milad Tower", "postcode": "1461967111", "distance": 8.0, "distanceKmFromAirport": 43, "URL": "https://www.miladtower.com/"},
            {"rank": 4, "name": "Grand Bazaar of Tehran", "postcode": "1131813111", "distance": 1.5, "distanceKmFromAirport": 36, "URL": ""},
            {"rank": 5, "name": "Tabiat Bridge", "postcode": "1415893111", "distance": 6.0, "distanceKmFromAirport": 41, "URL": ""},
            {"rank": 6, "name": "Sa'dabad Palace Complex", "postcode": "1983836641", "distance": 14.0, "distanceKmFromAirport": 49, "URL": "https://sadabadpalace.ir/"},
            {"rank": 7, "name": "Niavaran Palace Complex", "postcode": "1968963111", "distance": 12.0, "distanceKmFromAirport": 47, "URL": "https://niavarancollection.ir/"},
            {"rank": 8, "name": "Tehran Museum of Contemporary Art", "postcode": "1415893111", "distance": 5.0, "distanceKmFromAirport": 40, "URL": "https://www.tmoca.com/"},
            {"rank": 9, "name": "Darband Mountain Trail", "postcode": "1994614111", "distance": 15.0, "distanceKmFromAirport": 50, "URL": ""},
            {"rank": 10, "name": "Carpet Museum of Iran", "postcode": "1415893111", "distance": 5.5, "distanceKmFromAirport": 40, "URL": "https://icm.ir/"},
        ]
    },
    "tirana": {
        "things": [
            {"rank": 1, "name": "Skanderbeg Square", "postcode": "1001", "distance": 0.0, "distanceKmFromAirport": 24, "URL": ""},
            {"rank": 2, "name": "National History Museum", "postcode": "1001", "distance": 0.1, "distanceKmFromAirport": 24, "URL": "https://www.mhk.al/"},
            {"rank": 3, "name": "Bunk'Art 2", "postcode": "1001", "distance": 0.5, "distanceKmFromAirport": 25, "URL": "https://bunkart.al/"},
            {"rank": 4, "name": "Et'hem Bey Mosque", "postcode": "1001", "distance": 0.1, "distanceKmFromAirport": 24, "URL": ""},
            {"rank": 5, "name": "Pazari i Ri (New Bazaar)", "postcode": "1001", "distance": 0.5, "distanceKmFromAirport": 24, "URL": ""},
            {"rank": 6, "name": "Pyramid of Tirana", "postcode": "1001", "distance": 0.3, "distanceKmFromAirport": 24, "URL": ""},
            {"rank": 7, "name": "Dajti Mountain & Cable Car", "postcode": "1052", "distance": 10.0, "distanceKmFromAirport": 30, "URL": "https://www.dajtiekspres.com/"},
            {"rank": 8, "name": "National Art Gallery", "postcode": "1001", "distance": 0.3, "distanceKmFromAirport": 24, "URL": "https://www.gak.al/"},
            {"rank": 9, "name": "Artificial Lake Park (Parku i Liqenit)", "postcode": "1016", "distance": 2.5, "distanceKmFromAirport": 26, "URL": ""},
            {"rank": 10, "name": "Bunk'Art 1", "postcode": "1001", "distance": 5.0, "distanceKmFromAirport": 28, "URL": "https://bunkart.al/"},
        ]
    },
    "tivat": {
        "things": [
            {"rank": 1, "name": "Porto Montenegro", "postcode": "85320", "distance": 0.5, "distanceKmFromAirport": 3, "URL": "https://www.portomontenegro.com/"},
            {"rank": 2, "name": "Bay of Kotor (Boka Kotorska)", "postcode": "85320", "distance": 0.0, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 3, "name": "Kotor Old Town", "postcode": "85330", "distance": 10.0, "distanceKmFromAirport": 10, "URL": "https://www.kotor.travel/"},
            {"rank": 4, "name": "Our Lady of the Rocks", "postcode": "85340", "distance": 15.0, "distanceKmFromAirport": 15, "URL": ""},
            {"rank": 5, "name": "Lustica Peninsula", "postcode": "85320", "distance": 8.0, "distanceKmFromAirport": 8, "URL": ""},
            {"rank": 6, "name": "Buket Fortress", "postcode": "85320", "distance": 1.0, "distanceKmFromAirport": 4, "URL": ""},
            {"rank": 7, "name": "Perast", "postcode": "85335", "distance": 17.0, "distanceKmFromAirport": 18, "URL": "https://www.perast.com/"},
            {"rank": 8, "name": "St George Island", "postcode": "85335", "distance": 17.0, "distanceKmFromAirport": 18, "URL": ""},
            {"rank": 9, "name": "Tivat Promenade & Beaches", "postcode": "85320", "distance": 0.3, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 10, "name": "Kalimanj Cemetery", "postcode": "85320", "distance": 1.0, "distanceKmFromAirport": 4, "URL": ""},
        ]
    },
    "toulouse": {
        "things": [
            {"rank": 1, "name": "Cite de l'Espace", "postcode": "31400", "distance": 5.0, "distanceKmFromAirport": 15, "URL": "https://www.cite-espace.com/"},
            {"rank": 2, "name": "Basilique Saint-Sernin", "postcode": "31000", "distance": 0.5, "distanceKmFromAirport": 11, "URL": "https://www.basilique-saint-sernin.fr/"},
            {"rank": 3, "name": "Capitole de Toulouse", "postcode": "31000", "distance": 0.2, "distanceKmFromAirport": 11, "URL": "https://www.toulouse.fr/"},
            {"rank": 4, "name": "Les Jacobins", "postcode": "31000", "distance": 0.3, "distanceKmFromAirport": 11, "URL": "https://www.jacobins.toulouse.fr/"},
            {"rank": 5, "name": "Musee des Augustins", "postcode": "31000", "distance": 0.4, "distanceKmFromAirport": 11, "URL": "https://www.augustins.org/"},
            {"rank": 6, "name": "Canal du Midi", "postcode": "31000", "distance": 1.5, "distanceKmFromAirport": 12, "URL": "https://www.canal-du-midi.org/"},
            {"rank": 7, "name": "Aeroscopia", "postcode": "31700", "distance": 11.0, "distanceKmFromAirport": 2, "URL": "https://www.musee-aeroscopia.fr/"},
            {"rank": 8, "name": "Prairie des Filtres", "postcode": "31000", "distance": 0.5, "distanceKmFromAirport": 11, "URL": ""},
            {"rank": 9, "name": "Musee Saint-Raymond", "postcode": "31000", "distance": 0.4, "distanceKmFromAirport": 11, "URL": "https://saintraymond.toulouse.fr/"},
            {"rank": 10, "name": "Victor Hugo Market", "postcode": "31000", "distance": 0.3, "distanceKmFromAirport": 11, "URL": "https://www.marchevictorhugo.fr/"},
        ]
    },
    "treviso": {
        "things": [
            {"rank": 1, "name": "Piazza dei Signori", "postcode": "31100", "distance": 0.2, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 2, "name": "Cathedral of San Pietro", "postcode": "31100", "distance": 0.3, "distanceKmFromAirport": 3, "URL": "https://www.diocesitv.it/"},
            {"rank": 3, "name": "Calmaggiore", "postcode": "31100", "distance": 0.2, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 4, "name": "Medieval Walls & Canals", "postcode": "31100", "distance": 0.5, "distanceKmFromAirport": 4, "URL": ""},
            {"rank": 5, "name": "Fishmarket Island (Pescheria)", "postcode": "31100", "distance": 0.4, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 6, "name": "Museo di Santa Caterina", "postcode": "31100", "distance": 0.5, "distanceKmFromAirport": 4, "URL": "https://www.museicivicitreviso.it/"},
            {"rank": 7, "name": "Museo Bailo", "postcode": "31100", "distance": 0.3, "distanceKmFromAirport": 3, "URL": "https://www.museicivicitreviso.it/"},
            {"rank": 8, "name": "Prosecco Road", "postcode": "31015", "distance": 30.0, "distanceKmFromAirport": 30, "URL": "https://www.coneglianovaldobbiadene.it/"},
            {"rank": 9, "name": "Buranelli Canal", "postcode": "31100", "distance": 0.3, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 10, "name": "Treviso Craft Beer Scene", "postcode": "31100", "distance": 0.5, "distanceKmFromAirport": 4, "URL": ""},
        ]
    },
    "tripoli": {
        "things": [
            {"rank": 1, "name": "Leptis Magna", "postcode": "21310", "distance": 130.0, "distanceKmFromAirport": 155, "URL": ""},
            {"rank": 2, "name": "Sabrata Roman Theatre", "postcode": "21020", "distance": 70.0, "distanceKmFromAirport": 70, "URL": ""},
            {"rank": 3, "name": "Medina of Tripoli (Old City)", "postcode": "21301", "distance": 0.5, "distanceKmFromAirport": 35, "URL": ""},
            {"rank": 4, "name": "Saraya (Red Castle) Museum", "postcode": "21301", "distance": 0.3, "distanceKmFromAirport": 35, "URL": ""},
            {"rank": 5, "name": "Marcus Aurelius Arch", "postcode": "21301", "distance": 0.3, "distanceKmFromAirport": 35, "URL": ""},
            {"rank": 6, "name": "Gurgi Mosque", "postcode": "21301", "distance": 0.4, "distanceKmFromAirport": 35, "URL": ""},
            {"rank": 7, "name": "Ghadames Old Town (Oasis City)", "postcode": "21200", "distance": 570.0, "distanceKmFromAirport": 595, "URL": ""},
            {"rank": 8, "name": "Wadi el-Hitan (Valley of Whales) Day Trip", "postcode": "21301", "distance": 300.0, "distanceKmFromAirport": 325, "URL": ""},
            {"rank": 9, "name": "Green Square (Martyrs' Square)", "postcode": "21301", "distance": 0.2, "distanceKmFromAirport": 35, "URL": ""},
            {"rank": 10, "name": "Bazin (Semolina Bread)", "postcode": "21301", "distance": 0.0, "distanceKmFromAirport": 35, "URL": ""},
        ]
    },
    "trondheim": {
        "things": [
            {"rank": 1, "name": "Nidaros Cathedral", "postcode": "7013", "distance": 0.5, "distanceKmFromAirport": 35, "URL": "https://www.nidarosdomen.no/"},
            {"rank": 2, "name": "Nidelva Riverside", "postcode": "7010", "distance": 0.5, "distanceKmFromAirport": 35, "URL": ""},
            {"rank": 3, "name": "Archbishop's Palace Museum", "postcode": "7013", "distance": 0.5, "distanceKmFromAirport": 35, "URL": "https://www.erkebispegarden.no/"},
            {"rank": 4, "name": "Rockheim", "postcode": "7010", "distance": 1.0, "distanceKmFromAirport": 36, "URL": "https://www.rockheim.no/"},
            {"rank": 5, "name": "Stiftsgarden", "postcode": "7013", "distance": 0.3, "distanceKmFromAirport": 35, "URL": "https://www.royalcourt.no/"},
            {"rank": 6, "name": "Munkholmen Island", "postcode": "7010", "distance": 2.0, "distanceKmFromAirport": 37, "URL": ""},
            {"rank": 7, "name": "Kristiansten Fortress", "postcode": "7014", "distance": 1.0, "distanceKmFromAirport": 36, "URL": ""},
            {"rank": 8, "name": "Trondheim Art Museum", "postcode": "7012", "distance": 0.8, "distanceKmFromAirport": 35, "URL": "https://www.kunstmuseum.no/"},
            {"rank": 9, "name": "NTNU University Museum", "postcode": "7012", "distance": 1.0, "distanceKmFromAirport": 36, "URL": "https://www.ntnu.edu/museum"},
            {"rank": 10, "name": "Ravnkloa Fish Market", "postcode": "7010", "distance": 1.0, "distanceKmFromAirport": 36, "URL": ""},
        ]
    },
    "tunis": {
        "things": [
            {"rank": 1, "name": "Tunis Medina", "postcode": "1006", "distance": 0.5, "distanceKmFromAirport": 8, "URL": "https://www.tourismtunisia.com/"},
            {"rank": 2, "name": "Carthage Archaeological Site", "postcode": "2016", "distance": 15.0, "distanceKmFromAirport": 12, "URL": "https://www.amvppc.com.tn/"},
            {"rank": 3, "name": "Bardo National Museum", "postcode": "2000", "distance": 5.0, "distanceKmFromAirport": 12, "URL": "https://www.bardomuseum.tn/"},
            {"rank": 4, "name": "Sidi Bou Said", "postcode": "2026", "distance": 20.0, "distanceKmFromAirport": 16, "URL": ""},
            {"rank": 5, "name": "Souq of the Chechias (Hat Makers)", "postcode": "1008", "distance": 0.5, "distanceKmFromAirport": 8, "URL": ""},
            {"rank": 6, "name": "Dar Ben Abdallah Museum", "postcode": "1006", "distance": 0.5, "distanceKmFromAirport": 8, "URL": ""},
            {"rank": 7, "name": "Avenue Habib Bourguiba", "postcode": "1001", "distance": 0.3, "distanceKmFromAirport": 8, "URL": ""},
            {"rank": 8, "name": "Dougga Roman Ruins", "postcode": "9100", "distance": 110.0, "distanceKmFromAirport": 116, "URL": ""},
            {"rank": 9, "name": "Belvedere Park & Modern Art Museum", "postcode": "1002", "distance": 2.0, "distanceKmFromAirport": 9, "URL": ""},
            {"rank": 10, "name": "Lablabi Chickpea Soup", "postcode": "1006", "distance": 0.5, "distanceKmFromAirport": 8, "URL": ""},
        ]
    },
    "turku": {
        "things": [
            {"rank": 1, "name": "Turku Castle", "postcode": "20100", "distance": 2.0, "distanceKmFromAirport": 8, "URL": "https://www.turku.fi/en/turku-castle"},
            {"rank": 2, "name": "Turku Cathedral", "postcode": "20500", "distance": 0.5, "distanceKmFromAirport": 8, "URL": "https://www.turkuseurakunnat.fi/"},
            {"rank": 3, "name": "Aboa Vetus & Ars Nova", "postcode": "20100", "distance": 0.8, "distanceKmFromAirport": 8, "URL": "https://www.aboavetusarsnova.fi/"},
            {"rank": 4, "name": "Turku Art Museum", "postcode": "20100", "distance": 1.0, "distanceKmFromAirport": 9, "URL": "https://www.turuntaidemuseo.fi/"},
            {"rank": 5, "name": "Forum Marinum", "postcode": "20100", "distance": 2.0, "distanceKmFromAirport": 9, "URL": "https://www.forum-marinum.fi/"},
            {"rank": 6, "name": "Luostarinmaki Handicrafts Museum", "postcode": "20700", "distance": 1.5, "distanceKmFromAirport": 9, "URL": "https://www.turku.fi/en/luostarinmaki"},
            {"rank": 7, "name": "Turku Market Square", "postcode": "20100", "distance": 0.5, "distanceKmFromAirport": 8, "URL": ""},
            {"rank": 8, "name": "Archipelago National Park", "postcode": "21600", "distance": 25.0, "distanceKmFromAirport": 30, "URL": "https://www.nationalparks.fi/archipelagonp"},
            {"rank": 9, "name": "Old Great Square (Vanha Suurtori)", "postcode": "20500", "distance": 0.3, "distanceKmFromAirport": 8, "URL": ""},
            {"rank": 10, "name": "Ruissalo Island", "postcode": "20100", "distance": 5.0, "distanceKmFromAirport": 10, "URL": "https://www.turku.fi/en/ruissalo"},
        ]
    },
}

lookup = {city: {t["rank"]: t for t in data["things"]} for city, data in cities.items()}

for city_name, new_data in cities.items():
    filepath = os.path.join(base, f"{city_name}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        original = json.load(f)

    rank_lookup = {t["rank"]: t for t in new_data["things"]}

    updated_things = []
    for thing in original["things"]:
        rank = thing["rank"]
        patch = rank_lookup.get(rank, {})
        updated = {
            "rank": thing["rank"],
            "name": thing["name"],
            "postcode": patch.get("postcode", thing.get("postcode", "")),
            "distanceKmFromAirport": patch.get("distanceKmFromAirport", thing.get("distanceKmFromAirport", None)),
            "description": thing["description"],
            "distance": patch.get("distance", thing.get("distance", None)),
            "URL": patch.get("URL", thing.get("URL", "")),
        }
        updated_things.append(updated)

    original["things"] = updated_things

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(original, f, indent=2, ensure_ascii=False)

    print(f"Updated {city_name}.json")

print("All done!")
