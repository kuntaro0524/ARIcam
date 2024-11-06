import zmq
import neoapi
import cv2 as cv
import numpy as np
import threading

# ZMQのセットアップ
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:5555")

# カメラの初期化
fps_forCamera = 24
reshape = 1.0
camera = neoapi.Cam()
camera.Connect('ARI-Camera')
camera.f.PixelFormat.SetString('RGB8')
camera.f.AcquisitionFrameRateEnable.value = True
camera.f.AcquisitionFrameRate.value = fps_forCamera
camera.f.ExposureAuto.SetString("Continuous")
camera.f.BrightnessAutoPriority.value=0
#camera.f.ExposureTime.Set(15000)
camera.f.GainAuto.SetString("Off")
camera.f.GainSelector.SetString("All")
camera.f.Gain.value = 1.0

# 撮像フレームを表示するスレッド
def display_camera_feed():
    while True:
        frame = camera.GetImage().GetNPArray()
        frame = cv.resize(frame, (0, 0), fx=reshape, fy=reshape, interpolation=cv.INTER_LINEAR)
        cv.imshow("Live Camera Feed", frame)
        if cv.waitKey(1) & 0xFF == 27:  # 'ESC' キーで終了
            break
    cv.destroyAllWindows()

# コマンドを待ち受け、画像を保存するスレッド
def listen_for_commands():
    while True:
        message = socket.recv_json()  # クライアントからのJSONメッセージを受信
        filename = message.get("filename", "captured_image.png")
        
        # 撮像中のフレームを取得し保存
        frame = camera.GetImage().GetNPArray()
        frame = cv.resize(frame, (0, 0), fx=reshape, fy=reshape, interpolation=cv.INTER_LINEAR)
        cv.imwrite(filename, frame)
        socket.send_json({"message": f"Image saved as {filename}"})

# スレッドを開始
display_thread = threading.Thread(target=display_camera_feed)
command_thread = threading.Thread(target=listen_for_commands)

display_thread.start()
command_thread.start()

display_thread.join()
command_thread.join()

