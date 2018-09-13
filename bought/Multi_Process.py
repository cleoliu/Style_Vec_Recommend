'''
Pipe https://blog.csdn.net/CityzenOldwang/article/details/78584175
'''
import sys
import os.path
root_path = (os.path.abspath('../')) #STYLE2VEC
sys.path.append(root_path)
from word2vec import word2vec_test
from bought import recommend_cos
from pic_320 import image_process

from multiprocessing import Process, Queue
import os, time, random  
  


def Style2vec_function(model_name, itemi):  
    print('Process(%s) is writing...' % os.getpid())

    Style2vec_test = word2vec_test.Test(text_name=root_path+'/word2vec/'+model_name)
    item_list = Style2vec_test.test_20relation(first=itemi)
    image_process.random_photo_join(item_list, save_name='Style2vec')
  

def CNN_function(model_name, itemi):  
    print('Process(%s) is writing...' % os.getpid())

    CNN_test = word2vec_test.Test(text_name=root_path+'/word2vec/'+model_name)
    item_list = CNN_test.test_20relation(first=itemi)
    image_process.random_photo_join(item_list, save_name='CNN')


def myfunction(model_name, itemi, A_user_buy_to_list):
    print('Process(%s) is writing...' % os.getpid())

    recommend = recommend_cos.recommend(read_table='user_bought_history.txt', itemi=itemi, load_model=model_name)
    # user A
    A_sorted_dict = recommend.cos_5(A_user_buy_to_list)
    A_centroids = recommend.centers(A_sorted_dict)
    # 計算
    item_bought_to_list = recommend.bought_itemi_user()
    to_A_distance_dict = recommend.center_distance(item_bought_to_list, A_centroids)
    join_buy_list = recommend.join_user_bought(to_A_distance_dict)
    # 每種類各一件
    item_list = recommend.category_unique(join_buy_list)
    image_process.random_photo_join(item_list, save_name='myfunction')

def run(itemi, A_user_buy_to_list):
    p1 = Process(target=myfunction, args=('m_adam_300_1', itemi, A_user_buy_to_list))
    p2 = Process(target=CNN_function, args=('CNNvec_adam_300.txt', itemi))
    p3 = Process(target=Style2vec_function, args=('m_adam_300_1', itemi))  # 把 v 傳值進去
    p1.start()  
    p2.start()  
    p3.start()  
    p1.join()  
    p2.join()
    p3.join()
