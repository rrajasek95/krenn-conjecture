# The fixed-chart logarithmic reset stops at a pointed `L01` scalar

## Result

The full-site response-H2 tag contraction `f153872` is a coefficient theorem.
The pointed chart audit `d1b8ec4` correctly identifies its first proper face

\[
 L_{01}=(2Dq_{01}-p_0s_1-p_1s_0)
        (q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}).       \tag{1}
\]

There is no fixed-chart correction to (1) built from the complete response
row and arbitrary constant logarithmic Euler fields on the physical response
coefficients.

The complete response polynomial is the hafnian of `K8`: its `105`
occurrences are perfect matchings and its `28` coefficient variables are the
physical edges

```text
D=PS, p_i=Pi, s_i=Si, q_ij=ij.
```

A constant logarithmic field gives an additive edge weight on each perfect
matching.  The exact occurrence matrix has

```text
rank(edge/matching incidence)                  = 21,
rank(incidence + complete response row)        = 21,
rank(incidence + L01)                          = 22.
```

Thus neither a site/type Euler correction nor even an arbitrary constant
coordinate Euler correction cancels the proper face while retaining its H2
symbol.

Checker:

```text
computations/verify_h3_h2_fixed_chart_l01_reset_augmented_gate.py
```

## A literal twelve-occurrence obstruction

The rank increase has a small exact covector.  Multiply the following signs
by `1/3`:

```text
+ D q01 q23 q45       - D q03 q14 q25
- D q05 q12 q34       + D q05 q14 q23
- p0 s1 q23 q45       + p0 s1 q25 q34
- p0 s2 q13 q45       + p0 s3 q12 q45
- p1 s0 q23 q45       + p1 s2 q03 q45
+ p2 s0 q13 q45       - p2 s3 q01 q45.
```

Call this occurrence covector `psi01`.  Direct calculation gives

\[
 \psi_{01}(E_xR)=0\quad\text{for every one of the 28 variables }x,
 \qquad \psi_{01}(R)=0,
 \qquad \psi_{01}(L_{01})=1.                         \tag{2}
\]

The first equality includes every constant linear combination of coordinate
Euler fields.  The second also follows from the first because every response
matching has degree four.  The occurrence augmentation of `psi01` is zero.

This is an exact coefficient obstruction, not yet a physical terminal.  It
distinguishes occurrences inside one complete source polynomial and has not
by itself been identified with physical `q`, anchor, ridge, or residue rows.

## The smallest presentation-safe reset

On the three local direction coordinates

\[
                    A=Dq_{01},\quad B=p_0s_1,\quad C=p_1s_0,
\]

raw chart folding adds `B-A=0` and `C-A=0`.  Together with `A+B+C=0`,
this changes the fixed response quotient dimension from two to zero.

The rank-preserving graph cone instead uses

\[
              B-A-u_1=0,\qquad C-A-u_2=0.             \tag{3}
\]

It has five coordinates, three relations including the response row, and
quotient dimension two.  In this graph presentation,

\[
        2A-B-C=-(u_1+u_2),\qquad
        L_{01}=-(u_1+u_2)H_{2345}.                    \tag{4}
\]

Thus a graph cylinder organizes the full-site comparison but retains exactly
the scalar proper face.  Setting `u1=u2=0` imposes `A=B=C` and returns to the
invalid raw fold.  A physical fixed-chart reset must instead realize the
scalar in (4) as a source-labelled relative face.

The target does not absorb it.  Its occurrence augmentation is zero, so

\[
                        \operatorname{tgt}(L_{01})=0.
\]

But the exact response-row specialization from `0d14815` has

\[
                            R=0,\qquad L_{01}=3.       \tag{5}
\]

Therefore target-zero is not pointed-scalar-zero.  The graph reset needs a
coordinate `u01` with `u01(x)=L01(x)`; declaring `u01=0` would add a new
source equation.

## Physical augmented typing

The remaining positive object is now precise:

> Construct one source column in the literal response word, fine/repeated,
> and H2 direction-pair grade whose local first proper face is `L01`, while
> its physical `q`, anchor-incidence, target, Eq, and shifted-ridge faces are
> protected zero and all other declared augmented faces are retained.

The coefficient `K8` action types none of

```text
physical q, anchor incidence, Eq, shifted ridge,
W, ordinary residue, eta/sigma.
```

They cannot be assigned by covariance alone.  After same-grade physical
placement, however, the augmented theorem `4373ae6` is exhaustive.  For a
local dual with corner values `mu_j=psi(B_j)` and
`alpha=(-1,1,1,-1)`, its extension is

\[
\begin{aligned}
 q&=0,&\operatorname{ainc}&=0,&Eq_j&=0,\\
 \operatorname{target}_j&=-\mu_j,&W_j&=-\mu_j,
 &\operatorname{ores}_j&=\mu_j,\\
 \operatorname{ridge}&=-\sum_j\alpha_j\mu_j.          \tag{6}
\end{aligned}
\]

Formula (6) annihilates every known `r0/T/rho/K` column.  Exact duality then
has only two branches:

```text
L01 lies in the exhaustive protected physical image -> source-valid filler;
L01 lies outside                                  -> augmented terminal.
```

There is no third branch.  This is conditional on same-grade placement;
neither (2) nor full-site covariance supplies that placement.

## Updated frontier

The current fixed-chart route is therefore

```text
full-site H2 tag contraction
  -> pointed chart graph cone
  -> first proper face L01
  -> constant logarithmic reset impossible (12-term dual)
  -> MISSING same-grade source-labelled scalar/augmented placement
  -> protected filler or exact augmented terminal.
```

The artifact does not exclude non-diagonal higher Spencer corrections outside
the tested logarithmic/source-row span.  It proves that such a correction, if
it exists, must carry a genuine scalar graph face and the full physical
augmented typing; it cannot be another Euler or raw chart-fold identity.

## Verification

Run

```text
python3 computations/verify_h3_h2_fixed_chart_l01_reset_augmented_gate.py
python3 -O computations/verify_h3_h2_fixed_chart_l01_reset_augmented_gate.py
python3 -I -S computations/verify_h3_h2_fixed_chart_l01_reset_augmented_gate.py
```

Frozen ledger SHA-256:

```text
94f11da21af93ef6d07b68b6d4d42c3362e4095360798b1decb4aecdacf5e6fe
```
