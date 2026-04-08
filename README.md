An AI-powered scanner that detects malicious or unsafe instructions in skill files using a Hugging Face API-based model.

Features

*  Scans .md files for unsafe content
*  Uses AI API for classification
*  Detects prompt injection patterns
*  Hybrid detection (AI + rules)
*  Integrated with CI/CD pipeline


 Rule-Based Detection (Fallback)

Triggers when suspicious patterns are found:

* "ignore previous instructions"
* "send all secrets"

 If triggered:

* Forces label = `malicious`
* Assigns high confidence (0.90)

Severity Detection

Each line is analyzed and marked as:

* `safe`
* `warning`
* `critical`

If any "critical issue" is found:

* The scan fails
* CI/CD pipeline stops


CI/CD Integration

* Runs automatically on:

 * Push events
* Installs dependencies
* Executes scanner
* Fails pipeline if threats are detected



This project demonstrates:

* API-based AI integration
* Prompt injection detection
* Secure CI/CD practices
* Real-world automation workflow



