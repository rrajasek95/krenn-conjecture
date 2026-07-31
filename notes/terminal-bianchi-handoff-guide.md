# Handoff guide: attacking the terminal Bianchi landing error-free

Written 2026-07-31 for continuation by a smaller model.  This note is
operational, not mathematical: every formula restated here is copied from
an independently audited artifact, and everything else is a pointer.  If
this note and a cited file ever disagree, the cited file wins.

## 0. Non-negotiable ground rules

1. **Krenn's conjecture is OPEN.**  `SP-CLEAN-BRIDGE` is the only missing
   conjecture-level implication.  Never write, commit, or report anything
   that claims otherwise.  The certified spine
   (`certification/BASELINE.md`, tag `certified-spine-2026-07-30`) changes
   only through `certification/SUPERSESSIONS.md`, and only after an
   independently audited positive theorem explicitly supersedes a named
   dependency.  Research notes commit freely on `main` and change nothing
   by themselves.
2. **Exact arithmetic only.**  Python stdlib, `int`/`Fraction`, no numpy,
   no floats.  Checkers must use a `require()` that raises (never bare
   `assert`, which `-O` deletes) and must pass under `python3`,
   `python3 -O`, and `python3 -I -S`, plus `python3 -m py_compile` and
   `git diff --check`.  Keep every script running in seconds.
3. **Proved ≠ verified.**  "Verified on N random packets" is evidence;
   a formal polynomial identity checked on all monomials, or a hand proof,
   is a proof.  Say which one you have, every time.
4. **Nothing is committed without an independent re-audit** by a fresh
   agent that reads only the artifacts (not your reasoning) and tries to
   refute them.  Apply requested corrections, re-run all checker modes,
   then commit with a short imperative subject line.
5. **Do not reopen** anything in section 6 of
   `notes/consolidated-proof-frontier.md` (cutwise/one-anchor/top-apolar
   routes, dark rank refinements, etc.).

## 1. Workspace

Work in the clone `~/workplace/krenn-conjecture-terminal-bianchi`
(remote `github` → `https://github.com/rrajasek95/krenn-conjecture.git`,
branch `main`; last commit at handoff: `951ae50`).  Read first, in order:

1. `notes/research-checkpoint-2026-07-31-terminal-bianchi.md` — state and
   restart procedure;
2. `notes/h3-nonclean-twojet-middle-core.md` — the committed twenty-cut
   machinery, the exact cutwise physical formula, and the definition of
   the response companion \(M_{ab,S}\) and pure-anchor corrections
   (**take these definitions from that file, not from memory**);
3. `notes/three-anchor-apolar-double-polar-bianchi-reduction.md` — the
   double-polar reformulation (audited PASS 2026-07-31);
4. `notes/consolidated-proof-frontier.md`, section 5 — how the \(h=3\)
   statement sits under the uniform overlap lemma;
5. `notes/h3-hamming-two-tangent-or-clean-boundary.md` and
   `notes/h3-diagonal-segre-second-transgression-seven-row-guard.md` —
   the two guards that bound the target from both sides.

Model the code on `computations/verify_h3_nonclean_twojet_middle_core.py`
and `computations/verify_three_anchor_apolar_double_polar_bianchi_reduction.py`;
both contain reusable exact implementations of hafnians, matchings,
response layers, \(\Theta_S\), and formal edge-variable polynomials.

## 2. Audited dictionary (safe to restate)

Six sites \(W=\{0,\ldots,5\}\); symmetric zero-diagonal edge arrays; the
hafnian sums over the fifteen perfect matchings of \(K_6\).

* Response layers: \(Q_j=[t^j]\operatorname{haf}(q+tR)\), i.e.
  \(Q_j=R^{[j]}q^{[3-j]}\) (exactly \(j\) edges from \(R\)).
* Selected source row: \(\alpha Q_0+Q_1=0\), so \(\alpha=-Q_1/Q_0\).
* Terminal coefficient: \(\chi=\alpha Q_2+Q_3\); **cleanliness is
  \(\chi=0\)**, and the response-translation equations through order two
  leave exactly this one coefficient (\(\chi=-2Q_3\) on the normalized
  row).
* Twenty-cut average (committed):
  \({1\over8}\sum_{|S|=3}\Theta_S(2\alpha R,R,q)=\chi\); equivalently
  \([t^3](q+2tR+2\alpha t^2R)^{[3]}=8\chi\).  The factors \(8\) and
  \(2\alpha\) are audited — do not "simplify" them.
* Landing error: with \(B=2R+\beta\), \(A=2\alpha R+\gamma\),
  \[
   \mathfrak D(A,B)=(2\alpha R\beta+2R\gamma+\gamma\beta)q
     +4R^{[2]}\beta+2R\beta^{[2]}+\beta^{[3]}.
  \]
  Killing the aggregate \(\mathfrak D\) suffices; literal
  \(\beta=\gamma=0\) is sufficient but unnecessarily strong.
