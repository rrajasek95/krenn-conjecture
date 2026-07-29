#!/usr/bin/env python3
"""Audit the B=0 anchor filter on the equality-five witness boundary.

The underlying exact incidence, hard-capacity, two-hole, and free-plane
filters live in ``verify_n8_witness_union_five_stages.py``.  This checker
intersects their residual hard assignments with the additional live-branch
condition: three triple-zero sites are hard in three distinct colours.
"""

import importlib.util
from pathlib import Path


def load_five_stage_audit():
    path = Path(__file__).with_name("verify_n8_witness_union_five_stages.py")
    spec = importlib.util.spec_from_file_location("five_stage_audit", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    audit = load_five_stage_audit()
    expected = {
        (0, 1, 6, 7, 7, 7): 6,
        (0, 3, 5, 7, 7, 7): 6,
        (0, 3, 7, 7, 7, 7): 12,
    }

    survivors = {}
    for masks in audit.EXPECTED_RESIDUAL:
        retained = []
        for hard in audit.hard_assignments(masks):
            if audit.rank_two_certificate(masks, hard):
                continue
            if audit.free_plane_monomial_certificate(masks, hard):
                continue
            triple_hard_colours = {
                hard_mask
                for witness_mask, hard_mask in zip(masks, hard, strict=True)
                if witness_mask == 7 and hard_mask in (1, 2, 4)
            }
            if triple_hard_colours == {1, 2, 4}:
                retained.append(hard)
        if retained:
            survivors[masks] = len(retained)

    assert survivors == expected
    print("live B=0 equality-five survivor audit: PASS")


if __name__ == "__main__":
    main()
