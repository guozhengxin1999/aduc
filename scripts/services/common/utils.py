from fastapi import Request
from google.protobuf.json_format import MessageToDict
import pressure_pb2
import json


async def parse_request(request: Request):
    """解析请求数据，支持 JSON 和 Protobuf 格式"""
    content_type = request.headers.get("Content-Type", "")
    if "application/x-protobuf" in content_type:
        body = await request.body()
        input_data = pressure_pb2.Input()
        input_data.ParseFromString(body)

        # 提取 Protobuf 消息中的字段
        result = {}
        if input_data.HasField("fileNumber"):
            result["fileNumber"] = input_data.fileNumber
        if input_data.pressureData:
            result["pressureData"] = list(input_data.pressureData)
        return result

    else:
        return await request.json()


def create_protobuf_response(data: dict):
    """创建 Protobuf 格式的响应"""
    output = pressure_pb2.Output()
    if "pressureData" in data:
        output.pressureData.extend(data["pressureData"])  # 使用 extend 添加多个值
    elif "hasDetectedPressure" in data:
        output.hasDetectedPressure = data["hasDetectedPressure"]
    else:
        raise ValueError("Invalid output data")
    return output.SerializeToString()