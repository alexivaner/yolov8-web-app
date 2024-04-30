# streamlit_yolo_app.py

import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Frontend (Streamlit) part
st.title('YOLOv8 Object Detection')

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Send image to FastAPI
    files = {'file': uploaded_file.getvalue()}
    response = requests.post('http://localhost:8000/upload', files=files)

    if response.status_code == 200:
        result_json = response.json()
        st.json(result_json)
        # Visualize bounding boxes on the image
        for detection in result_json['predictions']:
            label = detection['label']
            confidence = detection['confidence']
            box = detection['box']
            st.image(image.crop(box), caption=f'{label} ({confidence:.2f})', use_column_width=True)