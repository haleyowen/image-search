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

to_analyze = []


@application.route("/")
def api_root():
    return render_template("test.html")


@application.route("/upload_file", methods=["POST"])
def api_upload():
    if request.method != 'POST':
        return "no"

    upload = request.files['file']
    image_id = str(uuid.uuid4())
    name = image_id+"."+upload.filename.split(".")[-1]

    web_path = "http://45.55.45.85/static/uploads/"+str(name)
    file_path = os.path.join(os.getcwd(), "static/uploads/")+str(name)

    to_analyze.append((web_path, image_id))

    upload.save(file_path)

    return jsonify({"message": "success"})


@application.route("/post_tags", methods=["POST"])
def api_post_tags():
    if len(to_analyze) < 1:
        return json.dumps({"msg": "done"})

    last = to_analyze.pop()
    web_path = last[0]
    image_id = last[1]

    tags = request.json

    tags_str = " ".join(word for word in tags)

    doc = {
        "image_name": image_id,
        "tags": tags_str,
        "path": web_path
    }

    es = Elasticsearch()
    es.index(index="image-search", doc_type="image", id=image_id,
             body=doc)

    if len(to_analyze) < 1:
        return json.dumps({"msg": "done"})
    return json.dumps({"msg": str(len(to_analyze))+" left"})


@application.route("/search", methods=["POST"])
def api_search():
    es = Elasticsearch()

    search_data = request.json
    search_data_str = " ".join(tags for tags in search_data)

    results = es.search(index="image-search",
                        body={"size": 200, "query":
                              {"match": {"tags": search_data_str}}})

    result_list = [str(v["_source"]["path"]) for v in results['hits']['hits']]

    return json.dumps(result_list)


@application.route("/top_terms", methods=["GET"])
def api_get_files():
    es = Elasticsearch()
    results = es.search(index="image-search",
                        body={"size": 200})
    freq = dict()

    for v in results['hits']['hits']:
        try:
            for x in v["_source"]["tags"].split():
                freq[x] = freq.get(x, 0) + 1
        except Exception as e:
            print(e)

    top_ten = list(sorted(freq.values()))[-5:] + [10]
    top_ten_tags = [tag for tag in freq if freq[tag] >= top_ten[0]]

    return json.dumps(list(set(top_ten_tags)))


@application.route("/post_url", methods=["POST"])
def api_post_url():
    global access_token, to_analyze

    if not access_token:
        r = requests.post("https://api.clarifai.com/v1/token/?grant_type=" +
                          "client_credentials&client_id=KuQ2EWXhdosMQyktS" +
                          "I1tw6Z3be7c677oA11p1g9o&client_secret=Kt84XYqK" +
                          "7nVnx3f05_B8pe2biv9bBlGZAHjFvEwF")
        access_token = r.json()['access_token']

    if len(to_analyze) < 1:
        return "200"

    full_name = to_analyze[-1][0]

    return str('https://api.clarifai.com/v1/tag/?url=' +
               full_name+'&access_token='+access_token)

if __name__ == "__main__":
    application.run(debug=True)
