import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from recommendation_module import recommend_places
from preprocessing_module import preprocess_text, create_stopwords
from weather_module import get_weather

# Đọc dữ liệu từ file Excel
file_path = "DataSet.xlsx"
df = pd.read_excel(file_path)

# Tạo danh sách stopwords từ DataFrame
vietnamese_stopwords = create_stopwords(df)

# Tiền xử lý mô tả trong DataFrame
df['Mô tả sau tách'] = df['Mô tả'].apply(lambda x: preprocess_text(str(x), vietnamese_stopwords))

# Tạo TF-IDF matrix từ mô tả đã xử lý
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df['Mô tả sau tách'])

# Giao diện Streamlit
st.set_page_config(page_title="Vietnam Travel Recommendation System", layout="wide")

# Tiêu đề lớn hơn
st.markdown("<h1 style='text-align: center; color: white; font-size: 40px;'>Vietnam Travel Recommendation System</h1>", unsafe_allow_html=True)

# Hướng dẫn với chữ to hơn
st.write("<h3 style='font-size: 20px;'>Nhập ba từ khóa để tìm kiếm các địa điểm du lịch tại Việt Nam phù hợp nhất.</h3>", unsafe_allow_html=True)

# Các input từ người dùng
keyword1 = st.text_input("Keyword 1", placeholder="Enter first keyword (e.g., beach)")
keyword2 = st.text_input("Keyword 2", placeholder="Enter second keyword (e.g., mountain)")
keyword3 = st.text_input("Keyword 3", placeholder="Enter third keyword (e.g., culture)")

if st.button("Submit"):
    if not (keyword1 and keyword2 and keyword3):
        st.write("<h4 style='font-size: 18px; color: red;'>Vui lòng nhập đủ 3 từ khóa.</h4>", unsafe_allow_html=True)
    else:
        # Nhập ba từ khóa từ người dùng
        user_keywords = [keyword1, keyword2, keyword3]
        
        # Gọi hàm để gợi ý các địa điểm
        recommendations = recommend_places(user_keywords, df, tfidf, tfidf_matrix, num_recommendations=3)

        # Hiển thị các địa điểm gợi ý với chữ to hơn
        st.write("<h3 style='font-size: 22px;'>Các địa điểm gợi ý phù hợp:</h3>", unsafe_allow_html=True)
        for _, row in recommendations.iterrows():
            # Tạo 3 cột cho mỗi địa điểm
            col1, col2, col3 = st.columns([4, 4, 4])  # Cột 1 và cột 2 chia đều không gian, cột 3 để trống

            # Dòng 1: Tên địa điểm với chữ lớn hơn
            with col1:
                st.markdown(f"<h4 style='font-size: 20px; font-weight: bold;'>{row['Tên địa điểm']}</h4>", unsafe_allow_html=True)
                st.write(f"**Vị trí:** {row.get('Vị trí', 'Không rõ')}")

            # Dòng 2: Mô tả với chữ lớn hơn
            with col1:
                st.write(f"<p style='font-size: 18px;'><strong>Mô tả:</strong> {row['Mô tả']}</p>", unsafe_allow_html=True)

            # Dòng 3: Hình ảnh địa điểm và thông tin thời tiết
            with col1:
                if pd.notna(row['Ảnh']):
                    st.image(row['Ảnh'], caption=row['Tên địa điểm'], width=350)  # Hiển thị ảnh
                else:
                    st.write("Không có ảnh")

            with col2:
                if pd.notna(row['Vị trí']):
                    weather = get_weather(row['Vị trí'])
                    if weather:
                        st.write(f"<h4 style='font-size: 18px;'>Thời tiết tại {row['Vị trí']}:</h4>", unsafe_allow_html=True)
                        col1, col2 = st.columns([1, 5])
                        with col1:
                            if weather["icon"]:
                                st.image(weather["icon"], width=50)  # Hiển thị icon thời tiết
                        with col2:
                            st.write(f"- Nhiệt độ: {weather['temperature']}°C")
                            st.write(f"- Mô tả: {weather['description']}")
                            st.write(f"- Độ ẩm: {weather['humidity']}%")
                    else:
                        st.write(f"Không thể lấy thông tin thời tiết cho {row['Vị trí']}.")
                else:
                    st.write("Không có thông tin thời tiết.")
