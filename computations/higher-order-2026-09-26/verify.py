#!/usr/bin/env python3
"""Replay exact support for the new written theorems; no assertion-only gates."""
import hashlib
import json
from pathlib import Path
from shared import ROOT, require
import critical
import w_connected

HERE = Path(__file__).resolve().parent


def main():
    dependencies = json.loads((HERE/'dependencies.json').read_text())
    for relative, expected in dependencies.items():
        require(hashlib.sha256((ROOT/relative).read_bytes()).hexdigest() == expected,
                'Pinned dependency unchanged: '+relative)
    result = dict(status='PASS', evidence_status='Written proofs with exact supporting checks; independent audit pending',
                  critical_core=critical.verify(), W_state=w_connected.verify(), dependencies=dependencies,
                  open_questions=['Unrestricted complex square-root rate law',
                                  'Fourth and higher order GHZ approaches to the critical core',
                                  'Disconnected two-root W cofactor graphs at eight or more sites',
                                  'W-state optimality for arbitrary colored cores'])
    files = sorted(p for p in HERE.iterdir() if p.suffix in ('.py', '.json', '.md') and p.name != 'results.json')
    files += [ROOT/'notes'/name for name in ('critical-core-higher-jets-2026-09-26.md',
                                           'two-root-w-connected-reduction-2026-09-26.md')]
    result['sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
