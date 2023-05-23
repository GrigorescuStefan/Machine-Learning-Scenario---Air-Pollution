import csv
import requests

csv_file = 'air_pollution.csv'
temp_file = 'temp_air_pollution.csv'

def search_csv(filename, temporary_file):
    with open(filename, 'r') as file:
        temp = open(temporary_file, 'a', newline='')
        writer = csv.writer(temp)
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows:
            if row[0] == '':
                row[0] = call_api(row[11])
            writer.writerow(row)
    return None

def call_api(city_name):
    api_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['results'][0]['country']
    else:
        print(f"Request failed with status code {response.status_code}.")
        return None

search_csv(csv_file, temp_file)
