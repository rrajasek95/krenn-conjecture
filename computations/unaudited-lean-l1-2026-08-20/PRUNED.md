# PRUNED — disk remediation, lane L1

> **UNAUDITED — lane L1, 2026-08-20.** Pinned krenn-conjecture HEAD
> `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`.
> Prompted by the volume reaching 0 free. Nothing under `staged/`,
> `canonical/`, `cores/`, `lrat/`, `lean/`, `encoder/`, `f2check/` was touched,
> and no source file of the working clone was touched.

## Result

| | before | after |
|---|---|---|
| `work/` | 7,364 MiB | **1,496 MiB** |
| free on the volume | 7.8 GiB | **19 GiB** |

Target was under 3 GB for `work/`; achieved 1.5 GB.

## What was deleted, and how to restore it

### 1. Mathlib build tree — 5,858 MiB — **cheaply restorable**

`work/fc/.lake/packages/mathlib/.lake/build/lib` and `.../build/ir`.

Restore with, from `work/fc`:

```bash
lake exe cache get
```

This unpacks from `~/.cache/mathlib` (833 MiB, **left in place deliberately**),
so the restore is a local decompression — minutes, no network, no re-download.
`.../build/bin` was kept so the `cache` executable itself does not have to be
rebuilt first, and mathlib's `.git` was kept so Lake does not try to re-clone.

`build/ir` holds the generated `.c` files, needed only to *recompile* Mathlib,
never to build against it.

**This was affordable because the current work needs no Mathlib at all** — see
§"Consequence" below.

### 2. Two unused Lean toolchains — 5,413 MiB — restorable by download

`~/.elan/toolchains/leanprover--lean4---v4.32.0` and `---v4.32.2`.

Verified unused first: every `lean-toolchain` in this repository pins
`leanprover/lean4:v4.27.0`, the only other pin anywhere in the repo is
`v4.33.0-rc1` (KitaKen1's `lean4web` edition, a different build that is not
installed and that we do not build), and a scan of every other workspace under
`/Users/rishi/workplace` found only `formal-conjectures`, also pinning
`v4.27.0`. The pinned toolchain was re-verified working after deletion.

**`v4.33.0` (2.7 GiB) was deliberately KEPT**, and this is a judgement call
worth flagging: `~/.elan/settings.toml` has `default_toolchain = "stable"`, so
a stray `lean`/`elan` invocation *outside* a pinned project resolves to the
current stable and would re-download multi-GB if absent. That is exactly the
failure that put 2.7 GiB on this disk in the first place (this lane caused it,
early on, by running `elan toolchain list` outside a project). Deleting
`v4.33.0` would invite the same download again. If the coordinator wants that
2.7 GiB back, the safe sequence is to first set elan's default to `v4.27.0` and
then delete — I have not changed that global setting, since it is shared with
the other lanes.

### 3. Editor-only artifacts — ~5 MiB — **PARTLY A MISTAKE, since repaired**

All `.ilean` and `.olean.server` files under `work/fc/.lake/packages`.

`.ilean` is indeed language-server-only and safe to delete.

**`.olean.server` is NOT.** In Lean 4.27's module system it is a required data
file, and deleting it makes `import` fail with

```
missing data file for module Batteries.Classes.Cast
```

Mathlib was unaffected — `lake exe cache get` restored its `.olean.server`
files along with everything else — but the eight dependency packages
(`batteries`, `aesop`, `proofwidgets`, `Qq`, `plausible`, `importGraph`,
`LeanSearchClient`, `Cli`) are not in that cache, so 53 Batteries modules and a
handful of others lost a required file. Worse, the sibling `.olean.server.hash`
files survived, so Lake believed the packages were up to date and reported the
error instead of rebuilding.

Repaired by clearing `.lake/build` for those eight packages and rebuilding them
from source (`work/fix_deps.sh`). The whole deletion had saved about 5 MiB.

**Rule for future pruning: delete `.ilean` only. Never `.olean*`.**

### 4. Superseded build tree — 69 MiB

`skeleton/lrat-probe/.lake`. That package is the `native_decide` UNSAT layer,
now the *fallback* rather than the plan (the kernel-reducible checker in
`staged/formal/n8-diagonal/N8Diagonal/Rup.lean` is the route of record). Its
**sources and its 30 MiB of CNF/LRAT artifacts were kept**; only the rebuildable
`.lake` output went. Restore with `lake build LratProbe` in that directory.

