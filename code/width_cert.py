"""Exact unimodality certificate for the q-Fibonomial P_{m,n} at a fixed width n.

Usage: python3 width_cert.py N THRESHOLD [EPS1 EPS2]

Proves: for every m >= N the coefficients of P_{m,N} increase weakly through the
centre (strictly where reported), by
  (A) an exact finite check for N <= m < THRESHOLD, and
  (B) a rational-arithmetic limiting-spline certificate for m >= THRESHOLD.
Only the Python standard library is used.  Every check raises CertificateError
on failure, so the program also fails under python -O.
"""
from fractions import Fraction as Q
from math import comb, factorial, lcm, prod
import json
import sys
import time


class CertificateError(Exception):
    pass


def check(condition, message):
    if not condition:
        raise CertificateError(message)


F = [0, 1]
while len(F) < 200:
    F.append(F[-1] + F[-2])


# ----------------------------------------------------------------------------
# Quasi-polynomial coefficients of 1/prod(1-q^w)
# ----------------------------------------------------------------------------
def denumerants(weights, length):
    d = [1] + [0] * (length - 1)
    for w in weights:
        for j in range(w, length):
            d[j] += d[j - w]
    return d


def interpolant(weights, period):
    """On each residue class rho mod period, h(rho + period*i) = sum_j c_j binom(i, j)."""
    degree = len(weights) - 1
    values = denumerants(weights, period * (degree + 1))
    pieces = []
    for rho in range(period):
        row = values[rho::period]
        diffs = []
        while row:
            diffs.append(row[0])
            row = [b - a for a, b in zip(row, row[1:])]
        check(len(diffs) == degree + 1, "interpolation length")
        pieces.append(diffs)
    return pieces


def h_eval(pieces, period, x):
    if x < 0:
        return 0
    i, rho = divmod(x, period)
    return sum(c * comb(i, j) for j, c in enumerate(pieces[rho]))


def mul_linear(poly, a, b):
    out = [Q(0)] * (len(poly) + 1)
    for j, c in enumerate(poly):
        out[j] += a * c
        out[j + 1] += b * c
    return out


def error_constant(pieces, period, degree, leading):
    """C with |h(k)/leading - k^degree| <= C (k+1)^(degree-1) for k >= 0."""
    worst = Q(0)
    for rho, cs in enumerate(pieces):
        binom = [Q(1)]
        poly = [Q(0)] * (degree + 1)
        for j, c in enumerate(cs):
            for k, v in enumerate(binom):
                poly[k] += c * v
            binom = mul_linear(binom, Q(-rho - j * period, period * (j + 1)), Q(1, period * (j + 1)))
        check(poly[-1] == leading, "leading coefficient of residue polynomial")
        worst = max(worst, sum(map(abs, poly[:-1])) / leading)
    return worst


# ----------------------------------------------------------------------------
# Signed knots of prod(1 - q^{a_j})
# ----------------------------------------------------------------------------
def signed_knots(numbers):
    knots = {0: 1}
    for value in numbers:
        result = dict(knots)
        for s, sign in knots.items():
            result[s + value] = result.get(s + value, 0) - sign
        knots = result
    return sorted((s, c) for s, c in knots.items() if c)


# ----------------------------------------------------------------------------
# (A) exact finite check
# ----------------------------------------------------------------------------
def bval(e, u):
    return sum(c * comb(u, j) for j, c in enumerate(e)) if u >= 0 else None


def breaks(e, lo, hi):
    """Points in [lo, hi] such that p(u)=sum e_j binom(u,j) is monotone between consecutive points."""
    pts = {lo, hi}
    if len(e) <= 2 or hi - lo <= 1:
        return pts
    r = e[1:]                       # forward difference, on [lo, hi-1]
    rb = sorted(breaks(r, lo, hi - 1))
    pts.update(rb)
    for a, b in zip(rb, rb[1:]):
        ra, rbv = bval(r, a), bval(r, b)
        if (ra >= 0) != (rbv >= 0):
            target = rbv >= 0
            lo2, hi2 = a + 1, b     # first t in (a, b] with class(r(t)) == target
            while lo2 < hi2:
                mid = (lo2 + hi2) // 2
                if (bval(r, mid) >= 0) == target:
                    hi2 = mid
                else:
                    lo2 = mid + 1
            pts.add(lo2)
    return pts


def integer_minimum(values, length):
    """Exact minimum over u=0..length-1 of the integer polynomial interpolating values at u=0..d."""
    e = []
    row = list(values)
    while row:
        e.append(row[0])
        row = [b - a for a, b in zip(row, row[1:])]
    pts = breaks(e, 0, length - 1)
    return min(bval(e, u) for u in pts)


def finite_check(m, n, pieces, period):
    """Return min_{0<=k<=K} Delta p_k for P_{m,n}, K = floor(deg/2), using h for weights F_2..F_n."""
    nums = F[m + 1:m + n + 1]
    deg = sum(nums) - sum(F[1:n + 1])
    centre = deg // 2
    knots = signed_knots(nums)
    pts = sorted({0, centre + 1, *(s for s, c in knots if 0 < s <= centre)})
    d = n - 2
    best = None
    for lo, hi in zip(pts, pts[1:]):
        active = [(s, c) for s, c in knots if s <= lo]
        for rho in range(period):
            first = lo + (rho - lo) % period
            if first >= hi:
                continue
            length = (hi - 1 - first) // period + 1
            samples = min(d + 1, length)
            vals = [sum(c * h_eval(pieces, period, first + u * period - s) for s, c in active)
                    for u in range(samples)]
            if length <= d + 1:
                local = min(vals)
            else:
                local = integer_minimum(vals, length)
            best = local if best is None else min(best, local)
    return best, centre


