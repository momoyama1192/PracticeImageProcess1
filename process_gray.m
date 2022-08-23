%% ファイル設定ここから
% 入力画像フォルダ設定
INPUT_DIR = "input/";
OUTPUT_DIR = "output/"; 

% 入力画像種類設定
INPUT_FILE = "airplane1.jpg";
% 設定ここまで


%% ファイル読み込み
% カラー画像で読み込み
input_color = imread(INPUT_DIR + INPUT_FILE);

% グレー変換
input_gray = rgb2gray(input_color);
imwrite(input_gray,OUTPUT_DIR + "gray_base.jpg"); % グレー変換後画像出力


%% (1) 折れ線型トーンカーブ (画素値[明るさ]k倍)
% ×2倍
output_gray_l2 = polygonalTone(input_gray,2);

% ×0.5倍
output_gray_l05 = polygonalTone(input_gray,0.5);

% 出力
imwrite(output_gray_l2,OUTPUT_DIR + "gray_res_l20.jpg");
imwrite(output_gray_l05,OUTPUT_DIR + "gray_res_l05.jpg");


%% (2) 初期値付き折れ線型トーンカーブ (画素値k倍 + 初期値a)
% 初期値128 + x0.5倍
output_gray_l05_ad = polygonalToneWithIni(input_gray,0.5,128);

% 出力
imwrite(output_gray_l05_ad,OUTPUT_DIR + "color_res_l05_ad.jpg");

%% (3) 2値化変換
output_gray_bin = binTone(input_gray,128);

% 出力
imwrite(output_gray_bin,OUTPUT_DIR + "gray_res_bin.jpg");


%% (4) ネガポジ変換
output_gray_negaposi = negaposiTone(input_gray);

% 出力
imwrite(output_gray_negaposi,OUTPUT_DIR + "gray_res_negaposi.jpg");


%% (5) ガンマ変換
% gamma = 1 [そのまま]
gamma = 1;
output_gray_gamma10 = gammaTone(input_gray,gamma);
output_color_gamma10 = gammaTone(input_color,gamma);

% gamma = 0.5
gamma = 0.5;
output_gray_gamma05 = gammaTone(input_gray,gamma);
output_color_gamma05 = gammaTone(input_color,gamma);

% gamma = 2.0
gamma = 2.0;
output_gray_gamma15 = gammaTone(input_gray,gamma);
output_color_gamma15 = gammaTone(input_color,gamma);

% 出力
imwrite(output_gray_gamma10,OUTPUT_DIR + "gray_res_gamma10.jpg");
imwrite(output_gray_gamma15,OUTPUT_DIR + "gray_res_gamma15.jpg");
imwrite(output_gray_gamma05,OUTPUT_DIR + "gray_res_gamma05.jpg");


%% (6) S字変換
output_gray_sig = sigmoidTone(input_gray);

% 出力
imwrite(output_gray_sig ,OUTPUT_DIR + "gray_res_sig.jpg");


%% (7) ソラリゼーション変換
output_gray_sola = solaTone(input_gray);

% 出力
imwrite(output_gray_sola,OUTPUT_DIR + "gray_res_sola.jpg");


%% 各種関数設定(MATLABは後ろに記入)
% (1) 折れ線型トーンカーブ (画素値k倍)
function output_img = polygonalTone(input_img,k)
    % MATLABではオーバーフローはそのまま255となるので、特別な対策は不要
    output_img = k * input_img; 
end

% (2) 初期値付き折れ線型トーンカーブ (画素値k倍 + 初期値a)
function output_img = polygonalToneWithIni(input_img,k,a)
    output_img = a + k * input_img; 
end

% (3) 2値化
function output_img = binTone(input_img,threshold)
    output_img = (input_img >= 128) * 255;
end

% (4) ネガポジ変換
function output_img = negaposiTone(input_img)
    output_img = 255 - input_img;
end

% (5) ガンマ補正[変換] (gamma)
function output_img = gammaTone(input_img,gamma)
    output_double = 255 * power(double(input_img) / 255,gamma); % 計算結果をいったん実数型(double)で保持
    output_img = uint8(output_double);
end

% (6) S字変換
function output_img = sigmoidTone(input_img)
    output_double = 255 ./ (1 * exp(-0.05 * (double(input_img) - 127.5)));  % 計算結果をいったん実数型(double)で保持 
    output_img = uint8(output_double);
end

% (7) ソラリゼーション
function output_img = solaTone(input_img)
    output_double = 127.5 - 255 / 2 * cos(3 * pi / 255 * double(input_img));  % 計算結果をいったん実数型(double)で保持
    output_img = uint8(output_double);
end

% (8) 色合い変換 (k > 1 で特定の色を強める、k < 1 で特定の色を弱める)
% color -> COLOR_RED(赤), COLOR_GREEN(緑), COLOR_BLUE(青), COLOR_ALL(全色) で設定 
function output_img = polygonalToneColor(input_img,k,color)
    output_img = input_img;
    if color == COLOR_ALL
        output_img = input_img * k;
    else
        output_img(:,:,color) = input_img(:,:,color) * k;
    end
end
