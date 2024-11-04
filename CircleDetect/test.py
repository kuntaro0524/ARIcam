import cv2
import numpy as np
from reportlab.pdfgen import canvas

def detect_circle(image_path):
    print(f" reading image from {image_path}")
    # 画像の読み込み
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 円検出 (HoughCirclesで円を検出)
    # 直径に相当する部分をminRadiusとmaxRadiusで指定
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=1, param1=100, param2=30, minRadius=60, maxRadius=90)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        print(circles)
        return circles
    else:
        return None

def calculate_shift(red_circle, green_circle):
    # 赤丸と緑丸の中心座標をもとにシフト量を計算
    x_shift = green_circle[0] - red_circle[0]
    y_shift = green_circle[1] - red_circle[1]
    return x_shift, y_shift

def create_pdf_report(x_shift, y_shift, output_path="report.pdf"):
    c = canvas.Canvas(output_path)
    c.drawString(100, 750, "移動量レポート")
    c.drawString(100, 730, f"X方向の移動量: {x_shift} px")
    c.drawString(100, 710, f"Y方向の移動量: {y_shift} px")
    c.save()

# メイン処理
import sys
import os

image_path = sys.argv[1]

if not os.path.exists(image_path):
    print("エラー: 画像ファイルが見つかりません。パスを確認してください。")
else:
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print("エラー: 画像が読み込めませんでした。画像形式やパスを確認してください。")
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("画像が正常に読み込まれ、グレースケール変換が完了しました。")

circles = detect_circle(image_path)

# circlesを描画する
from matplotlib import pyplot as plt

for ci in circles:
    cv2.circle(image, (ci[0], ci[1]), ci[2], (0, 255, 0), 2)
    
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()

if circles is not None:
    # 赤丸（5mm）と緑丸（6mm）の中心を特定（仮に先頭の2つを使用）
    red_circle = circles[0]
    green_circle = circles[1] if len(circles) > 1 else red_circle  # 赤丸がずれている場合

    x_shift, y_shift = calculate_shift(red_circle, green_circle)
    print(f"X方向の移動量: {x_shift} px")
    print(f"Y方向の移動量: {y_shift} px")

    create_pdf_report(x_shift, y_shift)

else:
    print("円が検出されませんでした。")