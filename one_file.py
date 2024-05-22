import firebase_admin
from firebase_admin import credentials, firestore
import csv
import json
import requests
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import joblib

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_ref = db.collection('air_pollution')

print("Starting Air Quality Machine Learning prediction algorithm!")

def firestore_to_csv(filename):
    print("Connecting to Firestore Databse to retrieve data...")
    data = [doc.to_dict() for doc in collection_ref.stream()]
    fieldnames = data[0].keys()
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def load_country_codes(filename):
    print("Loading Country Codes JSON...")
    with open(filename, 'r') as file:
        return json.load(file)

def search_csv(filename, temporary_file, country_codes):
    print("\nSearching entire CSV file for missing items...")
    with open(filename, 'r') as file:
        temp = open(temporary_file, 'a', newline='')
        writer = csv.writer(temp)
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows:
            if row[0] == '':
                country = call_api(row[11], country_codes)
                if country:
                    row[0] = country
                    writer.writerow(row)
            else:
                writer.writerow(row)
        temp.close()
    print("Finished writing the CSV file.")
    # input("Press any key to close...")
    return None

def call_api(city_name, country_codes):
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
            return handle_result(result, country_codes)

    response = requests.get(api_url_formatted)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            result = data['results'][0]
            return handle_result(result, country_codes)

    print(f"The API cannot find the details for {city_name}.")
    return None

def handle_result(result, country_codes):
    country = result.get('country')
    if not country:
        country_code = result.get('country_code')
        if country_code:
            return country_codes[country_code]
    return country

def train_model(processed_csv_file, model_file, label_encoder_file):
    print("\nProceeding with modifying the final data for training...")
    data = pd.read_csv(processed_csv_file)

    print("Dropping columns 'Country' and 'City' as they are irrelevant...")
    data = data.drop(['Country', 'City'], axis=1)

    print("Encodes the string values into numerical ones using LabelEncoder...")
    label_encoder = LabelEncoder()
    categorical_cols = ['AQI Category', 'CO AQI Category', 'Ozone AQI Category', 'NO2 AQI Category', 'PM2.5 AQI Category']
    for col in categorical_cols:
        data[col] = label_encoder.fit_transform(data[col])

    print("Dropping column 'AQI Category' from the train data and only keeping said column for the test data...")
    X = data.drop('AQI Category', axis=1)
    y = data['AQI Category']

    print("Splitting data 80% to training, and 20% to testing...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Random state makes sure the training and test data are split exactly at the same place, to keep consistent, number is chosen arbitrarily

    print("Using the RandomForestClassifier model to determine the outcome...")
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    joblib.dump(model, model_file)
    joblib.dump(label_encoder, label_encoder_file)

    return X_train

def make_predictions(model_file, label_encoder_file, X_train):
    model = joblib.load(model_file)
    label_encoder = joblib.load(label_encoder_file)

    new_data = pd.DataFrame({
        'NO2 AQI Value': [0],
        'CO AQI Category': ['Good'],
        'PM2.5 AQI Value': [120],
        'CO AQI Value': [1],
        'Ozone AQI Category': ['Moderate'],
        'NO2 AQI Category': ['Good'],
        'Ozone AQI Value': [50],
        'PM2.5 AQI Category': ['Moderate'],
        'AQI Value': [49]
    })

    print("\nTesting new data with the model to determine if the values are correct...")
    new_data = new_data[X_train.columns]
    categorical_cols = ['CO AQI Category', 'Ozone AQI Category', 'NO2 AQI Category', 'PM2.5 AQI Category']
    for col in categorical_cols:
        new_data[col] = label_encoder.transform(new_data[col])

    predictions = model.predict(new_data)

    reverse_mapping = {label_encoder.transform([category])[0]: category for category in label_encoder.classes_}
    predicted_labels = [reverse_mapping[prediction] for prediction in predictions]

    print("New Input Data:")
    print(new_data.to_string(index=False))
    print("\nPredicted AQI Category:", predicted_labels)

def main():
    csv_file = 'air_pollution.csv'
    processed_csv_file = 'processed_air_pollution.csv'
    country_codes_file = 'country_codes.json'
    model_file = 'AQI_Category.joblib'
    label_encoder_file = 'Label_Encoder.joblib'

    firestore_to_csv(csv_file)

    country_codes = load_country_codes(country_codes_file)

    search_csv(csv_file, processed_csv_file, country_codes)

    X_train = train_model(processed_csv_file, model_file, label_encoder_file)

    make_predictions(model_file, label_encoder_file, X_train)

if __name__ == "__main__":
    main()
