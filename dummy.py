import os
import hashlib
import unittest
from clarifai.client import ClarifaiApi
image_url = 'http://clarifai-img.s3.amazonaws.com/test/toddler-flowers.jpeg'
api = ClarifaiApi("KuQ2EWXhdosMQyktSI1tw6Z3be7c677oA11p1g9o","Kt84XYqK7nVnx3f05_B8pe2biv9bBlGZAHjFvEwF")
response = api.tag_image_urls(image_url)
#print("\n".join(map(str, (v for v in response['results']))))
print(response['results'][0]['result']['tag']['classes'])