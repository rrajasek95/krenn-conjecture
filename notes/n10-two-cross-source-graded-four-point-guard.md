# An ordered two-endpoint grade repairs the explicit two-cross guard

## Outcome

The smallest source-provenance repair succeeds on the explicit witness

\[
 A_{10}(t,s)=A_8\otimes g_{89}+tE_{08;00}+sE_{19;00}.    \tag{1}
\]

Do not sum the ordered cross-pair contribution immediately into the ordinary
output tensor.  Retain its six-site coefficient

\[
                  K_{01}=H_{\{2,3,4,5,6,7\}}(A_8)       \tag{2}
\]

as a separate \(((0,8;00),(1,9;00))\)-graded component.  Inserting colour
zero at old endpoints 0 and 1 reconstructs the mixed \(ts\) output
coefficient exactly.

The grade has a single boundary slice which gives an exact four-cut guard:
it belongs to the coefficient cylinders on the fixed cuts \(2,3,4\), but
does not belong on any candidate fourth cut \(0,1,5\).  Even after enlarging
each cylinder by every \(1,t,s,ts\) coefficient of every literal N=10
cofactor column, the same slice remains outside on each candidate.  Thus a
source-graded fixed-three-plus-fourth system forces the ordered-pair scalar
\(ts\) to vanish.

The ordinary summand still reconstructs \(H_8\) and \(\Delta_{8,3}\)
exactly.  The grade and its guard are stable under an additional isolated
matched-pair lift, giving an exact N=12 to N=10 to N=8 contraction identity.

This is a source-graded counterguard, not yet a proof about the ordinary
ungraded cylinder equations.  A separate provenance-separation lemma would
be needed to show that ungraded completeness forces the graded equations.

## 1. The retained six-site cofactor

For the anchored source, the ordered-pair grade is

\[
\begin{aligned}
 K_{01}={}&e_{210000}-e_{000012}+e_{000000}.              \tag{3}
\end{aligned}
\]

The two cross cells fix colours zero at old vertices 0 and 1 and at new
vertices 8 and 9.  Let \(J_{01}^{00}\) insert the two old endpoint colours.
Exact multiaffine coefficient extraction gives

\[
 [ts]H_{10}(A_{10}(t,s))
       =J_{01}^{00}(K_{01})\otimes e_0^{(8)}\otimes e_0^{(9)}.       \tag{4}
\]

Both linear full coefficients \([t]H_{10}\) and \([s]H_{10}\) vanish.
Equation (4) is checked against the literal perfect-matching expansion; the
grade is retained before output summation and therefore does not confuse its
all-zero word with the target's all-zero word.

Define the graded four-point contraction by

\[
 \Gamma_{01}(A_{10})=
 \left(P_a([1]H_{10}),\ K_{01}\right),                 \tag{5}
\]

where the first component is ordinary and the second is tagged by the four
incident vertices \((0,8;1,9)\).  The target has only ordinary grade:

\[
                 \Gamma_{01}(\Delta_{10,3})
                         =(\Delta_{8,3},0).              \tag{6}
\]

The first identity is independent of the controller because
\(P_a(H_8\otimes g)=H_8\) for every old \(a\).

## 2. The boundary-012 guard

The middle term of (3) inserts to the old word

\[
                         -e_{00000012}.                  \tag{7}
\]

For every adjacent cut \(C_z=\{z,6,7\}\), \(0\le z\le5\), its boundary word
is \((0,1,2)\) and its five-site insertion-shore row is

\[
                              q=-e_{00000}.              \tag{8}
\]

Let \({\cal S}^{(8)}_z\) be the literal old cofactor-column cylinder.  Exact
normal forms of (8) are

| cut | normal form of \(q\) modulo \({\cal S}^{(8)}_z\) |
|---:|---|
| 0 | \(e_{63}\) |
| 1 | \(e_{63}\) |
| 2 | \(0\) |
| 3 | \(0\) |
| 4 | \(0\) |
| 5 | \(e_{21}+e_{150}\) |

Thus the ordered-pair grade passes the three fixed cuts and fails every
candidate fourth cut.  For any

\[
                    \{2,3,4,z\},\qquad z\in\{0,1,5\},   \tag{9}
\]

the graded equations on all four cuts force \(ts=0\).

## 3. The coupled coefficient-cylinder audit

The preceding old-cylinder reduction is transparent, but a grade-aware
cylinder can naturally be larger: cofactor columns themselves have
\(1,t,s,ts\) components.  The checker therefore constructs the maximal
coefficientwise coupled module

