# Replay receipt (v0.1.0-candidate, 25 November 2026)

Release replay by the publisher from a fresh copy of the approved candidate (`code/` and `results/`), working directory
= package root, macOS arm64. Command, as in the brief: `uv run --no-project --python 3.12 python3 -I -B -O code/replay.py`.
Interpreter as printed inside the run: CPython 3.14.7 (the uv shim resolved the 3.12 request to 3.14.7), platform
macOS-27.2.1-arm64.

| Run | Command | Exit | Result |
|---|---|---|---|
| Full replay | `python3 -I -B -O code/replay.py` | 0 | nine PASS lines, "All nine certificate programs completed."; 182 s |
| Negative control 1 | verify_exceptional.py with the H3 residues (1, 5, 9) changed to (1, 9), under -O | 1 | `CertificateError: ('H3', 5, 'cyclotomic')` |
| Negative control 2 | verify_type_a.py with the positivity check `min(poly) >= 0` changed to `>= 1`, under -O | 1 | `CertificateError: verify_type_a.py line 68` |

stderr was empty for the passing run, and the replay left `code/` and `results/` unchanged. The lead's earlier clean
replay (24 November 2026, CPython 3.14.7) gave the same nine PASS lines. After the replay only the title-page DOI line
of manuscript.tex, a one-line typo fix in the Section 1 example (the product form of C_{4,3} now reads
[5]_q[8]_q/[2]_q; the coefficient list, code and outputs were already correct), the rebuilt PDF and the release records
changed; `code/`, `results/` and `ENVIRONMENT.txt` are
byte-identical to the replayed candidate.

Comparison rule (that of `code/replay.py`, also used by CI): text outputs equal after stripping surrounding whitespace;
`results/width*.json` equal as JSON after removing the timing field `"seconds"`. All arithmetic is exact, so no
floating-point tolerance is needed or used. CI on Linux runs eight of the nine certificate runs under `-O` as a blocking
job, both negative controls, and the full `code/replay.py` (including width seven) as a separate non-blocking job.
