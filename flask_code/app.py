# 로고 이미지 301*52 사이즈로 바꾸기
from flask import Flask, request, render_template, jsonify, Response
import os
import sensor_utils
import database_connect
import ThingSpeak_connect
import ex
import esp32cam_detect

# 현재 모듈(파일)의 이름을 가져와 애플리케이션의 루트 경로를 알수있도록 한다
app = Flask(__name__)


# 현재 LED 상태를 저장할 변수 (0 = OFF, 1 = ON)
led_status = 0

@app.route('/') # 경로 지정
def hello():
    return render_template("index.html") 

@app.route('/grap')
def grap():
    # 웹 그래프에 나타낼 최근 10개의 데이터를 가져오기
    temp_chart_Data = ThingSpeak_connect.get_sensor_data()
    
    # 웹에 나타낼 최근 1개의 데이터를 가져오기
    temp,humi = ThingSpeak_connect.get_sensor_data_one()
    
    return render_template("grap.html", chartData=temp_chart_Data, oneTempData=temp, oneHumiData=humi)

@app.route('/camera')
def camera():
    # 웹에 나타낼 최근 1개의 데이터를 가져오기
    temp,humi = ThingSpeak_connect.get_sensor_data_one()
    
    # 웹에 나타낼 최근 1개의 데이터를 가져오기
    led = ThingSpeak_connect.get_led_data_one()
    
    return render_template("camera.html", oneTempData=temp, oneHumiData=humi, ledData=led)

# 비디오 스트림 라우트 (실시간 객체 탐지 결과를 웹 페이지로 스트리밍)
@app.route('/video_feed')
def video_feed():
    # Flask에서 HTTP 응답을 생성
    # (box와 레이블이 그려진 프레임 데이터, 데이터 형식, 구분자)
    # generate에서 yield 할때 보내는 content-type이나 구분자도 이 두번째 인자와 세번째 인자에 맞추어야 한다.
    return Response(esp32cam_detect.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update_led_status', methods=['POST'])
def getButtonState():
    global led_status
    data = request.get_json()
    new_status = data.get('status')

    # 새로운 상태에 따라 LED 제어
    if new_status == 1:
        ThingSpeak_connect.set_led_state(new_status)
        led_status = 1  # LED를 켭니다.
    else:
        ThingSpeak_connect.set_led_state(new_status)
        led_status = 0  # LED를 끕니다.

    # 현재 LED 상태를 클라이언트에 반환
    return jsonify({'status': led_status})

def main():
    # ip주소, debug, port 번호 실행
    app.run(host='0.0.0.0', debug=True, port=443)

if __name__ == '__main__':
    main()