#!/usr/bin/env python3
"""Exact edge-block Moore--Penrose and contribution-energy controls."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_edge_block_energy.json"
HERMITIAN = (ROOT / "computations/unaudited-codex-hermitian-star-sos-2026-08-22"
             / "audit_hermitian_star_trace.py")
PINS = {
    HERMITIAN: "eb437133453d13ab0a5e3f964c25dfd60bc8846aeec3b24d7c3ad413198fa389",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def load_hermitian():
    spec = importlib.util.spec_from_file_location("frozen_hermitian_trace", HERMITIAN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scalar(module, value, number):
    return module.zmul(module.z(value), number)


def vector_add(module, left, right):
    return [module.zadd(a, b) for a, b in zip(left, right)]


def vector_sub(module, left, right):
    return [module.zsub(a, b) for a, b in zip(left, right)]


def vector_norm(module, vector):
    return sum((module.znorm(value) for value in vector), Fraction(0))


def block_control(module, source, n, label):
    words = tuple(product(range(3), repeat=n))
    word_index = {word: index for index, word in enumerate(words)}
    output_dict = module.amplitudes(source, n)
    output = [output_dict[word] for word in words]
    edge_records = []
    contributions = {}
    energy = Fraction(0)

    for edge in combinations(range(n), 2):
        p, q = edge
        residual = tuple(v for v in range(n) if v not in edge)
        residual_words = tuple(product(range(3), repeat=n-2))
        cofactors = []
        for residual_word in residual_words:
            full_word = [0] * n
            for site, colour in zip(residual, residual_word):
                full_word[site] = colour
            cofactors.append(module.cofactor(source, tuple(full_word), residual))
        h_e = vector_norm(module, cofactors)
        block = source[edge]
        block_norm = sum((module.znorm(value) for row in block for value in row),
                         Fraction(0))

        contribution = []
        for word in words:
            residual_word = tuple(word[v] for v in residual)
            index = sum(colour * 3**(n-3-position)
                        for position, colour in enumerate(residual_word))
            contribution.append(module.zmul(block[word[p]][word[q]],
                                             cofactors[index]))
        contributions[edge] = contribution
        contribution_norm = vector_norm(module, contribution)
        require(contribution_norm == h_e * block_norm,
                (label, edge, contribution_norm, h_e, block_norm))
        energy += contribution_norm

        # B_e is the sum of matching terms avoiding e.  The exact fibre row is
        # output-B_e=U_e.  Replay every one of the nine Moore--Penrose cells.
        base = vector_sub(module, output, contribution)
        required = vector_sub(module, output, base)
        numerator_norms = []
        output_is_kkt_multiplier = True
        for i, j in product(range(3), repeat=2):
            required_slice = []
            output_slice = []
            for residual_word in residual_words:
                word = [0] * n
                word[p], word[q] = i, j
                for site, colour in zip(residual, residual_word):
                    word[site] = colour
                index = word_index[tuple(word)]
                required_slice.append(required[index])
                output_slice.append(output[index])
            numerator = module.inner(cofactors, required_slice)
            expected = scalar(module, h_e, block[i][j])
            require(numerator == expected,
                    (label, edge, i, j, numerator, expected))
            output_is_kkt_multiplier &= (module.inner(cofactors, output_slice)
                                         == block[i][j])
            numerator_norms.append(module.ztext(numerator))

        edge_records.append({
            "edge": list(edge),
            "residual_cofactor_norm_squared_h": str(h_e),
            "source_block_norm_squared": str(block_norm),
            "contribution_norm_squared": str(contribution_norm),
            "TstarT": f"{h_e}*I9",
            "all_nine_moore_penrose_numerators_replayed": True,
            "Tstar_output_equals_source_block": output_is_kkt_multiplier,
            "visible": h_e != 0,
            "source_block_nonzero": block_norm != 0,
        })

    m = n // 2
    edge_count = n * (n-1) // 2
    total_contribution = [module.ZERO] * len(words)
    for contribution in contributions.values():
        total_contribution = vector_add(module, total_contribution, contribution)
    require(total_contribution == [scalar(module, m, value) for value in output],
            (label, "Euler contribution sum"))
    for vertex in range(n):
        star = [module.ZERO] * len(words)
        for edge, contribution in contributions.items():
            if vertex in edge:
                star = vector_add(module, star, contribution)
        require(star == output, (label, "star reconstruction", vertex))

    average = [scalar(module, Fraction(m, edge_count), value) for value in output]
    centered = Fraction(0)
    for contribution in contributions.values():
        centered += vector_norm(module, vector_sub(module, contribution, average))
    output_norm = vector_norm(module, output)
    floor = Fraction(m*m, edge_count) * output_norm
    require(energy == floor + centered,
            (label, "centered energy", energy, floor, centered))

    profile = Counter((record["residual_cofactor_norm_squared_h"],
                       record["source_block_norm_squared"])
                      for record in edge_records)
    return {
        "label": label,
        "n": n,
        "m": m,
        "edge_count": edge_count,
        "source_norm_squared": str(sum(
            (module.znorm(value) for matrix in source.values()
             for row in matrix for value in row), Fraction(0))),
        "output_norm_squared": str(output_norm),
        "output_support": sum(value != module.ZERO for value in output),
        "visible_edge_blocks": sum(record["visible"] for record in edge_records),
        "nonzero_source_blocks": sum(record["source_block_nonzero"]
                                     for record in edge_records),
        "edge_profile_h_blocknorm": [
            {"h": h, "block_norm_squared": a, "count": count}
            for (h, a), count in sorted(profile.items())
        ],
        "edge_energy": str(energy),
        "centered_floor": str(floor),
        "centered_SOS_slack": str(centered),
        "all_site_star_reconstructions": True,
        "all_edge_moore_penrose_replays": True,
        "global_KKT_multiplier_lambda_equals_output": all(
            record["Tstar_output_equals_source_block"] for record in edge_records),
        "edge_records": edge_records,
    }


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-n4-energy", action="store_true")
    args = parser.parse_args()
    for path, digest in PINS.items():
        require(file_sha(path) == digest, (str(path), file_sha(path), digest))
    module = load_hermitian()
    n4 = block_control(module, module.n4_source(), 4, "exact n4 ternary GHZ")
    n6 = block_control(module, module.n6_source(), 6,
                       "phased n6 block-injective own-output minimum")
    if args.mutate_n4_energy:
        n4["edge_energy"] = "5"
    require(n4["edge_energy"] == "6" and n4["centered_SOS_slack"] == "4", n4)
    require(n4["global_KKT_multiplier_lambda_equals_output"], n4)
    require(n6["edge_energy"] == "5136"
            and n6["centered_SOS_slack"] == "21093/5", n6)
    payload = {
        "status": "PASS exact edge-block recurrence; terminal Hermitian/Gram collapse",
        "source_pin": {str(path.relative_to(ROOT)): digest
                       for path, digest in PINS.items()},
        "theorem": {
            "block_map": (
                "For e=pq and residual matching tensor C_e, T_e(X)=X tensor C_e "
                "in endpoint-word order, hence T_e^*T_e=h_e I9, h_e=||C_e||^2."
            ),
            "least_norm": (
                "Writing Phi(A)=T_e(A_e)+B_e, a fibre norm minimum has A_e=0 "
                "when h_e=0.  When h_e!=0, A_e=h_e^(-1)T_e^*(Y-B_e); because "
                "Y-B_e=T_e(A_e), this visible-chart formula is tautological."
            ),
            "global_KKT": (
                "A regular global norm minimum obeys A_e=T_e^*lambda. Summing "
                "<A_e,A_e>=<lambda,T_eA_e> gives ||A||^2=m<lambda,Y>. "
                "The Fritz--John alpha=0 branch supplies no such normalized identity."
            ),
            "N8_energy": (
                "For U_e=T_e(A_e), sum_e U_e=4Y and sum_(e incident v)U_e=Y. "
                "Thus for ternary GHZ, sum_e h_e||A_e||^2 = "
                "12/7 + sum_e ||U_e-Y/7||^2."
            ),
        },
        "controls": {"n4": n4, "n6": n6},
        "terminal_verdict": (
            "The KKT sum is the archived global Euler trace.  The only positive "
            "edge-energy refinement is the centered contribution/star-frame SOS, "
            "equivalently the [8]+[6,2] perfect-matching incidence Gram sector. "
            "It gives a lower bound, not a vanishing summand; equality would make "
            "all U_e=Y/7 and therefore makes every contribution visible.  It contains "
            "no response-star variables and cannot force a clean cap."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        HERE.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("n4", n4["edge_energy"], n4["centered_SOS_slack"])
    print("n6", n6["edge_energy"], n6["centered_SOS_slack"])
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
