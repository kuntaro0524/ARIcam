#Mono8データライブ表示の場合
#opencv-python利用
import neoapi
import cv2
camera = neoapi.Cam()
camera.Connect('ARI-Camera')
camera.f.PixelFormat.SetString('RGB8')

#camera.f.PixelFormat.SetString('Mono8')
#設定値の取得と変更
#ホワイトバランス調整可能なら実行
if(camera.HasFeature("BalanceWhiteAuto")) :
        print("BalanceWhiteAuto: %s" %camera.f.BalanceWhiteAuto.value)
        camera.f.BalanceWhiteAuto.SetString("Once")

print("####################")
print(camera.f.ExposureAutoMaxValue.value)
print(camera.f.ExposureAutoMinValue.value)
print("####################")

#camera.f.ExposureTime.value = 30000.0
# camera.f.ExposureTime.Set(1.0)
camera.f.AcquisitionFrameRateEnable.value = True
camera.f.AcquisitionFrameRate.value = 10
print(f"{camera.f.AcquisitionFrameRate.value} frame rate")

while cv2.waitKey(1) != 27 :
        buffer = camera.GetImage()
#        mat_buffer = buffer.GetNPArray().reshape(buffer.GetHeight(), buffer.GetWidth())
        mat_buffer = buffer.GetNPArray()
        cv2.imshow("TEST", mat_buffer)

print(buffer.GetHeight(), buffer.GetWidth())
cv2.imwrite("test.png",mat_buffer)
