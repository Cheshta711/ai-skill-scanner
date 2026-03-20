import os
import sys
<<<<<<< HEAD
from detector import classify
from utils import get_severity, load_ignore

SKILLS_DIR = "skills"

def scan():
    ignore_list = load_ignore()
    found_critical = False
    results = []

    print("🔍 Scanning skills folder...\n")

    for file in os.listdir(SKILLS_DIR):
        if file.endswith(".md"):
            path = os.path.join(SKILLS_DIR, file)

            print(f"📄 Reading: {path}")

            with open(path) as f:
                content = f.read()

            label, score = classify(content)

            if label == "malicious":
                print(f"⚠ MALICIOUS ({score:.2f})")

                for i, line in enumerate(content.split("\n"), 1):

                    if any(ignore in line.lower() for ignore in ignore_list):
                        continue

                    severity = get_severity(line)

                    if severity != "safe":
                        print(f"{severity.upper()} Line {i}: {line}")

                        results.append({
                            "file": file,
                            "line": i,
                            "text": line,
                            "severity": severity
                        })

                        if severity == "critical":
                            found_critical = True

    # Save results for PR comment
    with open("results.txt", "w") as f:
        for r in results:
            f.write(f"{r['file']}:{r['line']} [{r['severity']}] {r['text']}\n")

    if found_critical:
        print("\n❌ Failing workflow — critical issues found")
        sys.exit(1)
    else:
        print("\n✅ Scan completed (no critical issues)")

if __name__ == "__main__":
    scan()
=======
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
>>>>>>> 953fb62b46feb2139c6d5d6f7de9fb07efbeb8a0
