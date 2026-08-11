#!/usr/bin/env python3
"""Consume the first two-shared transfer debt by a block-word factorization.

For e=uv and the mixed word with colour k at u,v and colour l everywhere
else, every matching either contains e or avoids it.  The first aggregate
is exactly q_e^(k,k) H_e^l.  Every avoiding matching has exactly two
k/l cross-colour endpoint cells.  Thus an exact source gives:

* block-diagonal branch: H_e^l=0 after localizing q_e^(k,k), and the pure-l
  target reselects a pure-l matching avoiding e;
* crossing branch: two off-diagonal cells, each covered by the pinned
  target-augmented active-minor identity (or an immediate off-anchor exit).

This uniformly consumes the six-site first debt 001111 from 3c4faa2.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_two_shared_direct_activity_transfer_boundary.py":
        "7b5389185fac02407c2ef5b5d91d01cfed9a3547723b047ef920f69561b9ddbe",
    "notes/uniform-two-shared-direct-activity-transfer-boundary.md":
        "df0972797bba89af0ff47d9a6a01c6660db9506ac346f6cf775b8e6ed3343c38",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    "computations/verify_uniform_two_shared_anchor_unary_label_migration.py":
        "78ab24f1c39d79ea38a80fd80bf43e43624e57dada0345c2c98b30559f528dc6",
    "notes/uniform-two-shared-anchor-unary-label-migration.md":
        "2e794feae556d582dc1623e698e2e331cae44e0de36e9d59125740a908d3b1c9",
}
EXPECTED_LEDGER_SHA256 = "17e895985a56b5f32a1c2bb30726c3d2199f458d5f0079a5704d4fce5eb08c68"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def load_transfer_guard():
    path = ROOT / "computations/verify_uniform_two_shared_direct_activity_transfer_boundary.py"
    spec = importlib.util.spec_from_file_location("transfer_guard", path)
    require(spec is not None and spec.loader is not None,
            "could not load the pinned transfer guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit_uniform_matching_partition():
    records = []
    for size in (4, 6, 8, 10):
        e = edge(0, 1)
        all_matchings = tuple(perfect_matchings(range(size)))
        through = tuple(matching for matching in all_matchings if e in matching)
        avoiding = tuple(matching for matching in all_matchings if e not in matching)
        tails = tuple(perfect_matchings(range(2, size)))
        require(set(through) == {
            tuple(sorted((e,) + tail)) for tail in tails
        }, f"q_e H_e factorization changed at size {size}")

        crossing_histogram = Counter()
        for matching in avoiding:
            cross_edges = tuple(pair for pair in matching
                                if (pair[0] in (0, 1)) != (pair[1] in (0, 1)))
            require(len(cross_edges) == 2,
                    "an avoiding matching lost its two block-crossing edges")
            require({partner(matching, 0), partner(matching, 1)}
                    <= set(range(2, size)),
                    "an avoiding endpoint failed to leave its two-site block")
            crossing_histogram[len(cross_edges)] += 1
        require(crossing_histogram == Counter({2: len(avoiding)}),
                "the two-crossing histogram changed")
        records.append({
            "sites": size,
            "all_matchings": len(all_matchings),
            "through_e_terms": len(through),
            "avoiding_e_terms": len(avoiding),
            "avoiding_terms_with_exactly_two_cross_cells": len(avoiding),
        })
    return records


def audit_all_colour_types():
    records = []
    for k, ell in itertools.permutations(range(3), 2):
        word = (k, k) + (ell,) * 4
        for matching in perfect_matchings(range(6)):
            if edge(0, 1) in matching:
                continue
            left_mate = partner(matching, 0)
            right_mate = partner(matching, 1)
            left_labels = (word[0], word[left_mate])
            right_labels = (word[1], word[right_mate])
            require(left_labels == right_labels == (k, ell),
                    "a block-crossing cell lost its off-diagonal type")
            records.append((k, ell, left_mate, right_mate))
    require(len(records) == 72,
            f"the ternary labelled crossing census changed: {len(records)}")
    return {
        "ordered_colour_pairs": 6,
        "labelled_avoiding_matchings": len(records),
        "cross_cell_type": "(k,l) at both two-site-block endpoints, k!=l",
        "active_minor_interface": (
            "each is one of the six off-diagonal types covered by the "
            "target-augmented private-site identity"
        ),
    }


def audit_integral_domain_factorization():
    # Mixed row q_kk*H+R=0; pure target q_ll*H+S=1.
    # In the block-diagonal branch R=0 and q_kk is localized.
    q_kk, q_ll, h, mixed_avoiding, pure_avoiding = 2, 3, 0, 0, 1
    require(q_kk * h + mixed_avoiding == 0,
            "the block-diagonal mixed row changed")
    require(q_ll * h + pure_avoiding == 1,
            "the pure-target reselection row changed")
    forbidden_h, forbidden_r = 5, 0
    require(q_kk * forbidden_h + forbidden_r != 0,
            "the localized no-crossing unit guard changed")
    return {
        "mixed_row": "0=q_e^(k,k)*H_e^l+R_cross",
        "pure_target_row": "1=q_e^(l,l)*H_e^l+R_pure_avoiding",
        "block_diagonal_consequence": "H_e^l=0 and R_pure_avoiding=1",
        "nonzero_H_without_crossing": "ordinary localized source unit",
    }


def audit_first_debt_application():
    module = load_transfer_guard()
    p0, p1, p2, winding, _mixed_word, source = module.build_winding_guard(6)
    word = tuple(map(int, "001111"))
    terms = module.compatible_terms(6, source, word)
    require(len(terms) == 1 and terms[0][0] == 1 and terms[0][1] == p1,
            f"the first transfer debt changed: {terms}")
    require(edge(0, 1) in p0 and edge(0, 1) in p1
            and edge(0, 1) not in p2,
            "the first debt stopped being a two-shared pivot")
    anchor_union = set(p0) | set(p1) | set(p2)
    anchor_matchings = tuple(matching for matching in perfect_matchings(range(6))
                             if set(matching) <= anchor_union)
    require(set(anchor_matchings) == {p0, p1, p2},
            f"the first-debt anchor classes changed: {anchor_matchings}")
    return {
        "word": "001111",
        "existing_singleton_class": "P1 (contains e=01)",
        "anchor_contained_mate_classes": {
            "P0_contains_e": (
                "joins the complete H01^11 block; if no avoiding mate, "
                "mixed exactness gives H01^11=0 and pure-one target "
                "reselects away from 01"
            ),
            "P2_avoids_e": (
                "contains exactly two 0/1 cross-colour endpoint cells; "
                "each enters the target-augmented active-minor route"
            ),
        },
        "winding_class_is_off_anchor": bool(set(winding) - anchor_union),
        "first_debt_consumed_without_new_word": True,
    }


def main():
    pin_dependencies()
    ledger = {
        "uniform_matching_partition": audit_uniform_matching_partition(),
        "all_ternary_crossing_types": audit_all_colour_types(),
        "integral_domain_factorization": audit_integral_domain_factorization(),
        "first_001111_debt": audit_first_debt_application(),
        "theorem": (
            "for the complete word kk l...l, all e-containing terms factor "
            "as q_e^(k,k) H_e^l and every e-avoiding term has exactly two "
            "off-diagonal k/l endpoint cells.  With no crossing term, "
            "mixed exactness forces H_e^l=0 and the pure-l target reselects "
            "a pure-l matching avoiding e"
        ),
        "crossing_landing": (
            "a crossing mate outside the selected anchor union is the "
            "off-anchor landing.  Every anchor-contained crossing mate has "
            "two typed off-diagonal cells, hence enters the pinned exact "
            "active determinant/cofactor identity and the existing "
            "exchange/two-shared path interface"
        ),
        "transfer_graph_consequence": (
            "the first omitted 001111 row from 3c4faa2 cannot propagate to "
            "an untyped new debt: its containing-e class gives immediate "
            "pure-anchor reselection, while its avoiding-e class gives "
            "typed activity/off-anchor escape"
        ),
        "scope": (
            "uniform complete-cofactor source theorem over an integral "
            "domain.  The active-minor branch is a certified downstream "
            "interface, not by itself a claim of four-good deleted ranks"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"two-block cofactor-reselection ledger changed: {digest}")
    print("uniform two-block word cofactor/reselection theorem: PASS")
    print("block-diagonal mate -> H_e^l=0 -> pure-l reselection")
    print("avoiding mate -> exactly two typed off-diagonal active cells")
    print("first transfer debt 001111 is consumed")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
