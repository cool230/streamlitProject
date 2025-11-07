import pandas as pd

# 파일 경로와 인코딩을 지정하여 CSV 파일 읽기
df = pd.read_csv('산업통상자원부_전시사업(국내 전시회)_20231231.csv', encoding='cp949')  # 또는 'euc-kr', 'ISO-8859-1' 등

# 데이터 확인
print(df.head())
