"""Complete six-vertex incidence-support classification and exact ground examples."""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "single-invertible-edge-ghz-2026-09-27"))
from edge_projection import Poly, T, require

VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
INDEX = {edge: i for i, edge in enumerate(EDGES)}
CIRCUITS = {
    "four_cycle": (((0, 1), 1), ((1, 2), -1), ((2, 3), 1), ((0, 3), -1)),
    "six_cycle": (((0, 1), 1), ((1, 2), -1), ((2, 3), 1),
                  ((3, 4), -1), ((4, 5), 1), ((0, 5), -1)),
    "two_triangles_one_vertex": (((0, 1), 1), ((1, 2), -1), ((0, 2), 1),
                                  ((0, 3), -1), ((3, 4), 1), ((0, 4), -1)),
    "two_triangles_one_bridge": (((0, 1), 1), ((1, 2), -1), ((0, 2), 1),
                                  ((0, 3), -2), ((3, 4), 1), ((4, 5), -1), ((3, 5), 1)),
}


def mask_of(edges):
    return sum(1 << INDEX[tuple(sorted(edge))] for edge in set(tuple(sorted(e)) for e in edges))


def adjacency(mask):
    result = [set() for _ in VERTICES]
    for k, (i, j) in enumerate(EDGES):
        if mask >> k & 1:
            result[i].add(j)
            result[j].add(i)
    return result


def bipartite_components(adj):
    colors = {}
    count = 0
    for root in VERTICES:
        if root in colors:
            continue
        colors[root] = 0
        stack = [root]
        bipartite = True
        while stack:
            i = stack.pop()
            for j in adj[i]:
                if j not in colors:
                    colors[j] = 1-colors[i]
                    stack.append(j)
                elif colors[j] == colors[i]:
                    bipartite = False
        count += bipartite
    return count


def labelled_circuits():
    families = {}
    for name, template in CIRCUITS.items():
        records = {}
        for perm in permutations(VERTICES):
            weights = {tuple(sorted((perm[i], perm[j]))): weight for (i, j), weight in template}
            require(all(weights.values()), "Every circuit edge has nonzero weight")
            require(all(sum(w for edge, w in weights.items() if i in edge) == 0
                        for i in VERTICES), "Explicit nonzero integer incidence-kernel witness")
            mask = mask_of(weights)
            if mask not in records:
                records[mask] = [weights.get(e, 0) for e in EDGES]
        families[name] = records
    require({k: len(v) for k, v in families.items()} == {
        "four_cycle": 45, "six_cycle": 60,
        "two_triangles_one_vertex": 90, "two_triangles_one_bridge": 90},
        "All labelled minimal supports")
    return families


def labelled_graphs(template):
    template = tuple(template)
    return {mask_of((perm[i], perm[j]) for i, j in template)
            for perm in permutations(VERTICES)}


def contains_outside_cycle(adj, i, j):
    outside = set(VERTICES)-{i, j}
    small = {tuple(sorted((r, s))) for r in outside for s in adj[r] & outside}
    small.update(combinations(sorted(adj[i] & outside), 2))
    small.update(combinations(sorted(adj[j] & outside), 2))
    return any(all(tuple(sorted((r, s))) in small
                   for r in pair for s in outside-set(pair))
               for pair in combinations(sorted(outside), 2))


def candidate_edges(adj):
    return [e for e in EDGES if e[1] not in adj[e[0]]
            and not adj[e[0]] & adj[e[1]] and not contains_outside_cycle(adj, *e)]


