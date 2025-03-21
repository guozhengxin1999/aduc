import struct

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
import json
import random
#from utils import parse_request, create_protobuf_response
import ContextVariable_pb2
import os
from typing import List

app = FastAPI()
#
# Decide whether protobuf should be used (optional environment variable)
proto = "PROTO" not in os.environ or os.environ["PROTO"].lower() in ["true", "t", "1"]

def create_protobuf_response(response_data: dict):
    """创建 Protobuf 格式的响应"""
    response_context_variables = ContextVariable_pb2.ContextVariables()
    for key, value in response_data.items():
        context_variable = ContextVariable_pb2.ContextVariable(
            name=key,
            value=ContextVariable_pb2.Value(bool=value)  # 假设返回的是布尔值
        )
        response_context_variables.data.append(context_variable)
    return response_context_variables.SerializeToString()

@app.post("/analysis")
async def analysis(request: Request):
    # 发送通知逻辑
    pressure_data: List[float] = []

    # 尝试读取 pressureData
    if proto:
        # 读取原始请求体
        body = await request.body()

        # 解析 Protobuf 消息
        context_variables = ContextVariable_pb2.ContextVariables()
        context_variables.ParseFromString(body)

        pressure_bytes = None
        # 提取 pressureData
        for context_variable in context_variables.data:
            if context_variable.name == "pressureData":
                pressure_bytes = context_variable.value.bytes
                pressure_data = [struct.unpack("f", pressure_bytes[i:i + 4])[0] for i in
                                 range(0, len(pressure_bytes), 4)]
                break
    else:
        # 解析 JSON 请求
        context_variables = await request.json()

        # 获取 pressureData
        if "pressureData" in context_variables:
            pressure_data = context_variables["pressureData"]

    # 检查 pressureData 是否有效
    if not pressure_data or not isinstance(pressure_data, list):
        raise HTTPException(
            status_code=400, detail="Invalid pressureData: No data provided or data is not a list"
        )

    # 深度分析逻辑
    has_threat = 1  # 100% 的概率返回 True

    # 准备响应数据
    response_data = {"hasThreat": has_threat}
    if proto:
        # 创建 Protobuf 格式的响应
        response = create_protobuf_response(response_data)
        media_type = "application/x-protobuf"
    else:
        # 创建 JSON 格式的响应
        response = json.dumps(response_data)
        media_type = "application/json"

    # 返回响应
    return Response(content=response, media_type=media_type)

# # ------------------------ 启动服务 -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8003)