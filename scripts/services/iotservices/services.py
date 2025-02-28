## video and microphone sensor sm, 1. data source, 2. handle images and audios
# iot device : pressure sensor sm, seat sensor sm
# edge device : detect
# cloud device :
import base64
import json
import cv2
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
import pandas as pd
import numpy as np
import logging
from typing import List, Dict

app = FastAPI()

# initial logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# simulate pressure data
pressure_data: List[Dict[str, float]] = []

# ## video sensor
# # sensor captures frame
# def capture_frame():
#     # video stream cature frame.
#     frame = np.ramdom.randint(0, 256, (480, 640, 3), dtype=np.uint8)
#     return frame
#
# @app.post("/capture_video")
# async def capture_video(request: Request):
#     frame = capture_frame()
#
#     #Encoding image frame as base64
#     _, buffer = cv2.imencode('.jpg', frame)
#     frame_data = base64.b64decode(buffer).decode('utf-8')
#
#     response_data = {"frame": frame_data}
#     response = json.dump(response_data)
#
#     return Response(content=response, media_type="application/json")


# sensor pressure
# 1: data transmission, initial state
@app.post("/transmit")
async def transmit(request: Request):
    data = await request.json()
    if not data or "data" not in data:
        raise HTTPException(status_code=400, detail="No data provided")

    # store data in global
    global pressure_data
    pressure_data.extend(data["data"])  # 追加新数据

    return {"message": "Data transmitted successfully", "received_data": data["data"]}


# 2. preprocessing
@app.post("/preprocess")
async def preprocess():
    global pressure_data
    if not pressure_data:
        raise HTTPException(status_code=400, detail="No data available for preprocessing")

    #  DataFrame, add timestamp
    df = pd.DataFrame(pressure_data, columns=['pressure'])
    df['timestamp'] = pd.date_range(start='26/2/2025', periods=len(df), freq='T')

    # update global data
    pressure_data = df.to_dict('records')

    return {"message": "Data preprocessed successfully", "data": pressure_data}


# 4. recording logs
@app.post("/log")
async def log():
    global pressure_data
    if not pressure_data:
        raise HTTPException(status_code=400, detail="No data available to log")

    # record data
    for record in pressure_data:
        logger.info(f"Record: {record}")

    return {"message": "Data logged successfully"}


# 5. notifying
@app.post("/notify")
async def notify():
    global pressure_data
    if not pressure_data:
        raise HTTPException(status_code=400, detail="No data available to notify")

    # print abnormal data
    anomalies = [record for record in pressure_data if record.get('anomaly', 0) == 1]
    for anomaly in anomalies:
        logger.info(f"Anomaly detected: {anomaly}")

    return {"message": "Notification sent successfully", "anomalies": anomalies}


# microphone sensor


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)


