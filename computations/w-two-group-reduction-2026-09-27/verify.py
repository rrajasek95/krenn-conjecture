#!/usr/bin/env python3
"""Replay exact two-group W bounds and the certified finite catalog."""

from pathlib import Path
import hashlib
import json
import two_group as T

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for name, digest in dependencies.items():
        T.require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                  "Pinned dependency: " + name)
    catalog = T.certificate_catalog()
    T.require(catalog == json.loads((HERE / "certificates.json").read_text()),
              "Saved finite-range certificates match exact reconstruction")
    T.require((catalog["splits"], catalog["branches"], catalog["maximum_sites"])
              == (171, 615, 40), "Complete stated catalog")
    result = dict(
        status="PASS",
        evidence_status="Written proof with exact supporting checks; independent audit pending",
        checks=dict(reductions=T.check_reductions(),
                    two_site_all_even_gap=T.check_two_site_tail(),
                    finite_catalog={k: v for k, v in catalog.items() if k != "catalog"}),
        dependencies=dependencies,
        conclusions=[
            "Every two-group scalar cancellation branch reduces to a positive variable and a sextic stationary equation",
            "For a two-site smaller group, every colored exact-W rate is strictly below (5/6) R_star at every even n>=6",
            "For every even 6<=n<=40, R_star is the attained optimum among all two-group ground sources",
            "Every proper split in that finite range has exact-W rate strictly below (80/81) R_star"],
        limitations=[
            "Unrestricted global W optimum remains open",
            "The finite catalog is not an all-size theorem for arbitrary unequal splits",
            "The ground weights are constant on the two groups and across them, up to site phases",
            "Optimizing scalar response does not certify feasibility of the minimum-row colored completion"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths += [ROOT / "notes/w-state-two-group-reduction-2026-09-27.md"]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
