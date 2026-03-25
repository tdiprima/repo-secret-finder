"""
Check: Are secret-looking files world-readable?
(Only works on Linux/Mac where file permissions exist.)
"""

import os
import stat

from ..results import Finding
from ..scanner import get_all_files

# Files that should NOT be world-readable
SECRET_FILENAMES = [
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "service-account.json",
    "secrets.yaml",
    "secrets.yml",
    ".htpasswd",
    "id_rsa",
    "id_ed25519",
]


def is_world_readable(filepath):
    """Check if a file has the 'others can read' permission bit."""
    try:
        file_stat = os.stat(filepath)
        return bool(file_stat.st_mode & stat.S_IROTH)
    except OSError:
        return False


def check_secret_files(repo_path):
    """Warn about world-readable secret files."""
    findings = []
    found_any = False

    for filepath in get_all_files(repo_path):
        basename = os.path.basename(filepath)

        if basename in SECRET_FILENAMES and is_world_readable(filepath):
            short_path = filepath.replace(repo_path, "").lstrip("/")
            findings.append(
                Finding("WARN", f"world-readable secret file: {short_path}")
            )
            found_any = True

    if not found_any:
        findings.append(Finding("OK", "no world-readable secrets"))

    return findings
