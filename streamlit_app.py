import streamlit as st
import pandas as pd
import os

# 设置本地 CSV 文件路径
csv_path = r"C:\Users\b00\Downloads\SPPALL\Quickly_get_faccts_sale.csv"

st.title("CSV 数据筛选器")

# 检查文件是否存在
if os.path.exists(csv_path):
    st.success(f"找到本地文件: `{csv_path}`")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"读取文件时出错: {e}")
        df = None
else:
    st.warning(f"本地文件未找到: `{csv_path}`，请上传 CSV 文件！")
    uploaded_file = st.file_uploader("选择 CSV 文件", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("文件上传成功！")
        except Exception as e:
            st.error(f"读取上传文件时出错: {e}")
            df = None
    else:
        df = None

# 只有当 df 不为空时，才显示筛选选项
if df is not None:
    # 选择筛选列
    filter_column = st.selectbox("选择要筛选的列", df.columns)

    # 获取唯一值
    unique_values = df[filter_column].dropna().unique()

    # 多选筛选器
    selected_values = st.multiselect("选择要筛选的值", unique_values)

    # 筛选数据
    if selected_values:
        filtered_df = df[df[filter_column].isin(selected_values)]
    else:
        filtered_df = df  # 若未选择筛选项，则显示全部数据

    # 显示数据
    st.write(filtered_df)

    # 允许下载筛选后的数据
    csv_download = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="下载筛选后的数据",
        data=csv_download,
        file_name="filtered_data.csv",
        mime="text/csv",
    )


