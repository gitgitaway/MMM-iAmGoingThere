import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

updates = {
    "pune": {
        "attractions": [
            {"rank": 1, "postcode": "411002", "distance": 2.0, "distanceKmFromAirport": 11, "URL": "https://www.shaniwadwada.in"},
            {"rank": 2, "postcode": "411006", "distance": 4.0, "distanceKmFromAirport": 13, "URL": "https://www.agakhanpalacepune.org"},
            {"rank": 3, "postcode": "412301", "distance": 25.0, "distanceKmFromAirport": 34, "URL": "https://www.maharashtratourism.gov.in"},
            {"rank": 4, "postcode": "411001", "distance": 4.0, "distanceKmFromAirport": 13, "URL": "https://www.osho.com"},
            {"rank": 5, "postcode": "411004", "distance": 2.0, "distanceKmFromAirport": 11, "URL": "https://www.punetourism.gov.in"},
            {"rank": 6, "postcode": "411001", "distance": 4.0, "distanceKmFromAirport": 13, "URL": "https://www.koregaonpark.info"},
            {"rank": 7, "postcode": "411038", "distance": 6.0, "distanceKmFromAirport": 14, "URL": "https://www.sndt.ac.in"},
            {"rank": 8, "postcode": "411002", "distance": 2.0, "distanceKmFromAirport": 11, "URL": "https://www.rajakelkarmuseum.com"},
            {"rank": 9, "postcode": "411001", "distance": 2.0, "distanceKmFromAirport": 11, "URL": "https://www.irctc.co.in"},
            {"rank": 10, "postcode": "411002", "distance": 2.0, "distanceKmFromAirport": 11, "URL": "https://www.bedekar.com"},
        ]
    },
    "punta_arenas": {
        "attractions": [
            {"rank": 1, "postcode": "6280000", "distance": 250.0, "distanceKmFromAirport": 265, "URL": "https://www.torresdelpaine.com"},
            {"rank": 2, "postcode": "6200000", "distance": 35.0, "distanceKmFromAirport": 52, "URL": "https://www.turismomagallanes.cl"},
            {"rank": 3, "postcode": "6200000", "distance": 1.0, "distanceKmFromAirport": 20, "URL": "https://www.turismomagallanes.cl"},
            {"rank": 4, "postcode": "6200000", "distance": 0.5, "distanceKmFromAirport": 20, "URL": "https://www.turismomagallanes.cl"},
            {"rank": 5, "postcode": "6200000", "distance": 1.5, "distanceKmFromAirport": 21, "URL": "https://www.turismomagallanes.cl"},
            {"rank": 6, "postcode": "6300000", "distance": 400.0, "distanceKmFromAirport": 419, "URL": "https://www.turismomagallanes.cl"},
            {"rank": 7, "postcode": "9410000", "distance": 310.0, "distanceKmFromAirport": 329, "URL": "https://www.parquesnacionales.gob.ar"},
            {"rank": 8, "postcode": "6200000", "distance": 24.0, "distanceKmFromAirport": 40, "URL": "https://www.turismomagallanes.cl"},
            {"rank": 9, "postcode": "6200000", "distance": 1.0, "distanceKmFromAirport": 20, "URL": "https://www.turismomagallanes.cl"},
            {"rank": 10, "postcode": "6200000", "distance": 1.0, "distanceKmFromAirport": 20, "URL": "https://www.turismomagallanes.cl"},
        ]
    },
    "punta_cana": {
        "attractions": [
            {"rank": 1, "postcode": "23301", "distance": 5.0, "distanceKmFromAirport": 28, "URL": "https://www.bavaro.do"},
            {"rank": 2, "postcode": "22000", "distance": 95.0, "distanceKmFromAirport": 117, "URL": "https://www.islasaona.com"},
            {"rank": 3, "postcode": "23301", "distance": 40.0, "distanceKmFromAirport": 62, "URL": "https://www.iguanamaniahoyo.com"},
            {"rank": 4, "postcode": "23301", "distance": 15.0, "distanceKmFromAirport": 38, "URL": "https://www.ziplinepuntacana.com"},
            {"rank": 5, "postcode": "23301", "distance": 5.0, "distanceKmFromAirport": 28, "URL": "https://www.puntacanatours.com"},
            {"rank": 6, "postcode": "23301", "distance": 10.0, "distanceKmFromAirport": 33, "URL": "https://www.buggieespuntacana.com"},
            {"rank": 7, "postcode": "23301", "distance": 15.0, "distanceKmFromAirport": 38, "URL": "https://www.manateelagon.com"},
            {"rank": 8, "postcode": "22000", "distance": 100.0, "distanceKmFromAirport": 122, "URL": "https://www.casadecampo.com.do"},
            {"rank": 9, "postcode": "23301", "distance": 8.0, "distanceKmFromAirport": 18, "URL": "https://www.capcana.com"},
            {"rank": 10, "postcode": "23301", "distance": 0.5, "distanceKmFromAirport": 25, "URL": "https://www.drinksmama.com"},
        ]
    },
    "pyongyang": {
        "attractions": [
            {"rank": 1, "postcode": "999091", "distance": 5.0, "distanceKmFromAirport": 28, "URL": "https://www.kcna.co.kp"},
            {"rank": 2, "postcode": "999091", "distance": 1.0, "distanceKmFromAirport": 24, "URL": "https://www.kcna.co.kp"},
            {"rank": 3, "postcode": "999091", "distance": 1.0, "distanceKmFromAirport": 24, "URL": "https://www.kcna.co.kp"},
            {"rank": 4, "postcode": "999091", "distance": 0.5, "distanceKmFromAirport": 24, "URL": "https://www.kcna.co.kp"},
            {"rank": 5, "postcode": "999091", "distance": 1.0, "distanceKmFromAirport": 24, "URL": "https://www.kcna.co.kp"},
            {"rank": 6, "postcode": "999091", "distance": 2.0, "distanceKmFromAirport": 25, "URL": "https://www.kcna.co.kp"},
            {"rank": 7, "postcode": "999091", "distance": 3.0, "distanceKmFromAirport": 26, "URL": "https://www.kcna.co.kp"},
            {"rank": 8, "postcode": "999091", "distance": 12.0, "distanceKmFromAirport": 34, "URL": "https://www.kcna.co.kp"},
            {"rank": 9, "postcode": "999161", "distance": 170.0, "distanceKmFromAirport": 189, "URL": "https://www.kcna.co.kp"},
            {"rank": 10, "postcode": "999091", "distance": 0.5, "distanceKmFromAirport": 24, "URL": "https://www.kcna.co.kp"},
        ]
    },
    "qingdao": {
        "attractions": [
            {"rank": 1, "postcode": "266031", "distance": 5.0, "distanceKmFromAirport": 34, "URL": "https://www.tsingtaobeerfestival.com"},
            {"rank": 2, "postcode": "266003", "distance": 4.0, "distanceKmFromAirport": 33, "URL": "https://www.qingdaotourism.gov.cn"},
            {"rank": 3, "postcode": "266071", "distance": 8.0, "distanceKmFromAirport": 37, "URL": "https://www.qingdaosailingcentre.com"},
            {"rank": 4, "postcode": "266003", "distance": 3.0, "distanceKmFromAirport": 32, "URL": "https://www.qingdaotourism.gov.cn"},
            {"rank": 5, "postcode": "266023", "distance": 5.0, "distanceKmFromAirport": 34, "URL": "https://www.tsingtaomuseum.com"},
            {"rank": 6, "postcode": "266100", "distance": 30.0, "distanceKmFromAirport": 30, "URL": "https://www.qingdaotourism.gov.cn"},
            {"rank": 7, "postcode": "266001", "distance": 1.0, "distanceKmFromAirport": 30, "URL": "https://www.qingdaotourism.gov.cn"},
            {"rank": 8, "postcode": "266003", "distance": 5.0, "distanceKmFromAirport": 34, "URL": "https://www.qingdaotourism.gov.cn"},
            {"rank": 9, "postcode": "266003", "distance": 4.0, "distanceKmFromAirport": 33, "URL": "https://www.qingdaoaquarium.com"},
            {"rank": 10, "postcode": "266002", "distance": 6.0, "distanceKmFromAirport": 35, "URL": "https://www.qingdaotourism.gov.cn"},
        ]
    },
    "quito": {
        "attractions": [
            {"rank": 1, "postcode": "170150", "distance": 0.5, "distanceKmFromAirport": 37, "URL": "https://www.quito.com.ec"},
            {"rank": 2, "postcode": "170902", "distance": 22.0, "distanceKmFromAirport": 28, "URL": "https://www.mitaddelmundo.com"},
            {"rank": 3, "postcode": "170001", "distance": 1000.0, "distanceKmFromAirport": 1035, "URL": "https://www.galapagos.org"},
            {"rank": 4, "postcode": "170150", "distance": 5.0, "distanceKmFromAirport": 41, "URL": "https://www.teleferico.com.ec"},
            {"rank": 5, "postcode": "170150", "distance": 0.3, "distanceKmFromAirport": 37, "URL": "https://www.iglesialcompania.org"},
            {"rank": 6, "postcode": "050150", "distance": 75.0, "distanceKmFromAirport": 106, "URL": "https://www.ecuadorgreen.com"},
            {"rank": 7, "postcode": "100201", "distance": 95.0, "distanceKmFromAirport": 118, "URL": "https://www.otavalomarket.com"},
            {"rank": 8, "postcode": "170150", "distance": 0.5, "distanceKmFromAirport": 37, "URL": "https://www.quito.com.ec"},
            {"rank": 9, "postcode": "220001", "distance": 250.0, "distanceKmFromAirport": 282, "URL": "https://www.yasuni.org"},
            {"rank": 10, "postcode": "170150", "distance": 0.5, "distanceKmFromAirport": 37, "URL": "https://www.quito.com.ec"},
        ]
    },
    "rabat": {
        "attractions": [
            {"rank": 1, "postcode": "10000", "distance": 1.0, "distanceKmFromAirport": 12, "URL": "https://www.rabattourisme.ma"},
            {"rank": 2, "postcode": "10000", "distance": 1.5, "distanceKmFromAirport": 13, "URL": "https://www.culturegouvma.org"},
            {"rank": 3, "postcode": "10000", "distance": 2.0, "distanceKmFromAirport": 13, "URL": "https://www.culturegouvma.org"},
            {"rank": 4, "postcode": "10000", "distance": 1.5, "distanceKmFromAirport": 13, "URL": "https://www.mmc.ma"},
            {"rank": 5, "postcode": "10020", "distance": 1.0, "distanceKmFromAirport": 12, "URL": "https://www.culturegouvma.org"},
            {"rank": 6, "postcode": "11000", "distance": 4.0, "distanceKmFromAirport": 15, "URL": "https://www.saletourisme.ma"},
            {"rank": 7, "postcode": "10010", "distance": 0.5, "distanceKmFromAirport": 12, "URL": "https://www.rabattourisme.ma"},
            {"rank": 8, "postcode": "10000", "distance": 1.5, "distanceKmFromAirport": 13, "URL": "https://www.culturegouvma.org"},
            {"rank": 9, "postcode": "10000", "distance": 1.0, "distanceKmFromAirport": 12, "URL": "https://www.culturegouvma.org"},
            {"rank": 10, "postcode": "10000", "distance": 1.0, "distanceKmFromAirport": 12, "URL": "https://www.rabattourisme.ma"},
        ]
    },
    "reus": {
        "attractions": [
            {"rank": 1, "postcode": "43201", "distance": 0.3, "distanceKmFromAirport": 3, "URL": "https://www.gaudicentre.cat"},
            {"rank": 2, "postcode": "43201", "distance": 0.5, "distanceKmFromAirport": 3, "URL": "https://www.visit.reus.cat"},
            {"rank": 3, "postcode": "43201", "distance": 0.3, "distanceKmFromAirport": 3, "URL": "https://www.casanavas.org"},
            {"rank": 4, "postcode": "43201", "distance": 0.2, "distanceKmFromAirport": 3, "URL": "https://www.visit.reus.cat"},
            {"rank": 5, "postcode": "43201", "distance": 0.4, "distanceKmFromAirport": 3, "URL": "https://www.museudereus.cat"},
            {"rank": 6, "postcode": "43201", "distance": 0.3, "distanceKmFromAirport": 3, "URL": "https://www.iglesiesantpere.cat"},
            {"rank": 7, "postcode": "43201", "distance": 0.3, "distanceKmFromAirport": 3, "URL": "https://www.mercadal.cat"},
            {"rank": 8, "postcode": "43840", "distance": 10.0, "distanceKmFromAirport": 12, "URL": "https://www.portaventuraworld.com"},
            {"rank": 9, "postcode": "43003", "distance": 14.0, "distanceKmFromAirport": 16, "URL": "https://www.tarragonaturisme.cat"},
            {"rank": 10, "postcode": "43580", "distance": 60.0, "distanceKmFromAirport": 62, "URL": "https://www.ebregreen.org"},
        ]
    },
    "rijeka": {
        "attractions": [
            {"rank": 1, "postcode": "51000", "distance": 0.5, "distanceKmFromAirport": 28, "URL": "https://www.ri-karneval.com.hr"},
            {"rank": 2, "postcode": "51000", "distance": 3.0, "distanceKmFromAirport": 30, "URL": "https://www.rijeka.hr"},
            {"rank": 3, "postcode": "51000", "distance": 0.5, "distanceKmFromAirport": 28, "URL": "https://www.pmi-ri.hr"},
            {"rank": 4, "postcode": "51000", "distance": 0.3, "distanceKmFromAirport": 28, "URL": "https://www.rijeka.hr"},
            {"rank": 5, "postcode": "51000", "distance": 0.5, "distanceKmFromAirport": 28, "URL": "https://www.rijeka.hr"},
            {"rank": 6, "postcode": "51000", "distance": 0.3, "distanceKmFromAirport": 28, "URL": "https://www.rijeka.hr"},
            {"rank": 7, "postcode": "51000", "distance": 0.3, "distanceKmFromAirport": 28, "URL": "https://www.rijeka.hr"},
            {"rank": 8, "postcode": "51410", "distance": 15.0, "distanceKmFromAirport": 42, "URL": "https://www.visitopatija.com"},
            {"rank": 9, "postcode": "51000", "distance": 2.0, "distanceKmFromAirport": 29, "URL": "https://www.rijeka.hr"},
            {"rank": 10, "postcode": "51511", "distance": 35.0, "distanceKmFromAirport": 50, "URL": "https://www.krk.hr"},
        ]
    },
    "riyadh": {
        "attractions": [
            {"rank": 1, "postcode": "11564", "distance": 1.0, "distanceKmFromAirport": 35, "URL": "https://www.masmak.org.sa"},
            {"rank": 2, "postcode": "11564", "distance": 2.0, "distanceKmFromAirport": 36, "URL": "https://www.nmc.gov.sa"},
            {"rank": 3, "postcode": "15326", "distance": 75.0, "distanceKmFromAirport": 108, "URL": "https://www.sauditourism.sa"},
            {"rank": 4, "postcode": "13711", "distance": 12.0, "distanceKmFromAirport": 40, "URL": "https://www.diriyah.sa"},
            {"rank": 5, "postcode": "12215", "distance": 5.0, "distanceKmFromAirport": 39, "URL": "https://www.kingdomcentre.com.sa"},
            {"rank": 6, "postcode": "12816", "distance": 10.0, "distanceKmFromAirport": 44, "URL": "https://www.riyadhzoo.org.sa"},
            {"rank": 7, "postcode": "11564", "distance": 1.0, "distanceKmFromAirport": 35, "URL": "https://www.sauditourism.sa"},
            {"rank": 8, "postcode": "12212", "distance": 5.0, "distanceKmFromAirport": 39, "URL": "https://www.alfaisaliahpower.com"},
            {"rank": 9, "postcode": "13243", "distance": 25.0, "distanceKmFromAirport": 55, "URL": "https://www.sauditourism.sa"},
            {"rank": 10, "postcode": "12386", "distance": 8.0, "distanceKmFromAirport": 42, "URL": "https://www.boulevardriyadh.com"},
        ]
    },
}

