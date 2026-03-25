"""
Walks the repo. Provides files. Does NOT check anything.
That's the checkers' job.
"""

import os

# Directories we never want to scan
SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
    ".next",
    ".nuxt",
}

# File extensions we consider "source code"
SOURCE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".rb", ".go", ".java", ".rs", ".php",
    ".sh", ".bash", ".zsh",
    ".yaml", ".yml", ".toml", ".json",
    ".tf", ".hcl",
}


def get_all_files(repo_path):
    """Yield every file path in the repo (skipping junk dirs)."""
    for root, dirs, files in os.walk(repo_path):
        # Modify dirs in-place to skip junk directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in files:
            yield os.path.join(root, filename)


def get_source_files(repo_path):
    """Yield only source code files."""
    for filepath in get_all_files(repo_path):
        _, ext = os.path.splitext(filepath)
        if ext.lower() in SOURCE_EXTENSIONS:
            yield filepath


def read_file_lines(filepath):
    """Read a file into lines. Return empty list if it fails."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    except (OSError, UnicodeDecodeError):
        return []
