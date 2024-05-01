# backend/app.py
from fastapi import HTTPException, FastAPI, UploadFile, File
from typing import List
from PIL import Image
import io
from ultralytics import YOLO
import ujson


# Import your Pydantic data models from data.py
from data import Skeleton


app = FastAPI()
# Load a model
model = YOLO('yolov8n.pt')  # pretrained YOLOv8n model

# Example route that accepts JSON data
@app.post("/json")
async def process_json_data(data: Skeleton):
    # Process the received JSON data here
    return {"message": "Received JSON data", "data": data.dict()}

@app.post("/upload")
async def process_upload_file(file: UploadFile = File(...)):
    # Check if the uploaded file is an image    
    # Read image data
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    #get image filename
    filename = file.filename
    result_filename = 'tmp/{}_result.jpg'.format(filename)
    json_filename = 'tmp/{}_result.json'.format(filename)

    # Process the uploaded image using YOLO
    # Example: Run YOLO model on the image (replace this with your actual YOLO processing)
    # Note: You may need to convert the image to a format suitable for YOLO
    #       and then process the detections accordingly.
    detections = model(image)  # Assuming YOLO model can directly process PIL images
    
    # You can further process 'detections' here
    # Process results list
    for result in detections:
        # result.show()  # display to screen
        result.save(filename=result_filename)  # save to disk
        
        resultJson = result.tojson()
        
        #save resultJson as json file
        with open(json_filename, 'w') as f:
            # no need to dump again
            f.write(resultJson)
        
        print("name",result.summary())
    
        
        
    # to json
    return {"message": "Image uploaded successfully", "detections": result.summary(), "filename": result_filename}

    
# Example route that accepts form data with multiple files
@app.post("/upload/multiple")
async def process_multiple_files(files: List[UploadFile] = File(...)):
    # Process the uploaded files here (e.g., run YOLOv8 model on each file)
    # Example: Save each file locally
    for file in files:
        with open(file.filename, "wb") as buffer:
            buffer.write(await file.read())
    return {"message": "Multiple files uploaded successfully"}

# Example route that accepts both JSON data and file uploads
@app.post("/mixed")
async def process_mixed_data(file: UploadFile = File(None), data: Skeleton = None):
    # Process the received data here (both JSON and file uploads)
    # Example: Run YOLOv8 model on the uploaded file and/or process JSON data
    response = {"message": "Mixed data received"}
    if file:
        with open(file.filename, "wb") as buffer:
            buffer.write(await file.read())
        response["file_uploaded"] = True
    if data:
        response["json_data"] = data.dict()
    return response
