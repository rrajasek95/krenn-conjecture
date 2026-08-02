# The smallest target-augmented filtered packet has zero \(d_2\)

Research obstruction only.  This note does not prove the unified overlap
theorem, `SP-CLEAN-BRIDGE`, or Krenn's conjecture.

## 1. Outcome

At \(h=3\), retain the selected direct matrix

\[
             D=\begin{pmatrix}A&B\\ F&U\end{pmatrix},
             \qquad \kappa=AU-BF\ne0,                    \tag{1}
\]

the connection/normal/curvature filtration, the normalized scalar-zero cap,
its physical target, and one diagonal same-power anchor.  There is a smallest
target-augmented **selected-row model** containing the scalar images of all
these data.  It is not yet a literal all-label full-source complex.  Its
filtration components \(d_0,d_{-1},d_{-2}\) satisfy every component of
\(d^2=0\), including on the direct-free boundary \(B=0\).

The adjugate contraction does exactly what the overlap formulas suggest.  If
the direct curvature correction is omitted, the drop-two square is

\[
                         \kappa z .                        \tag{2}
\]

Putting that literal correction back makes the filtered second differential
of the comparison cell

\[
 d_2[x]=-\kappa(1,\overline Y_c),                          \tag{3}
\]

where the coordinates are physical target and odd residue.  This is the
curvature-weighted scalar-zero **cap graph**, not the requested pair
\((0,-\kappa\overline Y_c)\).  The common diagonal-anchor mode has first
differential \((1,\overline Y_c)\), so (3) is zero on \(E_2\).

This is not only a failure to identify a promising nonzero representative.
In the target-augmented same-power cap complex,

\[
 d_{\rm cap}(T,R)=R-\overline Y_cT.                        \tag{4}
\]

Consequently

\[
 d_{\rm cap}(0,-\kappa\overline Y_c)
                  =-\kappa\overline Y_c\ne0.              \tag{5}
\]

Thus the hoped-for target-zero pair is not a \(d_0\)-cycle in the smallest
literal assembly.  Replacing (3) by that pair breaks the drop-one component
of \(d^2=0\) by exactly the right side of (5).  The diagonal anchor does not
nullhomotope only the target: it contributes
\(+\kappa(1,\overline Y_c)\) and cancels both target and residue.

This isolates the first missing row for the filtered route.  A larger
adjacent-power/cross-quotient relative Rees complex must contain a new
source-provenant low-grade target nullhomotopy whose \(d_0\)-boundary is the
cap-relation defect in (5), while its associated-grade response retains the
odd residue.  It must kill \(w\) without killing the residue.  Only after that
extension exists does one reach the separate problem of removing, or typing
the readout modulo, the surviving common chart mode.  The present
full-five-site and diagonal rows supply neither datum.

## 2. Literal scalar inputs

Write the columns and adjugate rows of (1) as

\[
 c_1=\binom AF,
 \qquad c_2=\binom BU,
 \qquad \lambda=(-F,A),
 \qquad \eta=(U,-B).                                     \tag{6}
\]

They obey

\[
 \lambda c_1=0,\qquad \eta c_2=0,
 \qquad \lambda c_2=\eta c_1=\kappa.                    \tag{7}
\]

These are the two-column scalar compression of the selected power-free
connection and normal/curvature packet.  No division by \(A,B,F,U\), or a
trace is used.  Equivalently, when desired,
\(\kappa^{-1}\operatorname{adj}D\) is the contraction on the open set
\(\kappa\ne0\).  Formula (7), rather than an assumed inverse entry, is what
is used below.  At \(h=3\), the uncancelled
curvature/direct-double Euler bracket is

\[
       \kappa\bigl(zZ_1-2Z_0\bigr),                       \tag{8}
\]

and (2) is its normalized radial carrier before the direct correction is
inserted.

For the selected surviving odd label \(c\), abbreviate
\(Y=\overline Y_c\ne0\).  The exact same-power target--residue lock says that
every admitted cap or diagonal anchor maps to

