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
* Terminal coefficient: \(\chi=\alpha Q_2+Q_3\), and the
  response-translation equations through order two leave exactly this one
  coefficient (\(\chi=-2Q_3\) on the normalized row).

  **Read \(\chi=0\) precisely.**  Cleanliness is a property of a cap
  *covector* \(K\): \(\mathcal E_{p,q}(K)=0\).  At \(h=3\),
  \(\mathcal E=sQ_2+Q_3\), so \(\chi\) is \(\mathcal E\) at the single
  **coordinate** cap \(K=E_{ab}\).  Every coordinate cap is **inactive** —
  \(\kappa_c(E_{ab})=\delta_{a=b=c}\), so \(\kappa_0\kappa_1\kappa_2=0\),
  including on the diagonal, where two of three vanish.  Since
  `SP-CLEAN-BRIDGE` needs an **active** clean point
  (\(s\kappa_0\kappa_1\kappa_2\ne0\)), \(\chi=0\) is the cleanliness of a
  point the bridge cannot use.  See
  `cap-line-cubic-and-why-the-landing-is-inactive.md`.  The older
  shorthand "cleanliness is \(\chi=0\)" is exact only inside the
  monochromatic star-sector ansatz, where the coordinate cap is the one
  under discussion; do not carry it outside that setting.
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
* Four-hole vector \(H(A)_e=\operatorname{haf}(A[W\setminus e])\) and
  polarization (Euler) identities, with
  \(H_k(e)=[t^k]\operatorname{haf}((q+tR)[W\setminus e])\):
  \(\langle R,H_k\rangle=(k+1)Q_{k+1}\),
  \(\langle q,H_k\rangle=(3-k)Q_k\), and
  \(\chi={1\over3}\langle A_{\rm cap},H(A_{\rm cap})\rangle\).  In the jet
  basis \(J_0=\alpha Q_0+Q_1\), \(J_1=\alpha Q_1+2Q_2\),
  \(J_2=\alpha Q_2+3Q_3\), \(J_3=\alpha Q_3\), the response contraction
  \(\alpha\langle R,H(A_{\rm cap})\rangle=\alpha^2J_1+3J_3\) has **no
  \(J_2\)**, while \(\alpha\chi=\alpha J_2-2J_3\).  See
  `notes/fourhole-cap-polarization-terminal-blindness.md`.
* Every row is a four-hole pairing.  With
  \(H(A)_e=\operatorname{haf}(A[W\setminus e])\) and \(q^w\) the internal
  quadratic read at the word \(w\),
  \(\operatorname{Row}(i,j,w)=\langle\tfrac{d_{ij}}3q^w+R^w_{ij},H(q^w)\rangle\)
  for every word and every label pair, cross-colour edges included.  So the
  \(27\) pure-word equations are nine caps paired against three grade-zero
  four-hole vectors: **the diagonal anchors and the four-hole interface are
  the same object**.  See
  `terminal-class-weight-invisibility-and-fourhole-grade-ladder.md`.
