#-*- coding: utf-8 -*-
import os, sys
import os.path
root_path = (os.path.abspath('../')) #STYLE2VEC
sys.path.append(root_path)
from bought import Comb
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw



def pic_320():
    '''將照片補為320*320,底圖為白色'''
    DATA_DIR = root_path+"/cnn/all_img"
    file_data = []

    for filename in os.listdir(DATA_DIR):
        img1 = Image.open(os.path.join(DATA_DIR, filename))                   #load img
        if img1.size != (320, 320):
            print ("Loading: %s" %(filename))
            img2 = Image.new('RGB', (320, 320), (255,255,255))                #建一个白底圖
            box1 = (0, 0, img1.size[0]-1, img1.size[1]-1)                     #選取input的圖片
            region = img1.crop(box1)                                          #複製input圖片
            img2.paste(region, ((320-img1.size[0])/2, (320-img1.size[1])/2))  #粘貼圖片(置中)
            img2.save(os.path.join(DATA_DIR, filename))

def random_photo_join(item_list=None, save_name=None):
    '''在目錄下隨機選擇X個商品組成10*5的縮圖'''
    # 如果沒有來源item_list
    if item_list is None:
        # 是存在model和購買紀錄的商品
        comb_list = Comb.dirdata()
        import random
        # 隨機50筆
        item_list = random.sample(comb_list, 50)

    # Image detail
    path = os.path.abspath('../cnn/all_img')
    ims = [Image.open(os.path.join(path, fn)) for fn in item_list] 
    width, height = ims[0].size
    # 新建底圖,'RGBA'=png透明底圖
    result = Image.new('RGBA',(width*10, height*5))
    # 設置浮水印字體,尺寸(查字體執行輸入:%windir%\fonts)
    font = ImageFont.truetype('ahronbd.ttf',size=70)
    
    for i, im in enumerate(ims):
        # 在圖片上添加文字
        draw = ImageDraw.Draw(im)
        draw.text((0, 0),str(i),(16,78,139),font=font)
        draw = ImageDraw.Draw(im)
        # 貼上縮圖
        loc = ((i % 10) * width, (int(i/10) * height)) 
        result.paste(im, loc)

    w,h = result.size
    result.thumbnail((w//4, h//4))

    # 保存:判斷有沒有save_name
    if save_name is None:
        result.save('merged.png')
        return item_list
    else:
        result.save('result_%s.png' %(save_name))


if __name__ == "__main__":
    random_photo_join()


