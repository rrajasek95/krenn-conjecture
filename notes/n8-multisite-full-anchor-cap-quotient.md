# Complete binary anchors force a nonzero higher cap tail

## The exact quotient

Let `q` be an ordinary six-site endpoint-coloured quadratic and let
`p0,p1,s0,s1` be arbitrary multisite endpoint stars.  Assume the complete
two-anchor packet

\[
 q^{[3]}=X_0,qquad
 p_i s_jq^{[2]}=\delta_{ij}X_{i+1}quad(i,j=0,1).        \tag{1}
\]

For

\[
 K=\begin{pmatrix}1&1\\-1&1\end{pmatrix},\qquad
 R_K=p_0s_0+p_0s_1-p_1s_0+p_1s_1,                       \tag{2}
\]

all four response tensors, not merely selected scalar coefficients, give

\[
                         R_Kq^{[2]}=X_1+X_2.             \tag{3}
\]

The exact divided-power expansion is therefore

\[
 (q+R_K)^{[3]}
   =X_0+X_1+X_2+R_K^{[2]}q+R_K^{[3]}.                  \tag{4}
\]

The checker is
`computations/verify_n8_multisite_full_anchor_cap_quotient.py`.

## What the extra diagonal anchor changes

It closes the first-insertion scope gap in `146199f`: the quotient in (1)
now has both pure diagonal anchors and both cross zeros.  It does **not**
alter the higher source-provenance grades.  Exact expansion of (2) gives

```text
in q*R_K^[2]:   8 nonzero repeated-label sectors,
in R_K^[3]:    16 nonzero row/column multiset sectors.
```

The eight quadratic sectors are the four same-entry squares, two
repeated-row terms, and two repeated-column terms recorded in
`n8-multisite-permanent-null-repeated-defect.md`.  The sole
distinct-row/distinct-column sector still cancels by `perm(K)=0`.  All
sixteen possible cubic row-multiset/column-multiset sectors are nonzero.

This is a finite universal normal form in the literal insertion grading:

```text
q^[3]                 insertion order 0, fixed by the top row
p_i*s_j*q^[2]         insertion order 1, fixed by the four responses
R_K^[2]*q             insertion order 2, eight repeated sectors
R_K^[3]               insertion order 3, sixteen cubic sectors.
```

Consequently the complete five tensors in (1) do not provide a formal
same-grade reduction of the 24 higher sectors.  Any such reduction must use
an additional physical collision, source syzygy, or connection/Bianchi
identity.

## No ordinary clean lift

There is nevertheless a decisive theorem-level consequence.  In every
characteristic-zero divided-power algebra,

\[
                         R_KR_K^{[2]}=3R_K^{[3]}.        \tag{5}
\]

Suppose an ordinary source realization of (1) killed the raw quadratic cap,
`R_K^[2]=0`.  Equation (5) would also give `R_K^[3]=0`; then (4) would be an
ordinary six-site realization of

\[
                         \Delta_{6,3}=X_0+X_1+X_2,
\]

contradicting the pinned arbitrary-complex six-site theorem.  Therefore

\[
 \boxed{\text{every ordinary full-anchor packet has }R_K^{[2]}\ne0.} \tag{6}
\]

So there is no ordinary source lift killing all eight raw repeated sectors.
This closes precisely the clean-cap generalization suggested by the
fixed-star proof.

## Remaining sharp alternative

Equation (6) does not say that multiplication by `q` is injective.  It is
still logically possible that

\[
                         R_K^{[2]}q=0,\qquad R_K^{[2]}\ne0. \tag{7}
\]

If (7) occurs, (4) and the six-site theorem force

\[
                         R_K^{[3]}\ne0.                 \tag{8}
\]

Thus the complete exact dichotomy is

\[
 R_K^{[2]}q\ne0
 \quad\text{or}\quad
 \bigl(R_K^{[2]}q=0\text{ and }R_K^{[3]}\ne0\bigr).     \tag{9}
\]

The extra anchors therefore force a dirty cap but do not decide whether its
first nonzero obstruction occurs at insertion order two or three.  Closing
that sharper alternative requires a source-specific relation between the
eight quadratic and sixteen cubic sectors; another response-row expansion
alone cannot do it.

## Reproduction

```bash
.venv/bin/python computations/verify_n8_multisite_full_anchor_cap_quotient.py
.venv/bin/python -O computations/verify_n8_multisite_full_anchor_cap_quotient.py
python3.14 computations/verify_n8_multisite_full_anchor_cap_quotient.py
```