* Double polar (audited): \(H(A)_{ij}=\operatorname{haf}(A[W\setminus\{i,j\}])\)
  for \(i\ne j\), \(H_{ii}=0\); cross-star \(\mathcal B_{ij}\) with
  \(\mathcal B_{ii}=0\); then
  \(H(H(A))=\operatorname{haf}(A)\,A+2\mathcal B(A)\) as a matrix
  identity.  For the cap \(A_{\rm cap}=\alpha q+R\):
  \(\operatorname{haf}(A_{\rm cap})=\chi\) and, for a nonzero cap,
  \(\chi=0\iff H(H(A_{\rm cap}))=2\mathcal B(A_{\rm cap})\).
  All-ones sanity check: \(\operatorname{haf}=15\), polar entry \(3\),
  double polar \(27\), defect \(12=2\cdot6\).
* The reciprocal Hankel component \(Q_0C_3-Q_2C_1\) is the
  **\(Q_0Q\)-scaled radial image** of the averaged scalar Bianchi class —
  it does not "equal" the scalar average.  (A previous audit rejected the
  looser wording; keep the exact phrasing.)

## 3. Known traps, each with its killing guard

| Tempting wrong move | Why it is wrong | Guard |
|---|---|---|
| Prove each cut value \(\Theta_S=0\) | Individually false | Rank-two clean packet: \(q=01{+}23{+}45\), \(u=(1,-1,2,0,1,1)\), \(v=(1,2,-2,1,-2,1)\), \(R=uv^{\mathsf T}+vu^{\mathsf T}\), \(\alpha=-2\), layers \((1,2,6,12)\), \(\chi=0\), yet all twenty cut values are nonzero and cancel only in total |
| Prove complementary pairs cancel | Also false on the same packet | Same packet |
| Use \(C_S=0\) as the physical cut equation | A complete selected row gives \(\alpha C_S+M_{ab,S}=0\), and diagonal rows add pure-anchor corrections | `h3-nonclean-twojet-middle-core.md` |
| Drop one or two diagonal anchors | Seven rows (all-word row + six off-diagonal + one anchor + good Segre stars + adjacent decomposition) can leave \(\chi=-2\) | `h3-diagonal-segre-second-transgression-seven-row-guard.md` |
| Force a global site derivation from the Hamming-two truncation | Not forced; its obstruction packet is already clean | `h3-hamming-two-tangent-or-clean-boundary.md` |
| Promote the sufficient literal landing \(\widehat A=2\alpha R,\ \widehat B=R\) to a necessary conclusion | Only aggregate error annihilation is necessary | Draft note, sections 3–4 |
| Treat the \(h=3\) statement as a new spine dependency | It is the finite local normal form of the uniform overlap lemma, a diagnostic | Frontier, section 5 |

## 4. The one open target

> In a genuine complete full-nine six-residual-site packet with all three
> diagonal anchors and source-faithful adjacent provenance, the sum of the
> physical response-companion terms, pure-anchor corrections, and landing
> errors equals the canonical twenty-cut aggregate; equivalently it kills
> \(\mathfrak D(A,B)\), or proves
> \(H(H(A_{\rm cap}))=2\mathcal B(A_{\rm cap})\).

This must be an **aggregate** theorem over all twenty three-sets and must
use the complete diagonal sector.  Two independent attack lines:

1. **Companion sum.**  Assemble
   \(\sum_S(\alpha C_S+\text{companion}_S+\text{anchor}_S)\) from the
   literal full-nine rows and compare with the twenty-cut aggregate.
   First build the exact packet model, test on the seven-row \(\chi=-2\)
   guard (the identity must fail there in exactly the anchor sector) and
   on random full-nine packets; only then attempt the multilinear proof.
2. **Four-hole interface.**  \(H(A_{\rm cap})\) is the vector of four-hole
   hafnians.  Determine which physical rows control which response grades
   of \(H(H(A_{\rm cap}))-2\mathcal B(A_{\rm cap})=\chi A_{\rm cap}\), and
   find the smallest grade the rows stop controlling.  Any edgewise claim
   must first be tested against the rank-two packet.

Work-in-progress files from agents on these lines use the prefixes
`wip-companion-*` and `wip-fourhole-*` (uncommitted; absence means the
attempt was not retained).  A success on either line is still only the
\(h=3\) local normal form: it must afterwards be transported through the
already isolated K6 four-cut/source-provenance interface to touch the
uniform conjecture, and even then it enters the spine only via a named
supersession.

## 5. Error-avoidance discipline for a smaller model

* Never write a formula from memory: copy it from an audited file and
  cite the file.  If two files disagree, stop and record the discrepancy
  instead of choosing.
* Before trusting any new identity, test it on the two standard probes:
  the rank-two clean packet (section 3) and the seven-row \(\chi=-2\)
  guard.  A candidate theorem that holds on the guard is wrong; one that
  fails on the clean packet is wrong.
* Verify normalization on the all-ones array before using any new
  hafnian/polar code (15, 3, 27, defect 12).
* Prefer formal polynomial identities (all 15 edge variables, exact
  monomial dictionaries) over random testing wherever the computation is
  small; the existing checkers show the pattern.
* One bounded task per agent; audits by fresh agents that only see the
  artifacts.  Do not let the writer audit itself.
* When stuck, produce an exact guard (a packet with the precise residual
  pinned as a formula) rather than a heuristic argument; guards are the
  currency of this project.
