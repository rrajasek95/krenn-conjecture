# The E14 central equality is one primitive mixed mapping-cylinder face

## Result

The moving-target fourth-Hasse top and the clean central reduced-Eq cell
have the correct **coefficient** sum.  In the quotient

```text
(private return R_E14, central incidence E=(H0-u)e_Eq)
```

their columns are

```text
D4 top       (1,0)
clean K_Eq   (0,1)
required     (1,1).
```

This equality does not yet give a physical pointed comparison.  Restoring
the source presentations produces a two-row mapping square.  Its bottom
edge is the pointed conormal `P_f=d(u_f-u)`, its top edge is the
moving-target `D4` occurrence transport, and its two vertical edges are the
objectwise central `K_Eq` maps.  The four-edge skeleton has

\[
 H_1\cong\mathbb Z,
 \qquad z=(1,-1,1,-1),
\]

and no two-cell.  Thus the edge data do not force the diagonal.  One mixed
mapping-cylinder/Tate face is both necessary and sufficient to fill `z` and
carry

\[
 \boxed{\Phi_{\rm orb}((H_0-u)e_{\rm Eq})=R_{E14}}. \tag{1}
\]

Checker:
[`verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py`](../computations/verify_h3_e14_pointed_orbit_keq_mapping_cylinder_gate.py).

## What functoriality does and does not prove

A full pointed **derived-algebra natural transformation** over the D4 orbit
would contain the missing square face, so (1) would follow from that stronger
hypothesis.  The currently available statement is only objectwise:
pointedness supplies the bottom conormal and the clean Eq construction
supplies the vertical edges.  It does not choose a homotopy between the two
routes around the square.

Equivalently, retain one additional physical-source coordinate recording
mixed-square incidence.  The separate D4, `K_Eq`, and horizontal cap data
have

```text
(R, E, mixed incidence) = (1,0,0), (0,1,0), (0,0,0),
```

while the required comparison is `(1,1,1)`.  The primitive dual
`(0,0,1)` kills all separate edge data and reads one on the comparison.
This is the first cotangent/excess class.  Forgetting source idempotents
forgets its third coordinate, which is why the formal coefficient sum looks
complete.

This also explains the earlier pointedness no-go.  A raw substitution
`H0-u -> 1-v04` cannot be pointed with nonzero `R_E14`.  Moving (1) to the
higher square face keeps the degree-zero algebra map pointed, but the higher
face must actually be constructed; pointedness alone does not create it.

## Relation to the coupled physical identity

For one nonzero root-label coefficient, retain

```text
(D4 return, root lower, root Eq, rooted ores).
```

Then

```text
D4 top          = (1, 0,0, 0)
P2_hidden       = (0,-1,0, 0)
O_-E            = (0,+1,+1,-1)
rooted d_even   = (0, 0,0,+1).
```

Consequently the exact physical identity from `649b7eb` is

\[
 P2_{\rm hidden}+O_{-E}+d_{\rm even}^{\rm root}
       =(0,0,+1,0),                                  \tag{2}
\]

the clean root-Eq face.  The D4 top is **not** literally
`P2_hidden=-E`: they occupy different direct-sum rows, and the root-lower
coordinate separates them.  A physical realization of (1) must carry
`P2_hidden` as a proper face of its totalization; it cannot identify it with
the occurrence top.

There is nevertheless a sharp positive sign coincidence.  The four
codimension-one faces of the oriented D4 cell have boundary signs

```text
(-1,+1,-1,+1)=D_root.
```

Thus the D4 boundary would give `P2_hidden=-E` if every marked D3 face had
the physical source-labelled image `-(B1+B4)=-2*d_even`.  The committed D4
orbit transports the marked occurrence with coefficient one; it does not
supply this label map, its factor two, or its `P3+K2` placement.  That
D3-to-`B1/B4` map is the exact first proper-face datum.

Likewise, D4 plus the horizontal cap graph has zero rooted labelled residue,
so it does not by itself construct `d_even`.  That conclusion changes only
after all three typed inputs are available:

\[
 p_i=(-Q_i,-\operatorname{ores}),\qquad n_i=(+Q_i,0),
\]

and the literal label map sends face `3` to `B4` and face `5` to `B1`.
Then

