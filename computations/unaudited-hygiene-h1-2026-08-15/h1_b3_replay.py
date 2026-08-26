#!/usr/bin/env python3
"""H1 / BLOCKER 3 -- replay every stored UNSAT proof with drat-trim.

UNAUDITED.  Hygiene agent H1, 2026-08-15.

Targets
  (a) the 31 m=17 orbit closure proofs of the W8 template-kill lane
      (computations/unaudited-template-kill-w8-2026-08-15/certificates/
       w8_m17_closure_o*.{cnf.gz,drup.gz});
  (b) the 7 W11 replacement proofs
      (computations/unaudited-sat-pair-w11-2026-08-15/w8_reproofs/).

For every proof this records, BEFORE the replay:
  * the DRUP tail check demanded by ledger item 5 (pysat+cadical
    get_proof() truncates mid-clause): does the proof terminate in a
    well-formed empty-clause line "0"?  Does its last line end in "0"?
  * line counts, addition/deletion counts, and a RAT-step scan (ledger
    item 16: the checker's proof system must cover the solver's).

and then runs drat-trim (backward, core-first, DRAT-capable) and parses
its stdout for the "s VERIFIED" token.  Return code is NOT trusted as a
success signal.

Usage:  python3 h1_b3_replay.py <group>      group in {m17, w11}
Writes  results_b3_<group>.jsonl  (one record per proof, flushed)
"""

from __future__ import annotations

import gzip
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DRAT = os.path.join(HERE, "tools", "drat-trim", "drat-trim")
SCRATCH = os.environ.get(
    "H1_SCRATCH",
    "/private/tmp/claude-501/-Users-rishi/f8396279-dd28-41de-876d-5c03a4d8d65a/scratchpad/m17",
)
TIMEOUT = int(os.environ.get("H1_TIMEOUT", "3600"))


class CheckFailure(Exception):
    pass


def require(cond, msg):
    if not cond:
        raise CheckFailure(msg)


def _open(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path, "r")


def scan_proof(path):
    """Structural scan of a DRUP/DRAT proof.  Pure text, no semantics."""
    n_add = n_del = n_lines = 0
    empty_clause_lines = []
    last_line = ""
    truncated = False
    maxvar = 0
    with _open(path) as fh:
        for n_lines, line in enumerate(fh, 1):
            last_line = line
            s = line.strip()
            if not s:
                continue
            if s.startswith("d"):
                n_del += 1
                body = s[1:].split()
            else:
                n_add += 1
                body = s.split()
            if body and body[-1] == "0":
                if len(body) == 1 and not s.startswith("d"):
                    empty_clause_lines.append(n_lines)
                for tok in body[:-1]:
                    try:
                        maxvar = max(maxvar, abs(int(tok)))
                    except ValueError:
                        pass
    # ledger item 5: a truncated get_proof() file ends mid-clause.
    if last_line and not last_line.endswith("\n"):
        truncated = True
    if last_line.strip() and last_line.strip().split()[-1] != "0":
        truncated = True
    return dict(
        lines=n_lines,
        additions=n_add,
        deletions=n_del,
        max_var_seen=maxvar,
        empty_clause_at=empty_clause_lines,
        terminates_in_empty_clause=bool(empty_clause_lines),
        truncated_tail=truncated,
        last_line_repr=repr(last_line[-40:]),
    )


def scan_cnf(path):
    header = None
    n_clause_lines = 0
    with _open(path) as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("c"):
                continue
            if s.startswith("p "):
                parts = s.split()
                header = dict(nvars=int(parts[2]), nclauses=int(parts[3]))
                continue
            n_clause_lines += 1
    require(header is not None, f"{path}: no p-line")
    return dict(header=header, clause_lines=n_clause_lines,
                header_matches_body=(n_clause_lines == header["nclauses"]))


VERIFIED = re.compile(r"^s VERIFIED", re.M)
NOT_VERIFIED = re.compile(r"^s NOT VERIFIED", re.M)
RATLINE = re.compile(r"c (\d+) RAT lemmas in core")


