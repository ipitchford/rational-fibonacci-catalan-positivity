"""Expand smaller classical and dihedral cases directly in integer arithmetic.

For each type and shift the quotient H_{D,a} is computed by exact polynomial division.
A non-polynomial quotient must occur exactly at the shifts excluded by the classification,
and every polynomial quotient must be symmetric with nonnegative coefficients.
Every failed test raises CertificateError, also under python -O.
"""
from math import gcd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_type_a import F, exact_quotient, profile, check, CertificateError


def classify(degrees, a, admissible):
    numerators = [F[a+d-1] for d in degrees]
    denominators = [F[d] for d in degrees]
    try:
        coefficients = exact_quotient(numerators, denominators)
    except CertificateError:
        check(not admissible, (degrees, a, "unexpected pole"))
        return
    check(admissible, (degrees, a, "unexpected polynomial"))
    profile(coefficients, numerators, denominators)


if __name__ == '__main__':
    count = 0
    for rank in range(2, 7):
        for a in range(1, 8):
            classify(tuple(range(2, 2 * rank + 1, 2)), a, a % 2 == 1)        # type B_rank
            classify(tuple(range(2, rank + 2)), a, gcd(a, rank + 1) <= 2)    # type A_rank
            count += 2
            if rank >= 4:
                classify(tuple(range(2, 2 * rank, 2)) + (rank,), a, a % 2 == 1)  # type D_rank
                count += 1
    for rank in range(3, 11):
        for a in range(1, 13):
            classify((2, rank), a, a % rank in (1, rank - 1))                # type I_2(rank)
            count += 1
    check(exact_quotient([F[4], F[6], F[8]], [F[2], F[4], F[6]]) == [1] * 21, "B3 at a=3")
    print(f"{count} classical and dihedral parameter checks passed. B3 at a=3 gives [21]_q.")
