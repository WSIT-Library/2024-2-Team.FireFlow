import requests
from datetime import datetime
import pytz

# ThingSpeak 설정
CHANNEL_ID = "2726166"
READ_API_KEY = "AU82REPOIW20JKPZ"
WRITE_API_KEY = "LGD2UEXJJWDQ751F"

LED_CHANNEL_ID = "2726168"
LED_WRITE_API_KEY = "GITGMUVXH6B46SD4"
LED_READ_API_KEY = "3CTBI0MAX1DWDU2I"

# US 시간 -> 한국 시간 변경
def convert_to_korean_time(time_str):
    # ISO 8601 형식의 문자열을 UTC 객체로 변환
    utc_time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    
    # 한국 시간대 객체 생성
    korean_timezone = pytz.timezone('Asia/Seoul')

    # ISO 문자열 UTC 객체로 바꾼 것을 한국 시간으로 변환
    korean_time = utc_time.astimezone(korean_timezone)

    # 한국 시간으로 변경한 것을 ISO 8601 형식 문자열로 다시 변환해서 반환
    return korean_time.isoformat()

# 하나의 데이터를 가져오는 함수
def get_sensor_data_one():
    url = f"https://api.thingspeak.com/channels/2726166/feeds.json"
    params = {
        "api_key": READ_API_KEY,
        "results": 1  # Retrieve only the latest data
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Check if feeds exist and return the latest values
            if data.get('feeds'):
                latest_feed = data['feeds'][0]
                field1 = float(latest_feed['field1']) if latest_feed['field1'] else None
                field2 = float(latest_feed['field2']) if latest_feed['field2'] else None
                return field1, field2
            else:
                print("No feeds available.")
    
    except Exception as e:
        print(f"Error getting sensor data: {e}")
    
    return 0, 0, 0  # Return None if there's an error or no data

# 최근 온도,습도 데이터 10개를 ThingSpeak로부터 가져오기
def get_sensor_data():
    url = f"https://api.thingspeak.com/channels/2726166/feeds.json"
    params = {
        "api_key": READ_API_KEY,
        "results": 10  # 최근 10개 데이터
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = []
            for feed in data['feeds']:
                time_str = convert_to_korean_time(feed['created_at'])
                results.append([
                    time_str,
                    float(feed['field1']) if feed['field1'] else None,
                    float(feed['field2']) if feed['field2'] else None ])
            print(results)
            return results
    except Exception as e:
        print(f"Error getting sensor data: {e}")
    return []



# 하나의 LED 데이터를 가져오는 함수
def get_led_data_one():
    url = f"https://api.thingspeak.com/channels/" + LED_CHANNEL_ID +"/feeds.json"
    params = {
        "api_key": LED_READ_API_KEY,
        "results": 1  # Retrieve only the latest data
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Check if feeds exist and return the latest values
            if data.get('feeds'):
                latest_feed = data['feeds'][0]
                field3 = float(latest_feed['field3']) if latest_feed['field3'] else 0
                return field3
            else:
                print("No feeds available.")
    
    except Exception as e:
        print(f"Error getting sensor data: {e}")
    
    return 0  # Return None if there's an error or no data


# LED 상태 변경하는 코드
def set_led_state(state):
    url = f"https://api.thingspeak.com/update"
    params = {
        "api_key": LED_WRITE_API_KEY,
        "field3": state
    }
    
    try:
        response = requests.get(url, params=params)
        print(response.content)
        return response.status_code == 200
    except Exception as e:
        print(f"Error setting LED state: {e}")
        return False
    

# ThingSpeak에서 CSV 파일을 다운로드하는 함수
def download_csv_from_thingspeak(output_csv="feeds.csv"):
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_csv, "wb") as file:
            file.write(response.content)
        print("CSV 파일 다운로드 완료.")
    else:
        print("데이터 다운로드 실패:", response.status_code)