"""Exact independent tests of the rational Fibonacci Catalan results, using stdlib."""
from fractions import Fraction
from functools import reduce
from itertools import combinations
from math import gcd, prod
import heapq
import json


class CertificateError(Exception):
    """Raised when any certificate check fails (independent of python -O)."""


def check(condition, message="certificate check failed"):
    if not condition:
        raise CertificateError(message)


F = [0, 1]
while len(F) < 100:
    F.append(F[-1] + F[-2])


def multiply_binomial(coefficients, exponent):
    result = coefficients + [0] * exponent
    for i, coefficient in enumerate(coefficients):
        result[i + exponent] -= coefficient
    return result


def exact_quotient(degrees, weights):
    numerator = [1]
    for degree in degrees:
        numerator = multiply_binomial(numerator, degree)
    for weight in weights:
        top = len(numerator) - weight
        check(top > 0, 'verify_type_a.py line 27')
        for i in range(weight, len(numerator)):
            numerator[i] += numerator[i - weight]
        check(not any(numerator[top:]), 'verify_type_a.py line 30')
        numerator = numerator[:top]
    return numerator


def semigroup_membership(weights):
    """Compute the exact Apery set by Dijkstra, independently of the proof bound."""
    divisor = reduce(gcd, weights)
    steps = [w // divisor for w in weights]
    modulus = min(steps)
    distances = [float("inf")] * modulus
    distances[0] = 0
    queue = [(0, 0)]
    while queue:
        distance, residue = heapq.heappop(queue)
        if distance != distances[residue]:
            continue
        for step in steps:
            value = distance + step
            next_residue = value % modulus
            if value < distances[next_residue]:
                distances[next_residue] = value
                heapq.heappush(queue, (value, next_residue))
    return lambda x: x % divisor == 0 and distances[(x // divisor) % modulus] <= x // divisor


def support_ok(weights, degrees):
    checked = 0
    for size in range(1, len(weights) + 1):
        for subset in combinations(weights, size):
            belongs = semigroup_membership(subset)
            check(sum(belongs(d) for d in degrees) >= size, 'verify_type_a.py line 61')
            checked += 1
    return checked


def profile(poly, degrees, weights):
    check(poly == poly[::-1], 'verify_type_a.py line 67')
    check(min(poly) >= 0, 'verify_type_a.py line 68')
    check(sum(poly) == Fraction(prod(degrees), prod(weights)), 'verify_type_a.py line 69')
    check(len(poly) - 1 == sum(degrees) - sum(weights), 'verify_type_a.py line 70')


def fibonomial(m, n):
    degrees = [F[i] for i in range(m + 1, m + n + 1)]
    weights = F[1:n + 1]
    return exact_quotient(degrees, weights)


def run():
    stats = dict(full_corrected_pairs=0, positive_double_trims=0,
                 support_subsets=0, certified_unimodal_pairs=0)
    for n in range(1, 13):
        for m in range(n, min(23 - n, 15) + 1):
            g = gcd(m, n)
            weights = [F[j] for j in range(1, n + 1) if j != g]
            degrees = F[m + 1:m + n]
            q = exact_quotient(degrees, weights)
            profile(q, degrees, weights)
            stats["full_corrected_pairs"] += 1
            stats["support_subsets"] += support_ok(weights, degrees)
            p = fibonomial(m, n)
            # P * [F_g] = corrected Catalan * [F_{m+n}].
            check(multiply_binomial(p, F[g]) == multiply_binomial(q, F[m + n]), 'verify_type_a.py line 93')
            if max(g, gcd(m - 1, n), gcd(m, n - 1)) <= 2:
                check(all(a <= b for a, b in zip(p, p[1:len(p)//2 + 1])), 'verify_type_a.py line 95')
                stats["certified_unimodal_pairs"] += 1
                if n >= 3:
                    subdegrees = degrees[:-1]
                    subweights = F[3:n + 1]
                    trim = exact_quotient(subdegrees, subweights)
                    profile(trim, subdegrees, subweights)
                    stats["support_subsets"] += support_ok(subweights, subdegrees)
                    check(len(trim) - 1 <= F[m + n], 'verify_type_a.py line 103')
                    stats["positive_double_trims"] += 1

    # Non-box example. Count its lattice points directly by degree.
    enumerator = [0] * (89 + 144 + 233 - (1 + 2 + 3) + 1)
    for i in range(89):
        for j in range(72):
            for k in range(125 if j == 0 else 77):
                enumerator[i + 2*j + 3*k] += 1
    check(enumerator == exact_quotient([89, 144, 233], [1, 2, 3]), 'verify_type_a.py line 112')
    check(sum(enumerator) == 497688, 'verify_type_a.py line 113')
    stats["non_box_objects"] = sum(enumerator)

    for m in range(4, 13):
        a, b = F[m+1:m+3]
        poly = fibonomial(m, 4)
        centre = (len(poly)-1)//2
        # floor(y+1/2) for y=(k+3)^2/12
        def three_parts(k):
            return 0 if k < 0 else ((k+3)**2 + 6)//12
        differences = [three_parts(k)-three_parts(k-a)-three_parts(k-b)+three_parts(k-2*a-b)
                       for k in range(centre + 1)]
        check(differences == [poly[0]] + [poly[k]-poly[k-1] for k in range(1, centre+1)], 'verify_type_a.py line 125')
        check(min(differences) == int(m > 4), 'verify_type_a.py line 126')
        if m < 8:
            stats[f"width4_m{m}"] = dict(centre=centre, min_difference=min(differences))

    stats["lucas_pairs"] = 0
    stats["lucas_support_subsets"] = 0
    for s, t in [(1, 2), (2, 1), (2, 3), (3, 2)]:
        u = [0, 1]
        for i in range(12):
            u.append(s*u[-1] + t*u[-2])
        for n in range(2, 6):
            for m in range(n, min(7, 10-n)+1):
                weights = [u[j] for j in range(1, n+1) if j != gcd(m, n)]
                degrees = u[m+1:m+n]
                profile(exact_quotient(degrees, weights), degrees, weights)
                stats["lucas_support_subsets"] += support_ok(weights, degrees)
                stats["lucas_pairs"] += 1

    for n, m in [(2, 3), (3, 4), (4, 5), (4, 4)]:
        g = gcd(n, m)
        weights = [F[j] for j in range(1, n + 1) if j != g]
        q = exact_quotient(F[m + 1:m + n], weights)
        stats[f"fingerprint_{m}_{n}"] = dict(degree=len(q)-1, count=sum(q),
                                             first=q[:16], last=q[-6:])
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    run()
