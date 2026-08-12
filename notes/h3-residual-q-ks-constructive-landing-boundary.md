# The residual-q KS lift closes the endpoint holonomy but not transverse rank

## Conditional theorem

Assume the exact residual response Kodaira--Spencer lift isolated in
`h3-shared-four-term-endpoint-word-change-inventory-boundary.md`: in the
labelled repeated comparison component it transports

\[
 T_{\rm pure}=a_{24}^{11}a_{35}^{11}
 \quad\longrightarrow\quad
 T_{\rm mix}=a_{24}^{21}a_{35}^{12},
\]

cancels

\[
 (P_+-P_-)(T_{\rm pure}-T_{\rm mix}),                 \tag{1}
\]

and has zero ordinary-residue remainder, target, $W$, and anchor incidence.
Here “source-provenant” has the physically sharp meaning of
`h3-residual-q-physical-duality-interface-counterguard.md`: the correction is
a column of the complete augmented map in word `1211222` and the labelled
repeated `P3+K2` grade, includes the physical `eta_z` relations and terminal
row, and obeys facewise

\[
 d r_v(\eta_z)=-d\Omega_v(\eta_z)
              =1+\delta_{vz}u_z/t.                    \tag{2}
\]

This is a hypothesis on a physical lift, not something constructed by the
checker below.  Both possible in-image terminal branches are sufficient: a
zero-indeterminate lift gives the attachment directly, while nonzero terminal
value on the correction kernel is already the stronger relative-generator
exit.

Under this hypothesis, the mixed curvature/rootless-bar near-hit becomes the
literal four-term attachment

\[
 A=E_+-E_-+\Omega-q_{\rm comp}.                       \tag{3}
\]

The physical rootless bar is

\[
 B=-\Omega+q_{\rm comp}.
\]

Therefore the source-valid composition in the same repeated fine grade is

\[
                         A+B=D:=E_+-E_-.               \tag{4}
\]

Equation (4) has two immediate, and sharply delimited, consequences:

1. it kills the one-dimensional unequal-tail five-lock holonomy of
   `727de71`; and
2. together with the unique signless E14 response $S=E_++E_-$, it splits
   both private endpoint orientations.

It does **not** produce a transverse physical head, an avoiding pure target
matching, or a rank-$(3,3,3,3)$ pair.  Its unconditional constructive effect
after assuming the lift is a strict decrease of the typed-component
filtration.

Checker:
`computations/verify_h3_residual_q_ks_constructive_landing_boundary.py`.

## Unequal-tail five-lock landing

The all-five residual module has the ordered rows

```text
unary, 11, 12, unary, 21, 22
```

and seven relative vertices.  Giving the middle unary edge weights $(1,2)$
and every other edge weights $(1,1)$ yields row rank six in an ambient
seven-space.  Its endpoint dual has values

\[
                     \lambda(E_+)=1,
                     \qquad \lambda(E_-)=\tfrac12,
\]

so $D$ is absent.  The internal five-column lock still has full rank, and
the crossed `12` and `21` rows use distinct ports; hence neither the
same-star dependence nor complementary-wedge exit is being smuggled in.

Adjoining (4) raises the row rank from six to seven.  Thus the relative
cokernel is zero.  This is stronger than formally rescaling the unequal
path: the hypothesized correction first makes (3) a source-valid row with
all protected readouts zero, and only then is it composed with the already
physical bar.  The endpoint determinant is consequently in the literal
source-row image of the repeated-grade quotient.

So, conditional on applying the KS lift in the selected marked tail orbit,
the injective/no-complementary-wedge five-lock provenance residual is closed.

## E14 self-loop landing

The complete unary plus four-response inventory has exactly one correct-tail
endpoint hit, and its coefficients are

\[
                           S=E_++E_-.                  \tag{5}
\]

The canonical E14 first-hit module before the new attachment has 269 columns
of rank 269 and a rational dual pairing $-1$ with the private residual.  This
is the frozen self-loop: reducing the private tail through the old response
rows can return the same endpoint orientation.

Equations (4)--(5) instead give, over the complex source field,

\[
 E_+=\frac{S+D}{2},
 \qquad
 E_-=\frac{S-D}{2}.                                   \tag{6}
\]

