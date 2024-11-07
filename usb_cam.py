import cv2 as cv

# カメラの初期化（通常はカメラ0がUSBカメラに対応）
cap = cv.VideoCapture(0)

# カメラの解像度設定 (オプション)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

# フレームを取得し、表示するループ
while True:
    # フレームを読み取る
    ret, frame = cap.read()
    
    # カメラからのフレーム取得が成功したかを確認
    if not ret:
        print("フレームを取得できませんでした。")
        break

    # 画像をウィンドウに表示
    cv.imshow('USB Camera Feed', frame)

    # 'q'キーが押されたらループを終了
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを解放してウィンドウを閉じる
cap.release()
cv.destroyAllWindows()

