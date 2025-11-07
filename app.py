import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="📊 데이터 분석 대시보드", layout="wide")
st.title("📈 간단한 데이터 분석 앱")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
df = None

if uploaded_file is not None:
    try:
        # 바이트로 읽기
        bytes_data = uploaded_file.read()

        try:
            # UTF-8 시도
            df = pd.read_csv(io.BytesIO(bytes_data), encoding='utf-8')
        except UnicodeDecodeError:
            # CP949 시도
            df = pd.read_csv(io.BytesIO(bytes_data), encoding='cp949')

    except Exception as e:
        st.error(f"📛 파일을 읽는 중 오류 발생: {e}")
        df = None

if df is not None and not df.empty and df.columns.size > 0:
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    st.subheader("📊 기본 통계 요약")
    st.write(df.describe())

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        selected_col = st.selectbox("시각화할 숫자형 컬럼 선택", numeric_cols)

        st.subheader(f"📉 {selected_col} 히스토그램")
        fig, ax = plt.subplots()
        ax.hist(df[selected_col].dropna(), bins=20, color='skyblue', edgecolor='black')
        ax.set_xlabel(selected_col)
        ax.set_ylabel("빈도")
        st.pyplot(fig)
    else:
        st.info("📌 숫자형 컬럼이 없어 히스토그램을 그릴 수 없습니다.")

    st.subheader("🔍 조건 필터링")
    filter_col = st.selectbox("필터링할 컬럼 선택", df.columns)
    unique_vals = df[filter_col].dropna().unique().tolist()
    if unique_vals:
        selected_val = st.selectbox("필터링할 값 선택", unique_vals)
        filtered_df = df[df[filter_col] == selected_val]
        st.write(f"🔎 {filter_col}이(가) {selected_val}인 데이터:")
        st.dataframe(filtered_df)
    else:
        st.info("📌 필터링할 값이 없습니다.")
else:
    st.info("📂 분석할 CSV 파일을 업로드해주세요.")
