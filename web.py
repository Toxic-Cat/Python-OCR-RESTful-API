import os
import sys
import uuid
import logging
from ocr_core import process_image
from flask import Flask, request, jsonify
from logging import Formatter, FileHandler

app = Flask(__name__)
app.config['CACHE_FOLDER'] = '~/ocr_image_cache/'
app.config['ALLOWED_EXTENSIONS'] = set(['tiff', 'bmp', 'png', 'jpg', 'jpeg', 'webp'])
app.config['VERSION'] = 1.0

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/v{}/ocr'.format(app.config['VERSION']), methods=['GET', 'POST'])
def ocr():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"status":"error","message":"Empty request!"})
        uploaded_image = request.files['image']
        if uploaded_image and allowed_file(str.lower(uploaded_image.filename)):
            ocr_output = process_image(uploaded_image)
            return jsonify({"status":"success","ocr_content":ocr_output})
        else:
            return jsonify({"status":"error","message":"Unsupport file type!"})
    if request.method == 'GET':
        return jsonify({"status":"error","message":"Please POST file and use 'image' as its key"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)