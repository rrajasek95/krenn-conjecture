# Sigma-evenized odd Cartan residue does not cancel the root-even labelled debt

The nearest physical dressing of the generic root-even reduced-Eq face has

\[
 (\operatorname{lower},\operatorname{Eq},W,
   \operatorname{target},\operatorname{ores})
       =(E,E,0,0,-E),
\quad
 E=2D_{\rm root}\otimes v,                             \tag{1}
\]

where

\[
 D_{\rm root}=(-1,1,-1,1),
 \qquad v={B_1+B_4\over2}.
\]

This note tests whether the physical endpoint-odd Cartan residue can remove
the final `-E` while preserving lower and Eq.

Checker:
[`verify_h3_cplus_root_even_labelled_ores_sigma_cartan_gate.py`](../computations/verify_h3_cplus_root_even_labelled_ores_sigma_cartan_gate.py).

## 1. What sigma does to the physical Cartan line

The physical Cartan cell `K_alpha` has

\[
 \operatorname{lower}(K_\alpha)=\operatorname{Eq}(K_\alpha)=0,
 \qquad
 \operatorname{ores}(K_\alpha)=
 \alpha=B_0+B_2-B_3-B_5.                              \tag{2}
\]

Thus adding it does preserve the desired Eq and lower coefficients.  It
also carries its pinned eta/sigma terminal packet, but granting cancellation
of that packet will only strengthen the attempted construction below.

There are two actions which must not be conflated.  The stabilizer inside
one canonical fine grade acts on pure labels as

\[
                    \sigma_B=(B_0\ B_5)(B_2\ B_3),    \tag{3}
\]

fixing `B1` and `B4`, and sends `alpha` to `-alpha`.

The physical cut symmetry `sigma=(2 5)(3 4)` moves the first lower object
to the second.  Through the two pinned K4 charts its transition is

\[
 \tau_B=(B_0\ B_5\ B_3\ B_2)(B_1\ B_4),              \tag{4}
\]

and therefore

\[
 \tau_B(\alpha)=\alpha'=B_0-B_2-B_3+B_5,
 \qquad \tau_B(v)=v.                                  \tag{5}
\]

Thus the cut-sigma even and odd combinations have objectwise residues
`(alpha,alpha')` and `(alpha,-alpha')`.  The within-grade involution adds
only `-alpha`.  Neither construction produces the fixed-plane vector `v`.

## 2. A complete labelled separator

The primitive covector

\[
                  \chi=(0,1,-1,0,1,-1)                \tag{6}
\]

satisfies

\[
 \chi(\mathbf1)=\chi(\alpha)=\chi(\alpha')=0,
 \qquad \chi(v)=1.                                    \tag{7}
\]

Now make a deliberately stronger grant than the physical inventory: in
each of the four root words, allow independent scalar-diagonal, `K_alpha`,
and cross-cut `K_alpha'` lines.  Their total residue space is

\[
 \mathbf Q^4\otimes\langle\mathbf1,\alpha,\alpha'\rangle. \tag{8}
\]

It has rank twelve.  The four word-local covectors `e_r^* tensor chi` kill
(8), while on the debt `-E` their values are

```text
+2, -2, +2, -2.
```

Thus adjoining `-E` raises the rank to thirteen.  In particular, the physical
sigma orbit—which is a subspace of the generous grant—cannot cancel it.
This remains true even if every eta/sigma terminal introduced by the Cartan
cells is declared harmless.

So neither sigma parity supplies the complete labelled residue, even after
granting more Cartan copies than the physical inventory currently contains.

## 3. The necessary source section

A pure section

\[
 d_{\rm even}:
 \quad \operatorname{ores}={B_1+B_4\over2},
 \quad
 \operatorname{lower}=\operatorname{Eq}=W=\operatorname{target}
 =\operatorname{ainc}=\operatorname{terminal}=0        \tag{9}
\]

does solve the residue problem: root decoration by `2D_root` supplies `+E`
and cancels (1) without changing Eq or lower.  The stronger supply of
separate sections `d_B1,d_B4` also suffices by averaging.  The present result
does not construct either object.

The exact weakest full-source criterion is the rank-one specialization of
the denominator membership theorem.  For the physical readout
`r_even:X -> Q d_even`, put `K=ker r_even` and choose a section `s`.  Then

\[
 d_{\rm even}\text{ is realized in }\ker J
 \quad\Longleftrightarrow\quad
 Js(d_{\rm even})\in J(K).                            \tag{10}
\]

Failure gives the corresponding one-dimensional dual covector.

## 4. Relation to the earlier `d_fixed,d_pair` gate

Gate I asks for one fixed section and one paired section, chosen from

```text
fixed:  B1 or B4,
paired: (B0+B5)/2 or (B2+B3)/2.
```

That rank-two quotient is not the quotient needed here.  Even after granting
both Cartan directions `alpha,alpha'`, for every one of the four choices,

\[
 v\notin
 \langle\alpha,\alpha',d_{\rm fixed},d_{\rm pair}\rangle; \tag{11}
\]

the rank increases from four to five when `v` is adjoined.  By contrast,
the two-fixed quotient `span(d_B1,d_B4)` contains `v`.

There is a useful conditional compression.  If the scalar ordinary-residue
row had a genuine six-label diagonal section `mathbf1`, then

\[
\begin{aligned}
 v&={1\over2}\mathbf1+{1\over2}\alpha'-2p_{05},\\
 v&={1\over2}\mathbf1-{1\over2}\alpha'-2p_{23}.
\end{aligned}                                           \tag{12}
\]

Thus a diagonal section plus either paired Gate-I section and the translated
Cartan line would close the coefficient problem.  The committed inventory
has only a scalar `ores` row and explicitly does not construct that
labelwise diagonal section.  Equation (12) is a sharper common construction
target, not a current closure.

The evaluated denominator routes are exactly

```text
face 3 -> B4,       face 5 -> B1.
```

The direct-free packet has both conditional memberships and would supply
`d_even` after the still-open physical placement/protected correction.  The
tilted packet has only the `B4` membership and therefore does not.  This is
the same sharp control found by the earlier rank-two theorem, now applied to
the two-fixed rather than fixed-plus-paired projection.

## Frontier

The shortest remaining source theorem for the labelled-ores part of generic
`C_+` is:

> Construct one same-grade sigma-covariant `d_even` section, or prove both
> fixed face-3/`B4` and face-5/`B1` memberships.

`K_alpha`, its sigma translate, scalar residue, and coarse cancellation do
not reduce this obligation.  Word/fine/repeated placement and the separate
lower/private `+E` debt from (1) remain part of the full `C_+` comparison.
