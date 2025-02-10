import uvicorn
from fastapi import FastAPI, Request, HTTPException, Response


app=FastAPI()

@app.post("/analyze_accident")
async def analyze_accident(request:Request):
    data = await request.json()

    # include accident results
    is_accident = data.get("is_accident", False)

    if is_accident:
        # emergency notice
        print("Emergency Notification: Accident Detection")

        # alert departments

    return Response(status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)