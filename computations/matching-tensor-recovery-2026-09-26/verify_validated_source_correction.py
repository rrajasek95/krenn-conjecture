"""Replay the global input chain and certify saved binary64 correction outputs.

Normal residuals are assembled directly from complementary matching tensors,
separately from the generator's dense Jacobian multiplication.
"""

import hashlib
import itertools
import json
import sys
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import covariance_noise_certificate as bounds
import validated_source_correction as correction
import verify_composed_shared_source_noise as shared_audit
from flint import fmpz_mat
from verify_shared_source_noise import audit_derivative, independent_tensor


def independent_forward(means, edges, forward):
    values = []
    for mu in means:
        values.extend(independent_tensor(mu, edges, tuple(range(len(mu)))))
    assert values == forward


def gradient_auditor(context):
    n, size = len(context["means"][0]), 3 ** len(context["means"][0])
    powers = [3**i for i in reversed(range(n))]
    denominator = context["matrix_denominator"]

    @lru_cache(None)
    def complementary(setting, sites):
        entries = independent_tensor(context["means"][setting], context["edges"], sites)
        scaled = [F(x) * denominator for x in entries]
        assert all(x.denominator == 1 for x in scaled)
        return [int(x) for x in scaled]

    terms = []
    for key in context["keys"]:
        if key[0] == "mu":
            _, setting, site, colour = key
            settings, fixed = [setting], {site: colour}
        else:
            _, i, j, a, b = key
            settings, fixed = range(len(context["means"])), {i: a, j: b}
        sites = tuple(i for i in range(n) if i not in fixed)
        offset = sum(powers[i] * a for i, a in fixed.items())
        indices = [
            offset + sum(powers[i] * a for i, a in zip(sites, word))
            for word in itertools.product(range(3), repeat=len(sites))
        ]
        terms.append(
            [
                (s * size + index, coefficient)
                for s in settings
                for index, coefficient in zip(indices, complementary(s, sites))
            ]
        )
    p = [[int(x) for x in row] for row in context["preconditioner"].tolist()]
    scale = context["preconditioner_scale"]
    normal_checks = []
    original = correction.projected_step_bound

    def checked(ctx, residual):
        assert ctx is context
        result = original(ctx, residual)
        integers, residual_denominator = bounds.common(residual)
        gradient = [
            sum(coefficient * integers[index] for index, coefficient in column)
            for column in terms
        ]
        whitened = [
            sum(p[j][i] * gradient[j] for j in range(len(p))) for i in range(len(p))
        ]
        approximate = [
            sum(p[i][j] * whitened[j] for j in range(len(p))) for i in range(len(p))
        ]
        total_den = denominator * residual_denominator * scale
        assert result[1] == F(sum(x * x for x in whitened), total_den**2)
        assert result[2] == F(sum(x * x for x in approximate), (total_den * scale) ** 2)
        normal_checks.append(True)
        return result

    return checked, normal_checks


def exact_rectangular_examples():
    """Nonzero preconditioner defect, compared with an analytic pseudoinverse."""
    context = {
        "matrix": fmpz_mat([[1, 0], [0, 2], [1, 1]]),
        "matrix_denominator": 1,
        "preconditioner": fmpz_mat([[1, 0], [0, 1]]),
        "preconditioner_scale": 2,
        "preconditioner_norm": bounds.upper_sqrt(F(1, 2)),
        "gram_error": bounds.upper_sqrt(F(7, 16)),
    }
    cases = 0
    for residual in itertools.product([-2, 0, 3], repeat=3):
        step, _, approximate_squared, defect = correction.projected_step_bound(
            context, residual
        )
        a, b, c = residual
        exact = [F(5 * a - 2 * b + 4 * c, 9), F(-a + 4 * b + c, 9)]
        approximate = [F(a + c, 4), F(2 * b + c, 4)]
        assert sum(x * x for x in exact) <= step**2
        assert sum((x - y) ** 2 for x, y in zip(exact, approximate)) <= defect**2
        assert approximate_squared == sum(x * x for x in approximate)
        cases += 1
    return {
        "residual_cases": cases,
        "analytic_pseudoinverse_checked": True,
        "nonzero_gram_defect_checked": True,
    }


def run():
    root = Path(__file__).parent
    saved = json.loads(
        (root / "validated-source-correction-certificate.json").read_text()
    )
    source_path = root / saved["source_certificate"]["file"]
    assert (
        hashlib.sha256(source_path.read_bytes()).hexdigest()
        == saved["source_certificate"]["sha256"]
    )
    print(
        "Replaying the complete shared-source input chain", file=sys.stderr, flush=True
    )
    replay = shared_audit.run()
    assert replay == json.loads(
        (root / "composed-shared-source-audit.json").read_text()
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("Correction replay attempted a numerical solve")

    correction.solve = forbidden
    context = correction.load_context(audit_derivative=audit_derivative)
    small_cases = exact_rectangular_examples()
    checked, checks = gradient_auditor(context)
    correction.projected_step_bound = checked
    print(
        "Checking corrected tensors and complementary-matching normal residuals",
        file=sys.stderr,
        flush=True,
    )
    rebuilt = correction.certify_outputs(
        context, saved["numerical_outputs"], audit_forward=independent_forward
    )
    assert rebuilt == saved["certificate"]
    assert len(checks) == 1 + len(saved["numerical_outputs"])
    invalid = list(context["center"])
    invalid[0] += 1
    try:
        correction.inspect_output(context, invalid)
    except AssertionError as error:
        assert str(error) == "Output lies outside the certified common ball"
    else:
        raise AssertionError("An output outside the certified ball was accepted")
    selected = saved["numerical_outputs"][rebuilt["selected_output_index"]]
    values = [F(float.fromhex(x)) for x in selected["parameter_hex"]]
    assert any(x != y for x, y in zip(values, context["center"]))
    source_error2 = sum((x - y) ** 2 for x, y in zip(values, context["center"]))
    selected_bound = rebuilt["output_checks"][rebuilt["selected_output_index"]]
    assert source_error2 <= F(selected_bound["global_source_error_bound"]) ** 2
    matrix = context["matrix"]
    null_residual = [F(0)] * matrix.nrows()
    assert correction.projected_step_bound(context, null_residual)[0] == 0
    return {
        "global_shared_source_input_chain_replayed": True,
        "saved_binary64_outputs_replayed_without_numerical_solve": True,
        "all_reference_derivative_entries_checked_separately": True,
        "all_corrected_tensors_checked_by_scalar_matching_recursion": True,
        "normal_residuals_checked_via_complementary_matchings": len(checks) - 1,
        "rectangular_preconditioner_examples": small_cases,
        "zero_normal_residual_has_zero_correction_bound": True,
        "output_outside_certified_ball_rejected": True,
        "selected_output_is_nontrivial": True,
        "selected_output_error_relative_to_synthetic_center_squared": str(
            source_error2
        ),
        "scope": "Exact a posteriori replay of numerical output values, with separate matching and normal-residual constructions. Shares bound propagation and arithmetic libraries; not a proof of the floating trajectory or an independent mathematical review.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
