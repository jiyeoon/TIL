import os
import sys
import math
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, num2date
from matplotlib.ticker import FuncFormatter
from prophet.plot import add_changepoints_to_plot

from sklearn.metrics import r2_score, mean_squared_error

from prophet import Prophet


class Prpht():
    def __init__(self, file_path, price_norm=True, sales_norm=True,
                 price_max=100, changepoint_range = 0.8, changepoints = [],
                 holiday_weight=10, price_weight=10, seasonality_weight=1, changepoint_weight = 0.05,
                 HOLIDAY_EVENT=True, OUTLIER_HANDLE=True, PRC=True, IQR=False, 
                 ADD_COUNTRY_HOLIDAY=True, ADD_MONTHLY_SEASONALITY=True, ADD_CHANGE_POINT=True,
                 DARW_CHANGEPOINT = True, SQRT_TRANSFORM=False,
                 START_DATE=None, END_DATE=None, PRED_DAYS=7):
        self.file_path = file_path
        self.start_date = START_DATE
        self.end_date = END_DATE
        self.IQR = IQR
        self.PRC = PRC
        self.PRED_DAYS = PRED_DAYS
        self.HOLDAY_EVENT = HOLIDAY_EVENT
        self.OUTLIER_HANDLE = OUTLIER_HANDLE
        self.ADD_COUNTRY_HOLIDAY = ADD_COUNTRY_HOLIDAY
        self.ADD_MONTHLY_SEASONALITY = ADD_MONTHLY_SEASONALITY
        self.ADD_CHANGE_POINT = ADD_CHANGE_POINT
        self.DRAW_CHANGEPOINT = DARW_CHANGEPOINT
        self.SQRT_TRANSFORM = SQRT_TRANSFORM

        self.prd_no = file_path.split('/')[-1].split('_')[0]
        self.holiday_weight = holiday_weight
        self.price_weight = price_weight
        self.changepoints = changepoints
        self.changepoint_range = changepoint_range
        self.seasonality_weight = seasonality_weight
        self.changepoint_weight = changepoint_weight
        
        self.price_norm = price_norm
        self.sales_norm = sales_norm
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
        
        # min-max
        self.y_max = df.y.max()
        if self.SQRT_TRANSFORM:
            df['y'] = np.sqrt(df.y)
        else:
            df['y'] = df.y / df.y.max() * 100
        if self.IQR:
            q3 = df['y'].quantile(q=0.75)
            iqr = df['y'].quantile(q=0.75) - df['y'].quantile(q=0.25)
            maximum = q3 + 1.5 * iqr
            df['y'] = df['y'].apply(lambda x : maximum if x >= maximum else x)
        if self.price_norm == True:
            df['avg_prc'] = df.avg_prc / df.avg_prc.max()
            if self.price_max != None:
                df['avg_prc'] = df['avg_prc'] * self.price_max
        
        df = df[['ds', 'y', 'avg_prc']]
        missing_fill_val = {'avg_prc' : df.avg_prc.median(), 'y': 0.0}
        df.fillna(missing_fill_val, inplace=True)
        df['floor'] = 0.0
        df['cap'] = 100
                
        return df
        
    
    def get_model_forecast_pred(self):
        train, test = self.data[:-self.PRED_DAYS], self.data[-self.PRED_DAYS:]
        model = Prophet(growth='logistic',
                        holidays=self.holidays,
                        holidays_prior_scale=self.holiday_weight,
                        seasonality_prior_scale=self.seasonality_weight,
                        changepoint_prior_scale=self.changepoint_weight,
                        changepoint_range=self.changepoint_range,
                        changepoints=self.changepoints if self.changepoints else None,
                )
        
        if self.ADD_COUNTRY_HOLIDAY:
            model.add_country_holidays(country_name='KR')
        if self.ADD_MONTHLY_SEASONALITY:
            model.add_seasonality(name='montly_seasonality', period=30.5, fourier_order=5)
        
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
    
    def get_rmsse(self):
        return self.rmse / (self._get_rmsse_under() * self.PRED_DAYS)
            
    
    def draw_case(self):
        fig, ax = plt.subplots(figsize=(12, 5))
        fig = self.model.plot(self.forecast, ax=ax)
        if self.DRAW_CHANGEPOINT:
            a = add_changepoints_to_plot(fig.gca(), self.model, self.forecast)
        ax.set_ylabel('sales')
        ax2 = ax.twinx()
        ax2.set_ylabel('scaled_price')
        plt.plot(self.data.ds, self.data.avg_prc, color='deeppink', label='price')
        plt.legend()
        plt.title('PRD_NO : {} \nIQR : {}, PRC : {}, y_max : {} \n RMSE : {}, R2_SCORE : {}'.format(self.prd_no, self.IQR, self.PRC, self.y_max, self.rmse, self.r2score))        
    
        
    def _get_holiday(self):
        # 십일절
        day11 = {
            'holiday' : '11day',
            'ds' : ['20{}-{}-11'.format(i, j) for i in range(19, 22) for j in range(1, 13)],
            'lower_window' : 0,
            'upper_window' : 0,
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
        
        holidays = [pd.DataFrame(day11), pd.DataFrame(new_years_day), pd.DataFrame(chusuck)]
        if self.OUTLIER_HANDLE:
            outlier = self._get_outlier()
            holidays.append(outlier)
        
        return pd.concat(holidays)
    
    
    def _get_rmsse_under(self):
        n = len(self.data[:-self.PRED_DAYS])
        a = np.array(self.data['y'][:-self.PRED_DAYS-1])
        b = np.array(self.data['y'][1:-self.PRED_DAYS])
        return np.sum((b-a) ** 2) / n-1
    
    
    def _get_outlier(self):
        q3 = self.data['y'].quantile(q=0.75)
        iqr = self.data['y'].quantile(q=0.75) - self.data['y'].quantile(q=0.25)
        thrshd = q3 + (1.5 * iqr)
        df = self.data[self.data.y > thrshd]
        ds = df.ds.values
        data = {
            'holiday' : 'outlier',
            'ds' : ds,
            'lower_window' : 0,
            'upper_window' : 1
        }
        
        return pd.DataFrame(data)
    
    def _get_changepoint(self):
        # todo
        change_points = []
        count = 0
        i = 0
        while i < len(self.data[:-self.PRED_DAYS]):
            if self.data.iloc[i]['y'] == 0:
                curr_date = self.data.iloc[i]['ds']
                count += 1
                i += 1
                while i < len(self.data[:-self.PRED_DAYS]):
                    if self.data.iloc[i]['y'] == 0:
                        count += 1
                        if count == 3:
                            change_points.append(curr_date)
                    else:
                        if count >= 3:
                            end_date = self.data.iloc[i]['ds']
                            change_points.append(end_date)
                        count = 0
                        break
                    i += 1
            else:
                count = 0
            i += 1
        
        if self.changepoints:
            change_points.extend(self.changepoints)
                        
        return change_points
    
    def get_raw_rmse(self, history=False): # sales : sales / max * 100
        targets = self.data['y'] if history else self.data[-self.PRED_DAYS:]['y']
        predictions = self.forecast['yhat'] if history else self.pred['yhat']
        
        if self.SQRT_TRANSFORM:
            targets = targets ** 2
            predictions = predictions ** 2
        else:
            targets = targets * self.y_max / 100 
            predictions = predictions * self.y_max / 100
        
        return math.sqrt(mean_squared_error(targets, predictions))
    
    def get_raw_rmsse(self, history=False):
        n = len(self.data)
        if self.SQRT_TRANSFORM:
            tmp = self.data['y'] ** 2
        else:
            tmp = self.data['y'] * self.y_max / 100
        a = np.array(tmp[:-1])
        b = np.array(tmp[1:])
        under = np.sum((b-a)**2) / n-1
        rmsse = self.get_raw_rmse() / under * self.PRED_DAYS

        return rmsse

    def get_raw_r2score(self, history=False):
        targets = self.data['y'] if history else self.data[-self.PRED_DAYS:]['y']
        predictions = self.forecast['yhat'] if history else self.pred['yhat']
        
        if self.SQRT_TRANSFORM:
            targets = targets ** 2
            predictions = predictions ** 2
        else:
            targets = targets * self.y_max / 100
            predictions = predictions * self.y_max / 100
        
        r2score = r2_score(targets, predictions)
        
        return r2score
        
        