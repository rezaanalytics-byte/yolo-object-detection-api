from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from ultralytics import YOLO
import io

app = FastAPI(title="YOLOv8 Object Detection API")

# بارگذاری مدل (از مدل پایه یا مدل سفارشی شما)
model_path = "yolov8n.pt" # می‌توانید مسیر best.pt خود را هم اینجا بگذارید
model = YOLO(model_path)

@app.post("/predict/")
async def predict_image(file: UploadFile = File(...)):
    # 1. خواندن عکس آپلود شده
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # 2. اجرای مدل YOLO
    results = model.predict(source=img, conf=0.5, verbose=False)
    
    # 3. استخراج نتایج
    detections = []
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]
        conf = float(box.conf[0])
        detections.append({
            "class": cls_name,
            "confidence": round(conf, 4)
        })
    
    return JSONResponse(content={"detections": detections})

@app.get("/")
async def root():
    return {"message": "YOLOv8 API is running! Send a POST request to /predict/ with an image."}