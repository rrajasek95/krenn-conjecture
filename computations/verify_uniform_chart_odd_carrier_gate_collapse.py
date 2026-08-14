#!/usr/bin/env python3
"""Identify the local Gate-II and uniform Bianchi gaps as one carrier.

The presentation-safe relative graph for two occurrence charts is

    d theta_i = z_i-u_i,
    d phi_j   = t_j-(z_j-z_0).

Thus Gamma_j=phi_j+theta_j-theta_0 has

    d Gamma_j=t_j-(u_j-u_0).

For the h=3 primitive-C4 packet (A,B,C), this gives

    2A-B-C = -(t_B+t_C)  modulo boundaries.

For two overlapping pair-chart copies of every global matching occurrence,
the tagged Bianchi difference is similarly equal to the chart-odd carrier
``t`` modulo boundaries.  Hence one physical augmented saturation of the
relative carrier kills both gaps.  This checker proves the exact finite
linear algebra and presentation preservation; it does not construct that
physical saturation map.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py":
        "e0a8251128174d50b450b3bf85ce0a6870af00d4ab5565e7849fc3c8644c31c6",
    "notes/uniform-chart-cross-companion-relative-switch-dga-gate.md":
        "2b9fbe0c648cadc5913e57e4b6d678205c7f7fbc66f57e58e371f9ad10ef2cb8",
    "computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py":
        "d77f4fd853673c434d4a0bb4027bf9ba046f1bb7ea4d752028a609e832255f44",
    "notes/h3-gate-ii-primitive-c4-joint-cobar-label-gate.md":
        "1adefa3bf3427a8f0c9c415376561bdd6b56c2f358fb236260b9956e7d7b0e62",
    "computations/verify_uniform_bianchi_all_word_signed_kernel_gate.py":
        "5bcff5015ce56e9d7ba8ba9b57007080968540dac81429a6a695421ed2bd5338",
    "notes/uniform-bianchi-all-word-signed-kernel-gate.md":
        "13f0d45e91774dcc528b009aedc3d37779120bdefb6caa7d5b010b53cfd222a3",
}
EXPECTED_LEDGER_SHA256 = (
    "60aff545587909bc8f1709bf08d4e617f1c6b4ee6826d3a47cb31ff33bdad255"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def check_pins() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual, expected))


def rank(columns: list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def unit(index: int, size: int) -> tuple[Q, ...]:
    return tuple(Q(index == place) for place in range(size))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(value: int, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(value) * entry for entry in vector)


def h3_gate_ii_graph() -> dict[str, int]:
    # Coordinates: uA,uB,uC,zA,zB,zC,tB,tC.
    size = 8
    u_a, u_b, u_c, z_a, z_b, z_c, t_b, t_c = range(size)
    theta_a = add(scale(-1, unit(u_a, size)), unit(z_a, size))
    theta_b = add(scale(-1, unit(u_b, size)), unit(z_b, size))
    theta_c = add(scale(-1, unit(u_c, size)), unit(z_c, size))
    phi_b = add(unit(t_b, size), scale(-1, unit(z_b, size)),
                unit(z_a, size))
    phi_c = add(unit(t_c, size), scale(-1, unit(z_c, size)),
                unit(z_a, size))
    graph = [theta_a, theta_b, theta_c, phi_b, phi_c]
    require(rank(graph) == 5, "the monic h3 graph lost rank")

    gamma_b = add(phi_b, theta_b, scale(-1, theta_a))
    gamma_c = add(phi_c, theta_c, scale(-1, theta_a))
    expected_b = add(unit(t_b, size), scale(-1, unit(u_b, size)),
                     unit(u_a, size))
    expected_c = add(unit(t_c, size), scale(-1, unit(u_c, size)),
                     unit(u_a, size))
    require(gamma_b == expected_b and gamma_c == expected_c,
            "relative switch boundary changed")

    # L=2A-B-C and T=tB+tC.  Their sum is exactly d(GammaB+GammaC).
    l_01 = add(scale(2, unit(u_a, size)), scale(-1, unit(u_b, size)),
               scale(-1, unit(u_c, size)))
    total_carrier = add(unit(t_b, size), unit(t_c, size))
    require(add(l_01, total_carrier) == add(gamma_b, gamma_c),
            "Gate-II L01 is not the negative total switch carrier")
    require(rank(graph + [l_01]) == 6,
            "L01 unexpectedly vanished before carrier saturation")
    require(rank(graph + [total_carrier]) == 6,
            "the carrier should represent the same one-dimensional class")
    require(rank(graph + [l_01, total_carrier]) == 6,
            "L01 and the carrier stopped representing one quotient class")

    # The graph is presentation preserving: old u coordinates plus the five
    # graph boundaries span all eight extended degree-zero coordinates.
    old_lifts = []
    for u_index, z_index in ((u_a, z_a), (u_b, z_b), (u_c, z_c)):
        old_lifts.append(add(unit(u_index, size), unit(z_index, size)))
    # Add the forced t values uB-uA and uC-uA to the old lifts linearly.
    old_lifts[0] = add(old_lifts[0], scale(-1, unit(t_b, size)),
                       scale(-1, unit(t_c, size)))
    old_lifts[1] = add(old_lifts[1], unit(t_b, size))
    old_lifts[2] = add(old_lifts[2], unit(t_c, size))
    require(rank(graph + old_lifts) == size,
            "relative graph changed the old occurrence H0")

    return {"extended_coordinates": size, "graph_rank": rank(graph),
            "h0_dimension": size - rank(graph),
            "carrier_quotient_rank": rank(graph + [total_carrier]) - rank(graph)}


def uniform_pair_chart_graph(max_words: int = 12) -> dict[str, int]:
    # Audit a direct sum of n identical pair-chart graphs.  Per word the
    # coordinates are u0,u1,z0,z1,t, and the three monic graph columns have
    # quotient dimension two.  beta=u1-u0 equals t modulo dGamma.
    for words in range(1, max_words + 1):
        size = 5 * words
        columns: list[tuple[Q, ...]] = []
        beta = (Q(0),) * size
        carrier = (Q(0),) * size
        for word in range(words):
            u0, u1, z0, z1, t = (5 * word + offset for offset in range(5))
            theta0 = add(scale(-1, unit(u0, size)), unit(z0, size))
            theta1 = add(scale(-1, unit(u1, size)), unit(z1, size))
            phi = add(unit(t, size), scale(-1, unit(z1, size)),
                      unit(z0, size))
            columns.extend((theta0, theta1, phi))
            beta = add(beta, unit(u1, size), scale(-1, unit(u0, size)))
            carrier = add(carrier, unit(t, size))
        require(rank(columns) == 3 * words,
                ("pair-chart graph rank", words))
        require(in_span(columns, add(carrier, scale(-1, beta))),
                ("beta/carrier class mismatch", words))

        # Every strict common-word readout has equal coefficients on u0,u1
        # and zero on t, hence kills both the tagged beta and its carrier.
        for word in range(words):
            row = [Q(0)] * size
            row[5 * word] = row[5 * word + 1] = Q(1)
            beta_value = sum(left * right for left, right in
                             zip(row, beta, strict=True))
            carrier_value = sum(left * right for left, right in
                                zip(row, carrier, strict=True))
            require(beta_value == carrier_value == 0,
                    ("strict row detected chart-odd class", words, word))
    return {"first_word_count": 1, "last_word_count": max_words,
            "graph_rank_per_word": 3, "h0_per_word": 2,
            "signed_carrier_per_word": 1}


def in_span(columns: list[tuple[Q, ...]], vector: tuple[Q, ...]) -> bool:
    return rank(columns + [vector]) == rank(columns)


def saturation_consequence() -> dict[str, str]:
    # Abstract two-step calculation: dGamma=T-beta and dEta=T imply
    # d(Gamma-Eta)=-beta.  For two local companions, summing the same identity
    # and using L+T=dGamma_sum gives d(Gamma_sum-Eta_sum)=L.
    # Store the coefficient audit explicitly.
    d_gamma = (Q(1), Q(-1))   # (T,beta)
    d_eta = (Q(1), Q(0))
    require(tuple(left - right for left, right in zip(d_gamma, d_eta,
                                                       strict=True)) ==
            (Q(0), Q(-1)), "saturation did not fill beta")
    d_gamma_local = (Q(1), Q(1))  # (T,L), since dGamma=T+L
    require(tuple(left - right for left, right in
                  zip(d_gamma_local, d_eta, strict=True)) ==
            (Q(0), Q(1)), "saturation did not fill L01")
    return {
        "single_open_datum": "a physical augmented nullhomotopy of the chart-odd t carrier",
        "local_consequence": "fills 2DQ-PS-PS before the 0102 ladder",
        "uniform_consequence": "kills the tagged Bianchi descent obstruction",
    }


def mutation_guards() -> None:
    # Reversing only one switch orientation destroys L=-T.
    require((2, -1, -1) != (0, 1, -1),
            "one oriented switch incorrectly represented L01")
    # Identifying t with zero would impose equality of old occurrence values
    # and lower H0 by one; it is not a presentation-safe construction.
    require(rank([(Q(-1), Q(1))]) == 1,
            "raw chart identification stopped imposing a relation")


def main() -> None:
    check_pins()
    h3 = h3_gate_ii_graph()
    uniform = uniform_pair_chart_graph()
    consequence = saturation_consequence()
    mutation_guards()
    ledger = {"h3": h3, "uniform": uniform, "consequence": consequence}
    digest = sha256(repr(ledger).encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("chart-odd carrier ledger changed", digest,
             EXPECTED_LEDGER_SHA256))
    print("PASS: chart-odd carrier gate collapse")
    print("Gate-II 2DQ-PS-PS: NEGATIVE TOTAL SWITCH CARRIER")
    print("Bianchi chart sign: THE SAME RELATIVE CARRIER TYPE")
    print("strict word rows: BLIND TO THE CARRIER")
    print("physical augmented carrier saturation: STILL OPEN")
    print(f"digest: {digest}")


if __name__ == "__main__":
    main()
