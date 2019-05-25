import os
import sys
import uuid
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify
from ocr_core import process_image

app = Flask(__name__)
app.config['CACHE_FOLDER'] = '~/ocr_image_cache/'
app.config['ALLOWED_EXTENSIONS'] = set(['tiff', 'bmp', 'png', 'jpg', 'jpeg', 'webp'])
app.config['VERSION'] = 1.0

@app.route('/v{}/ocr'.format(app.config['VERSION']), methods=['GET', 'POST'])
def ocr():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"status":"error","message":"Empty request!"})
        uploaded_image = request.files['image']
        extension = os.path.splitext(uploaded_image.filename)[1]
        if extension in app.config['ALLOWED_EXTENSIONS']:
            cache_file_name = str(uuid.uuid4()) + extension
            uploaded_image.save(os.path.join(app.config['CACHE_FOLDER'], cache_file_name))
            ocr_output = process_image(uploaded_image)
            return jsonify({"status":"success","ocr_content":ocr_output})
        else:
            return jsonify({"status":"error","message":"Unsupport file type!"})