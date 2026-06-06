import joblib
import os

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(
    os.path.join(BASE_DIR, "crop_recommendation_model.pkl")
)

scaler = joblib.load(
    os.path.join(BASE_DIR, "scaler.pkl")
)

def predict_crop(features):
    scaled_features = scaler.transform([features])
    prediction = model.predict(scaled_features)
    return prediction[0]