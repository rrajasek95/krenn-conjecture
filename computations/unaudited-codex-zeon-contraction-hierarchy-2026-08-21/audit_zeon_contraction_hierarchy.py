#!/usr/bin/env python3
"""Exact matching-partition audit of the n=8 zeon contraction hierarchy."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_zeon_contraction_hierarchy.json"
TAIL = (ROOT / "computations/unaudited-codex-tail-polar-source-lift-2026-08-21"
        / "results_tail_polar_source_lift.json")
REMOTE = (ROOT / "computations/unaudited-codex-tail-remote-hafnian-contraction-2026-08-21"
          / "results_tail_remote_hafnian_contraction.json")
BLOCKED = ROOT / "notes/target-blocked-site-polar-descent.md"
H3 = ROOT / "notes/h3-hamming-one-normal-incidence-compound-transgression.md"
PURE_SLICE = ROOT / "notes/full-nine-pure-slice-channel-routing.md"
DET_SPLIT = ROOT / "notes/determinant-split-route.md"
PINS = {
    str(TAIL.relative_to(ROOT)):
        "b97ef0b72d6e87ed3f1ffc61de4b5e237a71423fa31f47afd79b2e4ee64abbef",
    str(REMOTE.relative_to(ROOT)):
        "37497e633fc5c1b27dbea000b28fa04973b8da7f42294d3049cd73c9e0fc749b",
    str(BLOCKED.relative_to(ROOT)):
        "a2f380488ac51a47fc9441e35e520cec2ffeb361294297881128db95de55db07",
    str(H3.relative_to(ROOT)):
        "430e239756a058f9030795e0a685f5dfdf0b1817ea2eaedbc0b0f7750e9e67cd",
    str(PURE_SLICE.relative_to(ROOT)):
        "d9f4fadc89f80a2abeef5c1a7575d9eacbfe04b5a472c510c34d3d9214668a99",
    str(DET_SPLIT.relative_to(ROOT)):
        "9e461f309e5f6130a598e499dbe68cd840482f273ff0970440d926f558cc2954",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, partner),) + tail))


SITES = tuple(range(8))
MATCHINGS = tuple(perfect_matchings(SITES))


def contraction_partition(contracted):
    contracted = frozenset(contracted)
    records = []
    for matching in MATCHINGS:
        internal = tuple(edge for edge in matching if set(edge) <= contracted)
        crossing = tuple(edge for edge in matching
                         if len(set(edge) & contracted) == 1)
        residual = tuple(edge for edge in matching if not (set(edge) & contracted))
        require(2 * len(internal) + len(crossing) == len(contracted),
                ("contracted incidence", contracted, matching))
        records.append((len(internal), len(crossing), len(residual)))
    return Counter(records)


def label_bijection(contracted):
    contracted = tuple(contracted)
    residual = tuple(site for site in SITES if site not in contracted)
    labels = []
    for head in product(range(3), repeat=len(contracted)):
        for tail in product(range(3), repeat=len(residual)):
            word = [None] * 8
            for site, color in zip(contracted, head):
                word[site] = color
            for site, color in zip(residual, tail):
                word[site] = color
            labels.append("F_" + "".join(map(str, word)))
    require(len(labels) == 3**8 and len(set(labels)) == 3**8,
            ("contraction coordinate bijection", contracted))
    mixed = [label for label in labels if len(set(label[2:])) > 1]
    require(len(mixed) == 6558, ("mixed contraction count", contracted))
    return {
        "contracted_sites": list(contracted),
        "head_dimension": 3**len(contracted),
        "residual_dimension": 3**len(residual),
        "total_rank": len(labels),
        "mixed_rank": len(mixed),
        "label_sha256": sha256("\n".join(labels).encode()).hexdigest(),
    }


def offcount_census():
    counts = Counter()
    for word in product(range(3), repeat=8):
        counts[8 - max(word.count(color) for color in range(3))] += 1
    require(counts == Counter({4: 3150, 5: 1680, 3: 1344,
                               2: 336, 1: 48, 0: 3}), counts)
    return dict(sorted(counts.items()))


def invisible_chord_lower_powers():
    base = frozenset(((0, 1), (2, 3), (4, 5), (6, 7)))
    chorded = base | {(0, 2)}

    def supported(graph, size):
        supports = []
        for vertices in combinations(SITES, 2 * size):
            for matching in perfect_matchings(vertices):
                matching = frozenset(matching)
                if matching <= graph:
                    supports.append(tuple(sorted(matching)))
        return tuple(sorted(set(supports)))

    powers = {}
    for size in (1, 2, 3, 4):
        left = supported(base, size)
        right = supported(chorded, size)
        powers[str(size)] = {
            "base_support_count": len(left),
            "chorded_support_count": len(right),
            "new_support_count": len(set(right) - set(left)),
        }
        if size < 4:
            require(set(right) != set(left), ("lower power failed to change", size))
        else:
            require(left == right == (tuple(sorted(base)),),
                    "top power changed under invisible chord")
    require(tuple(sorted(((0, 2), (4, 5), (6, 7)))) in
            set(supported(chorded, 3)), "explicit q^3 chord term missing")
    return {
        "base": [list(edge) for edge in sorted(base)],
        "added_chord": [0, 2],
        "power_supports": powers,
        "same_top": "q_base^[4]=q_chorded^[4]=e_0^tensor8",
        "different_q3_term": "02|45|67",
    }


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    for relative, expected in PINS.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, (relative, observed, expected))
    require(len(MATCHINGS) == 105, "K8 matching count changed")

    partitions = {
        "one_site": {str(key): value for key, value in
                     sorted(contraction_partition((0,)).items())},
        "two_sites": {str(key): value for key, value in
                      sorted(contraction_partition((0, 1)).items())},
        "three_sites": {str(key): value for key, value in
                        sorted(contraction_partition((0, 1, 2)).items())},
    }
    require(partitions == {
        "one_site": {"(0, 1, 3)": 105},
        "two_sites": {"(0, 2, 2)": 90, "(1, 0, 3)": 15},
        "three_sites": {"(0, 3, 1)": 60, "(1, 1, 2)": 45},
    }, ("contraction matching partitions", partitions))

    bijections = [label_bijection((0,)), label_bijection((0, 1)),
                  label_bijection((0, 1, 2))]
    tail = json.loads(TAIL.read_text())
    profiles = Counter(row["profile"] for row in tail["row_ledger"])
    require(profiles == Counter({"3+3+2": 360, "6+1+1": 12, "7+1": 8}),
            ("frozen 380 row profile", profiles))
    remote = json.loads(REMOTE.read_text())
    require(remote["exact_nonzero_partial_remote_point"]["332_nonzero_count"] == 138,
            "remote omitted-row control changed")

    payload = {
        "status": "PASS exact zeon contraction hierarchy audit",
        "site_down_operator": {
            "definition": (
                "D_(i,c) contracts the V_i factor of the canonical site-graded "
                "component with e_c^*. Operators at distinct sites commute. "
                "No derivation on the square-zero quotient is asserted."
            ),
            "target": (
                "D_(U,c_U) Delta = product_(w notin U)x_(w,c) if all "
                "c_U=c, and zero otherwise"
            ),
        },
        "divided_power_identities": {
            "one_site": (
                "For W=B-{p}, q=Q|_W, l_(p,c)=sum_(j in W)A_pj[c,-]: "
                "D_(p,c)Q^[4]=l_(p,c)q^[3]=X_(W,c)."
            ),
            "two_sites": (
                "For W=B-{p,r}, q=Q|_W, endpoint stars p_c,s_d and "
                "a_cd=A_pr[c,d]: D_(p,c)D_(r,d)Q^[4]="
                "a_cd q^[3]+p_c s_d q^[2]=delta_cd X_(W,c)."
            ),
            "three_sites": (
                "For U={p,r,s}, W=B-U: D_(p,a)D_(r,b)D_(s,c)Q^[4]="
                "(a_pr[ab]l_s,c+a_ps[ac]l_r,b+a_rs[bc]l_p,a)q^[2] + "
                "l_p,a l_r,b l_s,c q = delta_(a=b=c)X_(W,a)."
            ),
            "matching_partition_counts": partitions,
        },
        "carrier_identification": {
            "cap_contraction": (
                "Summing the two-site identity against K gives "
                "s_K q^[3]+r_K q^[2]=T_K, with s_K=<K,A_pr>, "
                "r_K=sum_cd K_cd p_c s_d, T_K=sum_c K_cc X_c."
            ),
            "literal_response_edge": (
                "(r_K)_uv[alpha,beta]=sum_cd K_cd("
                "A_pu[c,alpha]A_rv[d,beta]+"
                "A_pv[c,beta]A_ru[d,alpha]), exactly the frozen carrier row."
            ),
            "X5_scope": (
                "At a fixed pair, the 9*3^6 coordinates are the original "
                "6561 word rows; their 6558 mixed coordinates are exactly X5."
            ),
            "frozen_tail_subset": dict(profiles),
        },
        "module_rank_theorem": {
            "fixed_contraction_coordinate_bijections": bijections,
            "statement": (
                "For every fixed nonempty U, D_U with its V_U colour output "
                "is the canonical reassociation B_8=(tensor_U V_i) tensor "
                "B_(8-|U|), hence rank 6561. Restricted to mixed target "
                "coordinates it has rank 6558."
            ),
            "ideal_consequence": (
                "The coordinate equations at any one fixed site, pair, or "
                "triple are a permutation/rebracketing of F_w-delta_w. "
                "They generate exactly the original normalized source ideal, "
                "not a smaller contraction ideal. Third contractions are "
                "literal site-downs of the pair/carrier identity."
            ),
        },
        "archive_crosswalk": {
            "full_nine_pure_slice": (
                "The equation M_d=E_dd-F_d*a is the constant residual-word "
                "coordinate of the two-site identity. Its channel-routing "
                "lemma is therefore a scalar projection of the same pair layer."
            ),
            "target_blocked_descent": (
                "The cap equation beta*q^[2]=sum lambda_c X_c is a selected "
                "pair/carrier projection. Its one-site polar and two-site dark "
                "quotient are literal contractions/quotients of that projection; "
                "they add incidence hypotheses, not new source rows."
            ),
            "determinant_3_plus_3": (
                "The six-site 3+3 formula has the same triple-site matching "
                "partition: 6 all-cross bijections plus 9 internal-left / "
                "internal-right / cross placements. It is the three-site "
                "contraction of a standalone six-site top equation (or a branch "
                "where such an equation has first been isolated), not an "
                "additional consequence of the n=8 top rows."
            ),
            "h3_compound": (
                "The marked scalar nu_x=rho_x(beta_x) in [X_c]R^[2]q is "
                "second order in the response R. Ordinary Hamming-one data are "
                "only Gamma_x=rho_x o iota_x^q. Reinjecting beta_x is nonlinear "
                "response data and is not another literal D_U coordinate."
            ),
            "genuinely_missing_layer": (
                "No higher literal site-down layer is missing: |U|>=4 still "
                "relabels the same top tensor. The first genuinely missing "
                "operation is response-dependent normal reinsertion, together "
                "with the archived cancellation equation alpha*sum_x nu_x="
                "-24*(u^{3})^T J3*v^{3}; it is not a new linear "
                "source module."
            ),
        },
        "sharp_counterexamples": {
            "top_does_not_determine_lower_powers": invisible_chord_lower_powers(),
            "proper_row_subset": (
                "The frozen remote point satisfies pure normalization, all "
                "12 selected 611 rows and all 8 selected 71 rows, but fails "
                "138 of the 360 332 rows. Thus the smaller linear-tail "
                "contraction packet is strictly weaker than the full layer."
            ),
        },
        "offcount_census": offcount_census(),
        "terminal_verdict": (
            "The third site-down layer is source-faithful but not new: with "
            "all colours retained it is an invertible regrouping of the 6558 "
            "mixed rows and a contraction of the existing carrier identity. "
            "Discarding coordinates can make it smaller only by losing "
            "information, as the remote point shows. A new cap criterion "
            "must add a nonlinear condition on the actual lower powers or "
            "carrier support; it cannot follow from the contraction hierarchy alone."
        ),
        "input_hashes": PINS,
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("zeon contraction hierarchy: PASS")
    print("matching partitions:", partitions)
    print("fixed U ranks total/mixed: 6561/6558 for |U|=1,2,3")
    print("frozen tail profiles:", dict(profiles))
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
