#!/usr/bin/env python3
"""Exact local test for the confluent-C4/HPL interpretation.

The chart-25 four-row functional is first decoded as a circuit between the
two perfect matchings

    A=(13)(56),  B=(15)(36)

on its residual four vertices.  Three rows contain one A term and one B
term, whereas the fourth contains two B terms.  This proves a small but
useful no-go statement: a first confluent derivative of the alternating
minor ``A_i B_j-A_j B_i`` cannot produce the fourth row, because its first
jet is ``U_i B_j-U_j B_i`` and has zero B^2 projection.

The script then gives a four-dimensional toy homological-perturbation model
in which the first transferred term produces the three cycle rows and the
second term produces the parallel-pair row with exactly the observed signs.
This proves consistency of the proposed mechanism, not its realization by
the literal hafnian source complex.

Finally the analogous four-term packet is embedded into the frozen chart-26
C4.  Its support-stabilizer/color orbit has no leading term dividing either
path-bearing degree-six colon lead, and the chosen packet is irreducible by
the complete degree-four layer.  The existing exact colon audit is replayed
to ensure that the packet has not been mistaken for a lower source identity.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "e637b076a0b447ecf68558cdda85fdbfbb7dac9a836bcbb3eab74ed46cbcfe4f"
)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DUAL = load(
    "n8_confluent_chart25_dual",
    "verify_n8_chart25_degree4_exact_dual.py",
)
COLON = load(
    "n8_confluent_chart26_colon",
    "verify_n8_chart26_c4_primitive_colon.py",
)
C4 = COLON.C4
D5 = COLON.D5
FIRST = COLON.FIRST
WEIGHT = COLON.WEIGHT


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_value(vector, key, value):
    result = vector.get(key, QQ(0)) + value
    if result:
        vector[key] = result
    else:
        vector.pop(key, None)


def add_scaled(target, source, scalar=1):
    for key, value in source.items():
        add_value(target, key, QQ(scalar) * value)


def apply_map(linear_map, vector):
    answer = {}
    for basis, coefficient in vector.items():
        add_scaled(answer, linear_map.get(basis, {}), coefficient)
    return answer


def compose(left, right, vector):
    return apply_map(left, apply_map(right, vector))


def chart25_matching_monomial(matching, assignment):
    return bytes(sorted(
        DUAL.BASE.COORDINATE_ID[
            (left, right, assignment[left], assignment[right])
        ]
        for left, right in matching
    ))


def product(first, second):
    return bytes(sorted(first + second))


def audit_chart25_circuit():
    matching_a = ((1, 3), (5, 6))
    matching_b = ((1, 5), (3, 6))
    states = {
        "u": {1: 1, 3: 1, 5: 1, 6: 1},
        "v": {1: 2, 3: 2, 5: 2, 6: 2},
        "s": {1: 1, 3: 2, 5: 1, 6: 2},
        "t": {1: 2, 3: 1, 5: 2, 6: 1},
    }
    a = {
        state: chart25_matching_monomial(matching_a, assignment)
        for state, assignment in states.items()
    }
    b = {
        state: chart25_matching_monomial(matching_b, assignment)
        for state, assignment in states.items()
    }
    residuals = (
        product(a["u"], b["v"]),
        product(a["s"], b["t"]),
        product(a["t"], b["s"]),
        product(b["u"], b["v"]),
    )
    require(tuple(row.hex() for row in residuals) == (
        "4c62bce5", "4d62b8e6", "4f5ebce8", "5e62b8bc"
    ), "chart-25 matching factorization changed")

    rows_by_residual = {}
    common = set(DUAL.EXPECTED_COMMON_FACTOR)
    for row, value in DUAL.FUNCTIONAL.items():
        residual = bytes(variable for variable in row if variable not in common)
        rows_by_residual[residual] = (row, value)
    require(set(rows_by_residual) == set(residuals),
            "chart-25 circuit support changed")

    orbit_sizes = []
    actual_weights = []
    degrees = []
    quotient_values = []
    for residual in residuals:
        row, value = rows_by_residual[residual]
        orbit = {
            bytes(sorted(transform[index] for index in row))
            for transform in DUAL.BASE.TRANSFORMS
        }
        orbit_sizes.append(len(orbit))
        actual_weights.append(QQ(value, len(orbit)))
        degrees.append(DUAL.BASE.row_degree(row))
        quotient_values.append(value)
    require(quotient_values == [-2, -1, -1, 1],
            "chart-25 quotient cochain changed")
    require(orbit_sizes == [8, 4, 4, 4],
            "chart-25 row-orbit sizes changed")
    require(actual_weights == [QQ(-1, 4)] * 3 + [QQ(1, 4)],
            "actual chart-25 cochain lost uniform local signs")
    require(degrees == [2, 2, 2, 4],
            "chart-25 filtration split changed")
    return {
        "matching_A": [list(edge) for edge in matching_a],
        "matching_B": [list(edge) for edge in matching_b],
        "residuals": [row.hex() for row in residuals],
        "quotient_values": quotient_values,
        "row_orbit_sizes": orbit_sizes,
        "actual_row_weights": [
            [value.numerator, value.denominator] for value in actual_weights
        ],
        "filtration_degrees": degrees,
    }


def audit_first_jet_no_go():
    # The coefficient of epsilon in
    # det((B_i+epsilon U_i, B_j+epsilon U_j),(B_i,B_j)).
    first_jets = {}
    for first in range(4):
        for second in range(first + 1, 4):
            jet = {
                tuple(sorted((f"U{first}", f"B{second}"))): 1,
                tuple(sorted((f"U{second}", f"B{first}"))): -1,
            }
            require(all(not (
                left.startswith("B") and right.startswith("B")
            ) for left, right in jet),
                    "an alternating first jet acquired a B^2 term")
            first_jets[f"{first}{second}"] = [
                [list(monomial), coefficient]
                for monomial, coefficient in sorted(jet.items())
            ]
    return {
        "first_jet_minors": first_jets,
        "parallel_B2_projection_rank": 0,
        "conclusion": (
            "one alternating first jet cannot produce the parallel-pair row"
        ),
    }


def audit_toy_hpl():
    # C consists of homology representatives x,A,B,C,D and one acyclic pair
    # u -> v.  The maps below are a literal contraction of (C,d0) onto H.
    basis = ("x", "A", "B", "C", "D", "u", "v")
    homology = {"x", "A", "B", "C", "D"}
    d0 = {"u": {"v": QQ(1)}}
    h = {"v": {"u": QQ(1)}}
    projection = {
        item: {item: QQ(1)} for item in homology
    }
    inclusion = dict(projection)
    identity = {item: {item: QQ(1)} for item in basis}

    for item in basis:
        left = compose(d0, h, {item: QQ(1)})
        add_scaled(left, compose(h, d0, {item: QQ(1)}))
        right = dict(identity[item])
        add_scaled(
            right,
            compose(inclusion, projection, {item: QQ(1)}),
            -1,
        )
        require(left == right, "the toy HPL contraction identity failed")

    perturbation = {
        "x": {"A": QQ(-1), "B": QQ(-1), "C": QQ(-1), "v": QQ(1)},
        "u": {"D": QQ(-1)},
    }
    source = {"x": QQ(1)}
    # Inclusion is the identity on x; spell the higher terms out to keep the
    # HPL signs visible.
    first = compose(projection, perturbation, source)
    second = compose(
        projection, perturbation,
        compose(h, perturbation, source),
    )
    second = {item: -value for item, value in second.items()}
    third = compose(
        projection, perturbation,
        compose(h, perturbation,
                compose(h, perturbation, source)),
    )
    transferred = dict(first)
    add_scaled(transferred, second)
    add_scaled(transferred, third)
    require(first == {"A": -1, "B": -1, "C": -1},
            "the toy first transferred term changed")
    require(second == {"D": 1},
            "the toy second transferred term changed")
    require(not third, "the toy HPL series did not terminate")
    require(transferred == {"A": -1, "B": -1, "C": -1, "D": 1},
            "the toy HPL packet changed")
    encode = lambda vector: {
        item: int(value) for item, value in vector.items()
    }
    return {
        "d0": {"u": {"v": 1}},
        "delta_x": {"A": -1, "B": -1, "C": -1, "v": 1},
        "delta_u": {"D": -1},
        "p_delta_i": encode(first),
        "minus_p_delta_h_delta_i": encode(second),
        "higher_terms": len(third),
        "transferred_packet": encode(transferred),
    }


def local_code(local_word):
    code = 0
    for colour in local_word:
        code = 3 * code + colour
    require(D5.decode_word(code)[4:] == tuple(local_word),
            "local word encoding changed")
    return code


def normalized_chart26_packet(first_colour, second_colour):
    u = local_code((first_colour,) * 4)
    v = local_code((second_colour,) * 4)
    s = local_code((first_colour, second_colour,
                    second_colour, first_colour))
    t = local_code((second_colour, first_colour,
                    first_colour, second_colour))
    terms = (
        (1, C4.N, u, C4.N, v),
        (-1, C4.M, u, C4.N, v),
        (-1, C4.M, s, C4.N, t),
        (-1, C4.M, t, C4.N, s),
    )
    raw = {}
    for coefficient, first_matching, first_state, second_matching, second_state in terms:
        row = product(
            C4.matching_monomial(first_matching, first_state),
            C4.matching_monomial(second_matching, second_state),
        )
        add_value(raw, row, coefficient)
    common = C4.common_monomial((raw,))
    return common, COLON.normalize_quotient(raw, common)


def order_key(row):
    return -len(row), -WEIGHT.weight(row), row


def transform_packet(packet, transform):
    answer = {}
    for row, coefficient in packet.items():
        transformed = bytes(sorted(
            output
            for output in (transform[variable] for variable in row)
            if D5.IS_OFF_SUPPORT[output]
        ))
        add_value(answer, transformed, coefficient)
    return answer


def audit_chart26_packet():
    common, packet = normalized_chart26_packet(1, 2)
    require(common.hex() == "09094848",
            "the chart-26 confluent packet core changed")
    require({row.hex(): value for row, value in packet.items()} == {
        "cae0f7": -1,
        "cbe0e5fa": -1,
        "cddcf8": -1,
        "dce0e5": 1,
    }, "the chart-26 four-term packet changed")
    packet_lead = min(packet, key=order_key)
    require(packet_lead.hex() == "cbe0e5fa",
            "the chart-26 packet lead changed")

    _originals, original_lead_to_code = FIRST.original_basis()
    require(packet_lead not in original_lead_to_code,
            "the confluent packet entered the degree-four source span")

    bad_leads = (
        bytes.fromhex("0951acc6f4f4"),
        bytes.fromhex("0952acc6f4f4"),
    )
    orbit_records = []
    dividing = []
    distinct_leads = set()
    for first_colour, second_colour in permutations(range(3), 2):
        _, coloured_packet = normalized_chart26_packet(
            first_colour, second_colour
        )
        for transform_index, transform in enumerate(D5.VARIABLE_TRANSFORMS):
            transformed = transform_packet(coloured_packet, transform)
            lead = min(transformed, key=order_key)
            distinct_leads.add(lead)
            hits = [
                bad.hex() for bad in bad_leads
                if FIRST.quotient(bad, lead) is not None
            ]
            dividing.extend(hits)
            orbit_records.append({
                "colours": [first_colour, second_colour],
                "transform": transform_index,
                "lead": lead.hex(),
                "divides_bad_leads": hits,
            })
    require(len(orbit_records) == 24 and len(distinct_leads) == 15,
            "the bounded chart-26 packet orbit changed")
    require(not dividing,
            "a bounded confluent-packet lead began reducing a bad class")

    colon_ledger, colon_digest = COLON.audit()
    require(colon_digest == COLON.EXPECTED_LEDGER_SHA256,
            "the chart-26 primitive colon audit changed")
    require([
        record["degree6_remainder_lead"]
        for record in colon_ledger["bad_representatives"]
    ] == [bad.hex() for bad in bad_leads],
            "the path-bearing colon leads changed")
    return {
        "common_factor": common.hex(),
        "packet": {
            row.hex(): int(value) for row, value in sorted(packet.items())
        },
        "weighted_lead": packet_lead.hex(),
        "degree4_reduction_steps": 0,
        "colour_stabilizer_packets": len(orbit_records),
        "distinct_orbit_leads": len(distinct_leads),
        "orbit_leads_dividing_bad_classes": len(dividing),
        "bad_degree6_leads": [bad.hex() for bad in bad_leads],
        "primitive_colon_sha256": colon_digest,
    }


def audit():
    ledger = {
        "chart25_circuit": audit_chart25_circuit(),
        "alternating_first_jet": audit_first_jet_no_go(),
        "toy_hpl": audit_toy_hpl(),
        "chart26_bounded_test": audit_chart26_packet(),
        "conclusion": (
            "the parallel row is impossible for one alternating first jet "
            "but is exactly compatible with the second HPL transfer term; "
            "the natural bounded chart26 packet does not reduce either colon"
        ),
        "scope_guard": (
            "the toy contraction proves algebraic consistency only; a "
            "source-labelled hafnian contraction and target comparison remain"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the confluent-C4/HPL ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print(
        "n=8 confluent C4/HPL model: PASS; "
        "first jet no-go, second transfer consistent, chart26 colon survives"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
