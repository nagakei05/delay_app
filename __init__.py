import os
import time

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['DELAY'] = 0

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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

    return app
