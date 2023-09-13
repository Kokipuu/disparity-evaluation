import os
import matplotlib.pyplot as plt
import csv
import cv2 as cv
import numpy as np
from PIL import Image



def generate_path(file_path, folder_path):
    # ディレクトリ取得
    dic_files = [f for f in os.listdir(file_path)]

    for dic in dic_files:
        dic_path = os.path.join(file_path, dic)
        # 出力するディレクトリの名前
        output_filename = f"{dic}"
        # 出力するディレクトリのパス
        output_path_name = os.path.join(folder_path, output_filename)

        # フォルダ名を生成
        folder_name_raw = 'disparity_map_raw'
        folder_name_cut = 'disparity_map_cut'
        folder_name_hist = 'disparity_map_hist'
        folder_name_data = 'disparity_map_data'
        folder_name_concat = 'disparity_map_cancat'

        # フォルダのパスを生成
        folder_path_raw = os.path.join(output_path_name, folder_name_raw)
        folder_path_cut = os.path.join(output_path_name, folder_name_cut)
        folder_path_hist = os.path.join(output_path_name, folder_name_hist)
        folder_path_data = os.path.join(output_path_name, folder_name_data)
        folder_path_concat = os.path.join(output_path_name, folder_name_concat)

        # フォルダを生成
        os.makedirs(folder_path_raw)
        os.makedirs(folder_path_cut)
        os.makedirs(folder_path_hist)
        os.makedirs(folder_path_data)
        os.makedirs(folder_path_concat)



def generate_raw(file_path, output_folder):

    # 画像ファイルの拡張子
    image_extension = ".png"
    # ディレクトリ内の画像ファイルのリストを取得
    image_files = [f for f in os.listdir(file_path) if f.endswith(image_extension)]

    # リスト内の画像ファイルを順に処理
    for image_file in image_files:
        image_path = os.path.join(file_path, image_file)
        image = cv.imread(image_path, cv.IMREAD_UNCHANGED)

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
        image = cv.imread(image_path, cv.IMREAD_UNCHANGED)

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


def generate_concat_image(image_cut_file_path, output_folder):

    # 画像ファイルの拡張子
    image_extension = ".png"
    # ディレクトリ内の画像ファイルのリストを取得
    image_files = [f for f in os.listdir(image_cut_file_path) if f.endswith(image_extension)]

    image_path_ = os.path.join(image_cut_file_path, image_files[0])
    image_ = cv.imread(image_path_, cv.IMREAD_UNCHANGED)
    concat_image = image_
    for image_file in image_files:
        image_path = os.path.join(image_cut_file_path, image_file)
        image = cv.imread(image_path, cv.IMREAD_UNCHANGED)
        concat_image = cv.hconcat([concat_image, image])
    
    # 出力する画像の名前
    output_filename = "hoge.png"
    # 出力する画像のパス
    output_path_image = os.path.join(output_folder, output_filename)
    cv.imwrite(output_path_image, concat_image)


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
        image = cv.imread(image_path, cv.IMREAD_UNCHANGED)
        
        if image is not None:
            # ヒストグラムの作成
            image_hist = cv.calcHist([image], [0], None, [65536], [0, 65536])
            fig, ax = plt.subplots(dpi=100)
            plt.plot(image_hist)

            # 出力する画像の名前
            output_filename = f"{image_file}"
            # 出力する画像のパス
            output_path_image = os.path.join(output_folder_1, output_filename)
            # 画像の保存
            plt.savefig(output_path_image)

            # 輝度の平均値
            img_average = np.average(image)
            # 輝度の標準偏差
            img_std = np.std(image)
            #輝度基準以下
            luminance_criteria_sum = 0
            flat_image = image.flatten()
            j_max = len(flat_image)
            for j in range(j_max):
                if flat_image[j] <= 4000:
                    luminance_criteria_sum += 1
            criteria_ratio = luminance_criteria_sum / j_max * 100

            # 輝度の割合を配列に保存
            luminance_sum = np.sum(image_hist)
            luminance_ratio = np.zeros(65536)
            for i in range(len(luminance_ratio)):
                temp_ratio = image_hist[i]*100/luminance_sum
                luminance_ratio[i] = np.round(temp_ratio,3)  # 小数第一位だと誤差が大きいので3ぐらいがいい


            # ゼロを取り除いたときの配列番号と値を表示
            non_zero_indices, non_zero_values = remove_zeros_and_get_indices(luminance_ratio)

            csv_filename = f"{image_file}" + ".csv"
            # 出力する画像のパス
            output_path_csv = os.path.join(output_folder_2, csv_filename)
            # raw dataの書き込み
            with open(output_path_csv, 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(['luminance', 'percentage', 'average', 'standard deviation','under_criteria%'])
                writer.writerow([non_zero_indices[0], non_zero_values[0], img_average, img_std,criteria_ratio])
                for index, value in zip(non_zero_indices[1:], non_zero_values[1:]):
                    writer.writerow([index, value])

        else:
            print("Error reading image:", image_file)


# 輝度値の割合(0%をcsvから除外)
def remove_zeros_and_get_indices(arr):
    non_zero_values = []
    non_zero_indices = []

    for index, value in enumerate(arr):
        if value != 0:
            non_zero_values.append(value)
            non_zero_indices.append(index)

    return non_zero_indices, non_zero_values
