import numpy as np
import cv2
import os
from os import listdir
from os.path import isfile, join
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#read from folder result_lip and write to same folder with name concate-output.jpg
def concatenate_images(outname,frames): 
	# concate_seq= np.array([0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,10,11,12,13,14,14])
	#read image
	print("[INFO]: Concatenating Images from {} to {} ".format(frames[0],frames[-1]))
	path="temporary_images/"
	row = frames[0:5]
	im_1 = cv2.imread(path + str(row[0]) , cv2.IMREAD_COLOR)
	im_2 = cv2.imread(path + str(row[1]) , cv2.IMREAD_COLOR)
	im_3 = cv2.imread(path + str(row[2]) , cv2.IMREAD_COLOR)
	im_4 = cv2.imread(path + str(row[3]) , cv2.IMREAD_COLOR)
	im_5 = cv2.imread(path + str(row[4]) , cv2.IMREAD_COLOR)
	layer1 = np.concatenate((im_1, im_2, im_3, im_4, im_5), axis=1)

	row = frames[5:10]
	im_6 = cv2.imread(path + str(row[0]) , cv2.IMREAD_COLOR)
	im_7 = cv2.imread(path + str(row[1]) , cv2.IMREAD_COLOR)
	im_8 = cv2.imread(path + str(row[2]) , cv2.IMREAD_COLOR)
	im_9 = cv2.imread(path + str(row[3]) , cv2.IMREAD_COLOR)
	im_10 = cv2.imread(path + str(row[4]) , cv2.IMREAD_COLOR)
	layer2 = np.concatenate((im_6, im_7, im_8, im_9, im_10), axis=1)

	row = frames[10:15]
	im_11 = cv2.imread(path + str(row[0]) , cv2.IMREAD_COLOR)
	im_12 = cv2.imread(path + str(row[1]) , cv2.IMREAD_COLOR)
	im_13 = cv2.imread(path + str(row[2]) , cv2.IMREAD_COLOR)
	im_14 = cv2.imread(path + str(row[3]) , cv2.IMREAD_COLOR)
	im_15 = cv2.imread(path + str(row[4]) , cv2.IMREAD_COLOR)
	layer3 = np.concatenate((im_11, im_12, im_13, im_14, im_15), axis=1)

	row = frames[15:20]
	im_16 = cv2.imread(path + str(row[0]) , cv2.IMREAD_COLOR)
	im_17 = cv2.imread(path + str(row[1]) , cv2.IMREAD_COLOR)
	im_18 = cv2.imread(path + str(row[2]) , cv2.IMREAD_COLOR)
	im_19 = cv2.imread(path + str(row[3]) , cv2.IMREAD_COLOR)
	im_20 = cv2.imread(path + str(row[4]) , cv2.IMREAD_COLOR)
	layer4 = np.concatenate((im_16, im_17, im_18, im_19, im_20), axis=1)

	row = frames[20:25]
	im_21 = cv2.imread(path + str(row[0]) , cv2.IMREAD_COLOR)
	im_22 = cv2.imread(path + str(row[1]) , cv2.IMREAD_COLOR)
	im_23 = cv2.imread(path + str(row[2]) , cv2.IMREAD_COLOR)
	im_24 = cv2.imread(path + str(row[3]) , cv2.IMREAD_COLOR)
	im_25 = cv2.imread(path + str(row[4]) , cv2.IMREAD_COLOR)
	layer5 = np.concatenate((im_21, im_22, im_23, im_24, im_25), axis=1)

	row = frames[25:30]
	im_26 = cv2.imread(path + str(row[0]) , cv2.IMREAD_COLOR)
	im_27 = cv2.imread(path + str(row[1]) , cv2.IMREAD_COLOR)
	im_28 = cv2.imread(path + str(row[2]) , cv2.IMREAD_COLOR)
	im_29 = cv2.imread(path + str(row[3]) , cv2.IMREAD_COLOR)
	im_30 = cv2.imread(path + str(row[4]) , cv2.IMREAD_COLOR)
	layer6 = np.concatenate((im_26, im_27, im_28, im_29, im_30), axis=1)

	output = np.concatenate((layer1, layer2, layer3, layer4, layer5,layer6), axis=0)
	# cv2.imshow('concat',output)
	# cv2.waitKey(0) 
	output_path = "concatenated_images/"
	cv2.imwrite(output_path+"{}_concate_output.jpg".format(outname), output)
	print("[INFO] concate done")


