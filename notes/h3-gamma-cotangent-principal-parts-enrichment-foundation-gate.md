# The Gamma detector does not descend to the canonical cotangent complex

## Outcome

Let

\[
 R=k[x_{ij}^{ab}],\qquad I=(F_w:w\in\{0,1,2\}^8),\qquad A=R/I
\]

be the official `EqSystemN 8 3` presentation.  Its canonical first-order
source object is

\[
 L_{A/k}=[I/I^2\longrightarrow \Omega_{R/k}\otimes_R A].       \tag{1}
\]

The fixed `Gamma_*` terminal is **not presently a class of (1)**.  EqSystem
has an honest site-colour multigrading after a minimal three-homogenizer Rees
repair, but it does not define the fine `t*q_(v,N)`, repeated `P3+K2`,
response/cap operation, or `B/Eq` axes.  More decisively, the normalized
`B-Eq` detector is nonzero on the kernel of the forgetful map from the two
presentation copies to the common cotangent occurrence.  It therefore does
not descend to a covector on (1), and its local one-dimensional cokernel line
cannot yet be identified with `Ext^1_A(L_A/k,M)` or a canonical `T^1` piece.

There is nevertheless a finite positive coefficient theorem.  Once the six
literal squarefree fine slots are chosen externally, every degree-complementing
Macaulay multiple is one of `48` divisor/complement pairs, and their six
Boolean Taylor complexes have differential ranks `6,12,6`.  Ordinary higher
Schreyer cells resolve kernels and cannot enlarge the degree-one image.

The exact remaining loophole is a shifted operation cell.  The actual
Koszul cell

\[
 \theta=\epsilon_F\wedge\epsilon_Q,
 \qquad d\theta=F\epsilon_Q-Q\epsilon_F                \tag{2}
\]

can be given horizontal response-to-cap degree `-1`; after totalization it is
a relative degree-one primitive with Eq-only boundary.  It has normalized
detector charge `-1`.  This is an admissible enriched counterguard, not an
assertion that a decorated GHZ source contains it.  Excluding it requires one
precise new axiom: operation-support conservativity/no orphan horizontal
desuspensions in a source-defined enriched cotangent complex.

Checker:
[`verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py`](../computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py).

## 1. The canonical grading that EqSystem really has

There are

\[
 {8\choose2}3^2=252
\]

oriented colour-edge variables and `3^8=6561` equations.  Each equation is a
sum over the `105` perfect matchings.  Put

\[
 \deg x_{ij}^{ab}=e_{i,a}+e_{j,b}\in\mathbb N^{24}.       \tag{3}
\]

Every matching monomial in the word row `F_w` then has degree

\[
 g_w=\sum_{i=0}^7 e_{i,w_i}.                            \tag{4}
\]

The checker verifies (4) on all

\[
 6561\cdot105=688905
\]

official monomial occurrences.

The mixed zero-target equations are homogeneous.  A pure equation is
`F_(c^8)-1`, so it is not: its two terms have degrees `g_(c^8)` and zero.
One common homogenizer cannot repair all three pure equations because the
three degrees are distinct.  The minimal multigraded Rees repair adjoins

\[
 u_0,u_1,u_2,\qquad \deg u_c=g_{c^8},                  \tag{5}
\]

and replaces `F_(c^8)-1` by `F_(c^8)-u_c`.

Equations (3)--(5) give an honest word **degree**, not a word idempotent.
For example, the product of two degree-`g_w` elements has site weight `16`,
not the site weight `8` of another word row.  Thus the homogeneous
decomposition does not by itself provide the word projectors used by the
physical mapping-cylinder grammar.

The full monomial-exponent grading does not help.  At the cap word
`01211222`, the `105` perfect-matching monomials have `105` distinct degrees
in `N^252`.  Hence `F_01211222` is not homogeneous in that grading.  A marked
fine occurrence is a term or presentation slot, not a grading of `A` or
`L_A/k`.

## 2. Which Gamma axes fail to be canonical

The following distinction is now exact.

