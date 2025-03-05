import csv
import os
import struct

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
import json
from google.protobuf.json_format import MessageToDict
#from utils import parse_request, create_protobuf_response
import ContextVariable_pb2
from typing import List

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

# ------------------------ 工具函数 -------------------------------
def get_pressure_data(file_path: str) -> float:
    """从 CSV 文件中读取所有行的压力数据"""
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        return [float(row[0]) for row in reader]

# ------------------------ 服务实现 -------------------------------
@app.post("/preprocess")
async def preprocess(request: Request):
    file_number =None

    if proto:
        # Read the raw request body
        body = await request.body()

        # Parse the protobuf message
        context_variables = ContextVariable_pb2.ContextVariables()
        context_variables.ParseFromString(body)

        # Extract specific values
        for context_variable in context_variables.data:
            context_variable_dict = MessageToDict(context_variable)

            # Check for cameraId and delay
            if context_variable_dict["name"] == "fileNumber":
                file_number= context_variable_dict["value"].get("integer")
    else:
        # Parse the request variables
        context_variables = await request.json()

        # Get context variables from the request json
        if "fileNumber" in context_variables:
            file_number = int(context_variables["fileNumber"])

    if file_number not in PRESSURE_FILES:
        raise HTTPException(status_code=400, detail=f"Invalid file number: {file_number}")

    # 读取压力数据
    file_path = PRESSURE_FILES[file_number]
    try:
        pressure_data = get_pressure_data(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read pressure data: {str(e)}")


    buffer_byte = b"".join(struct.pack("f", value) for value in pressure_data)
    # Prepare output data
    if proto:
        # Create response protobuf message
        response_context_variables = ContextVariable_pb2.ContextVariables()
        pressure_context_variable = ContextVariable_pb2.ContextVariable(
            name="pressureData",
            value=ContextVariable_pb2.Value(bytes=buffer_byte)  # 每个值单独赋值
         )
        response_context_variables.data.append(pressure_context_variable)

        # 序列化为 Protobuf 格式
        response = response_context_variables.SerializeToString()
        media_type = "application/x-protobuf"
    else:
        response = json.dumps({"pressureData": pressure_data})
        media_type = "application/json"


    # Return the protobuf response
    return Response(content=response, media_type=media_type)

@app.post("/notify")
async def notify():
    # 发送通知逻辑
    return Response(status_code=200)

@app.post("/record")
async def record():
    # 发送通知逻辑
    return Response(status_code=200)

    # pressure_data: List[float] = []
    #
    # if proto:
    #     # 读取原始请求体
    #     body = await request.body()
    #
    #     # 解析 Protobuf 消息
    #     context_variables = ContextVariable_pb2.ContextVariables()
    #     context_variables.ParseFromString(body)
    #
    #     # 提取 pressureData
    #     for context_variable in context_variables.data:
    #         context_variable_dict = MessageToDict(context_variable)
    #
    #         if context_variable_dict["name"] == "pressureData":
    #             # 提取列表类型的 pressureData
    #             pressure_data = context_variable_dict["value"].get("float", [])
    # else:
    #     # 解析 JSON 请求
    #     context_variables = await request.json()
    #
    #     # 获取 pressureData
    #     if "pressureData" in context_variables:
    #         pressure_data = context_variables["pressureData"]
    #
    # # 检查 pressureData 是否有效
    # if not pressure_data or not isinstance(pressure_data, list):
    #     raise HTTPException(
    #         status_code=400, detail="Invalid pressureData: No data provided or data is not a list"
    #     )
    #
    # # 在这里处理 pressureData，例如保存到数据库或文件
    # try:
    #     # 示例：将 pressureData 保存到文件
    #     with open("pressure_data_record.txt", "a") as f:
    #         f.write(f"{pressure_data}\n")
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500, detail=f"Failed to record pressure data: {str(e)}"
    #     )
    # try:
    #     input_data = await parse_request(request)
    #     pressure_data = input_data.get("pressureData")
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    #
    return Response(status_code=200)

# ------------------------ 启动服务 -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)