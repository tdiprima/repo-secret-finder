#!/usr/bin/env python3
"""
repo-sanity: A simple security scanner.

Usage:
    python main.py /path/to/repo
"""

import sys
import os

from .checkers import ALL_CHECKERS
from .printer import print_banner, print_finding, print_summary


def get_repo_path():
    """Get the repo path from command line args."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <path-to-repo>")
        sys.exit(1)
    return os.path.abspath(sys.argv[1])


def run_all_checkers(repo_path):
    """Run every checker. Collect all findings."""
    all_findings = []
    for checker in ALL_CHECKERS:
        findings = checker(repo_path)
        all_findings.extend(findings)
    return all_findings


def main():
    repo_path = get_repo_path()
    print_banner()

    findings = run_all_checkers(repo_path)

    for finding in findings:
        print_finding(finding)

    print_summary(findings)


if __name__ == "__main__":
    main()
