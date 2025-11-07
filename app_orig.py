import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 간단한 데이터 분석 앱")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
df = None  # 초기화

if uploaded_file is not None:
    try:
        # 먼저 UTF-8로 시도
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        try:
            # CP949로 재시도
            df = pd.read_csv(uploaded_file, encoding='cp949')
        except Exception as e:
            st.error(f"📛 파일을 CP949로 읽는 데 실패했습니다: {e}")
            df = None
    except Exception as e:
        st.error(f"📛 파일을 읽는 중 오류 발생: {e}")
        df = None

    # 데이터 유효성 검사
    if df is not None and not df.empty and df.columns.size > 0:
        st.subheader("📋 데이터 미리보기")
        st.dataframe(df.head())

        st.subheader("📊 기본 통계 요약")
        st.write(df.describe())
    else:
        st.warning("⚠️ 파일은 업로드되었지만, 데이터가 없거나 열 정보가 없습니다.")
else:
    st.info("📂 분석할 CSV 파일을 업로드해주세요.")

    # 기본 통계
    st.subheader("📊 기본 통계 요약")
    st.write(df.describe())

    # 컬럼 선택
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    selected_col = st.selectbox("시각화할 숫자형 컬럼 선택", numeric_cols)

    # 히스토그램
    st.subheader(f"📉 {selected_col} 히스토그램")
    fig, ax = plt.subplots()
    ax.hist(df[selected_col], bins=20, color='skyblue', edgecolor='black')
    st.pyplot(fig)

    # 조건 필터링
    st.subheader("🔍 조건 필터링")
    filter_col = st.selectbox("필터링할 컬럼 선택", df.columns)
    unique_vals = df[filter_col].dropna().unique().tolist()
    selected_val = st.selectbox("필터링할 값 선택", unique_vals)

    filtered_df = df[df[filter_col] == selected_val]
    st.write(f"{filter_col}이(가) {selected_val}인 데이터:")
    st.dataframe(filtered_df)