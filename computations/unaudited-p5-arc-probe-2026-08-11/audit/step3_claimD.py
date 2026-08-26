#!/usr/bin/env python3
"""Claim (D): the linearized Markov sequence c_i = dQ_{k+i}/dr_k.

Two things are checked:
 1. reproduce c_3 and c_4 for k=4 independently (interpolation, not duals),
    on the same three-step-recurrence arc the prototype used;
 2. decide whether c_4 = C*u*e1 is actually what the transfer conjecture
    requires, given the measured scope of the committed identities
    (step2 showed Q8 = C*u*W5 only MODULO W4).
"""
from fractions import Fraction as QQ
import time

from myarc import Arc, collapse, committed_point, load_base
from step1_claimA import solve_linear, g_relation


def interpolate(samples):
    """Exact Lagrange fit; returns coefficient list (ascending) of the unique
    polynomial of degree < len(samples) through the samples."""
    n = len(samples)
    coefficients = [QQ(0)] * n
    for i, (xi, yi) in enumerate(samples):
        basis = [QQ(1)]
        denominator = QQ(1)
        for j, (xj, _) in enumerate(samples):
            if i == j:
                continue
            basis = [QQ(0)] + basis
            for k in range(len(basis) - 1):
                basis[k] -= xj * basis[k + 1]
            denominator *= xi - xj
        scale = yi / denominator
        for k, value in enumerate(basis):
            coefficients[k] += scale * value
    while coefficients and not coefficients[-1]:
        coefficients.pop()
    return coefficients


def main():
    t0 = time.time()
    data = load_base()
    point = committed_point(data)
    a = data["layout_a"]
    z = lambda i: point[a[i]]
    s = solve_linear(data["first_relation"], point, data["first_bend"])
    point[data["first_bend"]] = s
    t = solve_linear(data["second_relation"], point, data["second_bend"])
    r3 = g_relation(data, point, s, t)
    e1 = z(0) + z(30) + z(52)
    e2 = z(0) * z(30) + z(0) * z(52) + z(30) * z(52)
    e3 = z(0) * z(30) * z(52)
    C = QQ(1, 2) * z(11) * z(16) ** 2 * z(41)
    u = z(26) + z(45)

    dynamic = set(data["local_variables"]) | {a[46]}
    normal = [collapse(r, point, dynamic) for r in data["normal"]]
    transverse = [collapse(r, point, dynamic) for r in data["transverse"]]
    targets = [collapse(r, point, dynamic) for r in data["obstruction"]]

    order = 11
    k = 4

    def run(bends):
        arc = Arc(data, point, order)
        arc.set_bends(bends)
        return [arc.step(m, normal, transverse, targets)
                for m in range(1, order + 1)]

    def arc_bends(delta):
        """The three-step-recurrence arc with r_k shifted by delta, exactly as
        the prototype's dual-number perturbation does."""
        bends = [z(46), s, t, r3]
        while len(bends) <= order:
            bends.append(-(e1 * bends[-1] + e2 * bends[-2] + e3 * bends[-3]))
        bends[k] += delta
        return bends

    samples = [QQ(0), QQ(1), QQ(2), QQ(-1), QQ(3, 5)]
    runs = {d: run(arc_bends(d)) for d in samples}
    print(f"[{time.time()-t0:.1f}s] {len(samples)} arcs run to order {order}")

    print("\n--- c_i = dQ_{k+i}/dr_k on the three-step recurrence arc, k=4 ---")
    expected = {3: C * u, 4: C * u * e1, 5: C * u * e2, 6: C * u * e3}
    for i in range(0, order - k + 1):
        n = k + i
        pts30 = [(d, runs[d][n - 1][29]) for d in samples]
        coefficients = interpolate(pts30)
        degree = len(coefficients) - 1
        c = coefficients[1] if len(coefficients) > 1 else QQ(0)
        tag = ""
        if i in expected:
            tag = f"   conjectured {expected[i]}  match={c == expected[i]}"
        print(f"c_{i} = dQ_{n}/dr_4 = {c}   (Q_{n} has degree {degree} in r_4)"
              f"{tag}")

    print("\n--- degrees of Q_n in r_4 (nonlinearity check) ---")
    for n in range(k, order + 1):
        pts30 = [(d, runs[d][n - 1][29]) for d in samples]
        print(f"Q_{n}^M30 coefficients in (r_4 - r_4^rec): "
              f"{[str(x) for x in interpolate(pts30)]}")

    print("\n--- is c_4 = C*u*e1 actually required? ---")
    print("step2 showed Q8 - C*u*W5 = A * W4 for some cofactor A (nonzero).")
    print("On any arc with W4 = 0 that gives dQ8/dr4 = C*u*e1 + A, so the")
    print("conjecture in its committed (mod-W4) form does NOT force c_4.")
    c4 = interpolate([(d, runs[d][7][29]) for d in samples])[1]
    print(f"measured c_4 = {c4}; C*u*e1 = {C*u*e1}; "
          f"implied cofactor A = {c4 - C*u*e1}")
    print(f"\ntotal {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