### 5. Leftover temporary directories

`/var/folders/**/T/f2_*` and `/var/folders/**/T/m4096_*`, left by
`f2check/f2_direct.py` and `work/measure_4096.py`.

## What was NOT deleted, and why

* **The 4096-case experiment** the coordinator flagged as ~1.3 GiB disposable
  is **not on disk** and never was: `work/measure_4096.py` writes each CNF and
  LRAT to a temp file, measures it, and unlinks it immediately. Its entire
  residue is `work/measure_4096.jsonl` (532 KiB, one JSON line per case) plus
  `measure_4096_common.json` and the log. All three are kept — they are the
  evidence for the 87-vs-4096 decision in `architecture.md` §5.1.
* **No duplicate FC clones exist.** `work/fc` is the only one in this lane;
  `/Users/rishi/workplace/formal-conjectures` is a separate checkout belonging
  to the phase-one `formal/` work, not this lane, and was left alone.
* `work/algal` (133 MiB) and `work/kitaken` (1.6 MiB) are the two related-work
  clones cited in `RELATED-4659.md`; both are small and were kept.

## Consequence for the current work — none

The immediate task (the trie store, then kernel-checking the 87 orbits) needs
**no Mathlib**: `N8Diagonal/Rup.lean` has zero imports. A dedicated
zero-dependency project was set up at `work/rup/` for exactly this, and it
type-checks `Rup.lean` in **2.4 s** against 12–16 s in the Mathlib-loaded clone
— so the pruning made the current loop about six times faster, not slower.

Mathlib is needed again only for `Haf/Product/Normal/Symm.lean`, i.e. for
components 3, 6–8 and 10. Run `lake exe cache get` in `work/fc` before resuming
those.

## Second round: the lane no longer carries a Mathlib at all

The `.olean.server` repair (§3) turned out to cascade: clearing the eight
dependency packages' build trees invalidated Mathlib's traces, so `lake build`
began rebuilding Mathlib **from source**. The volume fell from 12.4 GiB to
4.2 GiB free in about five minutes before this was caught and killed.

The recovery removed the problem rather than repairing it. There is a second,
**intact** formal-conjectures checkout on this box at
`/Users/rishi/workplace/formal-conjectures`, pinned to the same
`leanprover/lean4:v4.27.0`, with a complete build including every
`.olean.server`. It belongs to the phase-one `formal/` work, and
`formal/FORMALIZATION.md` already documents using it exactly this way — "the
sibling formal-conjectures checkout was used only for imports and compilation".

So `work/fc` was deleted outright (**7,255 MiB**) and the algebra modules are
now compiled against the sibling checkout, read-only, via
`work/lean_build.sh`: it reads `LEAN_PATH` out of that checkout with
`lake env`, then runs `lean -o` from our own tree with our output directory
appended. Nothing is written into the sibling checkout.

| | |
|---|---|
| lane footprint | **275 MiB** (target was under 7 GiB) |
| free on the volume | **21.7 GiB** |
| Mathlib copies owned by this lane | **none** |

`Rup.lean` and `Haf.lean` were rebuilt this way before `work/fc` was deleted,
to confirm the route works.

## Clean-as-you-go in the orbit loop

`work/build_all_orbits.sh` now checkpoints on **the log** rather than on build
output: an orbit already recorded `rc=0` in `ORBITS_ALL.txt` is skipped. That
allows each orbit's `.olean`, `.ilean`, `.trace`, `.ir` and even its generated
`.lean` to be deleted the moment its kernel check succeeds. The durable record
is the log line; the source of truth is `cores/n8z0/`, from which any single
orbit can be regenerated and re-verified with one command.

It also carries a courtesy guard: if free space falls below 4.5 GiB it stops
cleanly with `PAUSING` in the log rather than racing W18's box-wide guard at
4 GiB. A rerun resumes from the log.

## Standing practice from here

Builds in this lane clean their intermediates as they go, and long-lived build
trees are treated as caches to be dropped rather than assets to be kept. In
particular: iterate `Rup.lean` and the generated orbit modules in `work/rup/`
(zero dependencies, nothing to accumulate), and keep the Mathlib-backed clone
unpopulated except while algebra modules are actually being built.
