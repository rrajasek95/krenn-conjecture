# Two live trade signs force a cross-colour carrier dichotomy at \(h=3\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

Continue in the cross-colour terminal class of
[the internal-edge localization theorem](h3-cross-colour-repair-internal-edge-localization.md).
Put

\[
 u=d_{01}+2d_{02},\qquad v=d_{01}-2d_{02},             \tag{1}
\]

and, for \(c\in\{0,1\}\), abbreviate

\[
\begin{aligned}
 A_c&=q(2@c,5@2),\\
 B_c&=q(2@2,4@c),\\
 C_c&=q(3@c,5@2).
\end{aligned}                                         \tag{2}
\]

> **Two-sign terminal support dichotomy.** If \(u\ne0\) and \(v\ne0\), then
> all four \(2\)-mixed orientations on the internal edge \(23\) vanish, and
> exactly one or both of the following support alternatives holds:
> \[
> \begin{array}{ll}
> \text{\(4\)-carrier zero:}&B_0=B_1=0,\\[2mm]
> \text{\(5\)-carrier zero:}&A_0=A_1=C_0=C_1=0.
> \end{array}                                         \tag{3}
> \]

Using the degree-one relation

\[
             q(3@2,4@c)=-q(2@2,4@c)=-B_c,            \tag{4}
\]

the first branch in fact kills four carrier-\(4\) cells:

\[
 q(2@2,4@c)=q(3@2,4@c)=0\qquad(c=0,1).               \tag{5}
\]

Thus away from the two resonant hyperplanes \(u=0\) and \(v=0\), the hardest
cross-colour nonclean packet splits into complementary four-zero carrier
branches. This is a narrowing of the \(h=3\) terminal class, not a clean-cap
contradiction.

## 2. Direct proof from the full-row trade

The two sign families C2 in the localization note state:

\[
\begin{array}{rcl}
u\ne0&\Longrightarrow&
q(2@c,3@2)=0,\qquad A_cB_{c'}=0,\\
v\ne0&\Longrightarrow&
q(2@2,3@c)=0,\qquad C_cB_{c'}=0,
\end{array}                                          \tag{6}
\]

for every \(c,c'\in\{0,1\}\). With both scalars live, the first equations in
(6) kill the four orientations

\[
 q(2@0,3@2),\ q(2@1,3@2),\
 q(2@2,3@0),\ q(2@2,3@1).                            \tag{7}
\]

If \(B_0=B_1=0\), the first alternative in (3) holds. Otherwise choose
\(c'\) with \(B_{c'}\ne0\). Every product equation in (6) then gives

\[
                         A_0=A_1=C_0=C_1=0,
\]

which is the second alternative. No division by an internal edge variable
and no generic nonvanishing assumption beyond (1) is used.

## 3. Interaction with localization

Localization C3 says that some \(2\)-mixed edge with its non-\(2\) colour at
site \(2\) or \(3\) must remain live. Equation (7) removes the entire edge
\(23\) from that obligation. On the \(5\)-carrier-zero branch, (3) removes
the four candidate orientations from sites \(2,3\) to site \(5\) as well.
Consequently C3 must then place its live mass on an edge from \(2\) or \(3\)
to \(0,1,\) or \(4\).

On the \(4\)-carrier-zero branch, equations (5) concern the opposite
orientation—the colour \(2\) remains at sites \(2,3\)—so the localization
obligation is not automatically shortened in the same way. This asymmetry is
useful: a subsequent branch argument should treat the two carriers
separately rather than restoring a symmetric 20-variable search.

## 4. Exact audit

The load-bearing full-row identities (6), including their provenance from
the \(9\times729\) system, are already checked exhaustively by
[verify_h3_cross_colour_repair_internal_edge_localization.py](../computations/verify_h3_cross_colour_repair_internal_edge_localization.py)
in normal, optimized, and isolated modes.

[verify_h3_cross_colour_terminal_support_dichotomy.py](../computations/verify_h3_cross_colour_terminal_support_dichotomy.py)
audits the new logical step by exhausting all \(2^6=64\) zero/nonzero
patterns of \(A_0,A_1,B_0,B_1,C_0,C_1\). Exactly 19 obey all eight product
constraints: 16 lie in the \(B_0=B_1=0\) branch, while the three with live
\(B\)-support have all four \(A,C\) entries zero. It is standard-library
only and remains live under normal, optimized, and isolated Python.

## 5. Revised local frontier

The unconditional cross-colour terminal class now divides into:

1. the resonant sign branches \(d_{01}=\pm2d_{02}\), where only one trade
   family is available;
2. the two-sign \(4\)-carrier-zero branch (5); and
3. the two-sign \(5\)-carrier-zero branch, where localization must escape
   through sites \(0,1,4\).

The next exact search or hand lemma should be conditioned on these three
packets. Re-running the undivided 155-variable residual discards the carrier
information proved here.
