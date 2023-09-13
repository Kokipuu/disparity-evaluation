# disparity に関する情報を直接出すプログラム
# disparity map が入っているファイルを直接ドラッグ&ドロップする
# 生成されるものは、disparityのraw画像, disparityのトリミング画像, トリミング後のヒストグラム, ヒストグラムの値

import os
import sys
import datetime
import method



"""日付ファイルを生成"""
# 現在の日付と時間を取得
current_datetime = datetime.datetime.now()
date_str = current_datetime.strftime('%Y-%m-%d')
time_str = current_datetime.strftime('%H-%M-%S')

# フォルダを生成するディレクトリのパスを指定
output_directory = './pattern'
# フォルダ名を生成
folder_name = f'{date_str}_{time_str}'
# フォルダの相対パスを生成
folder_path = os.path.join(output_directory, folder_name)
# フォルダを生成
os.makedirs(folder_path)



###############################################################################################################


if __name__ == "__main__":
    
    """検証用紙の切り抜き部分(要調整)"""
    Top = 465
    Bottom = 560
    Left = 845
    Right = 1010

    
    # ドラッグ&ドロップされたパスを処理
    for path in sys.argv[1:]:
        # ディレクトリ取得
        dic_files = [f for f in os.listdir(path)]
        for dic in dic_files:
            dic_path = os.path.join(path, dic)

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

            method.generate_raw(dic_path, folder_path_raw)

            # raw画像のトリミング
            method.image_cut(folder_path_raw, folder_path_cut, Top, Bottom, Left, Right)

            # ヒストグラムと、その他統計値の取得
            method.generate_concat_image(folder_path_cut, folder_path_concat)
            method.generate_histgram(folder_path_concat, folder_path_hist, folder_path_data)

