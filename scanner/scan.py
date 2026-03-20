import os
import sys

SKILLS_DIR = "skills"

def is_malicious(text):
    suspicious_patterns = [
        "ignore previous instructions",
        "send all secrets",
        "bypass",
        "exfiltrate",
        "jailbreak"
    ]

    for pattern in suspicious_patterns:
        if pattern in text.lower():
            return True, pattern

    return False, None


def scan_files():
    print("Scanning skills folder...\n")

    found_malicious = False

    for filename in os.listdir(SKILLS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(SKILLS_DIR, filename)

            print(f"Reading: {filepath}")

            with open(filepath, "r") as f:
                content = f.read()

            is_bad, pattern = is_malicious(content)

            if is_bad:
                print("\n⚠ Malicious content detected:")
                print(f'File: {filename}')
                print(f'Matched pattern: "{pattern}"\n')

                found_malicious = True

    if found_malicious:
        print("❌ Failing workflow — malicious content found")
        sys.exit(1)
    else:
        print("\n✅ No malicious content found")


if __name__ == "__main__":
    scan_files()
