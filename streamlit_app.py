##streamlitで二元配置分散分駅
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from scipy import stats

#Webアプリの説明
st.title('二元配置分散分析')
st.write('二元配置分散分析を行うWebアプリです。')
st.caption("created by Dit-lab.(Daiki Ito)")

#Excelファイルのアップロード
st.write('以下のExcelファイルをアップロードしてください。')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    #Excelファイルの読み込み
    df = pd.read_excel(uploaded_file)
    st.write(df)
    #独立変数を２つ選択（数値変数は表示しない、データ型で判断）
    st.write('独立変数を２つ選択してください。')
    col_list = df.columns
    col_list_num = df._get_numeric_data().columns
    col_list_str = list(set(col_list) - set(col_list_num))
    col1 = st.selectbox('独立変数1', col_list_str)
    col2 = st.selectbox('独立変数2', col_list_str)
    #従属変数を選択（数値変数のみ候補に表示、複数選択可）
    st.write('従属変数を選択してください。')
    col_list = df.columns
    col_list_num = df._get_numeric_data().columns
    col_list_str = list(set(col_list) - set(col_list_num))
    col3 = st.multiselect('従属変数', col_list_num)
    #二元配置分散分析
    st.write('## 二元配置分散分析')
    #分析に使う変数の確認（clo1・col2によるcol3の平均値の差を検定します。）
    st.write('以下のデータについて、'+col1+'と'+col2+'による'+str(col3)+'の平均値の差を検定します。')
    st.write(df)
    #二元配置分散分析の実行
    df[col1] = df[col1].astype(str)
    df[col2] = df[col2].astype(str)
    df[col1+'_'+col2] = df[col1] + '_' + df[col2]
    anova = pd.DataFrame(index=col3, columns=['F値', 'p値'])
    for i in col3:
        model = ols(i + ' ~ ' + col1 + ' * ' + col2, data=df).fit()
        anova.loc[i, 'F値'] = model.fvalue
        anova.loc[i, 'p値'] = model.f_pvalue
    st.write(anova)
    #二元配置分散分析の結果の可視化
    st.write('## 可視化')
    #箱ひげ図（有意水準に応じてブラケットとアノテーションを表示）
    #p<0.01の場合は**、p<0.05の場合は*、p<0.1の場合は†を表示
    for i in col3:
        fig = px.box(df, x=col1, y=i, color=col2, points='all')
        fig.update_layout(title=i+'の箱ひげ図')
        st.plotly_chart(fig)
    
    #分散分析表
    st.write('## 分散分析表')
    st.write(anova)
    #F分布のパラメータ
    st.write('## F分布のパラメータ')
    st.write('有意水準：0.05')
    st.write('自由度1：'+str(anova.shape[0]-1))
    st.write('自由度2：'+str(df[col1].nunique()-1))
    st.write('自由度3：'+str(df[col2].nunique()-1))
    st.write('自由度4：'+str((df[col1].nunique()-1)*(df[col2].nunique()-1)))
    #F分布表
    st.write('## F分布表')
    st.write('自由度1：'+str(anova.shape[0]-1))
    st.write('自由度2：'+str(df[col1].nunique()-1))
    st.write('自由度3：'+str(df[col2].nunique()-1))
    st.write('有意水準：0.05')
    
    
    
    