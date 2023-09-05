# disparity に関する情報を直接出すプログラム
# disparity map が入っているファイルを直接ドラッグ&ドロップする
# 生成されるものは、disparityのraw画像, disparityのトリミング画像, トリミング後のヒストグラム, ヒストグラムの値

import os
import sys
import csv
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import datetime



"""日付ファイルを生成"""
# 現在の日付と時間を取得
current_datetime = datetime.datetime.now()
date_str = current_datetime.strftime('%Y-%m-%d')
time_str = current_datetime.strftime('%H-%M-%S')

# フォルダを生成するディレクトリのパスを指定
output_directory = 'C:/Users/puu02/Documents/03_JobHanting/summer_intern/Bosch/programm/disparity_evaluation/pattern/'  # your path

# フォルダ名を生成
folder_name = f'{date_str}_{time_str}'

# フォルダの絶対パスを生成
folder_path = os.path.join(output_directory, folder_name)

# フォルダを生成
os.makedirs(folder_path)


"""rawdataファイル / cutファイル / ヒストグラムファイル / 統計データファイルの生成"""
# フォルダ名を生成
folder_name_raw = 'disparity_map_raw'
folder_name_cut = 'disparity_map_cut'
folder_name_hist = 'disparity_map_hist'
folder_name_data = 'disparity_map_data'


# フォルダの絶対パスを生成
folder_path_raw = os.path.join(folder_path, folder_name_raw)
folder_path_cut = os.path.join(folder_path, folder_name_cut)
folder_path_hist = os.path.join(folder_path, folder_name_hist)
folder_path_data = os.path.join(folder_path, folder_name_data)

# フォルダを生成
os.makedirs(folder_path_raw)
os.makedirs(folder_path_cut)
os.makedirs(folder_path_hist)
os.makedirs(folder_path_data)


# ####################################################################################################################


def generate_raw(file_path, output_folder):

    # 画像ファイルの拡張子
    image_extension = ".png"
    # ディレクトリ内の画像ファイルのリストを取得
    image_files = [f for f in os.listdir(file_path) if f.endswith(image_extension)]

    # リスト内の画像ファイルを順に処理
    for image_file in image_files:
        image_path = os.path.join(file_path, image_file)
        image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

        if image is not None:
            # 出力する画像の名前
            output_filename = f"{image_file}"
            # 出力する画像のパス
            output_path_name = os.path.join(output_folder, output_filename)
            # 画像の出力
            cv.imwrite(output_path_name, image)

        else:
            print("Error reading image:", image_file)


####################################################################################################################


def image_cut(image_file_path, output_folder, Top, Bottom, Left, Right):

    # 画像ファイルの拡張子
    image_extension = ".png"
    # ディレクトリ内の画像ファイルのリストを取得
    image_files = [f for f in os.listdir(image_file_path) if f.endswith(image_extension)]

    # リスト内の画像ファイルを順に処理
    for image_file in image_files:
        image_path = os.path.join(image_file_path, image_file)
        image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

        if image is not None:
            # 画像のトリミング
            img_temp = image[Top:Bottom, Left:Right]   # img[top : bottom, left : right]

            # 出力する画像の名前
            output_filename = f"{image_file}"
            # 出力する画像のパス
            output_path_name = os.path.join(output_folder, output_filename)
            # 画像の出力
            cv.imwrite(output_path_name, img_temp)

        else:
            print("Error reading image:", image_file)



###############################################################################################################


def generate_histgram(image_cut_file_path, output_folder_1, output_folder_2):

    # 画像ファイルの拡張子
    image_extension = ".png"
    # ディレクトリ内の画像ファイルのリストを取得
    image_files = [f for f in os.listdir(image_cut_file_path) if f.endswith(image_extension)]

    # リスト内の画像ファイルを順に処理
    for image_file in image_files:
        # 読み込む画像のディレクトリ
        image_path = os.path.join(image_cut_file_path, image_file)
        # 画像の読み込み
        image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
        
        if image is not None:
            # ヒストグラムの作成
            image_hist = cv.calcHist([image], [0], None, [256], [0, 256])
            fig, ax = plt.subplots(dpi=100)
            plt.plot(image_hist)

            # 出力する画像の名前
            output_filename = f"{image_file}"
            # 出力する画像のパス
            output_path_image = os.path.join(output_folder_1, output_filename)
            # 画像の保存
            plt.savefig(output_path_image)



            # 画像の平均値
            img_average = np.average(image)
            # 画像の標準偏差
            img_std = np.std(image)

            # 輝度の割合を配列に保存
            luminance_sum = np.sum(image_hist)
            luminance_ratio = np.zeros(256)
            for i in range(len(luminance_ratio)):
                temp_ratio = image_hist[i]*100/luminance_sum
                luminance_ratio[i] = np.round(temp_ratio,1)

            # ゼロを取り除いたときの配列番号と値を表示
            non_zero_indices, non_zero_values = remove_zeros_and_get_indices(luminance_ratio)

            csv_filename = f"{image_file}" + ".csv"
            # 出力する画像のパス
            output_path_csv = os.path.join(output_folder_2, csv_filename)
            # raw dataの書き込み
            with open(output_path_csv, 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(['luminance', 'percentage', 'average', 'standard deviation'])
                writer.writerow([non_zero_indices[0], non_zero_values[0], img_average, img_std])
                for index, value in zip(non_zero_indices[1:], non_zero_values[1:]):
                    writer.writerow([index, value])

        else:
            print("Error reading image:", image_file)


# 輝度値の割合
def remove_zeros_and_get_indices(arr):
    non_zero_values = []
    non_zero_indices = []

    for index, value in enumerate(arr):
        if value != 0:
            non_zero_values.append(value)
            non_zero_indices.append(index)

    return non_zero_indices, non_zero_values


###############################################################################################################


if __name__ == "__main__":
    
    """検証用紙の切り抜き部分(要調整)"""
    Top = 450
    Bottom = 550
    Left = 920
    Right = 1100
    
    # ドラッグ&ドロップされたパスを処理
    for path in sys.argv[1:]:
        # raw 画像の生成
        generate_raw(path, folder_path_raw)
    
    # raw画像のトリミング
    image_cut(folder_path_raw, folder_path_cut, Top, Bottom, Left, Right)
    # ヒストグラムと、その他統計値の取得
    generate_histgram(folder_path_cut, folder_path_hist, folder_path_data)


