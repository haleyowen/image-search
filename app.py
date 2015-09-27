from flask import Flask, render_template, request, url_for, redirect, jsonify

import requests
import json
import os
import uuid
import ProcessImage

app = Flask(__name__)


@app.route("/")
def api_root():
    return render_template("test.html")


@app.route("/upload_file", methods=["POST"])
def api_upload():
    if request.method != 'POST':
        return "no"

    upload = request.files['file']
    image_id = str(uuid.uuid4())
    upload.save(os.path.join(os.getcwd(), "uploads/") + image_id)

    url = ["http://localhost:5000/uploads/" + image_id]
    tags = ProcessImage.process_image(url)
    
    doc = {
      "image_name": image_hash,
      "tags": tags
    }
    es.index(index="image-search", doc_type="image", id=image_id, body=json.dumps(doc))
    return "300"

@app.route("/image/<image_name>", methods=["GET"])
def api_get_image(image_name):
  search.get_image(image_name)

if __name__ == "__main__":
    app.run(debug=True)
