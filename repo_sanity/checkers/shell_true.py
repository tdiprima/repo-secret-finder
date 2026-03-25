"""
Check: Is anyone using subprocess with shell=True?
(This allows shell injection attacks.)
"""

import re

from ..results import Finding
from ..scanner import get_source_files, read_file_lines

# Patterns that match shell=True in subprocess calls
SHELL_TRUE_PATTERN = re.compile(
    r'subprocess\.\w+\(.*shell\s*=\s*True', re.IGNORECASE
)


def check_shell_true(repo_path):
    """Find subprocess calls with shell=True."""
    findings = []
    found_any = False

    for filepath in get_source_files(repo_path):
        lines = read_file_lines(filepath)

        for line_num, line in enumerate(lines, start=1):
            if SHELL_TRUE_PATTERN.search(line):
                short_path = filepath.replace(repo_path, "").lstrip("/")
                findings.append(
                    Finding("WARN", f"subprocess(shell=True) in {short_path}:{line_num}")
                )
                found_any = True

    if not found_any:
        findings.append(Finding("OK", "no subprocess(shell=True) found"))

    return findings
