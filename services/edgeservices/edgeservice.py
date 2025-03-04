import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
import json
from utils import parse_request, create_protobuf_response

app = FastAPI()

# ------------------------ 服务实现 -------------------------------
@app.post("/detect")
async def detect(request: Request):
    try:
        input_data = await parse_request(request)
        pressure_data = input_data.get("pressureData")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")

    # 检测逻辑
    is_abnormal = any(pressure > 150 for pressure in pressure_data)  # 压力 > 150 为异常

    # 准备响应数据
    response_data = {"hasDetectedPressure": is_abnormal}
    if "application/x-protobuf" in request.headers.get("Content-Type", ""):
        response = create_protobuf_response(response_data)
        media_type = "application/x-protobuf"
    else:
        response = json.dumps(response_data)
        media_type = "application/json"

    return Response(content=response, media_type=media_type)

# ------------------------ 启动服务 -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)