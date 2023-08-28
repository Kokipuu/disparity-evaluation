import cv2 as cv
import os


# HIGH = 1024
# WIDTH = 1856
# HIGH_W = 200
# WIDTH_W = 240

# Top = int((HIGH - HIGH_W) / 2)
# Bottom = int((HIGH + HIGH_W) / 2)
# Left = int((WIDTH - WIDTH_W) / 2)
# Right = int((WIDTH + WIDTH_W) / 2)


# 画像ファイルが格納されているディレクトリのパス
image_dir = "disparitymap_0828"

# 画像ファイルの拡張子
image_extension = ".png"

# ディレクトリ内の画像ファイルのリストを取得
image_files = [f for f in os.listdir(image_dir) if f.endswith(image_extension)]

# リスト内の画像ファイルを順に処理
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    if image is not None:
        # img_temp = image[Top:Bottom, Left:Right]   # img[top : bottom, left : right]
        img_temp = image[450:550, 920:1100]   # img[top : bottom, left : right]
        output_filename = f"{image_file}"
        cv.imwrite(output_filename, img_temp)
        print("Processing:", image_file)
    else:
        print("Error reading image:", image_file)


