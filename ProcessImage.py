from flask import Flask, render_template, request, url_for, redirect

import requests
import json
from json import dumps
import os
import hashlib
import unittest
from clarifai.client import ClarifaiApi

app = Flask(__name__)

app.config.from_object("config")


@app.route("/")
def api_root(output=None):
    return render_template("index.html", output=output)




@app.route("/process/",methods=["POST"])
def process_image():
    urls = request.values.get('urls') #list of urls for the images
    api = ClarifaiApi() 
    response = api.tag_image_urls(url) #add functionality to go through all urls and index
    print(response)


if False:
    @app.route("/submit/", methods=["POST"])
    def api_submit_question():
        question_number = request.values.get('question_number')
        number = 0 if(question_number == "1") else (1 if(question_number =="2") else 2)
        code = request.values.get('file')
        test_case_array = app.config['HR_TEST_CASES']
        test_cases = test_case_array[number]
        lang = request.values.get('lang')
        print(code)
        print(json.dumps(test_cases))
        print(lang)
        payload = {"source": code,
                   "api_key": app.config["HR_KEY"],
                   "lang": lang,
                   "testcases": json.dumps(test_cases)}

        try:
            response = requests.post(app.config["HR_URL"], data=payload)
            res_json = json.loads(response.text)
            output = res_json["result"]["stdout"]
        except Exception as e:
            output = "Exception - check console"
            print(e)

        return dumps(output)

if __name__ == "__main__":
    app.run(debug=True)