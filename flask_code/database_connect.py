import cx_Oracle  

def save_sensordata_db(temp_avg, humid_avg):
    try:
        
        # 오라클 연결
        conn = cx_Oracle.connect('MYSTUDY', 'MYSTUDY', '127.0.0.1:1521/xe')
        cursor = conn.cursor() # connection으로부터 cursor 생성 (데이터베이스의 Fetch 관리)
      
        
        # DB에 삽입할 '파일명'과 '파일경로'를 저장
        # image_name = date_time + file_name # 현재시각 + 파일명 : 겹치는 파일명이 없도록 만들어주는 역할
        
        # DB에 삽입
        sql = f"INSERT INTO SENSOR_DATA(id, temperature, humidity) VALUES((SELECT NVL(MAX(id) + 1, 1) FROM SENSOR_DATA),'{temp_avg}', '{humid_avg}')" 
        cursor.execute(sql)
        conn.commit() # DB에 SQL문 저장(반드시 저장해야 사용가능)
      
    except Exception as e : # 오류 발생 시 처리 방법
        print('db error :', e)
        conn.rollback() # 오류 발생 시 이전 상태 리턴     
    finally : # 마지막
        cursor.close(); conn.close()  # 열린 DB를 닫음(반드시 닫아줘야 작동한다)
