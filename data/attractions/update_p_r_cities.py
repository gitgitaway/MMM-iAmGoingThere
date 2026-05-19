import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

updates = {
    "port_of_spain": {
        "attractions": [
            {"rank": 1, "postcode": "100101", "distance": 0.5, "distanceKmFromAirport": 27, "URL": "https://www.ncctt.org"},
            {"rank": 2, "postcode": "500271", "distance": 35.0, "distanceKmFromAirport": 58, "URL": "https://www.asawright.org"},
            {"rank": 3, "postcode": "100101", "distance": 1.5, "distanceKmFromAirport": 28, "URL": "https://www.ncctt.org"},
            {"rank": 4, "postcode": "110102", "distance": 20.0, "distanceKmFromAirport": 35, "URL": "https://www.gotrinidadandtobago.com"},
            {"rank": 5, "postcode": "100101", "distance": 0.5, "distanceKmFromAirport": 27, "URL": "https://www.museums.gov.tt"},
            {"rank": 6, "postcode": "100200", "distance": 16.0, "distanceKmFromAirport": 12, "URL": "https://www.gotrinidadandtobago.com"},
            {"rank": 7, "postcode": "600201", "distance": 110.0, "distanceKmFromAirport": 137, "URL": "https://www.gotrinidadandtobago.com"},
            {"rank": 8, "postcode": "500272", "distance": 20.0, "distanceKmFromAirport": 45, "URL": "https://www.gotrinidadandtobago.com"},
            {"rank": 9, "postcode": "100101", "distance": 1.5, "distanceKmFromAirport": 28, "URL": "https://www.empvalleyzoo.com"},
            {"rank": 10, "postcode": "100101", "distance": 0.5, "distanceKmFromAirport": 27, "URL": ""},
        ]
    },
    "port_vila": {
        "attractions": [
            {"rank": 1, "postcode": "", "distance": 200.0, "distanceKmFromAirport": 205, "URL": "https://www.vanuatu.travel"},
            {"rank": 2, "postcode": "", "distance": 25.0, "distanceKmFromAirport": 30, "URL": "https://www.vanuatu.travel"},
            {"rank": 3, "postcode": "", "distance": 10.0, "distanceKmFromAirport": 15, "URL": "https://www.vanuatu.travel"},
            {"rank": 4, "postcode": "", "distance": 8.0, "distanceKmFromAirport": 8, "URL": "https://www.melecascades.com"},
            {"rank": 5, "postcode": "1006", "distance": 0.5, "distanceKmFromAirport": 6, "URL": "https://www.vanuatumuseum.org.vu"},
            {"rank": 6, "postcode": "1006", "distance": 5.0, "distanceKmFromAirport": 5, "URL": "https://www.hideaway.com.vu"},
            {"rank": 7, "postcode": "", "distance": 280.0, "distanceKmFromAirport": 285, "URL": "https://www.vanuatu.travel"},
            {"rank": 8, "postcode": "1006", "distance": 0.5, "distanceKmFromAirport": 6, "URL": ""},
            {"rank": 9, "postcode": "1006", "distance": 1.0, "distanceKmFromAirport": 6, "URL": ""},
            {"rank": 10, "postcode": "1006", "distance": 2.0, "distanceKmFromAirport": 7, "URL": ""},
        ]
    },
    "praia": {
        "attractions": [
            {"rank": 1, "postcode": "7610", "distance": 15.0, "distanceKmFromAirport": 16, "URL": "https://www.cidadevelha.gov.cv"},
            {"rank": 2, "postcode": "7600", "distance": 0.5, "distanceKmFromAirport": 2, "URL": ""},
            {"rank": 3, "postcode": "7600", "distance": 1.0, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 4, "postcode": "7600", "distance": 0.5, "distanceKmFromAirport": 2, "URL": ""},
            {"rank": 5, "postcode": "7600", "distance": 1.0, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 6, "postcode": "7600", "distance": 0.5, "distanceKmFromAirport": 2, "URL": ""},
            {"rank": 7, "postcode": "7701", "distance": 35.0, "distanceKmFromAirport": 36, "URL": ""},
            {"rank": 8, "postcode": "7850", "distance": 70.0, "distanceKmFromAirport": 71, "URL": ""},
            {"rank": 9, "postcode": "", "distance": 180.0, "distanceKmFromAirport": 181, "URL": "https://www.turismo.cv"},
            {"rank": 10, "postcode": "7600", "distance": 0.5, "distanceKmFromAirport": 2, "URL": ""},
        ]
    },
    "pristina": {
        "attractions": [
            {"rank": 1, "postcode": "10000", "distance": 0.5, "distanceKmFromAirport": 14, "URL": ""},
            {"rank": 2, "postcode": "10000", "distance": 1.0, "distanceKmFromAirport": 15, "URL": "https://www.biblioteka-ks.org"},
            {"rank": 3, "postcode": "10000", "distance": 0.3, "distanceKmFromAirport": 14, "URL": ""},
            {"rank": 4, "postcode": "10000", "distance": 0.5, "distanceKmFromAirport": 14, "URL": "https://www.tkk-ks.com"},
            {"rank": 5, "postcode": "10000", "distance": 0.8, "distanceKmFromAirport": 14, "URL": ""},
            {"rank": 6, "postcode": "10000", "distance": 0.5, "distanceKmFromAirport": 14, "URL": ""},
            {"rank": 7, "postcode": "10000", "distance": 0.5, "distanceKmFromAirport": 14, "URL": ""},
            {"rank": 8, "postcode": "13000", "distance": 9.0, "distanceKmFromAirport": 20, "URL": "https://www.manastirgrachanica.net"},
            {"rank": 9, "postcode": "10000", "distance": 5.0, "distanceKmFromAirport": 18, "URL": "https://www.bearsanctuary-pristina.org"},
            {"rank": 10, "postcode": "10000", "distance": 3.0, "distanceKmFromAirport": 16, "URL": ""},
        ]
    },
    "puerto_princesa": {
        "attractions": [
            {"rank": 1, "postcode": "5300", "distance": 80.0, "distanceKmFromAirport": 82, "URL": "https://www.puerto-undergroundriver.com"},
            {"rank": 2, "postcode": "5313", "distance": 230.0, "distanceKmFromAirport": 233, "URL": "https://www.elnidoparadise.com"},
            {"rank": 3, "postcode": "5300", "distance": 15.0, "distanceKmFromAirport": 18, "URL": ""},
            {"rank": 4, "postcode": "5300", "distance": 6.0, "distanceKmFromAirport": 8, "URL": ""},
            {"rank": 5, "postcode": "5300", "distance": 23.0, "distanceKmFromAirport": 26, "URL": ""},
            {"rank": 6, "postcode": "5300", "distance": 5.0, "distanceKmFromAirport": 7, "URL": ""},
            {"rank": 7, "postcode": "5300", "distance": 43.0, "distanceKmFromAirport": 46, "URL": ""},
            {"rank": 8, "postcode": "5300", "distance": 2.0, "distanceKmFromAirport": 5, "URL": ""},
            {"rank": 9, "postcode": "5300", "distance": 23.0, "distanceKmFromAirport": 26, "URL": ""},
            {"rank": 10, "postcode": "5300", "distance": 80.0, "distanceKmFromAirport": 82, "URL": ""},
        ]
    },
    "pune": {
        "attractions": [
            {"rank": 1, "postcode": "411002", "distance": 2.0, "distanceKmFromAirport": 11, "URL": "https://www.shaniwadwada.in"},
            {"rank": 2, "postcode": "411006", "distance": 4.0, "distanceKmFromAirport": 13, "URL": ""},
            {"rank": 3, "postcode": "412301", "distance": 25.0, "distanceKmFromAirport": 34, "URL": ""},
            {"rank": 4, "postcode": "411001", "distance": 4.0, "distanceKmFromAirport": 13, "URL": "https://www.osho.com"},
            {"rank": 5, "postcode": "411004", "distance": 2.0, "distanceKmFromAirport": 11, "URL": ""},
            {"rank": 6, "postcode": "411001", "distance": 4.0, "distanceKmFromAirport": 13, "URL": ""},
            {"rank": 7, "postcode": "411038", "distance": 6.0, "distanceKmFromAirport": 14, "URL": ""},
            {"rank": 8, "postcode": "411002", "distance": 2.0, "distanceKmFromAirport": 11, "URL": "https://www.rajakelkarmuseum.com"},
            {"rank": 9, "postcode": "411001", "distance": 2.0, "distanceKmFromAirport": 11, "URL": "https://www.irctc.co.in"},
            {"rank": 10, "postcode": "411002", "distance": 2.0, "distanceKmFromAirport": 11, "URL": ""},
        ]
    },
    "punta_arenas": {
        "attractions": [
            {"rank": 1, "postcode": "6280000", "distance": 250.0, "distanceKmFromAirport": 265, "URL": "https://www.torresdelpaine.com"},
            {"rank": 2, "postcode": "6200000", "distance": 35.0, "distanceKmFromAirport": 52, "URL": "https://www.turismomagallanes.cl"},
            {"rank": 3, "postcode": "6200000", "distance": 1.0, "distanceKmFromAirport": 20, "URL": ""},
            {"rank": 4, "postcode": "6200000", "distance": 0.5, "distanceKmFromAirport": 20, "URL": ""},
            {"rank": 5, "postcode": "6200000", "distance": 1.5, "distanceKmFromAirport": 21, "URL": ""},
            {"rank": 6, "postcode": "", "distance": 400.0, "distanceKmFromAirport": 419, "URL": ""},
            {"rank": 7, "postcode": "", "distance": 310.0, "distanceKmFromAirport": 329, "URL": "https://www.parquesnacionales.gob.ar"},
            {"rank": 8, "postcode": "", "distance": 24.0, "distanceKmFromAirport": 40, "URL": ""},
            {"rank": 9, "postcode": "6200000", "distance": 1.0, "distanceKmFromAirport": 20, "URL": ""},
            {"rank": 10, "postcode": "6200000", "distance": 1.0, "distanceKmFromAirport": 20, "URL": ""},
        ]
    },
    "punta_cana": {
        "attractions": [
            {"rank": 1, "postcode": "23301", "distance": 5.0, "distanceKmFromAirport": 28, "URL": ""},
            {"rank": 2, "postcode": "22000", "distance": 95.0, "distanceKmFromAirport": 117, "URL": ""},
            {"rank": 3, "postcode": "23301", "distance": 40.0, "distanceKmFromAirport": 62, "URL": "https://www.iguanamaniahoyo.com"},
            {"rank": 4, "postcode": "23301", "distance": 15.0, "distanceKmFromAirport": 38, "URL": ""},
            {"rank": 5, "postcode": "23301", "distance": 5.0, "distanceKmFromAirport": 28, "URL": ""},
            {"rank": 6, "postcode": "23301", "distance": 10.0, "distanceKmFromAirport": 33, "URL": ""},
            {"rank": 7, "postcode": "23301", "distance": 15.0, "distanceKmFromAirport": 38, "URL": ""},
            {"rank": 8, "postcode": "22000", "distance": 100.0, "distanceKmFromAirport": 122, "URL": "https://www.casadecampo.com.do"},
            {"rank": 9, "postcode": "23301", "distance": 8.0, "distanceKmFromAirport": 18, "URL": "https://www.capcana.com"},
            {"rank": 10, "postcode": "23301", "distance": 0.5, "distanceKmFromAirport": 25, "URL": ""},
        ]
    },
    "pyongyang": {
        "attractions": [
            {"rank": 1, "postcode": "999091", "distance": 5.0, "distanceKmFromAirport": 28, "URL": ""},
            {"rank": 2, "postcode": "999091", "distance": 1.0, "distanceKmFromAirport": 24, "URL": ""},
            {"rank": 3, "postcode": "999091", "distance": 1.0, "distanceKmFromAirport": 24, "URL": ""},
            {"rank": 4, "postcode": "999091", "distance": 0.5, "distanceKmFromAirport": 24, "URL": ""},
            {"rank": 5, "postcode": "999091", "distance": 1.0, "distanceKmFromAirport": 24, "URL": ""},
            {"rank": 6, "postcode": "999091", "distance": 2.0, "distanceKmFromAirport": 25, "URL": ""},
            {"rank": 7, "postcode": "999091", "distance": 3.0, "distanceKmFromAirport": 26, "URL": ""},
            {"rank": 8, "postcode": "999091", "distance": 12.0, "distanceKmFromAirport": 34, "URL": ""},
            {"rank": 9, "postcode": "999161", "distance": 170.0, "distanceKmFromAirport": 189, "URL": ""},
            {"rank": 10, "postcode": "999091", "distance": 0.5, "distanceKmFromAirport": 24, "URL": ""},
        ]
    },
    "qingdao": {
        "attractions": [
            {"rank": 1, "postcode": "266031", "distance": 5.0, "distanceKmFromAirport": 34, "URL": "https://www.tsingtaobeerfestival.com"},
            {"rank": 2, "postcode": "266003", "distance": 4.0, "distanceKmFromAirport": 33, "URL": ""},
            {"rank": 3, "postcode": "266071", "distance": 8.0, "distanceKmFromAirport": 37, "URL": ""},
            {"rank": 4, "postcode": "266003", "distance": 3.0, "distanceKmFromAirport": 32, "URL": ""},
            {"rank": 5, "postcode": "266023", "distance": 5.0, "distanceKmFromAirport": 34, "URL": "https://www.tsingtaomuseum.com"},
            {"rank": 6, "postcode": "266100", "distance": 30.0, "distanceKmFromAirport": 30, "URL": ""},
            {"rank": 7, "postcode": "266001", "distance": 1.0, "distanceKmFromAirport": 30, "URL": ""},
            {"rank": 8, "postcode": "266003", "distance": 5.0, "distanceKmFromAirport": 34, "URL": ""},
            {"rank": 9, "postcode": "266003", "distance": 4.0, "distanceKmFromAirport": 33, "URL": ""},
            {"rank": 10, "postcode": "266002", "distance": 6.0, "distanceKmFromAirport": 35, "URL": ""},
        ]
    },
    "quito": {
        "attractions": [
            {"rank": 1, "postcode": "170150", "distance": 0.5, "distanceKmFromAirport": 37, "URL": "https://www.quito.com.ec"},
            {"rank": 2, "postcode": "170902", "distance": 22.0, "distanceKmFromAirport": 28, "URL": "https://www.mitaddelmundo.com"},
            {"rank": 3, "postcode": "", "distance": 1000.0, "distanceKmFromAirport": 1035, "URL": "https://www.galapagos.org"},
            {"rank": 4, "postcode": "170150", "distance": 5.0, "distanceKmFromAirport": 41, "URL": "https://www.teleferico.com.ec"},
            {"rank": 5, "postcode": "170150", "distance": 0.3, "distanceKmFromAirport": 37, "URL": ""},
            {"rank": 6, "postcode": "050150", "distance": 75.0, "distanceKmFromAirport": 106, "URL": ""},
            {"rank": 7, "postcode": "100201", "distance": 95.0, "distanceKmFromAirport": 118, "URL": ""},
            {"rank": 8, "postcode": "170150", "distance": 0.5, "distanceKmFromAirport": 37, "URL": ""},
            {"rank": 9, "postcode": "", "distance": 250.0, "distanceKmFromAirport": 282, "URL": ""},
            {"rank": 10, "postcode": "170150", "distance": 0.5, "distanceKmFromAirport": 37, "URL": ""},
        ]
    },
    "rabat": {
        "attractions": [
            {"rank": 1, "postcode": "10000", "distance": 1.0, "distanceKmFromAirport": 12, "URL": ""},
            {"rank": 2, "postcode": "10000", "distance": 1.5, "distanceKmFromAirport": 13, "URL": ""},
            {"rank": 3, "postcode": "10000", "distance": 2.0, "distanceKmFromAirport": 13, "URL": ""},
            {"rank": 4, "postcode": "10000", "distance": 1.5, "distanceKmFromAirport": 13, "URL": "https://www.mmc.ma"},
            {"rank": 5, "postcode": "10020", "distance": 1.0, "distanceKmFromAirport": 12, "URL": ""},
            {"rank": 6, "postcode": "11000", "distance": 4.0, "distanceKmFromAirport": 15, "URL": ""},
            {"rank": 7, "postcode": "10010", "distance": 0.5, "distanceKmFromAirport": 12, "URL": ""},
            {"rank": 8, "postcode": "10000", "distance": 1.5, "distanceKmFromAirport": 13, "URL": ""},
            {"rank": 9, "postcode": "10000", "distance": 1.0, "distanceKmFromAirport": 12, "URL": ""},
            {"rank": 10, "postcode": "10000", "distance": 1.0, "distanceKmFromAirport": 12, "URL": ""},
        ]
    },
    "reus": {
        "attractions": [
            {"rank": 1, "postcode": "43201", "distance": 0.3, "distanceKmFromAirport": 3, "URL": "https://www.gaudicentre.cat"},
            {"rank": 2, "postcode": "43201", "distance": 0.5, "distanceKmFromAirport": 3, "URL": "https://www.visit.reus.cat"},
            {"rank": 3, "postcode": "43201", "distance": 0.3, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 4, "postcode": "43201", "distance": 0.2, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 5, "postcode": "43201", "distance": 0.4, "distanceKmFromAirport": 3, "URL": "https://www.museudereus.cat"},
            {"rank": 6, "postcode": "43201", "distance": 0.3, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 7, "postcode": "43201", "distance": 0.3, "distanceKmFromAirport": 3, "URL": ""},
            {"rank": 8, "postcode": "43840", "distance": 10.0, "distanceKmFromAirport": 12, "URL": "https://www.portaventuraworld.com"},
            {"rank": 9, "postcode": "43003", "distance": 14.0, "distanceKmFromAirport": 16, "URL": "https://www.tarragonaturisme.cat"},
            {"rank": 10, "postcode": "43580", "distance": 60.0, "distanceKmFromAirport": 62, "URL": ""},
        ]
    },
    "rijeka": {
        "attractions": [
            {"rank": 1, "postcode": "51000", "distance": 0.5, "distanceKmFromAirport": 28, "URL": "https://www.ri-karneval.com.hr"},
            {"rank": 2, "postcode": "51000", "distance": 3.0, "distanceKmFromAirport": 30, "URL": ""},
            {"rank": 3, "postcode": "51000", "distance": 0.5, "distanceKmFromAirport": 28, "URL": "https://www.pmi-ri.hr"},
            {"rank": 4, "postcode": "51000", "distance": 0.3, "distanceKmFromAirport": 28, "URL": ""},
            {"rank": 5, "postcode": "51000", "distance": 0.5, "distanceKmFromAirport": 28, "URL": ""},
            {"rank": 6, "postcode": "51000", "distance": 0.3, "distanceKmFromAirport": 28, "URL": ""},
            {"rank": 7, "postcode": "51000", "distance": 0.3, "distanceKmFromAirport": 28, "URL": ""},
            {"rank": 8, "postcode": "51410", "distance": 15.0, "distanceKmFromAirport": 42, "URL": "https://www.visitopatija.com"},
            {"rank": 9, "postcode": "51000", "distance": 2.0, "distanceKmFromAirport": 29, "URL": ""},
            {"rank": 10, "postcode": "51511", "distance": 35.0, "distanceKmFromAirport": 50, "URL": ""},
        ]
    },
    "riyadh": {
        "attractions": [
            {"rank": 1, "postcode": "11564", "distance": 1.0, "distanceKmFromAirport": 35, "URL": "https://www.masmak.org.sa"},
            {"rank": 2, "postcode": "11564", "distance": 2.0, "distanceKmFromAirport": 36, "URL": "https://www.nmc.gov.sa"},
            {"rank": 3, "postcode": "15326", "distance": 75.0, "distanceKmFromAirport": 108, "URL": ""},
            {"rank": 4, "postcode": "13711", "distance": 12.0, "distanceKmFromAirport": 40, "URL": "https://www.diriyah.sa"},
            {"rank": 5, "postcode": "12215", "distance": 5.0, "distanceKmFromAirport": 39, "URL": ""},
            {"rank": 6, "postcode": "12816", "distance": 10.0, "distanceKmFromAirport": 44, "URL": ""},
            {"rank": 7, "postcode": "11564", "distance": 1.0, "distanceKmFromAirport": 35, "URL": ""},
            {"rank": 8, "postcode": "12212", "distance": 5.0, "distanceKmFromAirport": 39, "URL": ""},
            {"rank": 9, "postcode": "13243", "distance": 25.0, "distanceKmFromAirport": 55, "URL": ""},
            {"rank": 10, "postcode": "12386", "distance": 8.0, "distanceKmFromAirport": 42, "URL": ""},
        ]
    },
}

FIELD_ORDER = ["rank", "name", "postcode", "distanceKmFromAirport", "description", "distance", "URL"]

for city_key, city_updates in updates.items():
    filepath = os.path.join(BASE, f"{city_key}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    update_map = {u["rank"]: u for u in city_updates["attractions"]}

    new_things = []
    for thing in data["things"]:
        rank = thing["rank"]
        upd = update_map.get(rank, {})
        merged = {
            "rank": thing["rank"],
            "name": thing["name"],
            "postcode": upd.get("postcode", thing.get("postcode", "")),
            "distanceKmFromAirport": upd.get("distanceKmFromAirport", thing.get("distanceKmFromAirport", None)),
            "description": thing["description"],
            "distance": upd.get("distance", thing.get("distance", None)),
            "URL": upd.get("URL", thing.get("URL", "")),
        }
        new_things.append(merged)

    data["things"] = new_things

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated: {city_key}.json")

print("All done.")
