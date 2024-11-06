from flask import Flask, request, jsonify
import neoapi
import cv2 as cv
import numpy as np

app = Flask(__name__)

# カメラの初期化
fps_forCamera = 24
reshape = 1.0
camera = neoapi.Cam()
camera.Connect('ARI-Camera')
camera.f.PixelFormat.SetString('RGB8')
camera.f.AcquisitionFrameRateEnable.value = True
camera.f.AcquisitionFrameRate.value = fps_forCamera
camera.f.ExposureAuto.SetString("Off")
camera.f.ExposureTime.Set(15000)
camera.f.GainAuto.SetString("Off")
camera.f.GainSelector.SetString("All")
camera.f.Gain.value = 1.0

# カメラの画像を保存

@app.route('/capture', methods=['POST'])
def capture_image():
    data = request.get_json()
    filename = data.get('filename', 'captured_image.png')
    
    try:
        frame = camera.GetImage().GetNPArray()
        frame = cv.resize(frame, (0, 0), fx=reshape, fy=reshape, interpolation=cv.INTER_LINEAR)
        cv.imwrite(filename, frame)
        return jsonify({"message": f"Image saved as {filename}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
