#!/usr/bin/env python3
"""Exact spoke-to-hole/Koszul boundary for canonical C6 word z=012111.

After the seven offanchor unary competitors are routed, the six remaining
matching monomials all use one edge 1-r, r in {0,3,4,5}.  Grouping by r
gives four common-tail classes of sizes 1,2,2,1.  The unary z row evaluates
the tail vector against q_1r, while the G11/G21 slices through the selected
s1@1:1 port evaluate it against the required word-changed p1/p2 entries.
The resulting q/p Koszul identity is literal.  If those p entries are
absent, the selected-port response differential is zero and cannot consume
the unary class; this is the exact first endpoint-word separator.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_c6_first_transgression_selected_port_boundary.py":
        "8729c85d5af458966942e567e5e840da9fe0acf0a9d89684b846bee82b791f9a",
    "notes/h3-c6-first-transgression-selected-port-boundary.md":
        "03bed57e2a1955795806b590e586c16e3a25948e719ff1d589a462460a8684b1",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
    "computations/verify_hafnian_private_site_matching_bijection_lemma.py":
        "310167f3f51cdbf7619497662b29b267f2d34de4c7e67c00110dba55d4c77efc",
    "notes/hafnian-private-site-matching-bijection-lemma.md":
        "97a0d153a2b275e7d81b2c1f54c9ba29b3d977ca439a7df4c0023b0e062856be",
}
EXPECTED_LEDGER_SHA256 = "6d65dad8ef8a5c4b92ffac320d87e22e3222e9f0d318602f490dba17b7618638"

Z = (0, 1, 2, 1, 1, 1)
SITES = tuple(range(6))
OLD_BASES = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 1), (2, 4), (3, 5)),
    ((0, 2), (1, 5), (3, 4)),
    ((0, 5), (1, 2), (3, 4)),
)
OLD_UNION = set().union(*(set(base) for base in OLD_BASES))
M = OLD_BASES[0]
N = OLD_BASES[3]
ANCHOR_COMPETITORS = (
    ((0, 1), (2, 4), (3, 5)),
    ((0, 2), (1, 3), (4, 5)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 2), (1, 5), (3, 4)),
    ((0, 5), (1, 3), (2, 4)),
    ((0, 5), (1, 4), (2, 3)),
)
PARTNERS = (0, 3, 4, 5)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return tuple(answer)


MATCHINGS = perfect_matchings(SITES)


def polynomial(*terms):
    answer = Counter()
    for coefficient, variables in terms:
        answer[tuple(sorted(variables))] += coefficient
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def add(*scaled):
    answer = Counter()
    for scalar, value in scaled:
        for monomial, coefficient in value.items():
            answer[monomial] += scalar * coefficient
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def multiply(left, right):
    answer = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def variable(name):
    return polynomial((1, (name,)))


def q_name(edge):
    return f"q{edge[0]}{edge[1]}_{Z[edge[0]]}{Z[edge[1]]}"


def tail_monomial(tail):
    value = polynomial((1, ()))
    for edge in tail:
        value = multiply(value, variable(q_name(edge)))
    return value


def partner_and_tail(matching):
    incident = next(edge for edge in matching if 1 in edge)
    partner = incident[0] if incident[1] == 1 else incident[1]
    tail = tuple(edge for edge in matching if edge != incident)
    return partner, tail


def audit_six_classes():
    groups = {partner: [] for partner in PARTNERS}
    for matching in ANCHOR_COMPETITORS:
        partner, tail = partner_and_tail(matching)
        require(partner in groups,
                "an anchor competitor acquired a new site-1 partner")
        groups[partner].append(tail)
    require({partner: len(tails) for partner, tails in groups.items()}
            == {0: 1, 3: 2, 4: 2, 5: 1},
            "the 1/2/2/1 tail profile changed")

    # For every fixed partner there are three residual tails.  After M,N
    # are removed, every tail not in the six-class inventory has an
    # offdiagonal physical edge outside the old four-base union.
    routing = {}
    for partner in PARTNERS:
        remaining = tuple(site for site in SITES
                          if site not in (1, partner))
        all_tails = perfect_matchings(remaining)
        selected = set(groups[partner])
        external = []
        old_excluded = []
        for tail in all_tails:
            matching = tuple(sorted(((min(1, partner), max(1, partner)),)
                                    + tail))
            if matching in (M, N):
                old_excluded.append(tail)
                continue
            if tail in selected:
                continue
            cells = tuple((edge, (Z[edge[0]], Z[edge[1]]))
                          for edge in matching)
            require(any(edge not in OLD_UNION and colours[0] != colours[1]
                        for edge, colours in cells),
                    "a nonselected tail stopped being an offanchor route")
            external.append(tail)
        routing[partner] = {
            "anchor_tails": tuple(groups[partner]),
            "old_M_or_N_tails": tuple(old_excluded),
            "external_tails": tuple(external),
        }
    require(sum(len(record["external_tails"])
                for record in routing.values()) == 5,
            "the grouped external-tail count changed")
    # The other two of the seven routes have site-1 partners 2 and hence do
    # not enter the four surviving partner classes.
    partner_two_external = []
    for matching in MATCHINGS:
        if matching in (M, N) or matching in ANCHOR_COMPETITORS:
            continue
        partner, tail = partner_and_tail(matching)
        if partner == 2:
            cells = tuple((edge, (Z[edge[0]], Z[edge[1]]))
                          for edge in matching)
            require(any(edge not in OLD_UNION and colours[0] != colours[1]
                        for edge, colours in cells),
                    "a partner-2 competitor stopped routing")
            partner_two_external.append(tail)
    require(len(partner_two_external) == 2,
            "the partner-2 external count changed")
    return groups, routing, tuple(partner_two_external)


def audit_common_tail_rows(groups):
    tails = {}
    for partner, records in groups.items():
        value = Counter()
        for tail in records:
            value = add((1, value), (1, tail_monomial(tail)))
        tails[partner] = value

    unary = Counter()
    responses = {colour: Counter() for colour in (1, 2)}
    for partner in PARTNERS:
        q_edge = tuple(sorted((1, partner)))
        unary = add((1, unary),
                    (1, multiply(variable(q_name(q_edge)), tails[partner])))
        for colour in (1, 2):
            p_name = f"p{colour}_{partner}_{Z[partner]}"
            responses[colour] = add(
                (1, responses[colour]),
                (1, multiply(variable(p_name), tails[partner])),
            )

    expected_unary = Counter()
    for matching in ANCHOR_COMPETITORS:
        expected_unary = add((1, expected_unary),
                             (1, tail_monomial(matching)))
    require(unary == expected_unary,
            "the six-monomial unary grouping changed")

    # Exact Koszul/private-site identity for each endpoint row and pivot r:
    # q_r R_i - p_ir H = sum_s (q_r p_is-p_ir q_s) T_s.
    koszul = []
    for colour in (1, 2):
        for pivot in PARTNERS:
            q_pivot = variable(q_name(tuple(sorted((1, pivot)))))
            p_pivot = variable(f"p{colour}_{pivot}_{Z[pivot]}")
            left = add(
                (1, multiply(q_pivot, responses[colour])),
                (-1, multiply(p_pivot, unary)),
            )
            right = Counter()
            for partner in PARTNERS:
                if partner == pivot:
                    continue
                q_partner = variable(q_name(tuple(sorted((1, partner)))))
                p_partner = variable(
                    f"p{colour}_{partner}_{Z[partner]}"
                )
                minor = add((1, multiply(q_pivot, p_partner)),
                            (-1, multiply(p_pivot, q_partner)))
                right = add((1, right),
                            (1, multiply(minor, tails[partner])))
            require(left == right,
                    "a common-tail Koszul identity changed")
            koszul.append({
                "endpoint_row": f"p{colour}",
                "pivot_partner": pivot,
                "identity": (
                    f"q_1{pivot}*R_{colour}-p{colour}_{pivot}*H="
                    "sum_s Delta_(pivot,s)*T_s"
                ),
            })
    return tails, unary, responses, koszul


def audit_endpoint_typing():
    selected = {
        "p1": (0, 1), "s1": (1, 1),
        "p2": (3, 2), "s2": (4, 2),
    }
    records = []
    for matching in ANCHOR_COMPETITORS:
        partner, tail = partner_and_tail(matching)
        required = {
            "G11": (f"p1@{partner}:{Z[partner]}", "s1@1:1"),
            "G21": (f"p2@{partner}:{Z[partner]}", "s1@1:1"),
        }
        records.append({
            "matching": matching,
            "partner": partner,
            "common_q_tail": tail,
            "required_selected_s1_port": "s1@1:1",
            "required_word_changed_p_ports": required,
        })
    require(all(record["required_selected_s1_port"] == "s1@1:1"
                for record in records),
            "the six classes stopped sharing the selected s1 port")
    require(selected["p1"] != (0, Z[0])
            and selected["p2"] != (3, Z[3]),
            "a fixed selected p port acquired the z word")
    return {
        "fixed_selected_ports": selected,
        "records": records,
        "required_p1_components": tuple(
            f"p1@{partner}:{Z[partner]}" for partner in PARTNERS
        ),
        "required_p2_components": tuple(
            f"p2@{partner}:{Z[partner]}" for partner in PARTNERS
        ),
        "selected_response_access_at_z": 0,
    }


def audit_separator(tails, unary, responses):
    # Associated grade: retain the unary six-class tails and fixed selected
    # endpoint block, but no word-changed p entry.  Both response slices
    # vanish identically while the unary polynomial remains a nonzero sum
    # of six distinct monomials.  The primitive functional on the row-label
    # module which reads H and kills R1,R2 is therefore a separator.
    zero_substitution = {
        f"p{colour}_{partner}_{Z[partner]}"
        for colour in (1, 2) for partner in PARTNERS
    }

    def substitute_zero(value):
        return Counter({monomial: coefficient
                        for monomial, coefficient in value.items()
                        if not (set(monomial) & zero_substitution)})

    require(all(not substitute_zero(value)
                for value in responses.values()),
            "a response slice survived after removing word-changed ports")
    require(substitute_zero(unary) == unary and len(unary) == 6,
            "the unary six-class failed to survive the separator grade")
    require({partner: len(value) for partner, value in tails.items()}
            == {0: 1, 3: 2, 4: 2, 5: 1},
            "the separator tail dimensions changed")
    return {
        "associated_grade": (
            "all p_i@r:z_r entries for r=0,3,4,5 are absent; the selected "
            "s1@1:1 port and six unary matching monomials are retained"
        ),
        "row_label_functional": {"H_z_anchor": 1,
                                  "G11_z_selected_s1_slice": 0,
                                  "G21_z_selected_s1_slice": 0},
        "primitive": True,
        "consequence": (
            "unary top plus the fixed selected response ports cannot force "
            "spoke-to-hole synchronization.  A positive proof must add a "
            "word-changed p component, an endpoint mate at another s hole, "
            "or a cross-word/Hessian boundary"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    groups, routing, partner_two = audit_six_classes()
    tails, unary, responses, koszul = audit_common_tail_rows(groups)
    ledger = {
        "word": "".join(map(str, Z)),
        "six_anchor_competitors": ANCHOR_COMPETITORS,
        "site1_partner_profile": {
            str(partner): len(groups[partner]) for partner in PARTNERS
        },
        "other_unary_competitors": {
            "external_in_partner_classes": routing,
            "external_with_partner_2": partner_two,
            "total_external": 7,
        },
        "endpoint_typing": audit_endpoint_typing(),
        "common_tail_rows": {
            "unary": "H=sum_r q_1r^(1,z_r) T_r",
            "G11_selected_s1_slice": "R1=sum_r p1_r^(z_r) T_r",
            "G21_selected_s1_slice": "R2=sum_r p2_r^(z_r) T_r",
            "tail_term_profile": {
                str(partner): len(tails[partner]) for partner in PARTNERS
            },
        },
        "koszul_identities": koszul,
        "first_separator": audit_separator(tails, unary, responses),
        "theorem": (
            "the six canonical C6 z competitors form four literal common-"
            "tail classes behind the selected s1@1 port.  Their source-"
            "valid q/p Koszul identities expose the exact candidate minors. "
            "If every required word-changed p entry is absent, a primitive "
            "associated-grade functional separates the unary class from "
            "both selected-port response slices"
        ),
        "scope": (
            "exact first endpoint-word boundary, not a full-source point or "
            "a proof that arbitrary endpoint mates cannot synchronize the "
            "class.  Complete response terms using another s hole and "
            "cross-word/Hessian relations are precisely the omitted source "
            "attachments"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"C6 spoke/hole ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 C6 z spoke-to-hole Koszul boundary: PASS")
    print("six anchor mates -> site1 partner profile 1/2/2/1")
    print("seven other unary competitors -> offanchor route")
    print("eight exact q/p common-tail Koszul identities")
    print("no word-changed p ports -> primitive unary/response separator")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
