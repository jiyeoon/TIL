import os
import sys
import math
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, num2date
from matplotlib.ticker import FuncFormatter

from sklearn.metrics import r2_score, mean_squared_error

from prophet import Prophet


class Prpht():
    def __init__(self, file_path, price_norm=True, price_max=None, holiday_weight=10, price_weight=10, PRC=True, IQR=True, START_DATE=None, END_DATE=None, PRED_DAYS=7):
        self.file_path = file_path
        self.start_date = START_DATE
        self.end_date = END_DATE
        self.IQR = IQR
        self.PRC = PRC
        self.PRED_DAYS = PRED_DAYS
        self.prd_no = file_path.split('/')[-1].split('_')[0]
        self.holiday_weight = holiday_weight
        self.price_weight = price_weight
        self.price_norm = price_norm
        self.price_max = price_max

        
        self.data = self.get_data()
        self.holidays = self._get_holiday()
        
        self.model, self.forecast, self.pred = self.get_model_forecast_pred()
        
        self.rmse = self.get_rmse()
        self.r2score = self.get_r2score()
        
        
        
    def get_data(self):
        df = pd.read_csv(self.file_path)
        self.start_date = df.iloc[0]['dt'] if not self.start_date else self.start_date
        self.end_date = df.iloc[len(df)-1]['dt'] if not self.end_date else self.end_date
        date_range = pd.date_range(start=self.start_date, end=self.end_date)
        df['ds'] = pd.to_datetime(df['dt'])
        df = df.set_index('ds')
        df = pd.merge(date_range.to_frame(), df, left_index=True, right_index=True, how='left')
        df['ds'] = df.index
        df = df.rename(columns={'sales' : 'y'})
        missing_fill_val = {'avg_prc' : df.avg_prc.median(), 'y': 0.0}
        df.fillna(missing_fill_val, inplace=True)
        
        if self.IQR:
            q3 = df['y'].quantile(q=0.75)
            iqr = df['y'].quantile(q=0.75) - df['y'].quantile(q=0.25)
            maximum = q3 + 1.5 * iqr
            df['y'] = df['y'].apply(lambda x : maximum if x >= maximum else x)
        
        # min-max
        df['y'] = (df.y - df.y.min()) / (df.y.max() - df.y.min())
        df['y'] = df['y'] * 100
        if self.price_norm:
            df['avg_prc'] = df.avg_prc / df.avg_prc.max()
            if self.price_max:
                df['avg_prc'] = df['avg_prc'] * self.price_max
        
        df = df[['ds', 'y', 'avg_prc']]
        df['floor'] = 0.0
        df['cap'] = df['y'].max()
        
        return df
        
    
    def get_model_forecast_pred(self):
        train, test = self.data[:-self.PRED_DAYS], self.data[-self.PRED_DAYS:]
        model = Prophet(growth='logistic',
                        holidays=self.holidays,
                        holidays_prior_scale=self.holiday_weight
                )
        
        if self.PRC:
            model.add_regressor('avg_prc', prior_scale=self.price_weight, standardize=False)    
            model.fit(train)
            future = model.make_future_dataframe(periods=self.PRED_DAYS)
            future = pd.merge(future, train, left_on='ds', right_on='ds', how='left')
            future = future[['ds', 'floor', 'cap', 'avg_prc']]
            future['avg_prc'] = self.data.avg_prc.values
            future_fill_missing = {'cap' : 100, 'floor' : 0.0}
            future.fillna(future_fill_missing, inplace=True)
        else:
            model.fit(train)
            future = model.make_future_dataframe(periods=self.PRED_DAYS)
            future['cap'] = 100
            future['floor'] = 0.0
        
        forecast = model.predict(future)
        pred = forecast[['ds', 'yhat']][-self.PRED_DAYS:]
        pred['yhat'] = np.where(pred['yhat'] < 0, 0, pred['yhat'])
        
        return model, forecast, pred
    
    
    def get_rmse(self):
        return math.sqrt(mean_squared_error(self.data[-self.PRED_DAYS:]['y'], self.pred['yhat']))
    
    
    def get_r2score(self):
        return r2_score(self.data[-self.PRED_DAYS:]['y'], self.pred['yhat'])
            
    
    def draw_case(self):
        fig, ax = plt.subplots(figsize=(12, 5))
        #fig = plt.figure(figsize=(12, 5))
        #ax = fig.subplots()
        self.model.plot(self.forecast, ax=ax)
        ax.set_ylabel('sales')
        ax2 = ax.twinx()
        ax2.set_ylabel('scaled_price')
        plt.plot(self.data.ds, self.data.avg_prc, color='deeppink', label='price')
        plt.legend()
        plt.title('IQR : {}, PRC : {} \n RMSE : {}, R2_SCORE : {}'.format(self.IQR, self.PRC, self.rmse, self.r2score))        
        
        
    def _get_holiday(self):
        # 십일절
        day11 = {
            'holiday' : '11day',
            'ds' : ['20{}-{}-11'.format(i, j) for i in range(19, 22) for j in range(1, 13)],
            'lower_window' : 0,
            'upper_window' : 1,
        }
        
        # 설날
        new_years_day = {
            'holiday' : '설날',
            'ds' : ['2020-01-25', '2021-02-12'],
            'lower_window' : -2,
            'upper_window' : 2
        }
        
        chusuck = {
            'holiday' : '추석',
            'ds' : ['2020-10-01', '2021-09-12'],
            'lower_window' : -2,
            'upper_window' : 2
        }
        
        return pd.concat([pd.DataFrame(day11), pd.DataFrame(new_years_day), pd.DataFrame(chusuck)])
        
    
    