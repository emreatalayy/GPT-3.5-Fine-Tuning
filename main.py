import requests
import json

# API anahtarınızı buraya girin
api_key = "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"


training_file_id = "file-l13cZmHxgy4vg0IR22uvkQSt"

# API endpoint
url = "https://api.openai.com/v1/fine_tuning/jobs"

# HTTP header
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "training_file": training_file_id,
    "model": "gpt-3.5-turbo-16k"
}
response = requests.post(url, headers=headers, json=data)

# Yanıtı yazdır
print(response.json())
