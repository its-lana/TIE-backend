import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..\PaddleOCR\ppstructure\table')))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..\PaddleOCR\ppstructure')))
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..\PaddleOCR')))


from flask import request, flash, redirect, url_for, send_from_directory
from app import app
from werkzeug.utils import secure_filename
from helpers import allowed_file, TableArgs
from PaddleOCR.ppstructure import table


@app.route('/table', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('extract_table', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/table/uploads/<name>')
def download_file(name):
    return send_from_directory("..\img",name)


@app.route('/table/extract/<name>')
def extract_table(name):
    args = TableArgs(image_dir="F:/Programming/Python/Flask/TIE/PaddleOCR/ppstructure/table/table3.jpg")
    table.predict_table.main(args=args)
    return send_from_directory("..\img",name)

# @app.route('/table/extract', methods=['GET', 'POST'])
# def upload_file():

