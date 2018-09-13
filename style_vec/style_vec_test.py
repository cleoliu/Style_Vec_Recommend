#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings(action='ignore',category=UserWarning,module='gensim')
import logging
from gensim.models import word2vec
from gensim.models.keyedvectors import KeyedVectors



class Test:
    def __init__(self, text_name):
        '''---load model---'''
        self.model = KeyedVectors.load_word2vec_format(text_name)
        #self.model = word2vec.Word2Vec.load(text_name)
        #self.model = KeyedVectors.load_word2vec_format(text_name, binary=False)

    def test_word_vec(self, word):
        '''a.印出詞向量'''
        # [-0.98200446  1.57162261  0.25008738  0.37547648  1.28689885 -0.41987607 -0.88645846 -1.44547033 -0.41050833 -0.06790406]
        print (self.model[word])


    def test_20relation(self, first):
        '''b.計算某個詞的相關詞列表'''
        y2 = self.model.most_similar(first, topn=20)  # 20个最相关的
        print (u"%s similarity word：\n" %(first))
        item_list = [first+".jpg"]
        for item in y2:
            print (item[0], item[1])
            item_list.append(item[0]+".jpg")
        print ("--------\n")
        return item_list


    def test_2similarity(self, first, second):
        '''c.計算兩個詞的相似度/相關程度
        woman & man similarity： 0.985365249752'''
        y1 = self.model.similarity(first, second)
        print ("%s & %s similarity：%s" %(first, second, y1))
        print ("--------\n")


    def test_Correspondence(self, first, second, third): 
        '''d.尋找對應關係
        "boy" is to "father" as "girl" is to ...?'''
        print (' "%s" is to "%s" as "%s" is to ...? \n' %(first, second, third))
        y3 = self.model.most_similar([third, second], [first], topn=3)
        for item in y3:
            print (item[0], item[1])
        print ("--------\n")
        '''
        more_examples = ["he his she", "big bigger bad", "going went being"]
        for example in more_examples:
            a, b, x = example.split()
            predicted = self.model.most_similar([x, b], [a])[0][0]
            print ("'%s' is to '%s' as '%s' is to '%s'" % (a, b, x, predicted)) # 'he' is to 'his' as 'she' is to 'her'
        print ("--------\n")
        '''


    def test_doesnt_match(self, string):
        '''e.尋找不合群的詞'''
        y4 = self.model.doesnt_match(string.split())
        print (u"Not gregarious：", y4)
        print ("--------\n")






if __name__ == "__main__":
    # ---test---
    text_name ="m_adam_300_1"
    test_model = Test(text_name=text_name)
    test_model.test_word_vec(word='1276241')                                           # a.印出詞向量  
    test_model.test_20relation(first='3224010')                                        # b.20個最相關的
    test_model.test_2similarity(first='1891321', second='1673639')                     # c.計算兩個詞的相似度/相關程度
    test_model.test_Correspondence(first='3002138', second='1944321', third='2687488') # d.尋找對應關係
    test_model.test_doesnt_match(string='breakfast cereal dinner lunch')               # e.尋找不合群的詞