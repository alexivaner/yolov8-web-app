# backend/app.py
from fastapi import HTTPException,FastAPI, UploadFile, File
from typing import List
from PIL import Image
import io
from ultralytics import YOLO
from data import Skeleton
from pydantic import ValidationError

app = FastAPI()
# Load a model
# modelDetection = YOLO('yolov8n.pt')  # pretrained YOLOv8n model
modelPose = YOLO('yolov8n-pose.pt')  # load an official model

def convert_and_validate(data):
    converted_data = []
    for item in data:
        keypoints = []
        for i in range(len(item["keypoints"]["x"])):
            keypoint = {
                "name": f"point{i+1}",
                "point": {
                    "x": item["keypoints"]["x"][i],
                    "y": item["keypoints"]["y"][i],
                    "z": item["keypoints"]["visible"][i]
                },
                "flags": None
            }
            keypoints.append(keypoint)

        skeleton = {
            "name": item["name"],
            "points": keypoints
        }
        converted_data.append(skeleton)

    try:
        for skeleton_data in converted_data:
            Skeleton(**skeleton_data)
        return True
    except ValidationError as e:
        return False

@app.post("/upload")
async def process_upload_file(file: UploadFile = File(...)):
    print("Processing uploaded file", file.content_type)
    try:
        # Check if the uploaded file is an image    
        # Read image data
        contents = await file.read()
        filename = file.filename

        if file.content_type.startswith("image"):
            image = Image.open(io.BytesIO(contents))
            #get image filename
            pose_result_filename = 'tmp/{}_pose_result.jpg'.format(filename)
            pose_json_filename = 'tmp/{}_pose_result.json'.format(filename)
            
        
        # Process the uploaded image using YOLO
        poses = modelPose(image)  # Assuming YOLO model can directly process PIL images
        for pose in poses:
            pose.save(filename=pose_result_filename)  # save to disk
            poseJson = pose.tojson()            
            #save poseJson as json file
            with open(pose_json_filename, 'w') as f:
                # no need to dump again
                f.write(poseJson)
            
        #Validate with pydantic
        validated = convert_and_validate(pose.summary())
        if(validated):
            print("Data is valid")
            return {"message": "Image uploaded successfully","poses":pose.summary(),
                    "poseFilename": pose_result_filename,
                    "poseJsonFilename": pose_json_filename}
        else:
            print("Data is invalid")
            raise HTTPException(status_code=400, detail="Invalid data")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid file")
    


