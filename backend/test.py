import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/nlptown/bert-base-multilingual-uncased-sentiment"

headers = {
    "Authorization": f"Bearer {os.environ['HUGGINGFACE_API_KEY']}",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({
    "inputs": "tres bon film, je le recommande vivement!",
})

print(output)
