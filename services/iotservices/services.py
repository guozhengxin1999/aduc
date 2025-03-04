import csv
import os

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
import json
from utils import parse_request, create_protobuf_response

app = FastAPI()

# ------------------------ 配置 -------------------------------
RESOURCES_DIR = os.path.join(os.path.dirname(__file__), ".", "resources")
PRESSURE_FILES = {
    1: os.path.join(RESOURCES_DIR, "pressure_data_1.csv"),
    2: os.path.join(RESOURCES_DIR, "pressure_data_2.csv"),
    3: os.path.join(RESOURCES_DIR, "pressure_data_3.csv"),
    4: os.path.join(RESOURCES_DIR, "pressure_data_4.csv"),
    5: os.path.join(RESOURCES_DIR, "pressure_data_5.csv"),
}

# ------------------------ 工具函数 -------------------------------
def get_pressure_data(file_path: str) -> float:
    """从 CSV 文件中读取所有行的压力数据"""
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        return [float(row[0]) for row in reader]

# ------------------------ 服务实现 -------------------------------
@app.post("/preprocess")
async def preprocess(request: Request):
    try:
        input_data = await parse_request(request)
        file_number = input_data.get("fileNumber")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")

    if file_number not in PRESSURE_FILES:
        raise HTTPException(status_code=400, detail=f"Invalid file number: {file_number}")

    # 读取压力数据
    file_path = PRESSURE_FILES[file_number]
    try:
        pressure_data = get_pressure_data(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read pressure data: {str(e)}")

    # 准备响应数据
    response_data = {"pressureData": pressure_data}
    if "application/x-protobuf" in request.headers.get("Content-Type", ""):
        response = create_protobuf_response(response_data)
        media_type = "application/x-protobuf"
    else:
        response = json.dumps(response_data)
        media_type = "application/json"

    return Response(content=response, media_type=media_type)

@app.post("/notify")
async def notify():
    # 发送通知逻辑
    print("Notification sent: Abnormal pressure detected!")
    return Response(status_code=200)

@app.post("/record")
async def record(request: Request):
    try:
        input_data = await parse_request(request)
        pressure_data = input_data.get("pressureData")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")

    # 记录逻辑
    with open("abnormal_records.txt", "a") as file:
        file.write(f"{pressure_data}\n")

    return Response(status_code=200)

# ------------------------ 启动服务 -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)