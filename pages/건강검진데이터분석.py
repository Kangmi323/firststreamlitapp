import streamlit as st
import pandas as pd

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
st.title("Health Test Data Analysis")

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

    # 데이터 통계 정보
    st.header("Descriptive Statistics")
    st.write("Statistical summary of numeric columns:")
    st.write(data.describe())

    # 컬럼 선택
    st.header("Column Analysis")
    selected_column = st.selectbox("Select a column for detailed analysis:", data.columns)

    if selected_column:
        st.write(f"Displaying details for column: {selected_column}")
        st.write(data[selected_column].describe())

        # 데이터 타입에 따른 시각화
        if pd.api.types.is_numeric_dtype(data[selected_column]):
            st.line_chart(data[selected_column])
        else:
            st.bar_chart(data[selected_column].value_counts())

    # 데이터 필터링
    st.header("Data Filtering")
    filter_column = st.selectbox("Select a column to filter:", data.columns)

    if filter_column:
        unique_values = data[filter_column].unique()
        selected_values = st.multiselect(
            f"Select values from column '{filter_column}':", unique_values
        )

        if selected_values:
            filtered_data = data[data[filter_column].isin(selected_values)]
            st.write(f"Filtered data based on {filter_column} values:")
            st.dataframe(filtered_data)

    # 데이터 저장 옵션
    st.header("Download Filtered Data")
    st.write("You can download the filtered dataset as a CSV file.")
    if 'filtered_data' in locals():
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv"
        )
    else:
        st.write("No filtered data available to download.")
else:
    st.write("Please upload a CSV file to get started.")
