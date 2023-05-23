import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

from data_classification import X_train

# Modelul antrenat propriu-zis
model = joblib.load('AQI_Category.joblib')

# Preiau label encoder-ul de la training, ca sa stiu ce date am, de pe ce coloane si ce mai trebuie sa adaug
label_encoder = joblib.load('Label_Encoder.joblib')

# Prepare the new input data
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
# AQI Values from 51 and up are considered Moderate, and from 100 it's already Unhealthy
# I need to mention the other factors contribute a lot, but AQI Value is the primary one


# Rearanjez coloanele sa arate exact la fel ca in timpul training-ului
new_data = new_data[X_train.columns]

# Perform preprocessing on the new input data
categorical_cols = ['CO AQI Category', 'Ozone AQI Category', 'NO2 AQI Category', 'PM2.5 AQI Category']
for col in categorical_cols:
    new_data[col] = label_encoder.transform(new_data[col])

# Make predictions on the new input data
predictions = model.predict(new_data)

# Reverse label encoding to get the string labels
reverse_mapping = {label_encoder.transform([category])[0]: category for category in label_encoder.classes_}
predicted_labels = [reverse_mapping[prediction] for prediction in predictions]

# Print the predicted AQI Category
print("\nNew Input Data:")
print(new_data.to_string(index=False))
print("\nPredicted AQI Category:", predicted_labels)
