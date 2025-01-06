import cv2
import torch
import pathlib
import platform

# YOLOv5 모델 로드 (GPU가 있으면 GPU 사용, 없으면 CPU 사용)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 모델 로드 ---> 경로를 윈도우에 맞도록 하는 코드 
# (pathlib 사용. 코드 도움: https://stackoverflow.com/questions/76994593/i-cant-load-my-yolov5-model-in-streamlit-this-is-the-error)
if platform.system() == 'Windows':
    pathlib.PosixPath = pathlib.WindowsPath
else:
    pathlib.WindowsPath = pathlib.PosixPath


# pathlib 라이브러리를 사용하여 YOLOv5 모델 파일의 경로를 동적으로 생성

# pathlib.Path(__file__): 현재 실행 중인 Python 파일의 경로를 나타내는 Path 객체 생성
# __file__: 실행 중인 파일의 위치를 나타내는 특별 변수
#.parent: 해당 파일이 속한 디렉토리의 경로를 반환. 예를 들어, 파일이 /project/app/main.py에 있다면 .parent는 /project/app 이다.
current_dir = pathlib.Path(__file__).parent.resolve() # .resolve(): 경로를 절대 경로로 변환

# pathlib 객체의 / 연산자를 이용하여 파일 경로를 보다 쉽게 결합. / 연산자를 사용하여 문자열 결합이 아닌 경로 결합을 하여
# 새로운 path 객체 생성 
model_path = current_dir / "mymodel" / "best.pt"

# Path 객체를 문자열로 (현재 model_path는 path 객체이다.)
model_path = str(model_path)

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path).to(device)



# 한글 클래스 이름 사전 생성
korean_names =  {0: '수확 불가능한 상추', 1: '수확 가능한 상추'}

# model.names를 직접 리스트로 대체 (원본데이터: {0: 'Lettuce-Not-Ready-to-Harvest', 1: 'Lettuce-Ready-to-Harvest'} )
model.names = korean_names

# ESP32-CAM 스트리밍 URL (실제 URL로 수정)
# ESP32-CAM에서 전송하는 MJPEG 비디오 스트림의 url
stream_url = "http://192.168.86.149:81/stream"



# 비디오 스트림 프레임 생성 (Flask에 전달할 이미지 포맷으로 변환)
# yield를 이용하여 비디오 데이터를 순차적으로 클라이언트에 전송
def generate():
    

    # 이 URL에서 비디오 스트림을 읽을 수 있도록 설정
    # 스트리밍되고있는 비디오의 프레임을 가져온다
    cap = cv2.VideoCapture(stream_url)
    
    # 아까 가져온 cap에서 지속적으로 프레임을 읽어온다
    # 매번 프레임을 받아와서 객체탐지를 하고 그 결과를 클라이언트에 전달
    while True:
        # 스트리밍된 비디오에서 한 프레임을 읽어온다
        # ret: 읽은 프레임이 정상적인지의 여부
        ret, frame = cap.read()
        if not ret: # ret이 false면 스트림의 끝
            break # 영상이 끝났으면 break
        
        # YOLO 모델을 사용하여 객체 탐지
        # BGR -> RGB 변환 (opencvㄴ는 bgr 형식, yolov5는 rgb 형식 사용)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  

        # 변환된 rgb 프레임을 파라미터로 해서 객체 탐지
        results = model(frame_rgb)
        
        # render 함수를 통해 탐지된 객체들을 이미지 위에 그리기
        # [0] 는 첫번쨰, 유일한 이미지를 가져옴
        # annotated_frame: 탐지된 객체들의 바운딩 박스와 레이블이 그려진 이미지
        annotated_frame = results.render()[0]

        # render()는 RGB 형식으로 이미지를 반환하므로 다시 BGR로 변환
        # 클라이언트가 정상적으로 이미지를 볼수있도록 하는 코드
        annotated_frame_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)  # RGB -> BGR 변환
        # 이미지를 JPEG 형식으로 인코딩
        # _는 이미지 크기(but 여기서는 안쓰임)
        _, jpeg = cv2.imencode('.jpg', annotated_frame_bgr)

        # 전송될 이미지를 byte stream으로 변환하여 저장
        frame_response = jpeg.tobytes()
        
        # 한 프레임을 순차적으로 클라이언트에 전송
        # --frame 는 각 프레임을 구분하는 구분자
        # content-type부터는 header, freame_response는 body
        # \r\n\r\n 는 header와 본문 분리
        # b는 byte 형태로 한다는 뜻
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_response + b'\r\n\r\n')