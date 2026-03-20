API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

SAFE = "safe"
MALICIOUS = "malicious"

SEVERITY_RULES = {
    "critical": ["send all secrets", "exfiltrate", "http"],
    "warning": ["ignore previous instructions", "bypass", "override"]
}