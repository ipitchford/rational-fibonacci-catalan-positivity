"""Rerun every certificate and compare with the shipped results.

Usage (from the package root):  python3 code/replay.py [--write]
Standard library only.  Exit status 0 means every program succeeded and every output
matched results/ (timing fields in the width certificates are ignored).
With --write the outputs are (re)written to results/ instead of compared.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE = ROOT / "code"
RESULTS = ROOT / "results"
JOBS = [
    (["verify_type_a.py"], "verify_type_a.json"),
    (["verify_exceptional.py"], "verify_exceptional.txt"),
    (["verify_pairs.py"], "verify_pairs.txt"),
    (["verify_classical.py"], "verify_classical.txt"),
    (["claims.py"], "claims.json"),
    (["width_cert.py", "4", "30"], "width4.json"),
    (["width_cert.py", "5", "50"], "width5.json"),
    (["width_cert.py", "6", "60"], "width6.json"),
    (["width_cert.py", "7", "70"], "width7.json"),
]


def normalise(name, text):
    if name.startswith("width"):
        data = json.loads(text)
        data.pop("seconds", None)
        return data
    return text.strip()


def main():
    write = "--write" in sys.argv
    failures = 0
    for args, name in JOBS:
        flags = ["-I", "-B"] + (["-O"] if sys.flags.optimize else [])
        cmd = [sys.executable, *flags, str(CODE / args[0]), *args[1:]]
        run = subprocess.run(cmd, capture_output=True, text=True)
        if run.returncode != 0:
            print("FAIL", name, run.stderr.strip().splitlines()[-1:] or "")
            failures += 1
            continue
        target = RESULTS / name
        if not write and not target.exists():
            print("FAIL", name, "missing stored output")
            failures += 1
            continue
        if write:
            target.write_text(run.stdout)
            print("WROTE", name, flush=True)
        elif normalise(name, run.stdout) == normalise(name, target.read_text()):
            print("PASS", name, flush=True)
        else:
            print("DIFF", name)
            failures += 1
    if failures:
        sys.exit(1)
    print("All nine certificate programs completed.")


if __name__ == "__main__":
    main()
