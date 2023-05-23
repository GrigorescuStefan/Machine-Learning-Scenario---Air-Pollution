# Machine-Learning-Scenario - Air-Pollution

I trained a model on my air-pollution data from my Firestore Database to accurately determine what AQI (Air Quality Index) is fit for a certain set of data.

Steps:
- Connected to the Firestore Database using the serviceAccountKey.json and saved it to a CSV (the limit of 50k reads and writes doesn't allow me to train the model directly on the data in my database)
- Filled the gaps in said CSV using an open-source Geocoding API - 
    https://open-meteo.com/en/docs/geocoding-api
- Trained a model on the data in the CSV using the library scikit-learn, and the RandomForestClassifier algorithm
- Tested said model on a new set of data to check for AQI Accuracy
