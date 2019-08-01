# -*- coding: utf-8 -*-

import numpy as np

import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

def createModel(nbClasses,imageSize):
	print("[+] Creating model...")
	#None as don't know number of rows, (iagesize X imagesize) in the png files and 1 to store class label
	convnet = input_data(shape=[None, imageSize, imageSize, 1], name='input')

	# Double number of convolutional filters to detect specific details in the image but not too much as to overfit
	#TODO: Take depth as a hyperparameter
	convnet = conv_2d(convnet, 64, 2, activation='elu', weights_init="Xavier")
	convnet = max_pool_2d(convnet, 2)

	convnet = conv_2d(convnet, 128, 2, activation='elu', weights_init="Xavier")
	convnet = max_pool_2d(convnet, 2)

	convnet = conv_2d(convnet, 256, 2, activation='elu', weights_init="Xavier")
	convnet = max_pool_2d(convnet, 2)

	convnet = conv_2d(convnet, 512, 2, activation='elu', weights_init="Xavier")
	convnet = max_pool_2d(convnet, 2)

	#Creates a fully connected neural network of 1024 neurons with "elu" activation function
	convnet = fully_connected(convnet, 1024, activation='elu')
	#Dropout 0.5 of the neurons (To consider while testing too)
	convnet = dropout(convnet, 0.5)
	#This is the output layer
	convnet = fully_connected(convnet, nbClasses, activation='softmax')
	#TODO: Try "adam" Optimizer
	#TODO: Try "softmax_categorical_crossentropy" loss
	#TODO: Try "binary_crossentropy" loss
	#TODO: Try "weighted_crossentropy" loss
	#TODO: Try "mean_square" loss
	#TODO: Try "hinge_loss" loss
	#TODO: Try "roc_auc_score" loss
	#TODO: Try "weak_cross_entropy_2d" loss
	#categorical cross entropy = -p(log (Softmax(q)))
	convnet = regression(convnet, optimizer='rmsprop', loss='categorical_crossentropy')
	#The Deep Neural net is prepared
	model = tflearn.DNN(convnet)
	print("    Model created! ✅")
	return model