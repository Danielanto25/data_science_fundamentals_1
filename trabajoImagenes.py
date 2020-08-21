#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 19:53:37 2020

@author: daniel
"""
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np


import matplotlib.pyplot as plt

model = ResNet50(weights='imagenet')

from flask import Flask, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
#Define the path to the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Specifies the maximum size (in bytes) of the files to be uploaded
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

            
        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ruta='/home/daniel/Documentos/reconocedor de imagenes/imagenes'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],ruta,filename))
            img_path = filename
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)


            preds = model.predict(x)
            # decode the results into a list of tuples (class, description, probability)
            # (one such list for each sample in the batch)
            a='Predicted:', decode_predictions(preds, top=1)[0]
            b=''
            c=''
            print(a)
            # print("COMO ESTAS?")
            for i in a[1]:
               b=i[1]
               c=str(int(round(i[2]*100)))
                
            # print("HOLA")
            # print(a)
            return '''<h2>La Imagen que acabas de Ingresar Corresponde a un '''+b+''' y Estoy un '''+c+'''%  Seguro</h2>'''
        else:
            return 'No allowed extension'

if __name__ == '__main__':
    app.run()