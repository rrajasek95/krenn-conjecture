# The nonzero E14 private placement is necessarily a higher chain face

## Result

The exact conditional assignment isolated by the E14 first-hit calculation is

\[
 F=H_0-u\longmapsto1-v_{04}^{00},\qquad
 e_{\rm Eq}\longmapsto
 m=(p_{1,0}^1s_{1,1}^1)u_{35}^{11}v_{24}^{11}.       \tag{1}
\]

It sends the product to the required private return

\[
 F e_{\rm Eq}\longmapsto
 R_{E14}=m(1-v_{04}^{00}).                            \tag{2}
\]

Equation (2) is the correct chain-level construction target.  It cannot be
the raw degree-zero part of a nontrivial pointed source-algebra map.

The checker is
[`verify_h3_e14_keq_private_placement_pointedness_gate.py`](../computations/verify_h3_e14_keq_private_placement_pointedness_gate.py).

## Pointedness forces the private return to vanish

At the central base point, `F=H0-u` vanishes.  A pointed algebra comparison
must therefore send `F` to a function vanishing at the physical source point,
modulo the complete physical source ideal.  All generators of that ideal
already vanish at the point, so (1) forces

\[
                         1-v_{04}^{00}=0.              \tag{3}
\]

Multiplying (3) by the physical factor `m` gives

\[
                         R_{E14}=0.                    \tag{4}
\]

Thus the two desired properties are mutually exclusive for the raw
substitution:

```text
v04=1:  the assignment is pointed, but R_E14=0;
v04=0, m=1: R_E14=1, but the assignment is not pointed.
```

The same argument holds if the image of `F` is changed by an arbitrary
combination of physical source equations: those equations vanish at the
physical point and cannot change (3).

This does not contradict the exact identity
`B_E14=U[000101]*v24+R_E14`.  In the pointed branch it simply reduces to
`B_E14=U*v24`.  In the nontrivial private branch, (2) must be realized by a
higher principal-parts/Koszul comparison rather than by a map of functions.

## Consequence for the shortest AugP2 theorem

The anchor/conormal law requires a pointed source comparison, whose first
missing homogeneous face is

\[
                       [d(u_f-u)]=0.                  \tag{5}
\]

The private E14 landing requires the higher chain face (2).  The raw
assignment (1) cannot prove both: when it is pointed, the higher face is
trivial; when the higher face is nonzero, it is not pointed.

Therefore the shortest honest local theorem is still one natural augmented
`P2` totalization, but it must contain at least two distinct homogeneous
faces:

1. a higher chain cell landing `(H0-u)eEq` on `R_E14`; and
2. a pointed conormal cell killing `d(u_f-u)`.

After the first face, the old unary column supplies the full E14 target and
the remaining word-resolved residue is exactly
`-2 D_root tensor d_even`; the committed rooted `d_even` hypothesis cancels
it.  The scalar cap residue `z_cap` is independent.  None of those facts
repairs pointedness of (1).

## Scope

This is a no-go for the displayed raw factor assignment, not for a larger
augmented source algebra.  A larger PP/bar totalization may contain an
additional homotopy whose total boundary is (2) while its degree-zero map is
pointed.  Constructing precisely that homotopy is now the positive target.
The nonpointed branch is not by itself a physical terminal.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
recorded in the checker.
