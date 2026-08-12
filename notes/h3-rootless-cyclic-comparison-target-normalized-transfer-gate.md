# Target normalization does not supply the cyclic comparison base vertex

## Exact transfer calculation

Work in the common degree \(M=abcde\), after the selected \(C_5\) cells
have been Laurent-normalized.  Let \(C_i\) be the five formal physical
comparison vertices in cyclic order \((1,3,5,2,4)\).  The desired cyclic
package is

\[
                         A=\sum_i C_i,
 \qquad (\operatorname{low},\operatorname{ainc},W,
          \operatorname{tgt},\operatorname{ores})(A)
                         =(5,0,0,0,0).                 \tag{1}
\]

Commit `c094bbb` constructs the target-normalized unary lift

\[
 x=R-T-Y\rho+Yd_{\rm ores},\qquad
 (\operatorname{low},\operatorname{ainc},W,
          \operatorname{tgt},\operatorname{ores})(x)
                         =(1,-1,0,0,0).                \tag{2}
\]

Put

\[
                         g_i=C_i-x.                    \tag{3}
\]

Then \(g_i\) has signature \((0,+1,0,0,0)\), so \(-g_i\) is already
the primitive relative-anchor signature.  The source-valid adjacent
comparison squares provide only

\[
                         E_i=g_i-g_{i+1}=C_i-C_{i+1}. \tag{4}
\]

Their saturated incidence lattice has rank four.  It is killed by the
primitive face-sum covector \(\epsilon\), while

\[
 \epsilon(x)=0,\qquad \epsilon(A)=5,
 \qquad \epsilon(A-5x)=5.                             \tag{5}
\]

Thus adding \(x\) to any source-valid transfer around the cycle cannot
construct either \(A\) or \(A-5x\).  The degree-five top supplies only
the compatibility \(\sum_iE_i=0\); it is not a base vertex.

There is an exact integral relation

\[
 (A-5x)-5g_0=-4E_0-3E_1-2E_2-E_3.                  \tag{6}
\]

Consequently, over characteristic zero, the following are equivalent
after the clean adjacent edges are supplied:

1. one physical base comparison \(g_i=C_i-x\);
2. the cyclic package \(A\);
3. the kernel class \(A-5x\).

Moreover,

\[
              -{A-5x\over5}
\]

is exactly the `0373033` primitive relative generator.  Hence explicit
construction of \(A\) is not a route around the generator gate: it is the
cyclic form of the same one-base-comparison construction.

## The literal adjacent squares stop one step earlier

The actual order-four PP comparison squares still have the pure-Eq defects

\[
                    a-b,\ c-d,\ e-a,\ b-c,\ d-e.     \tag{7}
\]

The target-normalized \(x\) is killed by

\[
                  \text{pure Eq}+\operatorname{ainc},
\]

whereas a reduced pure-Eq correction is detected.  Therefore no multiple
of \(x\) cleans an individual square while retaining zero physical anchor
incidence.  The defects do obey the already known Tate-weighted identity

\[
 ce(a-b)+be(c-d)+bd(e-a)+ad(b-c)+ac(d-e)=0.          \tag{8}
\]

Equation (8) is the degree-five top compatibility.  It cancels the cyclic
sum of defects but does not add a comparison vertex and therefore does not
change (5).

There are consequently two levels in the actual source:

1. the literal adjacent squares first require their zero-anchor reduced-Eq
   correction;
2. even granting those corrections, one physical base \(C_i-x\) remains.

The second is the sharp cyclic comparison gate.  It must retain the common
matching companion and repeated \(P_3\sqcup K_2\) fine grade.  Its physical
rootless readout is still the pinned law

\[
 d r_i(\eta_z)=1+\delta_{iz}{u_z\over t},
 \qquad \sum_i d r_i(\eta_z)=5+{u_z\over t}.         \tag{9}
\]

The unary lift \(x\) has no comparison/rootless component and does not
supply (9).

## Scope

This is an exact composition of the literal PP edge obstruction, the
normalized \(C_5\) presentation, target normalization, and the physically
typed indeterminacy-or-generator theorem.  It rules out constructing
\(A\) from the existing adjacent transfers plus \(x\).  It does not rule
out adjoining the one source-labelled common-companion comparison in (3).

Run:

```text
python3 computations/verify_h3_rootless_cyclic_comparison_target_normalized_transfer_gate.py
python3 -O computations/verify_h3_rootless_cyclic_comparison_target_normalized_transfer_gate.py
python3 -I -S computations/verify_h3_rootless_cyclic_comparison_target_normalized_transfer_gate.py
```

Frozen ledger SHA-256:

```text
24bf520cc498f7be06fb001a1187928781e05f05bed3ffbd3729f8cbcc50e3e6
```
