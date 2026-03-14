"""
Check: Are there database connection strings in source files?
"""

import re

from results import Finding
from scanner import get_source_files, read_file_lines

# Patterns covering common database connection string formats
DB_CONNECTION_PATTERNS = [
    (
        r'(?i)(postgresql|postgres|mysql|mariadb|mssql|sqlserver|oracle|mongodb|redis|sqlite)'
        r'(\+\w+)?://[^@\s"\']+:[^@\s"\']+@',
        "database connection string with credentials",
    ),
    (
        r'(?i)(db[_-]?password|database[_-]?password|db[_-]?pass)\s*[=:]\s*["\'][^"\']+["\']',
        "database password assignment",
    ),
    (
        r'(?i)(db[_-]?url|database[_-]?url|connection[_-]?string)\s*[=:]\s*["\'][^"\']+["\']',
        "database URL assignment",
    ),
    (
        r'(?i)Data\s+Source\s*=\s*[^;]+;\s*Password\s*=\s*[^;"\']+',
        "ADO.NET-style connection string with password",
    ),
    (
        r'(?i)mongodb(\+srv)?://[^@\s"\']+:[^@\s"\']+@',
        "MongoDB connection string with credentials",
    ),
    (
        r'(?i)redis://(:[^@\s"\']+@|[^@\s"\']+:[^@\s"\']+@)',
        "Redis connection string with credentials",
    ),
]


def check_db_connections(repo_path):
    """Scan source files for database connection strings containing credentials."""
    findings = []
    found_any = False

    for filepath in get_source_files(repo_path):
        lines = read_file_lines(filepath)

        for line_num, line in enumerate(lines, start=1):
            for pattern, description in DB_CONNECTION_PATTERNS:
                if re.search(pattern, line):
                    short_path = filepath.replace(repo_path, "").lstrip("/")
                    findings.append(
                        Finding("FAIL", f"{description} in {short_path}:{line_num}")
                    )
                    found_any = True
                    break  # one match per line is enough

    if not found_any:
        findings.append(Finding("OK", "no database connection strings found"))

    return findings
