import streamlit as st
import pytesseract
from PIL import Image
import re
from fuzzywuzzy import fuzz

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

st.title("Распознавание текста с изображения")

uploaded_file = st.file_uploader("Загрузите изображение", type=["png", "jpg", "jpeg"])


def extract_fio(text):
 
    pattern = r'([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)\s+([А-ЯЁ][а-яё]+)'
    matches = re.findall(pattern, text)
    
    unique_fio = []
    
    def is_similar(new_fio, existing_fio):
        return fuzz.ratio(new_fio, existing_fio) >= 90  

    for fio in matches:
        fio_str = " ".join(fio)
        if not any(is_similar(fio_str, existing) for existing in unique_fio):
            unique_fio.append(fio_str)
    
    return unique_fio


def extract_birth_dates(text):

    date_pattern = r'(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})'
    dates = re.findall(date_pattern, text)
    
    unique_dates = set(dates)
    
    return unique_dates


if uploaded_file is not None:
    
    image = Image.open(uploaded_file)
    
    st.image(image, caption="Загруженное изображение", use_column_width=True)
    

    if st.button("Распознать текст"):
        
        text = pytesseract.image_to_string(image, lang='rus')
        
        fio_list = extract_fio(text)
        
        if fio_list:
            st.subheader("Найденные ФИО:")
            for fio in fio_list:
                st.text(fio)  
        else:
            st.text("ФИО не найдено.")

        birth_dates = extract_birth_dates(text)
        
        if birth_dates:
            st.subheader("Найденные даты рождения:")
            for date in birth_dates:
                st.text(date)  
        else:
            st.text("Дата рождения не найдена.")
