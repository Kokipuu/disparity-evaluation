import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


dir_path = 'C:/Users/puu02/Documents/03_JobHanting/summer_intern/Bosch/programm/hoge/data-processing/'
image_path = 'ra_and_shu_pattern.png'
path_name = dir_path + image_path

# 画像の読み込み
img = cv.imread(path_name, cv.IMREAD_GRAYSCALE)

# # 画像のグレースケール表示
# plt.imshow(img)
# plt.gray()  
# plt.show()

# ヒストグラムの表示
img_hist = cv.calcHist([img], [0], None, [256], [0, 256])
plt.plot(img_hist)
plt.show()
# plt.savefig('b_B_p_G_0828_Am1049.png')

# 画像の平均値
img_average = np.average(img)
print(img_average)

# 画像の標準偏差
img_std = np.std(img)
print(img_std)

# 輝度値の割合
def remove_zeros_and_get_indices(arr):
    non_zero_values = []
    non_zero_indices = []

    for index, value in enumerate(arr):
        if value != 0:
            non_zero_values.append(value)
            non_zero_indices.append(index)

    return non_zero_indices, non_zero_values

luminance_sum = np.sum(img_hist)
luminance_ratio = np.zeros(256)
for i in range(len(luminance_ratio)):
    temp_ratio = img_hist[i]*100/luminance_sum
    luminance_ratio[i] = np.round(temp_ratio,1)

# ゼロを取り除いたときの配列番号と値を表示
non_zero_indices, non_zero_values = remove_zeros_and_get_indices(luminance_ratio)
for index, value in zip(non_zero_indices, non_zero_values):
    print(f"Luminance: {index}, ratio: {value} %")

