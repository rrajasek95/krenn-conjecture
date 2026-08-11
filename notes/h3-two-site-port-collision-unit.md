# A contracted two-site port collision gives an unrestricted-internal source unit

Research theorem.  `SP-CLEAN-BRIDGE` and Krenn's conjecture remain open.
This result weakens the internal-support hypotheses of the preceding
[two-site flag unit](h3-two-site-flag-h2-source-unit.md); it does not extract
the two-site port from an arbitrary full-nine packet.

## 1. Result

Work on six residual sites, call two of them `0,1`, and retain colours
`0,1`.  Every endpoint-coloured cell of the internal quadratic `q` is
arbitrary.  For one first-endpoint row (or contraction) and two
second-endpoint rows (or contractions), assume only the triangular two-site
port

\[
\begin{aligned}
 p_0&=A z_0^0+B z_1^0+C z_1^1,\\
 s_0&=D z_0^1,\\
 s_1&=E z_0^0+F z_0^1+G z_1^1,
\end{aligned}                                             \tag{1}
\]

with no other colour-`0/1` components.  Let `d00,d01` be the corresponding
direct entries and let `Fij(w)` denote the literal full-nine coefficient row,
including the target `-1` in `F00(000000)`.  Put

\[
             J=AG+CE,\qquad L=d_{01}D-d_{00}F.             \tag{2}
\]

Then, with no hypothesis on `q`,

\[
\boxed{
\begin{aligned}
 &-d_{01}J F_{00}(000000)+d_{00}J F_{01}(000000)\\
 &\quad+d_{01}BE F_{00}(010000)-d_{00}BE F_{01}(010000)
       =d_{01}J .
\end{aligned}}                                             \tag{3}
\]

Thus the port is source-empty on the chart `d01*J != 0`.  This is an
ordinary four-row polynomial certificate: no internal diagonal matching,
Hasse operator, evaluation, division, or cap codomain occurs.

The row labels need not themselves be physical coordinate labels.  Let
\(\xi,\eta,\theta\in\mathbb C^3\) be endpoint-label covectors and contract
the literal full-nine system to

\[
 F_{\xi,\eta}=\sum_{i,j}\xi_i\eta_jF_{ij},\qquad
 F_{\xi,\theta}=\sum_{i,j}\xi_i\theta_jF_{ij}.
\]

If, for one physical target label \(a\),

\[
 \xi_i\eta_i=\lambda\delta_{ia},\qquad
 \xi_i\theta_i=0\quad(0\le i\le2),                    \tag{3a}
\]

then these are respectively a pure anchor row of weight \(\lambda\) and a
crossed target-zero row.  Whenever their residual endpoint forms have the
same triangular two-site restriction (1), every identity below remains
valid after replacing the right side of (3) by

\[
                     d_{01}\lambda J.                         \tag{3b}
\]

This is source-faithful: the two contracted rows are literal scalar linear
combinations of the nine original generators.  Thus the landing theorem
requires a pure-anchor/crossed-zero **contraction**, not a pre-existing
literal `00/01` pair.  This is the form compatible with the automatic
two-chart packet and its diagonal-anchor transport problem.

There are two companion collision units.  On the active `d00*d01` chart,
if `B` or `C` is nonzero, every surviving packet must satisfy

\[
                         \boxed{J=0,\qquad L=0.}             \tag{4}
\]

Consequently the pure-matching hypotheses of the older Hamming-two unit are
needed only on the codimension-two aligned-port boundary (4), not on the
generic triangular port.

## 2. Universal port determinant

The identity is a special case of a source-row calculation independent of
the matching degree.  Fix a pure output word `Z` and three words `W` which
differ from it only at the two port sites.  Because both endpoint factors
are supported on those sites, the response part of row `i` at `W` is

\[
                              r_{i,W}Q,                      \tag{5}
\]

where `Q` is the same matching coefficient on the complementary sites.
Let

\[
 D_W=d_{01}F_{00}(W)-d_{00}F_{01}(W),\qquad
 U_W=d_{01}r_{00,W}-d_{00}r_{01,W}.                         \tag{6}
\]

