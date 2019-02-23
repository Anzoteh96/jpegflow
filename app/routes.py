import os
from app import app
from os.path import join, dirname, realpath
from flask import request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

##Image Upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template('index.html', title="Images")
