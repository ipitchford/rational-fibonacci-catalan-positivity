"""Exact checks of the small numerical statements in the introduction and in Sections 3-6.

Standard library only.  Every failed check raises CertificateError (also under python -O).
Writes a JSON summary to standard output.
"""
from fractions import Fraction
from math import gcd, isqrt
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_type_a import F, exact_quotient, check


def lucas(s, t, length=40):
    u = [0, 1]
    while len(u) < length:
        u.append(s * u[-1] + t * u[-2])
    return u


def primes_below(limit):
    sieve = bytearray([1]) * limit
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytearray(len(sieve[p * p::p]))
    return [p for p in range(limit) if sieve[p]]


def run():
    out = {}

    # Introduction: the (m,n) = (4,3) example.
    c43 = exact_quotient(F[5:7], [F[j] for j in range(1, 4) if j != 1])
    check(c43 == [1, 1, 2, 2, 3, 2, 3, 2, 2, 1, 1], "C_{4,3}")
    out["C_4_3"] = c43
    # the uncorrected quotient P/[F_{m+n}] agrees (g = 1)
    p43 = exact_quotient(F[5:8], F[1:4])
    out["P_4_3_degree"] = len(p43) - 1

    # Density of the unimodality family (Theorem 6.1).
    product = Fraction(13, 16)
    value = 13 / 16
    for p in primes_below(10 ** 6)[1:]:
        value *= 1 - 3 / p ** 2
    # tail: prod_{p >= 10^6}(1-3/p^2) >= 1 - 3 sum_{k >= 10^6} 1/k^2 >= 1 - 3/(10^6 - 1)
    out["density_product_primes_below_1e6"] = value
    out["density_tail_relative_bound"] = 3 / (10 ** 6 - 1)
    check(0.4078 < value * (1 - 3 / (10 ** 6 - 1)) and value < 0.4079, "density value")
    N = 2000
    count = sum(1 for m in range(1, N + 1) for n in range(1, N + 1)
                if gcd(m, n) <= 2 and gcd(m - 1, n) <= 2 and gcd(m, n - 1) <= 2)
    out["density_direct_count_N2000"] = count / N ** 2

    # Comparison with Gatzweiler-Levican-Santibanez-Yoshida, Theorem 3.9, for g <= 2:
    # sorted weights 1 = b_1 <= ... <= b_{n-1} = F_n (corrected list, n >= 3), smallest degree F_{m+1}.
    gly = {}
    for n in range(3, 41):
        bound = 2 * F[n] * (F[n - 1] // 2) - 1
        m = n
        while F[m + 1] <= bound:
            m += 1
        gly[n] = m
    out["GLY_first_m_by_n"] = {str(n): gly[n] for n in gly}
    out["GLY_first_m_minus_2n"] = sorted(set(gly[n] - 2 * n for n in gly if n >= 7))
    check(all(gly[n] == 2 * n - 3 for n in range(7, 41)), "GLY boundary 2n-3 for 7 <= n <= 40")

    # Lucas examples (Section 4).
    table = []
    for s, t in [(1, 2), (2, 1), (2, 3)]:
        u = lucas(s, t)
        weights = [u[j] for j in range(1, 4) if j != 1]
        degrees = u[5:7]
        q = exact_quotient(degrees, weights)
        table.append(dict(s=s, t=t, weights=weights, degrees=degrees, degree=len(q) - 1, value_at_1=sum(q)))
    check([(r["weights"], r["degrees"], r["degree"], r["value_at_1"]) for r in table] ==
          [([1, 3], [11, 21], 28, 77), ([2, 5], [29, 70], 92, 203), ([2, 7], [61, 182], 234, 793)],
          "Lucas table")
    out["lucas_table"] = table
    u = lucas(1, 2)
    corrected = exact_quotient(u[4:6], [u[j] for j in range(1, 4) if j != 3])
    five_eleven = exact_quotient([5, 11], [1, 1])
    check(corrected == five_eleven, "(s,t)=(1,2), (m,n)=(3,3)")
    check(2 * 2 + 5 * 5 == 29 and 35 * 2 == 70 and 14 * 5 == 70, "Pell relation degrees")

    # Fuss corollary 5.2: a = k h + 1 and a = k h - 1 are admissible in every row of Theorem 5.1.
    rows = {"G2": (6, (1, 5)), "F4": (6, (1, 5)), "E6": (6, (1, 5)), "E7": (6, (1, 5)),
            "E8": (30, (1, 7, 11, 13, 17, 19, 23, 29)), "H3": (10, (1, 5, 9)), "H4": (30, (1, 11, 19, 29))}
    coxeter_number = {"G2": 6, "F4": 12, "E6": 12, "E7": 18, "E8": 30, "H3": 10, "H4": 30}
    for name, (modulus, residues) in rows.items():
        h = coxeter_number[name]
        for k in range(0, 12):
            for a in (k * h + 1, k * h - 1):
                if a >= 1:
                    check(a % modulus in residues, ("Fuss", name, a))
    for r in range(1, 30):
        for k in range(0, 8):
            for a in (k * (r + 1) + 1, k * (r + 1) - 1):
                if a >= 1:
                    check(gcd(a, r + 1) <= 2, ("Fuss A", r, a))
            for h in (2 * r, 2 * r - 2):           # B_r and D_r (r >= 4) have even Coxeter numbers
                for a in (k * h + 1, k * h - 1):
                    if a >= 1:
                        check(a % 2 == 1, ("Fuss BD", r, a))
    out["fuss_shifts_checked"] = True

    # Remark 5.3: D = (4,6,9), a = 4 gives a polynomial with a negative coefficient.
    q = exact_quotient([F[4 + d - 1] for d in (4, 6, 9)], [F[d] for d in (4, 6, 9)])
    check(q[13] == -1 and min(q) == -1, "negative example")
    out["negative_example_coefficient_q13"] = q[13]
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    run()
