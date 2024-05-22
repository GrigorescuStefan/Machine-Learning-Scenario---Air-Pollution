import csv
import json
import requests

csv_file = 'air_pollution.csv'
temp_file = 'processed_air_pollution.csv'
country_codes_file = 'country_codes.json'

def load_country_codes(filename): 
    with open(filename, 'r') as file:
        return json.load(file)    
country_codes = load_country_codes(country_codes_file)

def search_csv(filename, temporary_file):
    with open(filename, 'r') as file:
        temp = open(temporary_file, 'a', newline='')
        writer = csv.writer(temp)
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows:
            if row[0] == '':
                country = call_api(row[11])
                if country:
                    row[0] = country
                    writer.writerow(row)
            else:
                writer.writerow(row)
        temp.close()
    print("Finished writing the CSV file.")
    # input("Press any key to close...")
    return None

def call_api(city_name):
    api_url_original = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    # formateaza 'Torre Del Greco' in 'Torre+Del+Greco' in URL

    formatted_city_name = city_name.replace(' ', '-')
    api_url_formatted = f"https://geocoding-api.open-meteo.com/v1/search?name={formatted_city_name}&count=1&language=en&format=json"
    # formateaza 'Lapu Lapu' in 'Lapu-Lapu' in URL

    response = requests.get(api_url_original)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            result = data['results'][0]
            return handle_result(result)

    response = requests.get(api_url_formatted)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            result = data['results'][0]
            return handle_result(result)

    print(f"The API cannot find the details for {city_name}.")
    return None

def handle_result(result):
    country = result.get('country')
    if not country:
        country_code = result.get('country_code')
        if country_code:
            return country_codes[country_code]
    return country

search_csv(csv_file, temp_file)
