#!/usr/bin/env python3
from kumikolib import Kumiko
import os
import time
import datetime
from bottle import route, run, template, request, static_file
import json

@route('/detect', method='POST')
def detect():
    upload = request.files.get('upload')       
    name, ext = os.path.splitext(upload.filename)
    print(ext.lower())
    if ext.lower() not in ('.png','.jpg','.jpeg'):
        return "File extension not allowed."
    timestamp=str(int(time.time()*1000))
    savedName=timestamp+ext
    save_path = "./uploaded/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = "{path}/{file}".format(path=save_path, file=savedName)
    if os.path.exists(file_path)==True:
        os.remove(file_path)
    upload.save(file_path)        
    kumiko = Kumiko()
    infos = []
    infos = kumiko.parse_images([file_path])
    os.remove(file_path)
    return {"infos":infos}


@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='www')


run(server="paste",host='0.0.0.0', port=8091)     

