import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


# 輝度値の割合
def remove_zeros_and_get_indices(arr):
    non_zero_values = []
    non_zero_indices = []

    for index, value in enumerate(arr):
        if value != 0:
            non_zero_values.append(value)
            non_zero_indices.append(index)

    return non_zero_indices, non_zero_values



# 画像ファイルが格納されているディレクトリのパス
image_dir = "data-processing"

# 画像の出力先のディレクトリのパス
output_dir = "histgram"

# 画像ファイルの拡張子
image_extension = ".png"

# ディレクトリ内の画像ファイルのリストを取得
image_files = [f for f in os.listdir(image_dir) if f.endswith(image_extension)]


# リスト内の画像ファイルを順に処理
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    
    if image is not None:
        # ヒストグラムの表示
        image_hist = cv.calcHist([image], [0], None, [256], [0, 256])
        fig, ax = plt.subplots(dpi=100)
        plt.plot(image_hist)
        # plt.show()

        # 出力する画像の名前
        output_filename = f"{image_file}"

        # 出力する画像のパス
        output_path_name = os.path.join(output_dir, output_filename)

        # 画像の保存
        plt.savefig(output_path_name)

        # 出力した画像の名前を表示
        print("Processing:", image_file)

        # 画像の平均値
        img_average = np.average(image)
        print(img_average)

        # 画像の標準偏差
        img_std = np.std(image)
        print(img_std)

        # 輝度の割合を配列に保存
        luminance_sum = np.sum(image_hist)
        luminance_ratio = np.zeros(256)
        for i in range(len(luminance_ratio)):
            temp_ratio = image_hist[i]*100/luminance_sum
            luminance_ratio[i] = np.round(temp_ratio,1)

        # ゼロを取り除いたときの配列番号と値を表示
        non_zero_indices, non_zero_values = remove_zeros_and_get_indices(luminance_ratio)
        for index, value in zip(non_zero_indices, non_zero_values):
            print(f"Luminance: {index}, ratio: {value} %")


    else:
        print("Error reading image:", image_file)

