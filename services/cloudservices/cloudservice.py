import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response
import json
import random
from utils import parse_request, create_protobuf_response

app = FastAPI()

@app.post("/analysis")
async def analysis(request: Request):
    try:
        input_data = await parse_request(request)
        pressure_data = input_data.get("pressureData")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")

    # 深度分析逻辑
    has_threat = 1  # 100% 的概率返回 True

    # 准备响应数据
    response_data = {"hasThreat": has_threat}
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