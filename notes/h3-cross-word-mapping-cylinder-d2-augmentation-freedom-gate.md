# `d^2` forces a closed mixed debt, not its filler or private/Eq value

## Verdict

Conditional on a physical, source-labelled top arrow from response word

```text
11:110000
```

to cap word

```text
01211222,
```

and on its known six `db01` and eighteen `dL01` faces, the strongest
`d^2`-forcing statement is false in two distinct ways:

1. `d^2=0` forces the associated naturality-square debt to be a closed
   primitive cycle, but does not force a source 2-cell bounding it.
2. Even after a mixed filler is granted, `d^2=0` does not fix its terminal
   private/reduced-`Eq` augmentation.

The exact augmentation freedom modulo the old cap rows is

\[
 \Pi_{B/Eq}(\kappa)\equiv\lambda(\delta,0),\qquad
 \delta=(1,1,-1,-1),\qquad
 \delta\cdot(B-Eq)=4\lambda,
 \quad \lambda\in\mathbb Q.                           \tag{1}
\]

Thus there is no forced exact value.  `lambda=0` is a dark filler and
`lambda=1` is a primitive bright control with unnormalized value `4` and
normalized value `1`.

Checker:
[`verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py`](../computations/verify_h3_cross_word_mapping_cylinder_d2_augmentation_freedom_gate.py).

## 1. What `d^2` actually forces

Use four presentation vertices and order the source-labelled edges as

```text
bottom P_f, left K_Eq, right K_Eq, top cross-word arrow.
```

Their vertex boundaries are the columns

\[
 \begin{aligned}
 b&=(-1,1,0,0),& \ell&=(-1,0,1,0),\\
 r&=(0,-1,0,1),& t&=(0,0,-1,1).
 \end{aligned}                                        \tag{2}
\]

This matrix has rank three.  Its primitive kernel is

\[
                        z=(1,-1,1,-1),                 \tag{3}
\]

and direct multiplication gives `d_1 z=0`.  Consequently the square
one-skeleton

\[
                    C_1=\mathbb Q^4\longrightarrow C_0=\mathbb Q^4
\]

already is a valid chain complex.  There is no `C_2`, so the degree-two
`d^2` condition is vacuous, while

\[
                         H_1\cong\mathbb Q.             \tag{4}
\]

This is the smallest exact counterguard to existence-by-`d^2`.  The top
edge and every objectwise boundary may exist physically, but edge
functoriality alone does not supply a homotopy between the two routes around
the square.

What is forced is the *debt* (3): once all four edges are present, their
oriented boundary is closed and primitive.  To force a filler one must add a
stronger hypothesis, such as a pointed derived-natural mapping cylinder or
explicit square exactness.  Under that hypothesis a normalized cell
`kappa` has

\[
                         d\kappa=z                     \tag{5}
\]

up to simultaneous orientation.  Equation (5) kills (4), but this is a
consequence of the extra exactness assumption, not of `d^2=0`.

## 2. Why `db01` and `dL01` do not change the conclusion

The known proper faces are strictly typed response objects.  Their literal
cap projection is

```text
six db01 images       = six copies of zero_8,
eighteen dL01 images  = eighteen copies of zero_8.
```

They conserve `delta.(B-Eq)` and leave the old cap rank at seven.  Their
nonzero response-side detectors are covectors on a different summand.  Thus
adjoining the exact `db01/dL01` boundary complex to (2) does not add a map
from the square debt to the terminal `B/Eq` coordinates.

This is the precise role of the physical typing: it prevents an informal
identification of a response direction coefficient with a cap
private/reduced-`Eq` coefficient.

## 3. Granting a filler still leaves its augmentation free

Let

\[
 A=\mathbb Q^8_{B/Eq}
\]

be the terminal projected cap block.  Extend the square complex by one
mixed generator and define

\[
 C_2=\langle\kappa\rangle
   \xrightarrow{d_2} C_1\oplus A
   \xrightarrow{d_1} C_0,
 \qquad
 d_2\kappa=(z,a),\qquad d_1=(d_{\rm square},0).        \tag{6}
\]

For every `a in A`,

\[
                 d_1d_2\kappa=d_{\rm square}z=0.      \tag{7}
\]

Hence the mixed-incidence coefficient in (5) and the cap augmentation `a`
are independent data.  The checker verifies (7) on a basis of all eight
augmentation directions and on the important controls

\[
 0,qquad (\delta,0),\qquad(0,\delta),\qquad
 (\delta,\delta).                                     \tag{8}
\]

In particular the two cells

```text
d kappa_dark   = (z, 0),          chi=0,  Psi=0,
d kappa_bright = (z, (delta,0)), chi=4,  Psi=1
```

have identical source-labelled square boundary and both satisfy `d^2=0`.
They are a chain-level logical counterguard.  The bright choice is not
asserted to be an already constructed physical source cell.

## 4. Exact quotient of the freedom

In the eight cap coordinates, the four private/`Eq` diagonals and four
signless `K2,2` companion columns have rank seven.  Their span is exactly
the kernel of

\[
                     \chi=\delta\cdot(B-Eq).           \tag{9}
\]

Since `chi(delta,0)=4`, every `a in A` has the unique quotient normal form

\[
 a\equiv\lambda(\delta,0)\pmod{\operatorname{im}M_{\rm old}},
 \qquad
 \lambda={\chi(a)\over4}.                             \tag{10}
\]

This proves (1).  It also separates two normalizations that were easy to
conflate:

- once filler existence is independently granted, its primitive square
  boundary coefficient is one, up to orientation;
- its normalized cap value `lambda=Psi(a)` remains arbitrary.

The packaging ranks `2 -> 3 -> 4` say that the mixed square incidence is a
new third homogeneous direction.  They do not identify that direction with
the one-dimensional private/`Eq` quotient.

## 5. Sharp extra hypotheses

The assumed top arrow and its PP faces supply:

- the top cross-word edge;
- the literal `db01/dL01` response boundaries; and
- after the objectwise `K_Eq` edges are included, the closed debt `z`.

They do not supply:

- a source 2-cell bounding `z`;
- the primitive cap face;
- physical `K_Eq`/invisible-cap descent in the cap grade; or
- the scalar `lambda` in (10).

The shortest existence hypothesis is therefore:

> the top arrow extends to a pointed derived-natural PP mapping cylinder
> whose mixed square cell has boundary `z`.

The shortest forced-augmentation hypothesis is one clause stronger:

> a physical source-labelled cap/`K_Eq` descent law computes
> `Pi_BEq(kappa)` modulo the old cap image.

Equivalently, that theorem must specify the one scalar

\[
                         \lambda=\Psi(\Pi_{B/Eq}\kappa).\tag{11}
\]

Then and only then is the requested value forced, namely `chi=4 lambda`.
For terminal landing it must be nonzero.  If a separate physical theorem
proves the primitive `B`-only convention, (11) is `lambda=1`, giving
`chi=4`; this number does not follow from `d^2`.

## Scope

This is an exact rational minimal-chain and cap-quotient theorem, retaining
the committed strict typing of the six `db01` and eighteen `dL01` faces.  It
refutes the implication from the stated top/boundary hypotheses to a mixed
filler or to a fixed augmentation.  It does not rule out construction of a
physical bright filler from the full source, nor does it claim that every
formal augmentation in (6) is source-valid.
