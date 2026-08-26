#!/usr/bin/env python3
"""Exact bounded screen for the global matching automaton/MPS quotient."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_global_minimal_mps.json"
PEPS = (ROOT / "computations/unaudited-codex-onehot-peps-holant-2026-08-21" /
        "results_onehot_peps_holant.json")
REES = (ROOT / "computations/unaudited-codex-x5-global-base-locus-2026-08-21" /
        "results_x5_global_base_locus.json")
PEPS_DIGEST = "6130619bd6a1c8efdebb17ca47f7db98582e128cc332070dbc340083bf7442b5"
REES_DIGEST = "f78123a1763b9632b1a00b10f29acae7663a61d5b18f356e835e9be5ff5b9296"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


# Laurent polynomials in t, represented by exponent -> integer coefficient.
def add(left, right):
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, 0) + coefficient
        if not answer[exponent]:
            del answer[exponent]
    return answer


def mul(left, right):
    answer = {}
    for a, x in left.items():
        for b, y in right.items():
            answer[a+b] = answer.get(a+b, 0) + x*y
    return {exponent: coefficient for exponent, coefficient in answer.items()
            if coefficient}


ONE = {0: 1}


def evaluate(polynomial, value):
    require(value or all(exponent >= 0 for exponent in polynomial),
            ("negative exponent at t=0", polynomial))
    return sum(Fraction(coefficient) * Fraction(value) ** exponent
               for exponent, coefficient in polynomial.items())


def valuation(polynomial):
    require(polynomial, "zero polynomial has no valuation")
    return min(polynomial)


def state_label(state):
    if not state:
        return "empty"
    return "{" + ",".join(f"{site}:{colour}" for site, colour in state) + "}"


def source_cell(source, left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    exponent = source.get((left, right, left_colour, right_colour))
    return {} if exponent is None else {exponent: 1}


def step(vector, site, colour, source, number_of_sites):
    """Read one physical symbol in the literal open-boundary matching DP."""
    answer = {}
    remaining_after = number_of_sites-site-1
    for state, coefficient in vector.items():
        # Leave this site open for a future matching edge.
        if len(state)+1 <= remaining_after:
            opened = state + ((site, colour),)
            answer[opened] = add(answer.get(opened, {}), coefficient)
        # Or close it against one earlier open site using the literal cell.
        for index, (left, left_colour) in enumerate(state):
            weight = source_cell(source, left, site, left_colour, colour)
            if weight:
                closed = state[:index] + state[index+1:]
                answer[closed] = add(answer.get(closed, {}),
                                     mul(coefficient, weight))
    return {state: coefficient for state, coefficient in answer.items()
            if coefficient}


def forward(prefix, source, number_of_sites):
    vector = {(): ONE}
    for site, colour in enumerate(prefix):
        vector = step(vector, site, colour, source, number_of_sites)
    return vector


def completion(state, suffix, cut, source, number_of_sites):
    vector = {state: ONE}
    for offset, colour in enumerate(suffix):
        vector = step(vector, cut+offset, colour, source, number_of_sites)
    return vector.get((), {})


def outputs(source, number_of_sites):
    answer = {}
    for word in product(range(3), repeat=number_of_sites):
        amplitude = forward(word, source, number_of_sites).get((), {})
        if amplitude:
            answer[word] = amplitude
    return answer


def exact_rank(matrix):
    work = [[Fraction(entry) for entry in row] for row in matrix]
    row = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next((index for index in range(row, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        pivot_value = work[row][column]
        for index in range(row+1, len(work)):
            if not work[index][column]:
                continue
            scale = work[index][column]/pivot_value
            for other in range(column, width):
                work[index][other] -= scale*work[row][other]
        row += 1
        if row == len(work):
            break
    return row


def flatten_rank(output, number_of_sites, cut, value):
    prefixes = sorted({word[:cut] for word in output})
    suffixes = sorted({word[cut:] for word in output})
    prefix_index = {word: index for index, word in enumerate(prefixes)}
    suffix_index = {word: index for index, word in enumerate(suffixes)}
    matrix = [[Fraction(0) for _ in suffixes] for _ in prefixes]
    for word, coefficient in output.items():
        matrix[prefix_index[word[:cut]]][suffix_index[word[cut:]]] = \
            evaluate(coefficient, value)
    return exact_rank(matrix)


def n4_source():
    matchings = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    source = {}
    for colour, matching in matchings.items():
        for left, right in matching:
            source[left, right, colour, colour] = 0
    return source, matchings


def matching_boundary_state(matching, colour, cut):
    return tuple(sorted((left, colour) for left, right in matching
                        if left < cut <= right))


def n4_audit():
    source, matchings = n4_source()
    output = outputs(source, 4)
    expected = {(colour,)*4: ONE for colour in range(3)}
    require(output == expected, "n=4 source stopped producing exact GHZ")
    ranks = [flatten_rank(output, 4, cut, 2) for cut in range(1, 4)]
    require(ranks == [3, 3, 3], ranks)

    quotient_states = {
        cut: {colour: matching_boundary_state(matchings[colour], colour, cut)
              for colour in range(3)}
        for cut in range(1, 4)
    }
    # Projection sends the three matching-path boundary states to colours and
    # every other state to zero.  Check the diagonal-copy intertwiner on the
    # full reachable row space, not just on the three pure paths.
    for cut in range(1, 4):
        reverse = {state: colour
                   for colour, state in quotient_states[cut].items()}
        require(len(reverse) == 3, (cut, quotient_states[cut]))
        for prefix in product(range(3), repeat=cut):
            projected = [dict() for _ in range(3)]
            for state, coefficient in forward(prefix, source, 4).items():
                if state in reverse:
                    colour = reverse[state]
                    projected[colour] = add(projected[colour], coefficient)
            expected_projection = [dict() for _ in range(3)]
            if len(set(prefix)) == 1:
                expected_projection[prefix[0]] = ONE
            require(projected == expected_projection,
                    ("n=4 quotient projection failed", cut, prefix,
                     projected, expected_projection))

    middle_profiles = []
    for ordering in permutations(range(4)):
        left = set(ordering[:2])
        counts = []
        for colour in range(3):
            crossing = sum((u in left) != (v in left)
                           for u, v in matchings[colour])
            counts.append(crossing)
        middle_profiles.append(tuple(sorted(counts)))
    require(set(middle_profiles) == {(0, 2, 2)} and len(middle_profiles) == 24,
            set(middle_profiles))
    return {
        "source": "colour c uses its own perfect matching of K4",
        "nonzero_output": {"".join(map(str, word)): list(poly.items())
                           for word, poly in output.items()},
        "internal_flattening_ranks": ranks,
        "quotient_states_by_cut": {
            str(cut): {str(colour): state_label(state)
                       for colour, state in states.items()}
            for cut, states in quotient_states.items()},
        "all_24_orderings_middle_crossing_profile": [0, 2, 2],
        "milestone": (
            "The reachable/observable quotient is the diagonal three-colour "
            "copy automaton, but at every middle cut one colour is represented "
            "by the empty boundary and two colours by two crossing edges."
        ),
    }


def laurent_source(power):
    edge_data = {
        (0, 1): (0, -power), (0, 3): (1, 0),
        (0, 7): (2, 0), (1, 4): (2, 0),
        (1, 6): (1, 0), (2, 3): (2, 0),
        (2, 4): (1, 0), (2, 5): (0, power),
        (3, 4): (0, 0), (5, 6): (2, 0),
        (5, 7): (1, 0), (6, 7): (0, 0),
    }
    return {(left, right, colour, colour): exponent
            for (left, right), (colour, exponent) in edge_data.items()}


def cut_contribution(word, cut, source, number_of_sites):
    prefix, suffix = word[:cut], word[cut:]
    answer = []
    for state, left in forward(prefix, source, number_of_sites).items():
        right = completion(state, suffix, cut, source, number_of_sites)
        if right:
            answer.append((state, left, right, mul(left, right)))
    return answer


def laurent_audit():
    expected_words = {
        (0,)*8: 0, (1,)*8: 0, (2,)*8: 0,
        tuple(map(int, "12012000")): 1,
        tuple(map(int, "21000012")): 1,
    }
    source = laurent_source(1)
    output = outputs(source, 8)
    require({word: valuation(poly) for word, poly in output.items()} ==
            expected_words, output)
    generic_ranks = [flatten_rank(output, 8, cut, 2)
                     for cut in range(1, 8)]
    require(generic_ranks == [3, 5, 5, 5, 4, 4, 3], generic_ranks)
    require(generic_ranks == [flatten_rank(output, 8, cut, 3)
                              for cut in range(1, 8)],
            "generic ranks changed between t=2 and t=3")
    special_ranks = [flatten_rank(output, 8, cut, 0)
                     for cut in range(1, 8)]
    require(special_ranks == [3]*7, special_ranks)

    cut_two = []
    for word in sorted(output):
        contributions = cut_contribution(word, 2, source, 8)
        require(len(contributions) == 1, (word, contributions))
        state, left, right, total = contributions[0]
        cut_two.append({
            "word": "".join(map(str, word)),
            "state": state_label(state),
            "forward_order": valuation(left),
            "backward_order": valuation(right),
            "total_order": valuation(total),
        })

    power_controls = {}
    for power in (1, 2, 7):
        result = outputs(laurent_source(power), 8)
        observed = {"".join(map(str, word)): valuation(poly)
                    for word, poly in result.items()}
        expected = {"00000000": 0, "11111111": 0, "22222222": 0,
                    "12012000": power, "21000012": power}
        require(observed == expected, (power, observed))
        zero_word = (0,)*8
        contribution = cut_contribution(zero_word, 2,
                                        laurent_source(power), 8)
        require(len(contribution) == 1, contribution)
        _state, left, right, _total = contribution[0]
        require((valuation(left), valuation(right)) == (-power, power),
                (power, left, right))
        power_controls[str(power)] = {
            "pure_zero_cut2_orders": [-power, power],
            "mixed_output_orders": [power, power],
        }
    return {
        "generic_flattening_ranks": generic_ranks,
        "GHZ_special_fibre_flattening_ranks": special_ranks,
        "cut2_source_faithful_factorization": cut_two,
        "valuation_redistribution_controls": power_controls,
        "singular_gauge": (
            "At cut two the colour-zero state has forward/backward orders "
            "(-N,+N). Normalizing both to order zero uses the state gauge "
            "diag(t^N,1,1), which is not invertible at t=0. The two mixed "
            "states have backward order N and disappear in the special fibre."
        ),
    }


def invisible_source(extra):
    edges = {(0, 1), (2, 3), (4, 5), (6, 7)}
    if extra:
        edges.add((0, 2))
    return {(left, right, 0, 0): 0 for left, right in edges}


def reachable_states(source, cut, number_of_sites):
    states = set()
    for prefix in product(range(3), repeat=cut):
        states.update(forward(prefix, source, number_of_sites))
    return states


def is_observable(state, source, cut, number_of_sites):
    return any(completion(state, suffix, cut, source, number_of_sites)
               for suffix in product(range(3), repeat=number_of_sites-cut))


def invisible_audit():
    base, enlarged = invisible_source(False), invisible_source(True)
    base_output, enlarged_output = outputs(base, 8), outputs(enlarged, 8)
    expected = {(0,)*8: ONE}
    require(base_output == enlarged_output == expected,
            (base_output, enlarged_output))
    base_reachable = reachable_states(base, 3, 8)
    enlarged_reachable = reachable_states(enlarged, 3, 8)
    new_states = enlarged_reachable-base_reachable
    witness = ((1, 0),)
    require(witness in new_states, new_states)
    require(not is_observable(witness, enlarged, 3, 8),
            "invisible-chord state became observable")
    base_essential = {state for state in base_reachable
                      if is_observable(state, base, 3, 8)}
    enlarged_essential = {state for state in enlarged_reachable
                          if is_observable(state, enlarged, 3, 8)}
    require(base_essential == enlarged_essential,
            (base_essential, enlarged_essential))
    return {
        "base_support_edges": 4,
        "enlarged_support_edges": 5,
        "added_edge": [0, 2],
        "common_output": "e_0^tensor8",
        "common_internal_flattening_ranks": [1]*7,
        "new_cut3_reachable_state": state_label(witness),
        "new_state_observable": False,
        "reachable_observable_state_sets_equal": True,
        "meaning": (
            "The extra literal edge creates a reachable direction, but it lies "
            "in the observable kernel. Minimalization erases exactly the edge "
            "coordinate whose deletion gives strict support descent."
        ),
    }


def main():
    peps = json.loads(PEPS.read_text())
    rees = json.loads(REES.read_text())
    require(peps["logical_sha256"] == PEPS_DIGEST,
            "frozen invisible-chord digest changed")
    require(rees["logical_sha256"] == REES_DIGEST,
            "frozen Laurent boundary digest changed")
    payload = {
        "status": "PASS exact global minimal-MPS bounded no-go",
        "automaton": {
            "boundary_basis": (
                "(S,alpha), where S is the set of processed unmatched sites "
                "and alpha records their physical colours"
            ),
            "transition": (
                "on symbol c at site j: open (j,c), or close i in S with "
                "literal weight A_ij[alpha(i),c]"
            ),
            "factorization": "H cut flattening = R_k O_k",
            "minimal_dimension": "rank(R_k O_k), hence 3 for exact GHZ",
            "exact_GHZ_minimal_form": (
                "the diagonal three-state copying automaton, up to internal "
                "GL3 gauges"
            ),
        },
        "n4_exact_GHZ": n4_audit(),
        "n8_Laurent_boundary": laurent_audit(),
        "invisible_chord_control": invisible_audit(),
        "remote_idempotent": {
            "controlled": False,
            "reason": (
                "The minimal automaton and all its canonical transitions factor "
                "through the top output tensor. The remote idempotent is source-"
                "relative tail data lying in reachable/observable kernels."
            ),
        },
        "verdict": {
            "diagonal_minimality_forces_clean_cap": False,
            "diagonal_minimality_forces_uniform_two_site_or_six_site_quotient": False,
            "diagonal_minimality_identifies_literal_support_descent": False,
            "smallest_missing_lemma": (
                "A source-relative kernel-lifting theorem: in a support-minimal "
                "exact source, turn every reachable/observable-kernel direction "
                "into either a deletable literal coordinate or an active cap."
            ),
            "reason": (
                "The n=4 exact model has diagonal minimal transitions but mixed "
                "boundary degrees (0,2,2); the Laurent GHZ limit needs a singular "
                "state gauge and hides arbitrarily large source valuations; the "
                "invisible chord is erased by the observable quotient."
            ),
            "retire_output_only_minimal_MPS": True,
        },
        "scope": {
            "broad_symbolic_solve": False,
            "claim_about_nonexistence_of_exact_n8_source": False,
            "upstream_digests": {
                "onehot_peps_holant": PEPS_DIGEST,
                "global_base_locus": REES_DIGEST,
            },
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps({
        "logical_sha256": payload["logical_sha256"],
        "n4_middle_profile": payload["n4_exact_GHZ"][
            "all_24_orderings_middle_crossing_profile"],
        "n8_generic_ranks": payload["n8_Laurent_boundary"][
            "generic_flattening_ranks"],
        "n8_special_ranks": payload["n8_Laurent_boundary"][
            "GHZ_special_fibre_flattening_ranks"],
        "invisible_state_observable": payload["invisible_chord_control"][
            "new_state_observable"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