def check_graph_classification():
    families = labelled_circuits()
    circuits = {mask: weights for family in families.values() for mask, weights in family.items()}
    classes = {
        "four_cycle_two_isolates": set(families["four_cycle"]),
        "complete_four_two_isolates": labelled_graphs(combinations(range(4), 2)),
        "complete_bipartite_two_three_one_isolate":
            labelled_graphs([(i, j) for i in (0, 1) for j in (2, 3, 4)]),
        "two_triangles_one_bridge": set(families["two_triangles_one_bridge"]),
    }
    require([len(v) for v in classes.values()] == [45, 15, 60, 90],
            "Canonical remaining graph orbits")
    adjacencies = [adjacency(mask) for mask in range(1 << len(EDGES))]
    bipartite = [bipartite_components(adj) for adj in adjacencies]
    for circuit in circuits:
        require(circuit.bit_count()-(6-bipartite[circuit]) == 1,
                "Every circuit has one-dimensional incidence kernel")
    valid = []
    counts = Counter()
    zero_rows = Counter()
    remaining_counts = Counter()
    maximum_directions = {0: 0, 1: 0, 2: 0}
    edge_tests = 0
    for mask in range(1 << len(EDGES)):
        # Rank is 6 minus the number of bipartite connected components.
        rank_test = bool(mask) and all(
            bipartite[mask ^ (1 << k)] == bipartite[mask]
            for k in range(len(EDGES)) if mask >> k & 1)
        covered = 0
        for circuit in circuits:
            if mask & circuit == circuit:
                covered |= circuit
        circuit_test = bool(mask) and covered == mask
        require(rank_test == circuit_test, "Independent incidence-rank and circuit-cover tests agree")
        if not rank_test:
            continue
        valid.append(mask)
        adj = adjacencies[mask]
        isolated = sum(not neighbors for neighbors in adj)
        zero_rows[isolated] += 1
        require(isolated <= 2, "Nonempty balanced support has at least four active vertices")
        if max(map(len, adj)) >= 4:
            counts["degree_four_rule"] += 1
            continue
        if any(mask & cycle == cycle for cycle in families["six_cycle"]):
            counts["six_cycle_rule"] += 1
            continue
        names = [name for name, orbit in classes.items() if mask in orbit]
        require(len(names) == 1, "Complete list after degree-four and six-cycle rules")
        name = names[0]
        counts[name] += 1
        bad = candidate_edges(adj)
        edge_tests += len(EDGES)
        if name in ("four_cycle_two_isolates", "complete_four_two_isolates"):
            expected = [e for e in EDGES if bool(adj[e[0]]) != bool(adj[e[1]])]
        elif name == "complete_bipartite_two_three_one_isolate":
            expected = []
        else:
            # Delete the unique bridge and compare the non-bridge vertices of its triangles.
            bridges = [(i, j) for i, j in EDGES if j in adj[i]
                       and len(adj[i]) == len(adj[j]) == 3]
            require(len(bridges) == 1, "Unique bridge between triangles")
            i, j = bridges[0]
            expected = sorted(tuple(sorted((u, v))) for u in adj[i]-{j} for v in adj[j]-{i})
        require(bad == expected, "Exact residual-edge list for every remaining labelled graph")
        require(len(bad) == {"four_cycle_two_isolates": 8,
                            "complete_four_two_isolates": 8,
                            "complete_bipartite_two_three_one_isolate": 0,
                            "two_triangles_one_bridge": 4}[name], "Residual count")
        remaining_counts[name] += bool(bad)
        maximum_directions[isolated] = max(maximum_directions[isolated], 2*len(bad))
    require(len(valid) == 10099 and dict(zero_rows) == {2: 60, 1: 846, 0: 9193},
            "Complete admissible-support census")
    require(maximum_directions == {0: 8, 1: 0, 2: 16}, "Universal residual-direction bounds")
    for odd_cycle in (((0, 1), (1, 2), (0, 2)),
                      ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4))):
        require(mask_of(odd_cycle) not in valid, "Minimum degree two alone is insufficient")
    require(mask_of(((0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5))) not in valid,
            "Two disconnected odd cycles cannot balance")
    witness_json = json.dumps({str(mask): circuits[mask] for mask in sorted(circuits)},
                              separators=(",", ":"), sort_keys=True)
    return dict(graphs_checked=1 << len(EDGES), admissible_graphs=len(valid),
                rejected_graphs=(1 << len(EDGES))-len(valid),
                minimal_support_counts={k: len(v) for k, v in families.items()},
                circuit_witness_sha256=hashlib.sha256(witness_json.encode()).hexdigest(),
                independent_tests_agree_on_every_graph=True,
                admissible_counts_by_zero_rows=dict(sorted(zero_rows.items())),
                classification=dict(sorted(counts.items())),
                graph_edge_tests=edge_tests,
                graphs_with_residual_directions=sum(remaining_counts.values()),
                maximum_projective_directions_by_zero_rows=maximum_directions,
                odd_cycle_negative_controls=3)


class HField:
    """Q[h]/(2 h^4+5 h^2-1), with only exact rational operations."""

    def __init__(self, value=0):
        self.c = tuple(Q(z) for z in value) if isinstance(value, (tuple, list)) else (Q(value), Q(0), Q(0), Q(0))
        require(len(self.c) == 4, "Quartic coefficient representation")

    def __add__(self, other):
        other = other if isinstance(other, HField) else HField(other)
        return HField(tuple(x+y for x, y in zip(self.c, other.c)))

    __radd__ = __add__

    def __neg__(self):
        return HField(tuple(-x for x in self.c))

    def __sub__(self, other):
        return self + (-other if isinstance(other, HField) else -HField(other))

    def __mul__(self, other):
        other = other if isinstance(other, HField) else HField(other)
        terms = [Q(0)]*7
        for i, j in product(range(4), repeat=2):
            terms[i+j] += self.c[i]*other.c[j]
        for k in range(6, 3, -1):
            terms[k-4] += terms[k]/2
            terms[k-2] -= 5*terms[k]/2
        return HField(terms[:4])

    __rmul__ = __mul__

    def __eq__(self, other):
        other = other if isinstance(other, HField) else HField(other)
        return self.c == other.c

    def __bool__(self):
        return any(self.c)

    def encode(self):
        return [str(x) for x in self.c]


def hafnian(source, vertices, zero, one):
    return sum((product_term(source, matching, one) for matching in T.matchings(tuple(vertices))), zero)


def product_term(source, matching, one):
    value = one
    for edge in matching:
        value *= source[edge]
    return value


