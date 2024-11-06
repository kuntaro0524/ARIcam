import cv2
import neoapi
#Mono8データライブ表示の場合
#opencv-python利用
camera = neoapi.Cam()
camera.Connect('ARI-Camera')
#camera.f.PixelFormat.SetString('BGR8')
##camera.f.PixelFormat.SetString('BayerRG10')
##camera.f.PixelFormat.SetString('BayerRG8')
#camera.f.PixelFormat.SetString('Mono10')
#camera.f.PixelFormat.SetString('Mono8')
camera.f.PixelFormat.SetString('RGB8')

while cv2.waitKey(1) != 27 :
	buffer = camera.GetImage()
	mat_buffer = buffer.GetNPArray()
	cv2.imshow("", mat_buffer)
