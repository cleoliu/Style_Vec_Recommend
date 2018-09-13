'''
將-專家推薦集-的-排列組和-輸出
'''
# -*- coding: UTF-8 -*-  

def lines(Combination): #計算總共筆數
    myfile = open(Combination) 
    lines = len(myfile.readlines())
    print "There are **%d** lines in %s" % (lines, Combination)

def write(a, Combination): #寫入新檔
    fw = open(Combination, "a")
    fw.write(str(a)+'\n')
    print(str(a))
    fw.close()

def level7(s, Combination):
    for f0 in s[0]:
        for f1 in s[1]:
            for f2 in s[2]:
                for f3 in s[3]:
                    for f4 in s[4]:
                        for f5 in s[5]:
                            for f6 in s[6]:
                                a = f0,f1,f2,f3,f4,f5,f6
                                write(a, Combination)

def level6(s, Combination):
    for f0 in s[0]:
        for f1 in s[1]:
            for f2 in s[2]:
                for f3 in s[3]:
                    for f4 in s[4]:
                        for f5 in s[5]:
                            a = f0,f1,f2,f3,f4,f5
                            write(a, Combination)

def level5(s, Combination):
    for f0 in s[0]:
        for f1 in s[1]:
            for f2 in s[2]:
                for f3 in s[3]:
                    for f4 in s[4]:
                        a = f0,f1,f2,f3,f4
                        write(a, Combination)

def level4(s, Combination):
    for f0 in s[0]:
        for f1 in s[1]:
            for f2 in s[2]:
                for f3 in s[3]:
                    a = f0,f1,f2,f3
                    write(a, Combination)

def level3(s, Combination):
    for f0 in s[0]:
        for f1 in s[1]:
            for f2 in s[2]:
                a = f0,f1,f2
                write(a, Combination)

def level2(s, Combination):
    for f0 in s[0]:
        for f1 in s[1]:
            a = f0,f1
            write(a, Combination)

def main(fashion_matchsets, Combination):
    fp = open(fashion_matchsets, "r")
    for line in iter(fp):
        line=line.strip('\n')        #逐行讀入
        s = line.replace(";", "},{") #";"取代為"},{""  
        s1 = s.split(" ")            #切割空格前後的字串,只需要後面的資料(原:1 160870;3118604)
        s = "[{"+str(s1[1])+"}]"     #取空白後的字串,前後加上[{ }]
        s = eval(s)                  #str轉list

    # ---判斷list長度---
        if len(s) == 2:
            level2(s, Combination)
        elif len(s) == 3:
            level3(s, Combination)
        elif len(s) == 4:
            level4(s, Combination)
        elif len(s) == 5:
            level5(s, Combination)
        elif len(s) == 6:
            level6(s, Combination)
        else:
            level7(s, Combination)

    # ---關閉讀入檔---
    fp.close()

    # ---計算總共筆數---
    lines(Combination)



if __name__ == "__main__":
    main(fashion_matchsets='dim_fashion_matchsets.txt',Combination='Combination_fashion.txt')