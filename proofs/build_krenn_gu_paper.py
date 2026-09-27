#!/usr/bin/env python3
"""Build the cited research manuscript and check references and layout."""
from pathlib import Path
import hashlib
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PROOFS = ROOT / 'proofs'
TEX = PROOFS / 'krenn-gu-all-orders-paper.tex'
ORIGINAL = PROOFS / 'krenn-gu-all-orders-two-replica-proof.md'
ORIGINAL_SHA256 = 'fb0fa1e9447d8044981692d6e9bbbeff8e6a2cfc90119b6a296cbf506b9a3c9d'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert digest(ORIGINAL) == ORIGINAL_SHA256, 'Frozen proof changed'
    source = TEX.read_text()
    entries = re.findall(r'\\bibitem\{([^{}]+)\}', source)
    assert len(entries) == len(set(entries)), 'Duplicate bibliography key'
    cited = {
        key
        for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^{}]+)\}', source)
        for key in group.split(',')
    }
    assert cited == set(entries), 'Missing or uncited bibliography entries'
    # A downloaded PDF needs absolute links to its research artifacts.
    assert all(url.startswith('https://') for url in
               re.findall(r'\\href\{([^{}]+)\}', source))
    executable = shutil.which('tectonic')
    if not executable:
        raise RuntimeError('Install Tectonic to build this manuscript')
    subprocess.run([executable, '--only-cached', '--keep-logs',
                    '--outdir', str(PROOFS), str(TEX)], cwd=ROOT, check=True)
    log = TEX.with_suffix('.log')
    problems = [line for line in log.read_text().splitlines()
                if any(flag in line for flag in
                       ['LaTeX Warning', 'Package hyperref Warning',
                        'Overfull', 'Underfull', 'Undefined control sequence'])]
    assert not problems, '\n'.join(problems)
    pdf = TEX.with_suffix('.pdf')
    assert pdf.exists() and pdf.stat().st_size > 1000
    assert digest(ORIGINAL) == ORIGINAL_SHA256, 'Frozen proof changed during build'
    log.unlink()
    print(f'{len(entries)} cited references; no citation, cross-reference, or layout warnings')
    for path in (TEX, pdf):
        print(f'{path.relative_to(ROOT)}  {digest(path)}  {path.stat().st_size} bytes')


if __name__ == '__main__':
    main()
