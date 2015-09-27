from datetime import datetime
from elasticsearch import Elasticsearch
import base64
import uuid
import json
import os
import io
from PIL import Image



#es.index(index="my-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})
#print(es.get(index="my-index", doc_type="test-type", id=42)['_source'])

def index_image(image):
  es = Elasticsearch()
  image_id = uuid.uuid4()
  doc = {
      "image_name": image_hash
      
  }
  es.index(index="image-search", doc_type="image", id=image_id, body=json.dumps(doc))

def get_image_hash(image_id):
  es = Elasticsearch()
  return es.get(index="image-search", doc_type="image", id=image_id)['_source']['image']

def get_image(image_id):
  return 

if __name__ == "__main__":

  with open("wizard-bubble.jpg", "rb") as f:
    index_image(f)

  print(get_image("283a5856-4514-4d37-be99-720184e48adc"))
