#!/usr/bin/env python3
"""Close the sole same-colour two-prototype support-16 anchor guard.

The two-cap orbit extension leaves exactly one stabilizer orbit having two
prototype faces but admitting a mutual-coordinate completion in which their
direct colours agree.  This checker keeps the literal source-star expansion
and tests the next two cap faces, whose residues have eight rather than two
expanded monomials.

The result is negative for the local cap-kernel route.  On the canonical
collision completion, cap 03 has the private output 2*K00^2.  Cap 05 has
outputs 2*K00*K02 and K00*K22+K02*K20, with saturation identity

  2*K00^2*K22
    = 2*K00*(K00*K22+K02*K20) - K20*(2*K00*K02).

Thus neither larger face has an active zero.  The two prototype faces also
fail in the exceptional chart w=(0,B,C): w^T K=0 makes their complementary
permanent -2*(B/C)*Kbb*Kbc, nonzero on the active torus.  This is a finite
local anchor-completion terminal, not a normalized full-source countermodel.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "ea3b2b56238cfc3218977818d7f0f09615b987d8b0b53d4010cdbbd56c96f717"
COLORS = (0, 1, 2)
NONANCHOR = -1


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROTOTYPE = load_local(
    "n8_support16_prototype_for_same_colour_terminal",
    "verify_n8_support16_two_cap_prototype_orbit_extension.py",
)
ORBIT = PROTOTYPE.ORBIT


def poly_add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def poly_scale(polynomial, scalar):
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def poly_multiply(*polynomials):
    require(polynomials, "empty polynomial product")
    dimension = len(next(iter(polynomials[0]), ()))
    answer = {(0,) * dimension: 1}
    for polynomial in polynomials:
        following = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                require(len(left) == len(right),
                        ("polynomial dimension mismatch", left, right))
                monomial = tuple(a + b for a, b in zip(left, right))
                following[monomial] += left_coefficient * right_coefficient
        answer = {monomial: coefficient
                  for monomial, coefficient in following.items()
                  if coefficient}
    return answer


def variable(index, dimension=9):
    exponent = [0] * dimension
    exponent[index] = 1
    return {tuple(exponent): 1}


def k_variable(left, right):
    return variable(3 * left + right)


def output_word(cap_edge, tag, orientations, states):
    """Return the literal six-site word of one expanded coordinate term."""
    p, q = cap_edge
    residual = tuple(vertex for vertex in range(8) if vertex not in cap_edge)
    letters = {}
    if tag is not None:
        require(states[tag] >= 0, ("live tag is noncoordinate", tag))
        letters[tag[0]] = states[tag]
        letters[tag[1]] = states[tag]
    for star_pair in orientations:
        require(len(star_pair) == 2, ("bad oriented factor", star_pair))
        for endpoint, external in star_pair:
            require(endpoint in cap_edge,
                    ("orientation left cap", cap_edge, star_pair))
            edge = tuple(sorted((endpoint, external)))
            require(states[edge] >= 0,
                    ("coordinate residue used nonanchor", cap_edge, edge))
            letters[external] = states[edge]
    require(set(letters) == set(residual),
            ("expanded term did not fill residual word", cap_edge, tag,
             orientations, letters, residual))
    return "".join(str(letters[vertex]) for vertex in residual)


def coefficient_monomial(orientations, states):
    coefficient = {(0,) * 9: 1}
    for star_pair in orientations:
        colours = []
        for endpoint, external in star_pair:
            edge = tuple(sorted((endpoint, external)))
            require(states[edge] >= 0,
                    ("coordinate coefficient used nonanchor", edge))
            colours.append(states[edge])
        coefficient = poly_multiply(
            coefficient, k_variable(colours[0], colours[1])
        )
    return coefficient


def coordinate_residue_polynomials(adjacency, edges, cap_edge, incidence,
                                   states):
    answer = {}
    residue_ledger = []
    for expanded in ORBIT.expanded_response_monomials(
            adjacency, edges, cap_edge):
        if ORBIT.contains_directed_star(expanded, incidence):
            continue
        term_index, kind, tag, factors, orientations = expanded
        word = output_word(cap_edge, tag, orientations, states)
        coefficient = coefficient_monomial(orientations, states)
        answer[word] = poly_add(answer.get(word, {}), coefficient)
        residue_ledger.append({
            "term_index": term_index,
            "kind": kind,
            "tag": tag,
            "factors": factors,
            "orientations": orientations,
            "word": word,
            "coefficient": coefficient,
        })
    return answer, tuple(residue_ledger)


def target_words(adjacency, edges, cap_edge, incidence, states):
    """Evaluate only the word labels after giving X_incidence colour r."""
    answer = {}
    target_edge = incidence[1]
    for colour in COLORS:
        chart_states = dict(states)
        chart_states[target_edge] = colour
        words = []
        for expanded in ORBIT.expanded_response_monomials(
                adjacency, edges, cap_edge):
            if not ORBIT.contains_directed_star(expanded, incidence):
                continue
            _term_index, _kind, tag, _factors, orientations = expanded
            words.append(output_word(
                cap_edge, tag, orientations, chart_states
            ))
        answer[colour] = tuple(sorted(words))
    return answer


def all_collision_completions(edges, target_edge, prototype_caps):
    """Enumerate every mutual-coordinate completion in one collision colour."""
    prototype_caps = tuple(prototype_caps)
    states = {target_edge: NONANCHOR}
    for edge in prototype_caps:
        states[edge] = 0
    incident = {
        vertex: tuple(edge for edge in edges
                      if vertex in edge and edge != target_edge)
        for vertex in range(8)
    }
    completions = []

    def recurse():
        for vertex in range(8):
            seen = {states[edge] for edge in incident[vertex]
                    if edge in states and states[edge] >= 0}
            remaining = sum(edge not in states for edge in incident[vertex])
            if 3 - len(seen) > remaining:
                return
        if all(edge in states for edge in edges):
            if all({states[edge] for edge in incident[vertex]}
                   == set(COLORS) for vertex in range(8)):
                completions.append(tuple(sorted(states.items())))
            return

        unassigned = tuple(edge for edge in edges if edge not in states)

        def pressure(edge):
            return sum(
                3 - len({states[item] for item in incident[vertex]
                         if item in states and states[item] >= 0})
                for vertex in edge
            )

        edge = max(unassigned, key=pressure)
        for colour in COLORS:
            states[edge] = colour
            recurse()
        del states[edge]

    recurse()
    return tuple(completions)


def pure_support_profile(edges, target_edge, completion):
    """Necessary pure-row support when the target vector has w0=0.

    The target edge may support colours 1 and 2 but not colour 0.  This is a
    support test only: it never claims that supported pure rows normalize.
    """
    edge_set = set(edges)
    states = dict(completion)
    counts = []
    for colour in COLORS:
        count = 0
        for raw_matching in ORBIT.BASE.perfect_matchings(tuple(range(8))):
            matching = tuple(tuple(sorted(edge)) for edge in raw_matching)
            if not all(edge in edge_set for edge in matching):
                continue
            compatible = True
            for edge in matching:
                if edge == target_edge:
                    if colour == 0:
                        compatible = False
                        break
                elif states[edge] != colour:
                    compatible = False
                    break
            if compatible:
                count += 1
        counts.append(count)
    return tuple(counts)


def audit_prototype_negative_stratum():
    """Check C*P_bc=-2*B*Kbb*Kbc after imposing w^T K=0."""
    # Laurent variables are (B,C,Kbb,Kbc); negative C exponent records the
    # localization C != 0.  Row_c=-(B/C)row_b gives Kcb and Kcc below.
    b = variable(0, 4)
    c = variable(1, 4)
    kbb = variable(2, 4)
    kbc = variable(3, 4)
    c_inverse = {(-0, -1, 0, 0): 1}
    kcb = poly_scale(poly_multiply(b, c_inverse, kbb), -1)
    kcc = poly_scale(poly_multiply(b, c_inverse, kbc), -1)
    permanent = poly_add(
        poly_multiply(kbb, kcc), poly_multiply(kbc, kcb)
    )
    expected = poly_scale(poly_multiply(b, c_inverse, kbb, kbc), -2)
    require(permanent == expected,
            ("same-colour permanent substitution changed", permanent,
             expected))
    denominator_cleared = poly_multiply(c, permanent)
    require(denominator_cleared
            == poly_scale(poly_multiply(b, kbb, kbc), -2),
            ("denominator-cleared negative stratum changed",
             denominator_cleared))
    return {
        "localized_variables": ("B", "C", "Kbb", "Kbc"),
        "row_relation": "row_c=-(B/C)row_b",
        "permanent": permanent,
        "denominator_cleared": denominator_cleared,
        "activity_implication": (
            "B,C,Kbb,Kcc nonzero and Kcc=-(B/C)Kbc force Kbc nonzero; "
            "therefore P_bc is nonzero"
        ),
    }


def audit_unique_collision_terminal():
    prototype_audit = PROTOTYPE.audit_all_orbits()
    candidates = tuple(
        item for item in prototype_audit["graph_ledgers"]
        if item["route"] == "same-colour-completion-guard"
        and len(item["prototype_faces"]) >= 2
    )
    require(len(candidates) == 1,
            ("unique two-prototype collision orbit changed", candidates))
    candidate = candidates[0]
    require((candidate["graph_index"], candidate["orbit_size"],
             candidate["incidence"], candidate["role"])
            == (10, 1, (0, (0, 1)), "never-private"),
            ("collision representative changed", candidate))
    record = ORBIT.terminal_two_rrx_records()[candidate["graph_index"]]
    edges = tuple(record["representative_edges"])
    adjacency = ORBIT.adjacency_from_edges(edges)
    incidence = candidate["incidence"]
    target_edge = incidence[1]
    prototype_caps = tuple(
        item[0] for item in candidate["prototype_faces"]
    )
    require(prototype_caps == ((0, 6), (0, 7)),
            ("collision prototype caps changed", prototype_caps))
    states = dict(candidate["collision_completion"])
    require(states[target_edge] == NONANCHOR,
            ("target edge became coordinate", states))
    require({states[edge] for edge in prototype_caps} == {0},
            ("prototype collision colour changed", states))

    face_shapes = {}
    face_ledgers = {}
    for cap_edge in tuple(edge for edge in edges if incidence[0] in edge):
        through, residue = PROTOTYPE.cap_shape(
            adjacency, edges, incidence, cap_edge
        )
        if not through:
            continue
        face_shapes[cap_edge] = (len(through), len(residue))
        if cap_edge not in ((0, 3), (0, 5)):
            continue
        polynomials, residue_ledger = coordinate_residue_polynomials(
            adjacency, edges, cap_edge, incidence, states
        )
        words = target_words(
            adjacency, edges, cap_edge, incidence, states
        )
        require(set(polynomials).isdisjoint(
                    word for colour_words in words.values()
                    for word in colour_words),
                ("target and residue output words collided", cap_edge,
                 polynomials, words))
        face_ledgers[cap_edge] = {
            "residue_polynomials": polynomials,
            "residue_terms": residue_ledger,
            "target_words_by_colour": words,
        }

    require(face_shapes == {
        (0, 3): (2, 8), (0, 5): (2, 8),
        (0, 6): (2, 2), (0, 7): (2, 2),
    }, ("collision face shape ledger changed", face_shapes))

    cap03 = face_ledgers[(0, 3)]["residue_polynomials"]
    cap05 = face_ledgers[(0, 5)]["residue_polynomials"]
    expected03 = {
        "000101": poly_add(poly_multiply(k_variable(0, 1), k_variable(1, 0)),
                           poly_multiply(k_variable(0, 0), k_variable(1, 1))),
        "011101": poly_add(poly_multiply(k_variable(0, 1), k_variable(1, 0)),
                           poly_multiply(k_variable(0, 0), k_variable(1, 1))),
        "020102": poly_scale(poly_multiply(
            k_variable(0, 0), k_variable(1, 0)), 2),
        "000000": poly_scale(poly_multiply(
            k_variable(0, 0), k_variable(0, 0)), 2),
    }
    expected05 = {
        "212110": poly_add(poly_multiply(k_variable(0, 1), k_variable(2, 2)),
                           poly_multiply(k_variable(0, 2), k_variable(2, 1))),
        "202220": poly_add(poly_multiply(k_variable(0, 0), k_variable(2, 2)),
                           poly_multiply(k_variable(0, 2), k_variable(2, 0))),
        "102110": poly_add(poly_multiply(k_variable(0, 1), k_variable(2, 0)),
                           poly_multiply(k_variable(0, 0), k_variable(2, 1))),
        "200000": poly_scale(poly_multiply(
            k_variable(0, 0), k_variable(0, 2)), 2),
    }
    require(cap03 == expected03,
            ("cap03 residue polynomial ledger changed", cap03))
    require(cap05 == expected05,
            ("cap05 residue polynomial ledger changed", cap05))

    # Exact active-torus certificates.  The cap03 generator is itself
    # 2*K00^2.  For cap05, the following combination belongs to its ideal.
    cap03_private = cap03["000000"]
    require(cap03_private == poly_scale(poly_multiply(
        k_variable(0, 0), k_variable(0, 0)), 2),
        ("cap03 private square changed", cap03_private))
    g0 = cap05["200000"]
    g1 = cap05["202220"]
    certificate = poly_add(
        poly_scale(poly_multiply(k_variable(0, 0), g1), 2),
        poly_scale(poly_multiply(k_variable(2, 0), g0), -1),
    )
    expected_certificate = poly_scale(poly_multiply(
        k_variable(0, 0), k_variable(0, 0), k_variable(2, 2)), 2)
    require(certificate == expected_certificate,
            ("cap05 saturation certificate changed", certificate,
             expected_certificate))

    completions = all_collision_completions(
        edges, target_edge, prototype_caps
    )
    require(candidate["collision_completion"] in completions,
            "canonical collision completion left exhaustive census")
    pure_profiles = Counter(
        pure_support_profile(edges, target_edge, completion)
        for completion in completions
    )
    missing_pure = sum(
        multiplicity for profile, multiplicity in pure_profiles.items()
        if 0 in profile
    )

    return {
        "graph_index": candidate["graph_index"],
        "orbit_size": candidate["orbit_size"],
        "role": candidate["role"],
        "representative_edges": edges,
        "directed_source_incidence": incidence,
        "prototype_caps": prototype_caps,
        "canonical_collision_completion": candidate["collision_completion"],
        "all_source_response_shapes": tuple(sorted(face_shapes.items())),
        "higher_rank_face_ledgers": tuple(sorted(face_ledgers.items())),
        "cap03_active_obstruction": cap03_private,
        "cap05_saturation_certificate": certificate,
        "collision_completion_count": len(completions),
        "pure_support_profile_histogram": tuple(sorted(pure_profiles.items())),
        "collision_completions_missing_a_pure_support": missing_pure,
        "prototype_negative_stratum": audit_prototype_negative_stratum(),
        "source_typing_warning": (
            "K03,K05,K06,K07 are independently typed cap covectors; no "
            "common-K construction is source-valid"
        ),
    }


def canonical(value):
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    ledger = canonical(audit_unique_collision_terminal())
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("same-colour collision terminal ledger changed", digest))

    profiles = ledger["pure_support_profile_histogram"]
    print("N=8 support-16 same-colour collision higher-rank terminal: PASS")
    print("  residual two-prototype stabilizer orbits: 1")
    print("  collision completions:", ledger["collision_completion_count"])
    print("  cap03 / cap05 residue terms: 8 / 8")
    print("  larger-face active-zero exits: 0 / 2")
    print("  pure-support profiles:", profiles)


if __name__ == "__main__":
    main()
