# 🔐 Repo Secret Finder 🔎

I wanted a lightweight way to scan my repositories for potential secret leaks without relying on tools like GitLeaks.

This project is a small scanner that detects common secrets in your codebase so you can catch leaks locally before they reach CI or GitHub security scans.

Detects:

- API keys (AWS, OpenAI, Stripe, GitHub tokens, generic key assignments)
- `.env` files committed to the repository
- Private keys (`.pem`, `.key`, `.p12`, `.pfx` files and key content markers)
- Secret files with overly permissive file permissions
- Missing `.gitignore` files
- Debug print statements, `breakpoint()` calls, and `pdb` usage
- Subprocess calls with `shell=True` (shell injection risk)
- Database connection strings with embedded credentials (PostgreSQL, MySQL, MongoDB, Redis, MSSQL, and ADO.NET-style strings)

## Example

```
$ repo_sanity /path/to/your/repo

  repo-sanity 🔍
  ────────────────────────────────────────

  [OK] no .env file found
  [OK] .gitignore exists
  [FAIL] private key content in secrets/deploy.pem
  [WARN] subprocess(shell=True) in scripts/run.py:12
  [FAIL] database connection string with credentials in config/db.py:8

  ────────────────────────────────────────
  2 critical  ·  1 warnings  ·  3 ok
```

## Install

```bash
git clone https://github.com/tdiprima/repo-secret-finder.git
cd repo-secret-finder
pip install .
```

No external dependencies required — uses the Python standard library only.

## Usage

```bash
# Scan a specific repo
repo_sanity /path/to/your/repo

# Scan the current directory
repo_sanity .
```

<br>
