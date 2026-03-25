"""
Check: Does the repo have a .gitignore?
"""

import os

from ..results import Finding


def check_gitignore(repo_path):
    """Warn if .gitignore is missing."""
    gitignore_path = os.path.join(repo_path, ".gitignore")

    if os.path.isfile(gitignore_path):
        return [Finding("OK", ".gitignore exists")]
    return [Finding("WARN", "missing .gitignore")]
