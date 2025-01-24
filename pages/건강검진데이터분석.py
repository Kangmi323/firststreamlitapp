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
st.title("Health Test Data: Blood Pressure Correlation Analysis")

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
    st.header("Identify Top Factors Correlated with Blood Pressure")
    numeric_data = data.select_dtypes(include=['float64', 'int64'])  # 숫자형 데이터만 선택

    if "혈압" in numeric_data.columns:
        st.write("Calculating correlation with 혈압:")
        correlation_with_bp = numeric_data.corr()["혈압"].sort_values(ascending=False)
        top_factors = correlation_with_bp.index[1:4]  # 상위 3가지 요인 추출

        st.write("Top 3 factors correlated with 혈압:")
        for i, factor in enumerate(top_factors, 1):
            st.write(f"{i}. {factor} (Correlation: {correlation_with_bp[factor]:.2f})")

        # 산점도 그리기
        st.header("Scatter Plots of Top Factors vs 혈압")
        for factor in top_factors:
            st.write(f"Scatter plot of {factor} vs 혈압:")
            fig, ax = plt.subplots()
            sns.scatterplot(x=numeric_data[factor], y=numeric_data["혈압"], ax=ax)
            ax.set_title(f"{factor} vs 혈압")
            st.pyplot(fig)
    else:
        st.error("Column '혈압' not found in the dataset. Please check the column names.")
else:
    st.write("Please upload a CSV file to get started.")
