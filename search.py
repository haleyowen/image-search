from datetime import datetime
from elasticsearch import Elasticsearch
import base64
import uuid
import json

es = Elasticsearch()

#es.index(index="my-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})
#print(es.get(index="my-index", doc_type="test-type", id=42)['_source'])

def index_image(image):
  global es
  image_id = uuid.uuid4()
  image_hash = base64.b64encode(image.read()).decode(encoding="UTF-8")
  doc = {
      "image": image_hash
  }
  es.index(index="image-search", doc_type="image", id=image_id, body=json.dumps(doc))

def get_image(image_id):
  global es
  return es.get(index="image-search", doc_type="image", id=image_id)['_source']['image']

#with open("wizard-bubble.jpg", "rb") as f:
#  index_image(f)

get_image("283a5856-4514-4d37-be99-720184e48adc")

