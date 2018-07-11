#!/home/icarus/anaconda2/bin/python
from flask import Flask
from flask import g
from flask_cors import CORS, cross_origin
from flask import request, Response, stream_with_context, render_template, redirect, url_for, send_file
#import cv2
from Driver import get_emotion



import time


app = Flask(__name__, template_folder='.', static_url_path = "", static_folder = "static")

nets = {}
ageGenderCache = {}
UPLOAD_FOLDER = "/home/icarus/projects/AgeGender/cgi-bin/static/"


@app.route('/frame' ,methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def processFrame():
    print ("In Frame")

    content = request.get_json(force=True)

    companyId = content["companyId"]

    #companyId = "abz"

    participantId = content["participantId"]

    #participantId = "123"

    campaignId = content["campaignId"]

    #campaignId = "567"

    image = content["image"]



    timestamp = 0
    if "timestamp" in content:
        timestamp = content["timestamp"]
    if(companyId is None or campaignId is None or participantId is None or image is None):
        return "No POST data found or missing parameters"
    start = image.find(",")
    image64 = image[start + 1:]
    data = {}
    data[time.time()] = image64
    print ("Getting Emos")
    res = get_emotion(nets, data, companyId, campaignId, participantId, timestamp, ageGenderCache)
    #res = detectEmotion(nets["faceCascade"], nets["keras_emo"], image)
    print ("Got emos")
    print (res)
    #res = get_emotion(nets,data, companyId, campaignId, participantId, timestamp, ageGenderCache )
    #print res
    #saveToDB(res)
    print ("Sending response")


    resp = Response(response=res,
                    status=200,
                    mimetype="application/json") 



    return resp

@app.route('/')
@app.route('/index')
@cross_origin()
def default():
    return "Hello There!!!"


if __name__ == '__main__':
    #processFrame()
   app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
