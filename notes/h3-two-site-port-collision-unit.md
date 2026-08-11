# A contracted two-site port collision gives an unrestricted-internal source unit

Research theorem.  `SP-CLEAN-BRIDGE` and Krenn's conjecture remain open.
This result weakens the internal-support hypotheses of the preceding
[two-site flag unit](h3-two-site-flag-h2-source-unit.md); it does not extract
the two-site port from an arbitrary full-nine packet.

**Scope correction.**  The port certificate and its contracted version are
ordinary full-source identities and are unchanged.  Earlier revisions of
Section 3 called the aligned cap fully clean.  The checker only retained
binary output words, while (1) permits arbitrary third-colour components;
therefore the unconditional conclusion is binary-face cleanliness.  Full
cleanliness follows only under the explicit whole-row support condition at
the end of Section 3.1.

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

The triangular coefficient pattern is not needed if the whole contracted
endpoint forms are already supported on the same two physical sites.  This
part of the theorem is uniform on \(2h\) residual sites for every \(h\ge3\):
replace the four-site cofactor below by \(q^{[h-1]}\) on the other
\(2h-2\) sites.  Write
\(d_A,d_C\) for the direct coefficients of a pure-anchor contraction and a
crossed target-zero contraction, and put

\[
 P=P(\xi),\qquad
 T=d_C S(\eta)-d_A S(\theta).
\tag{3c}
\]

Assume \(P\) and \(T\) are supported on two sites \(u,v\), with completely
arbitrary ternary coefficients there.  Denote the nine coefficients of the
edge response \(PT\) by

\[
 U_{bc}=P_u(b)T_v(c)+T_u(b)P_v(c),
 \qquad 0\le b,c\le2.
\tag{3d}
\]

For the word which is \(b,c\) at \(u,v\) and \(a\) at all other sites,
let \(D_{bc}\) be the coefficient of
\(d_CF_{\xi,\eta}-d_AF_{\xi,\theta}\).  Literal expansion gives, for every
\((b,c)\ne(a,a)\),

\[
 \boxed{U_{bc}D_{aa}-U_{aa}D_{bc}
             =-d_C\lambda U_{bc}.}
\tag{3e}
\]

Consequently, on the localized nonzero-anchor chart
\(d_C\lambda\ne0\), any off-target \(U_{bc}\ne0\) is an ordinary localized
source unit.  If every off-target
coefficient vanishes and \(U_{aa}=0\), the anchor coefficient itself is
\(-d_C\lambda\), again a unit.  The only surviving boundary is therefore

\[
 U_{bc}=0\ ((b,c)\ne(a,a)),\qquad U_{aa}\ne0.             \tag{3f}
\]

On (3f) the full ternary response is the single pure edge
\(U_{aa}e_a^{(u)}e_a^{(v)}\), its divided square is zero, and the rows force

\[
 q_{W\setminus\{u,v\}}^{[h-1]}
       ={d_C\lambda\over U_{aa}}Y_a.                       \tag{3g}
\]

Thus a whole-row two-site port needs neither the triangular normal form nor
an internal matching normalization: it is generically source-empty, and its
only survivor is a genuine inactive clean cap.  If only a two-colour
projection is supported on \(u,v\), the same determinant remains valid on
that projection, but the third-colour tail is not controlled.

There are two companion collision units.  On the active `d00*d01` chart,
if `B` or `C` is nonzero, every surviving packet must satisfy

\[
                         \boxed{J=0,\qquad L=0.}             \tag{4}
\]

Consequently the pure-matching hypotheses of the older Hamming-two unit are
needed only on the codimension-two aligned-port boundary (4), not on the
generic triangular port.

## 2. Universal single-edge determinant

The identities above are a special case of a source-row calculation
independent of the matching degree.  Fix a pure output word `Z` and words
`W` which differ from it only at the two port sites.  Because the effective
response is supported on that edge, the response part of row `i` at `W` is

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

For the triangular port (1), in the order `00,01,10,11`,

