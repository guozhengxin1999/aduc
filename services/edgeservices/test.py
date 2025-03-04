import requests
import pressure_pb2

# 创建 Protobuf 请求
input_data = pressure_pb2.Input()
pressureData = [120.5, 135.1999969482422, 110.80000305175781, 200.3000030517578, 150.6999969482422, 165.39999389648438, 180.10000610351562, 190.60000610351562, 210.89999389648438, 220.0, 230.5, 240.1999969482422, 250.8000030517578, 260.29998779296875, 270.1000061035156, 280.70001220703125, 290.3999938964844, 300.0, 95.5999984741211, 85.30000305175781]  # 文件编号
input_data.pressureData.extend(pressureData)
# 序列化 Protobuf 请求
serialized_data = input_data.SerializeToString()

print(serialized_data)

# 发送请求
url = "http://localhost:8000/detect"
headers = {"Content-Type": "application/x-protobuf"}
try:
    response = requests.post(url, headers=headers, data=serialized_data)
    response.raise_for_status()  # 检查 HTTP 状态码
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
    exit(1)

# 打印原始响应内容
print("Raw response content:", response.content)

# 解析响应
if response.headers["Content-Type"] == "application/x-protobuf":
    output = pressure_pb2.Output()
    try:
        output.ParseFromString(response.content)
        print("HasDetectedPressure:", output.hasDetectedPressure)
    except Exception as e:
        print("Failed to parse Protobuf response:", e)
else:
    try:
        print("JSON response:", response.json())
    except ValueError as e:
        print("Failed to parse JSON response:", e)
        print("Response content:", response.text)