def replay(cnf_gz, drup_gz, tag, scratch):
    """Decompress into scratch, run drat-trim, parse stdout, clean up."""
    os.makedirs(scratch, exist_ok=True)
    cnf = os.path.join(scratch, tag + ".cnf")
    drup = os.path.join(scratch, tag + ".drup")
    rec = {"tag": tag, "cnf_src": cnf_gz, "proof_src": drup_gz}
    try:
        for src, dst in ((cnf_gz, cnf), (drup_gz, drup)):
            if src.endswith(".gz"):
                with gzip.open(src, "rb") as fi, open(dst, "wb") as fo:
                    shutil.copyfileobj(fi, fo, 1 << 22)
            else:
                shutil.copyfile(src, dst)
        rec["cnf_scan"] = scan_cnf(cnf)
        rec["proof_scan"] = scan_proof(drup)
        t0 = time.time()
        proc = subprocess.run([DRAT, cnf, drup, "-t", str(TIMEOUT)],
                              capture_output=True, text=True,
                              timeout=TIMEOUT + 300)
        rec["wall_s"] = round(time.time() - t0, 2)
        out = proc.stdout + proc.stderr
        rec["returncode"] = proc.returncode
        rec["verified"] = bool(VERIFIED.search(out))
        rec["explicit_not_verified"] = bool(NOT_VERIFIED.search(out))
        m = RATLINE.search(out)
        rec["rat_lemmas_in_core"] = int(m.group(1)) if m else None
        rec["stdout_tail"] = out.strip().splitlines()[-8:]
        # return code is NOT the success signal (house rule); the token is.
        rec["verdict"] = "VERIFIED" if rec["verified"] else "FAILED"
    except subprocess.TimeoutExpired:
        rec["verdict"] = "TIMEOUT"
    except Exception as exc:                        # noqa: BLE001
        rec["verdict"] = "ERROR"
        rec["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        for p in (cnf, drup):
            if os.path.exists(p):
                os.remove(p)
    return rec


def targets_m17():
    d = os.path.join(ROOT, "computations",
                     "unaudited-template-kill-w8-2026-08-15", "certificates")
    sel = os.environ.get("H1_ORBITS")           # e.g. "1-30" or "0,5,7"
    if sel:
        want = set()
        for part in sel.split(","):
            if "-" in part:
                a, b = part.split("-")
                want.update(range(int(a), int(b) + 1))
            else:
                want.add(int(part))
    else:
        want = set(range(31))
    out = []
    for i in sorted(want):
        cnf = os.path.join(d, f"w8_m17_closure_o{i}.cnf.gz")
        pf = os.path.join(d, f"w8_m17_closure_o{i}.drup.gz")
        require(os.path.exists(cnf), f"missing {cnf}")
        require(os.path.exists(pf), f"missing {pf}")
        out.append((cnf, pf, f"m17_o{i}"))
    return out


def targets_w11():
    d = os.path.join(ROOT, "computations",
                     "unaudited-sat-pair-w11-2026-08-15", "w8_reproofs")
    require(os.path.isdir(d), f"missing {d}")
    out = []
    names = sorted(x for x in os.listdir(d)
                   if x.endswith(".drup") or x.endswith(".drup.gz"))
    for pf in names:
        base = pf[:-8] if pf.endswith(".drup.gz") else pf[:-5]
        # W11 named its replacements "<orbit>.lingeling.drup.gz"; the CNF is
        # the original W8 one, without the solver infix.
        for infix in (".lingeling", ".cadical", ".kissat"):
            if base.endswith(infix):
                base = base[: -len(infix)]
        cand = [os.path.join(d, base + s) for s in (".cnf", ".cnf.gz")]
        cand += [os.path.join(ROOT, "computations",
                              "unaudited-template-kill-w8-2026-08-15",
                              "certificates", base + s)
                 for s in (".cnf", ".cnf.gz")]
        cnf = next((c for c in cand if os.path.exists(c)), None)
        require(cnf is not None, f"no CNF for {pf}; looked in {cand}")
        out.append((cnf, os.path.join(d, pf), "w11_" + base))
    return out


def main():
    group = sys.argv[1] if len(sys.argv) > 1 else "m17"
    tg = {"m17": targets_m17, "w11": targets_w11}[group]()
    tag_sfx = os.environ.get("H1_OUT_SUFFIX", "")
    outp = os.path.join(HERE, f"results_b3_{group}{tag_sfx}.jsonl")
    print(f"[h1-b3] group={group} targets={len(tg)} -> {outp}", flush=True)
    nver = 0
    with open(outp, "w") as fh:
        for cnf, pf, tag in tg:
            rec = replay(cnf, pf, tag, SCRATCH)
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            nver += rec["verdict"] == "VERIFIED"
            print(f"[h1-b3] {tag:24s} {rec['verdict']:9s} "
                  f"{rec.get('wall_s','-')}s "
                  f"lines={rec.get('proof_scan',{}).get('lines','-')} "
                  f"trunc={rec.get('proof_scan',{}).get('truncated_tail','-')} "
                  f"rat={rec.get('rat_lemmas_in_core','-')}", flush=True)
    print(f"[h1-b3] group={group}: {nver}/{len(tg)} VERIFIED", flush=True)


if __name__ == "__main__":
    main()
