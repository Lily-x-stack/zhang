import urllib.request
import urllib.parse
import json

print("测试 Open-Meteo API 连接...")

try:
    test_url = "https://geocoding-api.open-meteo.com/v1/search?name=Beijing&count=1&language=zh"
    with urllib.request.urlopen(test_url, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
    print(f"地理编码API测试成功! 北京坐标: {data['results'][0]['latitude']}, {data['results'][0]['longitude']}")
except Exception as e:
    print(f"地理编码API测试失败: {e}")

try:
    test_url2 = "https://api.open-meteo.com/v1/forecast?latitude=39.90&longitude=116.39&current_weather=true"
    with urllib.request.urlopen(test_url2, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
    temp = data['current_weather']['temperature']
    print(f"天气API测试成功! 北京当前温度: {temp}°C")
except Exception as e:
    print(f"天气API测试失败: {e}")

print("\nAPI测试完成!")