| `Gamma_*` axis | status in the Rees cotangent complex |
|---|---|
| site-colour word | honest `N^24` degree |
| fine `t*q_(v,N)` | not homogeneous; marked term slot |
| repeated `P3+K2` | chart/deletion shape, not a defined filtration |
| response/cap/`AugP2`/`K_Eq` | no operation idempotents in `R`, `I`, or (1) |
| `B/Eq` | two enriched presentation copies, not a cotangent direct sum |
| root/window/protected rows | external augmentation labels/readouts |

Consequently there is no defined functor

\[
 \operatorname{gr}_{\Gamma_*}L_{A/k}\longrightarrow
 Y_{\Gamma_*}^{B\oplus Eq}                            \tag{6}
\]

whose degree-one image is the physical primitive registry.  Calling the
existing local cokernel an Ext class before constructing (6) is not merely
unproved; the proposed class fails the elementary descent test below.

## 3. Exact non-descent of the normalized detector

On the top occurrence orbit, write

\[
 W=B\oplus Eq=\mathbb Q^4\oplus\mathbb Q^4.
\]

The minimal forgetful map to the common coefficient occurrence is

\[
 f:W\longrightarrow\mathbb Q^4,\qquad f(b,e)=b+e.      \tag{7}
\]

Therefore every covector pulled back from the cotangent occurrence has the
tied form

\[
 f^*(\lambda)=(\lambda,\lambda).                       \tag{8}
\]

Put

\[
 \delta=(1,1,-1,-1),\qquad
 \omega=(\delta,-\delta).                              \tag{9}
\]

The tied pullbacks have rank `4`; adjoining `omega` raises their rank to `5`.
More intrinsically,

\[
 f(\delta,-\delta)=0,
 \qquad \omega(\delta,-\delta)=8.                     \tag{10}
\]

Thus `omega` is not the pullback of any functional on the canonical
cotangent occurrence.  The normalized functional `omega/4` takes value
`-1` on the Eq-only orbit `(0,delta)`.

The callable enriched cap presentation still has exact `B/Eq` rank `7/8`,
and all `128` callable columns are killed by (9).  This proves a
one-dimensional **enriched presentation detector**.  Equation (10) proves
that it is not, with the present definitions, a one-dimensional cotangent
`T^1` class.

## 4. Finite Taylor/Schreyer theorem for the coefficient part

The six literal selected cofactors are

```text
q45  q23  q35  q24  q34  q25.
```

For each one, the externally selected fine multiplier has three squarefree
factors, abstractly `(t_i,q01,q_i)`.  A degree-complementing relation
multiple is uniquely determined by choosing a subset of those three factors.
Thus there are exactly

\[
 6\cdot2^3=48                                      \tag{11}
\]

divisor/complement pairs, with relation-degree distribution

\[
 6,18,18,6.                                         \tag{12}
\]

Contraction by `(1,1,1)` on one exterior Boolean complex gives

\[
 0\to\mathbb Q\to\mathbb Q^3\to\mathbb Q^3
   \to\mathbb Q\to0
\]

with ranks `1,2,1`; the six copies therefore have ranks `6,12,6`.  The
checker constructs the signed matrices, verifies `d^2=0`, and verifies exactness
in both middle degrees.

This proves:

> Once a squarefree fine slot is externally fixed, all of its
> degree-complementing Macaulay multiples and unshifted Taylor/Schreyer
> syzygies are finite and exhaustive.  Higher cells land in the kernel of
> the already fixed `d1`, so they cannot add a new `C1 -> C0` image.

The qualification is load-bearing.  Equation (11) does not make the six fine
slots into a canonical summand of (1), nor does it classify cells whose total
degree is changed by a new operation direction.

## 5. The smallest shifted exotic

Take the actual equations

\[
 F=H_0-u,\qquad Q=Eq.
\]

Their canonical Tate model contains (2).  After relative base change `Q=0`
and the committed sign choice `C_K=-theta`, its boundary is

\[
 dC_K=-F e_{Eq}.                                     \tag{13}
\]

