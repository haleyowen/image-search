from flask import Flask, render_template, request, url_for, redirect

import requests
import json
from json import dumps
import os
import hashlib
import unittest
from clarifai.client import ClarifaiApi
from PyDictionary import PyDictionary

def process_image(urls):
    tags = {}
    dictionary = PyDictionary()
    api = ClarifaiApi("KuQ2EWXhdosMQyktSI1tw6Z3be7c677oA11p1g9o","Kt84XYqK7nVnx3f05_B8pe2biv9bBlGZAHjFvEwF")
    for u in urls:
        response = api.tag_image_urls(u)
        words = response['results'][0]['result']['tag']['classes']
        words_new = []
        for word in words:
            words_new.append(word)
            #words_new += dictionary.synonym(word) --> get synonyms (TODO)
        tags[u] = words_new

    print(tags,len(tags['http://i.imgur.com/qR41ox0.jpg']))

process_image(["http://i.imgur.com/qR41ox0.jpg"])
