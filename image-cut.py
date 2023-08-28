import cv2 as cv
import os


# # 画像中心に検証用の用紙がある場合
# HIGH = 1024
# WIDTH = 1856
# HIGH_W = 200
# WIDTH_W = 240
# Top = int((HIGH - HIGH_W) / 2)
# Bottom = int((HIGH + HIGH_W) / 2)
# Left = int((WIDTH - WIDTH_W) / 2)
# Right = int((WIDTH + WIDTH_W) / 2)

# (変更が必要な部分)
# 検証用紙の切り抜き部分
Top = 450
Bottom = 550
Left = 920
Right = 1100

# (変更が必要な部分)
# 画像ファイルが格納されているディレクトリのパス
image_dir = "disparitymap_0828"

# (変更が必要な部分)
# 画像の出力先のディレクトリのパス
output_dir = "image-processing"

# 画像ファイルの拡張子
image_extension = ".png"

# ディレクトリ内の画像ファイルのリストを取得
image_files = [f for f in os.listdir(image_dir) if f.endswith(image_extension)]

# リスト内の画像ファイルを順に処理
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

    if image is not None:
        img_temp = image[Top:Bottom, Left:Right]   # img[top : bottom, left : right]

        # 出力する画像の名前
        output_filename = f"{image_file}"

        # 出力する画像のパス
        output_path_name = os.path.join(output_dir, output_filename)

        # 画像の出力
        cv.imwrite(output_path_name, img_temp)

        # 出力した画像の名前を表示
        print("Processing:", image_file)

    else:
        print("Error reading image:", image_file)

