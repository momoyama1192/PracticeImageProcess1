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

# (8) 色合い変換 (k > 1 で特定の色を強める、k < 1 で特定の色を弱める)
# color -> COLOR_RED(赤), COLOR_GREEN(緑), COLOR_BLUE(青), COLOR_ALL(全色) で設定 
def polygonalToneWithColor(input_img,k,color):
    output_img = 1.0 * input_img
    if color == COLOR_ALL:
        output_img = np.dot(k,input_img) 
    else:
        output_img[:,:,color] = np.dot(k,input_img[:,:,color])
    return output_img

## 各種定数定義
COLOR_RED   = 2
COLOR_GREEN = 1
COLOR_BLUE  = 0 
COLOR_ALL   = 3  


## 保存場所設定
# 入出力フォルダ(ディレクトリ)設定 
INPUT_DIR = "input/"
OUTPUT_DIR = "output/"

# 入力ファイル設定 (INPUT_DIR, OUTPUT_DIR内に配置すればOK)
INPUT_FILE = "airplane1.jpg"
# 設定ここまで


## 画像読み込み
input_color = cv2.imread(INPUT_DIR + INPUT_FILE)

## (1) トーンカーブ
# x2倍
output_color_l20 = polygonalTone(input_color,2)

# x0.5倍
output_color_l05 = polygonalTone(input_color,0.5)

# 出力
cv2.imwrite(OUTPUT_DIR + "color_res_l20.jpg",output_color_l20)
cv2.imwrite(OUTPUT_DIR + "color_res_l05.jpg",output_color_l05)


## (2) 初期値付きトーンカーブ
# 初期値128 + x0.5倍
output_color_l05_ad = polygonalToneWithIni(input_color,0.5,128)

# 出力
cv2.imwrite(OUTPUT_DIR + "color_res_l05_ad.jpg",output_color_l05_ad)


## (3) 2値化変換
output_color_bin = binTone(input_color,128)

# 出力
cv2.imwrite(OUTPUT_DIR + "color_res_bin.jpg",output_color_bin)


## (4) ネガポジ変換
output_color_negaposi = negaposiTone(input_color)

# 出力
cv2.imwrite(OUTPUT_DIR + "color_res_negaposi.jpg",output_color_negaposi)


## (5) ガンマ変換
# gamma = 1 [そのまま]
gamma = 1.0
output_color_gamma10 = gammaTone(input_color,gamma)

# gamma = 0.5
gamma = 0.5
output_color_gamma05 = gammaTone(input_color,gamma)

# gamma = 2.0
gamma = 2.0
output_color_gamma20 = gammaTone(input_color,gamma)

# 出力
cv2.imwrite(OUTPUT_DIR + "color_res_gamma10.jpg",output_color_gamma10)
cv2.imwrite(OUTPUT_DIR + "color_res_gamma20.jpg",output_color_gamma20)
cv2.imwrite(OUTPUT_DIR + "color_res_gamma05.jpg",output_color_gamma05)


## (6) S字変換
output_color_sig = sigmoidTone(input_color)

# 出力
cv2.imwrite(OUTPUT_DIR + "color_res_sig.jpg",output_color_sig)


## (7) ソラリゼーション変換
output_color_sola = solaTone(input_color)

# 出力
cv2.imwrite(OUTPUT_DIR + "color_res_sola.jpg",output_color_sola)


## (8) 色合い変化
# 例1. 赤を強める [R x 1.5]
output_color = polygonalToneWithColor(input_color,1.5,COLOR_RED)
cv2.imwrite(OUTPUT_DIR + "color_red_plus.jpg",output_color)

# 例2. 青を弱める [B x 0.5]
output_color = polygonalToneWithColor(input_color,0.5,COLOR_BLUE)
cv2.imwrite(OUTPUT_DIR + "color_blue_minus.jpg",output_color)
