from flask import Flask, render_template, request, jsonify

import json
import os
import uuid
import requests

from elasticsearch import Elasticsearch

application = Flask(__name__, static_folder="static")
application.config['DEBUG'] = True

current_image_id = -1
name = -1
full_name = "UNDEFINED"
access_token = None


@application.route("/")
def api_root():
    return render_template("test.html")


@application.route("/upload_file", methods=["POST"])
def api_upload():
    global name, full_name
    if request.method != 'POST':
        return "no"

    upload = request.files['file']
    image_id = str(uuid.uuid4())
    name = image_id+"."+upload.filename.split(".")[-1]
    full_name = "http://45.55.45.85/static/uploads/"+str(name)

    file_path = os.path.join(os.getcwd(), "static/uploads/")+str(name)

    upload.save(file_path)

    # tags = process_image(["http://45.55.45.85/static/uploads/"+name])

    # doc = {
    #     "image_name": image_id,
    # }
    global current_image_id
    current_image_id = image_id

    # es = Elasticsearch()
    # es.index(index="image-search", doc_type="image", id=image_id,
    #         body=json.dumps(doc))

    return jsonify({"message": "success"})


@application.route("/post_tags", methods=["POST"])
def api_post_tags():
    # query = {
    #     "query": {
    #         "match": {
    #             "tags": search_terms
    #         }
    #     }
    # }

    global full_name, current_image_id

    tags = request.json

    print(tags)

    doc = {
        "image_name": current_image_id,
        "tags_hits": tags
    }

    es = Elasticsearch()
    es.index(index="image-search", doc_type="image", id=current_image_id,
             body=doc)

    print('made it')
    query_ids = {
        "query": {
            "match_all": {}
        }
    }

    results = es.search(index="image-search", body=query_ids)

    print(results)
    return json.dumps(results)


def api_get_files():
    return 0


@application.route("/post_url", methods=["POST"])
def api_post_url():
    global access_token

    if not access_token:
        r = requests.post("https://api.clarifai.com/v1/token/?grant_type=" +
                          "client_credentials&client_id=KuQ2EWXhdosMQyktS" +
                          "I1tw6Z3be7c677oA11p1g9o&client_secret=Kt84XYqK" +
                          "7nVnx3f05_B8pe2biv9bBlGZAHjFvEwF")
        access_token = r.json()['access_token']

    return str('https://api.clarifai.com/v1/tag/?url=' +
               full_name+'&access_token='+access_token)


def extract_tags_dict(obj):
    print(obj['results'][0]['result'])
    data = obj['results'][0]['result']['tag']
    tags = data['classes']
    probs = data['probs']
    return dict(zip(tags, probs))

if __name__ == "__main__":
    application.run(debug=True)
