# The first intrinsic condition after labelled GHZ normalization is a shared Hessian

## Result

The latent involution and the exact labelled quotient criterion do not ensure
that the nine cross tensors arise from one physical residual quadratic (q).
The missing source condition has a direct finite form: every word slice must
factor through the same deleted-word Hessian

\[
 H=q^{[2]}.
\]

For residual sites (U=\{0,\ldots,5\}), a pair (e=\{x,y\}), and a word
(ar w) on (U\setminus e), define

\[
 H_{e,\bar w}
 =\bigl[q^{[2]}\bigr]_{\bar w}
 =\operatorname{haf}_{\bar w}(q|_{U\setminus e}).       \tag{1}
\]

For physical endpoint stars (p_i,s_j), every common-(q) realization obeys

\[
 \boxed{
 C_{ij,w}=\sum_{x<y}
 \bigl(p_i(x,w_x)s_j(y,w_y)+p_i(y,w_y)s_j(x,w_x)\bigr)
 H_{xy,w|_{U\setminus\{x,y\}}}.}                        \tag{2}
\]

Equation (2) is independent of the involution equations and the GHZ slice
rank conditions.  A formal tensor can satisfy both earlier layers and fail a
single coefficient of (2).

The exact checker is
[`verify_h3_common_q_hessian_realization_gate.py`](../computations/verify_h3_common_q_hessian_realization_gate.py).
It uses only literal source variables, word labels, deletions, and divided
matching powers—no auxiliary (B/\mathrm{Eq}), (Gamma), or AugP2 axes.

## 1. First derivative and deletion conventions

Write

\[
 Q_w=[q^{[3]}]_w.
\]

For the decorated edge coordinate (q_{xy}(w_x,w_y)), differentiating the
perfect-matching sum selects precisely the matchings containing (xy):

\[
 \frac{\partial Q_w}
 {\partial q_{xy}(w_x,w_y)}
 =H_{xy,w|_{U\setminus\{x,y\}}}.                        \tag{3}
\]

There is no factorial in (3).  The divided power (q^{[3]}) contains every
unordered perfect matching once, and deleting its distinguished edge leaves
the four-site divided square (q^{[2]}), again with every matching once.

The key cross-word information is visible in the indexing of (1):
(H_{xy,\bar w}) does not depend on the two letters reinserted at (x,y).
The same coordinate is reused by all nine extensions of (ar w).  An
arbitrary family of 729 three-by-three matrices has no reason to admit this
shared deletion table.

Multiplying the selected cofactor (3) by the endpoint response coefficient

\[
 R_{ij,xy}(w)=
 p_i(x,w_x)s_j(y,w_y)+p_i(y,w_y)s_j(x,w_x)               \tag{4}
\]

and summing over the 15 residual pairs gives (2).

## 2. The finite polynomial appendage

The full common-power realization can be appended to the system with the
following literal variables and equations.

1. If (Q) is not already defined from (q), add the 729 cubic equations

   \[
   Q_w=\operatorname{haf}_w(q).                          \tag{5}
   \]

2. Add the (15\cdot3^4=1215) deleted Hessian coordinates and their
   three-term four-site hafnian equations

   \[
   H_{xy,\bar w}=q_{ab}q_{cd}+q_{ac}q_{bd}+q_{ad}q_{bc}, \tag{6}
   \]

   where (a,b,c,d) are the four remaining sites and every (q)-cell carries
   the letters prescribed by (ar w).

3. Add the (9\cdot3^6=6561) response equations (2).

Equations (6) ensure that the deletion tables come from one common (q), not
from independent formal cofactors.  They also carry the first Schreyer or
mixed-partial compatibility.  If (e,f) are disjoint decorated edges and
(g) is the remaining edge, then

\[
 \frac{\partial H_e}{\partial q_f}=q_g
 =\frac{\partial H_f}{\partial q_e}.                    \tag{7}
\]

For overlapping edges both derivatives are zero.  The checker verifies (3)
on all (15\cdot729=10935) edge-word slots, (7) on all
(90\cdot729=65610) ordered disjoint-edge slots, and (2) on all 6561
endpoint-row/word slots.

