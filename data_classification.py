import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv('temp_air_pollution.csv')

data = data.drop(['Country', 'City'], axis=1)

label_encoder = LabelEncoder()
categorical_cols = ['AQI Category', 'CO AQI Category', 'Ozone AQI Category', 'NO2 AQI Category', 'PM2.5 AQI Category']
for col in categorical_cols:
    data[col] = label_encoder.fit_transform(data[col])

X = data.drop('AQI Category', axis=1)
y = data['AQI Category']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

joblib.dump(model, 'AQI_Category.joblib')
joblib.dump(label_encoder, 'Label_Encoder.joblib')