The literal five-face Hasse packet realizes the same top commutator:
all `15` deleted-face/matching cubes have top `r0-T`, while a checked cube has
zero target and ordinary residue and diagonal-projection commutator
`(H0-u)eq`.

Now form a bicomplex enrichment and assign `theta` horizontal operation
degree `-1` from response to cap.  Its total degree is `2-1=1`; denote it

\[
 \Omega_{\mathrm{shift},0102}
   =\Sigma^{-1}_{\mathrm{response}\to\mathrm{cap},\Gamma_*}\theta.
                                                               \tag{14}
\]

It has literal relative boundary (13), `B/Eq` top orbit `(0,delta)`,
normalized detector charge `-1`, and `d^2=0` by the Koszul identity.  Forgetting
the horizontal enrichment leaves the already canonical vertical cell
`theta`.  Thus adjoining (14) does not change the official EqSystem or its
cotangent shadow, but it does change the enriched relative-`C1` image.

This is the requested explicit admissible exotic.  It is not a physical
counterexample: the checker does not construct its word/fine/repeated/root,
target, `q`, anchor, residue, `W`, or ridge faces in a full decorated GHZ
source.  It proves that those data—or an axiom excluding their independent
choice—are indispensable to essential surjectivity.

## 6. Exact conditional essential-surjectivity theorem

Assume a source-derived enrichment with:

1. honest response and cap operation idempotents;
2. one primitive nonidentity edge `Phi_KS,r0:response -> cap`;
3. operation-support conservativity: every horizontal desuspension is induced
   functorially by an actual lower operation arrow;
4. the standard word/`K_Eq` interchange laws; and
5. objectwise Hasse/Taylor/Schreyer exactness.

There is no composable pair of nonidentity operation edges in the graph

```text
response  ----Phi---->  cap.
```

Therefore no higher operation word can produce another off-diagonal primitive.
The only mixed word/`K_Eq` interchanges are the eight one-root instances

```text
0012  0102  0110  0111  0122  0212  1112  2112.
```

Their strict product boundary is tied, `(v,v)` in `(B,Eq)`, so all eight are
`omega`-dark.  Under hypotheses 1--5, every relative degree-one
operation-changing primitive is canonical, dark, or one of these eight.

This is the desired finite multigraded Taylor/Schreyer theorem **conditional
on a genuine enriched source and the no-orphan axiom**.  EqSystem alone does
not supply hypotheses 1--3, so it cannot promote the local detector.

## 7. Minimal foundational repair

Define a `GammaCotangentEnrichment` consisting of:

1. a filtered/dg `A`-bimodule `L_tilde` with orthogonal response/cap operation
   idempotents;
2. a conservative forgetful comparison from `L_tilde` to (1), or to its
   three-`u` Rees model;
3. honest fine, repeated, window and root filtrations;
4. a `B/Eq`-separated associated-graded chain map to the complete protected
   row object;
5. completeness for physical relative-`C1` primitives in the kernel of the
   forgetful comparison; and
6. operation-support conservativity/no orphan desuspensions.

The concrete source-derived candidate is now sharply located: start with the
`159` site-repeating Taylor/Spencer pair coordinates, contract each shared-site
pair to its doubled/missing-site `P3+K2` cap occurrence, and then apply the
proven `21`-pair full-star average.  This is not already a quotient of (1); it
is proposed data for `L_tilde`.  Its first decisive test is the literal chain
map equation on the actual `8580` order-six columns, retaining all
word/fine/repeated/operation labels.

Only after that construction is made can one meaningfully compute the
enriched `Ext^1` piece and decide whether it contains no bright class, exactly
the eight dark `kappa` interchanges, or the shifted class (14).

## Verification

Run:

```bash
python computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py --mode all
python computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py --mode cotangent
python computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py --mode grading
python computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py --mode macaulay
python computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py --mode omega
python computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py --mode exotic
python computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py --mode conditional
python computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py --mode contract
```

Each mode recomputes and pins the same exact ledger.
