# 🔐 Repo Secret Finder 🔎

CI pipelines often run without basic security checks, allowing secrets to leak into repositories undetected.

**Solution:** A lightweight scanner that detects common secret leaks in your codebase before CI or GitHub scanners do.

I cleaned up my whole codebase with this.

Detects:

- API keys (AWS, OpenAI, Stripe, GitHub tokens, generic key assignments)
- `.env` files committed to the repository
- Private keys (`.pem`, `.key`, `.p12`, `.pfx` files and key content markers)
- Secret files with overly permissive file permissions
- Missing `.gitignore` files
- Debug print statements, `breakpoint()` calls, and `pdb` usage
- Subprocess calls with `shell=True` (shell injection risk)

## Example

```
$ python main.py /path/to/your/repo

⚠ Possible AWS key in config/settings.py
⚠ .env file detected
✔ No private keys found
```

## Install

```bash
git clone https://github.com/tdiprima/Secret-Leak-Finder.git
cd Secret-Leak-Finder
```

No external dependencies required — uses the Python standard library only.

## Usage

```bash
python main.py /path/to/your/repo
```
