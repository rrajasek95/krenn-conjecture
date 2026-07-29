#!/usr/bin/env python3
"""Exact audit of the current h=8, k=5 collision-census ledger."""

from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


H = 8
P = 13
K = P - H
TOTAL = P + H + 2


def profile(triples=0, doubles=0, singletons=None):
    if singletons is None:
        singletons = TOTAL - 3 * triples - 2 * doubles
    assert singletons >= 0
    answer = (3,) * triples + (2,) * doubles + (1,) * singletons
    assert sum(answer) == TOTAL
    return answer


# This is an independent compact specification of all 44 frozen residuals.
# For each triple count, list exactly the allowed double counts.
allowed_double_counts = {
    5: (4, 3, 2, 1, 0),
    4: (5, 4, 3, 2, 1, 0),
    3: (7, 6, 4, 3, 2, 1, 0),
    2: (8, 5, 4, 3, 2, 1, 0),
    1: (6, 5, 4, 3, 2, 1, 0),
}
expected_frozen = {(4, 4) + (3,) * 5}
for triple_count, double_counts in allowed_double_counts.items():
    expected_frozen.update(
        profile(triples=triple_count, doubles=double_count)
        for double_count in double_counts
    )
expected_frozen.update(profile(doubles=double_count) for double_count in range(1, 12))

historical_closed = {
    profile(doubles=11),  # 2^11 1
    profile(doubles=10),  # 2^10 1^3
    (4, 4) + (3,) * 5,  # 4^2 3^5
    profile(triples=5, doubles=4),  # 3^5 2^4
    profile(triples=4, doubles=5),  # 3^4 2^5 1
    profile(triples=5, doubles=3),  # 3^5 2^3 1^2
    profile(triples=4, doubles=4),  # 3^4 2^4 1^3
    profile(triples=3, doubles=4),  # 3^3 2^4 1^6
    profile(triples=4, doubles=1),  # 3^4 2 1^9
    profile(triples=3, doubles=7),  # 3^3 2^7
    profile(triples=5, doubles=2),  # 3^5 2^2 1^4
    profile(triples=5, doubles=1),  # 3^5 2 1^6
    profile(triples=5, doubles=0),  # 3^5 1^8
    profile(triples=4, doubles=3),  # 3^4 2^3 1^5
    profile(triples=4, doubles=2),  # 3^4 2^2 1^7
    profile(triples=4, doubles=0),  # 3^4 1^11
    profile(triples=3, doubles=6),  # 3^3 2^6 1^2
    profile(triples=3, doubles=3),  # 3^3 2^3 1^8
}

# The all-order d=0..3 selected-lift incidence increment, preserving the
# earlier 18 attributions above.
incidence_closed = {
    profile(triples=3, doubles=2),
    profile(triples=3, doubles=1),
    profile(triples=3, doubles=0),
    profile(triples=2, doubles=5),
    profile(triples=2, doubles=4),
    profile(triples=2, doubles=3),
    profile(triples=2, doubles=2),
    profile(triples=2, doubles=1),
    profile(triples=2, doubles=0),
    profile(triples=1, doubles=6),
    profile(triples=1, doubles=5),
    profile(triples=1, doubles=4),
    profile(triples=1, doubles=3),
    profile(triples=1, doubles=2),
    profile(triples=1, doubles=1),
    profile(triples=1, doubles=0),
    *(profile(doubles=double_count) for double_count in range(1, 10)),
}

# The all-order d=5 endpoint closes the last profile.
endpoint_closed = {profile(triples=2, doubles=8)}
closed = historical_closed | incidence_closed | endpoint_closed

counts, frozen_tuple = frontier.census(H, P)
frozen = set(frozen_tuple)
assert (H, P, K, TOTAL) == (8, 13, 5, 23)
assert counts == {
    "H": 637,
    "S": 501,
    "C": 30,
    "L": 23,
    "R": 44,
    "Q": 19,
    "D": 1,
}
assert frozen == expected_frozen
assert len(frozen) == 44

