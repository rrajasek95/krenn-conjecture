# A two-site port collision gives an unrestricted-internal source unit

Research theorem.  `SP-CLEAN-BRIDGE` and Krenn's conjecture remain open.
This result weakens the internal-support hypotheses of the preceding
[two-site flag unit](h3-two-site-flag-h2-source-unit.md); it does not extract
the two-site port from an arbitrary full-nine packet.

## 1. Result

Work on six residual sites, call two of them `0,1`, and retain colours
`0,1`.  Every endpoint-coloured cell of the internal quadratic `q` is
arbitrary.  For the first endpoint row and two second endpoint rows assume
only the triangular two-site port

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

## 3. Proof impact

This is a direct Component-II/III interface for the unified two-chart
target.  A two-site shore or separated-port extraction no longer needs to
control the internal diagonal shadow in the generic port stratum.  It need
only produce a nonzero port collision `J` or `L`; either is immediately an
ordinary source unit of the kind required by the
[monic-anchor equivalence](h3-monic-anchor-attaching-unit-equivalence.md).

The exact remaining boundary is deliberately explicit.  A general source
may fail to admit the support form (1), and even on (1) the equations
`J=L=0` are coefficient-feasible before the other full-nine rows are used.
The earlier matching-shadow unit closes some points on that aligned boundary,
but no theorem here claims that every rootless or maximal-shore packet reaches
one of the two units.  The next extraction target is now:

> produce the triangular two-site port from the transported full-nine
> overlap; then either its port collision is nonzero and (3)/(7) is a unit,
> or use the aligned equations `J=L=0` with the remaining labelled rows to
> force an active clean cap or the older Hamming-two unit.

## 4. Verification

Run

```text
.venv/bin/python computations/verify_h3_two_site_port_collision_unit.py
.venv/bin/python -O computations/verify_h3_two_site_port_collision_unit.py
```

The checker uses dependency-free sparse integer polynomial arithmetic.  It
reconstructs all eight literal rows at the four port words from the physical
matching formula, without specializing any of the sixty possible ordered
binary internal cells.  It
verifies the four response factorizations, all three instances of (7), and
the sharpened identity (3), then pins the complete ledger digest
`109d35b77e33a90c2feb11802734b9274547cab029117479303671bd965bdd02`.
