import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

from data_classification import X_train

model = joblib.load('AQI_Category.joblib')

label_encoder = joblib.load('Label_Encoder.joblib')

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

new_data = new_data[X_train.columns]

categorical_cols = ['CO AQI Category', 'Ozone AQI Category', 'NO2 AQI Category', 'PM2.5 AQI Category']
for col in categorical_cols:
    new_data[col] = label_encoder.transform(new_data[col])

predictions = model.predict(new_data)

reverse_mapping = {label_encoder.transform([category])[0]: category for category in label_encoder.classes_}
predicted_labels = [reverse_mapping[prediction] for prediction in predictions]

print("\nNew Input Data:")
print(new_data.to_string(index=False))
print("\nPredicted AQI Category:", predicted_labels)
