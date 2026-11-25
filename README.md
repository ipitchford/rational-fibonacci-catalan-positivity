# Rational Fibonacci–Catalan polynomials: positivity, a Coxeter classification and q-Fibonomial unimodality up to width seven

**Fibonacci–Catalan polynomials have nonnegative coefficients.** Unrefereed research candidate, version 0.1.0-candidate.
DOI [10.5281/zenodo.24541015](https://doi.org/10.5281/zenodo.24541015) (all versions:
[10.5281/zenodo.24541014](https://doi.org/10.5281/zenodo.24541014)). Release page:
https://evidencepress.org/releases/rational-fibonacci-catalan-positivity/

## What this is about

**The objects.** Many counting formulas are ratios of products of whole numbers: the binomial coefficient
"m+n choose n", or the rational Catalan number (1/(m+n))·(m+n choose n), which counts staircase lattice paths. Now
replace each whole number j by the Fibonacci number F_j (1, 1, 2, 3, 5, 8, 13, ...), and each resulting number u by the
polynomial [u]_q = 1 + q + q² + ... + q^(u−1) with u terms (a "q-integer"). The results are the q-Fibonomial
coefficients P_{m,n}(q) and the rational q-Fibonacci–Catalan functions C_{m,n}(q) of Bergeron, Ceballos and Küstner
(SIGMA, 2020). For example

C_{4,3}(q) = [8]_q [13]_q / [2]_q = 1 + q + 2q² + 2q³ + 3q⁴ + 2q⁵ + 3q⁶ + 2q⁷ + 2q⁸ + q⁹ + q¹⁰.

**Why it matters.** When a formula like this turns out to be a polynomial with nonnegative coefficients,
mathematicians expect it to count something, graded by the power of q. Bergeron, Ceballos and Küstner saw nonnegative
coefficients in every case they computed (indices up to 15), wrote that they had neither a proof nor a combinatorial
model, and asked what the coefficients count. They also conjectured that the q-Fibonomial coefficients are
*unimodal*: their coefficients rise and then fall.

**What was known.** C_{m,n} is a polynomial when gcd(m,n) ≤ 2 (S. X. Li). Aliniaeifard observed, and Connelly, Ito,
Martinez, Shevchenko and Yang proved, that unimodality would imply the nonnegativity; Connelly et al. proved
unimodality when the smaller index is at most three. A general criterion of Gatzweiler, Levicán-Santibáñez and Yoshida
gives nonnegativity when the two indices are far apart (for n ≥ 7, exactly when m ≥ 2n − 3), leaving the pairs with
comparable indices, about half of all pairs, open.

**What is new.**

- *Positivity and the exact denominator* (Theorem 3.1). For every pair (m,n), the reduced denominator of C_{m,n} is
  exactly [F_g]_q with g = gcd(m,n), and the reduced numerator is the Hilbert series of an Artinian weighted complete
  intersection: its coefficients are the dimensions of the graded pieces of an explicit kind of algebra. So C_{m,n}
  has nonnegative coefficients whenever g ≤ 2. For instance
  C_{10,4} = [89]_q ([72]_{q²} [77]_{q³} + q^231 [48]_{q³}), a manifestly positive formula read off from the algebra
  (Example 3.3).
- *Lucas sequences* (Corollary 4.1). The same holds with Fibonacci numbers replaced by any Lucas sequence with coprime
  positive integer parameters, for example the Pell numbers.
- *Reflection groups* (Theorem 5.1). For the analogous Fibonacci product attached to any irreducible finite reflection
  (Coxeter) group, the shifts that give a polynomial are determined exactly, and every such polynomial has nonnegative
  coefficients. Every Fibonacci Fuss–Coxeter–Catalan quotient is positive (Corollary 5.2). The list shows that the
  coprimality condition suggested in the 2020 paper is too strong in types B and D: for B₃ with shift 3 the product is
  [21]_q.
- *Unimodality.* P_{m,n} is unimodal on an explicit set of index pairs of natural density about 0.408 (Theorem 6.1);
  for each fixed smaller index n ≥ 4 its coefficients increase strictly to the centre once m is large (Theorem 7.1);
  and P_{m,n} is unimodal whenever the smaller index is at most seven (Theorems 8.1 and 9.1; previously at most three).
  Width four has a short written proof; widths five, six and seven rest on exact computer certificates.

**Idea of the proof.** After cancelling, the quotient is a product of factors (1 − q^e)/(1 − q^w) with "big" degrees
e and "small" degrees w. Such a product counts monomials in a quotient ring when, for every group of small degrees,
enough big degrees can be written as sums of them. Fibonacci numbers make this checkable: divisibility of Fibonacci
numbers follows divisibility of their indices, and a coin-problem bound shows that the big degrees are large enough,
uniformly, even when the indices are close. For unimodality, as m grows the coefficient profile approaches a smooth
spline built from intervals of lengths 1, φ, φ², ... (φ the golden ratio), which is strictly peaked; exact rational
arithmetic with explicit error bounds turns this into a proof for widths five to seven.

**Limits.** The algebra gives a basis but *not* a combinatorial interpretation on the path-domino tilings of the 2020
paper, so that open problem remains open in its intended sense. The unrestricted unimodality conjecture remains open.
Widths five to seven and the exceptional reflection groups rely on exact, rerunnable computer certificates.
Galois-twisted non-crystallographic and reducible Coxeter cases are not treated. This is an unrefereed candidate; its
assurance is internal AI-assisted review and exact replays only (see [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md)).

**Credit.** Polynomiality is due to S. X. Li; the implication from unimodality to positivity to Aliniaeifard and
Connelly et al.; the complete-intersection criterion (Lemma 2.1) and the separated-degree case to Gatzweiler,
Levicán-Santibáñez and Yoshida.

## Where to read next

- The paper: [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex)), 14 pages. Section 1 is a
  plain introduction: the objects, why they matter, what was known, what is new, and a roadmap.
- Machine-readable map of claims and evidence: [AI_INDEX.md](AI_INDEX.md).
- Prior art, sources read and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json).
- Review summary (internal, AI-assisted): [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md).

