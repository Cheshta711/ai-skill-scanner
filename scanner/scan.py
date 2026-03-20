import os
import sys
from openai import OpenAI

client = OpenAI()

SKILLS_DIR = "skills"

def analyze_with_ai(content):
    prompt = f"""
You are a security analyzer.

Classify the following text as SAFE or MALICIOUS.
If malicious, return the exact suspicious lines.

Text:
{content}

Respond in this format:
Classification: SAFE or MALICIOUS
Reason: ...
Suspicious Lines: ...
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content


def scan_files():
    print("Scanning skills folder...\n")

    found_malicious = False

    for filename in os.listdir(SKILLS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(SKILLS_DIR, filename)

            print(f"Reading: {filepath}")

            with open(filepath, "r") as f:
                content = f.read()

            result = analyze_with_ai(content)
            print(result)

            if "MALICIOUS" in result:
                found_malicious = True

    if found_malicious:
        print("\n❌ Failing workflow — malicious content found")
        sys.exit(1)
    else:
        print("\n✅ No malicious content found")


if __name__ == "__main__":
    scan_files()