* Weight grading: internal edges \(-1\), star edges \(+1\), direct scalar
  \(+3\).  All \(105\) perfect matchings of the block array are weight zero,
  so \(q\mapsto q/\tau,\ p\mapsto\tau p,\ s\mapsto\tau s,\ d\mapsto\tau^3d\)
  fixes the whole matching tensor while \(\chi\mapsto\tau^6\chi\).  Hence
  \(\chi\) is **not a function of the row values**, and a landing theorem can
  only be a vanishing statement — never a formula, never a bound.
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
| Repair the guard's two missing anchors with **star**-sector material, keeping \(\chi\ne0\) | The anchor's carrier edge is exactly what the off-diagonal rows use to annihilate the direct scalars carrying \(\chi\); and the monochromatic ansatz has no completion at all | `h3-star-sector-anchor-terminal-class-trade.md` |
| Compute or bound \(\chi\) from row values, or look for a chart that "sees" it | Every chart is weight zero and \(\chi\) has weight six; a \(\tau\)-rescaling fixes all rows and scales \(\chi\) | `terminal-class-weight-invisibility-and-fourhole-grade-ladder.md` |
| Treat the two missing anchors as interchangeable | Colour 0's is restorable at its pure word; colour 1's lies in the seven-row ideal and is impossible | `h3-star-sector-pure-word-anchor-witness-and-colour-asymmetry.md` |
| Generalize the anchor peel or the anchor/terminal trade to another slice | Both need the frozen slice to have exactly one live four-set; a controlled comparison packet has neither | `h3-star-sector-transport-collapse-general-peel-degenerate.md` |
| Prove the landing without using the third colour's anchor | The alternating eight-cycle satisfies \(6560\) of the \(6561\) equations, failing only that anchor | `monochromatic-internal-quadratic-structure-and-eight-cycle-guard.md` |
| Reach \(\chi\) by contracting the four-hole vector against the response \(R\) | Provably blind to the terminal grade \(J_2\); an explicit witness pair has equal \(\langle R,H\rangle\) with \(\chi=0\) vs \(\chi=1\) | `fourhole-cap-polarization-terminal-blindness.md` |
| Repair the guard's two missing anchors with colour-0/1 *internal-quadratic* material, keeping \(\chi=-2\) | Any \(q\) carrying all three pure-word hafnians leaks at a mixed word; all 3375 matching triples leak.  Anchor \(c\) also needs two disjoint colour-\(c\) edges regardless of the stars | `three-anchor-internal-quadratic-leak.md` |
| Treat \(\chi=0\) as delivering an active clean point, or as "the" cleanliness condition | \(\chi\) is \(\mathcal E\) at a **coordinate** cap, and every coordinate cap is inactive.  The landing certifies the root \(z=0\), which *is* that cap | `cap-line-cubic-and-why-the-landing-is-inactive.md` |
| Adopt \(\mathcal E(I)=0,\ \tau\ne0\) as the next target because it certifies an *active* root | True, and unusable: that statement is equivalent to emptiness of the nine-row variety, i.e. to the open \((8,3)\) case | `clean-bridge-at-eight-is-the-open-case.md` |
| Name a root of the cap cubic, or bound one | The endpoint torus scales \(z\mapsto(g_i/g_j)z\) on an **off-diagonal** line, so no nonzero root is a function of the matching tensor.  (On a *diagonal* line the weight is zero and this gives nothing — do not quote it there) | `cap-line-cubic-and-why-the-landing-is-inactive.md`, section 5 |
| Trust a checker because it "passes under `-O`" | `-O` deletes `assert`.  A script whose only failure mechanism is a bare assert cannot fail under `-O`; if the work sits inside the assert expression, the work is deleted too.  Use a `require()` that raises | 542 of 794 checkers still had this defect as of 2026-08-01 |

## 4. The one open target

> In a genuine complete full-nine six-residual-site packet with all three
> diagonal anchors and source-faithful adjacent provenance, the sum of the
> physical response-companion terms, pure-anchor corrections, and landing
> errors equals the canonical twenty-cut aggregate; equivalently it kills
> \(\mathfrak D(A,B)\), or proves
> \(H(H(A_{\rm cap}))=2\mathcal B(A_{\rm cap})\).

**Read this target with the following two facts in hand.**  Both are recent,
both are audited, and together they change what a success here would be worth.

*The landing lands on an inactive root.*  Proving it moves a packet from
"possibly rootless" to "roots exist, all inactive" — it is branch 2's entry
condition, not an escape from the frontier's dichotomy.  On the least
degenerate packet available (the pure-word witness) the landing **holds** and
buys nothing: \(\gcd=z\) exactly, the sole clean point is \(z=0\) and
inactive, and the degree-two residual is rootless at full rank.  The active
analogue — \(\mathcal E(I)=0\) with \(\tau\ne0\), which *would* give the
descent — is not a usable substitute: it is **equivalent to the open case**.
See `cap-line-cubic-and-why-the-landing-is-inactive.md` and
`clean-bridge-at-eight-is-the-open-case.md`.

*At \(h=3\) the nine-row system **is** the open \((8,3)\) case.*  So
`SP-CLEAN-BRIDGE` at \(N=8\) is equivalent to \((8,3)\), and no \(h=3\) work
can shortcut it.  What \(h=3\) can still produce is **guards** — exact packets
with the residual pinned as a formula — and structure theorems.  Aim there.

