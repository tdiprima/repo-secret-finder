"""
Check: Are there API key patterns in source files?
"""

import re

from ..results import Finding
from ..scanner import get_source_files, read_file_lines

# Patterns that scream "this is an API key"
API_KEY_PATTERNS = [
    (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\'][A-Za-z0-9]', "API key assignment"),
    (r'(?i)(secret[_-]?key|secretkey)\s*[=:]\s*["\'][A-Za-z0-9]', "secret key assignment"),
    (r'(?i)(access[_-]?token)\s*[=:]\s*["\'][A-Za-z0-9]', "access token assignment"),
    (r'AKIA[0-9A-Z]{16}', "AWS access key"),
    (r'sk-[a-zA-Z0-9]{20,}', "OpenAI/Stripe-style secret key"),
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub personal access token"),
]


def check_api_keys(repo_path):
    """Scan source files for API key patterns."""
    findings = []
    found_any = False

    for filepath in get_source_files(repo_path):
        lines = read_file_lines(filepath)

        for line_num, line in enumerate(lines, start=1):
            for pattern, description in API_KEY_PATTERNS:
                if re.search(pattern, line):
                    short_path = filepath.replace(repo_path, "").lstrip("/")
                    findings.append(
                        Finding("FAIL", f"{description} in {short_path}:{line_num}")
                    )
                    found_any = True
                    break  # one match per line is enough

    if not found_any:
        findings.append(Finding("OK", "no API keys found"))

    return findings
