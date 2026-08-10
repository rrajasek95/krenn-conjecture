#!/usr/bin/env python3
"""Exact physical curvature/q-zero lower-face obstruction at h=3.

The automatic overlap rows compare perfect matchings inside one decorated
four-site word.  The endpoint bridge needed by the q-zero order-four symbol
changes that word.  Even inside one word, the committed old-cap landing
identifies matching-polar q-augmentation and ordinary residue, so curvature
differences cannot give its nonzero invisible lower face.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json


EXPECTED_DIGEST = "23f9575e8b40f0e5991cf5de8ed5af29711250ec54f51c399002c79a3c8561e8"
COLORS = tuple(range(3))
VERTICES = ("x", "v", "p", "q")
ODD_WORD = (1, 2, 1, 1, 2)
MATCHINGS = (
    (("x", "v"), ("p", "q")),
    (("x", "p"), ("v", "q")),
    (("x", "q"), ("v", "p")),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return (left, right) if VERTICES.index(left) < VERTICES.index(right) else (right, left)


def decorated_cell(pair, word):
    left, right = edge(*pair)
    colors = dict(zip(VERTICES, word, strict=True))
    return left, right, colors[left], colors[right]


def decorated_matching(index, word):
    return tuple(sorted(decorated_cell(pair, word) for pair in MATCHINGS[index]))


def rank(rows):
    work = [list(map(F, row)) for row in rows]
    if not work:
        return 0
    answer = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(answer, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right
                         for left, right in zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def add(left, right):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, F(0)) + coefficient
        if not result[monomial]:
            del result[monomial]
    return result


def scale(value, polynomial):
    return {monomial: F(value) * coefficient
            for monomial, coefficient in polynomial.items() if value * coefficient}


def variable(name):
    return {(name,): F(1)}


def multiply(*polynomials):
    result = {(): F(1)}
    for polynomial in polynomials:
        output = {}
        for left, left_value in result.items():
            for right, right_value in polynomial.items():
                monomial = tuple(sorted(left + right))
                output[monomial] = output.get(monomial, F(0)) + left_value * right_value
        result = {monomial: coefficient for monomial, coefficient in output.items()
                  if coefficient}
    return result


def subtract(left, right):
    return add(left, scale(-1, right))


def symbolic_automatic_normal():
    """Verify the selected fixed-label connection/normal identity."""
    A, B, Fq, U = (variable(name) for name in ("A", "B", "F", "U"))
    z, x, y, t, v, E = (variable(name) for name in ("z", "x", "y", "t", "v", "E"))
    f = add(multiply(A, z), multiply(x, y))
    g = add(multiply(B, z), multiply(x, t))
    H = add(add(multiply(A, v), multiply(E, y)), multiply(Fq, x))
    N = add(add(multiply(B, v), multiply(E, t)), multiply(U, x))
    D = subtract(multiply(A, t), multiply(B, y))
    kappa = subtract(multiply(A, U), multiply(B, Fq))
    connection = subtract(subtract(multiply(f, t), multiply(g, y)), multiply(D, z))
    normal = subtract(
        add(add(multiply(U, f), multiply(t, H)),
            add(scale(-1, multiply(Fq, g)), scale(-1, multiply(y, N)))),
        add(multiply(D, v), multiply(kappa, z)),
    )
    require(not connection, "automatic connection identity changed")
    require(not normal, "automatic curvature-normal identity changed")
    return kappa


def apply_global_permutation(word, permutation):
    return tuple(permutation[color] for color in word)


def main():
    kappa_polynomial = symbolic_automatic_normal()
    require(kappa_polynomial == {
        ("A", "U"): F(1),
        ("B", "F"): F(-1),
    }, "selected curvature sign changed")

    # Every fixed-label K4 curvature face joins two of the three perfect
    # matchings in one decorated vertex word.  Decorated matching monomials
    # determine that word uniquely, so the graph has exactly 3^4 triangular
    # components and cannot transport between vertex words.
    nodes = {}
    adjacency = {}
    curvature_faces = 0
    for word in product(COLORS, repeat=4):
        local = [decorated_matching(index, word) for index in range(3)]
        require(len(set(local)) == 3, "a decorated K4 matching collided")
        for node in local:
            previous = nodes.setdefault(node, word)
            require(previous == word, "a decorated matching lost its vertex word")
            adjacency.setdefault(node, set())
        for left, right in combinations(local, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)
            curvature_faces += 1
    require(len(nodes) == 243, "decorated matching census changed")
    require(curvature_faces == 243, "decorated curvature-face census changed")

    # Connected-component replay, independent of the construction order.
    unseen = set(nodes)
    components = []
    while unseen:
        start = next(iter(unseen))
        stack = [start]
        component = set()
        while stack:
            node = stack.pop()
            if node in component:
                continue
            component.add(node)
            stack.extend(adjacency[node] - component)
        unseen -= component
        components.append(component)
    require(len(components) == 81, "curvature word-component count changed")
    require(all(len(component) == 3 for component in components),
            "a curvature component stopped being a K3")

    # The physical endpoint bridge used by the order-four construction is
    #   old: (x,v,p,q)=(0,m_v,2,2),
    #   new: (x,v,p,q)=(0,0,0,0),
    # on the SAME physical matching xv|pq.  Fixed-label curvature never
    # changes the decorated word.  A global target colour permutation does
    # not help, because it preserves inequality of the labels.
    bridge_records = []
    for deleted, middle_color in enumerate(ODD_WORD):
        old_word = (0, middle_color, 2, 2)
        new_word = (0, 0, 0, 0)
        old_node = decorated_matching(0, old_word)
        new_node = decorated_matching(0, new_word)
        require(nodes[old_node] == old_word and nodes[new_node] == new_word,
                "endpoint bridge node lost its word")
        require(old_word != new_word, "old and zero endpoint words collided")
        require(new_node not in adjacency[old_node],
                "one curvature face unexpectedly performed endpoint recolouring")
        old_component = next(component for component in components if old_node in component)
        require(new_node not in old_component,
                "a sum of fixed-label curvature faces performed endpoint recolouring")
        permutation_checks = 0
        for permutation in permutations(COLORS):
            permuted_old = apply_global_permutation(old_word, permutation)
            permuted_new = apply_global_permutation(new_word, permutation)
            require(permuted_old != permuted_new,
                    "global colour permutation erased the bridge mismatch")
            permutation_checks += 1
        bridge_records.append({
            "deleted_face": deleted,
            "m_v": middle_color,
            "old_word": list(old_word),
            "new_word": list(new_word),
            "global_permutations_checked": permutation_checks,
            "same_curvature_component": False,
        })

    # Each of the three external matching polars of a fixed mixed word has
    # coefficient one under q-augmentation.  Under the ONLY COMMITTED
    # landing into the old split cap, the reset goes to the ordinary-response
    # generator rho and hence has the same coefficient in ores.  This is a
    # diagnostic obstruction to that landing, not a construction or theorem
    # about the still-undefined physical ores map on a new attaching chain.
    qaug = [F(1), F(1), F(1)]
    ores = [F(1), F(1), F(1)]
    require(rank([qaug, ores]) == 1, "old-cap qaug/ores lock changed")
    desired = [F(1), F(0)]
    readout_columns = [[qaug[index], ores[index]] for index in range(3)]
    require(rank(readout_columns) == 1, "matching-face readout rank changed")
    require(rank(readout_columns + [desired]) == 2,
            "an invisible nonzero q-augmentation entered the matching-face span")
    for left, right in combinations(range(3), 2):
        difference = [F(index == left) - F(index == right) for index in range(3)]
        require(sum(qaug[index] * difference[index] for index in range(3)) == 0,
                "curvature difference retained q-augmentation")
        require(sum(ores[index] * difference[index] for index in range(3)) == 0,
                "curvature difference retained ordinary residue")

    # Polynomial-weighted form: any weighted physical matching-face sum has
    # qaug=ores.  In particular the selected determinant signs (+,-) either
    # retain kappa in BOTH readouts or cancel it in BOTH; they cannot produce
    # (kappa,0) on the active open.
    weighted_records = []
    for left_weight, right_weight in (
        (F(2), F(1)),
        (F(5, 3), F(-7, 4)),
        (F(-2), F(-5)),
    ):
        value = left_weight - right_weight
        require(value != 0, "curvature weight probe accidentally vanished")
        weighted_readout = (value, value)
        require(weighted_readout != (value, F(0)),
            "curvature weights created an invisible lower face in the old cap")
        weighted_records.append({
            "left": str(left_weight),
            "right": str(right_weight),
            "qaug": str(value),
            "ordinary_residue": str(value),
        })

    # The residual four-site odd word is mixed for every deleted face, so
    # the physical target of every polar used above is genuinely zero.
    residual_words = []
    for deleted in range(len(ODD_WORD)):
        residual = ODD_WORD[:deleted] + ODD_WORD[deleted + 1:]
        require(len(set(residual)) == 2, "a q-zero face acquired pure target")
        residual_words.append(list(residual))

    ledger = {
        "automatic_rows": "fixed-label connection and curvature normal",
        "kappa_sign": "A*U-B*F",
        "decorated_matching_nodes": len(nodes),
        "curvature_faces": curvature_faces,
        "curvature_components": len(components),
        "component_sizes": sorted({len(component) for component in components}),
        "bridge_records": bridge_records,
        "residual_mixed_words": residual_words,
        "committed_old_cap_matching_face_readout_rank": rank(readout_columns),
        "committed_old_cap_rank_with_invisible_qaug": rank(readout_columns + [desired]),
        "weighted_sign_probes": weighted_records,
        "verdict": "fixed-label curvature misses the endpoint bridge; the old-cap landing also locks qaug to ores",
    }
    digest = sha256(json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    require(EXPECTED_DIGEST != "TO_BE_FILLED", "pin EXPECTED_DIGEST")
    require(digest == EXPECTED_DIGEST, ("ledger digest changed", digest, ledger))
    print("h=3 physical curvature/q-zero lower-face obstruction: PASS")
    print("decorated curvature components: 81 triangles")
    print("endpoint 22-to-00 bridge components hit: 0/5")
    print("old-cap matching-face qaug/ordinary-residue rank: 1; desired raises to 2")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
