import os
from app import app
from os.path import join, dirname, realpath
from flask import request, redirect, url_for, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
ALLOWED_EXTENSIONS = set(['png'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

##Image Upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## Route to upload files
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    error = None  

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            error = "No File Part"
            return render_template('index.html', title="Images", error=error)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            error = "No Selected File"
            return render_template('index.html', title="Images", error=error)
            
        # Check if user submits a PNG image
        if not allowed_file(file.filename):
            error = "File type not supported"
            return render_template('index.html', title="Images", error=error)

        # send file to be output if all formmatting is correct
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('index.html', title="Images", error=error)

@app.route('/show/<filename>')
def uploaded_file(filename):
    return render_template('index.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/return_file/<filename>')
def return_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment = True)

@app.route('/denoise/<filename>')
def denoise(filename):
    pass
