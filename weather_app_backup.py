# -*- coding: utf-8 -*-
"""
天气查询小程序 (双API版本)
使用 Open-Meteo 和 wttr.in 双API备份
无需API密钥，支持重复查询
"""

import urllib.request
import urllib.parse
import json
import time

WEATHER_CODES = {
    0: '晴', 1: '晴间多云', 2: '多云', 3: '阴',
    45: '雾', 48: '雾凇',
    51: '小雨', 53: '中雨', 55: '大雨',
    56: '冻雨', 57: '冻雨',
    61: '小雨', 63: '中雨', 65: '大雨',
    66: '冻雨', 67: '冻雨',
    71: '小雪', 73: '中雪', 75: '大雪', 77: '雪粒',
    80: '阵雨', 81: '阵雨', 82: '暴雨',
    85: '阵雪', 86: '暴雪',
    95: '雷阵雨', 96: '雷阵雨带雹', 99: '雷阵雨带雹'
}

def make_http_request(url, timeout=30, retries=2):
    """带重试机制的HTTP请求"""
    last_error = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'curl/7.68.0'}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except Exception as e:
            last_error = e
            if attempt < retries:
                print(f"  重试中... ({attempt + 1}/{retries})")
                time.sleep(1)
    print(f"网络错误: {str(last_error)}")
    return None

def get_weather_wttr(city_name):
    """使用 wttr.in API 获取天气"""
    try:
        encoded_city = urllib.parse.quote(city_name)
        url = f"https://wttr.in/{encoded_city}?format=j1"
        data = make_http_request(url)
        if data:
            result = json.loads(data.decode('utf-8'))
            current = result.get('current_condition', [{}])[0]
            temp = current.get('temp_C', 'N/A')
            desc = current.get('lang_zh', [{}])[0].get('value', current.get('weatherDesc', [{}])[0].get('value', '未知'))
            return {'temp': temp, 'desc': desc, 'city': city_name, 'success': True}
    except Exception as e:
        print(f"wttr.in API错误: {e}")
    return {'success': False}

def get_weather_openmeteo(city_name):
    """使用 Open-Meteo API 获取天气"""
    encoded_city = urllib.parse.quote(city_name)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=zh"
    data = make_http_request(url)
    if not data:
        return {'success': False}
    
    geo_data = json.loads(data.decode('utf-8'))
    if not geo_data.get('results'):
        return {'success': False, 'error': 'city_not_found'}
    
    result = geo_data['results'][0]
    lat, lon = result['latitude'], result['longitude']
    city = result.get('name', city_name)
    
    url2 = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data2 = make_http_request(url2)
    if not data2:
        return {'success': False}
    
    weather_data = json.loads(data2.decode('utf-8'))
    current = weather_data.get('current_weather', {})
    temp = current.get('temperature', 'N/A')
    code = current.get('weathercode', -1)
    desc = WEATHER_CODES.get(code, '未知')
    
    return {'temp': temp, 'desc': desc, 'city': city, 'success': True}

def get_weather(city_name):
    """双API调用，自动切换"""
    print(f"正在查询 {city_name} 的天气信息...")
    
    result = get_weather_openmeteo(city_name)
    if result.get('success'):
        return result
    
    if result.get('error') == 'city_not_found':
        print(f"错误: 找不到城市 '{city_name}'")
        return None
    
    print("主API失败，尝试备用API...")
    result2 = get_weather_wttr(city_name)
    if result2.get('success'):
        return result2
    
    return None

def main():
    print("="*40)
    print("       天气查询小程序")
    print("输入城市名查询，输入'q'或'退出'退出")
    print("="*40 + "\n")
    
    while True:
        city = input("请输入城市名称: ").strip()
        if city.lower() in ['q', 'quit', '退出']:
            print("感谢使用，再见！")
            break
        if not city:
            print("错误: 城市名称不能为空！\n")
            continue
        
        result = get_weather(city)
        if result:
            print("\n" + "="*40)
            print(f"城市: {result['city']}")
            print(f"温度: {result['temp']}°C")
            print(f"天气: {result['desc']}")
            print("="*40 + "\n")
        else:
            print("查询失败，请检查网络或稍后重试\n")

if __name__ == "__main__":
    main()
