# streamlit_yolo_app.py

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import ujson

# Frontend (Streamlit) part
st.title('YOLOv8 Object Detection')

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Split the layout into two columns
    col1, col2 = st.columns(2)

    # Display the uploaded image in the first column
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

    # Send image to FastAPI
    files = {'file': uploaded_file.getvalue()}
    response = requests.post('http://localhost:8000/upload', files=files)

    if response.status_code == 200:
        result_json = response.json()
        
        # Convert JSON string to Python object
        detections = result_json['poses']
        
        # Visualize image from the filename in result_json
        outputFilename = result_json['poseFilename']
        outputFilename = '../backend/' + outputFilename
        outputImage = Image.open(outputFilename)

        # Display the processed image in the second column
        with col2:
            st.image(outputImage, caption='Processed Image', use_column_width=True)
            # Button to download JSON text
            json_text = ujson.dumps(result_json, indent=4)
            st.download_button(
                label="Download JSON",
                data=json_text,
                file_name="result.json",
                mime="text/plain"
            )
            #Button to download image result 
            output_image_data = BytesIO()
            outputImage.save(output_image_data, format='JPEG')
            output_image_data.seek(0)

            # Button to download image result 
            st.download_button(
                label="Download Image",
                data=output_image_data,
                file_name="result.jpg",
                mime="image/jpeg"
            )
     