def check_ground_examples():
    old = T.original_ground()
    old_cof = {edge: T.hafnian(old, tuple(v for v in VERTICES if v not in edge)) for edge in EDGES}
    old_mask = mask_of(e for e, value in old_cof.items() if value)
    require(not T.hafnian(old, VERTICES) and all(old.values())
            and len(candidate_edges(adjacency(old_mask))) == 8, "Existing full-support four-cycle example")

    h = HField((0, 1, 0, 0))
    h2, h3 = h*h, h*h*h
    inverse = 2*h3+5*h
    require(h*inverse == 1 and 2*h2*h2+5*h2 == 1, "Defining quartic and inverse identity")
    a, e, s = inverse-3*h, -Q(1, 2)*inverse, inverse-h
    cross = [[a, h, h], [h, e, e], [h, e, e]]
    ground = {edge: HField(1) for edge in combinations(range(3), 2)}
    ground.update({edge: HField(1) for edge in combinations(range(3, 6), 2)})
    ground.update({(i, j+3): cross[i][j] for i, j in product(range(3), repeat=2)})
    cof = {edge: hafnian(ground, tuple(v for v in VERTICES if v not in edge),
                        HField(), HField(1)) for edge in EDGES}
    expected = {(0, 1): -s, (0, 2): -s, (1, 2): s,
                (3, 4): -s, (3, 5): -s, (4, 5): s,
                (0, 3): 1+Q(1, 2)*inverse*inverse}
    require(all(cof[edge] == expected.get(edge, HField()) for edge in EDGES),
            "All fifteen exact bridge-example cofactors")
    require(not hafnian(ground, VERTICES, HField(), HField(1)),
            "Full-support real bridge example has zero hafnian")
    for i in VERTICES:
        require(not sum((ground[edge]*cof[edge] for edge in EDGES if i in edge), HField()),
                "Every weighted cofactor row sums to zero")
    bad = candidate_edges(adjacency(mask_of(expected)))
    require(bad == [(1, 4), (1, 5), (2, 4), (2, 5)], "Bridge fixture residual pairs")
    # h is the positive root. 2 r^2+5 r-1 is increasing for r>=0.
    require(Q(-1) < 0 < 2*Q(1, 4)*Q(1, 4)+5*Q(1, 4)-1,
            "Positive h squared lies strictly between zero and one quarter")
    # All source/cofactor values claimed nonzero have same-sign nonzero coefficients in h.
    for value in list(ground.values())+list(expected.values()):
        nonzero = [coefficient for coefficient in value.c if coefficient]
        require(nonzero and (all(x > 0 for x in nonzero) or all(x < 0 for x in nonzero)),
                "Nonzero at every positive h, proving full support and exact cofactor support")
    return dict(four_cycle_fixture=dict(cofactor_edges=[list(e) for e, c in old_cof.items() if c],
                                       residual_projective_directions=16),
                bridge_fixture=dict(defining_polynomial="2*h^4+5*h^2-1",
                                    real_root_interval_squared=["0", "1/4"],
                                    cross_entries=dict(a=a.encode(), h=h.encode(), e=e.encode()),
                                    cofactor_values={f"{i}{j}": value.encode() for (i, j), value in expected.items()},
                                    zero_hafnian=True, full_support=True,
                                    residual_edges=[list(e) for e in bad],
                                    residual_projective_directions=8))


def check_tensor_identities():
    source = {(*edge, a, b): Poly.variable(f"t_{edge[0]}_{edge[1]}_{a}_{b}")
              for edge in EDGES for a, b in product(range(2), repeat=2)}
    def cell(i, j, word):
        if i > j:
            i, j = j, i
        return source[i, j, word[i], word[j]]
    def output(vertices, word):
        result = Poly()
        for matching in T.matchings(tuple(sorted(vertices))):
            term = Poly(1)
            for i, j in matching:
                term *= cell(i, j, word)
            result += term
        return result
    expansion_count = 0
    quartet_count = 0
    for word in product(range(2), repeat=6):
        full = output(VERTICES, word)
        for root in VERTICES:
            expansion = sum((cell(root, j, word)*output(tuple(v for v in VERTICES if v not in (root, j)), word)
                             for j in VERTICES if j != root), Poly())
            require(full.terms == expansion.terms, "Every root expansion includes each matching once")
            expansion_count += 1
    for i, j in EDGES:
        outside = [v for v in VERTICES if v not in (i, j)]
        for r, s in combinations(outside, 2):
            vertices = sorted((i, j, r, s))
            for colors in product(range(2), repeat=4):
                word = dict(zip(vertices, colors))
                rhs = (cell(i, j, word)*cell(r, s, word)
                       + cell(i, r, word)*cell(j, s, word)
                       + cell(i, s, word)*cell(j, r, word))
                require(output(vertices, word).terms == rhs.terms, "Propagation quartet identity")
                quartet_count += 1
    return dict(vertex_matching_expansions=expansion_count,
                propagation_quartet_identities=quartet_count)


def check():
    return dict(graph_classification=check_graph_classification(),
                exact_ground_examples=check_ground_examples(),
                tensor_identities=check_tensor_identities())
