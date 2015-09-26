from flask import Flask, render_template, request, url_for, redirect, jsonify

import requests
import json
import os

app = Flask(__name__)


@app.route("/")
def api_root():
    return render_template("test.html")


@app.route("/upload_file", methods=["POST"])
def api_upload():
    if request.method != 'POST':
        return "no"
    print(request.files)
    single_file = request.files['file']
    single_file.save(os.path.join(os.path.dirname(__file__), 'uploads/'))
    # file_size = os.path.getsize(os.path.join(updir, f.filename))
    # return jsonify(name=f.filename, size=file_size)
    return "123"

if __name__ == "__main__":
    app.run(debug=True)