\[
 U_{00}=-d_{00}BE,\qquad U_{01}=-d_{00}J,\qquad
 U_{10}=BL,\qquad U_{11}=CL.                               \tag{8}
\]

Equation (7) gives localized units in the `10` and `11` channels whenever
`B L` or `C L` is nonzero.  In the `01` channel both `F00` response
coefficients vanish, so the common factor `d00` cancels already in the
polynomial combination, yielding the sharper identity (3).

## 3. The aligned boundary has a pure binary-face cofactor tensor

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

then the binary projection of the aligned port satisfies

\[
          \pi_{01}(p_0T)=-d_{00}BE\,e_0^{(0)}e_0^{(1)}.   \tag{10}
\]

Thus, when `d00*B*E` is active, the surviving rows force the binary
projection of the complementary four-site divided square to be the nonzero
pure tensor

\[
 \pi_{01}(q_A^{[2]})=-{d_{01}\over d_{00}BE}Y_0^A.          \tag{11}
\]

For the contracted packet (3a), the same equation is

\[
 \pi_{ab}(q_A^{[2]})
       =-{d_{01}\lambda\over d_{00}BE}Y_a^A.                \tag{11a}
\]

The corresponding cap covector is
\(K_0=d_{01}\xi\eta^{\mathsf T}-d_{00}\xi\theta^{\mathsf T}\).
Its target ledger is \((d_{01}\lambda,0,0)\) after ordering the first
coordinate as \(a\), while its direct scalar vanishes and its binary
response projection has square zero.  No statement about the third-colour
components is implicit here.

This is the exact handoff to the older Hamming-two/matching-shadow argument:
the generic port is already empty, while the aligned port supplies a
source-provenant pure binary-face cofactor tensor.  It does not by itself
make the internal quadratic's diagonal support a perfect matching, control
the third-colour coefficients, or control the six-site top tensor.

### 3.1 The aligned port has an inactive clean binary face

There is also a useful cap interpretation of (10).  Let

\[
                    K_0=d_{01}E_{00}-d_{00}E_{01}.
\tag{12}
\]

Its direct scalar cancels identically,

\[
 s(K_0)=d_{01}d_{00}-d_{00}d_{01}=0,
\]

and the binary projection of its effective response is precisely

\[
 \bar r(K_0):=\pi_{01}r(K_0)
       =-d_{00}BE\,e_0^{(0)}e_0^{(1)}.                 \tag{13}
\]

Thus \(\bar r(K_0)^{[2]}=0\) in the binary site-square-zero algebra.  At
\(h=3\), writing bars for binary projection, the projected homogeneous
clean error is

\[
 \pi_{01}{\cal E}(K)
   =s(K)\bar r(K)^{[2]}\bar q+\bar r(K)^{[3]}.          \tag{14}
\]

so (13) gives \(\pi_{01}{\cal E}(K_0)=0\).  The target coefficients are

\[
                    (\kappa_0,\kappa_1,\kappa_2)
                         =(d_{01},0,0),                 \tag{15}
\]

and \(s(K_0)=0\).  Hence this is a literal **binary-face clean but
inactive** cap.  Full ternary cleanliness, which is required by descent,
does not follow unless the unrecorded third-colour components vanish or are
separately controlled.  Its projected capped source row is

\[
                   \bar r(K_0)\bar q^{[2]}=d_{01}X_0,  \tag{16}
\]

which is the cap form of (11).

There is nevertheless an exact binary osculation.  Put
\(\bar B=\pi_{01}r(I)\).  On the identity line

\[
 K(z)=K_0+zI,\qquad s(z)=z\tau,\qquad
 \bar r(z)=\bar r_0+z\bar B,
\]

where \(\tau=s(I)\) and \(\bar r_0=\bar r(K_0)\), divided-power expansion
using \(\bar r_0^{[2]}=0\) gives

\[
\boxed{
 \pi_{01}{\cal E}(K(z))
 =z^2\bar r_0\bigl(\tau\bar B\bar q+\bar B^{[2]}\bigr)
  +z^3\bigl(\tau\bar B^{[2]}\bar q+\bar B^{[3]}\bigr).} \tag{17}
\]

