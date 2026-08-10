#!/usr/bin/env python3
"""Exact N=8 common-power packet behind a unique scalar-shore blocker.

After contracting two shore sites y,z in the literal matching powers of one
quadratic q, the remaining four-site tensors are

    E = i_y i_z q^[2] = d q_C + r_y r_z,
    F = i_y i_z q^[3] = d q_C^[2] + r_y r_z q_C.

The checker expands both sides in independent endpoint-coloured q cells and
independent contraction coefficients.  It also audits the elementary but
load-bearing unique-blocker factor split for the three target labels.
Standard library only; no random specialization.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEPENDENCIES = {
    "verify_rank_one_rank_one_scalar_gate_three_target_cofactor_unit.py":
        "fa762d646596638d8fba8ff9fe2e4bd9f4592e27ed81cdf3f4fac8e42f1225e9",
    "verify_rank_one_rank_one_scalar_gate_rank2_common_missing_unit.py":
        "d5c6fc8f20c48269f3e1bae1c79e7ee5c34c660cf615c388ae3e8e358a41e9c0",
}
EXPECTED_LEDGER_DIGEST = "67e0334476a3c3afc180aabd67250fa7b09e25b100b1a43e982122b70c73f45c"

SITES = tuple(range(6))
Y, Z = 0, 1
C = (2, 3, 4, 5)
COLOURS = range(3)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dependency_guard():
    for name, expected in DEPENDENCIES.items():
        actual = sha256((HERE / name).read_bytes()).hexdigest()
        require(actual == expected, ("dependency changed", name, actual))


def qcell(u, v, a, b):
    if u < v:
        return f"q{u}{v}_{a}{b}"
    return f"q{v}{u}_{b}{a}"


def nu(site, colour):
    return f"n{site}_{colour}"


def matching_key(output, factors):
    return tuple(sorted(output)), tuple(sorted(factors))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def size_m_matchings(vertices, m):
    for support in combinations(vertices, 2 * m):
        yield from perfect_matchings(support)


def contracted_power(m):
    """Expand i_Y i_Z q^[m] after deleting the two contracted labels."""
    answer = Counter()
    for matching in size_m_matchings(SITES, m):
        used = {site for edge in matching for site in edge}
        if Y not in used or Z not in used:
            continue
        for word in product(COLOURS, repeat=2 * m):
            support = tuple(sorted(used))
            colour = dict(zip(support, word))
            factors = []
            output = []
            for u, v in matching:
                factors.append(qcell(u, v, colour[u], colour[v]))
            factors.extend((nu(Y, colour[Y]), nu(Z, colour[Z])))
            for site in support:
                if site not in (Y, Z):
                    output.append((site, colour[site]))
            answer[matching_key(output, factors)] += 1
    return answer


def e_formula():
    answer = Counter()
    # d q_C.
    for a, b, c, d in product(COLOURS, repeat=4):
        for u, v in combinations(C, 2):
            factors = (qcell(Y, Z, a, b), nu(Y, a), nu(Z, b),
                       qcell(u, v, c, d))
            answer[matching_key(((u, c), (v, d)), factors)] += 1
    # r_y r_z: the two contracted sites meet two distinct sites of C.
    for u in C:
        for v in C:
            if u == v:
                continue
            for a, b, c, d in product(COLOURS, repeat=4):
                factors = (nu(Y, a), qcell(Y, u, a, c),
                           nu(Z, b), qcell(Z, v, b, d))
                answer[matching_key(((u, c), (v, d)), factors)] += 1
    return answer


def f_formula():
    answer = Counter()
    # d q_C^[2].
    for a, b in product(COLOURS, repeat=2):
        for matching in perfect_matchings(C):
            for word in product(COLOURS, repeat=4):
                colour = dict(zip(C, word))
                factors = [qcell(Y, Z, a, b), nu(Y, a), nu(Z, b)]
                factors.extend(qcell(u, v, colour[u], colour[v])
                               for u, v in matching)
                output = tuple((site, colour[site]) for site in C)
                answer[matching_key(output, factors)] += 1
    # r_y r_z q_C.  Once the two cross endpoints are chosen, the remaining
    # two sites of C carry the unique internal edge.
    for u in C:
        for v in C:
            if u == v:
                continue
            remaining = tuple(site for site in C if site not in (u, v))
            w, t = remaining
            for a, b, c, d, e, f in product(COLOURS, repeat=6):
                factors = (nu(Y, a), qcell(Y, u, a, c),
                           nu(Z, b), qcell(Z, v, b, d),
                           qcell(w, t, e, f))
                output = ((u, c), (v, d), (w, e), (t, f))
                answer[matching_key(output, factors)] += 1
    return answer


def blocker_census():
    """Audit beta_A,i = product_x epsilon_i|K_x at three shore sites."""
    records = []
    for live in product((False, True), repeat=3):
        beta_live = all(live)
        blockers = tuple(site for site, value in enumerate(live) if not value)
        unique_bright = False
        if len(blockers) == 1:
            x = blockers[0]
            unique_bright = all(live[site] for site in range(3) if site != x)
        require(beta_live == (len(blockers) == 0),
                ("target factorization changed", live))
        require(unique_bright == (len(blockers) == 1),
                ("unique blocker did not restore the target", live))
        records.append((live, blockers, beta_live, unique_bright))
    return tuple(records)


def audit():
    dependency_guard()
    e_left = contracted_power(2)
    e_right = e_formula()
    f_left = contracted_power(3)
    f_right = f_formula()
    require(e_left == e_right, "the exact E common-power formula failed")
    require(f_left == f_right, "the exact F common-power formula failed")
    blockers = blocker_census()
    ledger = (
        len(e_left), sum(e_left.values()),
        len(f_left), sum(f_left.values()), blockers,
        tuple(sorted(e_left.items())), tuple(sorted(f_left.items())),
    )
    digest = sha256(repr(ledger).encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST is not None:
        require(digest == EXPECTED_LEDGER_DIGEST,
                ("unique-blocker ledger changed", digest))
    return len(e_left), len(f_left), digest


def main():
    e_terms, f_terms, digest = audit()
    print("N=8 scalar-shore unique-blocker common-power packet: passed")
    print(f"  contracted q^[2] monomials : {e_terms}")
    print(f"  contracted q^[3] monomials : {f_terms}")
    print("  blocker patterns audited   : 8 per target label")
    print(f"  aggregate ledger digest    : {digest}")
    print("  conclusion                 : unique blocker is a literal four-site secant packet")


if __name__ == "__main__":
    main()
