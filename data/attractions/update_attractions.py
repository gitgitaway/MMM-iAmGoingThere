import json
import os

base_path = r'c:\Users\junkp\MagicMirror\modules\MMM-iAmGoingThere\data\attractions'

# {city: {rank: (postcode, distance_from_city_km, distance_from_airport_km, url)}}
city_updates = {
    'roseau': {
        1:  ('',    13.0,  55, 'https://dominica.dm/'),
        2:  ('',     9.0,  57, 'https://dominica.dm/'),
        3:  ('',    11.0,  59, 'https://dominica.dm/'),
        4:  ('',    12.0,  55, 'https://whc.unesco.org/en/list/814'),
        5:  ('',    50.0,  25, 'https://kalinagobaranaaute.com/'),
        6:  ('',     1.0,  50, 'https://dominica.dm/'),
        7:  ('',     0.0,  50, ''),
        8:  ('',    40.0,  20, 'https://dominica.dm/'),
        9:  ('',     8.0,  56, 'https://dominica.dm/'),
        10: ('',     0.0,  50, ''),
    },
    'sal': {
        1:  ('7601', 12.0,  14, 'https://www.visitcaboverde.com/'),
        2:  ('7601', 12.0,  14, ''),
        3:  ('7600', 10.0,  10, 'https://www.pedrasdelume.com/'),
        4:  ('7601', 15.0,  17, ''),
        5:  ('7600',  0.0,   2, ''),
        6:  ('7600', 10.0,  12, ''),
        7:  ('7601', 12.0,  14, 'https://www.turtlescaboverde.com/'),
        8:  ('7600',  0.0, 220, ''),
        9:  ('7600',  0.0, 160, 'https://whc.unesco.org/en/list/1310'),
        10: ('7600',  0.0,   2, ''),
    },
    'salalah': {
        1:  ('211',   0.0,  15, 'https://www.omantourism.gov.om/'),
        2:  ('211',   5.0,  18, ''),
        3:  ('219',  35.0,  45, ''),
        4:  ('211',   3.0,  17, 'https://whc.unesco.org/en/list/1010'),
        5:  ('211',   3.0,  17, 'https://www.omantourism.gov.om/'),
        6:  ('218',  38.0,  50, ''),
        7:  ('217',  40.0,  50, ''),
        8:  ('219',  30.0,  40, ''),
        9:  ('211',   2.0,  16, ''),
        10: ('218',  80.0,  90, ''),
    },
    'samarkand': {
        1:  ('140100',  1.0,  13, 'https://en.uzbektourism.uz/'),
        2:  ('140100',  1.5,  13, ''),
        3:  ('140100',  1.0,  13, ''),
        4:  ('140100',  2.0,  14, ''),
        5:  ('140100',  3.0,  14, ''),
        6:  ('140100',  2.5,  14, ''),
        7:  ('140100',  1.0,  13, ''),
        8:  ('140100',  2.0,  14, ''),
        9:  ('140100',  3.0,  14, 'https://www.samarkandwine.com/'),
        10: ('140141',  5.0,  16, ''),
    },
    'san_jose': {
        1:  ('21007', 150.0, 165, 'https://www.sinac.go.cr/'),
        2:  ('50402', 135.0, 148, 'https://www.monteverdeinfo.com/'),
        3:  ('60601', 180.0, 195, 'https://www.sinac.go.cr/'),
        4:  ('10101',   0.5,  20, 'https://www.teatronacional.go.cr/'),
        5:  ('10101',   0.5,  20, ''),
        6:  ('70601', 250.0, 265, 'https://www.sinac.go.cr/'),
        7:  ('10101',   0.5,  20, 'https://www.museosdelbancocentral.org/'),
        8:  ('20501',  58.0,  45, 'https://www.sinac.go.cr/'),
        9:  ('70101', 160.0, 150, 'https://www.slothsanctuary.com/'),
        10: ('40901',  20.0,  15, 'https://www.cafebritt.com/'),
    },
    'san_pedro_sula': {
        1:  ('41101', 170.0, 180, 'https://www.ihah.hn/'),
        2:  ('21101',   0.0,  14, ''),
        3:  ('21101',   1.0,  15, 'https://www.ihah.hn/'),
        4:  ('21101',  20.0,  20, ''),
        5:  ('27103',  80.0,  88, ''),
        6:  ('21101',  35.0,  40, ''),
        7:  ('21101',  30.0,  40, ''),
        8:  ('21101',   5.0,  15, 'https://citymallhn.com/'),
        9:  ('34101',  60.0,  70, 'https://www.roatanonline.com/'),
        10: ('21101',   0.0,  14, ''),
    },
    'san_salvador': {
        1:  ('2101',  70.0, 100, ''),
        2:  ('2101',  78.0, 105, ''),
        3:  ('1101',   3.0,  46, 'https://www.cultura.gob.sv/'),
        4:  ('1101',   0.5,  44, ''),
        5:  ('1101',   1.0,  44, ''),
        6:  ('1101',   3.0,  46, ''),
        7:  ('1602',  35.0,  60, 'https://whc.unesco.org/en/list/675'),
        8:  ('1601',  40.0,  35, ''),
        9:  ('2302', 130.0, 165, ''),
        10: ('1101',   0.0,  44, ''),
    },
    'sanaa': {
        1:  ('11110',    0.0,   15, 'https://whc.unesco.org/en/list/385'),
        2:  ('11110',    0.0,   15, ''),
        3:  ('11110',    0.0,   15, ''),
        4:  ('11110',    3.0,   17, ''),
        5:  ('11110',    0.0,   15, ''),
        6:  ('11110',    1.0,   16, ''),
        7:  ('11110',   15.0,   25, ''),
        8:  ('11110',   15.0,   25, ''),
        9:  ('11110', 1100.0, 1100, 'https://whc.unesco.org/en/list/1263'),
        10: ('11110',    0.0,   15, ''),
    },
    'santa_cruz': {
        1:  ('',  220.0, 230, 'https://whc.unesco.org/en/list/529'),
        2:  ('',  130.0, 140, ''),
        3:  ('',  120.0, 130, 'https://whc.unesco.org/en/list/567'),
        4:  ('',   15.0,  28, ''),
        5:  ('',    0.0,  15, ''),
        6:  ('',   90.0,  95, ''),
        7:  ('',   20.0,  30, ''),
        8:  ('',   15.0,  25, 'https://www.guembe.com.bo/'),
        9:  ('',    0.0,  15, ''),
        10: ('',    0.0,  15, ''),
    },
    'santo_domingo': {
        1:  ('10210',   0.0,  30, 'https://whc.unesco.org/en/list/526'),
        2:  ('10210',   0.0,  30, 'https://www.museoalcazardecolon.gob.do/'),
        3:  ('10210',   0.0,  30, ''),
        4:  ('10205',   5.0,  25, ''),
        5:  ('10210',   0.0,  30, ''),
        6:  ('10210',   0.0,  30, 'https://www.museodelascasasreales.gov.do/'),
        7:  ('10210',   0.0,  30, ''),
        8:  ('32000', 240.0, 265, 'https://www.gosamana.com/'),
        9:  ('23000', 200.0, 170, 'https://www.puntacana.com/'),
        10: ('10210',   1.0,  30, ''),
    },
    'sanya': {
        1:  ('572013',  18.0,  40, ''),
        2:  ('572025',  23.0,   8, ''),
        3:  ('572014',  40.0,  15, 'https://www.nanshan.com.cn/'),
        4:  ('572022',  25.0,  48, ''),
        5:  ('572000',   3.0,  27, ''),
        6:  ('572022',  30.0,  52, ''),
        7:  ('572000',  15.0,  37, ''),
        8:  ('572000',  25.0,  45, 'https://www.missionhillschina.com/'),
        9:  ('572000',   2.0,  26, ''),
        10: ('572000',   0.0,  25, ''),
    },
    'sao_tome': {
        1:  ('',   0.0,   6, ''),
        2:  ('',  40.0,  45, ''),
        3:  ('',  13.0,  18, ''),
        4:  ('',  20.0,  25, ''),
        5:  ('',  55.0,  60, ''),
        6:  ('',  15.0,  20, ''),
        7:  ('',  10.0,  15, ''),
        8:  ('', 150.0, 155, ''),
        9:  ('',   0.0,   6, ''),
        10: ('',   0.0,   6, ''),
    },
    'shenzhen': {
        1:  ('518054',  12.0,  22, 'https://www.octloft.cn/'),
        2:  ('518054',  13.0,  21, 'https://www.szwow.com.cn/'),
        3:  ('518112',  15.0,  40, ''),
        4:  ('518000',   1.0,  31, ''),
        5:  ('518054',  13.0,  21, ''),
        6:  ('518054',  10.0,  23, ''),
        7:  ('518000',   2.0,  31, ''),
        8:  ('518054',  12.0,  22, 'https://sz.happyvalley.cn/'),
        9:  ('518120',  50.0,  80, ''),
        10: ('518000',   2.0,  32, ''),
    },
    'shiraz': {
        1:  ('73711',  60.0,  49, 'https://www.persepolis.ir/'),
        2:  ('71348',   1.0,  12, ''),
        3:  ('71379',   2.0,  11, 'https://www.hafezieh.ir/'),
        4:  ('73711',  55.0,  45, ''),
        5:  ('71878',   3.0,  13, ''),
        6:  ('71356',   0.5,  12, ''),
        7:  ('71358',   0.5,  12, ''),
        8:  ('71956',   4.0,  13, 'https://www.saadiah.ir/'),
        9:  ('71358',   0.5,  12, ''),
        10: ('73641', 120.0, 110, ''),
    },
    'siem_reap': {
        1:  ('170201',   6.0,  13, 'https://www.apsara.gov.kh/'),
        2:  ('170201',   9.0,  16, 'https://www.apsara.gov.kh/'),
        3:  ('170201',  10.0,  17, 'https://www.apsara.gov.kh/'),
        4:  ('170201',   6.0,  13, 'https://www.apsara.gov.kh/'),
        5:  ('170201',  25.0,  32, 'https://www.apsara.gov.kh/'),
        6:  ('170201',   0.0,   9, ''),
        7:  ('170201',  15.0,  22, ''),
        8:  ('170201',   2.0,  10, 'https://www.angkornationalmuseum.com/'),
        9:  ('170201',   2.0,  10, 'https://pharecircus.org/'),
        10: ('170201',  68.0,  75, 'https://www.apsara.gov.kh/'),
    },
}

for city, rank_data in city_updates.items():
    filepath = os.path.join(base_path, f'{city}.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_things = []
    for thing in data['things']:
        rank = thing['rank']
        postcode, distance, dist_airport, url = rank_data[rank]
        new_thing = {
            'rank': thing['rank'],
            'name': thing['name'],
            'postcode': postcode,
            'distanceKmFromAirport': dist_airport,
            'description': thing['description'],
            'distance': distance,
            'URL': url,
        }
        new_things.append(new_thing)

    data['things'] = new_things

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'Updated {city}.json')

print('All done.')
