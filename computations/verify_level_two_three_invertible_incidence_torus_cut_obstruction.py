#!/usr/bin/env python3
"""Exact factored-L0 obstruction on a 4-parameter 3I incidence torus.

Start with the exact 3I+1R+2Z incidence survivor and independently rescale
the two binary colours at each zero-star site 4 and 5.  The resulting four
nonzero parameters act only on the eight zero-multiplier cut blocks.

The checker proves the monomial identities

    Psi(M^h) = R Psi(M),        D^h = R D C^{-1},

term by term over the Laurent ring.  Thus rank 55/53 and both pure-target
incidences persist on the whole torus.  For the pure-zero factored-L0 cut
screen, the transformed matrix is obtained from the base cut matrix by
invertible row/column scaling and an invertible rescaling of all six gauge
variables.  The base cubic minors generate (1) over Q and F_32003, so they
generate (1) throughout the Laurent family.

Research evidence only.  This is a scoped obstruction on a four-parameter
subfamily, not a classification of the full incidence locus.  Singular is
the sole non-standard-library dependency.
"""

from itertools import product
from pathlib import Path
from runpy import run_path
from shutil import which
import subprocess


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "verify_level_two_three_invertible_l0_incidence_survivor.py"
CUT_SOURCE = (
    HERE / "verify_level_two_two_invertible_factored_l0_cut_obstruction.py"
)
source = run_path(str(SOURCE))
cut_core = run_path(str(CUT_SOURCE))

guard = source["guard"]
M = source["M"]
SITES = tuple(range(6))
COLOURS = (0, 1)
WORDS = tuple(product(COLOURS, repeat=6))
ZERO_SITES = (4, 5)
FREE_EDGES = frozenset(
    (u, v) for u in range(4) for v in ZERO_SITES
)
PARAMETERS = ("a0", "a1", "b0", "b1")
ZERO_EXPONENT = (0, 0, 0, 0)


def add_exp(*terms):
    return tuple(sum(term[index] for term in terms)
                 for index in range(len(PARAMETERS)))


def subtract_exp(left, right):
    return tuple(a - b for a, b in zip(left, right))


def weight_exp(site, colour):
    if site == 4:
        return tuple(int(index == colour) for index in range(4))
    if site == 5:
        return tuple(int(index == colour + 2) for index in range(4))
    return ZERO_EXPONENT


def cell_exp(u, v, a, b):
    return add_exp(weight_exp(u, a), weight_exp(v, b))


def row_exp(word):
    return add_exp(*(weight_exp(site, word[site]) for site in SITES))


def audit_base_candidate():
    changed = source["audit_replacement_scope"]()
    guard_slope = guard["audit_generic_kernel_equation"]()
    differential_ranks = guard["audit_rank_55"]()
    r2_tables = guard["audit_literal_r2"]()
    formal_slices, slope, incidence_ranks = source["audit_l0_incidence"]()
    require(slope == guard_slope, "base slope audits disagree")
    require(changed == frozenset(((3, 4, 1, 0),)),
            ("base specialization changed", changed))
    return (
        differential_ranks, len(r2_tables), formal_slices,
        incidence_ranks,
    )


def audit_torus_scope():
    require(PARAMETERS == ("a0", "a1", "b0", "b1"),
            "torus parameter order changed")
    require(M[3, 4, 0, 0] == 12 and M[3, 4, 1, 0] == 0,
            "the incidence-survivor base block changed")
    require(all(
        guard["RHO"][u] + guard["RHO"][v] == 0
        for u, v in FREE_EDGES
    ), "a rescaled cut block has nonzero generic-kernel multiplier")

    acted_nonzero = []
    for u, v, a, b in guard["CELLS"]:
        exponent = cell_exp(u, v, a, b)
        if exponent == ZERO_EXPONENT or M[u, v, a, b] == 0:
            continue
        require((u, v) in FREE_EDGES,
                ("the torus changes a determined nonzero cell", u, v, a, b))
        acted_nonzero.append((u, v, a, b))

    # At the identity all four parameters equal one.  Since every parameter
    # is a unit, multiplication by its monomial preserves the complete zero
    # pattern, hence every pure-column R2 witness audited at the base point.
    require(set(parameter for exponent in (
        cell_exp(u, v, a, b) for u, v, a, b in acted_nonzero
    ) for parameter, power in zip(PARAMETERS, exponent) if power)
            == set(PARAMETERS),
            "a declared torus parameter acts trivially")
    return len(acted_nonzero)