\[
 \widehat{\cal S}_z=
 \operatorname{span}_{\mathbb Q}
 \{[1]c_{h,i},[t]c_{h,i},[s]c_{h,i},[ts]c_{h,i}:h,i\}.   \tag{10}
\]

This includes the ordinary cofactor cylinder, both linear new-hole
families, and all quadratic old-hole cofactors.  It is deliberately a
superspace: failure modulo (10) cannot be repaired by choosing a smaller
source-graded cofactor module.

The exact audit is:

| cut | \(\dim\widehat{\cal S}_z\) | mixed residual rows outside | nonzero normal form |
|---:|---:|---:|---|
| 0 | 17 | boundary 012 only | \(e_{567}\) |
| 1 | 17 | boundary 012 only | \(e_{567}\) |
| 2 | 25 | none | -- |
| 3 | 25 | none | -- |
| 4 | 27 | none | -- |
| 5 | 24 | boundary 012 only | \(e_{189}\) |

This closes the cofactor loophole left open by merely reducing (8) modulo
the old cylinder.  In particular, the quadratic cofactor directions on cut
5 do not absorb the guarded mixed residual.

The audit is symbolic.  The four multiaffine corners recover coefficient
vectors exactly; they are not a search over values of \(t,s\).

## 4. Ordinary target reconstruction

For every old controller \(a\), the ordinary component satisfies

\[
 P_a(H_8\otimes g_{89})=H_8,
 \qquad
 P_a(\Delta_{10,3})=\Delta_{8,3}.                       \tag{11}
\]

The tagged component has target value zero by definition: it records a
specific ordered source pair, while \(\Delta\) is kept entirely in ordinary
grade.  This avoids the output-level collision which killed scalar
multitraces in the preceding note.

There is an important scope condition.  Equations (5)--(6) enlarge the data
retained from a finite source.  They are source-faithful, but they do not
descend to a function of the output tensor alone.  This is exactly why the
guard can distinguish two contributions to the same all-zero tensor word.

## 5. Forced-pair N-stability

Lift the old N=8 source once more by an isolated diagonal pair at vertices
8,9, and let a new outward cross pair use vertices 10,11.  Its ordered-pair
grade is

\[
                   K_{01}^{(8)}=K_{01}\otimes g_{89}.    \tag{12}
\]

The controlled trace on the appended old pair gives

\[
 P(K_{01}^{(8)})=K_{01},
 \qquad
 P(J_{01}^{00}K_{01}^{(8)})=J_{01}^{00}K_{01}.          \tag{13}
\]

On every cut, the boundary-012 guarded row contracts to the same
\(-e_{00000}\), with the same quotient normal form.  The ordinary component
and target contract exactly through

\[
                  N=12\longrightarrow N=10\longrightarrow N=8.    \tag{14}
\]

Therefore the grade and the nonzero counterguard stabilize on the isolated
forced-pair tower.  This is not full N-stability under arbitrary additions:
new sources incident to the intervening matched pair can create further
provenance grades and enlarge (10).  The next uniform theorem would need to
show that the direct sum of all ordered cross-pair grades remains separated,
or find the smallest cancellation between two such grades.

## 6. Remaining logical gap

The result proves the implication

\[
 \text{four complete **source-graded** cylinders}
       \quad\Longrightarrow\quad ts=0                  \tag{15}
\]

for the explicit pair.  It does not yet prove

\[
 \text{four complete ordinary cylinders}
       \quad\Longrightarrow\quad
 \text{four complete source-graded cylinders}.          \tag{16}
\]

Special-value cancellation between different provenance grades is the
only remaining escape in this bounded model.  Proving a torus-character or
filtration separation statement for (16), or finding an exact cancellation
counterexample, is now the sharp next step.  The explicit witness also
changes the colour-zero pure coefficient when \(ts\ne0\); any admissible
anchored N=10 source needs a compensating grade and must be tested together
with it.

## Reproduction

    python3 computations/verify_n10_two_cross_source_graded_four_point_guard.py
    python3 -O computations/verify_n10_two_cross_source_graded_four_point_guard.py
    python3 -I computations/verify_n10_two_cross_source_graded_four_point_guard.py
    python3 -S computations/verify_n10_two_cross_source_graded_four_point_guard.py

All matching expansions, coefficient modules, contractions, and normal forms
are exact over the rationals.
