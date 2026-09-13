from fastapi import FastAPI 
from pydantic import BaseModel
import joblib
from service import prediction
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pandas as pd

app = FastAPI()

# model loading
model_unpack = joblib.load('model/logreg.pkl')
meta_data = model_unpack['metadata']
model = model_unpack['model']
features_for_model = model_unpack['features']

# tools for transforming loading
tools_unpack = joblib.load('model/transformers.pkl')
ohe = tools_unpack['ohe']
std_scaler = tools_unpack['scaler']

class Form(BaseModel):
    visit_datetime: str
    visit_number: int
    geo_city: str
    utm_medium: str
    device_category: str
    device_browser: str
    brand: str
    

@app.get('/status')
def status():
    return 200

@app.get('/metadata')
def metadata_output():
    return meta_data

@app.post('/predict_proba')
def predict_proba(form: Form):
    df = pd.DataFrame.from_dict([form.dict()])

    df['hit_time'] = 42
    df['hit_number'] = 42
    df['client_id'] = 42

    probabilities = prediction(df, model, ohe, std_scaler, features_for_model)

    return {
        'Probability if will': probabilities[:, 1].tolist(),
        'Probability if will not': probabilities[:, 0].tolist()
    }

@app.post('/predict')
def predict(form: Form):
    df = pd.DataFrame.from_dict([form.dict()])

    df['hit_time'] = 42
    df['hit_number'] = 42
    df['client_id'] = 42

    probabilities = prediction(df, model, ohe, std_scaler, features_for_model)

    result = None
    
    if probabilities[:, 1] > 0.57:
        result = 1
    
    else:
        result = 0

    return {
        "Result": result
    }