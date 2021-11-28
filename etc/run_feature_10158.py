import os
import ast
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

from tqdm import tqdm
from prophet import Prophet
from sklearn.metrics import r2_score, mean_squared_error

PRED_DAYS = 7

def get_model_forecast(info):
    ds = ast.literal_eval(info['train_ds']) 
    y = ast.literal_eval(info['train_y']) 
    avg_prc = ast.literal_eval(info['train_avg_prc']) 
    test_y = ast.literal_eval(info['test_y'])
    test_avg_prc = ast.literal_eval(info['test_avg_prc'])
    dic = {
        'ds' : ds,
        'y' : y,
        'avg_prc' : avg_prc
    }
    data = pd.DataFrame(dic)
    holidays = pd.read_json(info['holidays'])
    
    ## feature engineering
    if data['avg_prc'].max() > 0:
        data['avg_prc'] = data['avg_prc'] / data['avg_prc'].max() * 100
    else:
        data['avg_prc'] = data['avg_prc'] / (data['avg_prc'].max() + 1) * 100
    data['cap'] = 100.0
    data['floor'] = 0.0
    
    ## run prophet
    model = Prophet(
        growth='logistic',
        holidays = holidays
    )
    model.add_country_holidays(country_name='KR')
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    if data['avg_prc'].isna().sum() == 0:
        model.add_regressor('avg_prc')
    model.fit(data)
    
    ## get estimation
    future = model.make_future_dataframe(periods=PRED_DAYS)
    if data['avg_prc'].isna().sum() == 0:
        future['avg_prc'] = pd.concat([pd.Series(avg_prc), pd.Series(test_avg_prc)], ignore_index=True)
    future['cap'] = 100
    future['floor'] = 0.0
    
    forecast = model.predict(future)
    
    return model, forecast

df = pd.read_csv('./data/feature_data_10158.csv')
n = len(df)

results = {
    'prd_no' : [],
    'model' : [],
    'forecast' : [],
    'y' : [],
    'r2_score' : [],
    'rmse' : [],
    'custom_metric' : []
}

for i in tqdm(range(n)):
    info = df.iloc[i]
    model, forecast = get_model_forecast(info)
    
    prd_no = info['prd_no']
    test_y = ast.literal_eval(info['test_y'])
    y = ast.literal_eval(info['train_y']) + test_y 
    test_yhat = forecast['yhat'][-PRED_DAYS:]
    
    r2score = r2_score(test_y, test_yhat)
    rmse = np.sqrt(mean_squared_error(test_y, test_yhat))
    custom_metric = (np.abs(test_y - test_yhat).sum() / PRED_DAYS) / np.mean(y)
    
    results['prd_no'].append(prd_no)
    results['model'].append(model)
    results['forecast'].append(forecast)
    results['y'].append(y)
    results['r2_score'].append(r2score)
    results['rmse'].append(rmse)
    results['custom_metric'].append(custom_metric)
    
    if i % 100 == 0:
        with open('feature_10158_results_{}.pickle'.format(i), 'wb') as f:
            pickle.dump(results, f)
            
with open('feature_10158_results_final.pickle', 'wb') as f:
    pickle.dump(results, f)