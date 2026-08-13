#!/usr/bin/env python3
"""Exact two-vertex contraction identity and a minimal descent counterguard.

For a decorated matching tensor W_X(A), contract vertices p,q by covectors
phi,psi.  With

  s=(phi tensor psi)(A_pq),
  a_u=(phi tensor id)(A_pu), b_u=(psi tensor id)(A_qu),
  R_uv=a_u tensor b_v+b_u tensor a_v,

the contraction is s W_U(A)+D W_U(A)[R].  If s is nonzero, replacing A by
A+R/s adds every term with at least two effective R edges.

The checker gives an honest six-vertex decorated graph whose chosen
contraction is Delta_3 on the four retained vertices but whose absorbed
four-vertex graph is Delta_3+12 e0^4.  This refutes descent from the local
contraction equation alone.  It is not a six-vertex Delta_3 source and hence
does not refute a theorem using all global GHZ coefficient equations.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json


EXPECTED_LEDGER_SHA256 = "c06f29f9f44bb7566388de3f9a9cd931d369b10b6509373c0fdfb9989e6bf026"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def edge(left, right):
    return min(left, right), max(left, right)


def add_edge(edges, left, right, entries):
    key = edge(left, right)
    require(key not in edges, ("edge assigned twice", key))
    if left < right:
        edges[key] = {tuple(colours): Q(value)
                      for colours, value in entries.items() if value}
    else:
        edges[key] = {(right_colour, left_colour): Q(value)
                      for (left_colour, right_colour), value in entries.items()
                      if value}


def add_edge_values(left, right):
    answer = dict(left)
    for colours, value in right.items():
        answer[colours] = answer.get(colours, Q(0)) + value
        if not answer[colours]:
            del answer[colours]
    return answer


def scale_edge(value, entries):
    return {colours: Q(value) * coefficient
            for colours, coefficient in entries.items() if value * coefficient}


def matching_tensor(vertices, edges, colours=3):
    vertices = tuple(vertices)
    answer = {}
    for word in itertools.product(range(colours), repeat=len(vertices)):
        local = dict(zip(vertices, word, strict=True))
        value = Q(0)
        for matching in perfect_matchings(vertices):
            term = Q(1)
            for left, right in matching:
                left, right = edge(left, right)
                term *= edges.get((left, right), {}).get(
                    (local[left], local[right]), Q(0)
                )
            value += term
        if value:
            answer[word] = value
    return answer


def add_tensors(*vectors):
    answer = {}
    for vector in vectors:
        for word, value in vector.items():
            answer[word] = answer.get(word, Q(0)) + value
            if not answer[word]:
                del answer[word]
    return answer


def scale_tensor(value, vector):
    return {word: Q(value) * coefficient
            for word, coefficient in vector.items() if value * coefficient}


def first_variation(vertices, base, direction, colours=3):
    """Coefficient of t in W(base+t*direction)."""
    vertices = tuple(vertices)
    answer = {}
    for word in itertools.product(range(colours), repeat=len(vertices)):
        local = dict(zip(vertices, word, strict=True))
        value = Q(0)
        for matching in perfect_matchings(vertices):
            for marked in range(len(matching)):
                term = Q(1)
                for index, raw_edge in enumerate(matching):
                    left, right = edge(*raw_edge)
                    source = direction if index == marked else base
                    term *= source.get((left, right), {}).get(
                        (local[left], local[right]), Q(0)
                    )
                value += term
        if value:
            answer[word] = value
    return answer


def contract_two_vertices(vertices, edges, p, q, phi, psi, colours=3):
    """Direct tensor contraction of W_vertices at p,q."""
    vertices = tuple(vertices)
    retained = tuple(vertex for vertex in vertices if vertex not in (p, q))
    full = matching_tensor(vertices, edges, colours)
    answer = {}
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    for word, value in full.items():
        coefficient = phi[word[positions[p]]] * psi[word[positions[q]]]
        if not coefficient:
            continue
        retained_word = tuple(word[positions[vertex]] for vertex in retained)
        answer[retained_word] = answer.get(retained_word, Q(0)) \
            + coefficient * value
    return {word: value for word, value in answer.items() if value}


def contraction_data(vertices, edges, p, q, phi, psi, colours=3):
    retained = tuple(vertex for vertex in vertices if vertex not in (p, q))
    pq = edges.get(edge(p, q), {})
    s = sum(phi[left_colour] * psi[right_colour] * value
            for (left_colour, right_colour), value in pq.items())
    # p,q are chosen after all retained vertices in the literal example, so
    # stored edge orientations put retained colour first.  Handle orientation
    # generally to keep the identity reusable.
    a, b = {}, {}
    for vertex in retained:
        p_edge = edges.get(edge(p, vertex), {})
        q_edge = edges.get(edge(q, vertex), {})
        if p < vertex:
            a[vertex] = {
                local_colour: sum(phi[p_colour] * value
                                  for (p_colour, colour), value in p_edge.items()
                                  if colour == local_colour)
                for local_colour in range(colours)
            }
        else:
            a[vertex] = {
                local_colour: sum(phi[p_colour] * value
                                  for (colour, p_colour), value in p_edge.items()
                                  if colour == local_colour)
                for local_colour in range(colours)
            }
        if q < vertex:
            b[vertex] = {
                local_colour: sum(psi[q_colour] * value
                                  for (q_colour, colour), value in q_edge.items()
                                  if colour == local_colour)
                for local_colour in range(colours)
            }
        else:
            b[vertex] = {
                local_colour: sum(psi[q_colour] * value
                                  for (colour, q_colour), value in q_edge.items()
                                  if colour == local_colour)
                for local_colour in range(colours)
            }
        a[vertex] = {colour: value for colour, value in a[vertex].items()
                     if value}
        b[vertex] = {colour: value for colour, value in b[vertex].items()
                     if value}

    direction = {}
    for left, right in itertools.combinations(retained, 2):
        entries = {}
        for left_colour, left_value in a[left].items():
            for right_colour, right_value in b[right].items():
                entries[left_colour, right_colour] = (
                    entries.get((left_colour, right_colour), Q(0))
                    + left_value * right_value
                )
        for left_colour, left_value in b[left].items():
            for right_colour, right_value in a[right].items():
                entries[left_colour, right_colour] = (
                    entries.get((left_colour, right_colour), Q(0))
                    + left_value * right_value
                )
        direction[edge(left, right)] = {
            colours_pair: value for colours_pair, value in entries.items()
            if value
        }
    base = {edge(left, right): edges.get(edge(left, right), {})
            for left, right in itertools.combinations(retained, 2)}
    return retained, s, a, b, base, direction


def contraction_identity_audit():
    # A deterministic nontrivial six-vertex stress graph checks the exact
    # identity independently of the counterguard below.
    vertices = tuple(range(6))
    p, q = 4, 5
    edges = {}
    for left, right in itertools.combinations(vertices, 2):
        entries = {}
        for c in range(3):
            entries[c, c] = Q((left + 1) * (right + 2) * (c + 1), 17)
        entries[(left + right) % 3, (left + 2 * right) % 3] = \
            entries.get(((left + right) % 3,
                         (left + 2 * right) % 3), Q(0)) + Q(1, 19)
        add_edge(edges, left, right, entries)
    phi = (Q(2), Q(-1), Q(3))
    psi = (Q(1), Q(4), Q(-2))
    retained, s, _a, _b, base, direction = contraction_data(
        vertices, edges, p, q, phi, psi
    )
    direct = contract_two_vertices(vertices, edges, p, q, phi, psi)
    formula = add_tensors(
        scale_tensor(s, matching_tensor(retained, base)),
        first_variation(retained, base, direction),
    )
    require(direct == formula and s != 0,
            "the exact two-vertex contraction identity changed")
    absorbed_edges = {
        value: add_edge_values(base[value], scale_edge(Q(1, s), direction[value]))
        for value in base
    }
    absorbed = scale_tensor(s, matching_tensor(retained, absorbed_edges))
    debt = add_tensors(absorbed, scale_tensor(-1, direct))
    require(debt, "the generic absorption debt vanished")
    return {
        "retained_vertices": len(retained),
        "direct_edge_scalar_nonzero": True,
        "direct_contraction_equals_sW_plus_first_variation": True,
        "absorbed_graph_has_nonzero_multi_effective_debt": True,
        "stress_contracted_support": len(direct),
        "stress_debt_support": len(debt),
    }


def oriented_matching_count(k):
    vertices = tuple(range(2 * k))
    counts = Counter()
    for matching in perfect_matchings(vertices):
        for orientations in itertools.product((0, 1), repeat=k):
            a_sites = []
            for (left, right), orientation in zip(matching, orientations,
                                                   strict=True):
                a_sites.append((left, right)[orientation])
            counts[tuple(sorted(a_sites))] += 1
    return counts


def effective_hafnian_audit():
    checked = {}
    for k in range(1, 5):
        counts = oriented_matching_count(k)
        require(len(counts) == len(tuple(itertools.combinations(range(2*k), k)))
                and set(counts.values()) == {__import__("math").factorial(k)},
                (k, counts))
        checked[k] = {
            "a_site_subsets": len(counts),
            "coefficient_per_subset": __import__("math").factorial(k),
        }
    return {
        "formula": (
            "Haf(R_S)=k! sum_{|I|=k} tensor_{i in I} a_i tensor "
            "tensor_{j in S\\I} b_j for |S|=2k"
        ),
        "orders_checked": checked,
    }


def build_local_delta3_counterguard():
    # Retained vertices 0,1,2,3; endpoints 4,5.  phi=psi=(1,1,1).
    # Endpoint edges contract to a_u=b_u=e0, hence every R_uv=2 e0e0.
    retained = (0, 1, 2, 3)
    vertices = tuple(range(6))
    p, q = 4, 5
    phi = psi = (Q(1), Q(1), Q(1))

    r_edges = {}
    for left, right in itertools.combinations(retained, 2):
        add_edge(r_edges, left, right, {(0, 0): 2})
    require(matching_tensor(retained, r_edges) == {(0, 0, 0, 0): Q(12)},
            "the rank-two effective K4 hafnian changed")

    # B=A+R realizes Delta3+Haf(R) by the three K4 perfect matchings.
    b_edges = {}
    add_edge(b_edges, 0, 1, {(0, 0): 13})
    add_edge(b_edges, 2, 3, {(0, 0): 1})
    add_edge(b_edges, 0, 2, {(1, 1): 1})
    add_edge(b_edges, 1, 3, {(1, 1): 1})
    add_edge(b_edges, 0, 3, {(2, 2): 1})
    add_edge(b_edges, 1, 2, {(2, 2): 1})
    a_edges = {
        value: add_edge_values(b_edges[value], scale_edge(-1, r_edges[value]))
        for value in b_edges
    }
    delta3 = {(0, 0, 0, 0): Q(1),
              (1, 1, 1, 1): Q(1),
              (2, 2, 2, 2): Q(1)}
    local_contraction = add_tensors(
        matching_tensor(retained, a_edges),
        first_variation(retained, a_edges, r_edges),
    )
    absorbed = matching_tensor(retained, b_edges)
    require(local_contraction == delta3
            and absorbed == add_tensors(delta3, {(0, 0, 0, 0): Q(12)}),
            (local_contraction, absorbed))

    # Lift the interface to an honest decorated six-vertex graph.
    parent = dict(a_edges)
    add_edge(parent, p, q, {(0, 0): 1})
    for vertex in retained:
        add_edge(parent, vertex, p, {(0, 0): 1})
        add_edge(parent, vertex, q, {(0, 0): 1})
    direct = contract_two_vertices(vertices, parent, p, q, phi, psi)
    data = contraction_data(vertices, parent, p, q, phi, psi)
    _retained, s, a, b, base, direction = data
    require(s == 1 and direct == delta3
            and base == a_edges and direction == r_edges
            and all(a[vertex] == {0: Q(1)} for vertex in retained)
            and all(b[vertex] == {0: Q(1)} for vertex in retained),
            "the honest six-vertex contraction guard changed")
    parent_tensor = matching_tensor(vertices, parent)
    require(parent_tensor != {
        (0,) * 6: Q(1), (1,) * 6: Q(1), (2,) * 6: Q(1)
    }, "the local guard unexpectedly became a global Delta3 source")
    return {
        "retained_target": "Delta_3",
        "direct_edge_scalar": int(s),
        "endpoint_contractions": "a_u=b_u=e0 on all four retained vertices",
        "effective_edges": "R_uv=2 e0 tensor e0",
        "multi_effective_Haf_R": "12 e0^tensor4",
        "contracted_parent_tensor": "Delta_3 exactly",
        "absorbed_retained_graph": "Delta_3+12 e0^tensor4",
        "parent_is_global_Delta3": False,
        "parent_tensor_support": len(parent_tensor),
        "logical_scope": (
            "an honest decorated-hafnian contraction counterexample to the "
            "local inference contracted Delta3 => cross debt zero; not a "
            "counterexample to a descent theorem using all parent GHZ rows"
        ),
    }


def normalized_endpoint_no_choice_guard():
    # Let every p-u and q-u edge be the identity tensor.  Then a_u=phi and
    # b_u=psi.  Under phi_c psi_c=1, the all-c component of every R edge is
    # 2, so the all-c component of Haf_4(R) is 3*2^2=12.  Thus no normalized
    # covector choice kills even the first two-effective-edge term.
    colours = 3
    values = []
    for colour in range(colours):
        r_cc = 2  # phi_c psi_c + psi_c phi_c
        values.append(3 * r_cc * r_cc)
    require(values == [12, 12, 12], values)
    return {
        "endpoint_maps": "identity V* -> V at every retained site",
        "normalized_target_condition": "phi_c*psi_c=1 for c=0,1,2",
        "Haf4_R_pure_colour_coefficients": values,
        "a_normalized_choice_with_Haf4_R_zero_exists": False,
        "scope": (
            "endpoint-factor no-choice guard only; global W_n=Delta_r may "
            "force these endpoint maps not to occur, which requires a new "
            "global source theorem"
        ),
    }


def direct_edge_access_audit(r=3):
    # On psi_c=1/phi_c, s=sum E_cd phi_c/phi_d.  Off-diagonal exponent
    # characters are distinct; diagonals share exponent zero and contribute
    # trace(E).  Hence s is identically zero exactly for diagonal traceless E.
    characters = Counter()
    for left in range(r):
        for right in range(r):
            exponent = [0] * r
            exponent[left] += 1
            exponent[right] -= 1
            characters[tuple(exponent)] += 1
    require(characters[(0,) * r] == r
            and all(multiplicity == 1 for exponent, multiplicity in characters.items()
                    if exponent != (0,) * r), characters)
    return {
        "normalized_subtorus": "psi_c=1/phi_c",
        "direct_scalar": "s(phi)=sum_cd E_cd phi_c/phi_d",
        "identically_dark_iff": "E is diagonal and trace(E)=0",
        "consequence": (
            "before multi-edge debt, a pair with diagonal-traceless direct "
            "edge has no normalized contraction with s nonzero"
        ),
    }


def audit():
    ledger = {
        "theorem": "decorated hafnian two-vertex contraction/descent guard",
        "exact_contraction_identity": contraction_identity_audit(),
        "rank_two_effective_hafnian": effective_hafnian_audit(),
        "literal_Delta3_contraction_counterguard":
            build_local_delta3_counterguard(),
        "normalized_endpoint_no_choice_guard":
            normalized_endpoint_no_choice_guard(),
        "direct_edge_access": direct_edge_access_audit(),
        "verdict": (
            "Two-vertex contraction is exactly s W(A)+D W(A)[R].  Absorbing "
            "R/s adds all k>=2 effective-edge terms.  These terms are not "
            "formal noise: an honest six-vertex decorated graph has a chosen "
            "contraction equal to Delta3 while its absorbed retained graph is "
            "Delta3+12e0^4.  Moreover identity endpoint maps make Haf4(R) "
            "nonzero for every normalized covector choice.  Therefore the "
            "monochromatic contracted tensor alone does not yield honest "
            "descent.  A positive theorem must use the complete parent GHZ "
            "equations to exclude/terminalize the endpoint no-choice guard; "
            "the checker does not construct a global Delta3 parent source."
        ),
        "scope": (
            "exact general identity, rank-two effective-edge formula, direct-"
            "edge access criterion, and minimal local contraction counterguard. "
            "Not a counterexample to the Krenn conjecture or to a descent "
            "lemma with additional global-source hypotheses."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("two-vertex contraction ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("two-vertex contraction: s W + first effective-edge variation")
    print("absorbed graph: ADDS ALL MULTI-EFFECTIVE-EDGE TERMS")
    print("honest local Delta3 contraction: CROSS DEBT 12 e0^4")
    print("global Delta3 parent counterexample: NOT CLAIMED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
