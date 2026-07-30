#!/usr/bin/env python3
"""Exact lightweight audit of the selector sum-channel mixing lock."""

from verify_two_chart_selector_provenance_sum_channel_guard import (
    add,
    omega,
    scale,
)


if not __debug__:
    raise RuntimeError("run without -O: this exact checker uses assertions")


def main():
    direct = (1, 1, 1, 2)
    forward = (0, 1, 0, 1)
    backward = (0, 1, 0, 1)
    edge_sum = add(forward, backward)
    k_forward = scale(-1, forward)
    k_backward = scale(-1, backward)

    assert forward == backward
    assert edge_sum == scale(2, forward)
    assert direct[1] or direct[2]
    assert omega(direct, direct) == 0
    assert omega(direct, (1, 0, 0, 0)) == 0
    assert omega(direct, (0, 0, 0, 1)) == 0
    assert omega(direct, (0, 1, 0, 0)) == 1
    assert omega(direct, edge_sum) == 2
    assert omega(direct, k_forward) == -1
    assert omega(direct, k_backward) == -1
    assert all(
        omega(direct, add(scale(residual, direct), scale(-1, forward))) == -1
        for residual in range(-4, 5)
    )

    common_cap_value = 1
    checked = 0
    for left in range(-4, 5):
        for right in range(-4, 5):
            mixture = add(scale(left, k_forward), scale(right, k_backward))
            detection = (left + right) * common_cap_value
            provenance = omega(direct, mixture)
            assert 2 * provenance == -detection * omega(direct, edge_sum)
            if detection:
                assert provenance
            checked += 1

    hessian_mix = add(scale(2, k_forward), scale(-1, k_backward))
    bianchi_difference = add(k_forward, scale(-1, k_backward))
    assert omega(direct, hessian_mix) == -1
    assert omega(direct, bianchi_difference) == 0

    print(f"selector sum-channel mixing lock: PASS ({checked} mixtures)")
    print(
        "  Hessian-repair coefficients (2,-1): "
        "formal common evaluation 1, provenance -1"
    )
    print(
        "  Bianchi coefficients (1,-1): "
        "formal common evaluation 0, provenance 0"
    )


if __name__ == "__main__":
    main()
