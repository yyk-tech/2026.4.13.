import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import platform
from supabase import create_client, Client


# 1. Supabase 연결 (비밀키 사용)
@st.cache_resource
def init_connection() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


# 2. 데이터 불러오기 (수파베이스에서 직접 가져옴!)
@st.cache_data
def load_data():
    supabase = init_connection()
    response = supabase.table("student_data").select("*").execute()
    return pd.DataFrame(response.data)


# 3. 한글 폰트 설정
def set_korean_font():
    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Darwin':
        plt.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False


# --- 메인 웹 UI ---
st.title("데이터 상관 관계 분석")

try:
    df = load_data()  # CSV 파일 없이 여기서 데이터를 짜잔! 하고 불러옵니다.

    st.subheader("원본 데이터")
    st.dataframe(df)

    st.subheader("상관 관계 히트맵")
    set_korean_font()

    # 숫자형 데이터만 추출하여 상관계수 계산
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax, vmin=-1, vmax=1)
    st.pyplot(fig)

    st.subheader("분석 결과 해석")
    st.write('''
    * **강한 양의 상관관계**: 서로 비례하여 함께 증가하는 요소들입니다. (예: 공부시간과 점수)
    * **강한 음의 상관관계**: 하나가 증가할 때 다른 하나는 감소하는 반비례 요소들입니다. (예: 게임시간과 점수)
    ''')
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")