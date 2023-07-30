import json
from math import asin, sin, cos, sqrt, radians
from typing import Any

import requests


def update_text(text: str):
    return text.replace('.', '\.').replace('-', '\-').replace('(', '\(').replace(")", "\)")


def geocoder(name: str, city: str, address: str) -> tuple:
    req_url: str = 'https://nominatim.openstreetmap.org/search'
    params1: dict = {'city': city, 'street': address, 'format': 'json', 'addressdetails': 1}
    params2: dict = {'city': city, 'street': name, 'format': 'json', 'addressdetails': 1}
    if requests.get(req_url, params=params1).text != '[]':
        shop_info: dict = json.loads(requests.get(req_url, params=params1).text)[0]
        return float(shop_info['lat']), float(shop_info['lon'])
    elif requests.get(req_url, params=params2).text != '[]':
        shop_info: dict = json.loads(requests.get(req_url, params=params1).text)[0]
        return float(shop_info['lat']), float(shop_info['lon'])
    else:
        return 0, 0


async def save_to_database(data: dict, user_id: str) -> None:
    with open("services/coffeeshops.json", "r") as file:
        database: dict = json.loads(file.read())
    cafe_name: str = data.pop('name')
    lat, lon = geocoder(cafe_name, data['city'], data['address'])
    data['lat'] = lat
    data['lon'] = lon

    database[user_id] = database.get(user_id, {})
    database[user_id][cafe_name] = data
    with open("services/coffeeshops.json", "w") as file:
        json.dump(database, file)


def print_entry(entry: tuple, lg_code: str, user_id: str) -> tuple:
    name, dist = entry[0], str(round(entry[1], 1)).replace('.', '\.')
    with open("services/coffeeshops.json", "r") as file:
        database: dict = json.loads(file.read())
    cshop: dict = database[user_id][name]

    if lg_code == 'ru':
        entry_string: str = f'{name}\n📍{cshop["address"] + ", " + cshop["city"]}\n{dist} км от вас\n\n{cshop["description"]}\n\nРейтинг: {cshop["rating"]}⭐'
    else:
        entry_string: str = f'{name}\n📍{cshop["address"] + ", " + cshop["city"]}{dist} km from you\n\n{cshop["description"]}\n\nRating: {cshop["rating"]}⭐'
    return entry_string, cshop['file_id']


def count_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r: int = 6371
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    return 2 * r * asin(sqrt(sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2))


async def find_three_nearest(lat1: float, lon1: float, user_id: str):
    with open("services/coffeeshops.json", "r") as file:
        database: dict = json.loads(file.read())
    dist_ratio = []
    user_database = database[user_id]
    for name, cshop in user_database.items():
        lat2, lon2 = cshop['lat'], cshop['lon']
        dist = count_distance(lat1, lon1, lat2, lon2)
        dist_ratio.append(tuple)
    return sorted(dist_ratio, key=lambda x: x[1])[:3]
