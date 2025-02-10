## video and microphone sensor sm, 1. data source, 2. handle images and audios
# iot device : pressure sensor sm, seat sensor sm
# edge device : detect
# cloud device :
import base64
import json
import cv2
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
import numpy as np


app = FastAPI()

## video sensor
# sensor captures frame
def capture_frame():
    # video stream cature frame.
    frame = np.ramdom.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    return frame

@app.post("/capture_video")
async def capture_video(request: Request):
    frame = capture_frame()

    #Encoding image frame as base64
    _, buffer = cv2.imencode('.jpg', frame)
    frame_data = base64.b64decode(buffer).decode('utf-8')

    response_data = {"frame": frame_data}
    response = json.dump(response_data)

    return Response(content=response, media_type="application/json")


# sensor pressure

# sensor seat

# microphone sensor


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)


