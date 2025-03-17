import struct
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
import json
import ContextVariable_pb2
import os
from typing import List, Union, Dict, Any

app = FastAPI()

# Decide whether protobuf should be used (optional environment variable)
proto = "PROTO" not in os.environ or os.environ["PROTO"].lower() in ["true", "t", "1"]

def create_protobuf_response(response_data: Dict[str, Any]):
    """创建 Protobuf 格式的响应，支持多种数据类型"""
    response_context_variables = ContextVariable_pb2.ContextVariables()
    for key, value in response_data.items():
        context_variable = ContextVariable_pb2.ContextVariable(name=key)
        if isinstance(value, bool):
            context_variable.value.bool = value
        elif isinstance(value, int):
            context_variable.value.integer = value
        elif isinstance(value, float):
            context_variable.value.float = value
        elif isinstance(value, str):
            context_variable.value.string = value
        elif isinstance(value, list):
            # 假设列表是浮点数列表
            context_variable.value.bytes = struct.pack(f"{len(value)}f", *value)
        elif isinstance(value, bytes):
            # 处理二进制数据（如图像或音频）
            context_variable.value.bytes = value
        response_context_variables.data.append(context_variable)
    return response_context_variables.SerializeToString()

async def extract_data(request: Request, data_key: str, data_type: str = "list") -> Union[List[float], int, bool, str, bytes]:
    """从请求中提取数据，支持多种数据类型"""
    if proto:
        body = await request.body()
        context_variables = ContextVariable_pb2.ContextVariables()
        context_variables.ParseFromString(body)
        for context_variable in context_variables.data:
            if context_variable.name == data_key:
                if data_type == "list":
                    return [struct.unpack("f", context_variable.value.bytes[i:i + 4])[0] for i in range(0, len(context_variable.value.bytes), 4)]
                elif data_type == "int":
                    return context_variable.value.int
                elif data_type == "bool":
                    return context_variable.value.bool
                elif data_type == "str":
                    return context_variable.value.string
                elif data_type == "bytes":
                    return context_variable.value.bytes  # 处理二进制数据
    else:
        context_variables = await request.json()
        if data_key in context_variables:
            if data_type == "bytes" and isinstance(context_variables[data_key], str):
                # 如果 JSON 中的二进制数据是 base64 编码的字符串
                import base64
                return base64.b64decode(context_variables[data_key])
            return context_variables[data_key]
    raise HTTPException(status_code=400, detail=f"Invalid {data_key}: No data provided or data is not a {data_type}")

async def create_response(response_data: Dict[str, Any]):
    """创建响应，支持 Protobuf 和 JSON 格式"""
    if proto:
        response = create_protobuf_response(response_data)
        media_type = "application/x-protobuf"
    else:
        response = json.dumps(response_data)
        media_type = "application/json"
    return Response(content=response, media_type=media_type)

# ----- detect angle using video -----
@app.post("/videoDetectAngle")
async def video_detect_angle(request: Request):
    video_data = await extract_data(request, "videoData", "list")
    video_angle = True  # 假设检测逻辑
    return await create_response({"videoAngle": video_angle})

# ----- detect smoke using video -----
@app.post("/videoDetectSmoke")
async def video_detect_smoke(request: Request):
    video_data = await extract_data(request, "videoData", "list")
    video_smoke = True  # 假设检测逻辑
    return await create_response({"videoSmoke": video_smoke})

# ----- detect collision using video -----
@app.post("/videoDetectCollision")
async def video_detect_collision(request: Request):
    video_data = await extract_data(request, "videoData", "list")
    video_collision = True  # 假设检测逻辑
    return await create_response({"videoCollision": video_collision})

# ----- detect passenger using video -----
@app.post("/videoDetectPassenger")
async def video_detect_passenger(request: Request):
    video_data = await extract_data(request, "videoData", "list")
    video_passenger = True  # 假设检测逻辑
    return await create_response({"videoPassenger": video_passenger})

# ----- detect collision using audio -----
@app.post("/audioDetectCollision")
async def audio_detect_collision(request: Request):
    audio_data = await extract_data(request, "audioData", "list")
    audio_collision = True  # 假设检测逻辑
    return await create_response({"audioCollision": audio_collision})

# ----- detect passenger using audio -----
@app.post("/audioDetectPassenger")
async def audio_detect_passenger(request: Request):
    audio_data = await extract_data(request, "audioData", "list")
    audio_passenger = True  # 假设检测逻辑
    return await create_response({"audioPassenger": audio_passenger})

# ----- process image data -----
@app.post("/processImage")
async def process_image(request: Request):
    image_data = await extract_data(request, "imageData", "bytes")
    # 假设对图像数据进行处理
    image_processed = True  # 假设处理逻辑
    return await create_response({"imageProcessed": image_processed})

# ----- process audio data -----
@app.post("/processAudio")
async def process_audio(request: Request):
    audio_data = await extract_data(request, "audioData", "bytes")
    # 假设对音频数据进行处理
    audio_processed = True  # 假设处理逻辑
    return await create_response({"audioProcessed": audio_processed})

# ------------------------ 启动服务 -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)