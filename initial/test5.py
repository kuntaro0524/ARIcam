import neoapi
import cv2 as cv
import numpy as np

#fpsを20.0にして撮影したい場合はfps=20.0にします (Min:2.5)
fps_forCamera = 24 
fps_forVideo = 24

#Binning ( 1 or 2 )
Binning = 2

#画像の縮小率(Original W x H :1280 x 1024)
reshape = 1.0

#動画保存用ファイル名
name = "sample"

# ExposureTimeの設定
#ExposureAuto = True
ExposureAuto = False

# Camera Setting
#設定値の取得と変更

camera = neoapi.Cam()
camera.Connect('ARI-Camera')

# PixelFormat(カラーモード)の選択
#camera.f.PixelFormat.SetString('BGR8')
#camera.f.PixelFormat.SetString('BayerRG10')
#camera.f.PixelFormat.SetString('BayerRG8')
#camera.f.PixelFormat.SetString('Mono10')
#camera.f.PixelFormat.SetString('Mono8')
camera.f.PixelFormat.SetString('RGB8')


print("camera.f.TriggerMode.value", camera.f.TriggerMode.value)

# Binning Mode (0:Average, 1:Sum)
print("\nBinning")
camera.f.BinningVerticalMode.value=0
camera.f.BinningHorizontalMode.value=0
print("camera.f.BinningHorizontalMode.GetString",camera.f.BinningHorizontalMode.GetString())
print("camera.f.BinningVerticalMode.GetString",camera.f.BinningVerticalMode.GetString())

# Num pixels for Binning
camera.f.BinningVertical.value = Binning
camera.f.BinningHorizontal.value = Binning 
print("camera.f.BinningVertical.value",camera.f.BinningVertical.value)
print("camera.f.BinningHorizontal.value",camera.f.BinningHorizontal.value)

#camera.f.BinningSelector.value = 1
print("camera.f.BinningSelector.value",camera.f.BinningSelector.value)
print("camera.f.BinningSelector.GetString",camera.f.BinningSelector.GetString())

#ホワイトバランス調整可能なら実行
print("\nWhite Balance")
if(camera.HasFeature("BalanceWhiteAuto")) :
        print("BalanceWhiteAuto: %s" %camera.f.BalanceWhiteAuto.value)
        camera.f.BalanceWhiteAuto.SetString("Once")

# ExposureTimeの設定
print("\nExposureTime and Gain")
if ExposureAuto == True :
    camera.f.ExposureAuto.SetString("Continuous") # Set ExposureAuto = ON
    #camera.f.ExposureAuto.SetString("Off")         # Set ExposureAuto = OFF

    # Auto ExposureTime のとき変更する値 (0: ExposureAuto, 1: GainAuto)
    camera.f.BrightnessAutoPriority.value=0
    print("camera.f.BrightnessAutoPriority.value",camera.f.BrightnessAutoPriority.value)
    print("camera.f.BrightnessAutoPriority.GetString",camera.f.BrightnessAutoPriority.GetString())

    # Auto ExposureTime のときのTarget Brightness ???
    #print("camera.f.BrightnessCorrection.value",camera.f.BrightnessCorrection.value)
    #print("camera.f.BrightnessCorrection.GetString",camera.f.BrightnessCorrection.GetString())
    #print("camera.f.CalibrationMatrixValueSelector.value",camera.f.CalibrationMatrixValueSelector.value)
else:
    # ExposureTimeを指定するときには ExposureAuto='Off' が必要
    camera.f.ExposureAuto.SetString("Off") # Set ExposureAuto = OFF
    camera.f.ExposureTime.Set(15000)

    # Gainを指定するときは GainAuto='Off', GainSelector='All' が必要
    print("camera.f.GainAuto.GetString",camera.f.GainAuto.GetString())
    print("camera.f.GainSelector.GetString",camera.f.GainSelector.GetString())
    camera.f.GainAuto.SetString("Off")
    camera.f.GainSelector.SetString("All")

    camera.f.Gain.value=1.0

# Get Exposure Time
print("camera.f.ExposureAuto.value",camera.f.ExposureAuto.value)
print("camera.f.ExposureAuto.GetString",camera.f.ExposureAuto.GetString())
print("camera.f.ExposureTime.value",camera.f.ExposureTime.value)
print("camera.f.Gain.value",camera.f.Gain.value)

print("ExposureAutoMax:",camera.f.ExposureAutoMaxValue.value)
print("ExposureAutoMin",camera.f.ExposureAutoMinValue.value)

# CameraのFrameRateの設定
print("\nVideoCaputer Setting")
camera.f.AcquisitionFrameRateEnable.value = True
camera.f.AcquisitionFrameRate.value = fps_forCamera

print("CameraFrameRate:",camera.f.AcquisitionFrameRate.value)

#動画保存時の形式を設定
# ビデオライターを作成（AVIコンテナとXVIDコーデックを使用）
fourcc = cv.VideoWriter_fourcc(*'DIVX')
ext = ".avi"

# ビデオライターを作成（webmコンテナとVP9 を使用）
#fourcc = cv.VideoWriter_fourcc(*'mp4v')
#ext = ".mp4"

# ビデオライターを作成（mp4コンテナとMJPGを使用）
#fourcc = cv.VideoWriter_fourcc(*'MJPG')
#ext = ".avi"

buffer = camera.GetImage()
frame_width = int(reshape * camera.f.Width.value)   # フレームの幅
frame_height = int(reshape * camera.f.Height.value) # フレームの高さ
print ("original width, original height",camera.f.Width.value, camera.f.Height.value)
print ("frame width, fraime height",frame_width, frame_height)

#(保存名前、fourcc,fps,サイズ)
video = cv.VideoWriter(name+ext, fourcc, fps_forVideo, (frame_width, frame_height))

SaveFlag = 0
ret = 0

#for i in range(0, 200):
while True:
   frame = camera.GetImage().GetNPArray()
   frame = cv.resize(frame, (0,0), fx=reshape,fy=reshape, interpolation= cv.INTER_LINEAR)
   key = cv.waitKey(1)
   #print (key)
   if key == 27 :
      break
   elif key == 113:
      print ("push q")
      if video.isOpened() == True:
          print ("close videoWriter") 
          video.release()
      #print ("ret",video.isOpened())
      SaveFlag = 0
   elif key == 115:
      print ("push s")
      video = cv.VideoWriter(name+ext, fourcc, fps_forVideo, (frame_width, frame_height))
      #print ("ret",video.isOpened())
      SaveFlag = 1

   if SaveFlag == 1:
#      print ("save movie")
      video.write(frame) #1フレーム保存する

   cv.imshow("window",frame)

cv.imwrite("test.png",frame)

# Do a bit of cleanup
print("\n Exit Program")
if video.isOpened() == True:
    print ("close videoWriter") 
    video.release()

cv.destroyAllWindows()

