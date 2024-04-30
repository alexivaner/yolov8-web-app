# backend/app.py
from fastapi import FastAPI, File, UploadFile
from typing import List

# Import your Pydantic data models from data.py
from data import Skeleton

app = FastAPI()

# Example route that accepts JSON data
@app.post("/json")
async def process_json_data(data: Skeleton):
    # Process the received JSON data here
    return {"message": "Received JSON data", "data": data.dict()}

# Example route that accepts file uploads
@app.post("/upload")
async def process_upload_file(file: UploadFile = File(...)):
    # Process the uploaded file here (e.g., run YOLOv8 model)
    # Example: Save the file locally
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": "File uploaded successfully"}

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