Only `F00(Z)` has a target term.  Direct expansion therefore gives

\[
                    \boxed{U_WD_Z-U_ZD_W=-d_{01}U_W.}       \tag{7}
\]

For the port (1), in the order `00,01,10,11`,

\[
 U_{00}=-d_{00}BE,\qquad U_{01}=-d_{00}J,\qquad
 U_{10}=BL,\qquad U_{11}=CL.                               \tag{8}
\]

Equation (7) gives localized units in the `10` and `11` channels whenever
`B L` or `C L` is nonzero.  In the `01` channel both `F00` response
coefficients vanish, so the common factor `d00` cancels already in the
polynomial combination, yielding the sharper identity (3).

## 3. The aligned boundary has a pure cofactor tensor

The failure of the three units is not an unspecified degeneracy.  Form the
source-row difference

\[
                 D_W=d_{01}F_{00}(W)-d_{00}F_{01}(W).
\]

On `J=L=0`, equations (7)--(8), now applied with every binary word on the
four complementary sites, give

\[
 D_{01}=D_{10}=D_{11}=0,
 \qquad
 D_{00}=-d_{01}-d_{00}BE\,Q_{0000}.                       \tag{9}
\]

Equivalently, if

\[
                       T=d_{01}s_0-d_{00}s_1,
\]

then the aligned port satisfies

\[
                  p_0T=-d_{00}BE\,e_0^{(0)}e_0^{(1)}.      \tag{10}
\]

Thus, when `d00*B*E` is active, the surviving rows force the entire
complementary four-site divided square to be the nonzero pure tensor

\[
                 q_A^{[2]}=-{d_{01}\over d_{00}BE}Y_0^A.    \tag{11}
\]

For the contracted packet (3a), the same equation is

\[
              q_A^{[2]}=-{d_{01}\lambda\over d_{00}BE}Y_a^A. \tag{11a}
\]

The corresponding cap covector is
\(K_0=d_{01}\xi\eta^{\mathsf T}-d_{00}\xi\theta^{\mathsf T}\).
Its target ledger is \((d_{01}\lambda,0,0)\) after ordering the first
coordinate as \(a\), while its direct scalar and response square still
vanish.  Hence the contracted aligned row is the same inactive clean cap,
without a fixed-label-row hypothesis.

This is the exact handoff to the older Hamming-two/matching-shadow argument:
the generic port is already empty, while the aligned port supplies a
source-provenant pure cofactor tensor rather than another free cancellation
tail.  It does not by itself make the internal quadratic's diagonal support
a perfect matching or control the six-site top tensor.

### 3.1 The aligned port is already an inactive clean cap

There is also a useful cap interpretation of (10).  Let

\[
                    K_0=d_{01}E_{00}-d_{00}E_{01}.
\tag{12}
\]

Its direct scalar cancels identically,

\[
 s(K_0)=d_{01}d_{00}-d_{00}d_{01}=0,
\]

and its effective response is precisely

\[
 r(K_0)=p_0(d_{01}s_0-d_{00}s_1)
       =-d_{00}BE\,e_0^{(0)}e_0^{(1)}.                 \tag{13}
\]

Thus \(r(K_0)^{[2]}=0\) in the site-square-zero algebra.  At \(h=3\) the
homogeneous clean error is

\[
 {\cal E}(K)=s(K)r(K)^{[2]}q+r(K)^{[3]},               \tag{14}
\]

so (13) gives \({\cal E}(K_0)=0\).  The target coefficients are

\[
                    (\kappa_0,\kappa_1,\kappa_2)
                         =(d_{01},0,0),                 \tag{15}
\]

and \(s(K_0)=0\).  Hence this is a literal **clean but inactive** cap, not
the active clean point required by descent.  Its capped source row is

\[
                         r(K_0)q^{[2]}=d_{01}X_0,       \tag{16}
\]

which is the cap form of (11).

The multiplicity of this inactive landing is also exact.  On the identity
line

