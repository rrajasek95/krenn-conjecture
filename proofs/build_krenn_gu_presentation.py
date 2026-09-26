#!/usr/bin/env python3
"""Build the GitHub math rendering and PDF without changing the audited proof.

The TeX body intentionally uses a small explicit subset, so the Markdown
conversion preserves every displayed formula instead of using a lossy parser.
"""
from pathlib import Path
import hashlib
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PROOFS = ROOT / 'proofs'
ORIGINAL = PROOFS / 'krenn-gu-all-orders-two-replica-proof.md'
EXPECTED_ORIGINAL = 'fb0fa1e9447d8044981692d6e9bbbeff8e6a2cfc90119b6a296cbf506b9a3c9d'
TEX = PROOFS / 'krenn-gu-all-orders-two-replica.tex'
MARKDOWN = PROOFS / 'krenn-gu-all-orders-two-replica-latex.md'
PDF = PROOFS / 'krenn-gu-all-orders-two-replica.pdf'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def markdown_body(source):
    body = source.split('% BEGIN_GITHUB_BODY\n', 1)[1].split('% END_GITHUB_BODY', 1)[0]
    references = {}
    section = 0
    theorem = 0
    lines = []
    for line in body.splitlines():
        match = re.fullmatch(r'\\section\{([^{}]+)\}\\label\{([^{}]+)\}', line)
        if match:
            section += 1
            theorem = 0
            references[match[2]] = str(section)
            lines.append(f'## {section}. {match[1]}')
            continue
        match = re.fullmatch(r'\\begin\{(theorem|lemma|corollary)\}\[([^\]]+)\]\\label\{([^{}]+)\}', line)
        if match:
            theorem += 1
            number = f'{section}.{theorem}'
            references[match[3]] = number
            lines.append(f'**{match[1].capitalize()} {number} ({match[2]}).**')
            continue
        match = re.fullmatch(r'\\begin\{proof\}(?:\[([^\]]+)\])?', line)
        if match:
            lines.append('**'+(match[1] or 'Proof')+'.**')
            continue
        if re.fullmatch(r'\\end\{(?:theorem|lemma|corollary)\}', line):
            continue
        if line == r'\end{proof}':
            lines.append(r'$\square$')
            continue
        for match in re.finditer(r'\\tag\{([^{}]+)\}\\label\{([^{}]+)\}', line):
            references[match[2]] = match[1]
        lines.append(line)
    text = '\n'.join(lines)
    text = re.sub(r'\\eqref\{([^{}]+)\}', lambda m: '('+references[m[1]]+')', text)
    text = re.sub(r'\\ref\{([^{}]+)\}', lambda m: references[m[1]], text)
    text = re.sub(r'\\label\{[^{}]+\}', '', text)
    text = re.sub(r'\\href\{([^{}]+)\}\{([^{}]+)\}', r'[\2](\1)', text)
    text = re.sub(r'\\textbf\{([^{}]+)\}', r'**\1**', text)
    text = re.sub(r'\\emph\{([^{}]+)\}', r'*\1*', text)
    text = text.replace(r'\begin{equation}', '$$').replace(r'\end{equation}', '$$')
    text = text.replace(r'\[', '$$').replace(r'\]', '$$')
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.S)
    text = text.replace('~', ' ')
    text = text.replace('--', '–')
    text = re.sub(r'\n{3,}', '\n\n', text)
    display = False
    spaced = []
    for line in text.splitlines():
        if line.strip() == '$$':
            if not display and spaced and spaced[-1] != '':
                spaced.append('')
            spaced.append('$$')
            if display:
                spaced.append('')
            display = not display
        else:
            spaced.append(line)
    assert not display, 'Unclosed GitHub display math'
    text = '\n'.join(spaced)
    text = re.sub(r'\n{3,}', '\n\n', text)
    for forbidden in [r'\section', r'\label', r'\eqref', r'\ref{',
                      r'\begin{theorem}', r'\begin{lemma}', r'\begin{proof}']:
        assert forbidden not in text, forbidden
    title = '# An all-orders two-replica proof of the complex weighted Krenn–Gu conjecture\n\n'
    links = ('[PDF](krenn-gu-all-orders-two-replica.pdf) · '
             '[LaTeX source](krenn-gu-all-orders-two-replica.tex) · '
             '[Audited source](krenn-gu-all-orders-two-replica-proof.md)\n\n')
    return title+links+text.strip()+'\n'


def main():
    assert digest(ORIGINAL) == EXPECTED_ORIGINAL, 'Audited source hash changed'
    MARKDOWN.write_text(markdown_body(TEX.read_text()), encoding='utf-8')
    executable = shutil.which('tectonic')
    if not executable:
        raise RuntimeError('tectonic is required to render the PDF')
    subprocess.run([executable, '--only-cached', '--keep-logs',
                    '--outdir', str(PROOFS), str(TEX)],
                   cwd=ROOT, check=True)
    assert PDF.exists() and PDF.stat().st_size > 1000
    log = TEX.with_suffix('.log')
    problems = [line for line in log.read_text().splitlines()
                if any(flag in line for flag in
                       ['LaTeX Warning', 'Package hyperref Warning',
                        'Overfull', 'Underfull', 'Undefined control sequence'])]
    assert not problems, '\n'.join(problems)
    log.unlink()  # Remove only this build's checked temporary log.
    print('TeX references and layout: no warnings')
    assert digest(ORIGINAL) == EXPECTED_ORIGINAL, 'Audited source changed during build'
    for path in [TEX, MARKDOWN, PDF]:
        print(f'{path.relative_to(ROOT)}  {digest(path)}  {path.stat().st_size} bytes')


if __name__ == '__main__':
    main()
