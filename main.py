import requests

api_key = "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"

# Dosya yolu
file_path = "C:\\Users\\atala\\OneDrive\\Masaüstü\\fine Tuning\\send_data3.jsonl"

# API endpoint
url = "https://api.openai.com/v1/files"
# HTTP header
headers = {
    "Authorization": f"Bearer {api_key}"
}
with open(file_path, "rb") as f:

    response = requests.post(
        url,
        headers=headers,
        files={"file": f},
        data={"purpose": "fine-tune"}
    )
print(response.json())

