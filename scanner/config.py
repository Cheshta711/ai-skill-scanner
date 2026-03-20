API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
SAFE = "safe"
MALICIOUS = "malicious"

SEVERITY_RULES = {
    "critical": ["send all secrets", "exfiltrate", "http"],
    "warning": ["ignore previous instructions", "bypass", "override"]
}