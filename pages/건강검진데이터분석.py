import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 데이터 로드 및 캐싱
@st.cache
def load_data():
    try:
        # 디버깅: 현재 디렉토리와 파일 확인
        st.write(f"Current directory: {os.getcwd()}")
        st.write("Files in the directory:", os.listdir(os.getcwd()))

        # 파일 경로 수정 (대소문자 정확히 지정)
        data = pd.read_csv('Healthtest_2023reduced.CSV', encoding="cp949")  # 한글 인코딩 변경
        return data
    except UnicodeDecodeError:
        try:
            data = pd.read_csv('Healthtest_2023reduced.CSV', encoding="utf-8")  # utf-8 시도
            return data
        except Exception as e:
            st.error(f"Error loading data with 'utf-8' encoding: {e}")
            return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# 앱 제목
st.title("Health Test Data: Blood Pressure Correlation Analysis")

data = load_data()

if data is not None:
    # 데이터프레임 표시
    st.header("Dataset Overview")
    st.write("Displaying the first few rows of the dataset:")
    st.dataframe(data.head())

    # 컬럼 이름 출력
    st.header("Column Names in Dataset")
    st.write("Columns available in the dataset:")
    st.write(data.columns.tolist())

    # 상관 분석 수행
    st.header("Identify Top Factors Correlated with Blood Pressure")
    numeric_data = data.select_dtypes(include=['float64', 'int64'])  # 숫자형 데이터만 선택

    # 사용자 지정 혈압 관련 컬럼 이름
    systolic_bp_column = st.text_input("Enter the column name for Systolic Blood Pressure (최고혈압):", "최고혈압")
    diastolic_bp_column = st.text_input("Enter the column name for Diastolic Blood Pressure (최저혈압):", "최저혈압")

    # 상관 분석에서 제외할 컬럼 설정
    excluded_columns = [systolic_bp_column, diastolic_bp_column]

    if systolic_bp_column in numeric_data.columns and diastolic_bp_column in numeric_data.columns:
        # 두 혈압 컬럼을 제외한 상관 분석
        correlation_matrix = numeric_data.drop(columns=excluded_columns).corr()

        st.write("Correlation analysis excluding blood pressure columns:")
        bp_combined = numeric_data[[systolic_bp_column, diastolic_bp_column]].mean(axis=1)  # 혈압 평균 계산
        correlation_with_bp_combined = numeric_data.corrwith(bp_combined).sort_values(ascending=False)

        # 상위 3개의 요인 추출
        top_factors = [col for col in correlation_with_bp_combined.index if col not in excluded_columns][:3]

        st.write("Top 3 factors correlated with blood pressure (excluding systolic and diastolic blood pressure):")
        for i, factor in enumerate(top_factors, 1):
            st.write(f"{i}. {factor} (Correlation: {correlation_with_bp_combined[factor]:.2f})")

        # 산점도 및 상관계수 시각화
        st.header("Scatter Plots of Top Factors vs Blood Pressure")
        for factor in top_factors:
            st.write(f"Scatter plot of {factor} vs Blood Pressure (Correlation: {correlation_with_bp_combined[factor]:.2f}):")
            fig, ax = plt.subplots()
            sns.scatterplot(x=numeric_data[factor], y=bp_combined, ax=ax)
            ax.set_title(f"{factor} vs Blood Pressure")
            st.pyplot(fig)
    else:
        st.error("Please ensure both systolic and diastolic blood pressure columns are correctly specified.")
else:
    st.error("Data could not be loaded. Please ensure the file exists and is correctly formatted.")
