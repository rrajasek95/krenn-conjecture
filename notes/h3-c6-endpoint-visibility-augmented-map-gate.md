# The canonical C6 blind quotient is not a physical terminal class

Research boundary.  This does not prove spoke-to-hole synchronization,
`SP-CLEAN-BRIDGE`, or Krenn's conjecture.

## Exact frozen quotient

At the canonical word `z=012111`, quotient the unary matching occurrence
module by the seven already-routed external-offdiagonal bases.  A basis is

```text
M, N, and the six anchor-contained competitors.
```

The selected-port response projection is zero at this word, so its only
literal relation is the unary column

\[
                         u=(1,1,1,1,1,1,1,1).
\]

The transgression residual is (r=M+N).  The primitive symmetric covector

\[
             \lambda=(3,3,-1,-1,-1,-1,-1,-1)          \tag{1}
\]

satisfies

\[
                    \lambda(u)=0,\qquad\lambda(r)=6.  \tag{2}
\]

Thus the **frozen selected-port projection** has a genuine occurrence-
cokernel class.  This is the strongest linear statement supplied by the
six-base aggregate alone.  The refined common-tail decomposition in
[`h3-c6-z-spoke-hole-koszul-boundary.md`](h3-c6-z-spoke-hole-koszul-boundary.md)
packages the same absence as a four-tail unary/response separator and gives
the exact source-valid Koszul identities once a missing endpoint component
exists.

## The class is destroyed by the first missing columns

The class (1) is not stable under the complete physical source inventory.
If the first advertised component `p1@0:0` is paired with the selected
`s1@1:1`, the `G11[z]` hole-01 coefficient has the three tails

```text
23|45, 24|35, 25|34.
```

The last already routes externally.  In the eight-class quotient the new
column is therefore

\[
                  c_{01}=M+(01|24|35),\qquad
                  \lambda(c_{01})=2.                  \tag{3}
\]

Likewise `p2@3:1` with the selected `s1@1:1` gives the `G21[z]` hole-13
column

\[
 c_{13}=(02|13|45)+(05|13|24),\qquad
                  \lambda(c_{13})=-2.                 \tag{4}

Hence (1) is not a physical terminal readout: either legitimate
word-changed response column pairs nontrivially with it.  The ranks of
`[u]`, `[u,r]`, and `[u,c01,c13]` are respectively `1,2,3` over the
integers and over every characteristic other than two or three.

## The smallest honest augmented map

At a fixed physical source (A=(q,p,s)), endpoint accessibility is governed
by the complete endpoint Jacobian

\[
 \widehat J_A:\bigoplus_{i=1}^2(E_{p_i}\oplus E_{s_i})
 \longrightarrow\bigoplus_{i,j=1}^2 k^{\{0,1,2\}^6}, \tag{5}
\]

\[
 \widehat J_A(\dot p,\dot s)_{ij,w}
 = [\dot p_i s_jq^{[2]}+p_i\dot s_jq^{[2]}]_w.        \tag{6}
\]

All endpoint sites, colours, output words, and common-`q` cofactors must
be retained.  The endpoint-only differential of the unary tensor is zero;
maximum-anchor safety is a separate readout.  The canonical visibility
readout supplied by the displayed boundary is only the pair

```text
q_z=(epsilon(p1@0:0), epsilon(p2@3:1)).
```

The six-base aggregate selects no canonical scalar projection of this pair.
After choosing either coordinate functional `epsilon`, ordinary linear
algebra gives the exact alternative

```text
epsilon detects ker(Jhat_A): a one-sided joint-kernel modification exists;
epsilon kills ker(Jhat_A): it descends to the image and yields the affine/Fitting dual branch.
```

This is Theorem A's contraction-or-Fitting alternative.  It is not the B/C
terminal dichotomy.  A B/C terminal covector must annihilate the image of
the **complete** physical augmented boundary map; equations (3)--(4) show
that the tempting symmetric covector (1) already fails on legitimate
physical endpoint columns.  Moreover no source-boundary/target/ordinary-
residue complex or physical terminal readout is present in (5), and the
selected skeleton does not determine (5).  A B/C-compatible class could be
discussed only after a complete physical augmented correction map and its
readouts were supplied.

## Consequence

Failure of selected-port visibility in the canonical C6 supplies an
**incomplete map**, not detected homology.  The next exact finite test is to
evaluate the full `2916 x 72` matrix of (5)--(6) at the
physical packet, append maximum-anchor readouts, and test each scalar
projection of `q_z` on `ker(Jhat_A)`.  A nonzero value is the one-sided
modification branch; annihilation gives the exact affine/Fitting dual
certificate.  The theorem needed to control that test uniformly remains
spoke-to-hole synchronization: use the unary top and full response tensors
to force one of (3)--(4), a joint-kernel target-line move, a unit, or a free
carrier.  Only after a column exists can complete-column proportionality,
Fitting, and Hall landing be applied.

Checker:
`computations/verify_h3_c6_endpoint_visibility_augmented_map_gate.py`.

## Verification

```text
python3 computations/verify_h3_c6_endpoint_visibility_augmented_map_gate.py
python3 -O computations/verify_h3_c6_endpoint_visibility_augmented_map_gate.py
python3 -I -S computations/verify_h3_c6_endpoint_visibility_augmented_map_gate.py
```

Frozen ledger SHA-256:

```text
3bd9b4005c8bf50e303b0197574abe613d5588c0854f37c9f5c838a81ac755b9
```
