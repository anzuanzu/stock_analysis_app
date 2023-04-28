import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime


def calculate_std(row, recent_years):
    eps_values = row[recent_years]
    return np.std(eps_values)


def analyze_data(file, current_year):
    data = pd.read_excel(file, engine='openpyxl')  # 使用 'openpyxl' 引擎替換 'xlrd'


    years = [f"{year}年度每股盈餘(元)" for year in range(current_year - 1, current_year - 6, -1)]
    dividend_years = [f"{year}合計股利" for year in range(current_year - 1, current_year - 6, -1)]

    data["盈餘標準差"] = data.apply(lambda row: calculate_std(row, years), axis=1)
    data["近5年平均EPS(元)"] = data[years].mean(axis=1)
    data["近5年平均合計股利(元)"] = data[dividend_years].mean(axis=1)
    data["股利發放率"] = data["近5年平均合計股利(元)"] / data["近5年平均EPS(元)"]

    sorted_data = data.sort_values("盈餘標準差", ascending=False)

    return sorted_data[["代號", "名稱", "盈餘標準差", "近5年平均EPS(元)", "近5年平均合計股利(元)", "股利發放率"]]


st.title("股票分析工具")

uploaded_file = st.file_uploader("選擇一個 .xlsx 文件", type="xlsx")  # 將 type 更改為 'xlsx'
current_year = st.number_input("請輸入當前年份：", min_value=1900, max_value=9999, value=2023, step=1)


if uploaded_file is not None:
    if st.button("分析"):
        result = analyze_data(uploaded_file, current_year)
        for i in range(1, 10):
            st.subheader(f"代號 {i} 開頭的股票")
            display_data = result[result["代號"].apply(lambda x: str(x).startswith(str(i)))]
            st.write(display_data)
else:
    st.warning("請選擇一個文件進行分析。")
