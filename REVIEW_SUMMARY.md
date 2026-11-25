# Review summary (internal, AI-assisted)

This is a rating-free public summary of the internal checking of version 0.1.0-candidate. It is not peer review,
independent reproduction or formal verification. No human referee has assessed the paper.

## What was done (24 November 2026)

1. **Combined five-role review panel** (one Claude subagent taking the roles of editor, methodology and proof rigour,
   domain and literature, perspective, and devil's advocate) on the first draft, with the cited sources obtained and
   read: Bergeron-Ceballos-Küstner, Connelly et al., Gatzweiler-Levicán-Santibáñez-Yoshida, Bender-Spaenlehauer,
   Billey-Swanson, Bennett-Carrillo-Machacek-Sagan, Sagan-Tirrell, Stanley-Zanello and Armstrong. The panel reran the
   programs and recomputed load-bearing claims. It found no critical issue; its major items concerned framing, the
   exact boundary with prior work, credit, overstatement of the counting description, and certificates that relied on
   `assert`.
2. **One revision round with extensions.** A context-first introduction and a split into Part I (positivity) and
   Part II (unimodality); the exact boundary of the separated-degree criterion of Gatzweiler-Levicán-Santibáñez-Yoshida
   (Remark 3.2, least m ≥ n is 2n − 3 for n ≥ 7); the support criterion credited to them (Lemma 2.1); the counting
   description demoted to a remark that explicitly does not answer the tiling question; credit to S. X. Li,
   Aliniaeifard and Connelly et al.; the correction of the coprimality condition in types B and D stated; the
   unverifiable 1974 degree-table citation replaced by Armstrong's memoir; all `assert` statements replaced by checks
   that raise an exception, also under `python -O`, with negative controls; new exact certificates for widths six and
   seven (unimodality up to width seven, previously five in the draft); the Fuss-Catalan corollary.
3. **Verification re-review and proof audit** of every new or rewritten proof (Remark 3.2, Theorem 9.1 and its
   certificate argument, Corollary 5.2, the revised Section 1). The re-reviewer reran every program except width seven
   (checked against a byte-identical earlier run), tested the exact-minimum routine against brute force, and checked
   the error constants and the Part B error bound against exact computation. No open correctness issue remained; minor
   wording and rounding items were applied.
4. **Clean replays** of all nine certificate runs from fresh copies under `python -I -B -O`, with two negative
   controls, by the lead and again by the publisher (see [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md)).

No Astra/Codex second-model review took place: that route reported the model as unsupported for the account.

## Main objections and how they were handled

| Objection | Disposition |
|---|---|
| "The separated-degree criterion already covers this." | Remark 3.2 computes its exact reach: for n ≥ 7 it gives m ≥ 2n − 3. Theorem 3.1 adds the comparable range n ≤ m ≤ 2n − 4 (about half of all pairs with m ≥ n) and the exact reduced denominator for every gcd. |
| "The complete intersection answers the open problem." | It does not, and the paper says so (Remark 3.4): it gives a graded algebra and a monomial basis, not a statistic on the path-domino tilings. An explicit model is Open Problem 1; pure-power models were shown to fail for most pairs. |
| "Credit is loose." | Li (polynomiality), Aliniaeifard and Connelly et al. (unimodality implies positivity), and Gatzweiler-Levicán-Santibáñez-Yoshida (criterion, separated case) are credited at the points of use. |
| "The certificates pass silently under -O." | Every check now raises an exception; corrupting the H3 residues or the positivity check makes the program exit 1 under `-O`. |
| "Widths five to seven are computer proofs." | Yes, and the paper says so. The arithmetic is exact (integers and rationals, Bernstein coefficients); the error bounds are proved in Section 9 and the margins exceed them by a factor of at least seven. |
| Not addressed | Gatzweiler-Krattenthaler and the q = 1 FiboCatalan literature are not cited; no claim depends on them. |

## Scope of assurance

Internal AI-assisted review only: written proofs checked by AI reviewers, exact computer certificates replayed,
sources read. No human specialist review, no independent reproduction by an unaffiliated party, no proof-assistant
formalisation. Literature searches were of limited scope (see [RESEARCH_GATES.json](RESEARCH_GATES.json)).
