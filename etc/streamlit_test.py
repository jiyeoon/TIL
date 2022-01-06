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
        '날짜' : ast.literal_eval(info['train_ds']),
        '판매량' : np.square(ast.literal_eval(info['train_y'])),
        '가격' : ast.literal_eval(info['train_avg_prc'])
    }
    
    result = pd.DataFrame(dic)
    result['날짜'] = pd.to_datetime(result['날짜'])
    st.dataframe(result)
    
    st.write("### 일자별 판매량 - 가격 그래프")
    fig, ax = plt.subplots()
    ax.plot(result['날짜'], result['판매량'], label='sales', ls='-')
    ax.set_ylabel('판매량')
    plt.legend()
    ax2 = ax.twinx()
    ax2.set_ylabel('가격')
    plt.plot(result['날짜'], result['가격'], color='deeppink', label='price')
    plt.legend()
    
    st.write("파란색 선 : 판매량, 분홍색 선 : 가격")
    st.pyplot(fig)
    
    st.write("### 가격 - 판매량 관계 그래프")
    tmp2 = result.groupby('가격').sum('판매량')
    st.dataframe(tmp2)
    st.line_chart(tmp2)
    