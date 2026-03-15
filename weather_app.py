# -*- coding: utf-8 -*-
"""
天气查询小程序
使用免费的 Open-Meteo API (无需API密钥)
功能：输入城市名查询实时天气，支持重复查询
"""

import urllib.request
import urllib.parse
import json
import time

# WMO天气代码映射表 (来自Open-Meteo文档)
WEATHER_CODES = {
    0: '晴',
    1: '晴间多云',
    2: '多云',
    3: '阴',
    45: '雾',
    48: '雾凇',
    51: '小雨',
    53: '中雨',
    55: '大雨',
    56: '冻雨',
    57: '冻雨',
    61: '小雨',
    63: '中雨',
    65: '大雨',
    66: '冻雨',
    67: '冻雨',
    71: '小雪',
    73: '中雪',
    75: '大雪',
    77: '雪粒',
    80: '阵雨',
    81: '阵雨',
    82: '暴雨',
    85: '阵雪',
    86: '暴雪',
    95: '雷阵雨',
    96: '雷阵雨带雹',
    99: '雷阵雨带雹'
}

def make_http_request(url, timeout=30, retries=2):
    """
    带重试机制的HTTP请求
    """
    last_error = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            last_error = e
            if attempt < retries:
                print(f"  重试中... ({attempt + 1}/{retries})")
                time.sleep(1)
    print(f"网络错误: {str(last_error)}")
    return None

def get_city_coordinates(city_name):
    """
    通过城市名获取经纬度
    使用 Open-Meteo Geocoding API
    """
    encoded_city = urllib.parse.quote(city_name)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=zh"
    
    data = make_http_request(url)
    if data and 'results' in data and len(data['results']) > 0:
        result = data['results'][0]
        return {
            'lat': result['latitude'],
            'lon': result['longitude'],
            'name': result.get('name', city_name),
            'country': result.get('country', '')
        }
    return None

def get_weather_data(lat, lon):
    """
    通过经纬度获取实时天气
    使用 Open-Meteo Weather API
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&language=zh"
    
    data = make_http_request(url)
    if data and 'current_weather' in data:
        return data['current_weather']
    return None

def format_weather_display(weather_data, city_info):
    """
    格式化天气显示
    """
    temp = weather_data.get('temperature', 'N/A')
    weather_code = weather_data.get('weathercode', -1)
    
    weather_desc = WEATHER_CODES.get(weather_code, '未知')
    
    print("\n" + "="*40)
    print(f"城市: {city_info['name']}")
    if city_info.get('country'):
        print(f"国家/地区: {city_info['country']}")
    print(f"温度: {temp}°C")
    print(f"天气状况: {weather_desc}")
    print("="*40 + "\n")

def check_requests_installed():
    """
    检查是否安装了requests库
    """
    try:
        import requests
        return True
    except ImportError:
        return False

def main():
    """
    主程序入口
    """
    print("="*40)
    print("       天气查询小程序")
    print("输入城市名查询天气，输入'q'或'quit'退出")
    print("="*40 + "\n")
    
    # 提示用户是否安装requests库
    if not check_requests_installed():
        print("提示: 推荐安装requests库以获得更好的网络体验")
        print("安装命令: pip install requests\n")
    
    while True:
        city = input("请输入城市名称: ").strip()
        
        if city.lower() in ['q', 'quit', '退出']:
            print("感谢使用，再见！")
            break
        
        if not city:
            print("错误: 城市名称不能为空！\n")
            continue
        
        print(f"正在查询 {city} 的天气信息...")
        
        # 获取城市坐标
        city_info = get_city_coordinates(city)
        
        if city_info is None:
            print(f"提示: 网络连接超时或找不到城市 '{city}'")
            print("建议: 检查网络连接或确认城市名称正确\n")
            continue
        
        # 获取天气数据
        weather_data = get_weather_data(city_info['lat'], city_info['lon'])
        
        if weather_data is None:
            print("错误: 获取天气信息失败，请稍后重试\n")
            continue
        
        # 显示结果
        format_weather_display(weather_data, city_info)

if __name__ == "__main__":
    main()