def reorder_fields(attraction):
    """Reorder attraction fields to: rank, name, postcode, distanceKmFromAirport, description, distance, URL"""
    return {
        "rank": attraction["rank"],
        "name": attraction["name"],
        "postcode": attraction["postcode"],
        "distanceKmFromAirport": attraction["distanceKmFromAirport"],
        "description": attraction["description"],
        "distance": attraction["distance"],
        "URL": attraction["URL"],
    }

def update_city(city_name):
    """Update a single city's attractions file"""
    filepath = os.path.join(BASE, f"{city_name}.json")
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if city_name not in updates:
        print(f"No updates defined for: {city_name}")
        return
    
    update_data = updates[city_name]
    attractions_list = update_data["attractions"]
    
    for attraction in data.get("things", []):
        rank = attraction.get("rank")
        for update in attractions_list:
            if update["rank"] == rank:
                attraction["postcode"] = update["postcode"]
                attraction["distance"] = update["distance"]
                attraction["distanceKmFromAirport"] = update["distanceKmFromAirport"]
                attraction["URL"] = update["URL"]
                break
    
    data["things"] = [reorder_fields(a) for a in data["things"]]
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Updated: {city_name}")

if __name__ == "__main__":
    cities = ["pune", "punta_arenas", "punta_cana", "pyongyang", "qingdao", "quito", "rabat", "reus", "rijeka", "riyadh"]
    for city in cities:
        update_city(city)
    print("All cities updated successfully!")
