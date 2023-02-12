import json
from math import asin, sin, cos, sqrt, radians
from typing import Any

import requests


def geocoder(name: str, city: str, address: str) -> tuple[float, float]:
    req_url: str = 'https://nominatim.openstreetmap.org/search'
    params1: dict[str, Any] = {'city': city, 'street': address, 'format': 'json', 'addressdetails': 1}
    params2: dict[str, Any] = {'city': city, 'street': name, 'format': 'json', 'addressdetails': 1}
    if requests.get(req_url, params=params1).text != '[]':
        shop_info: dict[str, Any] = json.loads(requests.get(req_url, params=params1).text)[0]
        return float(shop_info['lat']), float(shop_info['lon'])
    elif requests.get(req_url, params=params2).text != '[]':
        shop_info: dict[str, Any] = json.loads(requests.get(req_url, params=params1).text)[0]
        return float(shop_info['lat']), float(shop_info['lon'])
    else:
        return 0, 0


async def save_to_database(data: dict[str, Any]) -> None:
    with open("services/coffeeshops.json", "r") as file:
        database: dict[str, dict] = json.loads(file.read())
    cafe_name: str = data.pop('name')
    lat, lon = geocoder(cafe_name, data['city'], data['address'])
    data['lat'] = lat
    data['lon'] = lon
    database[cafe_name] = data
    with open("services/coffeeshops.json", "w") as file:
        json.dump(database, file)


def print_entry(entry: tuple[str, float], lg_code: str) -> tuple[str, str]:
    name, dist = entry[0], str(round(entry[1], 1)).replace('.', '\.')
    with open("services/coffeeshops.json", "r") as file:
        database: dict[str, dict] = json.loads(file.read())
    cshop: dict[str, Any] = database[name]
    if lg_code == 'ru':
        is_food: str = 'Есть' if cshop['food'] else 'Нет'
        entry_string: str = f'{dist} км от вас\nНазвание: {name}\nАдрес: {cshop["address"] + ", " + cshop["city"]}\nЕда: {is_food}\nЦена за латте: {cshop["latte_price"]}'
    else:
        is_food: str = 'Yes' if cshop['food'] else 'No'
        entry_string: str = f'{dist} km from you\nName: {name}\nAddress: {cshop["address"] + ", " + cshop["city"]}\nFood: {is_food}\nLatte price: {cshop["latte_price"]}'
    return entry_string, cshop['file_id']


def count_distance(lat1, lon1, lat2, lon2) -> float:
    r: int = 6371
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    return 2 * r * asin(sqrt(sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2))


async def find_three_nearest(lat1, lon1):
    with open("services/coffeeshops.json", "r") as file:
        database: dict[str, dict] = json.loads(file.read())
    dist_ratio = []
    for name, cshop in database.items():
        lat2, lon2 = cshop['lat'], cshop['lon']
        dist = count_distance(lat1, lon1, lat2, lon2)
        dist_ratio.append(tuple([name, dist]))
    return sorted(dist_ratio, key=lambda x: x[1])[:3]
