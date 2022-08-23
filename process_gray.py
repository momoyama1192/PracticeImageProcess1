import numpy as np
import cv2
import math

## 各種関数定義
# (1) 折れ線型トーンカーブ (画素値[明るさ]k倍)
def polygonalTone(input_img,k):
    return np.dot(k,input_img) # np.dot は画素値が255を超える画素を自動的に255に置き換えてくれる

# (2) 初期値付き折れ線型トーンカーブ (画素値k倍 + 初期値a)
def polygonalToneWithIni(input_img,k,a):
    return a + np.dot(k,input_img) # np.dot は画素値が255を超える画素を自動的に255に置き換えてくれる

# (3) 2値化
def binTone(input_img,threshold):
    # しきい値 threshold 以上を真っ白(画素値255)、しきい値未満を真っ黒(画素値0)とする
    return np.where(input_img >= threshold, 255, 0) 

# (4) ネガポジ変換
def negaposiTone(input_img):
    return 255 - input_img

# (5) ガンマ補正[変換] (gamma)
def gammaTone(input_img,gamma):
    output_float = 255 * np.power(input_img / 255, gamma)
    return output_float.astype(np.uint8)

# (6) S字変換
def sigmoidTone(input_img):
    output_float = 255 / (1 + np.exp(-0.05 * (input_img - 127.5) ) )
    return output_float.astype(np.uint8)

# (7) ソラリゼーション
def solaTone(input_img):
    output_float = 127.5 - 255 / 2 * np.cos(3 * math.pi / 255 * input_img)
    return output_float.astype(np.uint8)


## 設定ここから
# 入出力フォルダ設定 
INPUT_DIR = "input/"
OUTPUT_DIR = "output/"

# ファイル設定
INPUT_FILE = "airplane1.jpg"
# 設定ここまで


## ファイル読み込み
input_gray = cv2.imread(INPUT_DIR + INPUT_FILE, cv2.IMREAD_GRAYSCALE) # カラー画像をグレースケール画像に変換
cv2.imwrite(OUTPUT_DIR + "gray_base.jpg",input_gray) # 入力として使うグレースケール画像を出力


## (1) トーンカーブ
# x2倍
output_gray_l20 = polygonalTone(input_gray,2)

# x0.5倍
output_gray_l05 = polygonalTone(input_gray,0.5)

# 出力
cv2.imwrite(OUTPUT_DIR + "gray_res_l20.jpg",output_gray_l20)
cv2.imwrite(OUTPUT_DIR + "gray_res_l05.jpg",output_gray_l05)


## (2) 初期値付きトーンカーブ
#  初期値128 + x0.5倍
output_gray_l05_ad = polygonalToneWithIni(input_gray,0.5,128)

# 出力
cv2.imwrite(OUTPUT_DIR + "gray_res_l05_ad.jpg",output_gray_l05_ad)


## (3) 2値化変換
output_gray_bin = binTone(input_gray,128)

# 出力
cv2.imwrite(OUTPUT_DIR + "gray_res_bin.jpg",output_gray_bin)


## (4) ネガポジ変換
output_gray_negaposi = negaposiTone(input_gray)

# 出力
cv2.imwrite(OUTPUT_DIR + "gray_res_negaposi.jpg",output_gray_negaposi)


## (5) ガンマ変換
# gamma = 1 [そのまま]
gamma = 1.0
output_gray_gamma10 = gammaTone(input_gray,gamma)

# gamma = 0.5
gamma = 0.5
output_gray_gamma05 = gammaTone(input_gray,gamma)

# gamma = 2.0
gamma = 2.0
output_gray_gamma20 = gammaTone(input_gray,gamma)

# 出力
cv2.imwrite(OUTPUT_DIR + "gray_res_gamma10.jpg",output_gray_gamma10)
cv2.imwrite(OUTPUT_DIR + "gray_res_gamma20.jpg",output_gray_gamma20)
cv2.imwrite(OUTPUT_DIR + "gray_res_gamma05.jpg",output_gray_gamma05)


## (6) S字変換
output_gray_sig = sigmoidTone(input_gray)

# 出力
cv2.imwrite(OUTPUT_DIR + "gray_res_sig.jpg",output_gray_sig)


## (7) ソラリゼーション変換
output_gray_sola = solaTone(input_gray)

# 出力
cv2.imwrite(OUTPUT_DIR + "gray_res_sola.jpg",output_gray_sola)
