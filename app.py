import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import platform
from supabase import create_client, Client

# 1. Supabase 연결
@st.cache_resource
def init_connection() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# 2. 데이터 불러오기
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

st.title("데이터 상관 관계 분석")

try:
    df = load_data()
    
    st.subheader("원본 데이터")
    st.dataframe(df)
    
    # 숫자형 데이터만 자동으로 골라내기 (이 부분이 에러를 방지합니다)
    numeric_df = df.select_dtypes(include=['number'])
    
    if not numeric_df.empty:
        st.subheader("상관 관계 히트맵")
        set_korean_font()
        
        corr = numeric_df.corr()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax, vmin=-1, vmax=1)
        st.pyplot(fig)
        
        st.subheader("분석 결과 해석")
        st.write('''
        * **강한 양의 상관관계**: 서로 비례하여 함께 증가하는 요소들입니다.
        * **강한 음의 상관관계**: 하나가 증가할 때 다른 하나는 감소하는 반비례 요소들입니다.
        ''')
    else:
        st.warning("분석할 수 있는 숫자 데이터가 없습니다. 수파베이스의 컬럼 타입을 확인해 주세요.")

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
