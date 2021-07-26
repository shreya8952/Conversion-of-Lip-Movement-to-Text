# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import dlib
# import faceAlignment as fa
import sys
import select
import glob
import os
# import predict as pred
# import concate as conc
import time
import pandas as pd 
import matplotlib.pyplot as plt
from frechetdist import frdist
from os import listdir
from os.path import isfile, join
import numpy as np
import re
import math
import similarity
import slidingWindow
import concate
import requests
import random
import json


def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False

			
def clean_pictures():
	#clean folder
	files = glob.glob('pictures/*')
	for f in files:
	    os.remove(f)
	# files = glob.glob('result_lip/*')
	# for f in files:
	#     os.remove(f)



def clean_temporary_pictures():
	#clean folder
	files = glob.glob('temporary_images/*')
	for f in files:
	    os.remove(f)
	files = glob.glob('concatenated_images/*')
	for f in files:
	    os.remove(f)



def processImages():

	print("[INFO]:Processing images")
	#this tells us how to process the frames for the CNN model
	#also returns vertical_distances which is already calculated in the analyse window function
	#so we don't have to recalculate it
	clean_temporary_pictures()
	try:
		framesToProcess,vertical_distances = slidingWindow.analyseWindowSize()

		#each set is [start number,ending number]
		for frameSet in framesToProcess:
			if((frameSet[1]-frameSet[0]+1)<30):
				#we need to upscale to 30 #need to duplicate a few frames
				#these functions are in the concat script
				concate.upScaleFrames(frameSet)

			elif((frameSet[1]-frameSet[0]+1)>30):
				#we need to downscale to 30 #need to delete some boundry frames
				#these functions are in the concat script
				concate.downScaleFrames(frameSet)
			else:
				concate.zeroScaleFrames(frameSet)
				#it's perfect 30, we don't need to upscale or downscale
	
	except:
		pass
	#concat logic to come here


	#CNN model runs here



	#frechet distance model runs here
	# result = similarity.similarityIndex(vertical_distances)
	# outputfile = open("result_lip/text_.txt",'w')
	# outputfile.write(result)
	# outputfile.close()



# construct the argument parse and parse the arguments
# n is the max iteration number the program waits for "press Enter"
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=1000,
	help="# of frames to loop over for FPS test")
args = vars(ap.parse_args())

while True:
	clean_pictures()
	print("[INFO] sampling THREADED frames from webcam...")
	vs = WebcamVideoStream(src=0).start()
	fps = FPS().start()
	record_index=1
	triggered=heardEnter()
	if triggered==True:
		print("Triggered: Start speaking")
		triggered=False
	# loop over some frames...this time using the threaded stream
		while fps._numFrames < 1000:
			# grab the frame from the threaded video stream and resize it
			# to have a maximum width of 400 pixels
			frame = vs.read()
			# frame = cv2.resize(frame, (512, 256))
			triggered=heardEnter()

			print("frames: "+str(fps._numFrames)+" heardEnter: "+str(triggered)+ " record_index: "+str(record_index))

			if triggered==True:
				print("Triggered: Stop speaking")
				# sys.exit(0)
				break
				# record_index=1
				
			# if record_index>0:
				# if record_index%2==0:
			cv2.imwrite("pictures/"+str(record_index)+".jpg", frame)
			# else:
			# 	cv2.imwrite("dump.jpg", frame)
			record_index=record_index+1

			key= 0xFF & cv2.waitKey(35)
			# update the FPS counter
			fps.update()
		
		# displayText()

	# stop the timer and display FPS information
	fps.stop()
	# print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	# print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	# do a bit of cleanup
	vs.stop()

	processImages()
	print(displayText())


