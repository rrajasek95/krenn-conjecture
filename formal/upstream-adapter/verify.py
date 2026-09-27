#!/usr/bin/env python3
"""Check the full proof against the exact pinned formal-conjectures definitions."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
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
    spec = importlib.util.spec_from_file_location("local_verify", LOCAL / "verify.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sources = [ROOT / name for name in
               ["UpstreamAdapter.lean", "FullProof.lean", "FullProofAxioms.lean",
                "RealCorollaries.lean", "RealCorollariesAxioms.lean"]]
    for source in sources:
        if re.search(r"\bsorry\b|\badmit\b|^\s*(?:axiom|unsafe)\b",
                     module.without_comments(source.read_text()), re.MULTILINE):
            raise RuntimeError(f"Unaccepted proof construct in {source.name}")
    adapter_lib = ROOT / ".lake/build/lib/lean"
    adapter_lib.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    paths = [str(adapter_lib), str(LOCAL / ".lake/build/lib/lean")]
    if env.get("LEAN_PATH"):
        paths.append(env["LEAN_PATH"])
    env["LEAN_PATH"] = os.pathsep.join(paths)
    lean = ["lake", "env", "lean", "-DwarningAsError=true", "--root", str(ROOT)]
    adapter_output = run(lean + ["-o", str(adapter_lib / "UpstreamAdapter.olean"),
                                str(sources[0])], upstream, env)
    run(lean + ["-o", str(adapter_lib / "FullProof.olean"), str(sources[1])], upstream, env)
    proof_output = run(lean + [str(sources[2])], upstream, env)
    run(lean + ["-o", str(adapter_lib / "RealCorollaries.olean"), str(sources[3])], upstream, env)
    real_output = run(lean + [str(sources[4])], upstream, env)
    declarations = module.audit(adapter_output, sources[0].read_text())
    declarations += module.audit(proof_output, sources[2].read_text())
    declarations += module.audit(real_output, sources[4].read_text())
    output = adapter_output + proof_output + real_output
    (ROOT / "axioms.txt").write_text(output)
    metadata = {
        "status": "PASS",
        "upstream_repository": "https://github.com/rrajasek95/formal-conjectures",
        "upstream_revision": REVISION,
        "upstream_source": UPSTREAM_SOURCE,
        "upstream_source_sha256": hashlib.sha256((upstream / UPSTREAM_SOURCE).read_bytes()).hexdigest(),
        "source_hashes": {source.name: hashlib.sha256(source.read_bytes()).hexdigest()
                          for source in sources},
        "matching_model_sha256": hashlib.sha256((LOCAL / "MatchingModel.lean").read_bytes()).hexdigest(),
        "declarations_checked": len(declarations),
        "checked_declarations": declarations,
        "allowed_axioms": sorted(module.ALLOWED),
        "scope": "Full complex and real nonexistence for every even N >= 6 and D >= 3, including the exact upstream real special cases, using the exact upstream definitions.",
    }
    (ROOT / "verification.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"PASS: exact upstream all-orders theorem; {len(declarations)} declarations axiom-checked.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError) as error:
        (ROOT / "verification.json").write_text(json.dumps({
            "status": "FAIL", "error": str(error)
        }, indent=2) + "\n")
        print(error, file=sys.stderr)
        sys.exit(1)
