import os
import time

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['DELAY'] = 0
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    # a simple page that says hello
    @app.route("/")
    def root():
        return "<p>delay is {} s</p>".format(app.config['DELAY'])

    @app.route("/client")
    def client():
        return "<p>Hello, World!</p>"

    @app.route("/probe")
    def probe():
        time.sleep(app.config['DELAY'])
        if app.config['DELAY'] < 30:
            app.config['DELAY'] += 50
        return "<p>Hello, World!</p>"

    @app.route("/reset")
    def reset():
        app.config['DELAY'] = 0
        return "<p>Delay time is set to 0</p>"

    @app.route('/upload', methods=['GET', 'POST'])
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
                return redirect(url_for('download_file', name=filename))
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''

    return app
