#!/home/icarus/anaconda2/bin/python
import cgitb; cgitb.enable()
import collections
import time
#import cv2

import base64

import cgi

import uuid

import os

from MsTaktUtil import objToStr

from Microsoft import getResponse



#TEMP_FRAME_STORE = "/home/icarus/projects/AgeGender/tmp/"
import os


TEMP_FRAME_STORE = "/home/icarus/projects/AgeGender/cgi-bin/static/"


def appendResults(dirID, result):
    with open(dirID + ".json", "a") as resultFile:
        resultFile.write(result)

def get_emotion(nets, data, companyId, videoId, userId, timestamp, cache):
    print ("In get Emotion [Driver.py]")
    skip =["companyId","campaignId", "participantId"]
    orderedData = collections.OrderedDict(sorted(data.items()))
    result = ""
    try:
        for key in orderedData:
            if (key in skip):
                continue
            f = data[key]
            #frame = read64(f)
            #if (frame is "Error"):
            #    print ("Error in decoding base64")
            #    continue
            #img_name = str(userId) + ".jpeg"

            img_name = str(uuid.uuid4())

            dir_path = os.getcwd() + "/imgs/"

            path = dir_path + img_name
            #print ("saving image to + " + path + "[Driver.py]")
            #cv2.imwrite(path, frame)

            with open(path, "wb") as fh:
                fh.write(base64.decodebytes(f.encode()))

            # print "Created image: "  + path
            ####### Change this to swap models
            #result = analyze_data(nets, path, companyId, videoId, userId, timestamp, cache)
            result = analyze_data_microsoft(nets, path, companyId, videoId, userId, timestamp, cache)
            os.remove(path)
    except Exception as e:
        print ("Error: " + str(e) )
    return result

'''def get_emotion_image(nets, path, companyId, videoId, userId,  timestamp , cache):
    emotions = {}
    emotions['userId'] = userId
    emotions['videoId'] = videoId
    emotions['report'] = []
    result = analyze_data(nets, path, companyId,  videoId, userId, timestamp, cache)
    return result '''


def analyze_data_microsoft(nets, path, companyId, videoId, userId, timestamp, cache):
    print ("In Analyze In MS Service")
    emotions = []
    results = getResponse(path)
    metricsHash = objToStr(results, timestamp, companyId, videoId, userId)
    emotions.append(metricsHash)
    jsonStr = "["
    for i in emotions:
        jsonStr = jsonStr + str(i)
    jsonStr = jsonStr + "]"
    # print jsonStr
    return jsonStr




if __name__=="__main__":
    args = cgi.FieldStorage()
    action = None
    fileId = None
    if args.has_key("companyId"):
        companyId = args["companyId"].value
    if args.has_key("participantId"):
        participantId = args["participantId"].value
    if args.has_key("campaignId"):
        campaignId = args["campaignId"].value



