import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm

# Webアプリの説明
st.title('二元配置分散分析')
st.write('二元配置分散分析を行うWebアプリです。')
st.caption("created by Dit-lab.(Daiki Ito)")

# Excelファイルのアップロード
st.write('以下のExcelファイルをアップロードしてください。')
uploaded_file = st.file_uploader("ファイルを選択", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Excelファイルの読み込み
    df = pd.read_excel(uploaded_file)
    st.write('データプレビュー')
    st.dataframe(df)

    # 独立変数を2つ選択（数値変数は除外）
    st.write('独立変数を2つ選択してください。')
    col_list = df.columns.tolist()
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = [col for col in col_list if col not in num_cols]
    if len(cat_cols) < 2:
        st.error("カテゴリー変数が2つ以上必要です。")
    else:
        col1 = st.selectbox('独立変数1', cat_cols)
        remaining_cols = [col for col in cat_cols if col != col1]
        col2 = st.selectbox('独立変数2', remaining_cols)

        # 従属変数を選択（数値変数のみ）
        st.write('従属変数を選択してください。')
        col3 = st.multiselect('従属変数', num_cols)
        
        if col3:
            # 二元配置分散分析の実行
            st.write('## 二元配置分散分析の結果')
            anova_tables = []
            for dv in col3:
                formula = f'{dv} ~ C({col1}) + C({col2}) + C({col1}):C({col2})'
                model = ols(formula, data=df).fit()
                anova_table = sm.stats.anova_lm(model, typ=2)
                anova_table['従属変数'] = dv
                anova_tables.append(anova_table.reset_index())
            anova_results = pd.concat(anova_tables)
            st.write(anova_results)

            # 多重比較（TukeyのHSD検定）
            st.write('## 多重比較結果（TukeyのHSD検定）')
            df['group'] = df[col1].astype(str) + '_' + df[col2].astype(str)
            for dv in col3:
                tukey = pairwise_tukeyhsd(endog=df[dv], groups=df['group'], alpha=0.05)
                st.write(f'### {dv}')
                st.write(tukey.summary())

            # 可視化
            st.write('## グラフによる可視化')
            for dv in col3:
                mean_df = df.groupby([col1, col2])[dv].mean().reset_index()
                sem_df = df.groupby([col1, col2])[dv].sem().reset_index()
                mean_df['SEM'] = sem_df[dv]
                fig = px.bar(mean_df, x=col1, y=dv, color=col2, barmode='group', error_y='SEM', title=f'{dv}の平均値と標準誤差')
                st.plotly_chart(fig)
        else:
            st.error("従属変数を選択してください。")
