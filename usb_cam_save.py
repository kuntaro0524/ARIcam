import cv2 as cv

# カメラの初期化（0はカメラのインデックス）
cap = cv.VideoCapture(0)

# カメラ解像度の設定 (オプション)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

# 動画の保存設定
# コーデックの指定 (例: 'XVID'、'MJPG'、'DIVX' など)
fourcc = cv.VideoWriter_fourcc(*'XVID')
output_filename = "output_video.avi"
fps = 20.0  # フレームレート

# 保存する動画のサイズ (カメラの解像度に合わせます)
frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
out = cv.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

# フレームを取得し、表示・保存するループ
while True:
    ret, frame = cap.read()

    # フレーム取得に成功しているか確認
    if not ret:
        print("フレームを取得できませんでした。")
        break

    # フレームをウィンドウに表示
    cv.imshow('USB Camera Feed', frame)

    # フレームを動画ファイルに書き込み
    out.write(frame)

    # 'q'キーが押されたら終了
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# リソースの解放
cap.release()
out.release()
cv.destroyAllWindows()