Given that, this must be an **aggregate** theorem over all twenty three-sets
and must use the complete diagonal sector.  Two independent attack lines:

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
   *Progress (2026-07-31):* the admissible probe is now pinned.  The
   response contraction is blind to the terminal grade, so the pairing must
   go against the internal quadratic \(q\), or against the cap itself via
   \(\chi={1\over3}\langle A_{\rm cap},H(A_{\rm cap})\rangle\).  On the
   seven-row guard both \(J_0\) and \(J_3\) vanish and the whole failure
   sits in the invisible \(J_2\); the two missing anchors annihilate both
   the four-hole vector and the cap there, so the diagonal sector must
   enter *before* the pairing.

   *Progress (2026-07-31, later):* the anchor sector was probed and the
   colour-separated shortcut is dead — see
   `three-anchor-internal-quadratic-leak.md` (L0/L1/L2/L3).  The anchors
   cannot be carried by the internal quadratic, so a repair must use the
   **star** sector.

   *Progress (2026-07-31, latest): that star-sector repair has been executed
   and it fails.*  Freezing the guard's colour-2 slice and freeing everything
   else with monochromatic internal edges, the guard's **own** seven rows
   force \(\operatorname{supp}q_c\subseteq\{04,05,14,15,23\}\); the anchor
   then peels onto one edge,
   \(\operatorname{Row}(c,c,c^6)=q_c(2,3)\rho_c(c,c,W\setminus\{2,3\})\); and
   the same edge annihilates the direct scalars carrying the class, giving
   \(q_c(2,3)\chi=0\) on the seven-row variety.  Seven rows plus either
   *complete* anchor row is infeasible, and so is the nine-row system.  The
   hypothesis is attainable for colour 0 by an explicit witness with
   \(\chi=0\), and impossible for colour 1 by an ideal certificate.  See
   `h3-star-sector-anchor-terminal-class-trade.md` and
   `h3-star-sector-pure-word-anchor-witness-and-colour-asymmetry.md`.

   Three things bound what comes next, and should be read before choosing a
   target.  The peel and the trade need the frozen slice to have exactly one
   live four-set, so they do **not** generalize
   (`h3-star-sector-transport-collapse-general-peel-degenerate.md`).  Cross-colour
   internal edges are still open, but localized: any completion must put its
   \(2\)-mixed mass on an edge touching site \(2\) or \(3\)
   (`h3-cross-colour-repair-internal-edge-localization.md`).  And \(\chi\) is
   invisible to the matching tensor, so only a vanishing argument can ever
   work (`terminal-class-weight-invisibility-and-fourhole-grade-ladder.md`).
   On the two-sign branch \(d_{01}\pm2d_{02}\ne0\), the localization is now
   further split by
   `h3-cross-colour-terminal-support-dichotomy.md`: all four mixed
   orientations on edge \(23\) vanish, and either the four carrier-\(4\)
   cells or the four carrier-\(5\) cells vanish.  The two resonant
   hyperplanes retain only one sign family.

   **Next concrete steps, ranked.**
   1. Push the four-hole ladder up one grade.  The rows control
      \(\langle R,H_0\rangle=Q_1\) exactly; the first datum they do not
      control is \(\langle R,H_1\rangle=2Q_2\), at weight three.  Determine
      whether the *aggregate* of the nine rows reaches it, or pin the
      obstruction.  This is attack line 2 in the only form the anchors can
      enter.
   2. Close the monochromatic case in general.  Its structure is already
      reduced: class factorization, the sharp anchor lemma (a nonzero
      four-hole cofactor per colour, which strictly sharpens L0), the
      star-rank lemma, handle rigidity, and colour blindness, with two
      branches pinned as explicit residuals
      (`monochromatic-internal-quadratic-structure-and-eight-cycle-guard.md`).
      Note the eight-cycle guard: any proof must use the third colour's
      anchor.
   3. Decide the cross-colour case on the two carrier-zero branches and two
      one-sign resonant hyperplanes, or produce a guard there.

   Useful harness: the six new checkers all build the whole \(9\times729\)
   system as exact polynomials and decide it by splitting single-monomial
   equations into their factors.  Copy one of those rather than mutating
   `BLOCKS` in the committed guard checker.

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
* **Never use a bare `assert` in a checker.**  Define a `require()` that
  raises, and use it for every check.  `python3 -O` deletes assert
  statements, so a checker built on them prints its PASS line whether or
  not the property holds — and if the computation sits inside the assert
  expression, the computation never runs either.  Before believing a new
  checker, mutation-test it: inject a failure and confirm it raises under
  **both** `python3` and `python3 -O`.  A large `-O` speedup is proof that
  work was deleted; no speedup proves nothing, since deleting a cheap
  comparison costs no time.
* One bounded task per agent; audits by fresh agents that only see the
  artifacts.  Do not let the writer audit itself.
* When stuck, produce an exact guard (a packet with the precise residual
  pinned as a formula) rather than a heuristic argument; guards are the
  currency of this project.
