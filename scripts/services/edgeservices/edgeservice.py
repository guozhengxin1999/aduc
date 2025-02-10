import base64
import json

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
import cv2
import numpy as np

app=FastAPI()

def detect_accident(frame):
    # randomized simulated accidents
    return np.ramdom.choice([True, False], p=[0.1, 0.9])

@app.post("/process_video")
async def process_video(request:Request):
    data = await  request.json()
    frame_data = data.get("frame")

    if frame_data is None:
        raise HTTPException(status_code=400, detail="No frame data provided")

    # decode image frames
    np_arr = np.frombuffer(base64.b64decode(frame_data), np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # detect accident
    is_accident = detect_accident(frame)

    # send result to cloud
    responses_data = {"is_accident", is_accident}
    response = json.dump(responses_data)

    return Response(content=response, media_type="application/json")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)