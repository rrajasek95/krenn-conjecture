# The weakest intrinsic constructive object is one physical clean-cap witness

## Outcome

The constructive branch does not need a global `Phi`, a quasi-isomorphism
between the response and cap resolutions, an underived representative `r0`,
or an absolute decorated `Eq` contraction.

For an actual normalized exact source `A`, the weakest sufficient positive
datum is one tuple

\[
                       (p,q,K),                         \tag{1}
\]

where `p,q` are physical sites and
`K in (V_p tensor V_q)^*` is an actual covector satisfying

\[
 s_A(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0,
 \qquad {\cal E}_{p,q,A}(K)=0.                          \tag{2}
\]

Here `s_A(K)` is contraction with the physical edge block, the three
`kappa_c` are contractions with the three pure target directions, and
`E=0` is the proved clean-cap equation.  Once (1)--(2) are established in
the original source algebra, the existing clean-pair theorem constructs the
`N-2` source and contradicts minimum order.  No occurrence resolution is
logically needed after that point.

There are two other sufficient objects, but they answer different proof
questions:

1. a selected-carrier intrinsic coefficient factorization can give a local
   source contradiction before choosing `K`; and
2. a Fredholm covector on the complete physical presentation can close the
   terminal branch when no constructive witness is produced.

Conflating these three objects has made the local comparison look stronger
than the proof actually requires.

## 1. The three logically separate interfaces

| interface | weakest sufficient statement | what it yields |
|---|---|---|
| selected coefficient comparison | identify the two protected readouts on the chosen carrier with two equal intrinsic EqSystem composites | immediate contradiction to a nonzero `B-Eq` landing |
| physical cap selection | exhibit one actual `(p,q,K)` satisfying (2), or a conservative selected-carrier evaluation which produces it | clean-pair descent to order `N-2` |
| terminal/Fredholm | construct a covector on the full actual same-grade Macaulay/Jacobian image, nonzero on the required right-hand side | accepted terminal contradiction |

The first two are local and constructive.  The third is universal and must
survive every physical primitive column.  Neither local statement implies
the Fredholm one.

## 2. Minimal coefficient-only contradiction

The official EqSystem already has the exact divided-root/restriction
identity

\[
 I_cD_c\Phi_{\rm div}d
   =dI_c(\Phi_{\rm div})_{\widehat q}D_r                 \tag{3}
\]

for both `q23` and `q45`.  Commit `5771e31` verifies (3) on all 6,561
equation words, all 105 matching occurrences, and the marked collision
descendants.  Thus the intrinsic path commutator is zero.

A complete local `Phi` is unnecessary to use (3).  It would suffice to
prove, only on the selected normalized endpoint-even carrier, that

```text
protected B augmentation   factors through the left side of (3),
protected Eq augmentation  factors through the right side of (3),
```

with identical normalization and with the hidden
`lower/private=-E`, `word-resolved ores=+E` faces retained.  Then (3) forces
`B=Eq` on the actual source, while the required landing is

```text
actual tied image       (delta_plus,delta_plus),
required physical image (delta_plus,0).
```

The integral anti-diagonal detector reads `0` on the first and `3` on the
second.  This is an immediate source contradiction.

This statement is strictly weaker than a chain map on the entire response
complex: it concerns two composites on one selected carrier and their first
proper faces.  It is also not yet proved.  The original EqSystem has one
occurrence copy, whereas `B/Eq` is a doubled protected presentation.  The
factorization of those copies through (3), not equation (3) itself, is the
missing source-provenance theorem.

## 3. Minimal physical-cap construction

If the proof attacks descent directly, even the protected factorization is
avoidable.  One may choose `K` by any argument intrinsic to the actual
source equations and verify (2) directly.

The marked machinery is useful only as a possible selection mechanism.  In
that formulation the minimum map is a conservative partial evaluation

\[
 j_A:C_{\rm selected}\longrightarrow
       \operatorname{Cap}_{\rm phys}(A;p,q)             \tag{4}
\]

such that one selected class maps to the actual `K` of (1), physical
cofactor contraction agrees on the faces consumed by descent, and target
nonvanishing is reflected.  There is no need to define (4) on unrelated
resolution generators.

If `K`, its activity, and its clean error are checked directly, the
following hypotheses are unnecessary for the constructive branch:

* essential surjectivity onto all cap primitives;
* acyclicity of the augmented comparison cone;
* a chosen underived `r0` top;
* an absolute `dK_Eq=E` cell;
* extension of the protected Eq dual to a terminal; and
* preservation of `W/ridge/eta/sigma` rows not used by clean descent.

They become relevant only when the PAComp chain ladder is used to prove the
landing, or when one seeks a universal Fredholm alternative.

## 4. What the marked/divided-root construction actually supplies

The current positive chain is substantial:

1. `d97bf7a`: with parent/fine/reinsertion marks retained, response and
   marked cap totalizations resolve the same 90-parent module;
2. `d1215e0`: a source-derived six-root product supplies the physical
   response-to-cap word change;
3. `174c9ac` and `c3f6231`: multiplicity-divided roots transport all marked
   collision faces and construct both `q23/q45` P2 restrictions;
4. `1767822`: the lower coefficient maps canonically name `B1/B4` and the
   first `q/dq` detector survives;
5. `5771e31`: the corresponding restriction commutator is identically zero
   in the official EqSystem; and
6. `13c0db4`: endpoint polarization extends the selected word coefficient
   to a rank-nine evaluation natural in an arbitrarily supplied physical
   covector `K`.

This closes coefficient, word, fine, repeated-site, restriction,
reinsertion, first principal-parts, target, and endpoint-evaluation
naturality.

It stops at **selection**, not evaluation.  A fixed word observes only
`K_22`; the polarized nine-word family evaluates all nine coordinates but
does not choose common coefficients `K_ab`.  It therefore proves neither

\[
 s(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0
 \quad\text{nor}\quad {\cal E}(K)=0.                    \tag{5}
\]

The canonical fixed-word lift `K_22 E_22` is physical but inactive.  The
identity completion is active only when its scalar is nonzero and is clean
only when the known nonlinear identity-cap error vanishes.  Those are new
source consequences, not formal outputs of divided-root naturality.

The protected chain also still lands tied `B=Eq`.  This is fatal if the
chain is asked to realize the physical `B`-only PAComp landing, but it is not
an independent obstruction after an actual `K` satisfying (2) has been
constructed directly.

## 5. What the intrinsic `K3,3` work supplies

The recent matching work is already in the original coefficient equations,
so it bypasses the marked-presentation issue entirely.

* `eaff4ab` closes the first exact-minimum singleton-free repair by the
  even/odd `K3,3` permanent-triangle Laurent unit `1=-1`.
* `8e83f10` proves that every outside fine returns to a literal common-tail
  `C4`, while a tail-free factor triple closes immediately to the full
  six-term permanent.
* `64e98dc` gives an all-nonzero full-permanent guard with permanent zero and
  all nine `2x2` permanental cofactors nonzero.  Thus the six-term fibre is
  coefficient-compatible and is not forced clean.
* `1a26bbf` closes every cardinality-minimum repair of the canonical
  minimum-pure-debt completion by a new literal mixed singleton.

Therefore `K3,3` presently gives many direct source-unit exits, but not a
global clean-cap selection theorem.  Its exact stopping point is recursive:
the other minimum pure completions, nonminimum mate packets, and paths whose
spectator tail changes are not yet classified.  The first all-order
common-tail lift is formal; the first changing-tail obstruction is the
physical `K2,2` binomial

\[
 a_{01}a_{23}(a_{45}a_{67}+a_{46}a_{57}).               \tag{6}
\]

Thus this route can still finish by a well-founded unit/clean-cap/support
descent without ever constructing `Phi`.

## 6. Why Fredholm remains separate

Normalization makes the selected `N -> B` coefficient map valid because
the defect `(H0-u)E` vanishes.  It does not kill the protected class `E`:
the comparison cone retains an `H0` class, and a relative `dK=(H0-u)E`
becomes a new cycle after base change.  This is the exact counterexample to
promoting the constructive top map to a terminal.

An accepted Fredholm object must be a covector on the actual physical
same-grade module, annihilating every column of the official
EqSystem/Macaulay presentation and pairing nontrivially with the physical
right-hand side.  A dual on a declared operation grammar, the protected
`B-Eq` anti-diagonal before source factorization, or the extra homology of
the marked resolution is not enough.

The terminal route therefore needs one of:

1. an absolute source-derived decorated `Eq` contraction;
2. a canonical protected jet functor proved complete for all physical
   primitive columns; or
3. a direct finite Macaulay left-null certificate on the original enriched
   source presentation.

This is strictly stronger than either (3) on one carrier or the physical
cap witness (1)--(2).

## 7. Ranked attacks

### 1. Intrinsic repair descent

Extend the literal `K3,3`/parent repair DAG through nonminimum mates and the
first changing-tail `K2,2` packet.  The success certificate is a
well-founded trichotomy at each recurrent packet:

```text
mixed singleton or polynomial unit
  / active clean physical cap
  / strict occupied-support or tail reduction.
```

This is currently the shortest route because every input and output is
already source-provenant and several minimum layers are closed.

### 2. Direct physical `K` selection

Use the rank-nine endpoint-polarized evaluation only as a coordinate chart,
then prove existence of one common `K` satisfying (2) from the actual source
identities.  A successful certificate is an explicit formula for `K`, or a
saturated-ideal/resultant argument showing that the clean cubic has a zero
outside the activity divisors.  A valid failure certificate is an exact
source-compatible fibre with no active clean `K`, not merely a fixed-word
rank-one observation.

### 3. Selected protected factorization

Construct the two source factorizations around (3) only on the selected
carrier, including the hidden `-E/+E` faces.  Equality gives an immediate
coefficient contradiction.  Inequality on one literal face is the sharp
no-go and should redirect work to attacks 1--2.  Building a global `Phi`
before this local test is unnecessary.

### 4. Physical Fredholm promotion

Enumerate or characterize every actual same-grade primitive and extend the
Eq covector across them.  This remains the most expensive route because
canonicity and essential completeness are load-bearing, whereas neither is
needed for constructive descent.

## Bottom line

The proof should ask first for one physical consequence of the source:

```text
one active clean K, one literal unit, or one strict support-lowering move.
```

The marked-derived comparison has already supplied the coefficient
transport needed to investigate such a consequence, but it has not selected
the physical `K`.  The `K3,3` route has supplied several intrinsic units but
not a terminating all-order recurrence.  A global `Phi` or Fredholm
quasi-isomorphism is sufficient, not minimal, and should remain a fallback
rather than the entry condition for the constructive proof.
