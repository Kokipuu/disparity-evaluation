def remove_zeros_and_get_indices(arr):
    non_zero_values = []
    non_zero_indices = []

    for index, value in enumerate(arr):
        if value != 0:
            non_zero_values.append(value)
            non_zero_indices.append(index)

    return non_zero_indices, non_zero_values

# ゼロを多く含む配列
original_array = [0, 5, 0, 3, 0, 8, 0, 0, 2]

# ゼロを取り除いたときの配列番号と値を表示
non_zero_indices, non_zero_values = remove_zeros_and_get_indices(original_array)
for index, value in zip(non_zero_indices, non_zero_values):
    print(f"Index: {index}, Value: {value}")