def dense_minimum(m, n):
    p = [1]
    for a in F[m + 1:m + n + 1]:
        cp = p + [0] * a
        for j, c in enumerate(p):
            cp[j + a] -= c
        p = cp
    for w in F[1:n + 1]:
        for j in range(w, len(p)):
            p[j] += p[j - w]
        check(not any(p[-w:]), "dense division")
        p = p[:-w]
    check(p == p[::-1], "symmetry")
    c = (len(p) - 1) // 2
    return min([p[0]] + [p[k] - p[k - 1] for k in range(1, c + 1)])


# ----------------------------------------------------------------------------
# (B) limiting-spline certificate
# ----------------------------------------------------------------------------
def signed_margin(knots, left, right, d, sign):
    points = sorted({left, right, *(s for s, c in knots if left < s < right)})

    def lower(a, b, depth=0):
        cs = [sum(sign * c * comb(d, j) * (a - s) ** (d - j) * (b - a) ** j
                  for s, c in knots if s <= a) for j in range(d + 1)]
        bs = [sum(cs[j] * Q(comb(i, j), comb(d, j)) for j in range(i + 1)) for i in range(d + 1)]
        if min(bs) > 0:
            return min(bs)
        check(depth < 40, "Bernstein subdivision did not certify a positive margin")
        mid = (a + b) / 2
        return min(lower(a, mid, depth + 1), lower(mid, b, depth + 1))

    return min(lower(a, b) for a, b in zip(points, points[1:]))


def spline_certificate(n, threshold, eps1, eps2, pieces_by_r, period):
    T = F[threshold + 1]
    bstar = Q(F[threshold + 1], F[threshold])
    delta = max(abs(Q(F[threshold + 2], F[threshold + 1]) - bstar),
                abs(Q(F[threshold + 3], F[threshold + 2]) - bstar))
    # every later ratio F_{k+1}/F_k (k >= threshold+1) lies between the two ratios above
    v = [Q(1)] + [F[j - 2] + F[j - 1] * bstar for j in range(2, n + 1)]
    shift = (F[n + 1] - 1) * delta
    centre = sum(v) / 2
    X = centre + eps2 + 1
    tol = shift / 2 + Q(sum(F[1:n + 1]) + 4, 2 * T)
    check(tol < (eps2 - eps1) / 2, "centre tolerance")
    knots = signed_knots(v)
    report = {}
    for r in (1, 2):
        d = n - 1 - r
        weights = F[r + 1:n + 1]
        leading = Q(1, factorial(d) * prod(weights))
        C = error_constant(pieces_by_r[r], period, d, leading)
        lo, hi, sgn = (Q(1), centre - eps1, 1) if r == 1 else (centre - eps2, centre + eps2, -1)
        margin = signed_margin(knots, lo, hi, d, sgn)
        ratio_error = 2 ** n * d * X ** (d - 1) * shift
        partition_error = 2 ** n * C * (X + 1) ** (d - 1) / T
        check(margin > ratio_error + partition_error, f"spline margin r={r}: {float(margin)} vs {float(ratio_error)} + {float(partition_error)}")
        report[f"r{r}"] = dict(interval=[str(lo), str(hi)], degree=d, margin=float(margin),
                               error_bound=float(ratio_error + partition_error),
                               error_constant=float(C))
    report.update(threshold=threshold, delta=float(delta), centre=float(centre),
                  eps1=str(eps1), eps2=str(eps2), centre_tolerance=float(tol))
    return report


def run(n, threshold, eps1, eps2):
    period = lcm(*F[1:n + 1])
    pieces = {r: interpolant(F[r + 1:n + 1], period) for r in (1, 2)}
    # residue formulas agree with direct denumerants well beyond the samples
    for r in (1, 2):
        direct = denumerants(F[r + 1:n + 1], period * (n + 1) + 3000)
        check(all(h_eval(pieces[r], period, k) == c for k, c in enumerate(direct)), "residue formula")
    t0 = time.time()
    spline = spline_certificate(n, threshold, eps1, eps2, pieces, period)
    t1 = time.time()
    minima = {}
    for m in range(n, threshold):
        best, centre = finite_check(m, n, pieces[1], period)
        check(best >= 0, f"unimodality fails at m={m}")
        minima[m] = best
    t2 = time.time()
    dense = {}
    for m in range(n, n + 6):
        dm = dense_minimum(m, n)
        check(dm == minima[m], f"dense cross-check m={m}")
        dense[m] = dm
    out = dict(width=n, period=period, spline=spline,
               finite_minima={str(m): v for m, v in minima.items()},
               strict_from=min(m for m in minima if all(minima[k] >= 1 for k in minima if k >= m)),
               dense_cross_check=list(dense), seconds=dict(spline=round(t1 - t0, 1), finite=round(t2 - t1, 1)))
    return out


if __name__ == "__main__":
    n = int(sys.argv[1])
    threshold = int(sys.argv[2])
    eps1 = Q(sys.argv[3]) if len(sys.argv) > 3 else Q(1, 8)
    eps2 = Q(sys.argv[4]) if len(sys.argv) > 4 else Q(1, 4)
    result = run(n, threshold, eps1, eps2)
    print(json.dumps(result, indent=1))
