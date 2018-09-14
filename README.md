## Personalized collaborative filtering clothing recommendation system based on style vector space
* 服裝推薦系統的流程圖，分成三個階段：
	* 第一階段主要的訓練核心是利用 CNN 將圖片進行特徵向量化，大量的圖片特徵向量集結而成一個特徵向量空間。
	* 第二階段再利用此空間使用專家推薦集數據優化及調整，生成一個風格向量空間。
	* 第三階段則使用風格向量空間做推薦系統的實踐，使用購買記錄來尋找與用戶相近的消費者，推薦購買過的商品。
	
![](https://github.com/cleoliu/Style_Vec_Recommend/blob/master/Neural%20Networks%20Flow-Page-2.jpg?raw=true)
## Requirements
* windows 
* 4 CPU
* python 3.6

## install from pip
* GUI：
	* tkinter
* Math：
	* numpy
	* pandas
* Deep Learnin：
	* gensim
	* sklearn
	* tensorflow

## fashion_set
* Input：
	* dim_fashion_matchsets.txt（專家提供的搭配集數據）
* Run：
	* fashion_set_comb.py（專家搭配集排列組合）
	* del_symbol.py（normalization）

## pic_320
* image_process.py（圖片處理可調用的 funtion）

## cnn
* Run：
	* stely_CNN.py（16 VGGNet：4 max pooling +  1 average pooling +  1 Dense +  adam optimizer）
* Ouput：
	* CNNvec_1024.txt（No optimization & 1*1024 vector）
	* CNNvec_adam.txt（adam optimizer & 1*300 vector）
  
## style_vec
* Train：
	* style_vec_train.py
* Test：
	* style_vec_test.py
		* 印出詞向量
		* 20個最相關  
		* 計算兩者相似度  
		* 尋找對應關係  
		* 不和群的詞
* 可視化：
	* vsualize .py

## bought
* Run：
	* MAIN：GUI .py（GUI view）
	* Multi_Process.py（3-Process）
	* recommend_cos.py（recommend）
* Ouput：
	* result_CNN.png
	* result_Style2vec.png
	* result_myfunction.png
![enter image description here](https://github.com/cleoliu/Style_Vec_Recommend/blob/master/view.PNG?raw=true)