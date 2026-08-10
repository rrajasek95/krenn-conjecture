# The fixed-dark guard becomes active-clean on two overlapping charts

Research evidence only.  This is a bounded exact audit of the rational
packet in
[`n8-rank11-scalar-fixed-dark-plane-one-site-guard.md`](n8-rank11-scalar-fixed-dark-plane-one-site-guard.md),
not a source point and not a proof of `SP-CLEAN-BRIDGE`.  The packet fails
its labelled joint rows.  The result identifies the positive mechanism
which a uniform second-chart theorem should reproduce.

## 1. Restore the eight-site block array

The one-site guard is written as a six-site pair chart.  Restore its two
endpoint sites as $6,7$: the internal blocks are the displayed quadratic
$q$, the $6$- and $7$-stars are $p$ and $s$, and

\[
                         A_{67}=e_0\mu^{\mathsf T}.
\]

This gives a rational eight-site array with 37 decorated nonzero cells.
At any physical pair $uv$ and any nonzero decorated direct entry
$A_{uv}(a,b)$, form the canonical line

\[
                            K(z)=E_{ab}+zI.                 \tag{1}
\]

For $N=8$, if $s(z)=\langle K(z),A_{uv}\rangle$, $R(z)$ is the
effective endpoint-response quadratic, and $q_{uv}$ is the six-site
internal quadratic, the homogeneous clean error is

\[
 \mathcal E_{uv}(K(z))
   =s(z)R(z)^{[2]}q_{uv}+R(z)^{[3]}.
\tag{2}
\]

The checker expands every coefficient of (2) as a polynomial of degree at
most three in $z$, takes their exact common gcd, and removes the finitely
many roots at which $sK_{00}K_{11}K_{22}=0$.

## 2. Exact census

There are 37 canonical lines, one for every nonzero decorated block cell.
Thirty-five are clean somewhere.  Four are identically clean by support
concentration, and two further lines have a nontrivial active root:

\[
\begin{array}{c|c|c|c}
\text{pair}&(a,b)&s(z)&\gcd_w\mathcal E_w(K(z))\\ \hline
(1,7)&(0,2)&1+z&z-1\\
(2,7)&(0,1)&1&z-1.
\end{array}                                                \tag{3}
\]

Thus at $z=1$, respectively

\[
 K_{17}=E_{02}+I,
 \qquad
 K_{27}=E_{01}+I,                                         \tag{4}
\]

are clean, have nonzero direct scalar, and have all three diagonal target
coefficients equal to one.  Both are active clean caps.

The four identically clean active lines occur at decorated cells
$01{:}00$, $06{:}00$, $25{:}00$, and $34{:}00$.  They are useful
additional calibration, but (3) is the sharper overlap phenomenon:
nonzero clean-error coefficients cancel at one active parameter rather
than vanishing merely because the effective response lacks three disjoint
edges.

The original $(6,7)$ scalar chart has three nonzero direct entries and
three canonical lines.  Their common gcds are $1+z,z-1,z-1$, but in each
case the only clean root also zeros the direct scalar (and in the diagonal
case one target diagonal).  Hence none is active.  This matches the exact
inactive clean-plane calculation in the one-site note.

## 3. Proof impact

The fixed-dark guard is not an obstruction to the desired conclusion once
physical pair exchange is allowed.  Its inactive scalar cap plane is left
by two literal overlapping charts, each of which supplies the full descent
hypothesis.  Consequently the high-impact scalar-shore task is now sharply
formulated:

> transport the common cross-permanent/mixed-carrier ledger through a
> source-faithful overlapping pair presentation and prove that either an
> active clean line like (3) appears, or the labelled rows give an ordinary
> source unit/descent.

The calculation does not prove that an arbitrary fixed-dark packet has one
of the two displayed star patterns.  Entry minimality and the common
source-labelled carrier identity are still needed to force the pair
exchange.  It does show that trying to activate a cap *inside* the original
scalar plane is the wrong target: the successful caps live on different
physical pairs.

## 4. Exact audit

[`verify_n8_rank11_scalar_dark_plane_second_chart_line_audit.py`](../computations/verify_n8_rank11_scalar_dark_plane_second_chart_line_audit.py)
uses exact `Fraction` arithmetic and no external solver.  It reconstructs
all 37 cells, re-presents the array at every pair, expands (2), computes
every polynomial gcd, and audits the activity divisor.  Its deterministic
ledger digest is

```text
1c5b29962f4c29ef36c75e3775e50c557536b78c1a3e34289195a0a8eaa6a622
```
