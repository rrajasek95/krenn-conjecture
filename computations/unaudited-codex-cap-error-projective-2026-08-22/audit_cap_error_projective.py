#!/usr/bin/env python3
"""Bounded exact projective audit of intrinsic clean-cap error ideals."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
W25_DIR = ROOT / "computations" / "unaudited-x3core-w25-2026-08-15"
MPS_DIR = ROOT / "computations" / "unaudited-codex-global-minimal-mps-2026-08-21"
CAP_DIR = ROOT / "computations" / "unaudited-codex-cap-packet-2026-08-20"
sys.path.insert(0, str(W25_DIR))
sys.path.insert(0, str(MPS_DIR))
sys.path.insert(0, str(CAP_DIR))
import w25_core as core  # noqa: E402
import audit_minimum_norm_mps_guard as minimum_guard  # noqa: E402
import verify_minimal_norm_gauge as gauge  # noqa: E402


KVARS = tuple(f"zzk{i}{j}" for i in range(3) for j in range(3))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def n4_source():
    matrices = minimum_guard.n4_matrices()
    return {edge: [[Fraction(value) for value in row] for row in matrix]
            for edge, matrix in matrices.items()}


def om(value):
    return core.Om(Fraction(value[0]), Fraction(value[1]))


def phased_n6_source():
    fourier = (
        (gauge.Z1, gauge.Z1, gauge.Z1),
        (gauge.Z1, gauge.ZW, gauge.ZW2),
        (gauge.Z1, gauge.ZW2, gauge.ZW),
    )
    matrices = {}
    for edge in gauge.FOURIER_FACTORS[0] + gauge.FOURIER_FACTORS[1]:
        matrices[edge] = fourier
    for colour, factor in enumerate(gauge.FOURIER_FACTORS[2:]):
        anchor = tuple(tuple(gauge.Z1 if i == colour and j == colour
                             else gauge.Z0 for j in range(3))
                       for i in range(3))
        for edge in factor:
            matrices[edge] = anchor
    for edge, phase in gauge.FOURIER_PHASES.items():
        matrices[edge] = tuple(tuple(gauge.zmul(phase, entry) for entry in row)
                               for row in matrices[edge])
    return {edge: [[om(value) for value in row] for row in matrix]
            for edge, matrix in matrices.items()}


def load_w25():
    path = W25_DIR / "OBJECT_W25-F8_n8_allblocked_X3.json"
    obj = json.loads(path.read_text())
    return {tuple(map(int, key.split(","))):
            [[Fraction(value) for value in row] for row in matrix]
            for key, matrix in obj["blocks"].items()}


def load_w40():
    path = ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
    obj = json.loads(path.read_text())
    raw = obj["engine_audit"]["witness_B_integral"]["source"]
    source = {}
    for key, matrix in raw.items():
        clean = key.strip("()")
        edge = tuple(int(piece.strip()) for piece in clean.split(","))
        source[edge] = [[Fraction(value) for value in row] for row in matrix]
    return source


class Poly:
    """Sparse polynomial in the nine cap coordinates over Q or Q(omega)."""

    def __init__(self, terms=None):
        self.terms = {tuple(sorted(monomial)): coefficient
                      for monomial, coefficient in (terms or {}).items()
                      if coefficient}

    @staticmethod
    def var(index):
        return Poly({(index,): Fraction(1)})

    def __bool__(self):
        return bool(self.terms)

    def __add__(self, other):
        answer = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            value = answer.get(monomial, Fraction(0)) + coefficient
            if value:
                answer[monomial] = value
            else:
                answer.pop(monomial, None)
        return Poly(answer)

    def __mul__(self, other):
        answer = {}
        for left, a in self.terms.items():
            for right, b in other.terms.items():
                monomial = tuple(sorted(left + right))
                value = answer.get(monomial, Fraction(0)) + a * b
                if value:
                    answer[monomial] = value
                else:
                    answer.pop(monomial, None)
        return Poly(answer)

    def scale(self, scalar):
        return Poly({monomial: scalar * coefficient
                     for monomial, coefficient in self.terms.items()})

    def __pow__(self, exponent):
        require(exponent >= 0, exponent)
        answer = Poly({(): Fraction(1)})
        for _ in range(exponent):
            answer = answer * self
        return answer

    def evaluate(self, values):
        answer = Fraction(0)
        for monomial, coefficient in self.terms.items():
            term = coefficient
            for index in monomial:
                term *= values[index]
            answer += term
        return answer

    def singular(self, omega):
        from math import gcd, lcm
        denominator = 1
        for coefficient in self.terms.values():
            if core.is_om(coefficient):
                denominator = lcm(denominator, coefficient.a.denominator,
                                  coefficient.b.denominator)
            else:
                denominator = lcm(denominator, Fraction(coefficient).denominator)
        integer_terms = {}
        divisor = 0
        for monomial, coefficient in self.terms.items():
            if core.is_om(coefficient):
                a = int(coefficient.a * denominator)
                b = int(coefficient.b * denominator)
                integer_terms[monomial] = (a, b)
                divisor = gcd(divisor, abs(a), abs(b))
            else:
                a = int(Fraction(coefficient) * denominator)
                integer_terms[monomial] = (a, 0)
                divisor = gcd(divisor, abs(a))
        divisor = max(divisor, 1)
        pieces = []
        for monomial, (a, b) in sorted(integer_terms.items()):
            a, b = a // divisor, b // divisor
            if omega:
                coefficient = f"({a}+({b})*zw)"
            else:
                require(b == 0, (a, b))
                coefficient = str(a)
            factor = "*".join(KVARS[index] for index in monomial)
            pieces.append(coefficient if not factor else f"{coefficient}*{factor}")
        return "+".join(pieces) if pieces else "0"


def oriented(source, u, v):
    return core.oriented(source, u, v)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def cap_polynomials(source, pair):
    """Committed subset-of-matching formula for arbitrary even n."""
    n = core.sites_of(source)
    p, q = pair
    residual = tuple(site for site in range(n) if site not in pair)
    h = len(residual) // 2
    scalar = Poly()
    direct = oriented(source, p, q)
    for i, j in product(range(3), repeat=2):
        if direct[i][j]:
            scalar = scalar + Poly.var(3 * i + j).scale(direct[i][j])
    response = {}
    for a, b in combinations(residual, 2):
        apa, aqa = oriented(source, p, a), oriented(source, q, a)
        apb, aqb = oriented(source, p, b), oriented(source, q, b)
        matrix = [[Poly() for _ in range(3)] for _ in range(3)]
        for ca, cb in product(range(3), repeat=2):
            form = Poly()
            for i, j in product(range(3), repeat=2):
                coefficient = (apa[i][ca] * aqb[j][cb] +
                               aqa[j][ca] * apb[i][cb])
                if coefficient:
                    form = form + Poly.var(3 * i + j).scale(coefficient)
            matrix[ca][cb] = form
        response[(a, b)] = matrix

    equations = []
    equation_words = []
    slot = {site: index for index, site in enumerate(residual)}
    for word in product(range(3), repeat=len(residual)):
        total = Poly()
        for matching in perfect_matchings(residual):
            for response_count in range(2, h + 1):
                for chosen in combinations(range(h), response_count):
                    chosen = set(chosen)
                    term = scalar ** (h - response_count)
                    for index, (a, b) in enumerate(matching):
                        ca, cb = word[slot[a]], word[slot[b]]
                        if index in chosen:
                            term = term * response[(a, b)][ca][cb]
                        else:
                            term = term.scale(oriented(source, a, b)[ca][cb])
                    total = total + term
        if total:
            equations.append(total)
            equation_words.append(word)
    return (equations, equation_words, scalar,
            [Poly.var(0), Poly.var(4), Poly.var(8)])


def singular_profile(source, pair, max_power=6, associated=False,
                     timeout=120):
    n = core.sites_of(source)
    residual = tuple(site for site in range(n) if site not in pair)
    integral, scale = core.clear_denominators(source)
    omega = any(core.is_om(value) for matrix in integral.values()
                for row in matrix for value in row)
    equations, equation_words, scalar, kappas = cap_polynomials(integral, pair)
    sample_values = [core.oneelt(next(iter(integral.values()))[0][0]) * value
                     for value in (2, -3, 5, 7, -11, 13, 17, 19, -23)]
    sample_matrix = [sample_values[3 * i:3 * i + 3] for i in range(3)]
    direct = core.cap_error(integral, pair[0], pair[1], sample_matrix,
                            residual)
    symbolic = {word: polynomial.evaluate(sample_values)
                for word, polynomial in zip(equation_words, equations)}
    require(all(direct.get(word, 0) == symbolic.get(word, 0)
                for word in product(range(3), repeat=len(residual))),
            (pair, "two-engine cap error mismatch"))
    generators = [equation.singular(omega) for equation in equations]
    activity = "(" + scalar.singular(omega) + ")*(" + ")*(".join(
        kappa.singular(omega) for kappa in kappas) + ")"
    if omega:
        head = ["LIB \"elim.lib\";", "LIB \"primdec.lib\";",
                f'ring zzR=(0,zw),({",".join(KVARS)}),dp;',
                "minpoly=zw^2+zw+1;"]
    else:
        head = ["LIB \"elim.lib\";", "LIB \"primdec.lib\";",
                f'ring zzR=0,({",".join(KVARS)}),dp;']
    ideal_text = ",".join(generators) if generators else "0"
    lines = head + [
        f"ideal zzI={ideal_text};",
        "ideal zzG=std(zzI);",
        f"poly zzg={activity};",
        '"RAW_DIM "+string(dim(zzG));',
        '"RAW_GSIZE "+string(size(zzG));',
    ]
    for power in range(1, max_power + 1):
        lines.append(
            f'"MEM {power} "+string(reduce(zzg^{power},zzG)==0);')
    lines += [
        "list zzL=sat(zzI,zzg);",
        "ideal zzA=std(zzL[1]);",
        '"ACTIVE_DIM "+string(dim(zzA));',
        '"ACTIVE_UNIT "+string(size(zzA)==1 && zzA[1]==1);',
    ]
    if associated and generators:
        lines += [
            "list zzP=minAssGTZ(zzI);",
            '"NASS "+string(size(zzP));',
            "for (int zzi=1;zzi<=size(zzP);zzi++) {",
            " ideal zzQ=std(zzP[zzi]);",
            ' "ASS "+string(zzi)+" "+string(dim(zzQ))+" "+string(size(zzQ));',
            ' "BEGIN_ASS "+string(zzi);',
            " zzQ;",
            ' "END_ASS "+string(zzi);',
            "}",
        ]
    script = "\n".join(lines)
    core.no_shadow_guard(script, set(KVARS))
    output = core.run_singular(script, timeout=timeout)
    parsed = {"memberships": {}}
    active_associated = None
    for line in output.splitlines():
        fields = line.strip().split()
        if not fields:
            continue
        if fields[0] == "BEGIN_ASS":
            active_associated = int(fields[1])
            continue
        if fields[0] == "END_ASS":
            require(active_associated == int(fields[1]), fields)
            active_associated = None
            continue
        if active_associated is not None:
            parsed.setdefault("associated_generators", {}).setdefault(
                active_associated, []).append(line.strip())
            continue
        if fields[0] == "MEM":
            parsed["memberships"][int(fields[1])] = bool(int(fields[2]))
        elif fields[0] in {"RAW_DIM", "RAW_GSIZE",
                           "ACTIVE_DIM", "ACTIVE_UNIT", "NASS"}:
            parsed[fields[0].lower()] = int(fields[1])
        elif fields[0] == "ASS":
            parsed.setdefault("associated", []).append({
                "index": int(fields[1]), "affine_dim": int(fields[2]),
                "projective_dim": int(fields[2]) - 1,
                "basis_size": int(fields[3]),
            })
    require(set(parsed["memberships"]) == set(range(1, max_power + 1)),
            (pair, parsed, output[-1000:]))
    if "associated_generators" in parsed:
        for record in parsed.get("associated", []):
            record["generators"] = parsed["associated_generators"].get(
                record["index"], [])
        parsed.pop("associated_generators")
    parsed.update({
        "n": n,
        "pair": list(pair),
        "source_denominator_scale": scale,
        "error_degree": len(residual) // 2,
        "nonzero_error_generators": len(generators),
        "projective_base_dimension": parsed["raw_dim"] - 1,
        "least_activity_power_in_ideal": next(
            (power for power, yes in parsed["memberships"].items() if yes),
            None),
        "active_open_nonempty": not bool(parsed["active_unit"]),
        "activity_degree": 4,
    })
    return parsed


def main():
    mutate = "--mutate-w25-power" in sys.argv
    # The n=4 error is the empty sum by definition, so its ideal is zero.
    n4 = {
        "n": 4,
        "pair": [0, 1],
        "error_degree": 1,
        "nonzero_error_generators": 0,
        "projective_base_dimension": 8,
        "projective_base_locus": "all P^8",
        "active_open_nonempty": True,
        "least_activity_power_in_ideal": None,
    }
    phased = singular_profile(phased_n6_source(), (0, 1), associated=True)
    w25 = singular_profile(load_w25(), (0, 4), associated=True)
    w40 = singular_profile(load_w40(), (6, 7), associated=False)

    require(phased["active_open_nonempty"] in (True, False), phased)
    require(not w25["active_open_nonempty"], w25)
    observed_power = w25["least_activity_power_in_ideal"]
    claimed_power = (observed_power + 1) if mutate else observed_power
    require(claimed_power == observed_power and observed_power is not None,
            ("hostile W25 power mutation", claimed_power, w25))
    require(w40["active_open_nonempty"], w40)

    payload = {
        "controls": {
            "n4_exact_ghz": n4,
            "phased_n6_non_ghz": phased,
            "w25_n8_allblocked_x3_pair04": w25,
            "w40_n8_active_x4_pair67": w40,
        },
        "block_normality_test": (
            "At n4 and phased n6 every star and triangle map is injective, "
            "so the block-normal equations have zero polynomial content. "
            "They cannot impose a nonzero scalar contraction or syzygy of E "
            "in degree <=6 (indeed, in any degree) on that open chart."
        ),
        "terminal_verdict": (
            "The cap ideal correctly separates active and blocked controls, "
            "but minimum block-normality supplies no universal low-degree "
            "identity. Any forcing argument must use the GHZ mixed rows, not "
            "the intrinsic projective error ideal plus normality alone."
        ),
    }
    logical = json.dumps(payload, sort_keys=True, default=str,
                         separators=(",", ":"))
    print(json.dumps({"logical_sha256": sha256(logical.encode()).hexdigest(),
                      **payload}, sort_keys=True, indent=2, default=str))


if __name__ == "__main__":
    main()
