# coding: utf-8
from PIL import Image, ImageFilter
import os
import glob
import json
import pathlib
import argparse

# 引数の処理
parser = argparse.ArgumentParser(description='add two integers')
parser.add_argument('--setting')  
parser.add_argument('--imagedir')  
args = parser.parse_args()

# 設定ファイル
setting_file = args.setting

# 対象ディレクトリ以下のファイルをすべて対象にする
print(args.imagedir)
all_image_path_array = []
files = glob.glob(f'{args.imagedir}/*')
for file in files:
    all_image_path_array.append(file)
all_image_path_array.sort()

# 設定ファイルの読み込み
with open(setting_file, 'r') as f:
    setting = json.load(f)

# カード作成情報
image_num = setting['ImageNum']
card_height = setting['CardHeight']

# 名前部分の情報
nm_idx = setting['NameRect']['ImageIndex']
nm_x = setting['NameRect']['X']
nm_y = setting['NameRect']['Y']
nm_w = setting['NameRect']['W']
nm_h = setting['NameRect']['H']

# アイテム部分の情報
it_idx = setting['ItemRect']['ImageIndex']
it_x = setting['ItemRect']['X']
it_y = setting['ItemRect']['Y']
it_w = setting['ItemRect']['W']
it_h = setting['ItemRect']['H']

# 材料部分の情報
mat_idx = setting['MaterialRect']['ImageIndex']
mat_x = setting['MaterialRect']['X']
mat_y = setting['MaterialRect']['Y']
mat_w = setting['MaterialRect']['W']
mat_h = setting['MaterialRect']['H']

# 調合カテゴリ部分の情報
cat_idx = setting['CategoryRect']['ImageIndex']
cat_x = setting['CategoryRect']['X']
cat_y = setting['CategoryRect']['Y']
cat_w = setting['CategoryRect']['W']
cat_h = setting['CategoryRect']['H']


# 指定の1図鑑画像に対する枚数ずつ処理していく
it = iter(all_image_path_array)
while True:
    # 指定枚数分配列に詰め込む
    try:
        image_path_array = []
        for i in range(image_num):
            image_path_array.append(next(it))
    except StopIteration:
        break

    # 画像ファイルの読み込み
    target_items = list()
    for path in image_path_array:
        target_items.append(
            {
                "path": path,
                "image" : Image.open(path),
                "name" : os.path.splitext(os.path.basename(path))[0]
            }
        )

    # アイテム画像の切り抜き
    name_height = int(card_height * 0.15)
    im_name = Image.open(target_items[nm_idx]["path"])
    im_name = im_name.crop((nm_x, nm_y, nm_x + nm_w, nm_y + nm_h))
    im_name = im_name.resize((int(nm_w * name_height / nm_h), name_height))
    #im_name.save(target_items[nm_idx]["name"]+ '_name.png', quality=95)

    # アイテム画像の切り抜き
    im_item = Image.open(target_items[it_idx]["path"])
    im_item = im_item.crop((it_x, it_y, it_x + it_w, it_y + it_h))
    im_item = im_item.resize((int(it_w * card_height / it_h), card_height))
    #im_item.save(target_items[it_idx]["name"]+ '_item.png', quality=95)

    # 材料部分の切り抜き
    im_mat = Image.open(target_items[mat_idx]["path"])
    im_mat = im_mat.crop((mat_x, mat_y, mat_x + mat_w, mat_y + mat_h))
    im_mat = im_mat.resize((int(mat_w * card_height / mat_h), card_height))
    #im_mat.save(target_items[mat_idx]["name"]+ '_mat.png', quality=95)

    # 調合カテゴリ部分の切り抜き
    im_cat = Image.open(target_items[cat_idx]["path"])
    im_cat = im_cat.crop((cat_x, cat_y, cat_x + cat_w, cat_y + cat_h))
    im_cat = im_cat.resize((int(cat_w * card_height / cat_h), card_height))
    #im_cat.save(target_items[cat_idx]["name"]+ '_cat.png', quality=95)

    # カード型に結合
    im_card = Image.new("RGB", (im_item.width + im_mat.width + im_cat.width, card_height), color="black")
    im_card.paste(im_mat, (0, 0))
    im_card.paste(im_item, (im_mat.width, 0))
    im_card.paste(im_cat, (im_mat.width + im_item.width, 0))
    im_card.paste(im_name, (int((im_item.width + im_mat.width + im_cat.width) / 2 - nm_w / 2), 0))
    im_card.save(target_items[cat_idx]["name"]+ '_card.png', quality=95)
