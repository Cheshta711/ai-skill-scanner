import os
import sys
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

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            # AI classification
            label, score = classify(content)
            print("DEBUG:", label, score)

            # Rule-based detection (FIXED)
            if any(keyword in content.lower() for keyword in [
                "ignore previous instructions",
                "send all secrets"
            ]):
                label = "malicious"
                score = max(score, 0.9)

            # Only act if truly malicious
            if label == "malicious" and score > 0.5:
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

    # Save results
    with open("results.txt", "w", encoding="utf-8") as f:
        for r in results:
            f.write(f"{r['file']}:{r['line']} [{r['severity']}] {r['text']}\n")

    # Final decision
    if found_critical:
        print("\n❌ Failing workflow — critical issues found")
        sys.exit(1)
    else:
        print("\n✅ Scan completed (no critical issues)")


if __name__ == "__main__":
    scan()