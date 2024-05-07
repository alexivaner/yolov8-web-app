import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import ujson

# Frontend (Streamlit) part
st.set_page_config(layout="wide")  # Set layout to wide for better organization

# Title and description
st.title('YOLOv8 Object Detection')
st.markdown("""
            Upload an image or video to detect objects using YOLOv8.
            """)

# Upload image or video
uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    if uploaded_file.type == "video/mp4":
        # Display video in the first column
        with col1:
            video_bytes = uploaded_file.read()
            st.video(video_bytes, format='video/mp4')
    else:
        # Display uploaded image in the first column
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)

        # Send image to FastAPI
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'image/jpeg')}
        response = requests.post('http://localhost:8000/upload', files=files)

        if response.status_code == 200:
            result_json = response.json()

            # Display processed image and download buttons in the second column
            outputFilename = '../backend/' + result_json['poseFilename']
            outputImage = Image.open(outputFilename)

            with col2:
                st.image(outputImage, caption='Processed Image', use_column_width=True)

                # Display download buttons side by side
                download_col1, download_col2 = st.columns(2)

                # Download JSON button
                json_text = ujson.dumps(result_json, indent=4)
                download_col1.download_button(
                    label="Download JSON",
                    data=json_text,
                    file_name="result.json",
                    mime="text/plain",
                    key="json-download"
                )

                # Download image button
                output_image_data = BytesIO()
                outputImage.save(output_image_data, format='JPEG')
                output_image_data.seek(0)

                download_col2.download_button(
                    label="Download Image",
                    data=output_image_data,
                    file_name="result.jpg",
                    mime="image/jpeg",
                    key="image-download"
                )

# Add some spacing at the bottom for better aesthetics
st.markdown("<br>", unsafe_allow_html=True)
