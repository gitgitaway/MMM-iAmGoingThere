import json
import os

base_path = r"c:\Users\junkp\MagicMirror\modules\MMM-iAmGoingThere\data\attractions"

cities_data = {
    "ulaanbaatar": {
        "things": [
            {"rank": 1, "postcode": "14200", "distance": 1.5, "distanceKmFromAirport": 19, "URL": "https://www.gandan.mn"},
            {"rank": 2, "postcode": "14200", "distance": 0.5, "distanceKmFromAirport": 19, "URL": "https://nationalmuseum.mn"},
            {"rank": 3, "postcode": "14200", "distance": 0.1, "distanceKmFromAirport": 18, "URL": ""},
            {"rank": 4, "postcode": "17024", "distance": 6.0, "distanceKmFromAirport": 24, "URL": "https://bogdkhanmuseum.mn"},
            {"rank": 5, "postcode": "17330", "distance": 60.0, "distanceKmFromAirport": 75, "URL": "https://www.mongoliatourism.gov.mn"},
            {"rank": 6, "postcode": "17190", "distance": 54.0, "distanceKmFromAirport": 68, "URL": "https://www.genghiskhan.mn"},
            {"rank": 7, "postcode": "14240", "distance": 0.8, "distanceKmFromAirport": 19, "URL": "https://choijinlama.mn"},
            {"rank": 8, "postcode": "14201", "distance": 1.5, "distanceKmFromAirport": 20, "URL": "https://www.mongoliatourism.gov.mn"},
            {"rank": 9, "postcode": "13381", "distance": 3.0, "distanceKmFromAirport": 21, "URL": ""},
            {"rank": 10, "postcode": "14240", "distance": 0.5, "distanceKmFromAirport": 19, "URL": "http://www.nm.mn"},
        ]
    },
    "valletta": {
        "things": [
            {"rank": 1, "postcode": "VLT 1165", "distance": 0.3, "distanceKmFromAirport": 8, "URL": "https://www.stjohnscocathedral.com"},
            {"rank": 2, "postcode": "VLT 1010", "distance": 0.5, "distanceKmFromAirport": 8, "URL": "https://heritagemalta.mt"},
            {"rank": 3, "postcode": "VLT 1000", "distance": 0.4, "distanceKmFromAirport": 8, "URL": ""},
            {"rank": 4, "postcode": "MDN 1010", "distance": 12.0, "distanceKmFromAirport": 7, "URL": "https://www.visitmalta.com/en/a/mdina"},
            {"rank": 5, "postcode": "ZRQ 1010", "distance": 15.0, "distanceKmFromAirport": 14, "URL": "https://www.visitmalta.com/en/a/blue-grotto"},
            {"rank": 6, "postcode": "BKR 1000", "distance": 3.0, "distanceKmFromAirport": 6, "URL": "https://www.visitmalta.com/en/a/three-cities"},
            {"rank": 7, "postcode": "ZRQ 1000", "distance": 13.0, "distanceKmFromAirport": 12, "URL": "https://heritagemalta.mt/hagar-qim-temples"},
            {"rank": 8, "postcode": "VLT 1110", "distance": 0.2, "distanceKmFromAirport": 8, "URL": "https://www.visitmalta.com/en/a/republic-street-valletta"},
            {"rank": 9, "postcode": "VLT 2000", "distance": 0.3, "distanceKmFromAirport": 8, "URL": "https://heritagemalta.mt/national-museum-of-archaeology"},
            {"rank": 10, "postcode": "VCT 1011", "distance": 30.0, "distanceKmFromAirport": 35, "URL": "https://www.visitgozo.com"},
        ]
    },
    "varadero": {
        "things": [
            {"rank": 1, "postcode": "42200", "distance": 0.5, "distanceKmFromAirport": 18, "URL": "https://www.cubatravel.cu"},
            {"rank": 2, "postcode": "42200", "distance": 1.0, "distanceKmFromAirport": 19, "URL": "https://www.cubatravel.cu"},
            {"rank": 3, "postcode": "42200", "distance": 8.0, "distanceKmFromAirport": 13, "URL": ""},
            {"rank": 4, "postcode": "42200", "distance": 18.0, "distanceKmFromAirport": 5, "URL": "https://www.varawerogolfclub.com"},
            {"rank": 5, "postcode": "42200", "distance": 50.0, "distanceKmFromAirport": 65, "URL": ""},
            {"rank": 6, "postcode": "10400", "distance": 140.0, "distanceKmFromAirport": 155, "URL": "https://www.cubatravel.cu"},
            {"rank": 7, "postcode": "42200", "distance": 3.0, "distanceKmFromAirport": 17, "URL": ""},
            {"rank": 8, "postcode": "42200", "distance": 18.0, "distanceKmFromAirport": 5, "URL": "https://www.mansionxanadu.com"},
            {"rank": 9, "postcode": "42200", "distance": 2.0, "distanceKmFromAirport": 18, "URL": ""},
            {"rank": 10, "postcode": "42200", "distance": 1.0, "distanceKmFromAirport": 19, "URL": ""},
        ]
    },
    "varanasi": {
        "things": [
            {"rank": 1, "postcode": "221001", "distance": 0.5, "distanceKmFromAirport": 24, "URL": "https://varanasighat.in"},
            {"rank": 2, "postcode": "221001", "distance": 0.5, "distanceKmFromAirport": 24, "URL": ""},
            {"rank": 3, "postcode": "221001", "distance": 1.0, "distanceKmFromAirport": 25, "URL": ""},
            {"rank": 4, "postcode": "221001", "distance": 0.8, "distanceKmFromAirport": 25, "URL": "https://shrikashivishwanath.org"},
            {"rank": 5, "postcode": "221001", "distance": 1.0, "distanceKmFromAirport": 25, "URL": ""},
            {"rank": 6, "postcode": "221007", "distance": 10.0, "distanceKmFromAirport": 16, "URL": "https://www.sarnathmuseum.in"},
            {"rank": 7, "postcode": "221005", "distance": 3.0, "distanceKmFromAirport": 21, "URL": ""},
            {"rank": 8, "postcode": "221001", "distance": 2.0, "distanceKmFromAirport": 22, "URL": ""},
            {"rank": 9, "postcode": "221001", "distance": 1.5, "distanceKmFromAirport": 23, "URL": ""},
            {"rank": 10, "postcode": "221001", "distance": 0.5, "distanceKmFromAirport": 24, "URL": ""},
        ]
    },
    "venice": {
        "things": [
            {"rank": 1, "postcode": "30124", "distance": 0.1, "distanceKmFromAirport": 13, "URL": "https://www.basilicasanmarco.it"},
            {"rank": 2, "postcode": "30124", "distance": 0.5, "distanceKmFromAirport": 13, "URL": "https://www.veneziaunica.it"},
            {"rank": 3, "postcode": "30124", "distance": 0.1, "distanceKmFromAirport": 13, "URL": "https://palazzoducale.visitmuve.it"},
            {"rank": 4, "postcode": "30125", "distance": 0.8, "distanceKmFromAirport": 13, "URL": "https://www.mercatodireaaltovenezia.it"},
            {"rank": 5, "postcode": "30141", "distance": 1.5, "distanceKmFromAirport": 9, "URL": "https://www.muranoglass.com"},
            {"rank": 6, "postcode": "30124", "distance": 0.1, "distanceKmFromAirport": 13, "URL": "https://www.veneziaunica.it"},
            {"rank": 7, "postcode": "30123", "distance": 0.5, "distanceKmFromAirport": 13, "URL": "https://www.guggenheim-venice.it"},
            {"rank": 8, "postcode": "30012", "distance": 9.0, "distanceKmFromAirport": 6, "URL": "https://www.veneziaunica.it"},
            {"rank": 9, "postcode": "30123", "distance": 0.6, "distanceKmFromAirport": 13, "URL": "https://www.gallerieaccademia.it"},
            {"rank": 10, "postcode": "30125", "distance": 1.0, "distanceKmFromAirport": 13, "URL": "https://www.basilicadeifrari.it"},
        ]
    },
    "verona": {
        "things": [
            {"rank": 1, "postcode": "37121", "distance": 0.3, "distanceKmFromAirport": 14, "URL": "https://www.arena.it"},
            {"rank": 2, "postcode": "37121", "distance": 0.4, "distanceKmFromAirport": 14, "URL": "https://www.julietclub.com"},
            {"rank": 3, "postcode": "37121", "distance": 0.1, "distanceKmFromAirport": 14, "URL": "https://www.tourism.verona.it"},
            {"rank": 4, "postcode": "37121", "distance": 0.7, "distanceKmFromAirport": 14, "URL": "https://www.castelvecchiomuseo.comune.verona.it"},
            {"rank": 5, "postcode": "37123", "distance": 1.5, "distanceKmFromAirport": 15, "URL": "https://www.basilicasanzeno.it"},
            {"rank": 6, "postcode": "37121", "distance": 0.8, "distanceKmFromAirport": 14, "URL": "https://www.tourism.verona.it"},
            {"rank": 7, "postcode": "37121", "distance": 0.7, "distanceKmFromAirport": 14, "URL": "https://www.tourism.verona.it"},
            {"rank": 8, "postcode": "37121", "distance": 0.2, "distanceKmFromAirport": 14, "URL": "https://www.torredeilamberti.it"},
            {"rank": 9, "postcode": "37129", "distance": 0.8, "distanceKmFromAirport": 14, "URL": "https://www.giardinogiusti.com"},
            {"rank": 10, "postcode": "37121", "distance": 0.5, "distanceKmFromAirport": 14, "URL": "https://www.tourism.verona.it"},
        ]
    },
    "victoria_falls": {
        "things": [
            {"rank": 1, "postcode": "0363", "distance": 1.0, "distanceKmFromAirport": 20, "URL": "https://www.zimparks.org.zw"},
            {"rank": 2, "postcode": "0363", "distance": 2.0, "distanceKmFromAirport": 21, "URL": "https://www.tongabezi.com/devilspool"},
            {"rank": 3, "postcode": "0363", "distance": 2.5, "distanceKmFromAirport": 21, "URL": "https://www.safpar.net"},
            {"rank": 4, "postcode": "0363", "distance": 2.0, "distanceKmFromAirport": 21, "URL": "https://www.africaextreme.com"},
            {"rank": 5, "postcode": "0363", "distance": 4.0, "distanceKmFromAirport": 22, "URL": "https://www.wildhorisons.com"},
            {"rank": 6, "postcode": "0363", "distance": 5.0, "distanceKmFromAirport": 23, "URL": "https://www.zimparks.org.zw"},
            {"rank": 7, "postcode": "0363", "distance": 2.0, "distanceKmFromAirport": 21, "URL": "https://www.ulatravels.com"},
            {"rank": 8, "postcode": "0363", "distance": 3.0, "distanceKmFromAirport": 22, "URL": "https://www.theelephantcamp.com"},
            {"rank": 9, "postcode": "0363", "distance": 1.0, "distanceKmFromAirport": 20, "URL": "https://www.victoria-falls-hotel.com"},
            {"rank": 10, "postcode": "0363", "distance": 0.5, "distanceKmFromAirport": 19, "URL": ""},
        ]
    },
    "victoria_seychelles": {
        "things": [
            {"rank": 1, "postcode": "Praslin", "distance": 45.0, "distanceKmFromAirport": 50, "URL": "https://www.sif.sc/vallee-de-mai"},
            {"rank": 2, "postcode": "La Digue", "distance": 60.0, "distanceKmFromAirport": 65, "URL": "https://www.seychelles.travel"},
            {"rank": 3, "postcode": "Aldabra", "distance": 1150.0, "distanceKmFromAirport": 1155, "URL": "https://www.sif.sc/aldabra"},
            {"rank": 4, "postcode": "Victoria", "distance": 0.3, "distanceKmFromAirport": 11, "URL": "https://www.seychelles.travel"},
            {"rank": 5, "postcode": "Beau Vallon", "distance": 8.0, "distanceKmFromAirport": 6, "URL": "https://www.seychelles.travel"},
            {"rank": 6, "postcode": "Victoria", "distance": 0.3, "distanceKmFromAirport": 11, "URL": "https://www.seychelles.travel"},
            {"rank": 7, "postcode": "Mahé", "distance": 5.0, "distanceKmFromAirport": 14, "URL": "https://www.seychelles.travel"},
            {"rank": 8, "postcode": "Praslin", "distance": 45.0, "distanceKmFromAirport": 50, "URL": "https://www.seychelles.travel"},
            {"rank": 9, "postcode": "Victoria", "distance": 0.2, "distanceKmFromAirport": 11, "URL": ""},
            {"rank": 10, "postcode": "Victoria", "distance": 0.5, "distanceKmFromAirport": 11, "URL": "https://www.creolefestival.com"},
        ]
    },
    "vientiane": {
        "things": [
            {"rank": 1, "postcode": "0100", "distance": 4.0, "distanceKmFromAirport": 8, "URL": "https://www.tourismlaos.org"},
            {"rank": 2, "postcode": "0100", "distance": 2.0, "distanceKmFromAirport": 6, "URL": "https://www.tourismlaos.org"},
            {"rank": 3, "postcode": "0100", "distance": 25.0, "distanceKmFromAirport": 27, "URL": "https://www.tourismlaos.org"},
            {"rank": 4, "postcode": "0100", "distance": 1.5, "distanceKmFromAirport": 5, "URL": "https://www.tourismlaos.org"},
            {"rank": 5, "postcode": "0100", "distance": 1.5, "distanceKmFromAirport": 5, "URL": "https://www.tourismlaos.org"},
            {"rank": 6, "postcode": "0100", "distance": 1.0, "distanceKmFromAirport": 5, "URL": ""},
            {"rank": 7, "postcode": "0100", "distance": 1.0, "distanceKmFromAirport": 5, "URL": ""},
            {"rank": 8, "postcode": "0600", "distance": 150.0, "distanceKmFromAirport": 153, "URL": "https://www.tourismlaos.org"},
            {"rank": 9, "postcode": "0100", "distance": 2.0, "distanceKmFromAirport": 6, "URL": "https://www.copelaos.org"},
            {"rank": 10, "postcode": "0100", "distance": 1.0, "distanceKmFromAirport": 5, "URL": "https://www.tourismlaos.org"},
        ]
    },
    "vilnius": {
        "things": [
            {"rank": 1, "postcode": "LT-01100", "distance": 0.3, "distanceKmFromAirport": 6, "URL": "https://www.vilnius-tourism.lt"},
            {"rank": 2, "postcode": "LT-01108", "distance": 0.5, "distanceKmFromAirport": 6, "URL": "https://www.lnm.lt/en/gediminas-tower"},
            {"rank": 3, "postcode": "LT-01143", "distance": 0.2, "distanceKmFromAirport": 6, "URL": "https://www.vilnius-tourism.lt"},
            {"rank": 4, "postcode": "LT-01202", "distance": 1.0, "distanceKmFromAirport": 7, "URL": "https://www.uzupis.lt"},
            {"rank": 5, "postcode": "LT-01135", "distance": 0.8, "distanceKmFromAirport": 6, "URL": "https://www.ausrosvartai.lt"},
            {"rank": 6, "postcode": "LT-01122", "distance": 0.4, "distanceKmFromAirport": 6, "URL": "https://www.vu.lt"},
            {"rank": 7, "postcode": "LT-01100", "distance": 0.7, "distanceKmFromAirport": 7, "URL": "https://www.genocid.lt/muziejus"},
            {"rank": 8, "postcode": "LT-01109", "distance": 0.6, "distanceKmFromAirport": 6, "URL": "https://www.vilnius-tourism.lt"},
            {"rank": 9, "postcode": "LT-21101", "distance": 28.0, "distanceKmFromAirport": 32, "URL": "https://www.trakaimuziejus.lt"},
            {"rank": 10, "postcode": "LT-01124", "distance": 0.5, "distanceKmFromAirport": 6, "URL": "https://www.vilnius-tourism.lt"},
        ]
    },
    "weeze": {
        "things": [
            {"rank": 1, "postcode": "46509", "distance": 20.0, "distanceKmFromAirport": 22, "URL": "https://www.apx.de"},
            {"rank": 2, "postcode": "47546", "distance": 10.0, "distanceKmFromAirport": 12, "URL": "https://www.wunderlandkalkar.eu"},
            {"rank": 3, "postcode": "47623", "distance": 8.0, "distanceKmFromAirport": 10, "URL": "https://www.kevelaer.de"},
            {"rank": 4, "postcode": "47574", "distance": 9.0, "distanceKmFromAirport": 11, "URL": "https://www.goch.de"},
            {"rank": 5, "postcode": "47652", "distance": 8.0, "distanceKmFromAirport": 9, "URL": ""},
            {"rank": 6, "postcode": "47608", "distance": 13.0, "distanceKmFromAirport": 15, "URL": "https://www.geldern.de"},
            {"rank": 7, "postcode": "47574", "distance": 9.0, "distanceKmFromAirport": 11, "URL": "https://www.museumgoch.de"},
            {"rank": 8, "postcode": "47652", "distance": 5.0, "distanceKmFromAirport": 7, "URL": ""},
            {"rank": 9, "postcode": "47574", "distance": 6.0, "distanceKmFromAirport": 8, "URL": ""},
            {"rank": 10, "postcode": "47647", "distance": 3.0, "distanceKmFromAirport": 5, "URL": ""},
        ]
    },
    "wellington": {
        "things": [
            {"rank": 1, "postcode": "6011", "distance": 1.0, "distanceKmFromAirport": 7, "URL": "https://www.tepapa.govt.nz"},
            {"rank": 2, "postcode": "6011", "distance": 0.5, "distanceKmFromAirport": 8, "URL": "https://www.wellingtoncablecar.co.nz"},
            {"rank": 3, "postcode": "6022", "distance": 7.0, "distanceKmFromAirport": 2, "URL": "https://www.wetaworkshop.com"},
            {"rank": 4, "postcode": "6011", "distance": 0.5, "distanceKmFromAirport": 7, "URL": "https://www.wellingtonnz.com"},
            {"rank": 5, "postcode": "6011", "distance": 2.0, "distanceKmFromAirport": 7, "URL": "https://www.wellingtonnz.com"},
            {"rank": 6, "postcode": "6011", "distance": 0.8, "distanceKmFromAirport": 9, "URL": "https://www.wellingtonnz.com"},
            {"rank": 7, "postcode": "6012", "distance": 3.0, "distanceKmFromAirport": 11, "URL": "https://www.visitzealandia.com"},
            {"rank": 8, "postcode": "5771", "distance": 75.0, "distanceKmFromAirport": 80, "URL": "https://www.wairarapatourism.co.nz"},
            {"rank": 9, "postcode": "6160", "distance": 0.5, "distanceKmFromAirport": 8, "URL": "https://www.parliament.nz"},
            {"rank": 10, "postcode": "6021", "distance": 3.0, "distanceKmFromAirport": 5, "URL": "https://www.wellingtonzoo.com"},
        ]
    },
    "windhoek": {
        "things": [
            {"rank": 1, "postcode": "15001", "distance": 350.0, "distanceKmFromAirport": 385, "URL": "https://www.nwr.com.na"},
            {"rank": 2, "postcode": "31001", "distance": 435.0, "distanceKmFromAirport": 472, "URL": "https://www.namibiawildlife.org"},
            {"rank": 3, "postcode": "2812", "distance": 540.0, "distanceKmFromAirport": 576, "URL": "https://www.namibiatourism.com.na"},
            {"rank": 4, "postcode": "10005", "distance": 0.5, "distanceKmFromAirport": 42, "URL": "https://www.namibiatourism.com.na"},
            {"rank": 5, "postcode": "10005", "distance": 0.3, "distanceKmFromAirport": 42, "URL": "https://www.namibiatourism.com.na"},
            {"rank": 6, "postcode": "10003", "distance": 4.0, "distanceKmFromAirport": 46, "URL": "https://www.namibiatourism.com.na"},
            {"rank": 7, "postcode": "10005", "distance": 0.5, "distanceKmFromAirport": 42, "URL": "https://www.namibiatourism.com.na"},
            {"rank": 8, "postcode": "22000", "distance": 360.0, "distanceKmFromAirport": 393, "URL": "https://www.namibiatourism.com.na"},
            {"rank": 9, "postcode": "10000", "distance": 35.0, "distanceKmFromAirport": 8, "URL": "https://www.cheetah.org"},
            {"rank": 10, "postcode": "10003", "distance": 4.0, "distanceKmFromAirport": 46, "URL": ""},
        ]
    },
    "wroclaw": {
        "things": [
            {"rank": 1, "postcode": "50-101", "distance": 0.1, "distanceKmFromAirport": 13, "URL": "https://www.wroclaw.pl"},
            {"rank": 2, "postcode": "51-618", "distance": 4.0, "distanceKmFromAirport": 17, "URL": "https://www.halastulecia.pl"},
            {"rank": 3, "postcode": "50-330", "distance": 1.5, "distanceKmFromAirport": 14, "URL": "https://www.katedra.archidiecezja.wroc.pl"},
            {"rank": 4, "postcode": "50-011", "distance": 1.0, "distanceKmFromAirport": 14, "URL": "https://www.panoramaraclawicka.pl"},
            {"rank": 5, "postcode": "50-101", "distance": 0.5, "distanceKmFromAirport": 13, "URL": "https://www.krasnale.pl"},
            {"rank": 6, "postcode": "50-153", "distance": 1.0, "distanceKmFromAirport": 14, "URL": "https://www.mnwr.pl"},
            {"rank": 7, "postcode": "51-618", "distance": 4.0, "distanceKmFromAirport": 17, "URL": "https://www.zoo.wroclaw.pl"},
            {"rank": 8, "postcode": "50-329", "distance": 1.5, "distanceKmFromAirport": 14, "URL": "https://www.wroclaw.pl"},
            {"rank": 9, "postcode": "50-328", "distance": 1.5, "distanceKmFromAirport": 14, "URL": "https://www.ogrodbotaniczny.uni.wroc.pl"},
            {"rank": 10, "postcode": "50-101", "distance": 0.1, "distanceKmFromAirport": 13, "URL": "https://www.wroclaw.pl"},
        ]
    },
    "wuhan": {
        "things": [
            {"rank": 1, "postcode": "430060", "distance": 1.0, "distanceKmFromAirport": 31, "URL": "http://www.whyct.com.cn"},
            {"rank": 2, "postcode": "430072", "distance": 10.0, "distanceKmFromAirport": 39, "URL": "http://www.eastlake.gov.cn"},
            {"rank": 3, "postcode": "430060", "distance": 9.0, "distanceKmFromAirport": 38, "URL": "http://www.hbww.org"},
            {"rank": 4, "postcode": "430072", "distance": 11.0, "distanceKmFromAirport": 40, "URL": "https://www.whu.edu.cn"},
            {"rank": 5, "postcode": "430050", "distance": 3.0, "distanceKmFromAirport": 32, "URL": ""},
            {"rank": 6, "postcode": "430063", "distance": 1.5, "distanceKmFromAirport": 31, "URL": ""},
            {"rank": 7, "postcode": "430022", "distance": 4.0, "distanceKmFromAirport": 28, "URL": ""},
            {"rank": 8, "postcode": "430072", "distance": 12.0, "distanceKmFromAirport": 41, "URL": "https://www.wuhanhanshow.com"},
            {"rank": 9, "postcode": "430300", "distance": 35.0, "distanceKmFromAirport": 5, "URL": ""},
            {"rank": 10, "postcode": "430060", "distance": 1.0, "distanceKmFromAirport": 31, "URL": ""},
        ]
    },
}

def update_city_file(city_key, updates):
    filepath = os.path.join(base_path, f"{city_key}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    updates_by_rank = {u["rank"]: u for u in updates["things"]}

    new_things = []
    for thing in data["things"]:
        rank = thing["rank"]
        upd = updates_by_rank.get(rank, {})
        new_thing = {
            "rank": thing["rank"],
            "name": thing["name"],
            "postcode": upd.get("postcode", thing.get("postcode", "")),
            "distanceKmFromAirport": upd.get("distanceKmFromAirport", thing.get("distanceKmFromAirport", None)),
            "description": thing["description"],
            "distance": upd.get("distance", thing.get("distance", None)),
            "URL": upd.get("URL", thing.get("URL", "")),
        }
        new_things.append(new_thing)

    data["things"] = new_things

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated: {filepath}")

for city_key, updates in cities_data.items():
    update_city_file(city_key, updates)

print("All done!")
