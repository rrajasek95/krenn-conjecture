"""Exact tensor lifting behind the rank-independent star estimate."""

from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT/"computations/flat-core-rigidity-2026-09-27"))
from algebra import (E, ZERO, ONE, OMEGA, require, rank, clean, norm2,
                     restrict, outputs, four_outputs, four_derivative, five_core)

PERMS = list(permutations(range(3)))


def sym_lift(factors):
    """Factors have one center index each, and disjoint labelled leaf indices."""
    result = {}
    for chosen in product(*factors):
        leaves = [None]*5
        center = []
        value = ONE
        for (s, assignments), z in chosen:
            center.append(s)
            value *= z
            for i, a in assignments:
                require(leaves[i-1] is None, "Each leaf index occurs in exactly one factor")
                leaves[i-1] = a
        require(all(a is not None for a in leaves), "All five leaf indices occur")
        for order in PERMS:
            key = tuple(center[i] for i in order)+tuple(leaves)
            result[key] = result.get(key, ZERO)+value/6
    return clean(result)


def arm_factor(G, i):
    return [((s, ((i, a),)), z) for (s, a), z in G.items() if z]


def response_factor(R, triple):
    return [((word[0], tuple(zip(triple, word[1:]))), z) for word, z in R.items() if z]


def edge_lift(B, edge, G):
    # Attach the edge as extra leaf indices on one arm. Its norm factors
    # because its leaves are distinct from all three arm leaves.
    rest = [i for i in range(1, 6) if i not in edge]
    factors = [arm_factor(G[i], i) for i in rest]
    i, j = edge
    factors[0] = [((s, assignments+((i, a), (j, b))), z*w)
                  for (s, assignments), z in factors[0]
                  for (a, b), w in B.items() if w]
    return sym_lift(factors)


def add(*tensors):
    result = {}
    for tensor in tensors:
        for key, value in tensor.items():
            result[key] = result.get(key, ZERO)+value
    return clean(result)


def fixture(q, mode, k=5):
    G = {}
    for i in range(1, k+1):
        if mode == "identity":
            G[i] = {(a, a): ONE for a in range(q)}
        elif mode == "common_rank_one":
            G[i] = {(0, 0): E(i+1)}
        elif mode == "distinct_rank_one":
            u = [E(i+a+1, (i+a) % 2) for a in range(q)]
            v = [E(a+1, i % 2) for a in range(q)]
            G[i] = {(a, b): u[a]*v[b] for a, b in product(range(q), repeat=2)}
        elif mode == "basis_rank_one":
            G[i] = {((i-1) % q, i % q): ONE}
        elif mode == "mixed_ranks":
            G[i] = ({(a, a): E(a+1) for a in range(q)} if i % 2
                    else {(0, b): E(b+1, i % 3) for b in range(q)})
        else:
            raise ValueError("Unknown fixture")
    B = {(i, j): clean({(a, b): E((i+2*j+a+3*b) % 5-2,
                                  (i+j+2*a+b) % 3-1)
                        for a, b in product(range(q), repeat=2)})
         for i, j in combinations(range(1, k+1), 2)}
    source = {(0, i, a, b): z for i, block in G.items() for (a, b), z in block.items()}
    source.update({(i, j, a, b): z for (i, j), block in B.items() for (a, b), z in block.items()})
    return G, B, source


