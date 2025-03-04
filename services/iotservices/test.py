import requests
import pressure_pb2

# 创建 Protobuf 请求
input_data = pressure_pb2.Input()
input_data.fileNumber = 1  # 文件编号

# 序列化 Protobuf 请求
serialized_data = input_data.SerializeToString()

# 发送请求
url = "http://localhost:8000/preprocess"
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
        print("Pressure data:", output.pressureData)
    except Exception as e:
        print("Failed to parse Protobuf response:", e)
else:
    try:
        print("JSON response:", response.json())
    except ValueError as e:
        print("Failed to parse JSON response:", e)
        print("Response content:", response.text)