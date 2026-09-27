"""Four blind source proposals, exact single-source certificates, and alignment.

Example generation and planted-source comparisons are outside the proposal and
certificate routines. Noise is below double precision; no practical threshold
or validated floating correction is claimed.
"""

import argparse
import hashlib
import json
import math
import random
import sys
from fractions import Fraction as F
from pathlib import Path

import full_source_noise_recovery as single
import shared_source_alignment as alignment
import shared_source_local_certificate as joint
import source_chart_certificate as chart
from alignment_graph_characters import exact_examples
from restricted_source_inverse import serialize_edges


def encode_edges(edges):
    return serialize_edges(
        {e: [[str(x) for x in row] for row in b] for e, b in edges.items()}
    )


def make_observation(index):
    assert index in [1, 2, 3]
    n, edges = single.source_example()
    means = [[F(1), F(0), F(0)] for _ in range(n)]
    means[index - 1][0] = F(2)
    for i, row in enumerate(means):
        if index == 1:
            row[1] = F(1, 16)
        elif index == 2:
            row[2] = F(1, 16)
        else:
            row[1], row[2] = F(i % 3 - 1, 16), F(2 * (i % 2) - 1, 16)
    clean, clean_denominator = chart.rational_tensor(means, edges)
    noise_denominator = 2**170
    denominator = math.lcm(clean_denominator, noise_denominator)
    rng = random.Random(275170 + index)
    noise = [rng.choice([-1, 1]) for _ in range(3**n)]
    observed = [
        int(x) * (denominator // clean_denominator)
        + e * (denominator // noise_denominator)
        for x, e in zip(clean.reshape(-1), noise)
    ]
    mu, cov, diagnostics = single.propose_source(observed, denominator, n)
    print(f"Observation {index}: blind candidate ready", file=sys.stderr, flush=True)
    certificate = chart.certify(
        observed, denominator, F(47, noise_denominator), mu, cov
    )
    # Only now compare against the source used to construct the example.
    scales = [1 / row[0] for row in means[:-1]]
    scales.append(1 / math.prod(scales))
    assert mu == [[x * scales[i] for x in row] for i, row in enumerate(means)]
    assert all(
        cov[i, j] == [[x * scales[i] * scales[j] for x in row] for row in b]
        for (i, j), b in edges.items()
    )
    print(
        f"Observation {index}: global certificate passed", file=sys.stderr, flush=True
    )
    return {
        "sites": n,
        "observed_numerators": list(map(str, observed)),
        "observed_denominator": str(denominator),
        "error_budget": str(F(47, noise_denominator)),
        "candidate_means": [[str(x) for x in row] for row in mu],
        "candidate_edges": encode_edges(cov),
        "numerical_proposal_diagnostics": diagnostics,
        "chart_certificate": certificate,
        "comparison_only": {
            "actual_means": [[str(x) for x in row] for row in means],
            "actual_edges": encode_edges(edges),
            "clean_numerators": clean.reshape(-1).tolist(),
            "clean_denominator": clean_denominator,
            "noise_numerators": noise,
            "noise_denominator": str(noise_denominator),
        },
    }


def finish(records, paths, saved_joint=None):
    means, edges, certificate = alignment.align(records)
    assert means[0] == alignment.parse_source(records[0])[0]
    for mu, record in zip(means[1:], records[1:]):
        assert mu == [
            [F(x) for x in row] for row in record["comparison_only"]["actual_means"]
        ]
    local = joint.certify(
        means, edges, records, certificate["joint_source_error_bound"], saved_joint
    )
    matrix = list(map(list, zip(*[[x for row in mu for x in row] for mu in means])))
    return {
        "sites": len(means[0]),
        "observations": [
            {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in paths
        ],
        "certificate": certificate,
        "joint_local_certificate": local,
        "refined_mean_span": alignment.full_column_span(
            matrix, F(local["refined_global_joint_error_bound"])
        ),
        "graph_character_certificates": exact_examples(),
        "limitations": [
            "Every input source bound is conditional on its stated measurement-error budget; shared-source existence is assumed.",
            "Perturbations are below double precision in this example; this is a proof-chain certificate, not a practical noise threshold.",
            "All true compatible sources are enclosed after one common product-one scaling. No latent unsampled mean directions are recovered.",
            "Not Lean formalized or independently peer reviewed.",
        ],
    }


def run(output_dir):
    base = Path(__file__).parent
    first = base / "full-source-noise-certificate.json"
    paths, records = [first], [json.loads(first.read_text())]
    for index in [1, 2, 3]:
        record = make_observation(index)
        path = output_dir / f"shared-source-observation-{index}.json"
        path.write_text(json.dumps(record, indent=2) + "\n")
        paths.append(path)
        records.append(record)
    return finish(records, paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    print(json.dumps(run(args.output_dir), indent=2))
