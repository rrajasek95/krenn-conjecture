# A universal relative occurrence graph exists; its centered carrier is the exact classical defect

## Result

The eight pointed `P2` sections can be packaged by one explicit relative
graph resolution. Let `A` be the physical coefficient algebra and let

\[
                         u_0,\ldots,u_{11}\in A        \tag{1}
\]

be the twelve literal matching-occurrence functions in one response word.
No algebraic independence of the `u_i` is assumed. Put

\[
                         C=12I-J.                     \tag{2}
\]

Adjoin graph variables `z_i`, centered carrier variables `t_i`, and Koszul
generators `theta_i,phi_i` with

\[
 d\theta_i=z_i-u_i,
 \qquad
 d\phi_i=t_i-(Cz)_i.                                 \tag{3}
\]

The equations are successively monic in `z_i` and `t_i`. Their Koszul
complex is therefore a resolution of `A`, with

\[
                         z=u,\qquad t=Cu              \tag{4}
\]

in degree-zero homology. Thus (3), with `t` retained, has exactly the old
classical physical fibre.

Now define

\[
                 \Gamma_i=\phi_i+\sum_jC_{ij}\theta_j. \tag{5}
\]

Then

\[
                         d\Gamma_i=t_i-(Cu)_i.        \tag{6}
\]

This is the sought universal `C_i` family—but relative to the centered
carrier `t`. It replaces eight unrelated source columns by one natural
formula indexed by the marked occurrence.

The exact obstruction is now transparent. Turning (6) into the absolute
boundary `dGamma_i=-(Cu)_i` means setting `t_i=0`. That changes

\[
                         H_0:A\longrightarrow A/(Cu). \tag{7}
\]

On the complete response fibre `sum_i u_i=0`, equation `Cu=0` forces every
`u_i=0`. Hence killing the carrier is not a presentation change or a
contractible graph attachment; it imposes the desired new occurrence
equations on the old physical fibre.

Checker:
[verify_h2_p2_relative_occurrence_graph_resolution_gate.py](../computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py).

## 1. Presentation-safe graph resolution

Work in

\[
 K=A[z_0,\ldots,z_{11},t_0,\ldots,t_{11}]
       \otimes\Lambda(\theta_0,\ldots,\theta_{11},
                       \phi_0,\ldots,\phi_{11}).       \tag{8}
\]

First quotienting by `z_i-u_i` eliminates the twelve `z` variables without
changing `A`. After that, quotienting by `t_i-(Cz)_i` eliminates the twelve
`t` variables. Because each equation is monic in a fresh variable, the
twenty-four equations form a regular sequence even when `A` has zero
divisors. Therefore the Koszul augmentation

\[
 K\longrightarrow A,qquad
 z\mapsto u,quad t\mapsto Cu,quad\theta,\phi\mapsto0 \tag{9}
\]

is a quasi-isomorphism.

At the linear conormal level, the checker uses coordinates `(u,z,t)`. The
twenty-four columns

\[
 d\theta_i=(-e_i,e_i,0),
 \qquad
 d\phi_i=(0,-C_i,e_i)                                \tag{10}
\]

have rank 24, while the twelve columns `(e_i,e_i,C e_i)` complete them to
rank 36. Formula (6) follows by direct substitution:

\[
 d\phi_i+\sum_jC_{ij}d\theta_j
  =t_i-(Cz)_i+(Cz)_i-(Cu)_i.
\]

The carrier satisfies `sum_i t_i=0` in `H0`, because every row and column
sum of `C` is zero. Its full rank is eleven. On the endpoint-even private
sector relevant to the displayed P2 packet, the rank is five.

## 2. Root principal-parts functoriality

A labelled one-root face retains the structural occurrence tag and maps one
word object to another. Let `D` be its diagonal occurrence mask. Extend the
root derivation by

\[
\begin{aligned}
 Xu&=Du',& Xz&=Dz',& X\theta&=D\theta',\\
 Xt&=CDz',& X\phi&=0.                                \tag{11}
\end{aligned}
\]

Then

