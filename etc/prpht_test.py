import os
import math
import warnings
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
from prpht import Prpht

PRED_DAYS = 7
START_DATE = '2020-10-01'
END_DATE = '2021-10-05'

MODE = 'custom'

data = {
    'prd_no' : [],
    'rmse' : [],
    'r2score' : [],
    'rmsse' : [],
    'raw_rmse' : [],
    'raw_r2score' : [],
    'raw_rmsse' : []
}


def estimate(file_path, params, MODE='auto'):
    params['file_path'] = file_path
    p = Prpht(**params)
    
    if MODE == 'custom':
        auto_changepoints = p.model.changepoints.to_list()
        custom_changepoints = p._get_changepoint()
        changeoints = auto_changepoints + custom_changepoints
        
        params['changepoints'] = changeoints
        
        p = Prpht(**params)
        
    return p.rmse, p.r2score, p.get_rmsse(), p.get_raw_rmse(), p.get_raw_r2score(), p.get_raw_rmsse()

def main(params, MODE='auto'):
    curr_path = os.path.dirname(os.path.abspath('__file__'))
    target_path = os.path.join(curr_path, 'data', '1006')
    listdir = os.listdir(target_path)
    listdir.sort()
    
    for file_name in tqdm(listdir[:100]):
        print(file_name, " start!")
        if 'csv' not in file_name:
            continue
        prd_no = file_name.split('_')[0]
        file_path = os.path.join(target_path, file_name)
        try:
            rmse, r2score, rmsse, raw_rmse, raw_r2score, raw_rmsse = estimate(file_path, params, MODE=MODE)
        except:
            continue
        data['prd_no'].append(prd_no)
        data['rmse'].append(rmse)
        data['r2score'].append(r2score)
        data['rmsse'].append(rmsse)
        data['raw_rmse'].append(raw_rmse)
        data['raw_r2score'].append(raw_r2score)
        data['raw_rmsse'].append(raw_rmsse)
    
    result = pd.DataFrame(data)
    result.to_csv('./1006_result_custom.csv')
    
if __name__ == '__main__':
    params = {
        'START_DATE' : START_DATE,
        'END_DATE' : END_DATE,
        'IQR' : False,
        'seasonality_weight' : 1,
        'changepoint_weight' : 0.3,
        'changepoint_range' : 0.8,
        'HOLIDAY_EVENT' : True,
        'ADD_MONTHLY_SEASONALITY' : True,
        'ADD_COUNTRY_HOLIDAY' : True,
        'ADD_CHANGE_POINT' : False,
        'price_norm' : True,
        'OUTLIER_HANDLE' : True,
        'PRED_DAYS' : PRED_DAYS,
    }
    main(params, MODE='custom')
        
        
        