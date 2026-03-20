import requests
import os
from config import API_URL

API_KEY = os.getenv("HF_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def classify(text):
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": ["malicious", "safe"]
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        print("API RESPONSE:", result) 
    except:
        return "safe", 0.0

    # ✅ Handle new Hugging Face format
    if isinstance(result, list) and len(result) > 0:
        for item in result:
            if item["label"] == "malicious":
                return "malicious", item["score"]
        return "safe", 0.0

    # ✅ Handle old format (fallback)
    if isinstance(result, dict) and "labels" in result:
        return result["labels"][0], result["scores"][0]

    return "safe", 0.0