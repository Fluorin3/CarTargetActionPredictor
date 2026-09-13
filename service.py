import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import FunctionTransformer
import os

def add_date_features(df, date_col='visit_datetime'):

    df[date_col] = pd.to_datetime(df[date_col])
    
    df['hour'] = df[date_col].dt.hour
    df['dayofweek'] = df[date_col].dt.dayofweek
    df['month'] = df[date_col].dt.month
    df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)
    
    
    df['time_block'] = pd.cut(df['hour'], 
                               bins=[0, 6, 12, 18, 24], 
                               labels=['night', 'morning', 'afternoon', 'evening'])
    
    # кодирование в формат для ML
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    
    df['dow_sin'] = np.sin(2 * np.pi * df['dayofweek'] / 7)
    df['dow_cos'] = np.cos(2 * np.pi * df['dayofweek'] / 7)
    
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    # Относительные признаки
    min_date = df[date_col].min()
    df['days_since_start'] = (df[date_col] - min_date).dt.days
    
    # Удаляем исходные 
    df = df.drop([date_col, 'hour', 'dayofweek', 'month'], axis=1)
    
    return df

def prediction(df, model, ohe, std_scaler, safe_features):

    # data transforming
    
    df = add_date_features(df)

    # standarting

    columns_for_scale = ['visit_number', 'client_id', 'hit_time', 'hit_number', 'days_since_start']
    scaled = std_scaler.transform(df[columns_for_scale])

    df[columns_for_scale] = scaled
    
    # encoding

    columns_cat = ['utm_medium', 'device_category', 'device_browser', 'brand', 'geo_city', 'time_block']
    encoded = ohe.transform(df[columns_cat])
    df[ohe.get_feature_names_out()] = encoded

    # delete unhealthy and fruitless columns

    df = df.drop(['client_id', 'hit_time', 'hit_number'], axis=1)
    df = df.drop(columns_cat, axis=1)

    # prediction

    prediction = model.predict_proba(df[safe_features])

    return prediction