\[
                 g_\gamma=(\gamma,\gamma Y).             \tag{9}
\]

The normalized scalar-zero cap is \(g_{-1}=(-1,-Y)\).  The all-label
five-site row is identical in the two canonical charts, including its target,
so the chart-difference mode cancels while this common mode remains.  These
are literal selected coefficient consequences; no inverse to coefficient
extraction is being postulated.

## 3. The three-grade total complex

Let the ground field be any characteristic-zero field containing the selected
coefficients.  The nonzero graded pieces, displayed by cochain degree, are

| degree | \(G_2\) | \(G_1\) | \(G_0\) |
|---|---|---|---|
| \(0\) | \(\langle x\rangle\) | \(\langle e,a\rangle\) | \(0\) |
| \(1\) | \(0\) | \(V_1\cong k^2\) | \(V_0\oplus\langle T,R\rangle\), \(V_0\cong k^2\) |
| \(2\) | \(0\) | \(0\) | \(\langle z,w\rangle\) |

Here \(x\) is the oriented comparison cell, \(e\) is its adjugate middle
lift, \(a\) is the common diagonal-anchor mode, \(z\) is the radial curvature
row, and \(w\) is the target-augmented cap-relation row.  Define the nonzero
components of the differential by

\[
\begin{array}{c|lll}
 &d_0&d_{-1}&d_{-2}\\ \hline
e&c_1\in V_1&(c_2,-\kappa g_1)\in V_0\oplus\langle T,R\rangle&0\\
a&0&g_1&0\\
x&0&-c_1\in V_1&-c_2\in V_0\\
v\in V_1&0&-\eta(v)z&0\\
v\in V_0&\lambda(v)z&0&0\\
(T,R)&(R-YT)w&0&0.
\end{array}                                                \tag{10}
\]

The cap term in \(d_{-1}e\) is exactly \(\kappa\) times the normalized
scalar-zero cap (9), with the selected orientation.  The \(a\)-row is the
same-power diagonal companion.  The term \(d_{-2}x=-c_2\) is the direct
curvature correction.  Hence (10) is the smallest target-augmented scalar
packet obtained by attaching the literal cap graph to the two-column
adjugate overlap packet.

The equations in \(d^2=0\) are transparent.  The only nontrivial drop-one
check is on \(e\):

\[
 d_0d_{-1}e+d_{-1}d_0e
   =\lambda c_2\,z-\eta c_1\,z
      -\kappa d_{\rm cap}(g_1)w=0.                       \tag{11}
\]

The drop-two check on \(x\) is

\[
 d_0d_{-2}x+d_{-1}^2x
                  =-\lambda c_2\,z+\eta c_1\,z=0.        \tag{12}
\]

Without \(d_{-2}x\), the second term in (12) is precisely \(\kappa z\),
which proves (2).  Thus this selected-row direct-matrix model has no hidden
middle obstruction: its adjugate contraction is exact, including when
\(B=0\).  This does not assert acyclicity of the full source overlap complex.

For completeness, the possible drop-three and drop-four components are

\[
 d_{-1}d_{-2}+d_{-2}d_{-1},
 \qquad d_{-2}^2.
\]

They vanish identically in (10), because $d_{-2}$ is zero from degree one
to degree two and $d_{-1}$ kills the grade-zero image of $d_{-2}x$.  The
checker verifies these two components separately as well as drops zero, one,
and two; the total-square check is an additional consistency check.

## 4. The computed \(d_2\) and its indeterminacy

One has \(d_{-1}x=-c_1\) and \(d_0e=c_1\), so the corrected lift in the
filtered-\(d_2\) formula is \(y=e\).  Therefore

\[
\begin{aligned}
 \beta_2(x,e)
   &=d_{-2}x+d_{-1}e\\
   &=-c_2+(c_2,-\kappa g_1)
     =-\kappa g_1,
\end{aligned}                                             \tag{13}
\]

