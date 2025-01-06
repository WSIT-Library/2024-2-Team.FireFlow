import os
from datetime import datetime,timedelta
import csv
import pytz

# 현재 실행하는 py 파일과 같은 폴더 경로를 기반으로 파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, 'sensor_data.txt')

# 온도와 습도 데이터를 txt 파일에 저장하는 함수
def save_sensor_data(temperature, humidity):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(filename, 'a') as file:
        file.write(f"{timestamp},{temperature},{humidity}\n")

# txt 파일에서 데이터를 불러와 리스트로 반환하는 함수
def load_sensor_data():
    data = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                timestamp, temperature, humidity = line.strip().split(',')
                data.append((timestamp, float(temperature), float(humidity)))
        return data
    except FileNotFoundError:
        return []

# 리스트를 받아 온도와 습도의 평균을 계산하여 반환하는 함수
def calculate_averages(data):
    if not data:
        return None, None
    temp_sum = sum(entry[1] for entry in data)
    humid_sum = sum(entry[2] for entry in data)
    count = len(data)
    return temp_sum / count, humid_sum / count

# txt 파일 내용을 전부 삭제하는 함수
def clear_sensor_data():
    with open(filename, 'w') as file:
        # 빈 내용으로 파일을 열어 모든 내용을 삭제합니다
        file.write('')

# CSV 파일을 TXT로 변환
def today_convert_csv_to_txt(input_csv, output_txt=filename):
    # UTC와 KST 시간대 설정
    utc_tz = pytz.UTC  # UTC ISO 
    kst_tz = pytz.timezone('Asia/Seoul')
    
    # 현재 시간을 KST 기준으로 설정하여 오늘 날짜 계산
    today_kst = datetime.now(kst_tz)
    today_date = today_kst.strftime("%Y-%m-%d")  # 오늘 날짜 (형식: 'YYYY-MM-DD')
    
    with open(input_csv, "r") as csv_file, open(output_txt, "w") as txt_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # 헤더 무시
        
        for row in csv_reader:
            try:
                date_time, field1, field2 = row[0], row[2], row[3]
                
                # UTC 시간을 datetime 객체로 변환 (새로운 형식 처리)
                # '2024-11-04 09:17:34 UTC' 형식 처리
                utc_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S UTC")
                utc_time = utc_tz.localize(utc_time)
                
                # UTC를 KST로 변환
                kst_time = utc_time.astimezone(kst_tz)
                
                # 오늘 날짜의 데이터만 필터링
                if kst_time.strftime("%Y-%m-%d") == today_date:
                    temperature = float(field1)
                    humidity = float(field2)
                    
                    # 온도와 습도 값이 유효할 때만 텍스트 파일에 기록
                    if 0 <= temperature <= 100 and 0 <= humidity <= 100:
                        txt_file.write(f"{kst_time.strftime('%Y-%m-%d %H:%M:%S')},{temperature},{humidity}\n")
            
            except (ValueError, IndexError) as e:
                print(f"Error processing row: {e}")
                continue  # 데이터에 오류가 있을 경우 건너뛰기

# CSV 파일을 TXT로 변환
def convert_csv_to_txt(input_csv, output_txt=filename):
    # UTC와 KST 시간대 설정
    utc_tz = pytz.UTC  # UTC ISO 
    kst_tz = pytz.timezone('Asia/Seoul')
    
    # 현재 시간을 KST 기준으로 설정하여 어제 날짜 계산
    today_kst = datetime.now(kst_tz)
    yesterday = today_kst - timedelta(days=1)
    yesterday_date = yesterday.strftime("%Y-%m-%d")  # 하루 전 날짜 (형식: 'YYYY-MM-DD')
    
    with open(input_csv, "r") as csv_file, open(output_txt, "w") as txt_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # 헤더 무시
        
        for row in csv_reader:
            try:
                date_time, field1, field2 = row[0], row[2], row[3]
                
                # UTC 시간을 datetime 객체로 변환 (새로운 형식 처리)
                # '2024-11-04 09:17:34 UTC' 형식 처리
                utc_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S UTC")
                utc_time = utc_tz.localize(utc_time)
                
                # UTC를 KST로 변환
                kst_time = utc_time.astimezone(kst_tz)
                
                # 어제 날짜의 데이터만 필터링 int(string) float(string)
                if kst_time.strftime("%Y-%m-%d") == yesterday_date:
                    temperature = float(field1)
                    humidity = float(field2)
                    
                    # 온도와 습도 값이 유효할 때만 텍스트 파일에 기록 printf
                    if 0 <= temperature <= 100 and 0 <= humidity <= 100:
                        txt_file.write(f"{kst_time.strftime('%Y-%m-%d %H:%M:%S')},{temperature},{humidity}\n")
            
            except (ValueError, IndexError) as e:
                print(f"Error processing row: {e}")
                continue  # 데이터에 오류가 있을 경우 건너뛰기