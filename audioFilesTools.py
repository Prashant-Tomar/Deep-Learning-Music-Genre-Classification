# -*- coding: utf-8 -*-
import eyed3

#Remove logs
eyed3.log.setLevel("ERROR")

def isMono(filename):
	audiofile = eyed3.load(filename)
	return audiofile.info.mode == 'Mono'

def getGenre(filename):
	audiofile = eyed3.load(filename)
	if not audiofile.tag.genre:
		#No genre
		return None
	else:
		return audiofile.tag.genre.name.encode('utf-8')