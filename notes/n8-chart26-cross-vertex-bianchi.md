# The cross-vertex Bianchi square does not remove the chart-26 square

## Universal opposite-order identity

Fix distinct vertices \(v,q\).  Choose partners \(u\ne v,q\) and
\(r\ne v,q\), an outside color word, colors \(a,a'\) at \(v\), and colors
\(b,b'\) at \(q\).  Put

\[
 A=X_{vu}(a,d_u),\quad A'=X_{vu}(a',d_u),\qquad
 B=X_{qr}(b,d_r),\quad B'=X_{qr}(b',d_r),
\]

and abbreviate the four hafnian coefficients by \(H_{a,b}\), etc.  The
four one-end star transports are

\[
\begin{array}{ll}
 R_v(b)=A'H_{a,b}-AH_{a',b},&
 R_v(b')=A'H_{a,b'}-AH_{a',b'},\\
 R_q(a)=B'H_{a,b}-BH_{a,b'},&
 R_q(a')=B'H_{a',b}-BH_{a',b'}.
\end{array}
\]

They obey the exact cross-vertex Koszul identity

\[
 \boxed{B'R_v(b)-BR_v(b')-A'R_q(a)+AR_q(a')=0.}       \tag{1}
\]

Expanding (1) cancels each of its four corner terms once with each sign.
Thus changing the two colors in opposite orders is formally flat.  Combining
this with the star-minor formula expresses every \(R\) by smaller hafnian
cofactors, so (1) is also the precise Bianchi identity among the universal
one-end cells.  When a selected partner is the other changing vertex, the
coefficient depends on both corner colors; the direct-double identity is
the corresponding diagonal companion.

## Exact chart-26 specialization

Take \(v=7,q=5,u=6,r=4\), and write

\[
 A=\mathtt{f4}=(67{:}01),\quad A'=\mathtt{f5}=(67{:}02),
 \qquad B=\mathtt{c6}=(45{:}00),\quad B'=\mathtt{c7}=(45{:}01).
\]

For word codes \(1,2,10,11\), respectively denoting the four corners
\((1,0),(2,0),(1,1),(2,1)\) at \((v,q)\), equation (1) is

\[
 \mathtt{c7}R_v(0)-\mathtt{c6}R_v(1)
 -\mathtt{f5}R_q(1)+\mathtt{f4}R_q(2)=0.              \tag{2}
\]

Exact normalized expansion gives 180-term, originally reduced cells with
leading monomials

\[
\begin{array}{c|c}
R_v(0)&\mathtt{0948cfebf5}\\
R_v(1)&\mathtt{0948cfeff4}\\
R_q(1)&\mathtt{0948c6d9e4}\\
R_q(2)&\mathtt{0948c6cfef}.
\end{array}
\]

The two edge-\(57\) direct-double diagonals are

\[
 \mathtt{ef}H_1-\mathtt{eb}H_{11},\qquad
 tH_2-\mathtt{ec}H_{10},                              \tag{3}
\]

where \(\mathtt{ee}=(57{:}11)\) is a chart-support coordinate and hence
becomes \(t\).  Both diagonal expressions reduce exactly to zero against
the original generators.  Equations (2)--(3) are therefore the complete
four-corner compatibility packet relevant to this color square.

## What cancels, and what does not

The provisional degree-six cell has 546 terms and leading monomial

\[
                 M=\mathtt{0948cfcfebef},               \tag{4}
\]

with \(\mathtt{cf}=(46{:}00)\) repeated.  Reducing it by all three new
opposite-order one-end cells in (2) uses no column and leaves the polynomial
unchanged.  Thus (2) cancels the repeated term in the *difference* between
opposite-order compositions, but does not reduce either composition.

This is not merely a local failure.  The complete degree-five Buchberger
layer contains 84,005 mutually reduced squarefree leads.  Exhaustive exact
comparison finds

\[
 \#\{L:\ L\text{ is a degree-five lead and }L\mid M\}=0. \tag{5}
\]

No original degree-four lead divides \(M\), either.  Hence \(M\) is a
genuine minimal non-squarefree generator of the chart-26 initial ideal.
The hoped-for Bianchi cancellation does occur as a syzygy, but it cannot
restore a squarefree initial ideal under this term order.  This closes the
specific gap left by the provisional computation; it does not determine
the later Buchberger layers or localized target membership.

## Verification

Run

```text
python3 computations/verify_n8_chart26_cross_vertex_bianchi.py
```

The checker expands (2), verifies both diagonals in (3), reconstructs (4),
and scans every lead in the complete degree-five layer before asserting
(5).