def check_fixture(q, mode, lift=True, k=5):
    G, B, source = fixture(q, mode, k)
    R = {triple: outputs(restrict(source, (0,)+triple), n=4, colors=q)
         for triple in combinations(range(1, k+1), 3)}
    a2, M2 = min(map(norm2, G.values())), max(map(norm2, G.values()))
    observed = sum(map(norm2, R.values()))
    leaf_strength = sum(map(norm2, B.values()))
    lower = Fraction(k-2, 18)*a2**3/M2**2*leaf_strength
    require(observed >= lower, "Rank-independent coercivity in a complex fixture")
    record = dict(colors=q, leaves=k, arms=mode, min_arm_squared=str(a2),
                  max_arm_squared=str(M2), response_squared=str(observed),
                  lower_bound=str(lower))
    if lift:
        require(k == 5, "The direct lift uses five leaves")
        Z = {edge: edge_lift(block, edge, G) for edge, block in B.items()}
        Y = {}
        for triple, response in R.items():
            rest = [i for i in range(1, 6) if i not in triple]
            lifted = sym_lift([response_factor(response, triple),
                               *(arm_factor(G[i], i) for i in rest)])
            require(lifted == add(*(Z[edge] for edge in combinations(triple, 2))),
                    "Every tensor coefficient of the lifted matching identity")
            Y[triple] = lifted
            require(norm2(lifted) <= M2**2*norm2(response), "Symmetrization upper bound")
        for edge, lifted in Z.items():
            require(norm2(lifted) >= a2**3*norm2(B[edge])/6,
                    "Three-arm symmetrization lower bound")
        y2, z2 = sum(map(norm2, Y.values())), sum(map(norm2, Z.values()))
        row2 = sum(norm2(add(*(Z[edge] for edge in Z if i in edge))) for i in range(1, 6))
        require(y2 == z2+row2, "Hilbert-valued five-leaf incidence norm identity")
        record.update(lifted_response_squared=str(y2), lifted_edge_squared=str(z2),
                      lifted_row_squared=str(row2))
    if k == 5 and q <= 2:
        base = {(0, i, a, b): z for i, block in G.items() for (a, b), z in block.items()}
        _, rows = four_derivative(base, k+1, q)
        actual = rank(list(rows.values()))
        require(actual == q*q*k*(k-1)//2, "Star derivative rank survives matrix rank loss")
        record["derivative_rank"] = actual
    return record


def check_symmetrization():
    # Independent vector-level check of the Gram-permanent formula.
    records = []
    for vectors in (
        [[ONE, ZERO, ZERO], [ZERO, ONE, ZERO], [ZERO, ZERO, ONE]],
        [[ONE, ONE], [ONE, OMEGA], [ONE, OMEGA*OMEGA]],
        [[E(2, 1), E(-1)], [E(1, -2), E(3)], [E(2), E(1, 1)]],
    ):
        q = len(vectors[0])
        sym = {}
        for word in product(range(q), repeat=3):
            sym[word] = sum((vectors[0][word[p[0]]]*vectors[1][word[p[1]]]
                             *vectors[2][word[p[2]]] for p in PERMS), ZERO)/6
        gram = [[sum((x.conjugate()*y for x, y in zip(u, v)), ZERO)
                 for v in vectors] for u in vectors]
        permanent = sum((gram[0][p[0]]*gram[1][p[1]]*gram[2][p[2]]
                         for p in PERMS), ZERO)
        product_norm = 1
        for u in vectors:
            product_norm *= sum(x.abs2() for x in u)
        require(permanent == E(6*norm2(sym)), "Gram permanent equals six symmetric norms")
        require(6*norm2(sym) >= product_norm, "Three-vector lower bound")
        records.append(dict(norm_squared=str(norm2(sym)), product_norm_squared=str(product_norm)))
    require(records[0]["norm_squared"] == "1/6", "Orthogonal vectors attain the one-sixth factor")
    return records


def check():
    cases = [(1, "identity"), (2, "identity"), (2, "common_rank_one"),
             (2, "distinct_rank_one"), (2, "mixed_ranks"), (3, "basis_rank_one")]
    fixtures = [check_fixture(q, mode) for q, mode in cases]
    fixtures.append(check_fixture(2, "mixed_ranks", lift=False, k=6))
    # Removing the fifth arm admits the non-star cube-root flat source.
    critical = five_core()
    require(not four_outputs(critical, 5, 1), "Four-leaf counterexample is flat")
    require(all(critical.get((i, 4, 0, 0), ZERO) for i in range(4)),
            "All four arms are nonzero")
    require(any(i < j < 4 for i, j, a, b in critical),
            "The four-leaf counterexample has nonzero leaf edges")
    return dict(fixtures=fixtures, vector_symmetrization=check_symmetrization(),
                four_leaf_extension="REJECTED by exact cube-root core")
