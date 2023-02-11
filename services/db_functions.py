import json
from typing import Any
import requests


def geocoder(name: str, city: str, address: str)-> tuple[float, float]:
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


async def save_to_database(data: dict[str, Any]):
    with open("services/coffeeshops.json", "r") as file:
        database: dict[str, dict] = json.loads(file.read())
    cafe_name: str = data.pop('name')
    lat, lon = geocoder(cafe_name, data['city'], data['address'])
    data['lat'] = lat
    data['lon'] = lon
    database[cafe_name] = data
    with open("services/coffeeshops.json", "w") as file:
        json.dump(database, file)
