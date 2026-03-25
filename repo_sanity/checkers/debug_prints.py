"""
Check: Are there debug print() calls left in the code?
Only flags prints that look like debugging, not all prints.
"""

import re

from ..results import Finding
from ..scanner import get_source_files, read_file_lines

# Patterns that look like debug prints (not regular logging)
DEBUG_PATTERNS = [
    re.compile(r'print\s*\(\s*f?["\']debug', re.IGNORECASE),
    re.compile(r'print\s*\(\s*f?["\']TODO', re.IGNORECASE),
    re.compile(r'print\s*\(\s*f?["\']HACK', re.IGNORECASE),
    re.compile(r'print\s*\(\s*f?["\']FIXME', re.IGNORECASE),
    re.compile(r'print\s*\(\s*f?["\']XXX', re.IGNORECASE),
    re.compile(r'print\s*\(\s*f?["\']HERE', re.IGNORECASE),
    re.compile(r'print\s*\(\s*f?["\']###', re.IGNORECASE),
    re.compile(r'breakpoint\s*\(\s*\)'),
    re.compile(r'import\s+pdb'),
    re.compile(r'pdb\.set_trace\s*\('),
]


def check_debug_prints(repo_path):
    """Find debug prints and breakpoints."""
    findings = []
    found_any = False

    for filepath in get_source_files(repo_path):
        lines = read_file_lines(filepath)

        for line_num, line in enumerate(lines, start=1):
            for pattern in DEBUG_PATTERNS:
                if pattern.search(line):
                    short_path = filepath.replace(repo_path, "").lstrip("/")
                    findings.append(
                        Finding("WARN", f"debug code in {short_path}:{line_num}")
                    )
                    found_any = True
                    break

    if not found_any:
        findings.append(Finding("OK", "no debug prints found"))

    return findings
