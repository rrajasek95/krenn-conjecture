#!/usr/bin/env python3
"""Audit the physical scope of the full-S8 H2 tag contraction.

The coefficient calculation of df8c061 is correct: d,p_i,s_i,q_ij are the
edges PS,Pi,Si,ij of K8 and the response polynomial is S8-covariant.  But a
transposition exchanging P with a residual site is a morphism between two
response-chart objects.  It is not a relative boundary in one fixed pointed
source presentation.

For the representative four-set {P,S,0,1}, the swap P<->0 exchanges

    A=D*q01  <->  C=p1*s0,     B=p0*s1 fixed.

It therefore kills the coefficient tag v=2A-B-C after raw chart folding.
Canonical retained-chart transport sends the moved endpoint back and gives
zero boundary instead.  Raw folding adds the two relations A=B=C and lowers
fixed-source H0.  The presentation-preserving cone retains graph coordinates;
on v its first proper face is exactly

    L01=(2Dq01-p0s1-p1s0)*(q23q45+q24q35+q25q34),

the target-zero centered scalar isolated in 0d14815.  Thus df8c061 removes
the tag only conditional on a pointed endpoint-chart PP comparison carrying
L01 with its word/fine/direction grade.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_h2_full_site_groupoid_tag_contraction.py":
        "eb2acb53ca9364ff4639985996f75321800d74b798858cda04084e997a15aa23",
    "notes/h3-h2-full-site-groupoid-tag-contraction.md":
        "47394c03902597892a2a4c01bc488dfc34f782e635e822e946304e1d5686faf1",
    "computations/verify_h3_h2_direction_tag_maschke_c4_coinvariant_gate.py":
        "bee87b90c32720583f50d1c65dc2280dd337a46d197932d8c22aab802362d9ff",
    "notes/h3-h2-direction-tag-maschke-c4-coinvariant-gate.md":
        "f61147619b6758924c700fd3a4d99a1edb398ed9abc23f417fdf745209055d29",
    "computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py":
        "47378f8ce904021bb802e0e4fd59de1591f0cd7333e1fcbc645e62cf40deb499",
    "notes/h3-h2-c4-trivial-tag-euler-scalar-face-gate.md":
        "3d16b7a1b77030eaaa5ba3fc342b927a7ee750db2c4f8091868591acc261477f",
    "computations/verify_h3_centered_occurrence_endpoint_matching_maschke_pointed_gate.py":
        "1994697181c6034267d98a26a28ab4c69c3fcb979b657c8d7d06fc81b86650ed",
    "notes/h3-centered-occurrence-endpoint-matching-maschke-pointed-gate.md":
        "c56f3d4dd1f04f34e5a6c88f077820cf118eea5de31affc8f4196e4bd78fe75c",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
}
EXPECTED_LEDGER_SHA256 = (
    "88738bb4d854b9e862dbc4b9d6acd217fadc815aad874c873adf0795c5d4e596"
)
P_SITE = 6
S_SITE = 7
SITES = tuple(range(8))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def variable_edge(variable) -> frozenset[int]:
    kind = variable[0]
    if kind == "q":
        return frozenset((variable[1], variable[2]))
    if kind == "p":
        return frozenset((variable[1], P_SITE))
    if kind == "s":
        return frozenset((variable[1], S_SITE))
    require(kind == "d", variable)
    return frozenset((P_SITE, S_SITE))


def edge_variable(edge: frozenset[int]):
    left, right = sorted(edge)
    if (left, right) == (P_SITE, S_SITE):
        return ("d",)
    if right == P_SITE:
        return ("p", left)
    if right == S_SITE:
        return ("s", left)
    return ("q", left, right)


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
            yield tuple(sorted((tuple(sorted((first, second))),) + tail))


def act_variable(variable, permutation):
    edge = frozenset(permutation[site] for site in variable_edge(variable))
    return edge_variable(edge)


def act_monomial(monomial, permutation):
    return tuple(sorted(act_variable(variable, permutation)
                        for variable in monomial))


def act_word(word, permutation):
    answer = [None] * len(word)
    for site, colour in enumerate(word):
        answer[permutation[site]] = colour
    return tuple(answer)


def rank(rows) -> int:
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot = 0
    for column in range(len(work[0])):
        selected = next((row for row in range(pivot, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        value = work[pivot][column]
        work[pivot] = [entry / value for entry in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right
                         in zip(work[row], work[pivot], strict=True)]
        pivot += 1
    return pivot


def decorated_direction(pair, word):
    answer = []
    for variable in sorted(pair):
        left, right = sorted(variable_edge(variable))
        answer.append((variable[0], left, right, word[left], word[right]))
    return tuple(answer)


def coefficient_and_chart_audit(classification, scalar_gate):
    _target, response_terms = classification.source_monomials()
    edge_matchings = {
        tuple(sorted(tuple(sorted(variable_edge(variable)))
                     for variable in monomial))
        for monomial in response_terms
    }
    expected_matchings = set(perfect_matchings(SITES))
    require(edge_matchings == expected_matchings
            and len(edge_matchings) == 105,
            "the response stopped being the K8 hafnian")

    permutation = list(SITES)
    permutation[0], permutation[P_SITE] = P_SITE, 0
    permutation = tuple(permutation)
    require({act_monomial(monomial, permutation)
             for monomial in response_terms} == set(response_terms),
            "the endpoint-residual swap stopped preserving the response set")

    q = classification.q
    p = classification.p
    s = classification.s
    direct = classification.D
    a_pair = frozenset((direct, q(0, 1)))
    b_pair = frozenset((p(0), s(1)))
    c_pair = frozenset((p(1), s(0)))
    require(act_monomial(tuple(a_pair), permutation) == tuple(sorted(c_pair))
            and act_monomial(tuple(c_pair), permutation) == tuple(sorted(a_pair))
            and act_monomial(tuple(b_pair), permutation) == tuple(sorted(b_pair)),
            "the A/C chart bridge changed")

    # In local coordinates A,B,C the raw group action exchanges A,C.  A
    # second four-set transposition exchanges A,B.  These two raw relations
    # span the centered plane and kill v.  They also lower H0 after folding.
    response_row = (Q(1), Q(1), Q(1))
    relation_ab = (Q(-1), Q(1), Q(0))
    relation_ac = (Q(-1), Q(0), Q(1))
    invariant = (Q(2), Q(-1), Q(-1))
    require(rank((relation_ab, relation_ac)) == 2
            and tuple(-relation_ab[i] - relation_ac[i] for i in range(3))
                == invariant,
            "the local raw chart contraction changed")
    require(rank((response_row,)) == 1
            and rank((response_row, relation_ab, relation_ac)) == 3,
            "raw chart folding stopped lowering the fixed-source quotient")

    # The presentation-preserving graph cone adds two coordinates.  Its
    # quotient dimension is the original 3-1=2 rather than zero.
    graph_rows = (
        (Q(1), Q(1), Q(1), Q(0), Q(0)),
        (Q(-1), Q(1), Q(0), Q(-1), Q(0)),
        (Q(-1), Q(0), Q(1), Q(0), Q(-1)),
    )
    require(rank(graph_rows) == 3 and 5 - rank(graph_rows) == 2,
            "the minimal chart graph cone changed H0")

    # Retained-label transport applies the inverse chart identification at
    # the moved endpoint.  Since sigma is an involution, every moved tag
    # returns to itself, so its bar boundary is zero rather than e_C-e_A.
    require(all(act_monomial(act_monomial(tuple(pair), permutation),
                             permutation) == tuple(sorted(pair))
                for pair in (a_pair, b_pair, c_pair)),
            "retained chart transport stopped being identity")

    all_words = tuple(itertools.product(range(3), repeat=8))
    fixed_words = tuple(word for word in all_words
                        if act_word(word, permutation) == word)
    moved_words = tuple(word for word in all_words
                        if act_word(word, permutation) != word)
    require(len(fixed_words) == 3 ** 7
            and len(moved_words) == 2 * 3 ** 7,
            (len(fixed_words), len(moved_words)))
    require(all((len(set(word)) == 1)
                == (len(set(act_word(word, permutation))) == 1)
                for word in all_words),
            "the GHZ target coefficient changed under the site swap")

    witness_word = (0, 0, 0, 0, 0, 0, 1, 1)
    transported_word = act_word(witness_word, permutation)
    require(transported_word == (1, 0, 0, 0, 0, 0, 0, 1),
            transported_word)
    old_tag = decorated_direction(a_pair, witness_word)
    new_tag = decorated_direction(c_pair, transported_word)
    require(old_tag != new_tag, (old_tag, new_tag))
    fixed_word = (0,) * 8
    require(decorated_direction(a_pair, fixed_word)
            != decorated_direction(c_pair, fixed_word),
            "operation profile was forgotten even in a fixed word")

    # Pin the first proper face independently through the C4 Euler audit.
    scalar_ledger, scalar_digest = scalar_gate.audit()
    require(scalar_digest == scalar_gate.EXPECTED_LEDGER_SHA256,
            "the C4 scalar-face ledger changed")
    scalar = scalar_ledger["literal_product_rule"]
    require(scalar["scalar_face_occurrences"] == 9
            and scalar["target_augmentation"] == "0"
            and scalar["response_row_countermodel"]["response_value"] == "0"
            and scalar["response_row_countermodel"]["scalar_face_value"] == "3",
            "the endpoint-chart scalar proper face changed")

    return {
        "coefficient_action": {
            "response_is_K8_hafnian": True,
            "response_matchings": len(edge_matchings),
            "chart_bridge": "physical site transposition P<->0",
            "local_action": "A=Dq01 <-> C=p1s0; B=p0s1 fixed",
            "raw_relations_span_centered_plane": True,
            "C4_vector_in_raw_relations": "v=-(B-A)-(C-A)",
        },
        "fixed_pointed_source_guard": {
            "response_only_quotient_dimension": 3 - rank((response_row,)),
            "after_raw_chart_folding_dimension": (
                3 - rank((response_row, relation_ab, relation_ac))
            ),
            "presentation_preserving_graph_cone_dimension": (
                5 - rank(graph_rows)
            ),
            "retained_chart_bar_boundary": 0,
            "raw_folded_bar_boundary": "e_(sigma tag)-e_tag",
            "conclusion": (
                "the site swap is an isomorphism between chart objects, not "
                "a nullhomotopy in one fixed pointed source presentation"
            ),
        },
        "word_fine_repeated_rows": {
            "all_words": len(all_words),
            "word_fixed_by_P0_swap": len(fixed_words),
            "word_changed_by_P0_swap": len(moved_words),
            "witness_word": "00000011",
            "transported_witness_word": "10000001",
            "witness_direction_before": repr(old_tag),
            "witness_direction_after": repr(new_tag),
            "even_when_word_fixed": (
                "Hasse order and squarefree four-set are preserved, but the "
                "literal direction grade DQ changes to PS"
            ),
            "complementary_tail_2345": "fixed by this representative swap",
            "physical_comparison_needed": (
                "a word/fine/direction-labelled endpoint-chart PP cylinder; "
                "coefficient relabelling alone is not that cylinder"
            ),
        },
        "target_and_first_proper_face": {
            "GHZ_target_site_permutation_invariant": True,
            "target_defect": 0,
            "first_nonzero_proper_face": scalar["scalar_zero_face"],
            "proper_face_occurrence_support": scalar["scalar_face_occurrences"],
            "proper_face_target_augmentation": scalar["target_augmentation"],
            "response_row_countermodel": scalar["response_row_countermodel"],
            "pointed_cone_boundary": "d epsilon_01=L01-u_01",
        },
    }


def terminal_scope_audit() -> dict[str, object]:
    terminal = load(
        "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py",
        "h2_full_site_chart_terminal",
    )
    ledger, digest = terminal.audit()
    require(digest == terminal.EXPECTED_LEDGER_SHA256,
            "the terminal-promotion ledger changed")
    fork = ledger["post_placement_dichotomy"]
    require(fork["third_branch"] is False,
            "the terminal promotion acquired a third branch")
    return {
        "same_grade_placement_needed_first": True,
        "then_extended_rows": "q/ainc/target/W/ores/ridge",
        "post_placement_alternative": fork["exact_alternative"],
        "third_branch": fork["third_branch"],
        "untyped_before_chart_cylinder": ["anchor", "physical q", "ridge", "eta/sigma"],
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    classification = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "h2_full_site_chart_classification",
    )
    scalar_gate = load(
        "computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py",
        "h2_full_site_chart_scalar",
    )
    full_s8 = load(
        "computations/verify_h3_h2_full_site_groupoid_tag_contraction.py",
        "h2_full_site_rank",
    )
    full_ledger, full_digest = full_s8.audit()
    require(full_digest == full_s8.EXPECTED_LEDGER_SHA256
            and set(full_ledger["full_S8_action_rank"].values()) == {140},
            "the coefficient full-S8 theorem changed")
    ledger = {
        "theorem": "h3 full-site H2 chart-swap pointed scalar guard",
        "pins": PINS,
        "pinned_full_S8_ledger": full_digest,
        "literal_audit": coefficient_and_chart_audit(classification, scalar_gate),
        "augmented_promotion_scope": terminal_scope_audit(),
        "answer": (
            "df8c061 is exact as a coefficient/groupoid rank theorem.  The "
            "endpoint-residual swap is a target-safe source algebra "
            "isomorphism between response charts, but raw folding is not a "
            "boundary in the fixed pointed source.  Its first proper face is "
            "the nine-term target-zero centered scalar L01 from 0d14815.  A "
            "physical endpoint-chart PP cylinder carrying L01 is precisely "
            "the remaining datum; after it is placed, 4373ae6 gives filler "
            "or augmented terminal."
        ),
        "scope": (
            "exact canonical h=3 uncoloured response algebra, all ternary "
            "word transports, and conditional augmented promotion.  It does "
            "not construct the pointed endpoint-chart cylinder."
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("full-S8 coefficient contraction: EXACT")
    print("P<->0: source chart isomorphism, not fixed-pointed boundary")
    print("word fixed/changed: 2187/4374; target defect 0")
    print("first proper face: nine-term centered scalar L01")
    print("after same-grade chart cylinder: FILLER OR TERMINAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
