# Codex root attack interface: intrinsic `N=8` cap incidence

Status: **UNAUDITED WORKING INTERFACE**.  This note changes no certified
claim.  Its purpose is to keep the new attack in the original matching
coefficient system and to give every lane the same accepted terminals.

## 1. Source equations and the only descent target

Let `A_uv in V_u tensor V_v`, `dim(V_u)=3`, be endpoint-ordered blocks on
eight sites and impose the literal equations

```text
H_8(A) = Delta_(8,3).
```

For a pair `p,q`, put `U=B-{p,q}`.  A cap covector `K` has nine homogeneous
coordinates.  With the notation of the certified clean-pair theorem,

```text
s(K)       = <K,A_pq>,
kappa_c(K) = K_cc,
R_ab(K)    = K |-(A_pa A_qb + A_pb A_qa).
```

At the eight-to-six boundary the exact cap error is the cubic tensor

```text
6 E_pq(K) = 3 s(K) r(K)^2 x + r(K)^3.                 (1)
```

For a word `w in {0,1,2}^U`, expansion by a perfect matching `M` of `U`
has the denominator-free coefficient form

```text
E_pq,w(K) = sum_M [
    s (R_e R_f A_g + R_e A_f R_g + A_e R_f R_g)
      + R_e R_f R_g
  ].                                                     (2)
```

where `{e,f,g}=M` and every block entry is selected by `w`.  Equivalently,
after cancelling the common factor six, each typed matching contributes
the three `s R R A` choices and the one `R R R` choice with coefficient
one.  No individual occurrence is inferred from a cancelling sum.

Define the activity polynomial

```text
g_pq(K) = s(K) kappa_0(K) kappa_1(K) kappa_2(K).       (3)
```

The only cap output accepted by the induction is a point with every
coefficient of (1) zero and `g_pq != 0`.

## 2. Exact blocked-pair criterion

Fix the source `A` over an algebraically closed field and let

```text
R_K = F[K_00,...,K_22],
I_pq(A) = < E_pq,w(K) : w in {0,1,2}^U >.
```

Then the following are equivalent:

1. `(p,q)` has an active clean cap;
2. `V(I_pq(A))` meets the principal open set `D(g_pq)`;
3. `I_pq(A) : g_pq^infinity` is a proper ideal;
4. the Rabinowitsch ideal
   `<I_pq(A), t g_pq-1>` in `R_K[t]` is proper.

Thus a pair is **blocked** exactly when either saturation is the unit ideal.
This is the intrinsic nine-cap-variable decision already used experimentally
in W25.  It is not a heuristic cap library.  The equivalence is the usual
localization/Rabinowitsch argument and introduces no auxiliary source
coordinate.

For a blocked pair an exact certificate has the literal form

```text
1 = Q_0(K,t) (t g_pq(K)-1) + sum_w Q_w(K,t) E_pq,w(K). (4)
```

The next useful datum is not merely the Boolean verdict `blocked`: it is a
low-degree certificate (4), stratified by which source cells are nonzero.
Its coefficients can expose the source minors or deletions responsible for
blocking.  A computation that returns only `unit` without retaining or
interpreting (4) does not advance the proof.

## 3. Honest `N=8` theorem interface

Choose an exact source using only normalization operations that have been
proved to preserve the literal coefficient equations.  The provisional safe
lexicographic order is **minimum occupied-cell support first**, followed by
maximum anchors inside that minimum-support stratum.  No theorem currently
identified permits swapping this for the repository's frequent
maximum-anchor-first normalization.  The A1 claim that a minimum-cell-support
source can be balanced is being re-audited separately.

Do not impose all nonzero moduli equal to one.  The stored 13-cell object used
to reject that step is itself only a mixed-row solution (its pure amplitudes
are `(1,0,0)`) and is gauge-unstable, so it is not a full exact-source
counterexample to a minimum-source theorem.  The correct present verdict is:
the all-moduli-one step is **unproved and its published justification is
invalid**, not that a minimum full exact source with this property has been
ruled out.

A sufficient theorem at order eight is:

> Every such minimum source has one of:
>
> 1. a pair for which the ideal in Section 2 is proper;
> 2. a literal source-ideal unit or source-module separator;
> 3. a source-valid deletion, contraction, or deformation that strictly
>    decreases the declared well-founded normalization.

Outcome 1 invokes certified descent and the certified six-site theorem.
Outcome 2 contradicts exactness.  Outcome 3 contradicts minimality.  No
`B/Eq/AugP2`, response-KS, HPL, raw parent fold, or equality of auxiliary
characters is an accepted terminal without a displayed map to one of these
three source-level outcomes.

## 4. What a coverage proof must consume

The W40 rational level-4 point is a hard boundary control.  Its restrictions
to all three binary palettes are exact and agree on shared pure data, while
genuinely trichromatic `(3,3,2)` rows fail.  Therefore:

