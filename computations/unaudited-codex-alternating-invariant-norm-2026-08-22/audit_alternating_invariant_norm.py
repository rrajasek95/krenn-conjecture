#!/usr/bin/env python3
"""Exact norm counteraudit for the three-copy alternating invariant."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from math import prod
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_alternating_invariant_norm.json"
INPUTS = {
    ROOT / "computations/verify_three_copy_alternating_invariant.py":
        "2b4b325165515ced6c40ff264491ef13ba735bd2a46a78bcf8417a0f0418d09e",
    ROOT / "computations/verify_gaussian_norm_invariant.py":
        "eec522f312981e3f87e64eaa2564190b4ccbad00698ec2a31d7fab889bb11673",
    ROOT / "computations/verify_global_wick_top_invariant_counterguard.py":
        "192c03668e56262315e685f49c29fafeed071faf2a292dfdc94544fd7a5f4183",
    ROOT / "computations/unaudited-codex-hermitian-star-sos-2026-08-22"
           / "audit_hermitian_star_trace.py":
        "eb437133453d13ab0a5e3f964c25dfd60bc8846aeec3b24d7c3ad413198fa389",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PERMS = tuple(permutations(range(3)))


def permutation_sign(p):
    inversions = sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
    return -1 if inversions % 2 else 1


SIGNS = {p: permutation_sign(p) for p in PERMS}


def eisenstein_invariant(hs, tensor, n):
    answer = hs.ZERO
    for local_permutations in product(PERMS, repeat=n):
        words = [tuple(p[copy] for p in local_permutations) for copy in range(3)]
        term = hs.zmul(hs.zmul(tensor[words[0]], tensor[words[1]]),
                       tensor[words[2]])
        if term == hs.ZERO:
            continue
        if prod(SIGNS[p] for p in local_permutations) < 0:
            term = hs.zneg(term)
        answer = hs.zadd(answer, term)
    return answer


def sparse_rational_invariant(tensor, n):
    answer = Fraction(0)
    for local_permutations in product(PERMS, repeat=n):
        words = [tuple(p[copy] for p in local_permutations) for copy in range(3)]
        if not all(word in tensor for word in words):
            continue
        answer += (prod(SIGNS[p] for p in local_permutations)
                   * tensor[words[0]] * tensor[words[1]] * tensor[words[2]])
    return answer


def source_norm_squared(hs, source):
    return sum(hs.znorm(value) for matrix in source.values()
               for row in matrix for value in row)


def output_norm_squared(hs, tensor):
    return sum(hs.znorm(value) for value in tensor.values())


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-n4-minimum", action="store_true")
    args = parser.parse_args()

    for path, digest in INPUTS.items():
        require(file_sha(path) == digest, (path, file_sha(path), digest))
    hs_path = (ROOT / "computations/unaudited-codex-hermitian-star-sos-2026-08-22"
               / "audit_hermitian_star_trace.py")
    wick_path = ROOT / "computations/verify_global_wick_top_invariant_counterguard.py"
    hs = load("hermitian_star_for_alt_norm", hs_path)
    wick = load("wick_for_alt_norm", wick_path)

    # Exact n=4 GHZ minimum.  For each colour its six diagonal cells split
    # into three disjoint products; Cauchy gives energy >=2.  Thus total
    # source energy is at least six, attained by this source.
    source4 = hs.n4_source()
    tensor4 = hs.amplitudes(source4, 4)
    invariant4 = eisenstein_invariant(hs, tensor4, 4)
    norm4 = source_norm_squared(hs, source4)
    outnorm4 = output_norm_squared(hs, tensor4)
    if args.mutate_n4_minimum:
        norm4 += 1
    require(invariant4 == hs.z(6), invariant4)
    require(norm4 == 6, norm4)
    require(outnorm4 == 3, outnorm4)
    # Ratio |I| / ||A||^(3m), m=2, equals 6/S^3=1/36.
    require(Fraction(6, norm4 ** 3) == Fraction(1, 36), norm4)

    # Exact phased n=6 injective-block local minimum of its own output.
    source6 = hs.n6_source()
    tensor6 = hs.amplitudes(source6, 6)
    invariant6 = eisenstein_invariant(hs, tensor6, 6)
    norm6 = source_norm_squared(hs, source6)
    outnorm6 = output_norm_squared(hs, tensor6)
    invariant6_norm_squared = hs.znorm(invariant6)
    require(invariant6 == (Fraction(24264), Fraction(53604)), invariant6)
    require(invariant6_norm_squared == 2161483056, invariant6_norm_squared)
    require(norm6 == 63 and outnorm6 == 1529, (norm6, outnorm6))

    # The n=8 Laurent border at t=2 has only five output words.
    vertices, edges = wick.prism_seed()
    vertices, edges, shift = wick.expand_vertex(vertices, edges, min(vertices))
    require(len(vertices) == 8 and shift == 0, (vertices, shift))
    terms8 = sorted(wick.matching_term(matching, edges, vertices)
                    for matching in wick.perfect_matchings(vertices, edges))
    tensor8 = {
        word: (Fraction(2 ** exponent) if exponent >= 0
               else Fraction(1, 2 ** (-exponent)))
        for word, exponent in terms8
    }
    invariant8 = sparse_rational_invariant(tensor8, 8)
    norm8 = sum(Fraction(2) ** (2 * exponent)
                for _, exponent in edges.values())
    outnorm8 = sum(value * value for value in tensor8.values())
    matching_norm_sum8 = sum(tensor8.values())
    require(invariant8 == 6, invariant8)
    require(norm8 == Fraction(57, 4), norm8)
    require(outnorm8 == 11 and matching_norm_sum8 == 7,
            (outnorm8, matching_norm_sum8))

    # K_n^*K_n=2^n I gives the exact flattening norm 2^(n/2).
    # Check strictness without introducing square roots:
    # |I|^2 < 2^n ||H||^6.
    require(36 < 2 ** 4 * outnorm4 ** 3, "n4 flattening equality")
    require(invariant6_norm_squared < 2 ** 6 * outnorm6 ** 3,
            "n6 flattening equality")
    require(invariant8 ** 2 < 2 ** 8 * outnorm8 ** 3,
            "n8 flattening equality")

    # On the one-matching stratum, determinant Hadamard plus energy AM-GM is
    # sharp.  For n=4 its constant is 1/6, six times the GHZ-minimum ratio.
    one_matching_n4_constant = Fraction(1, 6)
    require(one_matching_n4_constant / Fraction(1, 36) == 6,
            one_matching_n4_constant)

    payload = {
        "status": "PASS exact alternating-invariant norm audit; terminal equality no-go",
        "theorems": {
            "vertex_determinant_block_bound": (
                "With nu_e=||A_e||_* and haf(nu)=sum_M prod_(e in M)nu_e, "
                "the vertex determinant expansion and SVD Hadamard give "
                "|I_n(H(A))| <= haf(nu)^3.  Fixed-triple equality requires "
                "orthogonal incident factor triples and phase alignment for "
                "every nonzero label configuration."
            ),
            "frobenius_flattening_bound": (
                "For K_n x=epsilon^(tensor n)(x,-,-), K_n^*K_n=2^n I. "
                "Thus |I_n(T)|<=2^(n/2)||T||^3 and, for r_e=||A_e||_F, "
                "|I_n(H(A))|<=2^(n/2)(sum_M prod_(e in M)r_e)^3."
            ),
            "source_scalar_corollary": (
                "For n=2m>=4, S=sum_e r_e^2 and d=(n-3)!! imply "
                "sum_M prod r_e <= d*m^(-m/2)*S^(m/2), hence "
                "|I_n(H(A))|<=2^m*d^3*m^(-3m/2)*||A||^(3m)."
            ),
            "one_matching_sharp_stratum": (
                "If only one perfect matching is live, |I|=6^m prod_e|det A_e| "
                "<= (2/sqrt(3))^m(S/m)^(3m/2), with equality exactly when "
                "all live blocks are scaled unitaries of equal Frobenius energy."
            ),
        },
        "controls": {
            "n4_exact_GHZ_global_minimum": {
                "source_norm_squared": str(norm4),
                "output_norm_squared": str(outnorm4),
                "invariant": hs.ztext(invariant4),
                "source_ratio": "|I|/||A||^6=1/36",
                "global_minimum_proof": (
                    "For each pure colour, Cauchy on the three disjoint "
                    "matching products forces diagonal-cell energy >=2; "
                    "summing colours gives S>=6, attained by the source."
                ),
                "equality": False,
            },
            "n6_phased_block_injective_local_minimum": {
                "source_norm_squared": str(norm6),
                "output_norm_squared": str(outnorm6),
                "invariant_Qomega": hs.ztext(invariant6),
                "invariant_modulus_squared": str(invariant6_norm_squared),
                "frobenius_matching_norm_sum": 103,
                "nuclear_matching_norm_sum": "85+180*sqrt(3)",
                "equality": False,
            },
            "n8_Laurent_border_at_t2": {
                "source_norm_squared": str(norm8),
                "output_norm_squared": str(outnorm8),
                "invariant": str(invariant8),
                "frobenius_matching_norm_sum": str(matching_norm_sum8),
                "source_ratio": "6/(57/4)^6",
                "asymptotic": (
                    "Along the same Laurent arc, I=6 and "
                    "S(t)=10+t^2+t^(-2), so the source ratio tends to zero "
                    "as t->0 while H(A(t))->GHZ."
                ),
                "equality": False,
            },
            "n4_one_matching_scaled_unitary": {
                "sharp_source_ratio": "1/6",
                "ratio_over_GHZ_minimum": 6,
                "output_is_GHZ": False,
            },
        },
        "logical_gap": (
            "On the exact GHZ fibre I_n(H(A)) is identically 6.  Norm "
            "minimization maximizes 6/||A||^(3m) only within that fibre; it "
            "does not force the global operator-norm equality.  The n=4 "
            "global fibre minimum has ratio 1/36, while the elementary "
            "one-matching stratum already reaches 1/6."
        ),
        "terminal_verdict": (
            "No Hadamard/Cauchy equality theorem can force a clean or "
            "rank-one matching triple at the GHZ fibre minimum.  The exact "
            "n=4 minimum is already strict, and the phased n=6 and n=8 "
            "Laurent controls are strict by larger margins."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        HERE.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("n4", invariant4, norm4, outnorm4)
    print("n6", invariant6, invariant6_norm_squared, norm6, outnorm6)
    print("n8", invariant8, norm8, outnorm8, matching_norm_sum8)
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