Every binary-face clean-error coordinate therefore has a double root at the
inactive point.  If \(\tau\ne0\), the line is active away from
\(z=0,-d_{01}\).  After removing the forced \(z^2\), a necessary condition
for a full clean landing is the explicit linear binary tensor pencil

\[
 \bar r_0(\tau\bar B\bar q+\bar B^{[2]})
       +z(\tau\bar B^{[2]}\bar q+\bar B^{[3]}).        \tag{18}
\]

A full active clean landing must give a common non-boundary root of (18),
but a root of (18) is not sufficient until the third-colour error
coordinates are also killed.  If the whole contracted rows, not only their
binary projections, are supported on the two port sites, then bars may be
removed everywhere in (13)--(18); in that stronger case \(K_0\) is a
genuine inactive clean cap and (18) is the full residual.

## 4. Proof impact

This is a direct Component-II/III interface for the unified two-chart
target.  The automatic full-nine theorem already makes every contraction
in (3a) a legal source row.  What it does not automatically supply is the
following fixed-support incidence:

> there are endpoint covectors \(\xi,\eta,\theta\), a target label \(a\),
> and two residual sites such that (3a) holds and the scalar-zero effective
> response
> \(P(\xi)(d_CS(\eta)-d_AS(\theta))\) is supported on their single
> physical edge.

This is the exact **single-edge contracted-port compatibility** still to be
extracted from a two-site shore, separated selectors, or the transported
overlap.  It is strictly weaker than the triangular flag: the endpoint
coefficients on the two sites are arbitrary, and only their scalar-zero
response combination matters.  Ordinary endpoint selectors alone do not
imply it because they neither preserve a fixed target label nor remove the
response from the other four sites.  Conversely, once this incidence is
produced, (3e)--(3g) give either an ordinary source unit or a genuine
inactive clean cap without any internal diagonal shadow.

The exact remaining boundary is deliberately explicit.  A general source
may fail to admit a single-edge response, and binary support alone leaves
the third-colour components.  The earlier matching-shadow unit closes some
points on the triangular aligned boundary, but no theorem here claims that
every rootless or maximal-shore packet reaches the one-edge theorem.
Equation (17) supplies a bounded binary necessary test when only the
projection is available.  The next extraction target is now:

> produce a pure-anchor/crossed-zero contraction whose scalar-zero response
> is supported on one physical edge; or, if only its binary projection is
> edge-supported, use the remaining labelled rows to kill the third-colour
> tail.  The full-support case is already closed by (3e)--(3g).

## 5. Verification

Run

```text
.venv/bin/python computations/verify_h3_two_site_port_collision_unit.py
.venv/bin/python -O computations/verify_h3_two_site_port_collision_unit.py
```

The checker uses dependency-free sparse integer polynomial arithmetic.  It
reconstructs all eight literal rows at the four triangular-port words from
the physical matching formula, without specializing any of the sixty
possible ordered binary internal cells.  It
verifies the four response factorizations, all three instances of (7), the
aligned factorization (9) on all 64 binary output words, and the sharpened
identity (3).  It separately retains a symbolic anchor weight `lambda` and
verifies the contracted pure-anchor/crossed-zero form (3a)--(3b).  With
eighteen completely generic ternary endpoint coefficients on two sites, it
then reconstructs all 729 output words and all eight determinant channels
in (3e), with no coefficient zero inside the port.  A source-faithful
mutation which adds one endpoint component at a third site leaves a nonzero
36-term determinant residual, guarding the single-edge support hypothesis.
It also
expands the binary identity (17) coefficientwise on all 64 binary words
with completely generic binary `q` and `B`, verifies the single-edge
square-zero statement on all 240 four-site binary slices, and then pins the
complete ledger digest
`d7e0fef7952808046faddd0022c39e124acbd365909c0628dc1972e861e7ec0b`.
