# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings(action='ignore',category=UserWarning,module='gensim')
import numpy as np
import pandas as pd
from gensim import matutils
from gensim.models import word2vec
from gensim.models.keyedvectors import KeyedVectors
from sklearn import cluster
from sklearn.cluster import KMeans

import sys
import os.path
root_path = (os.path.abspath('../')) #STYLE2VEC
sys.path.append(root_path)
from pic_320 import image_process


class recommend:
    def __init__(self, read_table, itemi, load_model):
        '''初始化'''
        self.df = pd.read_table(read_table,sep=' ', header=None, names=['user_id','item_id','create_at']).applymap(str)
        self.itemi = itemi
        self.model = KeyedVectors.load_word2vec_format(load_model)
        self.vocab = list(self.model.wv.vocab)


    def buy_list(self, user):
        '''2. 找出{user}買的商品'''
        user_buy = self.df.loc[self.df['user_id']== user,['item_id']]
        user_buy_to_list = user_buy['item_id'].tolist()
        while self.itemi in user_buy_to_list:
            user_buy_to_list.remove(self.itemi) # 減掉itemi
        #print ("--------user %s buy--------" %(user))
        #print(user_buy_to_list)
        return user_buy_to_list


    def cos_5(self, user_buy_to_list):
        '''3. 找出最接近 il 的 5件商品'''
        # 如果買過的商品不在model裡:取vocab&user_buy_to_list交集
        in_model = [val for val in self.vocab if val in user_buy_to_list]

        # 找出最接近 il 的商品
        similarity_dict = {}
        for i in in_model :
            y1 = self.model.similarity(self.itemi, i) # 比較COS相似度
            similarity_dict.update({i:y1}) # 存入字典{itemid,similarity}    
        sorted_dict = sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True) # 依similarity排序大到小
        #print ("--------接近 %s 的商品--------" %(self.itemi))
        #print(sorted_dict)    
        return sorted_dict


    def centers(self, sorted_dict):
        '''4. 計算{i1~i6}共六點的中心點ac'''
        # 獲取詞的向量
        wordvector = [self.model[self.itemi]] # list:先加入itemi(i1)
        for i in sorted_dict:
            wordvector.append(self.model[i[0]]) # 加入i2~i6相似的商品的vector

        # 計算中心點
        estimator = KMeans(n_clusters=1)
        res = estimator.fit_predict(wordvector[:6]) # [:6]:取vector前六個
        lable_pred = estimator.labels_
        centroids = estimator.cluster_centers_ # 值:中心點
        #print ("--------中心點--------")
        #print(centroids)
        return centroids


    def bought_itemi_user(self):
        '''5. 找出買過itemi的人'''
        item_bought = self.df.loc[self.df['item_id']== self.itemi,['user_id']]
        item_bought_to_list = item_bought['user_id'].tolist()
        #print ("--------買過 %s 的人--------" %(self.itemi))
        #print(item_bought_to_list)
        return item_bought_to_list


    def center_distance(self, item_bought_to_list, A_centroids):
        '''6. 計算ac,bc...zc距離'''
        # dict:收集中心點
        all_center_dict = {}
        for i in item_bought_to_list:
            user_buy_to_list = recommend.buy_list(self, user=i)
            # 如果user_buy_to_list為空list:pass, 情況:買過的商品只有i
            if user_buy_to_list == []:
                #print("user_buy_to_list:N/A")
                pass
            else:
                # 如果sorted_dict為空list:pass, 情況:買過的商品不在model
                sorted_dict = recommend.cos_5(self, user_buy_to_list)
                if sorted_dict == []:
                    #print("sorted_dict:N/A")
                    pass
                else:
                    centroids = recommend.centers(self, sorted_dict)
                    all_center_dict.update({i:centroids}) #{user:center}

        # 計算與A中心點的距離
        distance_dict = {}
        for key in all_center_dict :
            distance = np.dot(matutils.unitvec(A_centroids[0]), matutils.unitvec(all_center_dict[key][0]))
            distance_dict.update({key:distance}) #{user:useri2A_distance}
        to_A_distance_dict = sorted(distance_dict.items(), key=lambda item: item[1], reverse=True) #[('9531708', 1.0), ('2953949', 0.9984370601131513), ('3590311', 0.9982105339905234)]
        #print ("--------計算與A中心點的距離 user:useri2A_distance--------") 
        #print(to_A_distance_dict)
        return to_A_distance_dict


    def join_user_bought(self, to_A_distance_dict):
        '''7. 總和與a最接近的五個人他們買過的5件商品'''
        join_buy_list = []
        for i in to_A_distance_dict[1:6] :
            user_buy_to_list = recommend.buy_list(self, [i][0][0])
            sorted_dict = recommend.cos_5(self, user_buy_to_list)
            join_buy_list.extend(sorted_dict)
        #print ("--------總和與a最接近的五個人他們買過的5件商品(join_buy_list)--------") 
        #print(join_buy_list)
        return join_buy_list


    def category_unique(self, join_buy_list):
        '''輸出每種類各一種商品,帶.jpg'''
        # 輸出單品名稱.jpg
        img_dirs = [self.itemi+'.jpg']
        for i in range(len(join_buy_list)):
            img_dirs.append(join_buy_list[i][0]+'.jpg')
        #return img_dirs
        
        # 輸出每種類各一種商品
        dc = pd.read_table('dim_items.txt',sep=' ', header=None, names=['item_id','cat_id', 'terms']).applymap(str)
        cat_list = []
        item_list = []
        for i in img_dirs:
            cat_id = dc.loc[dc['item_id']== i[:-4],['cat_id']] #i[:-4]:去掉".jpg"
            cat_id = cat_id['cat_id'].to_string(index=False)
            # 如果分類已存在cat_list:pass不存
            if (cat_id in cat_list) == True:
                pass
            else:
                cat_list.append(cat_id)
                item_list.append(i)
        #print(item_list)
        return item_list

if __name__ == "__main__":
    itemi = '1014695'
    recommend = recommend(read_table='user_bought_history.txt', itemi=itemi, load_model='m_adam_300_1')

    # user A
    A_user_buy_to_list = recommend.buy_list(user='1446156')
    A_sorted_dict = recommend.cos_5(A_user_buy_to_list)
    A_centroids = recommend.centers(A_sorted_dict)

    item_bought_to_list = recommend.bought_itemi_user()
    to_A_distance_dict = recommend.center_distance(item_bought_to_list, A_centroids)
    join_buy_list = recommend.join_user_bought(to_A_distance_dict)
    # 每種類各一件
    item_list = recommend.category_unique(join_buy_list)
    image_process.random_photo_join(item_list, save_name=itemi)
    # 不處理每種類各一件:return img_dirs
    #img_dirs = recommend.category_unique(join_buy_list)
    #image_process.random_photo_join(img_dirs, save_name=itemi)CLE