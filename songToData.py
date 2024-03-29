# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
import os
from PIL import Image
import eyed3

from sliceSpectrogram import createSlicesFromSpectrograms
from audioFilesTools import isMono, getGenre
from config import rawDataPath,spectrogramsPath,pixelPerSecond,tempDataPath

#Tweakable parameters
desiredSize = 128

#Define
currentPath = os.path.dirname(os.path.realpath(__file__)) 

#Remove logs
eyed3.log.setLevel("ERROR")

#Create spectrogram from mp3 files
def createSpectrogram(filename,newFilename):
	#Create temporary mono track if needed
	if isMono(rawDataPath+filename):
		#Copy the file as is
		command = 'cp "{}" "{}"'.format(rawDataPath+filename,tempDataPath+newFilename)
	else:
		#Creates a mono(single channel) output file which is a mix-down of input channels 1 and 2
		command = 'sox "{}" "{}" remix 1,2'.format(rawDataPath+filename,tempDataPath+newFilename)
		
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print(errors)

	filename.replace(".mp3","")
	#Create monochrome(-m) raw spectrogram(-r) with resolution of (pixelPerSecond by 200) pixels in size (-X, -Y)
	# Raw spectrogram : suppress the display of axes and legends
	command = "sox '{}' -n spectrogram -Y 200 -X {} -m -r -o '{}.png'".format(tempDataPath+newFilename,pixelPerSecond,spectrogramsPath+newFilename.replace(".mp3",""))
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print(errors)

	#Remove tmp mono track
	os.remove(tempDataPath+newFilename)

#Creates .png whole spectrograms from mp3 files
def createSpectrogramsFromAudio():
	genresID = dict()
	files = os.listdir(rawDataPath)
	files = [file for file in files if file.endswith(".mp3")]
	nbFiles = len(files)

	#Create path if not existing
	if not os.path.exists(os.path.dirname(spectrogramsPath)):
		try:
			os.makedirs(os.path.dirname(spectrogramsPath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#Rename files according to genre
	for index,filename in enumerate(files):
		print("Creating spectrogram for file {}/{}...".format(index+1,nbFiles))
		fileGenre = getGenre(rawDataPath+filename)
		genresID[fileGenre] = genresID[fileGenre] + 1 if fileGenre in genresID else 1
		fileID = genresID[fileGenre]
		newFilename = fileGenre+"_"+str(fileID)+".mp3"
		createSpectrogram(filename,newFilename)

#Whole pipeline .mp3 -> .png slices
def createSlicesFromAudio():
	print("Creating spectrograms...")
	createSpectrogramsFromAudio()
	print("Spectrograms created!")

	print("Creating slices...")
	createSlicesFromSpectrograms(desiredSize)
	print("Slices created!")