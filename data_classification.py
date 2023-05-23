import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv('temp_air_pollution.csv')

# Sterg coloanele pe care nu le folosesc la ML
data = data.drop(['Country', 'City'], axis=1)

# dau Encode la datele de tip string, pentru a avea valori numerice intre 0 si 1
label_encoder = LabelEncoder()
categorical_cols = ['AQI Category', 'CO AQI Category', 'Ozone AQI Category', 'NO2 AQI Category', 'PM2.5 AQI Category']
for col in categorical_cols:
    data[col] = label_encoder.fit_transform(data[col])


# Impart csv-ul in coloanele folosite la train si test
X = data.drop('AQI Category', axis=1)
y = data['AQI Category']


# Impart intreg csv-ul ca sa nu folosesc aceleasi date la train si la test, random_state e un RNG care ajuta in minimizarea bias-ului (sa nu iau eu ce date vreau pt train si test, test_size 0.2 = 20% din csv e luat la intamplare)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestClassifier()


model.fit(X_train, y_train)


y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


joblib.dump(model, 'AQI_Category.joblib')
joblib.dump(label_encoder, 'Label_Encoder.joblib')
