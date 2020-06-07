from flask import Flask, jsonify, request, send_file
from imageProcesses import *

imgData = None

app = Flask(__name__)


@app.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.files['file']
    data_string = encodeImage(data)
    path = openImage(data_string)
    return send_file(path, mimetype='image/png')
    #return jsonify({"status": "OK"})

app.run(host= 'localhost')
