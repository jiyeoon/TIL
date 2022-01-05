from re import M
import streamlit as st
import pandas as pd
import ast 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.write("""
            # Dynamic Pricing Demo Page
         """)


df = pd.read_csv('./data/ctlg_training_data_220104.csv')
#st.write(df.dtypes)

ctlg_no = st.text_input('Enter catalog no', '13917540')

if st.button('Enter'):
    tmp = df[df.ctlg_no == int(ctlg_no)]
    info = tmp.iloc[0]
    dic = {
        'ds' : ast.literal_eval(info['train_ds']),
        'y' : np.square(ast.literal_eval(info['train_y'])),
        'avg_prc' : ast.literal_eval(info['train_avg_prc'])
    }
    
    result = pd.DataFrame(dic)
    result['ds'] = pd.to_datetime(result['ds'])
    st.dataframe(result)
    
    st.write("### 일자별 판매량 - 가격 그래프")
    fig, ax = plt.subplots()
    ax.plot(result['ds'], result['y'], label='sales', ls='-')
    ax.set_ylabel('sales')
    plt.legend()
    ax2 = ax.twinx()
    ax2.set_ylabel('price')
    plt.plot(result['ds'], result['avg_prc'], color='deeppink', label='price')
    plt.legend()
    
    st.write("파란색 선 : sales, 분홍색 선 : price")
    st.pyplot(fig)
    
    st.write("### 가격 - 판매량 관계 그래프")
    tmp2 = result.groupby('avg_prc').sum('y')
    st.dataframe(tmp2)
    st.line_chart(tmp2)
    