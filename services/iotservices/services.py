import csv
import json
import os
import struct
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
from google.protobuf.json_format import MessageToDict
from typing import List, Dict, Any, Union

import ContextVariable_pb2

app = FastAPI()

# Decide whether protobuf should be used (optional environment variable)
proto = "PROTO" not in os.environ or os.environ["PROTO"].lower() in ["true", "t", "1"]

# ------------------------ 配置 -------------------------------
RESOURCES_DIR = os.path.join(os.path.dirname(__file__), ".", "resources")
PRESSURE_FILES = {
    1: os.path.join(RESOURCES_DIR, "pressure_data_1.csv"),
    2: os.path.join(RESOURCES_DIR, "pressure_data_2.csv"),
    3: os.path.join(RESOURCES_DIR, "pressure_data_3.csv"),
    4: os.path.join(RESOURCES_DIR, "pressure_data_4.csv"),
    5: os.path.join(RESOURCES_DIR, "pressure_data_5.csv"),
}

# ------------------------ 通用函数 -------------------------------
async def get_data(request: Request, key: str, data_type: str = "int") -> Union[int, float, str, List[float]]:
    """从请求中提取数据，支持多种数据类型"""
    if proto:
        body = await request.body()
        context_variables = ContextVariable_pb2.ContextVariables()
        context_variables.ParseFromString(body)
        for context_variable in context_variables.data:
            context_variable_dict = MessageToDict(context_variable)
            if context_variable_dict["name"] == key:
                if data_type == "int":
                    return context_variable_dict["value"].get("integer")
                elif data_type == "float":
                    return context_variable_dict["value"].get("float")
                elif data_type == "str":
                    return context_variable_dict["value"].get("string")
                elif data_type == "list":
                    return [struct.unpack("f", context_variable.value.bytes[i:i + 4])[0] for i in range(0, len(context_variable.value.bytes), 4)]
    else:
        context_variables = await request.json()
        if key in context_variables:
            return context_variables[key]
    raise HTTPException(status_code=400, detail=f"Invalid {key}: No data provided or data is not a {data_type}")

def read_csv_file(file_path: str, columns: List[str]) -> Dict[str, List[float]]:
    """读取 CSV 文件并提取指定列的数据"""
    data = {column: [] for column in columns}
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                for column in columns:
                    data[column].append(float(row[column]))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read CSV file: {str(e)}")
    return data

def create_response(response_data: Dict[str, Any]):
    """创建响应，支持 Protobuf 和 JSON 格式"""
    if proto:
        response_context_variables = ContextVariable_pb2.ContextVariables()
        for key, value in response_data.items():
            context_variable = ContextVariable_pb2.ContextVariable(name=key)
            if isinstance(value, bool):
                context_variable.value.bool = value
            elif isinstance(value, int):
                context_variable.value.int = value
            elif isinstance(value, float):
                context_variable.value.float = value
            elif isinstance(value, str):
                context_variable.value.string = value
            elif isinstance(value, list):
                context_variable.value.bytes = struct.pack(f"{len(value)}f", *value)
            response_context_variables.data.append(context_variable)
        response = response_context_variables.SerializeToString()
        media_type = "application/x-protobuf"
    else:
        response = json.dumps(response_data, indent=2)
        media_type = "application/json"
    return Response(content=response, media_type=media_type)

# ------------------------ 接口实现 -------------------------------
@app.post("/preprocessVideos")
async def preprocess_video(request: Request):
    file_number = await get_data(request, "fileNumber", "int")
    if file_number not in PRESSURE_FILES:
        raise HTTPException(status_code=400, detail=f"Invalid file number: {file_number}")

    file_path = PRESSURE_FILES[file_number]
    data = read_csv_file(file_path, ["airbag(kPa)"])
    return create_response({"videoData": data["airbag(kPa)"]})

@app.post("/processAudio")
async def process_audio(request: Request):
    file_number = await get_data(request, "fileNumber", "int")
    if file_number not in PRESSURE_FILES:
        raise HTTPException(status_code=400, detail=f"Invalid file number: {file_number}")

    file_path = PRESSURE_FILES[file_number]
    data = read_csv_file(file_path, ["airbag(kPa)"])
    return create_response({"audioData": data["airbag(kPa)"]})

@app.post("/preprocess")
async def preprocess(request: Request):
    file_number = await get_data(request, "fileNumber", "int")
    if file_number not in PRESSURE_FILES:
        raise HTTPException(status_code=400, detail=f"Invalid file number: {file_number}")

    file_path = PRESSURE_FILES[file_number]
    data = read_csv_file(file_path, ["airbag(kPa)", "door(ΔkPa)", "seat(N)"])
    return create_response({
        "airBagData": data["airbag(kPa)"],
        "doorData": data["door(ΔkPa)"],
        "seatData": data["seat(N)"]
    })

@app.post("/airbagCheck")
async def airbag_check():
    return Response(status_code=200)

@app.post("/doorCheck")
async def door_check():
    return Response(status_code=200)

@app.post("/seatCheck")
async def seat_check():
    return Response(status_code=200)


# -----unlock the door -----
@app.post("/unlockDoors")
async def unlock_doors():
    return Response(status_code=200)

# ----- disconnect fuel and battery -----
@app.post("/disconnectPower")
async def disconnect_power():
    return Response(status_code=200)

# ----- guidance rescue -----
@app.post("/guidanceRescue")
async def guidance_rescue():
    return Response(status_code=200)


# ------------------------ 启动服务 -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)