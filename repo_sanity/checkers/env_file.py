"""
Check: Is a .env file sitting in the repo?
"""

import os

from ..results import Finding


def check_env_file(repo_path):
    """Look for .env files. Return findings."""
    findings = []
    env_path = os.path.join(repo_path, ".env")

    if os.path.isfile(env_path):
        findings.append(Finding("WARN", ".env file committed"))
    else:
        findings.append(Finding("OK", "no .env file found"))

    return findings
