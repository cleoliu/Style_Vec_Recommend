#-*- coding: utf-8 -*-

from keras import backend as K
from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D, AveragePooling2D
from keras.optimizers import SGD
import cv2
import cv2, numpy as np
import numpy as np

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.layers import merge, Input

from os import listdir
import h5py as h5py


def VGG_16(weights_path=None):

	model = Sequential()
	model.add(ZeroPadding2D((1,1),input_shape=(64,64,3))) 

	model.add(Conv2D(64, (3, 3), activation='relu')) #1
	model.add(ZeroPadding2D((1,1)))
	model.add(Conv2D(64, (3, 3), activation='relu')) #2

	model.add(MaxPooling2D((2,2), strides=(2,2))) #3M
	model.add(ZeroPadding2D((1,1)))
	model.add(Conv2D(128, (3, 3), activation='relu')) #4
	model.add(ZeroPadding2D((1,1)))
	model.add(Conv2D(128, (3, 3), activation='relu')) #5

	model.add(MaxPooling2D((2,2), strides=(2,2))) #6M
	model.add(ZeroPadding2D((1,1)))
	model.add(Conv2D(256, (3, 3), activation='relu')) #7
	model.add(ZeroPadding2D((1,1)))
	model.add(Conv2D(256, (3, 3), activation='relu')) #8

	model.add(MaxPooling2D((2,2), strides=(2,2))) #9M
	model.add(ZeroPadding2D((1,1)))
	model.add(Conv2D(512, (3, 3), activation='relu')) #10
	model.add(ZeroPadding2D((1,1)))
	model.add(Conv2D(512, (3, 3), activation='relu')) #11

	model.add(MaxPooling2D((2,2), strides=(2,2))) #12M
	model.add(ZeroPadding2D((1,1)))
	model.add(Conv2D(512, (3, 3), activation='relu')) #13
	model.add(ZeroPadding2D((1,1)))
	model.add(Conv2D(512, (3, 3), activation='relu')) #14

	model.add(AveragePooling2D(pool_size=(3, 3)))

	model.add(Dense(300, activation='relu'))

	model.summary()

	if weights_path:
		model.load_weights(weights_path)

	return model



if __name__ == "__main__":
	# 取得所有檔案與子目錄名稱
	mypath = "all_img"
	files = listdir(mypath)

	# write : file count & 1024
	fp = open("CNNvec_adam.txt", "a")
	fp.write(str(len(files)))
	fp.write(" 300")
	fp.write('\n')
	
	model = VGG_16()
	#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) #categorical_crossentropy:转化成one-hot 向量

	# file
	for f in files:
		# write : file name
		fp.write(str(f[:-4]))
		print(f)
		# input img
		img = image.load_img("all_img/"+f, target_size=(64, 64))
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)
		x = preprocess_input(x)
		
		out = model.predict(x)
		features = model.predict(x) # get 1024 features

		# write img vec
		for  i  in  range(300):
			fe = features[0][0][0][i]
			fp.write(" ")
			fp.write(str(fe))

		fp.write('\n')
	fp.close()

	#(1,1,1,1024)
	print(features.shape) 

	
	


#http://msrc.cm.nsysu.edu.tw/ezfiles/135/1135/img/2968/VGG16.html
#https://github.com/f496328mm/cifar10_vgg16_kaggle