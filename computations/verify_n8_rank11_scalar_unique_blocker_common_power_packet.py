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
    "verify_four_site_arbitrary_superposition_dressed_packet_obstruction.py":
        "6c83e9a4bf925a47f69feef2465bac9ede5ad16704f462212a8119fb9d5db497",
    "verify_rank_one_rank_one_scalar_gate_three_target_cofactor_unit.py":
        "fa762d646596638d8fba8ff9fe2e4bd9f4592e27ed81cdf3f4fac8e42f1225e9",
    "verify_rank_one_rank_one_scalar_gate_rank2_common_missing_unit.py":
        "d5c6fc8f20c48269f3e1bae1c79e7ee5c34c660cf615c388ae3e8e358a41e9c0",
}
EXPECTED_LEDGER_DIGEST = "ff1de944007e724149c2eeb45d5724614b60aaa2f3bbaf5b24c70c6b156ade20"

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


def projective_vectors():
    """Primitive representatives of P^2 over the {-1,0,1} audit grid."""
    answer = []
    for vector in product((-1, 0, 1), repeat=3):
        if vector == (0, 0, 0):
            continue
        first = next(value for value in vector if value)
        normalized = vector if first == 1 else tuple(-value for value in vector)
        if normalized not in answer:
            answer.append(normalized)
    return tuple(answer)


def tensor(left, right):
    return tuple(a * b for a in left for b in right)


def dependent_three(first, second, third):
    """Exact rank<=2 test for three nonproportional integer vectors."""
    pivot = next(
        ((i, j, first[i] * second[j] - first[j] * second[i])
         for i in range(len(first)) for j in range(i + 1, len(first))
         if first[i] * second[j] != first[j] * second[i]),
        None,
    )
    require(pivot is not None, "projective tensors became proportional")
    i, j, determinant = pivot
    alpha = third[i] * second[j] - third[j] * second[i]
    beta = first[i] * third[j] - first[j] * third[i]
    return all(determinant * third[k] == alpha * first[k] + beta * second[k]
               for k in range(len(first)))


def segre_line_census():
    """Regression audit for the three-rank-one-tensor alignment lemma."""
    vectors = projective_vectors()
    points = tuple((left, right, tensor(left, right))
                   for left in vectors for right in vectors)
    dependent = 0
    for indices in combinations(range(len(points)), 3):
        selected = tuple(points[index] for index in indices)
        if not dependent_three(*(entry[2] for entry in selected)):
            continue
        dependent += 1
        left_aligned = len({entry[0] for entry in selected}) == 1
        right_aligned = len({entry[1] for entry in selected}) == 1
        require(left_aligned or right_aligned,
                ("a distinct dependent Segre triple left both rulings", indices))
    require(len(vectors) == 13 and len(points) == 169,
            "projective Segre audit grid changed")
    return len(vectors), len(points), dependent


def audit():
    dependency_guard()
    e_left = contracted_power(2)
    e_right = e_formula()
    f_left = contracted_power(3)
    f_right = f_formula()
    require(e_left == e_right, "the exact E common-power formula failed")
    require(f_left == f_right, "the exact F common-power formula failed")
    blockers = blocker_census()
    segre = segre_line_census()
    ledger = (
        len(e_left), sum(e_left.values()),
        len(f_left), sum(f_left.values()), blockers, segre,
        tuple(sorted(e_left.items())), tuple(sorted(f_left.items())),
    )
    digest = sha256(repr(ledger).encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST is not None:
        require(digest == EXPECTED_LEDGER_DIGEST,
                ("unique-blocker ledger changed", digest))
    return len(e_left), len(f_left), segre, digest


def main():
    e_terms, f_terms, segre, digest = audit()
    print("N=8 scalar-shore unique-blocker common-power packet: passed")
    print(f"  contracted q^[2] monomials : {e_terms}")
    print(f"  contracted q^[3] monomials : {f_terms}")
    print("  blocker patterns audited   : 8 per target label")
    print(f"  Segre line census          : {segre[2]} dependent triples")
    print(f"  aggregate ledger digest    : {digest}")
    print("  conclusion                 : unique blocker is a literal four-site secant packet")


if __name__ == "__main__":
    main()
