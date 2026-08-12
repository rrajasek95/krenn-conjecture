#!/usr/bin/env python3
"""Close the nonzero P2:21 branch by its first private coefficient.

The L-pair affine boundary has residual word 001122 and L ports P2,S3.
Adjoining P2:21 supplies both crossed rows R21 and R22.  Before a five-lock
argument is needed, however, the pure-one private word 11111121 contains
the selected L monomial.  At exact carrier support it is the unique term.

Every possible cancellation mate either has an off-anchor P:21 edge, or
uses P0/P2.  In the latter case replacing P:21 by the already selected
P:11 cell gives a nonzero pure-one target matching different from L; it
omits one of the two L-only edges carrying the old 02 cells.  Reselecting
that matching therefore makes an old off-diagonal cell nonanchor.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_l_pair_affine_response_obstruction.py":
        "8d566f61acfcec9c83410986de52cff0021fb1a9a7048c22a40c118bb706aace",
    "notes/h3-axis-target-coloop-l-pair-affine-response-obstruction.md":
        "ed536b301c8938fb036159ee0258aa27cc5231775ea72ea317fbc7f604825b60",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "9223046b5bf36dcb3635350fbfbc6fec5e0af85f66f812fd8050eb789ee608d9"
)

P, S = 6, 7
PURE_ONE = (1,) * 8
PRIVATE_WORD = (1,) * 6 + (2, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decorated_cell(edge, word):
    return edge, (word[edge[0]], word[edge[1]])


def term_supported(matching, word, q_support, p_support, s_support):
    for edge in matching:
        if P in edge:
            site = edge[0] if edge[1] == P else edge[1]
            if (word[P], site, word[site]) not in p_support:
                return False
        elif S in edge:
            site = edge[0] if edge[1] == S else edge[1]
            if (word[S], site, word[site]) not in s_support:
                return False
        elif decorated_cell(edge, word) not in q_support:
            return False
    return True


def audit():
    affine = load(
        "computations/verify_h3_axis_target_coloop_l_pair_affine_response_obstruction.py",
        "l_pair_affine_dependency",
    )
    top = load(
        "computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py",
        "return_top_dependency",
    )
    four = load(
        "computations/verify_h3_axis_target_coloop_four_diagonal_switch_five_lock.py",
        "four_diagonal_dependency",
    )
    second = load(
        "computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py",
        "second_hybrid_dependency",
    )
    first = load(
        "computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py",
        "first_hybrid_dependency",
    )
    routing = load(
        "computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py",
        "routing_dependency",
    )

    records = affine.boundary_records(top, second, first, routing)
    all_matchings = tuple(routing.perfect_matchings(range(8)))
    bright = tuple(matching for matching in all_matchings
                   if routing.edge(P, S) not in matching)
    direct = tuple(matching for matching in all_matchings
                   if routing.edge(P, S) in matching)
    require(len(records) == 4 and len(all_matchings) == 105
            and len(bright) == 90 and len(direct) == 15,
            "the affine-record or direct-free matching count changed")

    private_routes = Counter()
    rainbow_rows = Counter()
    reselection_omissions = Counter()
    representative = None

    for residual, candidate in records:
        L, M, K = (residual[key] for key in ("L", "M", "K"))
        first_word, _sources, q_support = top.selected_q_support(
            second, residual, candidate
        )
        p_support, s_support = four.selected_endpoint_support(
            second, residual, candidate, first_word
        )
        p_support, s_support = set(p_support), set(s_support)

        # Literal notation is endpoint head first, then residual colour.
        missing = (2, 2, 1)  # P2:21
        require(missing not in p_support
                and (1, 2, 1) in p_support
                and (1, 0, 1) in p_support,
                "the missing/selected P-port types changed")
        p_support.add(missing)

        # The first target-augmented/private row is the pure-one response
        # with only P changed from head 1 to head 2.
        exact_private = tuple(
            matching for matching in bright
            if term_supported(matching, PRIVATE_WORD, q_support,
                              p_support, s_support)
        )
        require(exact_private == (L,),
                "11111121 stopped being private at exact carrier support")

        l_tail = tuple(edge for edge in L if P not in edge and S not in edge)
        require(len(l_tail) == 2
                and all(edge not in set(K) | set(M) for edge in l_tail),
                "the two old 02 cells stopped lying on L-only edges")

        for matching in bright:
            if matching == L:
                continue
            p_partner = routing.partner(matching, P)
            if p_partner not in (0, 2):
                # The hypothetical mate has literal P-w:21 on an edge
                # outside K union L union M.
                require(routing.edge(P, p_partner)
                        not in set(K) | set(L) | set(M),
                        "an external P:21 mate entered the anchor union")
                private_routes["external_P21_active_minor"] += 1
                continue

            # P0:11 and P2:11 are already selected.  Replacing the mate's
            # P-w:21 factor by P-w:11 preserves every other pure-one factor,
            # so the same physical matching is a nonzero pure-one target
            # monomial and may be reselected as L'.
            require((1, p_partner, 1) in p_support,
                    "an internal mate lost its selected pure-one P factor")
            omitted = tuple(edge for edge in l_tail if edge not in matching)
            require(omitted,
                    "an alternate pure-one matching retained both L-only edges")
            private_routes[
                "P2_same_port_reselection" if p_partner == 2
                else "P0_avoiding_reselection"
            ] += 1
            reselection_omissions[len(omitted)] += 1

        # The old rainbow 02 cells are now included.  P2:21 supplies both
        # R21 and R22 because sites 2 and 3 have residual colour 1.
        rainbow_q = set(q_support)
        for edge in l_tail:
            rainbow_q.add(decorated_cell(edge, affine.RAINBOW_WORD))
        row_data = {}
        for label, word in (
                ("R21", affine.RAINBOW_WORD + (2, 1)),
                ("R22", affine.RAINBOW_WORD + (2, 2))):
            supported = tuple(
                matching for matching in bright
                if term_supported(matching, word, rainbow_q,
                                  p_support, s_support)
            )
            require(supported == (L,),
                    f"{label} stopped being private at exact carrier support")
            p_cell = (word[P], 2, word[2])
            s_cell = (word[S], 3, word[3])
            require(p_cell == (2, 2, 1),
                    "the rainbow row mistyped P2:21")
            rainbow_rows[(label, p_cell, s_cell)] += 1
            row_data[label] = {
                "word": "".join(map(str, word)),
                "P_port": "P2:21",
                "S_port": f"S3:{word[S]}1",
                "exact_supported_matching": L,
            }

        if representative is None:
            representative = {
                "K": K,
                "L": L,
                "M": M,
                "private_word": "11111121",
                "private_selected_matching": L,
                "L_only_02_edges": l_tail,
                "rainbow_rows": row_data,
            }

    require(private_routes == Counter({
        "external_P21_active_minor": 240,
        "P0_avoiding_reselection": 60,
        "P2_same_port_reselection": 56,
    }), f"the private-mate route split changed: {private_routes}")
    require(sum(reselection_omissions.values()) == 116,
            "an internal private mate lost its anchor reselection")
    require(rainbow_rows == Counter({
        ("R21", (2, 2, 1), (1, 3, 1)): 4,
        ("R22", (2, 2, 1), (2, 3, 1)): 4,
    }), f"the R21/R22 port typing changed: {rainbow_rows}")

    ledger = {
        "records": len(records),
        "private_word": "11111121",
        "complete_matching_split": {
            "direct_PS21_terms_zero_in_normal_form": len(direct),
            "direct_free_terms": len(bright),
        },
        "private_exact_support": "one selected L monomial per record",
        "complete_private_alternate_routes": dict(sorted(private_routes.items())),
        "internal_reselection_omitted_L_only_edges": {
            str(key): value for key, value in sorted(reselection_omissions.items())
        },
        "rainbow_rows": [
            {
                "row": row,
                "P_port": "P2:21",
                "S_port": f"S3:{s_cell[0]}1",
                "records": count,
            }
            for (row, _p_cell, s_cell), count in sorted(rainbow_rows.items())
        ],
        "typing_correction": (
            "00112222 uses P2:21 and S3:21, not P2:22/S3:22, "
            "because residual sites 2 and 3 carry colour 1"
        ),
        "representative": representative,
        "conclusion": (
            "If P2:21 is nonzero, its first private row is a localized unit "
            "unless a cancellation mate is present. Every mate either is an "
            "off-anchor P:21 active-minor carrier or yields a nonzero "
            "alternate pure-one matching; reselection then makes one old "
            "L-only 02 cell nonanchor. P2:21 also supplies literal R21 and "
            "R22, but the branch exits before E2/common-covector/five-lock. "
            "Thus the sole surviving affine block has P2:21=0."
        ),
        "scope": (
            "this closes the nonzero P2:21 branch only; it does not derive "
            "P2:21 or close the original rank-one affine block where it is zero"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the frozen P2:21 private-row ledger changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("h3 target-coloop P2:21 private-row closure: PASS")


if __name__ == "__main__":
    main()
