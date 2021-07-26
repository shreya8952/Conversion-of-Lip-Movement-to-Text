from os import listdir
from os.path import isfile, join
import cv2
import dlib
import re
import numpy as np
import math

detector = dlib.get_frontal_face_detector() #Face detector
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") #Landmark identifier. Set the filename to whatever you named the downloaded file


def verticalDistanceCalculate(frame_path):
    img = cv2.imread(frame_path)
    dets = detector(img)
    # output face landmark points inside retangle
    # shape is points datatype
    # http://dlib.net/python/#dlib.point
    for k, d in enumerate(dets):
        shape = predictor(img, d)

    vec = np.empty([68, 2], dtype=int)
    for b in range(68):
        vec[b][0] = shape.part(b).x
        vec[b][1] = shape.part(b).y
    vertical_distance = (math.sqrt( pow(abs(vec[66][0]-vec[62][0]), 2)+pow(abs(vec[66][1]-vec[62][1]), 2)))
    return vertical_distance

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


#returns a list of list which contains frames which should be processed
def analyseWindowSize():
    print("[INFO]: Analysing window sizes")
    frames = [f for f in listdir("pictures") if isfile(join("pictures", f))]
    try:
        frames.remove(".DS_Store")
    except:
        pass
    frames.sort(key=natural_keys)
    # now each of these frames are going undergo the facial landmark AREA and VERTICAL height calculation
    path = "pictures"
    vertical_distances = []
    # try:
    for each_frame in frames:
        if(each_frame != ".DS_Store"):
            v = verticalDistanceCalculate(path + "/"+each_frame)
            vertical_distances.append(v)
    
    v_max = max(vertical_distances)
    new_vertical_distances = [i/v_max for i in vertical_distances]
    
    # print(new_vertical_distances)
    # new_vertical_distances = [0.020777048221211104, 0.014691591690258264, 0.020777048221211104, 0.020777048221211104, 0.03285139771708852, 0.03285139771708852, 0.014691591690258264, 0.03285139771708852, 0.029383183380516528, 0.22232412465600274, 0.6030714964849961, 0.706572395418632, 0.6772489136836541, 0.7359006398833362, 0.7058082853265872, 0.837549590041159, 0.4556762419419314, 0.25018879122384174, 0.2938318338051653, 0.22037387535387398, 0.2497570587343905, 0.19155491976677386, 0.19155491976677386, 0.17691019085124388, 0.11753273352206611, 0.16425698858544258, 0.04407477507077479, 0.014691591690258264, 0.020777048221211104, 0.029383183380516528, 0.04155409644242221, 0.04155409644242221, 0.23552413180621065, 0.8541363406443014, 1.0, 0.9412943038945661, 0.8239088631680209, 0.9706462341175618, 0.8966686552539431, 0.9412943038945661, 0.9266190816686277, 0.8679237315066902, 0.5014548228386626, 0.36758350665146056, 0.13303802104754786, 0.07491271271436449, 0.07491271271436449, 0.020777048221211104, 0.06570279543417704, 0.04155409644242221, 0.03285139771708852, 0.020777048221211104, 0.07345795845129133, 0.014691591690258264, 0.03285139771708852, 0.03285139771708852, 0.03285139771708852, 0.014691591690258264, 0.020777048221211104, 0.12114996869476305, 0.22232412465600274, 0.32354874470585393, 0.30991946622470046, 0.29529733832677757, 0.3529041426632936, 0.35382038170248775, 0.32454786827202187, 0.3529041426632936, 0.3379066088759401, 0.338225840509608, 0.338225840509608, 0.08936546344394365, 0.338225840509608, 0.16227393413601093, 0.03285139771708852, 0.020777048221211104, 0.014691591690258264, 0.03285139771708852, 0.014691591690258264, 0.020777048221211104, 0.020777048221211104, 0.014691591690258264, 0.03285139771708852, 0.03285139771708852, 0.058766366761033056, 0.3379066088759401, 0.3529041426632936, 0.08814955014154958, 0.0, 0.11844739893962328, 0.10388524110605551, 0.19155491976677386, 0.2971190541766813, 0.020777048221211104, 0.08814955014154958, 0.26485643578703416, 0.23689479787924655, 0.28259840863937696, 0.30852342549542355, 0.07345795845129133, 0.029383183380516528, 0.014691591690258264, 0.0, 0.014691591690258264, 0.03285139771708852, 0.03285139771708852, 0.0, 0.014691591690258264, 0.020777048221211104, 0.020777048221211104, 0.014691591690258264, 0.3088730272228759, 0.5297128715740683, 0.5443824533891167, 0.6030714964849961, 0.6759728901032522, 0.632421403359122, 0.6759728901032522, 0.6612848458211911, 0.6617742635611755, 0.6759728901032522, 0.6759728901032522, 0.7200378914172672, 0.5291013113875882, 0.060574984347381525, 0.060574984347381525, 0.03285139771708852, 0.014691591690258264, 0.014691591690258264, 0.014691591690258264, 0.029383183380516528, 0.046458892194419114, 0.014691591690258264, 0.020777048221211104, 0.03285139771708852, 0.0, 0.03285139771708852, 0.03285139771708852]
    # for i in range(0,len(new_vertical_distances)):
    #     print("Frame {} - Distance {}".format(i+1,new_vertical_distances[i]))

    # print("Total frames: ", len(new_vertical_distances))
    ranges = [0.01,0.02,0.03,0.00,0.0] #the numbers have to be this small to be considered as word boundries
    current_difference = 0

    index_val = 1
    framesToProcess = []
    print("New distances unsplit:",new_vertical_distances)
    #lets try to find the distances now
    #the number 15 was decided to give a healthy gap between the words. Around 15 frames will be taken to speak for any acceptable speed
    for k in range(1,len(new_vertical_distances)-1):
        prev = new_vertical_distances[k-1]
        current = new_vertical_distances[k]
        nextt = new_vertical_distances[k+1]
        if(round(prev,2) in ranges and round(current,2) in ranges and round(nextt,2) in ranges):
            if(k-current_difference>15):
                print("WORD BOUNDRY AT FRAME:{} | Frames to Process: {} to {} ".format(k+1,current_difference+1,k+1))
                framesToProcess.append([current_difference+1,k+1])
                current_difference = k
        
        index_val = k
    
    # if(current_difference!=index_val and (index_val-current_difference)>15):
    #     print("LAST WORD BOUNDRY AT FRAME: {} | Frames to Process: {} to {} ".format(index_val+1,current_difference+1,index_val+1))
    #     framesToProcess.append([current_difference+1,index_val+1])
    

    #new_vertical_distances is returned too as it is used by the frechet model
    print("[INFO]: Frames to process are: ",framesToProcess)
    return framesToProcess, new_vertical_distances 



# analyseWindowSize()