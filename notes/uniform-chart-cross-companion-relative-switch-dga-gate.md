# The omitted chart companions form one relative switch DGA

## Canonical parent of every omitted matching

After selecting one chart-direction edge and one tail edge, the complete
lower coefficient is a perfect-matching sum on `2h-2` vertices.  Call the
two surviving chart vertices `r,s`.

The fixed-chart terms contain `rs`.  Every omitted term pairs `r,s` to two
distinct residual vertices `y,z`.  It has a unique fixed parent obtained by
the four-cycle switch

\[
             rs,yz\quad\longleftrightarrow\quad
             ry,sz\quad\hbox{or}\quad rz,sy .        \tag{1}
\]

Thus each fixed term has exactly `2h-4` companions, and every companion has
one parent.  With

\[
 |F|=(2h-5)!!,qquad |C|=(2h-4)(2h-5)!!,
\]

the complete packet has `(2h-3)!!` terms, as required.

Checker:
[`verify_uniform_chart_cross_companion_relative_switch_dga_gate.py`](../computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py).

## The smallest presentation-safe graph schema

For every occurrence `M`, add a graph coordinate `z_M`.  For every
companion `c`, add a switch carrier `t_c`.  Let `p(c)` be its parent and add
degree-one generators

\[
\begin{aligned}
 d\theta_M&=z_M-u_M,\\
 d\phi_c&=t_c-(z_c-z_{p(c)}).
\end{aligned}                                      \tag{2}
\]

Both equations are monic in the new variables.  Hence (2) resolves the old
occurrence algebra: eliminate `z=u` and
`t_c=u_c-u_p(c)`.  The combination

\[
 \Gamma_c=\phi_c+\theta_c-\theta_{p(c)}
\]

has

\[
 d\Gamma_c=t_c-(u_c-u_{p(c)}).                       \tag{3}
\]

In particular `d^2=0`.  Explicit matrices at `h=3,4` verify that the graph
plus its natural augmentation spans the whole extended degree-zero module
and that `H0` has the original complete-packet dimension.

Let `P` be the sum of all complete-packet occurrences, `F` the fixed sum,
and `T=sum t_c`.  Every parent occurs `2h-4` times, so summing (3) gives

\[
             \boxed{P-(2h-3)F=T-d\Gamma_{\rm sum}.}  \tag{4}
\]

Thus `T` is exactly the cross-chart completion carrier.  Setting `t=0` is
not a construction: it identifies every companion with its parent and
changes the degree-zero fibre from dimension `(2h-3)!!` to `(2h-5)!!`.

## Proper faces and induction

A child and its parent share `h-3` spectator edges.  Differentiating a
common edge commutes with the parent map in (1), so that face is exactly the
same relative switch graph at order `h-1`.

The switch cycle has four other faces:

```text
two child-only cross-edge faces,
two parent-only fixed-edge faces.
```

Their retained operation labels place them in the committed
`C2+/C4/P2` lower list.  There is no further face species.  Formally,
for any labelled occurrence-face operator `X`, extend (2) by

```text
Xu and Xz = the same occurrence face,
Xtheta     = its graph lift,
Xt_c       = X(z_c-z_parent),
Xphi       = 0.
```

Then `[d,X]=0`; two commuting labelled faces retain `d^2=0` and give the
same cobar square as the relative `P2` graph.

The exhaustive counts through `h=6` are:

| h | fixed | companions | complete | companions per fixed |
|---:|---:|---:|---:|---:|
| 2 | 1 | 0 | 1 | 0 |
| 3 | 1 | 2 | 3 | 2 |
| 4 | 3 | 12 | 15 | 4 |
| 5 | 15 | 90 | 105 | 6 |
| 6 | 105 | 840 | 945 | 8 |

At `h=3`, the two children of the one fixed term split into their difference
and sum.  The difference is the endpoint-odd Cartan line.  The sum is the
endpoint-even carrier `T`.  The pinned `7b67277` calculation identifies its
coefficient exactly with the transported `D6`/`C+` class

\[
                    (2,2,-1,-1,-1,-1).               \tag{5}
\]

So the conditional `C+/P2` construction has exactly the right
**kappa-weighted even coefficient projection**.  It does not yet constitute
the whole lower carrier landing.  The `D,Q` and `P,S` faces are `C4` faces;
the pinned finite descent leaves one generic flat, tail-covariant,
same-grade relative-`C4` primitive, and explicitly proves that its operation
and repeated grade do not identify it with `P2` by relabelling.

## What remains independent

This does not turn the conditional coefficient formula into a physical
source map.  The committed interface still lacks the restriction/
reinsertion map from the relative occurrence carrier `t` to the physical
target, reduced-Eq, residue, `q`, anchor, `W`, ridge, word, fine, and
repeated-grade rows.  Equation (4) shows sharply why the carrier cannot be
killed formally.

There are therefore two homological levels and one precise lower refinement:

1. a top fixed-chart Spencer generator whose scalar proper face is
   `L_h=(2A-B-C)H_(h-1)`;
2. its lower chart-completion carrier, whose `QQ/PQ/SQ` physical landing is
   the `C+/P2` interface above and whose `DQ/PS` face still needs the generic
   relative-`C4` primitive.

`C+/P2` does not replace the top generator: it lives on its proper face and
has the forced target-bearing signature, whereas `L_h` is the retained
fixed-chart scalar.  Conversely, once the **full** physical `C+` interface
is built, its objectwise `K_Eq` correction supplies central Eq.  Central Eq
is not a third independent cell.

The shortest positive theorem is one natural augmented map from the
universal switch carriers `t_c` to the physical even `C+/P2` orbit,
including the same-grade `DQ/PS` relative-`C4` face, compatible with
common-edge recursion and all four switch-cycle faces, and composed with
the separate top chart-Spencer generator.

The checker proves the matching-switch DGA and formal labelled proper-face
classification.  It does not claim the physical carrier landing.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
`891417e16e2eacce959d576a8b2e2a09d61e3c97a9aede9c9216211ba326dc16`.