\[
 K(z)=K_0+zI,qquad s(z)=z\tau,qquad r(z)=r_0+zB,
\]

where \(\tau=s(I)\), \(B=r(I)\), and \(r_0=r(K_0)\), divided-power expansion
using \(r_0^{[2]}=0\) gives

\[
\boxed{
 {\cal E}(K(z))
 =z^2r_0\bigl(\tau Bq+B^{[2]}\bigr)
  +z^3\bigl(\tau B^{[2]}q+B^{[3]}\bigr).}             \tag{17}
\]

Every clean-error coordinate therefore has a double root at the inactive
point.  If \(\tau\ne0\), the line is active away from
\(z=0,-d_{01}\).  After removing the forced \(z^2\), the aligned boundary is
only the explicit linear tensor pencil

\[
 r_0(\tau Bq+B^{[2]})
       +z(\tau B^{[2]}q+B^{[3]}).                      \tag{18}
\]

Thus the aligned-port problem belongs exactly to the all-inactive
osculating ledger.  It is no longer an arbitrary six-site clean-error
cubic: an active landing is equivalent to one common non-boundary root of
the linear pencil (18), or to an ordinary source unit which excludes the
packet.

## 4. Proof impact

This is a direct Component-II/III interface for the unified two-chart
target.  The automatic full-nine theorem already makes every contraction
in (3a) a legal source row.  What it does not automatically supply is the
following fixed-support incidence:

> there are endpoint covectors \(\xi,\eta,\theta\), a target label \(a\),
> a second residual output axis, and two residual sites such that (3a)
> holds and the binary projections of
> \(P(\xi),S(\eta),S(\theta)\) have the triangular port (1).

This is the exact **contracted-port compatibility** still to be extracted
from a two-site shore, separated selectors, or the transported overlap.
Ordinary endpoint selectors alone do not imply it: they neither preserve a
fixed target label nor force the other binary components off the four-site
shore.  Conversely, once this incidence is produced, no internal diagonal
shadow is needed on the generic port stratum.  A nonzero port collision `J`
or `L` is immediately an ordinary source unit of the kind required by the
[monic-anchor equivalence](h3-monic-anchor-attaching-unit-equivalence.md).

The exact remaining boundary is deliberately explicit.  A general source
may fail to admit the support form (1), and even on (1) the equations
`J=L=0` are coefficient-feasible before the other full-nine rows are used.
The earlier matching-shadow unit closes some points on that aligned boundary,
but no theorem here claims that every rootless or maximal-shore packet reaches
one of the two units.  Equation (17) adds a second exact route on the aligned
boundary: use the remaining labelled rows to kill the linear residual (18),
or force its common root away from the activity divisor.  The next extraction
target is now:

> produce the contracted triangular two-site port from the transported
> full-nine overlap; then either its port collision is nonzero and (3)/(7)
> is a unit,
> or use the aligned equations `J=L=0` with the remaining labelled rows to
> force an active root of (18), an ordinary source unit, or the older
> Hamming-two unit.

## 5. Verification

Run

```text
.venv/bin/python computations/verify_h3_two_site_port_collision_unit.py
.venv/bin/python -O computations/verify_h3_two_site_port_collision_unit.py
```

The checker uses dependency-free sparse integer polynomial arithmetic.  It
reconstructs all eight literal rows at the four port words from the physical
matching formula, without specializing any of the sixty possible ordered
binary internal cells.  It
verifies the four response factorizations, all three instances of (7), the
aligned factorization (9) on all 64 binary output words, and the sharpened
identity (3).  It separately retains a symbolic anchor weight `lambda` and
verifies the contracted pure-anchor/crossed-zero form (3a)--(3b).  It also
expands (17) coefficientwise on all 64 binary words
with completely generic `q` and `B`, verifies the single-edge square-zero
statement on all 240 four-site binary slices, and then pins the
complete ledger digest
`57f5101d82dc81752edb8105ceb303d66f1569d5bf49efad3af5f6ab21853bf9`.