This is presentation-efficient rather than equation-minimal: eliminating
the (H)'s recovers the direct quartic source equations.  Its value is that
it exposes exactly which cross-word cofactor must be shared, so a failed
coordinate has an unambiguous physical deletion label.

## 3. A formal exact-nine tensor with no fixed-source lift

Use the literal 77-cell N=8 guard at endpoints ((2,3)), with residual sites
((0,1,4,5,6,7)).  Let (C^{\rm phys}_{ij}=p_is_jq^{[2]}) be its actual
cross tensors.  They satisfy all 1215 equations (6), all 6561 equations (2),
and the mixed-partial identities (7).

The guard misses only the pure (0^8) and (1^8) target normalizations.
Repair these **formally** by setting

\[
\begin{aligned}
 C^{\rm form}_{00}&=C^{\rm phys}_{00}+X_0,\\
 C^{\rm form}_{11}&=C^{\rm phys}_{11}+X_1,\\
 C^{\rm form}_{ij}&=C^{\rm phys}_{ij}\quad\text{otherwise}.
\end{aligned}                                            \tag{8}

With the same direct block (a) and the same (q^{[3]}), (8) satisfies all
nine exact coarse equations

\[
 a_{ij}q^{[3]}+C^{\rm form}_{ij}=\delta_{ij}X_i.         \tag{9}

Its quotient slices are exactly

\[
 E_{00},E_{11},E_{22},                                  \tag{10}

\]

so it passes the 27 slice-minor equations and both rank-three factor-span
opens from `81bbb0f`.  Since the change in (8) lies inside (W), it is also
invisible to all (W^\perp) anticommutators.  Thus (8) passes every earlier
involution/GHZ-normalization test.

It fails common-(q) realization in exactly two source-labelled coordinates:

\[
 (i,j,w)=(0,0,0^6),\qquad(1,1,1^6),                     \tag{11}

\]

both with residual (+1).

## 4. The smallest failing identity

At the first coordinate in (11), the only nonzero response-edge coefficient
in (4) is

\[
 R_{00,01}(0^6)=23.
\]

Its complementary four-site common-(q) cofactor is

\[
 H_{01,0^4}=0.
\]

Every other term of (2) is identically zero.  Therefore the literal physical
identity is

\[
 [C_{00}]_{0^6}=23H_{01,0^4}=0.                         \tag{12}

\]

The formal GHZ repair (8) requires its left side to be one.  Hence the first
independent appendage can be the single scalar equation

\[
 \boxed{1=23\cdot0,}                                    \tag{13}

\]

with the pair, word, endpoint labels, and deleted cofactor all retained.
This is not a disguised GHZ rank failure: (10) is the exact normalized
diagonal tensor.  It is not an involution failure either: adding (X_0) lies
in the quotient-killed target span.  Equation (13) detects only the missing
common-power/source realization.

## 5. Exact scope and next use

The no-lift statement fixes the literal residual quadratic (q) and the six
physical endpoint stars (p_i,s_j).  It proves that (8) cannot be obtained by
those source data.  It does not exclude a completely unrelated
refactorization with new stars, nor a different quadratic (q') having the
same cubic tensor (q'^{[3]}=q^{[3]}).  Excluding those possibilities would
require eliminating the variables in (5)--(6), rather than evaluating them
on one fixed physical chart.

For the intrinsic proof, the useful finite hierarchy is now:

1. solve the involution/containment equations;
2. impose the exact labelled slice criterion;
3. impose the shared Hessian equations (5)--(7) and reconstruction (2);
4. only then test the common direct matrix and scalar-zero selected-line
   compatibility.

The formal repair (8) proves that step 3 is logically independent of steps
1--2 and can fail at one literal coefficient.

## Reproduction

The checker uses exact rational arithmetic and passes normal, optimized,
isolated, no-site, isolated-no-site, and byte-compilation modes.  Its frozen
ledger digest is

```text
32e0e3257c226402e10868d184094b4dcc5e52d879dc2f41e502199d7781435c
```