\[
\begin{aligned}
 X(d\theta)&=D(z'-u')=d(X\theta),\\
 X(d\phi)&=CDz'-CDz'=0=d(X\phi),\\
 X(d\Gamma)&=CD(z'-u')=d(CD\theta').                 \tag{12}
\end{aligned}
\]

Thus every labelled root is a chain derivation of the relative graph
resolution. For two root directions on distinct factors, their diagonal
masks commute. Equations (11)--(12) then give equal two-step actions on
`theta` and `t`; the signed two-path cobar has `d^2=0`, exactly as in the
explicit square of `711f051`.

The important qualification is visible in (11): `Xt` uses the graph
coordinate `z`. This is a perfectly valid relative graph action, but it does
not descend to a physical action on a pre-existing `t` carrier—there is no
such physical carrier yet. The construction solves source-side coherence,
not physical landing.

The first-principal-parts reinsertion has the equally exact form

\[
               \delta(q\Gamma)=q\,\delta\Gamma+(\delta q)\Gamma. \tag{13}
\]

The second term is present in `K`. Its image in the labelled physical
`Q/ores` rows remains part of the carrier-landing theorem.

## 3. Exact relation to the eight P2 sections

The section-count theorem gives the private preimage as

\[
 z_{\rm priv}=
 {35\over1728}(c_0+c_3)
 -{1\over432}(c_2+c_4+c_7+c_9)
 -{19\over1728}(c_8+c_{11}),                         \tag{14}
\]

where `c_i=(Cu)_i=12u_i-sum_j u_j`. Apply the same coefficients to the
relative generators (5). Their boundary is

\[
                         t_{z_{\rm priv}}-z_{\rm priv}(u). \tag{15}
\]

Thus the graph resolution genuinely replaces eight ad hoc columns by one
indexed family and its one displayed linear combination. It does not erase
the eight literal tags: they reappear as eight instantiations of `Gamma_i`
and as the carrier component `t_zprivate`.

## 4. The sharp classical-fibre defect

At the linear occurrence level, take

\[
                         u=e_0-e_1.                   \tag{16}
\]

It obeys the complete response equation `sum u_i=0`, but

\[
                         Cu=12(e_0-e_1)\ne0.          \tag{17}
\]

The relative graph (3) contains this point, with `z=u` and `t=Cu`. The
absolute quotient `t=0` excludes it. Exact ranks say the same thing:

```text
graph relations                         rank 24 in 36 coordinates
graph + t=0                             rank 35
graph + t=0 + complete response         rank 36.
```

This counterpoint is a sharp quotient of the literal response block, not a
claim that it extends to a full nonlinear Krenn source. Its role is to prove
that the graph manipulation alone cannot preserve the old classical fibre.

More categorically, any boundary in a resolution of `A` maps to zero under
the augmentation (9). But `(Cu)_i` maps to the generally nonzero physical
function `12u_i-sum u_j`. Therefore no quasi-isomorphic graph presentation
can make it an absolute boundary without either:

- retaining an external carrier with the same physical value, as `t` does;
- restricting to the closed subfibre `(Cu)_i=0`; or
- mapping the first nonlift to an accepted physical terminal.

## 5. What remains physical

The relative carrier has rank eleven, and its endpoint-even private part
has rank five. The already isolated primitive cap `p=(-Q,-ores)` is one
rank-one projected class. It is not the whole carrier: `7e9467c` separates
the pointed conormal from `p`, and even the best same-label `p_Q`
cancellation leaves a labelled `ores` value detected by `-35/72`.

The next map is therefore precise:

> Construct an augmented physical landing of the relevant `t`-carrier orbit
> into the mixed-target, cap `Q/ores`, `dq`, anchor, Eq, `W`, eta/sigma, and
> physical-`q` rows, natural for the labelled roots and restriction/
> reinsertion. Or prove that its first nonlift covector extends over the
> complete augmented source as an accepted exchange, relative generator, or
> Fredholm terminal.

With that map, (15) supplies the P2 boundary and the explicit graph cobar
supplies all higher coherence. Without it, setting `t=0` simply assumes the
centered occurrence theorem.

## Scope

This is an exact algebraic construction over an arbitrary physical
coefficient algebra `A`. It constructs the relative graph/Koszul family and
its labelled root action. It does not construct the physical carrier
landing or promote an abstract carrier covector to a terminal.

Run:

```text
python3 computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py
python3 -O computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py
python3 -I -S computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py
```

Frozen ledger SHA-256:

```text
3886506f894797f08cad5b581461f5e4e8e42d512246f3647515cb8e6e41f6d9
```