which proves (3).  It is a \(d_0\)-cycle by (4), as required by \(d^2=0\).
But \(a\) is a \(d_0\)-cycle and

\[
                         d_1[a]=g_1.                       \tag{14}
\]

Thus (13) is \(d_1[-\kappa a]\), so

\[
                             d_2[x]=0                       \tag{15}
\]

in the actual \(E_2\)-quotient of this bounded packet.

For completeness, \(H^1(G_0,d_0)\) is two-dimensional: one generator is
the direct kernel \(c_1\in V_0\), and the other is the cap graph \(g_1\).
The image in (14) removes the latter, leaving a one-dimensional \(E_2\)
group.  The comparison class (13) has no component in its survivor.

There is also an exact readout obstruction.  The pair-valued map
\((T,R)\) does not descend to \(E_2\), because it is nonzero on the
indeterminacy \(g_1\).  The unique scalar graph-annihilating readout at this
level is proportional to \(R-YT\), but it vanishes on (13).  Deleting the
target coordinate would return the desired number \(-\kappa Y\); equation
(5) shows exactly why that deletion is not a map of the augmented complex.

## 5. Sharp missing datum and scope

The first obstruction occurs before a subtle higher-page uniqueness issue.
Forcing the proposed representative

\[
                         p=(0,-\kappa Y)                  \tag{16}
\]

into \(d_{-1}e\) changes (11) by

\[
                          -\kappa Y\,w.                   \tag{17}
\]

Thus a successful enlargement must first provide a literal relative
generator \(n_c\) with the typed adjacent-power/cross-quotient boundary
needed to cancel (17), but whose associated-grade readout still retains
\(-\kappa Y\).  Merely using the diagonal anchor adds
\(\kappa g_1=(\kappa,\kappa Y)\) and sends (13) to \((0,0)\).  After adding
any new generator, one must separately prove that its residue readout kills
the common-mode first-differential image in (14).

This calculation has deliberately limited scope.

* It is a bounded scalar quotient of selected literal coefficient rows,
  not the full \(18\)-cap-row, all-label EqSystem and not yet a literal
  full-source filtered complex.
* It does not prove that every possible relative Rees extension or
  five-site restriction--insertion complex factors through (10).
* It does prove that the smallest target-augmented adjugate assembly of the
  presently available rows has zero filtered \(d_2\), and it names the first
  new \(d^2\)-row required to obtain the target-zero odd residue.
* It is unchanged at trace zero and on the selected scalar boundary \(B=0\);
  neither case requires trace division or a nonzero selected $pr$ entry.
  Here \(B=0\) is only a condition in the compressed matrix (1), not an
  assertion that the entire physical $pr$ direct block vanishes.

The independent
[five-exposed selected-cap counterguard](h3-five-exposed-two-chart-selected-cap-landing-counterguard.md)
(commit `7ed244e`) shows that even the \(9+9\) selected cap rows, all selected
overlap rows, the crossed slice, and diagonal frame bookkeeping do not imply
the raw grade-split landing.  The present calculation is complementary: it
tests the weaker filtered organization and finds the earlier target-augmented
cycle defect (17).  A cross-word full-source coupling or the new relative
nullhomotopy could in principle evade both bounded results.

In the
[unified full-nine target](unified-full-nine-two-chart-overlap-jet-saturation-target.md),
this missing nullhomotopy is the first concrete interface between Components
III and IV: it must provide the inactive target-zero response, after which
the same filtered class still needs the rootless Macaulay readout and the
mixed-ledger/common-mode faithfulness theorem.

The dependency-free checker
[`verify_h3_target_augmented_filtered_d2_first_obstruction.py`](../computations/verify_h3_target_augmented_filtered_d2_first_obstruction.py)
builds all component matrices over `Fraction`, checks all five possible
filtration components of \(d^2\) through drop four, computes (13), computes
the \(E_2\) ranks, checks the common-mode indeterminacy, and mutation-checks
both defects (2) and (17).
It pins the exact packet digest and runs in normal, optimized, isolated, and
optimized-isolated modes.
