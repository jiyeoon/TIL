from re import M
import streamlit as st
import pandas as pd
import ast 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3

con = sqlite3.connect('./test.db')
cur = con.cursor()


def main():
    st.set_page_config(layout='wide')
    st.write("""
                # Dynamic Pricing Demo Page
            """)

    prd_no = st.text_input('Enter product no', '2826341919')

    if st.button('Enter'):
        
        sql = "SELECT * FROM product WHERE prd_no={}".format(prd_no)
        cur.execute(sql)
        data = cur.fetchone()
        st.session_state['data'] = data
        dic = {
            '날짜' : ast.literal_eval(data[1]),
            '판매량' : np.square(ast.literal_eval(data[2])),
            '가격' : ast.literal_eval(data[3])
        }
        
        result = pd.DataFrame(dic)
        result = result.astype({
            '판매량' : int,
            '가격' : int
        })
        result['날짜'] = pd.to_datetime(result['날짜'])
        styler = result.style.format({
            '날짜' : lambda x : x.strftime("%Y-%m-%d"),
            '가격' : lambda x : "{:,}".format(x)
        })
        
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            col1.subheader('일자별 가격 - 판매량 그래프')
            col1.dataframe(styler)
            
            fig = make_subplots(specs=[[{'secondary_y' : True}]])
            
            fig.add_trace(
                go.Scatter(x=result['날짜'], y=result['가격'],
                        mode='lines', name='가격'),
                secondary_y = False,
            )
            
            fig.add_trace(
                go.Scatter(x=result['날짜'], y=result['판매량'], mode='lines', name='판매량'),
                secondary_y = True,
            )
            
            fig.update_xaxes(title_text="날짜")
            
            fig.update_yaxes(title_text='가격', secondary_y=False, tickformat='000')
            fig.update_yaxes(title_text='판매량', secondary_y=True, tickformat='000')
            
            col2.plotly_chart(fig, use_container_width=True)
        
        
        ## 가격 - 판매량 관계 그래프
        with st.container():
            tmp2 = result.groupby('가격').agg({'판매량' : 'sum', '날짜' : 'count'}).reset_index()
            tmp2['판매량/날짜수'] = tmp2['판매량'] // tmp2['날짜']
            tmp2['날짜수'] = tmp2['날짜']
            tmp2 = tmp2[['가격', '판매량', '날짜수', '판매량/날짜수']]
            col1, col2 = st.columns([1, 3])
            col1.subheader("가격 - 판매량 관계 그래프")
            col1.dataframe(tmp2)
            
            fig = make_subplots(specs=[[{'secondary_y' : True}]])
            
            fig.add_trace(
                go.Scatter(x=tmp2['가격'], y=tmp2['판매량/날짜수'],
                        mode='lines+markers', name='판매량/날짜수'),
                secondary_y = False,
            )
            
            fig.add_trace(
                go.Scatter(x=tmp2['가격'], y=tmp2['판매량'], mode='lines+markers', name='판매량'),
                secondary_y = True
            )
            
            fig.update_xaxes(title_text="가격")
            
            fig.update_yaxes(title_text='판매량', secondary_y=True, tickformat='000')
            fig.update_yaxes(title_text='판매량/날짜수', secondary_y=False, tickformat='000')
            
            col2.plotly_chart(fig, use_container_width=True)
        
        
if __name__ == '__main__':
    main()