\[
 d_{\rm even}
 =-\frac12\big[(p_3+n_3)_{B_4}+(p_5+n_5)_{B_1}\big]
 ={B_1+B_4\over2}.                                  \tag{3}
\]

Thus rooted `d_even` is a composite face once the primitive cap, physical
`K_Eq` descent, and labelled face map are part of the same comparison.  It
is circular to use `d_even` to dress `K_Eq` and then cite that dressed cell
as the `n` needed to derive `d_even`.

The cap relation is similarly exact but conditional:

\[
 z_{\rm cap}=p+n=(0,-\operatorname{ores}_{\rm cap}). \tag{4}
\]

The horizontal cap graph normalizes target/residue after placement; it does
not manufacture the source-labelled `p` or `n` entering (4).

There is no further coefficient ambiguity once the two labelled face maps
exist.  In source order `(face3,face5)` and target order `(B1,B4)`, the cap
residue and literal label matrices are

\[
 F=-I_2,\qquad L=\begin{pmatrix}0&1\\1&0\end{pmatrix},
 \qquad LF=\begin{pmatrix}0&-1\\-1&0\end{pmatrix}.   \tag{5}
\]

Thus `rank(LF)=2`, `det(LF)=-1`, and its eigenvalues are `-1` on the even
line `(1,1)` and `+1` on the odd line `(1,-1)`.  In particular

\[
 -\tfrac12 LF(1,1)=(\tfrac12,\tfrac12)=d_{\rm even}. \tag{6}
\]

So a supplied rho-even pair plus the literal label map forces the desired
`d_even` coefficient with the correct sign; no coefficient kernel remains.
The odd face difference is a separate unconstructed sector if only the
even orbit top is known, but it is not needed for the even packet.  The
open issue is source-labelled provenance of `L` and of both `p+n` faces,
not another scalar transfer direction.

## Minimal source datum and remaining face count

The minimal new central object is one mixed two-cell
`kappa_orb,Eq`.  Its square boundary is `z`, its principal physical image is
`R_E14`, and its full proper-face packet must include:

- the hidden root-lower face `-E`;
- the invisible physical `K_Eq` cap face `n`;
- the literal face-`3/5` to `B4/B1` label transport; and
- the central Eq incidence.

After this cell is installed, the old unary row supplies `T12`; no separate
`T12` generator remains.

Solving (2)--(4) leaves four independent homogeneous face types in the
shortest augmented `P2` theorem:

1. `P_f`, the pointed conormal;
2. one cap base face, written either as primitive `p` or as `z_cap` after
   the `n` face of the mixed cell is retained;
3. `kappa_orb,Eq`, the mixed orbit/central-Eq face; and
4. `gamma=-dOmega`, the shifted Kähler/ridge face.

One natural augmented comparison may package all four, but they have
independent detectors.  In particular, the new central cell does not make
the shifted ridge automatic; it only makes eta/sigma automatic after the
labelled ridge is supplied.

The two cap bases do not change this count.  Since `z_cap=p+n` and `n` is a
proper face of `kappa_orb,Eq`, the bases `(p,kappa)` and
`(z_cap,kappa)` differ by a triangular determinant-one change.  Rewriting
in terms of `z_cap` makes the simultaneous construction noncircular, but it
does not remove a homogeneous face.

## Word, grade, and beta scope

The missing cell is genuinely off-diagonal among physical source summands:

```text
cap input       word 01211222, fine t*q_(v,N), repeated P3+K2
lower P2 inputs words 0112/q23:21 and 0121/q45:12
D4 response     110000 -> G11[111111]
unary E14 top   word 000101.
```

Same-word multiplication cannot provide this transport.  The square class
is primitive over `Z`, hence remains free after base change to `Z[beta]`,
on the generic fibre, and at `beta=0`.  A generic construction therefore
does not automatically supply the `D0`/Bockstein face: the mixed cell and
all its proper faces must be defined integrally over `k[beta]`.

This is an exact canonical `h=3` obstruction/construction interface.  It
does not construct `kappa_orb,Eq`, the all-`h` spectator transport, or a
physical terminal from its primitive dual.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
printed by the checker:

```text
12cfdfac6b8c3b76b2445a443404e0575ee61aa2d8b7ad816cc154151e2ccf21
```
