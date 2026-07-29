#!/usr/bin/env python3
"""Clean-room audit of the finite three-term pair-cap exhaustion.

This file uses only the Python standard library.  In particular, it does not
import either of the primary computation modules.  Matchings are generated as
four-edge subsets of K_8, polarized coefficients are reconstructed directly
from subsets of the nine q-cells, and the two-dimensional Gram obstruction is
checked through projective orthogonality components (not union--find closure).
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
import hashlib
from itertools import combinations, permutations, product


SITES = tuple(range(8))
COLOURS = tuple(range(3))
ALL_SITES_MASK = (1 << 8) - 1
EDGES = tuple(combinations(SITES, 2))
TRIPLES_OF_NINE = tuple(combinations(range(9), 3))
FOURS_OF_NINE = tuple(combinations(range(9), 4))
PURE_WORDS = {tuple([colour] * 8) for colour in COLOURS}

EXPECTED_EXACT = 9_888
EXPECTED_SHORT = 7_968
EXPECTED_CLOSURE_ONLY = 1_920
EXPECTED_PRIMARY_LEDGER_SHA256 = (
    "5f42b78f2f972ed25a96f6ea01a25dcaf2b1c108174ba0fe2d0804132dddb639"
)

EXPECTED_AUDIT_LEDGER_SHA256 = (
    "20e054d75b6dd11d1dd219fe4677242ab17f6dd1cac0860457eda6f93788b36f"
)


def edge_mask(edge):
    return (1 << edge[0]) | (1 << edge[1])


def enumerate_matchings():
    """Generate matchings by filtering C(28,4), unlike the primary recursion."""
    result = []
    for four_edges in combinations(EDGES, 4):
        union = 0
        disjoint = True
        for edge in four_edges:
            mask = edge_mask(edge)
            if union & mask:
                disjoint = False
                break
            union |= mask
        if disjoint and union == ALL_SITES_MASK:
            result.append(four_edges)
    return tuple(result)


MATCHINGS = enumerate_matchings()
FLAGGED = tuple(
    (matching, distinguished)
    for matching in MATCHINGS
    for distinguished in matching
)
BASE = (((0, 1), (2, 3), (4, 5), (6, 7)), (0, 1))


def permute_flagged(flagged, permutation):
    matching, distinguished = flagged
    image_matching = tuple(sorted(
        tuple(sorted((permutation[left], permutation[right])))
        for left, right in matching
    ))
    image_distinguished = tuple(sorted((
        permutation[distinguished[0]], permutation[distinguished[1]]
    )))
    return image_matching, image_distinguished


@dataclass(frozen=True)
class QCell:
    edge: tuple[int, int]
    colour: int
    label: int

    @property
    def mask(self):
        return edge_mask(self.edge)


@dataclass(frozen=True)
class FContribution:
    leftover_modes: tuple[int, int]
    coefficient_monomial: tuple[int, int, int]


@dataclass(frozen=True)
class ClosureCertificate:
    kind: str
    required_pair: tuple[int, int]
    zero_path: tuple[int, ...] = ()
    odd_cycle: tuple[int, ...] = ()
    paths_from_cycle: tuple[tuple[int, ...], tuple[int, ...]] = ((), ())


def q_cells(flagged_by_colour):
    cells = []
    for colour, (matching, distinguished) in enumerate(flagged_by_colour):
        for edge in matching:
            if edge != distinguished:
                cells.append(QCell(edge, colour, len(cells)))
    assert len(cells) == 9
    return tuple(cells)


def decorated_completions(cells, distinguished):
    """List all q-cell triples completing one distinguished physical edge."""
    wanted = ALL_SITES_MASK ^ edge_mask(distinguished)
    completions = []
    for triple in TRIPLES_OF_NINE:
        masks = tuple(cells[index].mask for index in triple)
        if (masks[0] & masks[1]) or (masks[0] & masks[2]) or (masks[1] & masks[2]):
            continue
        if (masks[0] | masks[1] | masks[2]) != wanted:
            continue
        completions.append(tuple(cells[index].colour for index in triple))
    return tuple(completions)


def is_exact_three_term_support(flagged_by_colour, cells):
    """Check z q^[3]=Delta combinatorially, without a matching lookup table."""
    for colour, (_matching, distinguished) in enumerate(flagged_by_colour):
        completions = decorated_completions(cells, distinguished)
        if completions != ((colour, colour, colour),):
            return False
    return True


def disjoint_triples(cells):
    result = []
    for triple in TRIPLES_OF_NINE:
        masks = tuple(cells[index].mask for index in triple)
        if (masks[0] & masks[1]) or (masks[0] & masks[2]) or (masks[1] & masks[2]):
            continue
        result.append((triple, masks[0] | masks[1] | masks[2]))
    return tuple(result)


def word_from_cells(cells, indices):
    word = [-1] * 8
    for index in indices:
        cell = cells[index]
        word[cell.edge[0]] = cell.colour
        word[cell.edge[1]] = cell.colour
    return word


def coefficient_support(cells):
    """Construct the support ledgers for F=q^[3] and Q=q^[4]."""
    f_words = defaultdict(list)
    for triple, used_mask in disjoint_triples(cells):
        base_word = word_from_cells(cells, triple)
        leftovers = tuple(site for site in SITES if not (used_mask & (1 << site)))
        assert len(leftovers) == 2
        for left_colour, right_colour in product(COLOURS, repeat=2):
            word = list(base_word)
            word[leftovers[0]] = left_colour
            word[leftovers[1]] = right_colour
            modes = tuple(sorted((
                3 * leftovers[0] + left_colour,
                3 * leftovers[1] + right_colour,
            )))
            f_words[tuple(word)].append(FContribution(modes, triple))

    q_four = defaultdict(list)
    for four in FOURS_OF_NINE:
        masks = tuple(cells[index].mask for index in four)
        if any(masks[i] & masks[j] for i in range(4) for j in range(i + 1, 4)):
            continue
        assert (masks[0] | masks[1] | masks[2] | masks[3]) == ALL_SITES_MASK
        q_four[tuple(word_from_cells(cells, four))].append(four)
    return dict(f_words), dict(q_four)


def six_distinguished_modes(flagged_by_colour):
    pairs = []
    modes = []
    for colour, (_matching, distinguished) in enumerate(flagged_by_colour):
        pair = tuple(3 * site + colour for site in distinguished)
        pairs.append(pair)
        modes.extend(pair)
    assert len(modes) == len(set(modes)) == 6
    local_index = {mode: index for index, mode in enumerate(modes)}
    required = tuple(
        tuple(sorted((local_index[left], local_index[right])))
        for left, right in pairs
    )
    return tuple(modes), required


def pure_and_zero_gram_data(flagged_by_colour, cells, f_words, q_four):
    """Extract only coefficient equations that are singleton support identities."""
    modes, required = six_distinguished_modes(flagged_by_colour)
    local_index = {mode: index for index, mode in enumerate(modes)}
    pure_monomials = []

    for colour, (_matching, distinguished) in enumerate(flagged_by_colour):
        word = tuple([colour] * 8)
        contributions = f_words.get(word, ())
        expected_modes = tuple(sorted((
            3 * distinguished[0] + colour,
            3 * distinguished[1] + colour,
        )))
        assert len(contributions) == 1
        assert contributions[0].leftover_modes == expected_modes
        assert word not in q_four
        monomial = contributions[0].coefficient_monomial
        assert len(monomial) == len(set(monomial)) == 3
        assert all(cells[index].colour == colour for index in monomial)
        pure_monomials.append(monomial)

    zero_edges = set()
    zero_monomials = {}
    for word, contributions in f_words.items():
        if word in PURE_WORDS or word in q_four or len(contributions) != 1:
            continue
        contribution = contributions[0]
        left, right = contribution.leftover_modes
        if left not in local_index or right not in local_index:
            continue
        edge = tuple(sorted((local_index[left], local_index[right])))
        assert edge[0] != edge[1]
        monomial = contribution.coefficient_monomial
        assert len(monomial) == len(set(monomial)) == 3
        zero_edges.add(edge)
        zero_monomials.setdefault(edge, set()).add(monomial)

    # If the same Gram edge was exposed by several different singleton words,
    # each word separately gives a nonzero scalar multiple of that Gram entry.
    assert all(monomials for monomials in zero_monomials.values())
    return required, frozenset(zero_edges), tuple(pure_monomials), zero_monomials


def short_seven_entry_certificate(required, zero_edges):
    """The labelled 3 nonzero + 4 zero pattern used by the primary split."""
    pair0, pair1, pair2 = required
    for a in pair0:
        b = pair0[0] if a == pair0[1] else pair0[1]
        for c in pair1:
            for f in pair2:
                wanted = {
                    tuple(sorted((a, f))),
                    tuple(sorted((b, f))),
                    tuple(sorted((a, c))),
                    tuple(sorted((c, f))),
                }
                if wanted <= zero_edges:
                    return True
    return False


def adjacency(zero_edges):
    graph = [set() for _ in range(6)]
    for left, right in zero_edges:
        graph[left].add(right)
        graph[right].add(left)
    return tuple(tuple(sorted(neighbours)) for neighbours in graph)


def path_between(graph, start, finish):
    queue = deque([start])
    parent = {start: None}
    while queue:
        vertex = queue.popleft()
        if vertex == finish:
            break
        for neighbour in graph[vertex]:
            if neighbour not in parent:
                parent[neighbour] = vertex
                queue.append(neighbour)
    if finish not in parent:
        return ()
    reversed_path = []
    vertex = finish
    while vertex is not None:
        reversed_path.append(vertex)
        vertex = parent[vertex]
    return tuple(reversed(reversed_path))


def odd_cycle_in_component(graph, component):
    """Find a literal simple odd cycle; six vertices make DFS exhaustive."""
    allowed = set(component)
    for start in sorted(allowed):
        stack = [(start, (start,))]
        while stack:
            vertex, path = stack.pop()
            for neighbour in graph[vertex]:
                if neighbour == start and len(path) >= 3 and len(path) % 2 == 1:
                    return path + (start,)
                if neighbour in allowed and neighbour not in path and len(path) < len(allowed):
                    stack.append((neighbour, path + (neighbour,)))
    return ()


def projective_orthogonality_certificate(required, zero_edges):
    """Find a contradiction via parity of the orthogonality involution.

    A zero edge applies the involution L -> L^perp to projective lines.  A
    bipartite zero component therefore alternates between L and L^perp; an
    odd cycle forces L=L^perp, so its entire component is one isotropic line.
    """
    graph = adjacency(zero_edges)
    component_id = [-1] * 6
    parity = [-1] * 6
    components = []
    bipartite = []

    for root in range(6):
        if component_id[root] != -1:
            continue
        cid = len(components)
        queue = deque([root])
        component_id[root] = cid
        parity[root] = 0
        vertices = []
        is_bipartite = True
        while queue:
            vertex = queue.popleft()
            vertices.append(vertex)
            for neighbour in graph[vertex]:
                if component_id[neighbour] == -1:
                    component_id[neighbour] = cid
                    parity[neighbour] = parity[vertex] ^ 1
                    queue.append(neighbour)
                else:
                    assert component_id[neighbour] == cid
                    if parity[neighbour] == parity[vertex]:
                        is_bipartite = False
        components.append(tuple(sorted(vertices)))
        bipartite.append(is_bipartite)

    for pair in required:
        left, right = pair
        if component_id[left] != component_id[right]:
            continue
        cid = component_id[left]
        if bipartite[cid]:
            if parity[left] == parity[right]:
                continue
            path = path_between(graph, left, right)
            assert path and (len(path) - 1) % 2 == 1
            return ClosureCertificate("odd_zero_path", pair, zero_path=path)

        cycle = odd_cycle_in_component(graph, components[cid])
        assert cycle
        root = cycle[0]
        left_path = path_between(graph, root, left)
        right_path = path_between(graph, root, right)
        assert left_path and right_path
        return ClosureCertificate(
            "isotropic_component",
            pair,
            odd_cycle=cycle,
            paths_from_cycle=(left_path, right_path),
        )
    return None


def validate_walk(graph, walk):
    assert walk
    for left, right in zip(walk, walk[1:]):
        assert right in graph[left]


def validate_closure_certificate(certificate, required, zero_edges):
    """Replay only literal graph facts used in the projective proof."""
    assert certificate.required_pair in required
    graph = adjacency(zero_edges)
    left, right = certificate.required_pair
    if certificate.kind == "odd_zero_path":
        path = certificate.zero_path
        assert path[0] == left and path[-1] == right
        validate_walk(graph, path)
        assert (len(path) - 1) % 2 == 1
        return
    assert certificate.kind == "isotropic_component"
    cycle = certificate.odd_cycle
    assert cycle[0] == cycle[-1]
    assert len(set(cycle[:-1])) == len(cycle) - 1
    validate_walk(graph, cycle)
    assert (len(cycle) - 1) % 2 == 1
    left_path, right_path = certificate.paths_from_cycle
    assert left_path[0] == cycle[0] == right_path[0]
    assert left_path[-1] == left and right_path[-1] == right
    validate_walk(graph, left_path)
    validate_walk(graph, right_path)


def main():
    assert len(EDGES) == 28
    assert len(MATCHINGS) == 105
    assert len(set(MATCHINGS)) == 105
    assert all(len({site for edge in matching for site in edge}) == 8 for matching in MATCHINGS)
    assert len(FLAGGED) == 420
    assert len(set(FLAGGED)) == 420
    assert BASE in FLAGGED
    assert len(FLAGGED) ** 2 == 176_400
    base_orbit = {
        permute_flagged(BASE, permutation)
        for permutation in permutations(SITES)
    }
    assert base_orbit == set(FLAGGED)
    assert 40_320 // len(base_orbit) == 96

    exact_count = 0
    short_count = 0
    closure_only_count = 0
    closure_kinds = Counter()
    zero_edge_histogram = Counter()
    primary_digest = hashlib.sha256()
    audit_digest = hashlib.sha256()

    for flagged1 in FLAGGED:
        for flagged2 in FLAGGED:
            flagged = (BASE, flagged1, flagged2)
            cells = q_cells(flagged)
            if not is_exact_three_term_support(flagged, cells):
                continue
            exact_count += 1

            f_words, q_four = coefficient_support(cells)
            required, zero_edges, pure_monomials, zero_monomials = (
                pure_and_zero_gram_data(flagged, cells, f_words, q_four)
            )

            # This explicitly audits the weighted extension.  Each equation
            # used below has one formal squarefree monomial in nonzero q-cell
            # weights.  Pure equations therefore prescribe a nonzero Gram
            # value; mixed equations prescribe zero.  No cancellation is used.
            assert all(len(monomial) == 3 for monomial in pure_monomials)
            assert all(
                len(monomial) == 3
                for monomials in zero_monomials.values()
                for monomial in monomials
            )

            short = short_seven_entry_certificate(required, zero_edges)
            certificate = projective_orthogonality_certificate(required, zero_edges)
            assert certificate is not None
            validate_closure_certificate(certificate, required, zero_edges)

            if short:
                short_count += 1
            else:
                closure_only_count += 1
                closure_kinds[certificate.kind] += 1
            zero_edge_histogram[len(zero_edges)] += 1

            primary_digest.update(repr((flagged1, flagged2, int(short))).encode())
            primary_digest.update(b"\n")
            audit_record = (
                flagged1,
                flagged2,
                tuple(sorted(zero_edges)),
                required,
                int(short),
                certificate.kind,
                certificate.required_pair,
            )
            audit_digest.update(repr(audit_record).encode())
            audit_digest.update(b"\n")

    assert exact_count == EXPECTED_EXACT
    assert short_count == EXPECTED_SHORT
    assert closure_only_count == EXPECTED_CLOSURE_ONLY
    assert short_count + closure_only_count == exact_count
    assert primary_digest.hexdigest() == EXPECTED_PRIMARY_LEDGER_SHA256
    assert audit_digest.hexdigest() == EXPECTED_AUDIT_LEDGER_SHA256

    print("independent eight-site three-term pair-cap audit: PASS")
    print("C(28,4) gives 105 matchings and 420 flagged matchings: PASS")
    print("S_8 orbit of the normalized first flag has size 420: PASS")
    print("all 176400 normalized flagged pairs scanned: PASS")
    print("9888 exact three-decorated-term supports: PASS")
    print("7968 short-pattern + 1920 closure-only contradictions: PASS")
    print(f"closure-only certificate kinds: {dict(sorted(closure_kinds.items()))}")
    print(f"zero-edge histogram: {dict(sorted(zero_edge_histogram.items()))}")
    print(f"published ledger SHA-256: {primary_digest.hexdigest()}")
    print(f"independent ledger SHA-256: {audit_digest.hexdigest()}")
    print("all closure certificates replay as literal odd paths/cycles: PASS")
    print("arbitrary nonzero weights on the same exact supports: PASS")


if __name__ == "__main__":
    main()