def concatFrameSet(frameSet):
	pass

#frameset = [ending frame number, starting frame number]
def upScaleFrames(frameSet):
	#if less than 30
	upScaleFactor = 30 - (frameSet[1]-frameSet[0]+1)
	print("\n \n")
	print("[INFO]: Upscaling frameSet {} -> {} by factor {}".format(frameSet[0],frameSet[1],upScaleFactor))

	#upscaling algorithm
	#reading the frames
	frames = [f for f in listdir("pictures") if isfile(join("pictures", f))]
	try:
		frames.remove(".DS_Store")
	except:
		pass
	frames.sort(key=natural_keys)
	frames = frames[frameSet[0]-1:frameSet[1]]
	print("[INFO]: Old frames before upscaling:".format(frames))
	# now each of these frames are going undergo the facial landmark AREA and VERTICAL height calculation
	
	new_path = "temporary_images"
	for each_frame in frames:
		if(each_frame != ".DS_Store"):
			frame_read = cv2.imread('pictures'+ "/"+each_frame)
			cv2.imwrite(new_path + "/"+each_frame,frame_read)

	#repeating boundry frames
	print("[INFO]: Reading boundry frame for upscaling: {} ".format(frameSet[1]))
	boundry_frame = cv2.imread('pictures'+ "/"+str(frameSet[1])+".jpg")
	framenumber = 1 #keep incrementing this 
	for k in range(upScaleFactor):
		print("[INFO]: Writing duplicate frames while upscaling upscaling: {} ".format(frameSet[1]+framenumber))
		cv2.imwrite(new_path + "/"+str(frameSet[1]+framenumber)+".jpg",boundry_frame)
		frames.append(str(frameSet[1]+framenumber)+".jpg")
		framenumber+=1

	print("[INFO]: New frames after upscaling:".format(frames))

	concatenate_images(str(frameSet[0])+"_"+str(frameSet[1]-1),frames) #-1 here coz that frame is not included


def downScaleFrames(frameSet):
	#if more than 30
	downScaleFactor = (frameSet[1]-frameSet[0]+1) - 30
	print("[INFO]: Downscaling frameSet {} -> {} by factor {}".format(frameSet[0],frameSet[1],downScaleFactor))
	
	#upscaling algorithm
	#reading the frames
	frames = [f for f in listdir("pictures") if isfile(join("pictures", f))]
	try:
		frames.remove(".DS_Store")
	except:
		pass
	frames.sort(key=natural_keys)
	frames = frames[frameSet[0]-1:frameSet[1]-downScaleFactor]
	print(frames)
	# now each of these frames are going undergo the facial landmark AREA and VERTICAL height calculation
	
	new_path = "temporary_images"
	for each_frame in frames:
		if(each_frame != ".DS_Store"):
			frame_read = cv2.imread('pictures'+ "/"+each_frame)
			cv2.imwrite(new_path + "/"+each_frame,frame_read)

	concatenate_images(str(frameSet[0])+"_"+str(frameSet[1]-1),frames) #-1 here coz that frame is not included


def zeroScaleFrames(frameSet):
	#zero algorithm - just shifting frames
	#reading the frames
	frames = [f for f in listdir("pictures") if isfile(join("pictures", f))]
	try:
		frames.remove(".DS_Store")
	except:
		pass
	frames.sort(key=natural_keys)
	frames = frames[frameSet[0]-1:frameSet[1]]
	print(frames)
	# now each of these frames are going undergo the facial landmark AREA and VERTICAL height calculation
	
	new_path = "temporary_images"
	for each_frame in frames:
		if(each_frame != ".DS_Store"):
			frame_read = cv2.imread('pictures'+ "/"+each_frame)
			cv2.imwrite(new_path + "/"+each_frame,frame_read)

	concatenate_images(str(frameSet[0])+"_"+str(frameSet[1]-1),frames) #-1 here coz that frame is not included
	




if __name__ == "__main__":
	directory = "pictures"
	folders = []
	for x in os.walk(directory):
		folders = x[1]
		break

	# the folders list contains a list of all the subfolders print(folders)
	#we need to call the concat function on each of these sub folders
	for eachfolder in folders:
		concate_images(eachfolder)
