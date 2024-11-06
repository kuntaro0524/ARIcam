import neoapi
#カメラの初期化と1枚画像キャプチャ
camera = neoapi.Cam()
camera.Connect('ARI-Camera')
camera.f.PixelFormat.SetString('RGB8')
buffer = camera.GetImage()