* binary compatibility cannot be a terminal obstruction;
* a support or packet funnel using only one- and two-colour rows is
  incomplete;
* every proposed coverage lemma must identify where a trichromatic row is
  used, and its positive-through-filter control must include this point.

The thirteen-exit packet remains a candidate local generator, not a proved
cover.  Before its closure can be used, one must prove that every minimal
source reaches a literal instance of that packet or give a separately
accepted terminal for the omitted branch.

## 5. Bounded attack order

1. Decide and retain low-degree blocked-pair certificates on exact or
   near-exact boundary families, beginning with the W40 point and the W25
   all-blocked point.
2. Determine which genuinely trichromatic rows change those certificates.
   This is a load-bearing-row test on the raw ideal, not random
   specialization away from the solution variety.
3. On the resulting finite source strata, extract a source minor, singleton,
   unit, or support-decreasing identity from (4).
4. Only after an `N=8` coverage theorem survives independent audit should
   the successful local move be promoted to a terminal-ear recurrence for
   arbitrary even order.

This order makes a failed idea return an explicit counterexample or an exact
residual ideal instead of another layer of conditional proof architecture.

## 6. First-wave pivot: the level-4 clean-cap theorem

The first adversarial family changes the preferred local target.  It gives a
four-parameter Laurent family satisfying all `4,881` level-4 equations and
shows that binary compatibility alone is false.  At its integral point,
however, exact cap saturation finds active clean pairs; several have the
literal cap `K=+/-I`.  Thus level-4 nonemptiness does **not** furnish an
all-blocked counterexample.

The leading falsifiable statement is now:

> **X4-to-cap at N=8 (open).**  If an endpoint-ordered ternary source on
> eight sites has the three pure amplitudes equal to one and every mixed
> amplitude of off-count at most four equal to zero, then some pair has a
> cap in `V(I_pq) intersect D(g_pq)`.

Full exactness implies the hypotheses, so this statement plus certified
descent and the certified six-site theorem would prove the general
bicoloured `N=8,d=3` case.  It is strictly sharper than the refuted claim
that the level-4 system is empty.

Required adversarial calibration:

* the W25 all-blocked object satisfies only level 3, so it is a lower-rung
  negative control, not a counterexample;
* the four-parameter W40 family is a positive level-4 control with explicit
  caps;
* a dedicated builder must try to solve level 4 while forcing all 28 cap
  Rabinowitsch ideals to be units.  Failure of an uncalibrated search is no
  evidence for the theorem.

The literal thirteen-exit lemma is demoted to a possible mechanism for
proving X4-to-cap.  Its six-site common-tail sector has 13 exits, but its raw
eight-site lift also has 90 crossing-tail occurrences forming 45 response
groups.  Any packet proof must close those responses rather than treating
the tail as a spectator.

## 7. Response-star reduction and the first exact branch kill

For a pair `p,q` and a residual centre `v`, let `L_pqv(A)` be the linear map
from the nine cap coordinates to every cell of `R_ab(K)` with `ab` not
incident with `v`.  If `K` lies in its kernel, all nonzero response edges lie
in the star at `v`.  Hence no two are disjoint, `r^2=0`, and the certified
error formula gives `E_pq(K)=0`.

The remaining activity requirement is also finite linear algebra.  Put

```text
ell_0=K_00, ell_1=K_11, ell_2=K_22, ell_3=<K,A_pq>.
```

Over an infinite field, `ker L` contains a point on which all four `ell_i`
are nonzero exactly when no `ell_i` vanishes identically on `ker L`, or
equivalently when none belongs to `rowspan L`.  Therefore any one of the
`28*6=168` pair/centre choices satisfying

```text
ell_i not-in rowspan(L_pqv) for i=0,1,2,3                 (5)
```

gives an active clean cap using only linear equations in `K`.  The W40
four-torus satisfies (5) at `(p,q,v)=(6,7,5)` with `K=I` identically.

This replaces the first attack on 729 cubic error coefficients by a finite
row-span disjunction.  The adversarial complement says that for every one
of the 168 choices at least one of four functionals belongs to the indicated
row space.  The next constructive lane intersects precisely that complement
with the raw level-4 equations; a separate builder tries to realize it.

A second first-wave output is an **unaudited candidate branch theorem** for
the fixed W33-D5 twisted-4+4 binary representative.  Treating all 140 cells
involving colour 2 as free, 21 raw coefficient equations have an explicit
integer-polynomial certificate of `1`.  In triangular form, 13 equations
kill auxiliary cells, seven equations kill every pure-colour-2 cell incident
with site 0, and the pure `22222222` equation then reads `0=1`.  Two of the
seven equations have the indispensable `(3,3,2)` profile.  A fresh audit is
rebuilding this certificate and its target-preserving gauge scope before the
result is eligible for any spine promotion.
