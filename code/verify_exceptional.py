"""Verify every finite test in the exceptional Coxeter classification.

Uses Python 3.9+ and only the standard library. A failing test raises an exception.
In a row 'small a' counts admissible parameter/subset pairs before the respective
semigroup conductor. Each such pair is tested by its exact Apéry representatives.
"""
from functools import reduce
from heapq import heappop, heappush
from itertools import combinations
from math import gcd, lcm


class CertificateError(Exception):
    """Raised when any certificate check fails (independent of python -O)."""


def check(condition, message="certificate check failed"):
    if not condition:
        raise CertificateError(message)


CASES = [
    ("G2", (2, 6), 6, (1, 5)),
    ("F4", (2, 6, 8, 12), 6, (1, 5)),
    ("E6", (2, 5, 6, 8, 9, 12), 6, (1, 5)),
    ("E7", (2, 6, 8, 10, 12, 14, 18), 6, (1, 5)),
    ("E8", (2, 8, 12, 14, 18, 20, 24, 30), 30,
     (1, 7, 11, 13, 17, 19, 23, 29)),
    ("H3", (2, 6, 10), 10, (1, 5, 9)),
    ("H4", (2, 12, 20, 30), 30, (1, 11, 19, 29)),
]

def fibonacci(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a

def apery(generators):
    """Least semigroup element in each residue class of the first generator."""
    step = generators[0]
    distances = [None] * step
    distances[0] = 0
    queue = [(0, 0)]
    while queue:
        distance, residue = heappop(queue)
        if distance != distances[residue]:
            continue
        for generator in generators[1:]:
            new_distance = distance + generator
            new_residue = new_distance % step
            old_distance = distances[new_residue]
            if old_distance is None or new_distance < old_distance:
                distances[new_residue] = new_distance
                heappush(queue, (new_distance, new_residue))
    check(all(distance is not None for distance in distances), 'verify_exceptional.py line 46')
    return distances

def verify(name, degrees, modulus, residues):
    h = max(degrees)
    period = lcm(*degrees)
    divisor_counts = {}
    for k in range(3, h + 1):
        total = sum(d % k == 0 for d in degrees)
        if total:
            divisor_counts[k] = total

    # Testing the cyclotomic factors Phi_{F_k} is necessary. This loop shows
    # that these tests exclude precisely the parameters outside the row.
    check(period % modulus == 0, 'verify_exceptional.py line 60')
    for a in range(1, period + 1):
        passes = all(
            sum((a + d - 1) % k == 0 for d in degrees) >= count
            for k, count in divisor_counts.items()
        )
        check(passes == (a % modulus in residues), (name, a, "cyclotomic"))

    total_pairs = 0
    max_conductor = 0
    max_first_large = 0
    for size in range(1, len(degrees) + 1):
        for subset in combinations(degrees, size):
            index = reduce(gcd, subset)
            factor = fibonacci(index)
            generators = sorted({fibonacci(d) // factor for d in subset})
            distances = apery(generators)
            step = generators[0]
            scaled_conductor = factor * (max(distances) - step + 1)
            first_large = 1
            while fibonacci(first_large + min(degrees) - 1) < scaled_conductor:
                first_large += 1

            # Beyond the conductor, divisibility by the gcd suffices. When
            # F_index=1, every integer is divisible, including F_odd.
            index_period = 1 if index <= 2 else index
            for a in range(1, lcm(modulus, index_period) + 1):
                if a % modulus in residues:
                    count = sum((a + d - 1) % index_period == 0
                                for d in degrees)
                    check(count >= size, (name, subset, a, "large"))

            # Below the conductor, use exact semigroup membership.
            for a in range(1, first_large):
                if a % modulus not in residues:
                    continue
                count = 0
                for d in degrees:
                    value = fibonacci(a + d - 1)
                    quotient, remainder = divmod(value, factor)
                    if remainder == 0 and quotient >= distances[quotient % step]:
                        count += 1
                total_pairs += 1
                check(count >= size, (name, subset, a, "small"))

            max_conductor = max(max_conductor, scaled_conductor)
            max_first_large = max(max_first_large, first_large)

    print(f"{name:2} {period:5} {2**len(degrees)-1:5} {max_conductor:12}"
          f" {max_first_large:8} {total_pairs:7}")

if __name__ == "__main__":
    print("W  period subsets    conductor  first_a small_a")
    for case in CASES:
        verify(*case)