assert closed <= frozen
assert len(historical_closed) == 18
assert len(incidence_closed) == 25
assert len(endpoint_closed) == 1
assert historical_closed.isdisjoint(incidence_closed)
assert historical_closed.isdisjoint(endpoint_closed)
assert incidence_closed.isdisjoint(endpoint_closed)
assert len(closed) == 44
assert closed == frozen
open_profiles = frozen - closed
assert not open_profiles
assert profile(doubles=9) in incidence_closed  # formerly open 2^9 1^5

# The accepted proof artifacts and their exact audits must all exist.
accepted_artifacts = (
    HERE.parent / "notes/live-three-zero-eighth-split-k5-eleven-double-one-singleton-matching-closure.md",
    HERE / "verify_live_three_zero_eighth_split_k5_eleven_double_one_singleton_matching_closure.py",
    HERE.parent / "notes/live-three-zero-eighth-split-k5-ten-double-three-singleton-projective-matching-closure.md",
    HERE / "verify_live_three_zero_eighth_split_k5_ten_double_three_singleton_projective_matching_closure.py",
    HERE.parent / "notes/live-three-zero-eighth-split-all-order-formal-five-layer-duality.md",
    HERE / "verify_live_three_zero_eighth_split_all_order_formal_five_layer_duality.py",
    HERE.parent / "notes/live-three-zero-eighth-split-k5-formal-five-layer-increment.md",
    HERE / "verify_live_three_zero_eighth_split_k5_formal_five_layer_increment.py",
    HERE.parent / "notes/live-three-zero-eighth-split-k5-five-triple-saturated-cubic-robin-rectangle-closure.md",
    HERE / "verify_live_three_zero_eighth_split_k5_five_triple_saturated_cubic_robin_rectangle_closure.py",
    HERE.parent / "notes/live-three-zero-eighth-split-k5-mixed-linear-plane-increment.md",
    HERE / "verify_live_three_zero_eighth_split_k5_mixed_linear_plane_increment.py",
    HERE.parent / "notes/live-three-zero-eighth-split-k5-seven-double-formal-linear-plane-closure.md",
    HERE / "verify_live_three_zero_eighth_split_k5_seven_double_formal_linear_plane_closure.py",
    HERE.parent / "notes/live-three-zero-eighth-split-k5-unified-pair-drop-linear-plane-closure.md",
    HERE / "verify_live_three_zero_eighth_split_k5_unified_pair_drop_linear_plane_closure.py",
    HERE.parent / "notes/live-three-zero-eighth-split-k5-three-double-second-jet-closure.md",
    HERE / "verify_live_three_zero_eighth_split_k5_three_double_second_jet_closure.py",
    HERE.parent / "notes/live-three-zero-eighth-split-all-order-ten-singleton-incidence-closure.md",
    HERE / "verify_live_three_zero_eighth_split_all_order_ten_singleton_incidence_closure.py",
    HERE.parent / "notes/live-three-zero-eighth-split-all-order-low-mixed-role-incidence-closure.md",
    HERE / "verify_live_three_zero_eighth_split_all_order_low_mixed_role_incidence_closure.py",
    HERE.parent / "notes/live-three-zero-eighth-split-all-order-mixed-role-census.md",
    HERE / "verify_live_three_zero_eighth_split_all_order_mixed_role_census.py",
    HERE.parent / "notes/live-three-zero-eighth-split-all-order-five-double-six-class-residue-closure.md",
    HERE / "verify_live_three_zero_eighth_split_all_order_five_double_six_class_residue_closure.py",
)
assert all(path.is_file() for path in accepted_artifacts)


print("h=8, k=5 updated collision census: PASS")
print("frozen residuals: 44")
print("accepted closures: 44 = 18 historical + 25 incidence + 1 endpoint")
print("open profiles: 0")
