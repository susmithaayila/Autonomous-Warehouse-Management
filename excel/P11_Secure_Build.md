# P11_Secure_Build Data View

## Sheet: Static Analysis & Audit

| Scan Tool | Target Component | Vulnerability Detected | Severity | Status / Fix |
| --- | --- | --- | --- | --- |
| Bandit | backend/main.py | B104: Hardcoded bind to 0.0.0.0 | LOW | Refactored to bind via environment variable |
| pip-audit | Python Dependencies | No known CVE vulnerabilities in pinned packages | NONE | PASSED |


