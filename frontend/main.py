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
        
        # Convert JSON string to Python object
        detections = result_json['detections']
        
        #Visualize image from the filename in result_json
        outputFilename = result_json['filename']
        outputFilename = '../backend/'+outputFilename
        outputImage = Image.open(outputFilename)
        st.image(outputImage, caption='Processed Image', use_column_width=True)
        
    
        # # Visualize bounding boxes on the image
        # for detection in detections:
        #     print(detection)
        #     label = detection['name']
        #     confidence = detection['confidence']
            
        #     #extract box from x1,y1,x2,y2
        #     box = detection['box']
        #     box = (box['x1'], box['y1'], box['x2'], box['y2'])
            
        #     st.image(image.crop(box), caption=f'{label} ({confidence:.2f})', use_column_width=True)
            
