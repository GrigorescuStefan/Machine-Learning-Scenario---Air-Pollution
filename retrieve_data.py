import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

collection_ref = db.collection('air_pollution')

data = [doc.to_dict() for doc in collection_ref.stream()]

fieldnames = data[0].keys()
filename = 'air_pollution.csv'

with open(filename, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)