The endpoint quotient rank rises from one to two.  In the routed endpoint
and tail quotient, the private E14 orientation is now in the source-row span,
so reduction cannot leave another copy of that orientation.  This closes the
E14 self-loop under the exact KS hypothesis.  It does not reconstruct the
full Spencer chain realizing the hypothesis.

## What decreases

Use the conditional sequential potential already frozen for the C6 route,

\[
 \Phi=(\hbox{total endpoint support},
        \hbox{number of unresolved typed base components}),              \tag{7}
\]

ordered lexicographically.  The KS landing does not delete a physical source
coefficient.  Instead, it resolves one marked endpoint/tail orbit while
preserving endpoint support:

\[
                         (s,c)\longmapsto(s,c-1).       \tag{8}
\]

This is a strict, well-founded decrease.  In particular the routed E14
self-loop changes $(s,1)$ to $(s,0)$ rather than returning to $(s,1)$ by a
new witness choice.  The checker verifies (8) on a finite rectangle only as
a replay of lexicographic strictness; the mathematical statement follows
directly for every $c>0$.

The gain is therefore **termination/provenance**, not transverse rank.

## First remaining physical guards

The KS attachment has target and anchor-incidence readouts zero.  Its two
endpoint orientations live in the response/source-word factor, so their
independence cannot by itself change the local physical rank matrix.  Three
already frozen modules locate the first independent guards precisely.

### 1. Same-head local rank guard

For a minimum axis circuit with three active colours, the complete response
tail rank is three but the local outer-head span has rank one.  The four
deleted-star ranks are

```text
2, 2, 3, 3.
```

Thus the first anchor-contained rank statement still needed is:

> a source-labelled occupied tail lies on a transverse local outer head with
> nonzero cofactor and supplies both missing rank-three minors, or it enters
> an already strict/effective Hall envelope.

Endpoint orientation rank two is not a substitute for this statement.

### 2. Outside-arm target-coloop guard

In the full unary/`11`/`12`/`21`/`22` boundary, both response modules have
column rank three and joint-kernel dimension zero, yet their pure target is
supported only at port zero.  Restoring the outside arm therefore still
requires an avoiding nonzero pure target matching or an additional physical
source column raising both deficient stars.  The KS row, whose target is
zero, supplies neither.

### 3. Opposite Hall-star guard

If the carrier passes to the opposite Hall star, the exact residual is the
existing alternative:

* the unary bridge is dark on the two effective leaf spans; or
* the three surviving blocks obey

\[
                          B_{ab}+A_{Rc}+A_{Pc}=0.       \tag{9}
\]

The next Hall theorem must exclude bridge darkness or straighten one anchor
correction into a free/effective carrier.  Existing strict Hall envelopes
remain closed; (9) is the first non-strict anchor-contained guard.

These are structural source-labelled modules, not asserted full GHZ
sources.  They show exactly why the KS boundary data alone cannot imply the
missing rank theorem.  A global incidence theorem may still exclude all
three.

## Updated frontier

Conditional on the residual-q KS lift, the endpoint/tail provenance branch
is finished: the unequal-tail five-lock and E14 orientation self-loop both
land, and repeated use strictly decreases (7).  The fastest downstream
target is now a source-labelled local-rank restoration theorem:

> every KS-resolved occupied common-tail carrier either meets an avoiding
> pure target matching, supplies a transverse outer head with both deficient
> rank-three minors, or enters the effective strict Hall envelope.

The exact exceptions that theorem must rule out or absorb are the
target-family coloop, the same-head $(2,2,3,3)$ carrier, and the opposite
Hall-star bridge-dark/three-block triangle lock.  No further endpoint
holonomy statement is required on this branch.

## Verification

Run:

```text
python3 computations/verify_h3_residual_q_ks_constructive_landing_boundary.py
python3 -O computations/verify_h3_residual_q_ks_constructive_landing_boundary.py
python3 -I -S computations/verify_h3_residual_q_ks_constructive_landing_boundary.py
```

The checker pins the exact residual-q mismatch, unequal-tail five-lock,
canonical E14 first-hit module, sequential potential, local rank guard,
full-five target coloop, and Hall bridge/triangle boundary.