## Replaying the checks

Python 3.9 or later, standard library only. From the package root:

```sh
python3 -I -B -O code/replay.py
```

Expected: nine PASS lines, then "All nine certificate programs completed.", exit status 0. `code/replay.py` reruns
every certificate program (with the same `-I`, `-B` and `-O` flags) and compares its output with `results/`. Every
check uses exact arithmetic (integers and fractions), and the few printed decimals are correctly rounded
conversions, so the outputs are platform independent; the only field ignored is the
timing field `"seconds"` in `results/width*.json`. Run time about three to five minutes on a laptop, almost all in
`width_cert.py 7 70`. Each program raises an exception on any failed check, also under `python -O` (no `assert` is
used). With uv: `uv run --python 3.12 python3 -I -B -O code/replay.py`.

## Contents

| Path | What it is |
|---|---|
| `manuscript.tex`, `manuscript.pdf` | The paper (14 pages) |
| `code/verify_type_a.py` | Theorem 3.1 on 104 pairs (support test on 8695 subsets), Example 3.3, the width-four difference formula, Corollary 4.1 on 60 pairs and four parameter choices |
| `code/verify_exceptional.py`, `code/verify_pairs.py` | Two independent finite certificates for the exceptional rows of Theorem 5.1 |
| `code/verify_classical.py` | Direct expansion of 187 classical and dihedral cases of Theorem 5.1 |
| `code/claims.py` | Numerical statements of Section 1, Remark 3.2, Section 4, Corollary 5.2 and Theorem 6.1 |
| `code/width_cert.py` | Exact certificates of Section 9 for widths four to seven |
| `code/replay.py` | Reruns all nine certificate runs and compares with `results/` |
| `results/` | Recorded outputs |
| `ENVIRONMENT.txt` | Reference environment and replay command |
| `refs.bib` | Bibliography, from Crossref and arXiv records |
| `AI_INDEX.md`, `RESEARCH_GATES.json`, `REVIEW_SUMMARY.md`, `REPLAY_RECEIPT.md` | Release records |
| `CITATION.cff`, `.zenodo.json`, `LICENSE.md`, `MANIFEST.sha256` | Citation, archive metadata, licences, hashes |
| `.github/` | CI: manifest, eight certificate runs under `-O` compared with `results/`, negative controls; full replay with width seven as a separate non-blocking job |

## Licence and citation

Creator: Anonymous. Text, the paper, recorded outputs and records: CC0-1.0. Code: MIT. See [LICENSE.md](LICENSE.md)
and [CITATION.cff](CITATION.cff). Cite as: Anonymous (2026), *Rational Fibonacci–Catalan polynomials: positivity, a
Coxeter classification and q-Fibonomial unimodality up to width seven*, version 0.1.0-candidate, Evidence Press,
doi:10.5281/zenodo.24541015.
