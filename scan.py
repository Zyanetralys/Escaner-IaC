import os, re, json, argparse, sys
from pathlib import Path

PATTERNS = {
    "aws_key": r"(?i)(AKIA|ASIA)[0-9A-Z]{16}",
    "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
    "password": r"(?i)(password|passwd|secret)\s*[:=]\s*['\"][^'\"]{8,}"
}

def scan_file(f):
    hits = []
    try:
        with open(f, encoding="utf-8", errors="ignore") as fp:
            content = fp.read()
            for k, pat in PATTERNS.items():
                if re.search(pat, content):
                    hits.append(k)
    except: pass
    return hits

def run(root):
    results = {}
    for p in Path(root).rglob("*.{tf,yml,yaml,json,env,sh}"):
        h = scan_file(p)
        if h: results[str(p)] = h
    return results

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("path", nargs="?", default=".")
    args = p.parse_args()
    out = run(args.path)
    print(json.dumps(out, indent=2))
    sys.exit(1 if out else 0)
