import sys
sys.path.insert(0, "src")

from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

import pipe
from app_exception import *


import os


UPLOAD_FOLDER = 'static/img_storage/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def get_main_page():
    return render_template('index.html', title='Home', user='user')

@app.route('/convert', methods=['GET', 'POST'])
def start_convert():
    file = request.files['file']
    try:
        blur = bool(request.form['add_blur'])
    except:
        blur = False
    colors_num = int(request.form['colors'])
    max_pieces_size = int(request.form['pieces_size'])

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        f_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(f_path)
        try:
            pipe.pipe(f_path, colors_num=colors_num, blur=blur, max_pieces_size=max_pieces_size)
            with open('vot-eto-da-both.svg') as f:
                vector = f.read()
                return {'status': 'OK', 'raster': f'../{f_path}', 'vector': vector}
        except QuantizeError:
            return {
                'status': 'ERROR', 
                'error': 'QuantizeError', 
                'error_msg': 'Number of colors is higher than img pixels num!'
            }
    else:
        return {
            'status': 'ERROR', 
            'error': 'FormatError', 
            'error_msg': 'This input file format not supprted!',
        }
    return 'Error'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Flask, Response

@app.route("/getSVG")
def get_svg():
    with open('vot-eto-da-both.svg') as f:
        svg = f.read()
    return Response(
        svg,
        mimetype="image/svg+xml",
        headers={"Content-disposition":"attachment; filename=ouput.svg"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8001', debug=True)