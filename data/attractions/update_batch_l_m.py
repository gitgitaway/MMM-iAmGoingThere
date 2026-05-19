import json
import os

base = r"c:\Users\junkp\MagicMirror\modules\MMM-iAmGoingThere\data\attractions"

updates = {
    "luang_prabang": [
        {"rank":1,"postcode":"0600","distance":0.5,"distanceKmFromAirport":5,"URL":""},
        {"rank":2,"postcode":"0600","distance":29.0,"distanceKmFromAirport":33,"URL":"https://www.kuangsifalls.com/"},
        {"rank":3,"postcode":"0600","distance":0.2,"distanceKmFromAirport":4,"URL":""},
        {"rank":4,"postcode":"0600","distance":0.8,"distanceKmFromAirport":5,"URL":""},
        {"rank":5,"postcode":"0600","distance":0.3,"distanceKmFromAirport":4,"URL":""},
        {"rank":6,"postcode":"0600","distance":0.5,"distanceKmFromAirport":5,"URL":""},
        {"rank":7,"postcode":"0600","distance":0.3,"distanceKmFromAirport":4,"URL":""},
        {"rank":8,"postcode":"0600","distance":0.3,"distanceKmFromAirport":4,"URL":""},
        {"rank":9,"postcode":"0600","distance":25.0,"distanceKmFromAirport":21,"URL":""},
        {"rank":10,"postcode":"0600","distance":15.0,"distanceKmFromAirport":19,"URL":""},
    ],
    "lucknow": [
        {"rank":1,"postcode":"226003","distance":1.0,"distanceKmFromAirport":19,"URL":"https://uptourism.gov.in/"},
        {"rank":2,"postcode":"226003","distance":1.2,"distanceKmFromAirport":19,"URL":""},
        {"rank":3,"postcode":"226003","distance":1.0,"distanceKmFromAirport":19,"URL":""},
        {"rank":4,"postcode":"226001","distance":1.5,"distanceKmFromAirport":20,"URL":"https://asi.nic.in/"},
        {"rank":5,"postcode":"226001","distance":1.0,"distanceKmFromAirport":19,"URL":""},
        {"rank":6,"postcode":"226003","distance":1.5,"distanceKmFromAirport":20,"URL":""},
        {"rank":7,"postcode":"226001","distance":3.5,"distanceKmFromAirport":22,"URL":"https://www.lucknowzoo.com/"},
        {"rank":8,"postcode":"226001","distance":3.0,"distanceKmFromAirport":21,"URL":""},
        {"rank":9,"postcode":"226003","distance":1.0,"distanceKmFromAirport":19,"URL":""},
        {"rank":10,"postcode":"226003","distance":1.5,"distanceKmFromAirport":20,"URL":""},
    ],
    "luton": [
        {"rank":1,"postcode":"LU6 2LF","distance":8.0,"distanceKmFromAirport":10,"URL":"https://www.zsl.org/whipsnade-zoo"},
        {"rank":2,"postcode":"MK17 9WA","distance":18.0,"distanceKmFromAirport":20,"URL":"https://www.woburnabbey.co.uk/"},
        {"rank":3,"postcode":"LU1 3TQ","distance":3.0,"distanceKmFromAirport":5,"URL":"https://www.lutonhoo.com/"},
        {"rank":4,"postcode":"LU6 2GY","distance":10.0,"distanceKmFromAirport":12,"URL":"https://www.nationaltrust.org.uk/dunstable-downs-and-whipsnade-estate"},
        {"rank":5,"postcode":"LU1 4LX","distance":3.5,"distanceKmFromAirport":5,"URL":"https://www.lutonculture.com/stockwood/"},
        {"rank":6,"postcode":"LU2 7HA","distance":1.5,"distanceKmFromAirport":4,"URL":"https://www.lutonculture.com/wardown/"},
        {"rank":7,"postcode":"LU5 4RS","distance":9.0,"distanceKmFromAirport":11,"URL":""},
        {"rank":8,"postcode":"HP4 1NX","distance":15.0,"distanceKmFromAirport":15,"URL":"https://www.chilternsaonb.org/"},
        {"rank":9,"postcode":"SG3 6PY","distance":28.0,"distanceKmFromAirport":30,"URL":"https://www.knebworthhouse.com/"},
        {"rank":10,"postcode":"AL2 1EX","distance":24.0,"distanceKmFromAirport":24,"URL":"https://www.dehavillandmuseum.co.uk/"},
    ],
    "luxembourg_city": [
        {"rank":1,"postcode":"L-1468","distance":0.5,"distanceKmFromAirport":7,"URL":"https://www.luxembourg-city.com/en/place/bock-casemates"},
        {"rank":2,"postcode":"L-1017","distance":0.2,"distanceKmFromAirport":6,"URL":"https://monarchie.lu/"},
        {"rank":3,"postcode":"L-2240","distance":0.3,"distanceKmFromAirport":6,"URL":"https://www.cathol.lu/"},
        {"rank":4,"postcode":"L-1114","distance":0.8,"distanceKmFromAirport":7,"URL":""},
        {"rank":5,"postcode":"L-2090","distance":1.5,"distanceKmFromAirport":8,"URL":"https://www.mudam.com/"},
        {"rank":6,"postcode":"L-1344","distance":0.5,"distanceKmFromAirport":7,"URL":""},
        {"rank":7,"postcode":"L-1629","distance":0.7,"distanceKmFromAirport":7,"URL":""},
        {"rank":8,"postcode":"L-1645","distance":1.0,"distanceKmFromAirport":7,"URL":""},
        {"rank":9,"postcode":"L-1468","distance":0.3,"distanceKmFromAirport":6,"URL":"https://mnha.lu/"},
        {"rank":10,"postcode":"L-9408","distance":40.0,"distanceKmFromAirport":46,"URL":"https://www.vianden-castle.lu/"},
    ],
    "lviv": [
        {"rank":1,"postcode":"79000","distance":0.5,"distanceKmFromAirport":8,"URL":"https://lviv.travel/"},
        {"rank":2,"postcode":"79008","distance":1.2,"distanceKmFromAirport":8,"URL":""},
        {"rank":3,"postcode":"79000","distance":0.2,"distanceKmFromAirport":7,"URL":""},
        {"rank":4,"postcode":"79000","distance":0.3,"distanceKmFromAirport":7,"URL":""},
        {"rank":5,"postcode":"79000","distance":0.4,"distanceKmFromAirport":7,"URL":""},
        {"rank":6,"postcode":"79010","distance":2.5,"distanceKmFromAirport":10,"URL":"https://lychakiv.org/"},
        {"rank":7,"postcode":"79000","distance":0.4,"distanceKmFromAirport":7,"URL":""},
        {"rank":8,"postcode":"79000","distance":0.3,"distanceKmFromAirport":7,"URL":""},
        {"rank":9,"postcode":"79013","distance":3.0,"distanceKmFromAirport":10,"URL":"https://skansen.lviv.ua/"},
        {"rank":10,"postcode":"79000","distance":0.3,"distanceKmFromAirport":7,"URL":"https://chocolate.lviv.ua/"},
    ],
    "majuro": [
        {"rank":1,"postcode":"96940","distance":1500.0,"distanceKmFromAirport":1500,"URL":"https://whc.unesco.org/en/list/1339"},
        {"rank":2,"postcode":"96960","distance":1.0,"distanceKmFromAirport":4,"URL":""},
        {"rank":3,"postcode":"96940","distance":1200.0,"distanceKmFromAirport":1200,"URL":""},
        {"rank":4,"postcode":"96960","distance":0.5,"distanceKmFromAirport":4,"URL":""},
        {"rank":5,"postcode":"96960","distance":1.0,"distanceKmFromAirport":4,"URL":""},
        {"rank":6,"postcode":"96960","distance":34.0,"distanceKmFromAirport":37,"URL":""},
        {"rank":7,"postcode":"96960","distance":1.0,"distanceKmFromAirport":4,"URL":""},
        {"rank":8,"postcode":"96960","distance":0.5,"distanceKmFromAirport":4,"URL":""},
        {"rank":9,"postcode":"96960","distance":5.0,"distanceKmFromAirport":8,"URL":""},
        {"rank":10,"postcode":"96960","distance":1.0,"distanceKmFromAirport":4,"URL":""},
    ],
    "makassar": [
        {"rank":1,"postcode":"90111","distance":0.5,"distanceKmFromAirport":19,"URL":""},
        {"rank":2,"postcode":"91811","distance":320.0,"distanceKmFromAirport":338,"URL":""},
        {"rank":3,"postcode":"90114","distance":1.5,"distanceKmFromAirport":20,"URL":""},
        {"rank":4,"postcode":"90131","distance":2.0,"distanceKmFromAirport":20,"URL":""},
        {"rank":5,"postcode":"92111","distance":8.0,"distanceKmFromAirport":26,"URL":""},
        {"rank":6,"postcode":"90561","distance":42.0,"distanceKmFromAirport":60,"URL":""},
        {"rank":7,"postcode":"90000","distance":10.0,"distanceKmFromAirport":28,"URL":""},
        {"rank":8,"postcode":"90561","distance":40.0,"distanceKmFromAirport":58,"URL":""},
        {"rank":9,"postcode":"90111","distance":0.3,"distanceKmFromAirport":18,"URL":""},
        {"rank":10,"postcode":"90111","distance":1.0,"distanceKmFromAirport":19,"URL":""},
    ],
    "malabo": [
        {"rank":1,"postcode":"GQ-LB","distance":0.2,"distanceKmFromAirport":7,"URL":""},
        {"rank":2,"postcode":"GQ-LB","distance":0.1,"distanceKmFromAirport":7,"URL":""},
        {"rank":3,"postcode":"GQ-LB","distance":3.0,"distanceKmFromAirport":10,"URL":""},
        {"rank":4,"postcode":"GQ-LB","distance":0.5,"distanceKmFromAirport":8,"URL":""},
        {"rank":5,"postcode":"GQ-LB","distance":12.0,"distanceKmFromAirport":19,"URL":""},
        {"rank":6,"postcode":"GQ-BS","distance":32.0,"distanceKmFromAirport":39,"URL":""},
        {"rank":7,"postcode":"GQ-KS","distance":60.0,"distanceKmFromAirport":67,"URL":""},
        {"rank":8,"postcode":"GQ-LB","distance":42.0,"distanceKmFromAirport":49,"URL":""},
        {"rank":9,"postcode":"GQ-LB","distance":0.5,"distanceKmFromAirport":8,"URL":""},
        {"rank":10,"postcode":"GQ-LB","distance":0.5,"distanceKmFromAirport":8,"URL":""},
    ],
    "male": [
        {"rank":1,"postcode":"20026","distance":20.0,"distanceKmFromAirport":22,"URL":""},
        {"rank":2,"postcode":"07020","distance":120.0,"distanceKmFromAirport":122,"URL":""},
        {"rank":3,"postcode":"20026","distance":10.0,"distanceKmFromAirport":12,"URL":""},
        {"rank":4,"postcode":"20026","distance":0.2,"distanceKmFromAirport":2,"URL":""},
        {"rank":5,"postcode":"20375","distance":0.3,"distanceKmFromAirport":2,"URL":"https://museum.gov.mv/"},
        {"rank":6,"postcode":"20026","distance":0.3,"distanceKmFromAirport":2,"URL":""},
        {"rank":7,"postcode":"20026","distance":50.0,"distanceKmFromAirport":52,"URL":""},
        {"rank":8,"postcode":"20026","distance":15.0,"distanceKmFromAirport":17,"URL":""},
        {"rank":9,"postcode":"20026","distance":0.5,"distanceKmFromAirport":3,"URL":""},
        {"rank":10,"postcode":"20026","distance":0.3,"distanceKmFromAirport":2,"URL":""},
    ],
    "malmo": [
        {"rank":1,"postcode":"211 15","distance":1.5,"distanceKmFromAirport":32,"URL":"https://www.hsvab.se/en/turning-torso/"},
        {"rank":2,"postcode":"211 19","distance":1.5,"distanceKmFromAirport":32,"URL":""},
        {"rank":3,"postcode":"211 18","distance":1.0,"distanceKmFromAirport":31,"URL":"https://malmo.se/Uppleva-och-gora/Museer-och-utstallningar/Malmo-Museum.html"},
        {"rank":4,"postcode":"211 22","distance":0.5,"distanceKmFromAirport":31,"URL":""},
        {"rank":5,"postcode":"230 32","distance":6.0,"distanceKmFromAirport":24,"URL":"https://www.oresundsbron.com/"},
        {"rank":6,"postcode":"211 24","distance":1.0,"distanceKmFromAirport":31,"URL":"https://www.modernamuseet.se/malmo/en/"},
        {"rank":7,"postcode":"211 22","distance":0.3,"distanceKmFromAirport":30,"URL":""},
        {"rank":8,"postcode":"214 21","distance":2.0,"distanceKmFromAirport":32,"URL":""},
        {"rank":9,"postcode":"211 34","distance":0.3,"distanceKmFromAirport":30,"URL":"https://petrikyrkan.se/"},
        {"rank":10,"postcode":"211 24","distance":1.0,"distanceKmFromAirport":31,"URL":""},
    ],
    "managua": [
        {"rank":1,"postcode":"47000","distance":75.0,"distanceKmFromAirport":86,"URL":"https://www.isladeometepe.com/"},
        {"rank":2,"postcode":"21000","distance":90.0,"distanceKmFromAirport":101,"URL":"https://catedraldeleon.org/"},
        {"rank":3,"postcode":"21000","distance":90.0,"distanceKmFromAirport":101,"URL":""},
        {"rank":4,"postcode":"52100","distance":28.0,"distanceKmFromAirport":39,"URL":"https://www.marena.gob.ni/"},
        {"rank":5,"postcode":"11001","distance":0.5,"distanceKmFromAirport":12,"URL":""},
        {"rank":6,"postcode":"11001","distance":3.0,"distanceKmFromAirport":14,"URL":""},
        {"rank":7,"postcode":"10001","distance":47.0,"distanceKmFromAirport":58,"URL":""},
        {"rank":8,"postcode":"11000","distance":52.0,"distanceKmFromAirport":63,"URL":""},
        {"rank":9,"postcode":"11001","distance":2.0,"distanceKmFromAirport":13,"URL":""},
        {"rank":10,"postcode":"10001","distance":47.0,"distanceKmFromAirport":58,"URL":""},
    ],
    "manama": [
        {"rank":1,"postcode":"614","distance":5.0,"distanceKmFromAirport":12,"URL":"https://www.qalatalbahrainsite.com/"},
        {"rank":2,"postcode":"193","distance":1.5,"distanceKmFromAirport":9,"URL":"https://www.bahrainmuseum.gov.bh/"},
        {"rank":3,"postcode":"1038","distance":3.0,"distanceKmFromAirport":10,"URL":"https://www.alfateh-mosque.com/"},
        {"rank":4,"postcode":"306","distance":0.5,"distanceKmFromAirport":8,"URL":""},
        {"rank":5,"postcode":"1062","distance":32.0,"distanceKmFromAirport":39,"URL":"https://www.bahraingp.com/"},
        {"rank":6,"postcode":"917","distance":40.0,"distanceKmFromAirport":47,"URL":""},
        {"rank":7,"postcode":"319","distance":5.0,"distanceKmFromAirport":12,"URL":"https://whc.unesco.org/en/list/1364"},
        {"rank":8,"postcode":"905","distance":15.0,"distanceKmFromAirport":22,"URL":""},
        {"rank":9,"postcode":"200","distance":5.0,"distanceKmFromAirport":12,"URL":""},
        {"rank":10,"postcode":"1061","distance":6.0,"distanceKmFromAirport":13,"URL":""},
    ],
    "mandalay": [
        {"rank":1,"postcode":"05251","distance":160.0,"distanceKmFromAirport":198,"URL":"https://www.baganmyanmar.net/"},
        {"rank":2,"postcode":"05012","distance":2.0,"distanceKmFromAirport":40,"URL":""},
        {"rank":3,"postcode":"05011","distance":1.5,"distanceKmFromAirport":40,"URL":""},
        {"rank":4,"postcode":"05041","distance":11.0,"distanceKmFromAirport":49,"URL":""},
        {"rank":5,"postcode":"05032","distance":2.5,"distanceKmFromAirport":41,"URL":""},
        {"rank":6,"postcode":"05012","distance":1.5,"distanceKmFromAirport":40,"URL":""},
        {"rank":7,"postcode":"05012","distance":1.0,"distanceKmFromAirport":39,"URL":""},
        {"rank":8,"postcode":"05012","distance":1.5,"distanceKmFromAirport":40,"URL":""},
        {"rank":9,"postcode":"05060","distance":20.0,"distanceKmFromAirport":58,"URL":""},
        {"rank":10,"postcode":"05051","distance":20.0,"distanceKmFromAirport":58,"URL":""},
    ],
    "manila": [
        {"rank":1,"postcode":"1002","distance":3.0,"distanceKmFromAirport":10,"URL":"https://www.intramuros.gov.ph/"},
        {"rank":2,"postcode":"1000","distance":2.5,"distanceKmFromAirport":10,"URL":"https://rizalpark.gov.ph/"},
        {"rank":3,"postcode":"1002","distance":3.0,"distanceKmFromAirport":10,"URL":"https://www.sanagustinchurch.org.ph/"},
        {"rank":4,"postcode":"1006","distance":3.5,"distanceKmFromAirport":11,"URL":""},
        {"rank":5,"postcode":"1000","distance":2.5,"distanceKmFromAirport":10,"URL":"https://www.nationalmuseum.gov.ph/"},
        {"rank":6,"postcode":"1634","distance":7.0,"distanceKmFromAirport":14,"URL":"https://www.bgcbonifacioglobalcity.com/"},
        {"rank":7,"postcode":"1201","distance":48.0,"distanceKmFromAirport":55,"URL":""},
        {"rank":8,"postcode":"1001","distance":2.5,"distanceKmFromAirport":10,"URL":""},
        {"rank":9,"postcode":"1005","distance":3.0,"distanceKmFromAirport":10,"URL":"https://www.malacanang.gov.ph/"},
        {"rank":10,"postcode":"1210","distance":4.0,"distanceKmFromAirport":11,"URL":""},
    ],
    "manzini": [
        {"rank":1,"postcode":"H114","distance":20.0,"distanceKmFromAirport":25,"URL":"https://www.biggameparks.org/mlilwane/"},
        {"rank":2,"postcode":"H322","distance":60.0,"distanceKmFromAirport":65,"URL":"https://www.biggameparks.org/hlane/"},
        {"rank":3,"postcode":"H101","distance":32.0,"distanceKmFromAirport":37,"URL":"https://www.ngwenyaglass.co.sz/"},
        {"rank":4,"postcode":"M202","distance":0.3,"distanceKmFromAirport":5,"URL":""},
        {"rank":5,"postcode":"H116","distance":20.0,"distanceKmFromAirport":25,"URL":""},
        {"rank":6,"postcode":"H116","distance":20.0,"distanceKmFromAirport":25,"URL":"https://www.swazi-cultural-village.com/"},
        {"rank":7,"postcode":"H116","distance":20.0,"distanceKmFromAirport":25,"URL":""},
        {"rank":8,"postcode":"H101","distance":35.0,"distanceKmFromAirport":40,"URL":""},
        {"rank":9,"postcode":"H302","distance":62.0,"distanceKmFromAirport":67,"URL":""},
        {"rank":10,"postcode":"M202","distance":0.3,"distanceKmFromAirport":5,"URL":""},
    ],
}

def reorder(thing, upd):
    return {
        "rank": thing["rank"],
        "name": thing["name"],
        "postcode": upd["postcode"],
        "distanceKmFromAirport": upd["distanceKmFromAirport"],
        "description": thing["description"],
        "distance": upd["distance"],
        "URL": upd["URL"],
    }

for city, city_updates in updates.items():
    fpath = os.path.join(base, f"{city}.json")
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)

    upd_by_rank = {u["rank"]: u for u in city_updates}
    new_things = []
    for thing in data["things"]:
        r = thing["rank"]
        if r in upd_by_rank:
            new_things.append(reorder(thing, upd_by_rank[r]))
        else:
            new_things.append(thing)
    data["things"] = new_things

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated {city}.json")

print("Done.")
