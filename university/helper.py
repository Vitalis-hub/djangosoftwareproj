import requests
import re


def get_directions(origin, destination):
    query = {
        "origin": origin,
        "destination": destination,
        "key": "AIzaSyCt5UgnRu8VgbuyPR7MMl4FKk3bjhWl2qg",
        "travel_mode": "WALKING",
    }

    response = requests.get("https://maps.googleapis.com/maps/api/directions/json?", params=query)
    cleanr = re.compile('<.*?>')
    cleaned_direction_list = []
    for item in response.json()['routes'][0]['legs'][0]['steps']:
        raw_text = item['html_instructions']
        clean_text = re.sub(cleanr, '', raw_text)
        cleaned_direction_list.append(clean_text)
    return cleaned_direction_list
