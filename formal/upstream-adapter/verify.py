#!/usr/bin/env python3
"""Check the literal adapter against a fixed formal-conjectures checkout."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
LOCAL = ROOT.parent / "all-orders"
REVISION = "e2c4441f9545b85790aebcfaa445e194fcab9d5b"
UPSTREAM_SOURCE = "FormalConjectures/Paper/MonochromaticQuantumGraph.lean"


def run(args: list[str], cwd: Path, env=None) -> str:
    result = subprocess.run(args, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        print(result.stdout, end="")
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(args)}")
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True,
                        help=f"formal-conjectures checkout at {REVISION}")
    args = parser.parse_args()
    upstream = args.upstream.resolve()
    revision = run(["git", "rev-parse", "HEAD"], upstream).strip()
    if revision != REVISION:
        raise RuntimeError(f"Expected upstream commit {REVISION}, got {revision}")
    run(["git", "diff", "--exit-code", REVISION, "--", UPSTREAM_SOURCE,
         "lakefile.toml", "lake-manifest.json", "lean-toolchain"], upstream)
    print(run(["lake", "--wfail", "build"], LOCAL), end="")
    print(run(["lake", "--wfail", "build",
               "FormalConjectures.Paper.MonochromaticQuantumGraph"], upstream), end="")
    env = os.environ.copy()
    env["LEAN_PATH"] = str(LOCAL / ".lake/build/lib/lean") + (
        os.pathsep + env["LEAN_PATH"] if env.get("LEAN_PATH") else "")
    source = ROOT / "UpstreamAdapter.lean"
    output = run(["lake", "env", "lean", "-DwarningAsError=true", str(source)], upstream, env)
    spec = importlib.util.spec_from_file_location("local_verify", LOCAL / "verify.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    declarations = module.audit(output, source.read_text())
    (ROOT / "axioms.txt").write_text(output)
    metadata = {
        "status": "PASS",
        "upstream_repository": "https://github.com/rrajasek95/formal-conjectures",
        "upstream_revision": REVISION,
        "upstream_source": UPSTREAM_SOURCE,
        "upstream_source_sha256": hashlib.sha256((upstream / UPSTREAM_SOURCE).read_bytes()).hexdigest(),
        "adapter_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "matching_model_sha256": hashlib.sha256((LOCAL / "MatchingModel.lean").read_bytes()).hexdigest(),
        "declarations_checked": len(declarations),
        "checked_declarations": declarations,
        "allowed_axioms": sorted(module.ALLOWED),
        "scope": "Exact equivalence of local and upstream solutions; no nonexistence theorem is asserted.",
    }
    (ROOT / "verification.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"PASS: literal upstream adapter; {len(declarations)} declarations axiom-checked.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError) as error:
        (ROOT / "verification.json").write_text(json.dumps({
            "status": "FAIL", "error": str(error)
        }, indent=2) + "\n")
        print(error, file=sys.stderr)
        sys.exit(1)
