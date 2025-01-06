import os
from apscheduler.schedulers.background import BackgroundScheduler
import sensor_utils
import database_connect
import ThingSpeak_connect

# deamon = True 속성을 주어 메인 프로세스가 종료되면 같이 종료되도록 함으로써
# background에서 계속 돌아가는걸 방지하도록 하자
sched = BackgroundScheduler(daemon=True)

@sched.scheduled_job('cron', hour='0',minute='0',id='daily_job')
def save_db_fromdata():

    # 1. thingspeak에서 csv 파일을 저장
    get_all_thingspeak_data()

    # 1. 하루종일 모인 txt 내에 있는 온도/습도 데이터를 바탕으로
    # 온도 평균하고 습도 평균을 구하고 반환
    temp_avg, humi_avg = sensor_utils.calculate_averages(sensor_utils.load_sensor_data())
    
    # 2. db에 connect하는 py 파일을 통해 db에 연결뒤 온도하고 습도 평균 데이터 저장
    database_connect.save_sensordata_db(temp_avg, humi_avg)

    print("DB 저장 프로세스 완료")

# csv 파일을 가져와서 txt파일로 파싱 및 저장
def get_all_thingspeak_data():

    # 현재 실행하는 py 파일과 같은 폴더 경로를 기반으로 파일 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_filename = os.path.join(current_dir, 'feeds.csv')
     
    ThingSpeak_connect.download_csv_from_thingspeak(csv_filename)
    sensor_utils.convert_csv_to_txt(csv_filename)
    # sensor_utils.today_convert_csv_to_txt(csv_filename)
    print("하루 전 데이터 변환 작업 완료.")

sched.start()