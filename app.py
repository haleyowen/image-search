from flask import Flask, render_template, request, url_for, redirect, jsonify

import requests
import json
import os

app = Flask(__name__, static_folder="static")


@app.route("/")
def api_root():
    return render_template("test.html")


@app.route("/upload_file", methods=["POST"])
def api_upload():
    if request.method != 'POST':
        return "no"

    upload = request.files['file']
    upload.save(os.path.join(os.getcwd(), "static/img/") + upload.filename)

    return jsonify({"message": "success"})

if __name__ == "__main__":
    app.run(debug=True)
