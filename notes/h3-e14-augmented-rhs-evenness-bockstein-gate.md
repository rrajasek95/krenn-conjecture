# The E14 coupled right side is primitive, leaving a rho-even `Z/2` class

## Result

On the six alternating root-label lines, the coupled equation from the
simultaneous D4/P2/`K_Eq`/`d_even` gate is

\[
 (I+LF)K=A+X+LFC.                                      \tag{1}
\]

Write

\[
 D=(-1,1,-1,1),\qquad e=B_1+B_4,\qquad E=D\otimes e.
\]

The three literal contributions are

\[
 \pi_D(A)=-e,\qquad \pi_D(X)=+e,\qquad \pi_D(LFC)=+e. \tag{2}
\]

Here `A` is the D4 hidden face, `X` is the private packet of the old physical
`O_-E` lift, and `LFC` is the normalized cap face:

\[
 d_{even}={B_1+B_4\over2},\qquad
 L(d_{even})=2D\otimes d_{even}=E.                    \tag{3}
\]

Consequently

\[
             \boxed{A+X+LFC=e},                      \tag{4}
\]

which is primitive in `Z^6`, not even.  Since `LF` is the identity on the
alternating sector, (1) becomes

\[
                       2K=B_1+B_4.                   \tag{5}
\]

Thus

- over the theorem's characteristic-zero ring `k[beta]`, the unique solution
  is `K=(B1+B4)/2`, with no beta denominator;
- over `Z[beta]`, there is no solution;
- the obstruction is the rho-even class `[B1+B4]` in
  `coker(2I_6)=(Z[beta]/2)^6`.

The last two bullets concern only an optional integral coefficient form.  They
are **not** an obstruction to the conjecture over `k`: `2` is a unit in the
characteristic-zero field, so `K=e/2` is regular and beta-integral.  The open
proof issue remains physical construction and typing of the augmented
comparison, not parity.

Checker:
[verify_h3_e14_augmented_rhs_evenness_bockstein_gate.py](../computations/verify_h3_e14_augmented_rhs_evenness_bockstein_gate.py).

## Integral Smith calculation

The transfer gate gives

\[
 LF=P_D\otimes I_6.
\]

Restricting `I+LF` to the six labelled `D`-lines therefore gives `2I_6`.
Its Smith invariants are

```text
2,2,2,2,2,2
```

and its determinant is `64`.  Modulo two, the actual right side is

```text
(0,1,0,0,1,0).
```

The involution rho exchanges `B1` and `B4`, so this class is rho-even.  It
is still primitive in the invariant integral lattice: `B1+B4` is the orbit
sum basis vector, not twice another invariant vector.  In the selected
rho-even orbit the obstruction is therefore one `Z/2` class.  Either the
`B1` or `B4` coefficient modulo two detects it.

The sign remains load-bearing.  If the cap orientation were opposite, the
operator would be `I-LF`, which is already singular over `Q`; the committed
face signs instead give (5), nonsingular rationally but non-unimodular.

## The centered `/3`, `/30` construction does not leave a spare two

The selected-fibre compression gives the exact identities

\[
 (A_{match}+I)c_f=3c_{01},\qquad
 c_{01}=30b_{01}-R.                                   \tag{6}
\]

Equivalently,

\[
             3R+(A_{match}+I)c_f=90b_{01}.            \tag{7}
\]

Hence

\[
 \epsilon_{01}=
 {3\epsilon_R+(A_{match}+I)\epsilon_{c_f}\over90}.   \tag{8}
\]

This makes the selected response edge and its mixed `K_Eq` square automatic
over `Q[beta]`, assuming the physical centered lift.  It does not make (4)
even after normalization.

Indeed, even under the strongest augmented-naturality grant, the numerator
of the D-character right side is `90e`.  The scaled coupled system is

\[
                    2K_{num}=90e,
 \qquad K_{num}=45e.                                  \tag{9}
\]

The solution in (9) is integral but is not divisible by `90`.  Dividing by
the selected-fibre normalization returns `e/2`.  The only factor two in

\[
                   90=2\cdot3^2\cdot5
\]

has already been consumed by (8).  The complete coefficient projector
records the same fact as

\[
                         {8\over720}={1\over90}.       \tag{10}
\]

Thus `/3` and `/30` introduce no additional two-primary obstruction, but
they also supply no spare factor two for (5).

## Divided powers do not repair the parity

The four-root Boolean Hasse profile is

```text
1,4,6,4,1,
```

so the D4 top coefficient is one.  Likewise, for the relevant multi-affine
product,

\[
             D^{[2]}(fg)=D^{[1]}(f)D^{[1]}(g),        \tag{11}
\]

again with coefficient one.  The selected cap faces are

\[
                     face_3\mapsto-B_4,
 \qquad              face_5\mapsto-B_1.              \tag{12}
\]

Their sum has two different free labels, each with unit coefficient.  It is
not coordinatewise divisible by two.  Divided-power normalization therefore
does not turn the right side into `2e`.

An actual divided square of one repeated labelled source could carry a
factor two, but it would be a new source type and must be shown to have the
canonical word/fine/repeated grade and all augmented faces.  It is not the
current Boolean D4 or multi-affine product-rule cell.

## Relation to the existing Bockstein

The generic C-plus Smith gate has a beta-primary class and asks for a
Bockstein cell `V` with zero root output.  The obstruction above is different:
it is the constant class `[B1+B4]` modulo two in the alternating root output.
Because the existing `V` is root-zero, it cannot change (4).

If one additionally demands a `Z[beta]` coefficient form, the smallest
integral repair would be:

> Construct one source-valid augmented column whose alternating
> `D`-character proper face is `B1+B4` modulo two, so that the total coupled
> right side becomes 2-divisible.  It must also retain the selected response,
> word/fine/repeated, target, cap, ridge, `q`, and eta/sigma typing.  The old
> root-zero beta-Bockstein is a different operation.

Over characteristic-zero `k[beta]`, no such parity repair is needed:
multiplication by two is a unit, and the remaining issue is only physical
construction of the augmented face map.  Moreover, the `Z/2` class must not
be conflated with the genuine beta-Bockstein: `e/2` has no pole or division by
`beta`, so the beta-integral branch is unchanged.  The `Z/2` statement matters
only if a separate integral coefficient-lattice refinement is required.

## Scope

This is exact in the canonical `h=3` E14 quotient

\[
 \mathbb Z^4_{root}\otimes\mathbb Z^6_{B_0,\ldots,B_5}.
\]

It assumes the coupled comparison identifies the D4 hidden, old `O_-E`, and
cap faces as in the previous gate.  The source-valid realization of that
comparison remains open; the present calculation determines its exact
integral normalization and the primitive class left if no extra two-primary
face is supplied.

## Verification

Run normally, optimized, and isolated/no-site.  Expected headline:

```text
A+X+LFC on D-lines: B1+B4 (PRIMITIVE, NOT EVEN)
coupled equation: 2K=B1+B4
over char-0 k[beta]: K=(B1+B4)/2 (BETA-INTEGRAL)
optional Z[beta] form only: NONZERO RHO-EVEN Z/2 CLASS
```
