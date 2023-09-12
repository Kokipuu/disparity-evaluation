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
        method.generate_raw(path, folder_path_raw)
    
    # raw画像のトリミング
    method.image_cut(folder_path_raw, folder_path_cut, Top, Bottom, Left, Right)
    # ヒストグラムと、その他統計値の取得
    method.generate_histgram(folder_path_cut, folder_path_hist, folder_path_data)


