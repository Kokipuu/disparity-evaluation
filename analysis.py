import os
import csv
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import datetime


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

# csvファイルの出力先のファイル
output_csv = "percentage"

# フォルダを生成するディレクトリのパスを指定
output_directory_histgram = 'C:/Users/puu02/Documents/03_JobHanting/summer_intern/Bosch/programm/hoge/histgram/'
output_directory_percentage = 'C:/Users/puu02/Documents/03_JobHanting/summer_intern/Bosch/programm/hoge/percentage/'

# 現在の日付と時間を取得
current_datetime = datetime.datetime.now()
date_str = current_datetime.strftime('%Y-%m-%d')
time_str = current_datetime.strftime('%H-%M-%S')
# フォルダ名を生成
folder_name = f'{date_str}_{time_str}'
# フォルダの絶対パスを生成
folder_path_histgram = os.path.join(output_directory_histgram, folder_name)
folder_path_percentage = os.path.join(output_directory_percentage, folder_name)
# フォルダを生成
os.makedirs(folder_path_histgram)
os.makedirs(folder_path_percentage)


# リスト内の画像ファイルを順に処理
for image_file in image_files:
    # 読み込む画像のディレクトリ
    image_path = os.path.join(image_dir, image_file)
    # 画像の読み込み
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    
    if image is not None:
        # ヒストグラムの表示
        image_hist = cv.calcHist([image], [0], None, [256], [0, 256])
        fig, ax = plt.subplots(dpi=100)
        # ヒストグラムの保存
        plt.plot(image_hist)
        # plt.show()

        # 出力する画像の名前
        output_filename = f"{image_file}"
        # 出力する画像のパス
        output_path_image = os.path.join(folder_path_histgram, output_filename)
        # 画像の保存
        plt.savefig(output_path_image)
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

        csv_filename = f"{image_file}" + ".csv"
        # 出力する画像のパス
        output_path_csv = os.path.join(output_csv, csv_filename)
        # raw dataの書き込み
        with open(output_path_csv, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['luminance', 'percentage'])
            for index, value in zip(non_zero_indices, non_zero_values):
                writer.writerow([index, value])

    else:
        print("Error reading image:", image_file)

