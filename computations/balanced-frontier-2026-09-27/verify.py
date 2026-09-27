#!/usr/bin/env python3
"""Replay exact support; exploratory optimization is not an acceptance input."""
from pathlib import Path
import hashlib,json
import triangle,w_response

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def main():
    dependencies=json.loads((HERE/'dependencies.json').read_text())
    for name,expected in dependencies.items():
        triangle.require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,'Pinned dependency: '+name)
    result=dict(status='PASS',evidence_status='Written proofs and exact checks; independent audit pending',
                triangle_classification=triangle.check(),unrestricted_W_response=w_response.check(),dependencies=dependencies,
                unresolved=['Unrestricted GHZ square-root rate law','Scalar six-site W threshold 520/9','Global unrestricted W optimum'])
    files=[p for p in HERE.iterdir() if p.suffix in ('.py','.md','.json') and p.name not in ('results.json','exploration.json')]
    files += [ROOT/'notes'/name for name in ('triangle-response-rank-classification-2026-09-27.md','w-state-unrestricted-response-bound-2026-09-27.md','w-state-no-ground-matching-optimum-2026-09-27.md')]
    result['sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
