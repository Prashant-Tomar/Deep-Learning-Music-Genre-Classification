import eyed3
import os

from audioFilesTools import getGenre
from config import rawDataPath

#Function to add genre data to file
def classifyGenres():
    #First identify all the files
    files = os.listdir(rawDataPath)
    files = [file for file in files if file.endswith(".mp3")]
    for index,filename in enumerate(files):
        
        #For every file check if genre is specified
        audiofile = eyed3.load(rawDataPath+filename)
        if audiofile.tag.genre is None:
            
            #Assign genre to file
            audiofile.tag.genre = filename.partition(".")[0].decode('utf-8')
            print(("{} has genre {}").format(filename, audiofile.tag.genre))
            audiofile.tag.save()
        else:
            print(("{} has genre {}").format(filename, audiofile.tag.genre))
