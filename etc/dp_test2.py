import os
import math
from numpy.core.fromnumeric import mean
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, num2date
from matplotlib.ticker import FuncFormatter
from pandas.core.indexes import period
from tqdm import tqdm
from datetime import datetime

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error

from prophet import Prophet


PRED_DAYS = 60 * 24
START_DATE = '2019-01-01'
END_DATE = '2021-09-07'


def estimate(file_path):
    try:
        df = pd.read_csv(file_path)
    except:
        raise FileNotFoundError('파일을 찾을 수 없습니다')
    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='1H')[:-1]
    df['ds'] = df['dt'].map(str) + " " + df['dhour'].map(str) + ":00:00"
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.set_index('ds')
    df = pd.merge(date_range.to_frame(), df, left_index=True, right_index=True, how='left')
    df['ds'] = df.index
    df = df.rename(columns={'sales' : 'y'})
    missing_fill_val = {'avg_prc' : df.avg_prc.median(), 'y' : 0}
    df.fillna(missing_fill_val, inplace=True)
    q3 = df['y'].quantile(q=0.75)
    cap = q3 * 1.5
    df['y'] = df['y'].apply(lambda x : cap if x >= cap else x)
    df = df[['ds', 'y', 'avg_prc']]
    
    scaler = MinMaxScaler()
    scaled_value = scaler.fit_transform(df[['avg_prc', 'y']].values)
    df[['avg_prc', 'y']] = scaled_value
    df['floor'] = 0
    df['cap'] = 1.2
    
    train = df[:-PRED_DAYS]
    test = df[-PRED_DAYS:]
    
    m = Prophet(growth='logistic', holidays=holidays, holidays_prior_scale=1)
    m.add_regressor('avg_prc')
    m.fit(train)
    future = m.make_future_dataframe(periods=PRED_DAYS, freq='H')
    future = pd.merge(future, train, left_on='ds', right_on='ds', how='left')
    future = future[['ds', 'floor', 'cap', 'avg_prc']]
    future_fill_missing = {'avg_prc' : df.iloc[len(df)-1]['avg_prc'], 'cap' : 1.2, 'floor' : 0}
    future.fillna(future_fill_missing, inplace=True)
    forecast = m.predict(future)
    
    pred = forecast[['ds', 'yhat']][-PRED_DAYS:]
    pred['yhat'] = np.where(pred['yhat'] < 0, 0, pred['yhat'])
    
    rmse = math.sqrt(mean_squared_error(test['y'], pred['yhat']))
    r2score = r2_score(test['y'], pred['yhat'])
    
    return rmse, r2score
    

target_dir = os.path.dirname(os.path.abspath('__file__'))
target_dir = os.path.join(target_dir, 'data', '0913')
listdir = os.listdir(target_dir)
print(len(listdir))

data = {'prd_no' : [],
       'rmse' : [],
       'r2_score': []}


holidays = {
    'holiday' : '11day',
    'ds' : pd.to_datetime([
        '20{}-{}-11'.format(i, j) for i in range(19, 22) for j in range(1, 13)
    ]),
    'lower_window' : 0,
    'upper_window' : 1,
}
holidays = pd.DataFrame(holidays)


for file_name in tqdm(listdir):
    if 'csv' not in file_name:
        continue
    
    prd_no = file_name.split('_')[0]
    file_path = os.path.join(target_dir, file_name)
    
    try:
        rmse, r2score = estimate(file_path)
    except Exception as e:
        print("Error occured :", e)
        continue

    data['prd_no'].append(prd_no)
    data['rmse'].append(rmse)
    data['r2_score'].append(r2score)
    

result = pd.DataFrame(data)
print(result.info())

result.to_csv('./result_{}.csv'.format(datetime.today()))