# Disparity mapの解析

解析したいDisparity mapが入っているフォルダを直接, main.py にドラッグ&ドロップする。
ステレオカメラから出力される複数枚の同じ状態のDisparity mapのフォルダを入力することで，
日付フォルダが生成され，その中に

    1. disparity_map_raw: inputしたDisparity map
    2. disparity_map_cut: inputしたDisparity mapの有効範囲を切り出したDisparity
    3. disparity_map_concat:切り出したDisparity mapを結合したDisparity map
    4. disparity_mao_hist: 結合したDisparity mapのヒストグラム
    5. disparity_mao_data: 結合したDisparity mapの輝度値の割合，標準偏差，平均，輝度値4096以下の割合

が生成される．

## 1. Disparity mapの前処理

inputするDisparity mapの中で有効な範囲を切り取る．
有効な範囲は目視で設定する．
設定する座標は以下の4点で指定し，長方形で切り取る．

```main.py
    """検証用紙の切り抜き部分(要調整)"""
    Top = 440
    Bottom = 550
    Left = 850
    Right = 1030
```

切り取られたDisparity mapは，横方向に全て結合する．

## 2. 統計データの取得

前処理で取得したDisparity mapについて，ヒストグラムを作成する．
また，Disparity mapの輝度値の割合，標準偏差，平均，輝度値4096以下の割合を取得する．
輝度値4096は，輝度情報として出力されるdisparityの有効値が4096以下なのでこの値を使用した．

## 注意事項
同じ状況でDisparity mapを取得しても，異なるdisparity mapが取得去れることがある．
そのため．複数枚のDisparity mapを入力として扱う．
