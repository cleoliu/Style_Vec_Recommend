# -*- coding: UTF-8 -*-  
import re


def del_symbol():
    # read
    fp = open("Combination_fashion_list.txt", "r")
    s = fp.read()
    s = re.sub(r'[^\w\s]','',s) #正規化去除符號
    fp.close()

    # write
    fp = open("Combination_fashion_str.txt", "a")
    fp.write(s)
    fp.close()

def replace_symbol():
    fp = open("CNNvec.txt", "r")
    s = fp.read()
    s = s.replace(".", ".000") # ";"取代為"},{""  
    fp.close()

    fp = open("CNNvec_1.txt", "a")
    fp.write(s)
    fp.close()

if __name__ == "__main__":
    replace_symbol()
