"""
Check: Are there private keys in the repo?
"""

import os

from ..results import Finding
from ..scanner import get_all_files, read_file_lines

# File extensions that are private keys
KEY_FILE_EXTENSIONS = [".pem", ".key", ".p12", ".pfx"]

# Strings that appear inside private key files
KEY_FILE_MARKERS = [
    "-----BEGIN RSA PRIVATE KEY-----",
    "-----BEGIN PRIVATE KEY-----",
    "-----BEGIN EC PRIVATE KEY-----",
    "-----BEGIN OPENSSH PRIVATE KEY-----",
]


def check_private_keys(repo_path):
    """Look for private key files or private key content."""
    findings = []
    found_any = False

    for filepath in get_all_files(repo_path):
        short_path = filepath.replace(repo_path, "").lstrip("/")

        # Check 1: suspicious file extension
        _, ext = os.path.splitext(filepath)
        if ext.lower() in KEY_FILE_EXTENSIONS:
            findings.append(Finding("FAIL", f"private key file: {short_path}"))
            found_any = True
            continue

        # Check 2: private key marker inside file
        lines = read_file_lines(filepath)
        for line in lines:
            for marker in KEY_FILE_MARKERS:
                if marker in line:
                    findings.append(
                        Finding("FAIL", f"private key content in {short_path}")
                    )
                    found_any = True
                    break
            if found_any:
                break

    if not found_any:
        findings.append(Finding("OK", "no private keys found"))

    return findings
