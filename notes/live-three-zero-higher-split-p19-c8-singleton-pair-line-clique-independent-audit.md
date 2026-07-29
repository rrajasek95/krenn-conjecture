# Independent audit: the (p=19, C=8) singleton pair-line clique

## 1. Scope

This note independently reconstructs the closure of

\[
                         2^{10}1^{h+1}                       \tag{1}
\]

from the one-double selection used in
[the primary closure](live-three-zero-higher-split-p19-c8-singleton-pair-line-clique-closure.md).
The points requiring a separate check are the existence of the relation
three-spaces for every (p=h+k=19), the common-unit transport after the
selected double is removed, the dimension-four/full-pencil branches, and
the bidegree-six interpolation step.

## 2. The formal selection is uniform in the split

Fix one singleton value (r), select the other (h) singleton layers,
and put one of the ten doubles (i) in formal role two.  The selected
label count is (h+2), and the complement is (2^9 1), of mass nineteen
and with ten value classes.  Thus a five-dimensional selected-row kernel
has relation space

\[
                 {cal S}_i\subseteq\mathbb C[z]_{\le6},
                 \qquad \dim{cal S}_i=3.                    \tag{2}
\]

Here is the exact dimension check.  With (d=1) and (s=h), the
low-role pair-drop theorem gives selected-kernel dimension at least four.
For a hypothetical six-space its sharp Wronskian excess is

\[
  22-h+\max(0,6-k)
   =22-h+\max(0,h-13)=9                              \tag{3}
\]

for each (13\le h\le18), since (k=19-h).  Hence the dimension is at
most five.  If it were four, it would equal the pair-drop span, and the
dimension-four part of the low-role selected-lift incidence theorem
applies with (d=1).  Its terminal square-pencil gap is

\[
                 (s-1)-((h-1)-2)=2>0,                         \tag{4}
\]

including the possible zero singleton.  Therefore the selected kernel
has dimension exactly five and (2) follows.

## 3. Exact common baseline

Put

\[
                         g_i=(z-i)^3(z+i)^2.                  \tag{5}
\]

Remove the selected double while retaining the same (h) singleton
layers.  The baseline is now independent of (i); its complementary
rows are ten exact order-two rows and the exact order-one row at (r).
At a row different from (i), (5) is a unit and the product rule is the
exact change of normalization.  At (i), its order-three zero kills the
complete two-jet.  Consequently

\[
      g_i{cal S}_i\subseteq{cal K}\subseteq
      \mathbb C[z]_{\le11}                                  \tag{6}
\]

for one common kernel and one common local unit at each baseline row.
This verifies the point needed later: the singleton unit is independent
of the pair (i,j), and the double unit at a tested (v) is independent
of every (x,y\ne v).

If (D=\dim{cal K}\ge6), its forced weight and cap are respectively

\[
             10(D-2)+(D-1)=11D-21,
             \qquad D(12-D).                                \tag{7}
\]

Their difference is (D^2-D-21>0).  The exact-row gcd correction is
nonnegative, so (D\le5).

## 4. Pair lines

Distinct double values are nonopposite, hence (g_i,g_j) are coprime and

\[
 g_i\mathbb C[z]_{\le6}\cap g_j\mathbb C[z]_{\le6}
                 =g_ig_j\mathbb C[z]_{\le1}.                \tag{8}
\]

Dimension three is impossible because two three-spaces would have a
three-dimensional intersection inside the pencil (8).  In dimension
four their intersection would be the whole pencil, but its member
(g_ig_j(z-r)) violates the common row ((U_rT)'(r)=0).  The same test
excludes a full-pencil intersection in dimension five.  Thus

\[
 \dim{cal K}=5,
 \qquad
 g_i{cal S}_i\cap g_j{cal S}_j
       =\langle g_ig_j\ell_{ij}\rangle .                    \tag{9}
\]

The factor (ell_{ij}) cannot vanish at (r), by the same first-row
test.  Normalize it as

\[
 \ell_{ij}=1+d_{ij}(z-r),\qquad
 a_x={5r+x\over r^2-x^2},\qquad
 \Lambda=-{U_r'(r)\over U_r(r)}.                            \tag{10}
\]

Applying the single common row at (r) to (9) gives, without any
pair-dependent unit,

\[
                         d_{ij}=\Lambda-a_i-a_j.              \tag{11}
\]

## 5. Clique identity and terminal pole

Fix a double (v), and let (Omega) be the other nine doubles.  For
distinct (x,y\in\Omega), apply the common row
((U_vT)''(v)=0) to the generator in (9).  With

\[
 A_x={5v+x\over v^2-x^2},\qquad
 R_x={4(5v^2+2vx-x^2)\over(v^2-x^2)^2},                     \tag{12}
\]

the product rule gives exactly the symmetric equation

\[
 Q_{xy}(1+(v-r)d_{xy})+2P_{xy}d_{xy}=0,                     \tag{13}
\]

where

\[
\begin{aligned}
 P_{xy}&=u+A_x+A_y,\\
 Q_{xy}&=c+R_x+R_y+2u(A_x+A_y)+2A_xA_y.
\end{aligned}                                               \tag{14}
\]

After multiplication by

\[
 (r^2-x^2)(r^2-y^2)(v^2-x^2)^2(v^2-y^2)^2,                 \tag{15}
\]

the numerator has degree at most six separately in (x,y).  For each
of nine choices of (x), the other eight clique vertices are roots in
(y), so the numerator vanishes identically in (y); its coefficient
polynomials then have nine roots in (x), so the numerator is the zero
polynomial.

The excluded double pole (y=v) would therefore have zero coefficient.
Directly from (12)--(14), that coefficient is

\[
 6\left[1+(v-r)(\Lambda-a_x-a_v)\right].                    \tag{16}
\]

Clearing (r^2-x^2) leaves

\[
 K(r^2-x^2)-(v-r)(5r+x),                                    \tag{17}
\]

whose coefficient of (x) is (-(v-r)\ne0).  This is a structural
contradiction, including (r=0).  The (C=8) endpoint is therefore
closed.

## 6. Machine reconstruction

[verify_live_three_zero_higher_split_p19_c8_singleton_pair_line_clique_independent_audit.py](../computations/verify_live_three_zero_higher_split_p19_c8_singleton_pair_line_clique_independent_audit.py)
checks all six splits, the kernel and intersection inequalities, the
quintic logarithmic jets, the separate bidegree-six bound, and the exact
double-pole coefficient.
