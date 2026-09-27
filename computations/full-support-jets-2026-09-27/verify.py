#!/usr/bin/env python3
"""Replay exact support for the full-support jet and W-shear proofs."""
from pathlib import Path
import hashlib,json
import jets,shears

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def main():
    dependencies=json.loads((HERE/'dependencies.json').read_text())
    for name,expected in dependencies.items():
        jets.require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,'Pinned dependency: '+name)
    result=dict(status='PASS',evidence_status='Written proofs with exact checks; independent audit pending',
                jets=jets.check(),shears=shears.check(),dependencies=dependencies,
                unresolved=['Unrestricted GHZ square-root rate law','Global unrestricted W optimum'])
    files=[p for p in HERE.iterdir() if p.suffix in ('.py','.md','.json') and p.name!='results.json']
    files += [ROOT/'notes'/name for name in ('full-support-single-color-jets-2026-09-27.md','w-state-shear-normalization-obstruction-2026-09-27.md')]
    result['sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
