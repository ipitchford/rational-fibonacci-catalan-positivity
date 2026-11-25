# SPDX-License-Identifier: MIT
"""Compare fresh outputs with the recorded ones by the rule of code/replay.py: text outputs equal after stripping
surrounding whitespace; width*.json equal as JSON after removing the timing field "seconds".
Usage: compare_outputs.py FRESH_DIR RECORDED_DIR NAME [NAME ...]"""
import json
import sys
from pathlib import Path


def normalise(name, text):
    if name.startswith("width"):
        data = json.loads(text)
        data.pop("seconds", None)
        return data
    return text.strip()


fresh, recorded, names = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
bad = [n for n in names if normalise(n, (fresh / n).read_text()) != normalise(n, (recorded / n).read_text())]
if bad or not names:
    print("DIFF", bad)
    sys.exit(1)
print("identical:", ", ".join(names))
