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
	* GUI .py（view）
	* Multi_Process.py（3-Process）
	* recommend_cos.py（recommend）
* Ouput：
	* result_CNN.png
	* result_Style2vec.png
	* result_myfunction.png
