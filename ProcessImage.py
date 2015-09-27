from flask import Flask, render_template, request, url_for, redirect

import requests
import json
from json import dumps
import os
import hashlib
import unittest
from clarifai.client import ClarifaiApi

def process_image(urls):
    tags = dict()
    api = ClarifaiApi("KuQ2EWXhdosMQyktSI1tw6Z3be7c677oA11p1g9o","Kt84XYqK7nVnx3f05_B8pe2biv9bBlGZAHjFvEwF")

    for u in urls:
        response = api.tag_image_urls(u)
        tags[u] = response['results'][0]['result']['tag']['classes']

    return tags
