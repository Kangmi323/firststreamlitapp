import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 로드 및 캐싱
@st.cache
def load_data(file):
    try:
        data = pd.read_csv(file, encoding="utf-8")
        return data
    except UnicodeDecodeError:
        try:
            data = pd.read_csv(file, encoding="latin1")  # 다른 일반적인 인코딩
            return data
        except Exception as e:
            st.error(f"Error loading data with 'latin1' encoding: {e}")
            return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# 앱 제목
st.title("Health Test Data Correlation Analysis")

# 파일 업로드
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

data = None
if uploaded_file is not None:
    data = load_data(uploaded_file)

if data is not None:
    # 데이터프레임 표시
    st.header("Dataset Overview")
    st.write("Displaying the first few rows of the dataset:")
    st.dataframe(data.head())

    # 상관 분석 수행
    st.header("Correlation Analysis")
    numeric_data = data.select_dtypes(include=['float64', 'int64'])  # 숫자형 데이터만 선택

    if not numeric_data.empty:
        st.write("Calculating correlation matrix for numeric columns:")
        correlation_matrix = numeric_data.corr()

        # 상관 행렬 시각화
        st.write("Correlation matrix:")
        st.dataframe(correlation_matrix)

        st.write("Heatmap of the correlation matrix:")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        # 사용자 선택 기반 상관 관계 확인
        st.header("Analyze Pairwise Correlation")
        column_options = list(numeric_data.columns)
        col1, col2 = st.selectbox("Select first column:", column_options), st.selectbox("Select second column:", column_options)

        if col1 and col2:
            correlation_value = numeric_data[col1].corr(numeric_data[col2])
            st.write(f"Correlation between {col1} and {col2}: {correlation_value:.2f}")

            # 산점도 그리기
            st.write(f"Scatter plot of {col1} vs {col2}:")
            fig, ax = plt.subplots()
            sns.scatterplot(x=numeric_data[col1], y=numeric_data[col2], ax=ax)
            ax.set_title(f"Scatter plot of {col1} vs {col2}")
            st.pyplot(fig)
    else:
        st.write("No numeric columns available for correlation analysis.")
else:
    st.write("Please upload a CSV file to get started.")
