import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle
import re
from urllib.parse import urlparse
# Load the feature-engineered dataset
path =  r"replace with path of  feature_extracted_dataset.csv" # Provide the actual path to your dataset
df = pd.read_csv(path)
# Ensure the columns are as expected
required_columns = ['url', 'url_length', 'num_special_chars', 'type_label']
for col in required_columns:
    if col not in df.columns:
        raise KeyError(f"Column '{col}' is missing from the dataset.")
# Handle categorical columns ('url')
if df['url'].dtype == 'object':
    label_encoder_url = LabelEncoder()
    df['url'] = label_encoder_url.fit_transform(df['url'])
    with open('label_encoder_url.pkl', 'wb') as f:
        pickle.dump(label_encoder_url, f)
else:
    label_encoder_url = None
# Prepare feature columns
feature_columns = ['url', 'url_length', 'num_special_chars']
X = df[feature_columns].astype(float)  # Ensure features are numeric
y = df['type_label']  # Labels: 0 = non-malicious, 1 = malicious
# Train the XGBoost model on all data
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X, y)
# Test the model on all data
y_pred = model.predict(X)
accuracy = accuracy_score(y, y_pred)
#print(f"Model Accuracy on all data: {accuracy * 100:.2f}%")
# Save the trained model using XGBoost's method
model.save_model('xgboost_model.json')
# Function to calculate URL features
def extract_features_from_url(url):
    url_length = len(url)
    num_special_chars = len(re.findall(r'[\W_]', url))
    # Load the label encoder
    with open('label_encoder_url.pkl', 'rb') as f:
        label_encoder_url = pickle.load(f)
    # Encode the URL
    if label_encoder_url is not None:
        url_encoded = label_encoder_url.transform([url])[0] if url in label_encoder_url.classes_ else -1
    else:
        url_encoded = -1
    # Return features as a DataFrame with appropriate types
    features = {
        'url': [float(url_encoded)],
        'url_length': [float(url_length)],
        'num_special_chars': [float(num_special_chars)]
    }
    return pd.DataFrame(features)
# Function to predict a new URL (malicious or non-malicious)
def predict_url(url):
    # Load the model
    model = xgb.XGBClassifier()
    model.load_model('xgboost_model.json')
    # Extract features from the entered URL
    new_url_features = extract_features_from_url(url)
    # Debugging
    # print("Extracted features:", new_url_features)
    # Ensure feature dimensions match
    if new_url_features.shape[1] != len(feature_columns):
       # print(f"Error: Feature shape mismatch. Expected {len(feature_columns)}, got {new_url_features.shape[1]}")
        return
    # Predict the label for the new URL (0 = non-malicious, 1 = malicious)
    prediction = model.predict(new_url_features)[0]
    # Debugging
    print( prediction)
    #label = 1 if prediction == 1 else 0
    # print(1 if label else 0)
# Accept user input and classify the URL
if __name__ == "__main__":
    user_url = input()
    predict_url(user_url)