import os
import sys
from datetime import datetime

# Try AI
try:
    from google import genai
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

SKILLS_DIR = "skills"


# 🎨 Logging helpers
def log_info(msg):
    print(f"[INFO] {msg}")

def log_alert(msg):
    print(f"[ALERT] {msg}")

def log_fail(msg):
    print(f"[FAIL] {msg}")

def log_safe(msg):
    print(f"[SAFE] {msg}")


# 🧠 AI analysis
def analyze_with_ai(content):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Classify as SAFE or MALICIOUS:\n{content}"
        )
        return response.text
    except Exception as e:
        log_info(f"AI unavailable → {e}")
        return None


# 🔒 Rule-based fallback
def fallback_rule_based(content):
    patterns = {
        "ignore previous instructions": "HIGH",
        "send all secrets": "HIGH",
        "bypass": "MEDIUM",
        "exfiltrate": "HIGH",
        "jailbreak": "MEDIUM"
    }

    for pattern, severity in patterns.items():
        if pattern in content.lower():
            return {
                "status": "MALICIOUS",
                "pattern": pattern,
                "severity": severity
            }

    return {"status": "SAFE"}


# 🚀 Main scan
def scan_files():
    log_info("Scan started")
    log_info(f"Timestamp: {datetime.now()}\n")

    found_malicious = False

    for filename in os.listdir(SKILLS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(SKILLS_DIR, filename)

            log_info(f"Analyzing file: {filepath}")

            with open(filepath, "r") as f:
                content = f.read()

            result = None

            # Try AI first
            if AI_AVAILABLE:
                result = analyze_with_ai(content)

            # Fallback if AI fails
            if not result:
                log_info("Using fallback detection")
                result = fallback_rule_based(content)

            # Handle dict (rule-based)
            if isinstance(result, dict):
                if result["status"] == "MALICIOUS":
                    log_alert("Threat detected!")
                    print(f"        File      : {filename}")
                    print(f"        Severity  : {result['severity']}")
                    print(f"        Pattern   : {result['pattern']}")
                    print(f"        Action    : BLOCKED\n")

                    found_malicious = True
                else:
                    log_safe(f"{filename} is safe\n")

            else:
                # AI response
                print(result)
                if "MALICIOUS" in result.upper():
                    found_malicious = True

    # Final result
    if found_malicious:
        log_fail("Scan completed — malicious content found ❌")
        sys.exit(1)
    else:
        log_safe("Scan completed — no threats detected ✅")


if __name__ == "__main__":
    scan_files()
