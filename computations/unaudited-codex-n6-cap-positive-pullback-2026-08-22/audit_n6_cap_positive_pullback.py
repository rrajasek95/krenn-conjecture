#!/usr/bin/env python3
"""Exact local Hermitianization and commonization guard for N6 certificates."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_n6_cap_positive_pullback.json"
HS = (ROOT / "computations/unaudited-codex-hermitian-star-sos-2026-08-22"
      / "audit_hermitian_star_trace.py")
CAPS = (ROOT / "computations/unaudited-codex-x4-cap-falsifier-2026-08-20"
        / "results_binary_pool_join.json")
PINS = {
    HS: "eb437133453d13ab0a5e3f964c25dfd60bc8846aeec3b24d7c3ad413198fa389",
    CAPS: "c6ec4d3878a7fff3b2af91d2a32331dacb3adf223d638c7bc5d2725e5bcd1947",
    ROOT / "proofs/six-site-arbitrary-complex-obstruction.md":
        "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
    ROOT / "proofs/saturated-rank-graph-obstruction.md":
        "97f7f1003f0e5c3f2b68e91a8ad1f514390339c7fcf5327fbfab93ec116db841",
    ROOT / "proofs/low-rank-graph-laurent-obstruction.md":
        "9140f354c93c1495b8f07d5a59acb014e33c9f231fa102fc9e6c91d9d2e0c611",
    ROOT / "proofs/exceptional-triangle-obstruction.md":
        "e9dee45efb1508273decb21dd7435d153109be3092cbabd075487919806500b1",
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


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def find_phased_c6_rectangle(hs):
    source = hs.n6_source()
    exceptional = set(hs.FACTORS[0] + hs.FACTORS[1])
    all_matchings = tuple(tuple(sorted(matching))
                          for matching in hs.perfect_matchings(range(6)))
    cycle_matchings = tuple(tuple(sorted(matching))
                            for matching in hs.FACTORS[:2])

    def compatible(matching, word):
        return all(source[edge][word[edge[0]]][word[edge[1]]] != hs.ZERO
                   for edge in matching)

    for edge in sorted(exceptional):
        u, v = edge
        tail = tuple(site for site in range(6) if site not in edge)
        for rows in combinations(range(3), 2):
            for columns in combinations(range(3), 2):
                for tail_colours in product(range(3), repeat=4):
                    fixed = dict(zip(tail, tail_colours))
                    words = []
                    good = True
                    for a in rows:
                        for b in columns:
                            word = tuple(a if site == u else b if site == v
                                         else fixed[site] for site in range(6))
                            live = tuple(matching for matching in all_matchings
                                         if compatible(matching, word))
                            if set(live) != set(cycle_matchings) or len(set(word)) == 1:
                                good = False
                                break
                            words.append(word)
                        if not good:
                            break
                    if not good:
                        continue

                    first = next(m for m in cycle_matchings if edge in m)
                    second = next(m for m in cycle_matchings if edge not in m)
                    tail_factor = hs.ONE
                    for other_edge in first:
                        if other_edge != edge:
                            tail_factor = hs.zmul(
                                tail_factor,
                                source[other_edge][fixed[other_edge[0]]]
                                                  [fixed[other_edge[1]]],
                            )
                    edge_u = next(e for e in second if u in e)
                    edge_v = next(e for e in second if v in e)
                    remote = next(e for e in second if e not in (edge_u, edge_v))
                    remote_factor = source[remote][fixed[remote[0]]][fixed[remote[1]]]

                    p_values = []
                    for a in rows:
                        left = a if edge_u[0] == u else fixed[edge_u[0]]
                        right = a if edge_u[1] == u else fixed[edge_u[1]]
                        p_values.append(source[edge_u][left][right])
                    q_values = []
                    for b in columns:
                        left = b if edge_v[0] == v else fixed[edge_v[0]]
                        right = b if edge_v[1] == v else fixed[edge_v[1]]
                        q_values.append(hs.zmul(source[edge_v][left][right],
                                               remote_factor))
                    x = [[source[edge][a][b] for b in columns] for a in rows]
                    residual = [[
                        hs.zadd(hs.zmul(tail_factor, x[i][j]),
                                hs.zmul(p_values[i], q_values[j]))
                        for j in range(2)] for i in range(2)]
                    determinant = hs.zsub(hs.zmul(x[0][0], x[1][1]),
                                          hs.zmul(x[0][1], x[1][0]))
                    combination = hs.zsub(
                        hs.zmul(tail_factor,
                                hs.zsub(hs.zmul(residual[0][0], x[1][1]),
                                        hs.zmul(residual[0][1], x[1][0]))),
                        hs.zmul(p_values[0],
                                hs.zsub(hs.zmul(q_values[0], residual[1][1]),
                                        hs.zmul(q_values[1], residual[1][0]))),
                    )
                    right = hs.zmul(hs.zmul(tail_factor, tail_factor), determinant)
                    require(combination == right, (combination, right))
                    require(hs.znorm(right) > 0, right)
                    return {
                        "edge": list(edge),
                        "row_colours": list(rows),
                        "column_colours": list(columns),
                        "tail_colours": list(tail_colours),
                        "first_matching": [list(e) for e in first],
                        "second_matching": [list(e) for e in second],
                        "tail_localizer": hs.ztext(tail_factor),
                        "determinant": hs.ztext(determinant),
                        "combination": hs.ztext(combination),
                        "positive_identity_value": str(hs.znorm(combination)),
                        "residual_matrix": [[hs.ztext(value) for value in row]
                                            for row in residual],
                    }
    raise RuntimeError("no phased C6 free rectangle")


def mutation_counterguard():
    # Old locally closed packet: F_ab=L X_ab+P_a Q_b.  Turn on one extra
    # matching monomial Z only in the (0,0) corner.  All localizers and the
    # determinant remain live although all four mutated residuals vanish.
    localizer = 1
    p = (1, 1)
    q = (1, 1)
    extra = 1
    x = ((-2, -1), (-1, -1))
    residual = (
        (localizer*x[0][0] + p[0]*q[0] + extra,
         localizer*x[0][1] + p[0]*q[1]),
        (localizer*x[1][0] + p[1]*q[0],
         localizer*x[1][1] + p[1]*q[1]),
    )
    determinant = x[0][0]*x[1][1] - x[0][1]*x[1][0]
    combination = (
        localizer*(residual[0][0]*x[1][1] - residual[0][1]*x[1][0])
        - p[0]*(q[0]*residual[1][1] - q[1]*residual[1][0])
    )
    require(residual == ((0, 0), (0, 0)), residual)
    require(determinant == 1 and localizer == 1 and extra == 1,
            (determinant, localizer, extra))
    require(combination == 0, combination)
    return {
        "L": localizer,
        "P": list(p),
        "Q": list(q),
        "Z_new_matching": extra,
        "X": [list(row) for row in x],
        "mutated_residuals": [list(row) for row in residual],
        "det_X": determinant,
        "old_identity_left": combination * combination,
        "old_identity_right": localizer ** 4 * determinant ** 2,
        "conclusion": (
            "The old chart localizer remains one, but its SOS identity fails "
            "after a formerly absent matching term is activated."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-local-identity", action="store_true")
    args = parser.parse_args()
    for path, digest in PINS.items():
        require(file_sha(path) == digest, (path, file_sha(path), digest))

    hs = load("hs_for_n6_cap_positive", HS)
    rectangle = find_phased_c6_rectangle(hs)
    if args.mutate_local_identity:
        rectangle["positive_identity_value"] = "0"
    require(rectangle["positive_identity_value"] == "3", rectangle)

    mutation = mutation_counterguard()
    require(mutation["old_identity_left"] == 0
            and mutation["old_identity_right"] == 1, mutation)

    # The two smallest Laurent Hermitianizations have exact PSD Gram matrices.
    signed_binomial_gram = [[2, 0], [0, 2]]  # rows (1,1), (1,-1)
    translated_trinomial_difference_gram = [
        [0, 0, 0], [0, 4, 0], [0, 0, 0]
    ]  # |(1+r+s)-(1-r+s)|^2=4|r|^2.
    require(all(signed_binomial_gram[i][i] > 0 for i in range(2)),
            signed_binomial_gram)
    require(translated_trinomial_difference_gram[1][1] == 4,
            translated_trinomial_difference_gram)

    caps = json.loads(CAPS.read_text())["controls"]
    require(caps["W40"]["star_passes"] == 6, caps["W40"])
    require(caps["W25"]["star_passes"] == 0
            and caps["W25"]["triangle_passes"] == 0, caps["W25"])

    tensor4 = hs.amplitudes(hs.n4_source(), 4)
    pure4 = {(colour,) * 4 for colour in range(3)}
    require(sum(value != hs.ZERO and word not in pure4
                for word, value in tensor4.items()) == 0, "n4 GHZ control")
    tensor6 = hs.amplitudes(hs.n6_source(), 6)
    pure6 = {(colour,) * 6 for colour in range(3)}
    mixed_norm6 = sum(hs.znorm(value) for word, value in tensor6.items()
                      if word not in pure6)
    require(mixed_norm6 == 1526, mixed_norm6)

    generic_degree_scale = 3 ** 135
    payload = {
        "status": "PASS local Hermitian pullback; terminal low-degree/common-weight no-go",
        "global_certificate_fact": {
            "statement": (
                "Because the 135-variable normalized N6 ideal has empty "
                "complex zero set, Hilbert Nullstellensatz guarantees one "
                "global certificate 1=sum_w Q_w F_w, independent of the "
                "rank/support branches."
            ),
            "quantitative_inequality": (
                "Cauchy gives 1 <= (sum_w |Q_w(y)|^2)(sum_w |F_w(y)|^2)."
            ),
            "generic_effective_degree_scale": str(generic_degree_scale),
            "generic_effective_degree_digits": len(str(generic_degree_scale)),
            "qualification": (
                "3^135 is recorded only as the scale of a generic singly-"
                "exponential effective bound; the frozen branch proof has "
                "no polynomial multiplier or degree ledger."
            ),
        },
        "local_positive_constructions": {
            "C6_free_rectangle": rectangle,
            "fraction_free_identity": (
                "If F_ab=L X_ab+P_a Q_b, then "
                "L(F_ij X_kl-F_il X_kj)-P_i(Q_j F_kl-Q_l F_kj)="
                "L^2 det(X). Taking modulus square gives one exact PSD "
                "source-faithful identity with RHS |L|^4|det X|^2."
            ),
            "Laurent_signed_Gram": signed_binomial_gram,
            "translated_trinomial_Gram": translated_trinomial_difference_gram,
        },
        "finite_cover_audit": {
            "exact_small_radical_test": (
                "For the free-rectangle activity a=L*det(X), the one-chart "
                "localizer ideal <L> saturates to the unit ideal by a: "
                "1 is in <L>:(L*det(X))^infinity. Thus the smallest "
                "localizer cover passes exactly."
            ),
            "localizer_radical": (
                "The nonzero-coordinate products can cover the open part of "
                "each exact support stratum and can in principle be raised "
                "to common projective K-degree. The artifacts do not export "
                "one unified full-chart localizer list for a larger radical "
                "calculation. This is not the obstruction exposed here."
            ),
            "failure": (
                "The certificate identities are valid on locally closed "
                "support strata: besides ell!=0 they require specified "
                "matching monomials to be exactly absent. |ell|^(2M) does "
                "not vanish when an absent monomial is turned on, so summing "
                "weighted identities is not a valid global identity."
            ),
            "exact_support_mutation": mutation,
            "compilation": (
                "A full algebraic case-split compilation is possible in "
                "principle by combining zero branches with saturated-open "
                "certificates and raising localizer powers. Repeating this "
                "through the support/rank SAT tree causes uncontrolled "
                "degree growth; the LRAT/semantic artifacts store no Q_w."
            ),
        },
        "controls": {
            "n4_exact_GHZ": "all mixed amplitudes zero",
            "phased_n6": {
                "mixed_residual_norm_squared": str(mixed_norm6),
                "role": (
                    "Actual source-faithful C6 rectangle with live minor and "
                    "local SOS value three; stationarity for its own output "
                    "does not make the N6 GHZ residual small."
                ),
            },
            "W40": caps["W40"],
            "W25": caps["W25"],
        },
        "minimum_norm_coupling": (
            "After cap pullback, y=x+r/s and the one-site normalization uses "
            "s/kappa_c. The global Q_w(y) therefore acquires high powers and "
            "inverse activity factors. Near s*kappa_0*kappa_1*kappa_2=0 its "
            "Cauchy lower bound degenerates. The minimum-norm normal equations "
            "supply no bound on Q_w or any reason that an effective N6 "
            "residual is small; phased N6 is the exact guard."
        ),
        "terminal_verdict": (
            "The archive supports useful chartwise PSD identities and "
            "abstractly guarantees a global Nullstellensatz/Cauchy inequality, "
            "but it does not compile to a low-degree common Hermitian identity "
            "or a positive lower bound coupled to attained N8 minimum norm."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        HERE.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("rectangle", rectangle)
    print("mutation", mutation)
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
