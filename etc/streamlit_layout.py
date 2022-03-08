import sqlite3
import ast
import pandas as pd
import numpy as np
import seaborn as sns

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Layout():
    
    def __init__(self, prd_no, opt_nm, ctlg_no=None):
        self.ctlg_no = ctlg_no
        self.prd_no = prd_no
        self.opt_nm = opt_nm
        
        self.con = sqlite3.connect('./test.db')
        self.cur = self.con.cursor()
        
        self.sales_df = self.load_sales_data()
        self.price_df = self.load_price_data()
        self.price_tmp = self.get_price_data_groupby()
        
    def load_sales_data(self):
        if self.ctlg_no:
            sql = f"SELECT * FROM product5 WHERE ctlg_no = {self.ctlg_no} AND prd_no = {self.prd_no} AND opt_nm = '{self.opt_nm}'"
        else:
            sql = f"SELECT * FROM product5 WHERE prd_no = {self.prd_no} AND opt_nm = '{self.opt_nm}'" 
        self.cur.execute(sql)
        prd_data = self.cur.fetchone()
        if not prd_data:
            return None
        else:
            dic = {
                '날짜' : ast.literal_eval(prd_data[3]),
                '판매량' : ast.literal_eval(prd_data[4]),
                '가격' : ast.literal_eval(prd_data[5])
            }
            df = pd.DataFrame(dic)
            df = df.astype({'판매량' : int, '가격' : int})
            df['날짜'] = pd.to_datetime(df['날짜'])
            return df
    
    def load_price_data(self):
        if self.ctlg_no:
            sql = f"SELECT * FROM price5 WHERE ctlg_no = {self.ctlg_no} AND prd_no = {self.prd_no} AND opt_nm = '{self.opt_nm}'"
        else:
            sql = f"SELECT * FROM price5 WHERE prd_no = {self.prd_no} AND opt_nm = '{self.opt_nm}'" 
        df = pd.read_sql_query(sql, self.con)
        if len(df) == 0:
            return None
        else:
            df = df.astype({'price' : float, 'sales' : float, 'ds_count' : float})
            df['판매량/날짜수'] = df['sales'] / df['ds_count']
            df = df[['price', 'sales', 'ds_count', '판매량/날짜수']]
            df = df.sort_values('price')
            return df
    
    def get_price_data_groupby(self):
        n_decimal = len(str(self.price_df['price'].min())) - 3
        result = self.price_df.round({'price' : -n_decimal})
        result = result.groupby('price').agg({
            'sales' : 'sum', 'ds_count' : 'sum'
        }).reset_index()
        result['판매량/날짜수'] = result['sales'] / result['ds_count']
        result = result[result['ds_count'] >= 5]
        return result
        
    # get sales hisotry with pandas styler
    def get_sales_history_styler(self):
        styler = self.sales_df.style
        styler.format({
            '날짜' : lambda x : x.strftime('%Y-%m-%d'),
            '가격' : lambda x : '{:,}'.format(x)
        })
        styler.apply(self._color_max, subset=['가격', '판매량'])
        styler.apply(self._color_min, subset=['가격', '판매량'])
        styler.apply(self._color_mean, subset=['가격', '판매량'])
        
        return styler
    
    # get price history with pandas styler
    def get_price_styler(self):
        styler = self.price_df_with_ds_thrshd.style
        styler.apply(self._color_max, subset=['price', 'sales', 'ds_count']) #, '쿠폰할인', '임직원할인', '즉시할인', '복수구매할인'])
        styler.apply(self._color_min, subset=['price', 'sales', 'ds_count']) # , '쿠폰할인', '임직원할인', '즉시할인', '복수구매할인'])
        styler.format({
            'price' : lambda x : '{}'.format(int(x)),
            'sales' : lambda x : '{}'.format(int(x)),
            'ds_count' : lambda x : '{}'.format(int(x)),
            '판매량/날짜수' : lambda x : '{:.2f}'.format(x),
        })
        styler.hide_index()
        
        return styler
    
    # 일별 판매량 그래프
    def draw_daily_sales_history(self):
        fig = make_subplots(specs=[[{'secondary_y' : True}]])
        fig.add_trace(
            go.Scatter(x=self.sales_df['날짜'], y=self.sales_df['가격'],
                    mode='lines', name='가격'),
            secondary_y = False,
        )
        fig.add_trace(
            go.Scatter(x=self.sales_df['날짜'], y=self.sales_df['판매량'], mode='lines', name='판매량'),
            secondary_y = True,
        )
        fig.update_xaxes(title_text="날짜")
        fig.update_yaxes(title_text='가격', secondary_y=False, tickformat='000')
        fig.update_yaxes(title_text='판매량', secondary_y=True, tickformat='000')
        
        return fig
    
    # 필요 없는 부분임...
    def get_monthly_sales_styler(self):
        monthly = self._get_monthly_sales_history()
        return monthly.styler
    
    # 월별 판매량 그래프 - Bar Graph
    def draw_monthly_sales_history_bar(self):
        monthly = self._get_monthly_sales_history()
        fig = go.Figure(
            [go.Bar(x=monthly['년월'], y=monthly['판매량'])]
        )
        fig.update_layout(title='월별 판매량 그래프')
        return fig
    
    # 월별 판매량 그래프 - Box plot
    def draw_monthly_sales_history_box(self):
        fig = go.Figure()
        for year in [2021, 2022]:
            for month in range(1, 13):
                filtered = self.sales_df[(self.sales_df['날짜'].dt.year == year)&(self.sales_df['날짜'].dt.month==month)]
                y = filtered['판매량']
                fig.add_trace(
                    go.Box(
                        y=y,
                        name= str(year) + '-' + str(month),
                    )
                )
        fig.update_layout(title='월별 판매량 box plot')
        return fig
    
    # 가격대별 그래프 - 전체 히스토그램
    def draw_histogram_per_price_range(self):
        df = self._get_sales_data_per_price_range()
        fig = px.histogram(df, x='날짜', y='판매량', color='가격범위', histfunc='sum')
        fig.update_layout(title='가격대별 판매 추이')
        return fig
    
    # 가격대별 그래프 - Pie plot
    def draw_pie_per_price_range(self):
        df = self._get_sales_data_per_price_range()
        tmp = df['가격범위'].value_counts().sort_index()
        labels, values = tmp.index.to_list(), list(tmp.values)
        
        fig = go.Figure(
            data = [go.Pie(labels=labels, values=values, sort=False)]
        )
        fig.update_layout(title='가격대별 판매량')
        return fig
    
    # 가격대별 그래프 - 가격대별 히스토그램
    def draw_each_histogram_per_price_range(self):
        result = self._get_sales_data_per_price_range()
        tmp = result['가격범위'].value_counts().sort_index()
        labels, values = tmp.index.to_list(), list(tmp.values)
        
        fig = make_subplots(rows=2, cols=2) if len(labels) == 4 else make_subplots(rows=1, cols=len(labels))
        if len(labels) == 4:
            idx = 0
            for row in range(1, 3):
                for col in range(1, 3):
                    fig.append_trace(
                        go.Histogram(histfunc='sum', x=result['날짜'], y=result['{}'.format(labels[idx])], name='{}'.format(labels[idx])),
                        row=row, col=col
                    )
                    idx += 1
        else:
            idx = 0
            for col in range(1, len(labels)+1):
                fig.append_trace(
                    go.Histogram(histfunc='sum', x=result['날짜'], y=result['{}'.format(labels[idx])], name='{}'.format(labels[idx])),
                    row=1, col=col
                )
                idx += 1
        fig.update_layout(title='가격대별 판매량 분포')
        fig.update_xaxes(title='날짜')
        fig.update_yaxes(title='판매량')
        return fig
    
    # 가격대별 그래프 - 가격대별 sales history
    def draw_each_sales_history_per_price_range(self):
        result = self._get_sales_data_per_price_range()
        tmp = result['가격범위'].value_counts().sort_index()
        labels = tmp.index.to_list()

        fig = make_subplots(rows=2, cols=2) if len(labels) == 4 else make_subplots(rows=1, cols=len(labels))
        if len(labels) == 4:
            idx = 0
            for row in range(1, 3):
                for col in range(1, 3):
                    fig.append_trace(
                        go.Scatter(
                            x=result['날짜'], y=result['{}'.format(labels[idx])],
                            name=labels[idx]
                        ),
                        row=row, col=col, 
                    )
                    idx += 1
        else:
            for col in range(1, len(labels)+1):
                fig.append_trace(
                    go.Scatter(
                        x=result['날짜'], y=result['{}'.format(labels[col-1])],
                        name=labels[col-1]
                    ),
                    row=1, col=col, 
                )
        fig.update_layout(title='가격대별 판매량 history')
        fig.update_xaxes(title='날짜')
        fig.update_yaxes(title='판매량')
        return fig
                        
    # 가격/판매량 관계 그래프 - line plot
    def draw_prc_sales_line(self):
        tmp3 = self.price_tmp
        fig = make_subplots(specs=[[{'secondary_y' : True}]])  
        fig.add_trace(
            go.Scatter(x=tmp3['price'], y=tmp3['판매량/날짜수'],
                    mode='lines+markers', name='판매량/날짜수'),
            secondary_y = False,
        )
        fig.add_trace(
            go.Scatter(x=tmp3['price'], y=tmp3['sales'], mode='lines+markers', name='판매량'),
            secondary_y = True
        )
        fig.update_layout(title='가격 - 판매량 관계 그래프')
        fig.update_xaxes(title_text="가격")
        fig.update_yaxes(title_text='판매량', secondary_y=True, tickformat='000')
        fig.update_yaxes(title_text='판매량/날짜수', secondary_y=False, tickformat='000')
        
        return fig
        
    # 가격/판매량 관계 그래프 - bubble plot
    def draw_prd_sales_bubble(self):
        tmp3 = self.price_tmp
        marker_size = tmp3['ds_count'] / tmp3['ds_count'].max() * 100
        
        fig = make_subplots(specs=[[{'secondary_y' : True}]])
        fig.add_trace(
            go.Scatter(x=tmp3['price'], y=tmp3['sales'],
                    mode='markers', name='판매량',
                    marker_size=marker_size
                    ),
            secondary_y = False,
        )
        filtered = tmp3[tmp3['ds_count']/tmp3['ds_count'].max()*100 >= 40]
        X, y = filtered[['price']], filtered[['sales']]
        
        # regression line (Linear regression)
        model = make_pipeline(PolynomialFeatures(2), LinearRegression()) #LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(tmp3[['price']])
        
        fig.add_trace(
            go.Scatter(
                x=tmp3['price'], y=y_pred[:, -1],
                mode='lines', name='linear regression'
            )
        )
        fig.update_layout(title='가격 - 판매량 버블 그래프')
        fig.update_xaxes(title_text="가격")
        fig.update_yaxes(title_text='판매량', secondary_y=False, tickformat='000', range=[-tmp3['sales'].max() * 0.25, tmp3['sales'].max() * 1.5])
        return fig
    
    # 가격/판매량 관계 그래프 - 누적 그래프
    def draw_prd_sales_cumm(self):
        tmp3 = self.price_tmp
        fig = make_subplots()
        fig.add_trace(
            go.Scatter(
                x=tmp3['price'], y=tmp3['sales'].cumsum(),
                mode='lines+markers', name='누적판매량',
            )
        )
        fig.update_layout(title='가격 - 판매량 누적 그래프')
        fig.update_xaxes(title_text='가격')
        fig.update_yaxes(title_text='누적 판매량', tickformat='000')
        return fig
    
    # 가격대별 판매량 데이터
    def _get_sales_data_per_price_range(self):
        result = self.sales_df.copy()
        bins = [result['가격'].quantile(q=qq) for qq in [0, 0.25, 0.5, 0.75, 1]]
        bins = sorted(list(set(bins)))
        labels = ['{}~{}'.format(int(bins[i]), int(bins[i+1])) for i in range(len(bins)-1)]
        
        result['가격범위'] = pd.cut(result['가격'], bins=bins, labels=labels, include_lowest=True)
        
        for label in labels:
            result['{}'.format(label)] = result.apply(lambda x: x['판매량'] if x['가격범위']==label else 0, axis=1)
        
        return result
        
    # 월별 판매량
    def _get_monthly_sales_history(self):
        monthly = self.sales_df.resample('1M', on='날짜').sum()
        monthly['년월'] = monthly.index.strftime('%Y-%m')
        monthly.reset_index(inplace=True)
        return monthly[['년월', '판매량']]

    # for styling..
    def _color_max(self, s):
        is_max = s == s.max()
        return ['background-color : yellow' if v else '' for v in is_max]
    
    def _color_min(self, s):
        is_min = s == s.min()
        return ['background-color : lightblue' if v else '' for v in is_min]
    
    def _color_mean(self, s):
        is_mean = s == int(s.mean())
        return ['background-color : deeppink' if v else '' for v in is_mean]
    