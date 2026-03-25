"""
Prints findings in color. That's the whole file.
"""

# ANSI color codes (no dependencies needed)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

COLORS = {
    "OK": GREEN,
    "WARN": YELLOW,
    "FAIL": RED,
}


def print_banner():
    """Print the tool name. Just vibes."""
    print()
    print(f"{BOLD}  repo-sanity 🔍{RESET}")
    print(f"  {'─' * 40}")
    print()


def print_finding(finding):
    """Print one finding with color."""
    color = COLORS.get(finding.level, RESET)
    tag = f"{color}{BOLD}[{finding.level}]{RESET}"
    print(f"  {tag} {finding.message}")


def print_summary(findings):
    """Print a count of warns and fails at the end."""
    warns = sum(1 for f in findings if f.level == "WARN")
    fails = sum(1 for f in findings if f.level == "FAIL")
    oks = sum(1 for f in findings if f.level == "OK")

    print()
    print(f"  {'─' * 40}")

    if fails > 0:
        print(f"  {RED}{BOLD}{fails} critical{RESET}", end="")
    else:
        print(f"  {GREEN}{BOLD}0 critical{RESET}", end="")

    print(f"  ·  ", end="")

    if warns > 0:
        print(f"{YELLOW}{BOLD}{warns} warnings{RESET}", end="")
    else:
        print(f"{GREEN}{BOLD}0 warnings{RESET}", end="")

    print(f"  ·  {GREEN}{oks} ok{RESET}")
    print()
