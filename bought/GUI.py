'''
3. GUI
    input:
        1.受訪者從 {50} 個商品中選擇欲搭配商品 = **i
        2.受訪者從另外 {50} 個商品中選出自己喜愛的 {10} 件單品 = **buy_list
    處理:多執行緒
        a. myfunction
        b. Style2vec
        c. CNN
    ouput:
        搭配結果
    圖片路徑**
'''

from tkinter import *  
import tkinter.scrolledtext as tkst
import threading  
import time  
from PIL import ImageTk,Image  
from tkinter import filedialog
from tkinter.filedialog import askopenfilename  
import tkinter.ttk as ttk


import sys
import os.path
root_path = (os.path.abspath('../')) #STYLE2VEC
sys.path.append(root_path)
from pic_320 import image_process
from bought import Multi_Process
  


def choosepic():  
    '''上傳圖片,並顯示路徑和縮圖在視窗中'''
    path_ = askopenfilename()  
    path.set(path_) 
    # 顯示位置(path)
    e1 = Entry(root, state='readonly', text=path)  
    e1.grid(row=3, columnspan=2) 
    # 顯示縮圖
    im = Image.open(e1.get())
    im = im.resize((160, 160))
    img = ImageTk.PhotoImage(im)  
    l1 = Label(root, height=160)  
    l1.grid(row=4, columnspan=2) 
    l1.config(image=img)  
    l1.image = img #keep a reference

def create_image_label(name):
    global image_file, im, image_label    
    image_file = Image.open('result_%s.png' % name)
    im = ImageTk.PhotoImage(image_file)
    image_label = Label(root,image = im)
    image_label.grid(row=11, columnspan=2)

def Button_CNN():
    create_image_label('CNN')
def Button_Style2vec():
    create_image_label('Style2vec')
def Button_myfunction():
    create_image_label('myfunction')


def fun():
    # itemi
    itemi = itemi_text.get()
    itemii = str(item_list[int(itemi)][:-4])
    # A buy list
    style = style_text.get()
    style_list = style.split(',')
    A_user_buy_to_list = []
    for i in style_list:
        A_user_buy_to_list.append(str(item_list[int(i)][:-4]))

    # 執行多執行緒
    #Multi_Process.run('1038784', A_user_buy_to_list)
    Multi_Process.run(itemii, A_user_buy_to_list)

    # 顯示結果
    lf = ttk.Labelframe(text='結果輸出')
    lf.grid(row=9, columnspan=2)

    Button1 = ttk.Button(lf, text='CNN', command=Button_CNN)
    Button1.grid(row=10, column=0, padx=(20, 20), pady=(20, 20))
    Button2 = ttk.Button(lf, text='Style2vec', command=Button_Style2vec)
    Button2.grid(row=10, column=1, padx=(20, 20), pady=(20, 20))
    Button3 = ttk.Button(lf, text='myfunction', command=Button_myfunction)
    Button3.grid(row=10, column=2, padx=(20, 20), pady=(20, 20))

    var.set('運算結束')


if __name__ == '__main__':
    #window
    root=Tk()  #實例化出一個父窗口
    root.title('Style vector recommendation')  #窗口標題  
    root.geometry('+600+100') #geometry('290x160+10+10'):290 160為窗口大小，+10 +10 定義窗口彈出時的默認展示位置  

    #image(0,0)
    item_list = image_process.random_photo_join() #**50圖片name
    pil_image = Image.open('merged.png')
    background_image = ImageTk.PhotoImage(pil_image)
    Label(root, image=background_image).grid(row=0, columnspan=2)

    #text(1,0)
    Label(root, text='輸入預搭配商品的編號, 或點擊"選擇圖片"上傳圖片').grid(row=1, columnspan=2)
    #itemi_text輸入窗(2,0)
    itemi_text = StringVar()
    Entry(root, width=22, textvariable = itemi_text).grid(row=2, column=0, sticky=E)
    itemi_text.set(" ")
    #選擇圖片Button(2,1)
    path = StringVar()  
    Button(root, text='選擇圖片', command=choosepic).grid(row=2, column=1, sticky=W) 

    #text(5,0)
    Label(root, text='輸入喜愛商品的編號, 以逗號分隔, 不限數量:').grid(row=5, columnspan=2)
    #style_text輸入層(6,0)
    style_text = StringVar()
    Entry(root, width=30, textvariable=style_text).grid(row=6, columnspan=2)
    style_text.set(" ")

    #執行button(7,0)
    Button(root, text='開始', width=15, height=2 , font='bold', command=fun).grid(row=7, columnspan=2)
    #點擊執行(8,0)
    var = StringVar() 
    Label(root, fg='red', textvariable=var).grid(row=8, columnspan=2)
    var.set('點擊執行')

    #父窗口進入事件循環，可以理解為保持窗口運行，否則界面不展示
    root.mainloop() 