def audit_matching_monomials():
    full_checks = 0
    cofactor_checks = 0
    for word in WORDS:
        output_exponent = row_exp(word)
        for matching in guard["MATCHINGS"][SITES]:
            exponent = add_exp(*(
                cell_exp(u, v, word[u], word[v]) for u, v in matching
            ))
            require(exponent == output_exponent,
                    ("matching monomial identity failed", word, matching))
            full_checks += 1

        for u, v in guard["EDGES"]:
            remaining = tuple(
                site for site in SITES if site not in (u, v)
            )
            expected = subtract_exp(
                output_exponent,
                cell_exp(u, v, word[u], word[v]),
            )
            for matching in guard["MATCHINGS"][remaining]:
                exponent = add_exp(*(
                    cell_exp(r, s, word[r], word[s])
                    for r, s in matching
                ))
                require(exponent == expected,
                        ("cofactor monomial identity failed",
                         word, u, v, matching))
                cofactor_checks += 1

    require((full_checks, cofactor_checks) == (960, 2_880),
            "matching-monomial check count changed")
    return full_checks, cofactor_checks


def audit_pure_preimage_and_cut_transform(preimage):
    pure_zero_exponent = row_exp((0,) * 6)
    require(pure_zero_exponent == (1, 0, 1, 0),
            "pure-zero output monomial changed")

    # If D K=e0, then K^h_cell=C_cell*K_cell/R_0 satisfies D^h K^h=e0:
    # every summand in output row x has exponent R_x-C+C-R_0=R_x-R_0.
    preimage_checks = 0
    for word in WORDS:
        expected = subtract_exp(row_exp(word), pure_zero_exponent)
        for u, v, a, b in guard["CELLS"]:
            if (word[u], word[v]) != (a, b):
                continue
            transformed = add_exp(
                subtract_exp(row_exp(word), cell_exp(u, v, a, b)),
                subtract_exp(cell_exp(u, v, a, b), pure_zero_exponent),
            )
            require(transformed == expected,
                    ("transformed preimage exponent failed", word, u, v, a, b))
            preimage_checks += 1

    # On the cut {0,1}|{2,3,4,5}, C_cell splits into a row and a column
    # monomial.  After extracting C_cell/R_0, the gauge term is the base
    # term with the invertible substitution lambda_i=R_0*mu_i.
    cut_checks = 0
    for r in cut_core["LEFT"]:
        for a in COLOURS:
            for u in cut_core["RIGHT"]:
                for b in COLOURS:
                    split = add_exp(weight_exp(r, a), weight_exp(u, b))
                    require(split == cell_exp(r, u, a, b),
                            ("cut monomial does not split", r, u, a, b))
                    gauge_after_factoring = subtract_exp(
                        cell_exp(r, u, a, b),
                        subtract_exp(cell_exp(r, u, a, b),
                                     pure_zero_exponent),
                    )
                    require(gauge_after_factoring == pure_zero_exponent,
                            ("gauge-variable rescaling changed", r, u, a, b))
                    cut_checks += 1

    require(preimage_checks == 960,
            ("preimage transform check count changed", preimage_checks))
    require(cut_checks == 32,
            ("cut transform check count changed", cut_checks))
    return preimage_checks, cut_checks, sum(value != 0 for value in preimage)


def audit_base_cut_unit_ideal():
    cut_source = {"core": guard, "guard": guard, "M": M}
    cut, preimage = cut_core["build_cut_matrix"](cut_source)
    transform_counts = audit_pure_preimage_and_cut_transform(preimage)

    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    version = subprocess.run(
        (executable, "--version"),
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )
    require(version.returncode == 0
            and "Singular" in version.stdout + version.stderr,
            "could not identify the Singular executable")
    q_payload = cut_core["audit_unit_ideal"](executable, 0, cut, "Q")
    fp_payload = cut_core["audit_unit_ideal"](
        executable, 32_003, cut, "F32003"
    )
    return transform_counts, q_payload, fp_payload


def main():
    base = audit_base_candidate()
    acted = audit_torus_scope()
    monomial_checks = audit_matching_monomials()
    transform, q_payload, fp_payload = audit_base_cut_unit_ideal()
    print("three-invertible incidence-torus cut obstruction: all checks passed")
    print("  exact family             : 4-parameter colour torus at sites 4,5")
    print(f"  acted nonzero cells      : {acted}/32 zero-multiplier cells")
    print(f"  matching exponent checks : {monomial_checks[0]}+{monomial_checks[1]}")
    print(f"  base ranks/R2/slices     : {base}")
    print(f"  preimage/cut transforms  : {transform}")
    print(f"  base cut ideals Q/F32003 : {q_payload}, {fp_payload}")
    print("  torus cut ideal          : (1) after Laurent base change")
    print("  scope                    : four-dimensional subfamily only")


if __name__ == "__main__":
    main()
