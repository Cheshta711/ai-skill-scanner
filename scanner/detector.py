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

    except Exception as e:
        print("API ERROR:", e)
        return "safe", 0.0

    # ✅ NEW FORMAT (router API returns list of dicts)
    if isinstance(result, list) and len(result) > 0:
        try:
            # 🔥 Pick label with highest score
            best = max(result, key=lambda x: x["score"])
            return best["label"], best["score"]
        except:
            return "safe", 0.0

    # ✅ OLD FORMAT (fallback)
    if isinstance(result, dict) and "labels" in result and "scores" in result:
        try:
            labels = result["labels"]
            scores = result["scores"]

            # pick highest score
            max_index = scores.index(max(scores))
            return labels[max_index], scores[max_index]
        except:
            return "safe", 0.0

    # ❌ If API returns error
    if isinstance(result, dict) and "error" in result:
        print("API ERROR RESPONSE:", result["error"])
        return "safe", 0.0

    return "safe", 0.0
