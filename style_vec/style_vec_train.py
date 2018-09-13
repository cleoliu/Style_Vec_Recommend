# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import logging
from gensim import utils
from gensim.models import word2vec
from gensim.models.word2vec import Word2Vec



def regular_train(text_name):
    '''正規訓練'''
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus(text_name)  #加載語料
    model = word2vec.Word2Vec(sentences, size=300, sg=1, window=2, hs=0, iter=1)  #訓練skip-gram模型; 默認window=5
    # 保存模型，以便重用
    model.save(text_name+"300.model")
    # 以一種C語言可以解析的形式存儲詞向量
    model.wv.save_word2vec_format(text_name+"300.model.bin", binary=True)
    model.wv.save_word2vec_format(text_name+"300.model.txt", binary=False)


def join_CNN_train(intersect_model, model_sv):
    '''載入cnn當預訓練'''
    sentences = word2vec.LineSentence("Combination_fashion_str")
    epochs = 1  
    model = Word2Vec(  
        size = 300,    #向量维度:這表示的是訓練出的詞向量會有幾維
        min_count = 1, #若這個詞出現的次數小於min_count，那他就不會被視為訓練對象
        workers = 4,   #執行緒數目,別超過4
        sample = 1e-5, #負採樣:高頻詞彙的隨機降採樣的配置閾值
        window = 5,    #窗口大小:往左往右看幾個字
        sg = 1,        #語言模型:sg=1則採用skip-gram算法
        hs = 0,        #0=negative sampling
        )

    #model=Word2Vec.load_word2vec_format('data/ws2v_chat_ltp5')  
    #model.reset_from(model1)  
    model.build_vocab(sentences)
    model.intersect_word2vec_format(intersect_model, binary=False)  
    for epoch in range(epochs):  
        print('epoch' + str(epoch+1))  
        try:  
            model.train(sentences, epochs=model.iter, total_examples=model.corpus_count)  #訓練  
            model.alpha *= 0.9  #更新學習率  
            model.min_alpha = model.alpha  
            model.save((model_sv + str(epoch+1))+".model")
            model.wv.save_word2vec_format(model_sv + str(epoch+1))  
        except KeyboardInterrupt:  
            print ('saving the model' + model_sv + str(epoch+1))  
            model.save((model_sv + str(epoch+1))+".model")
            model.wv.save_word2vec_format(model_sv + str(epoch+1))



if __name__ == "__main__":
    # ---train&save---
    regular_train(text_name="m_adam_300_1")
    join_CNN_train(intersect_model="CNNvec_adam_300.txt", model_sv='m_adam_300_')