# Full occurrence symmetrization leaves the original Eq normal class

## Result

Using all 90 pure matching occurrences is genuinely better than choosing
one: it cancels every private occurrence-graph face integrally and leaves a
single symmetric class.  But that class is exactly the original Eq
conormal, not a boundary of the occurrence simplex.

Write

\[
 H_0=\sum_{M=1}^{90}f_M,qquad E_M=f_M-z_M,qquad
 B=\sum_{M=1}^{90}z_M-U.                               \tag{1}
\]

The 90 equations `E_M=0` adjoin contractible graph coordinates
`z_M=f_M`.  The physical pure equation pulls back as

\[
                 F_0=H_0-U=\sum_M E_M+B.              \tag{2}
\]

Let `d a_M=E_M` and `d r0=F0 e_Eq`.  Then the full integral chain

\[
 K_{\rm sym}=r_0-\sum_Ma_Me_{\rm Eq}                  \tag{3}
\]

has the exact boundary

\[
                         \boxed{dK_{\rm sym}=B e_{\rm Eq}.}  \tag{4}
\]

No division by 90 is needed.  Equation (4) is the strongest valid output of
the occurrence symmetrization.  Eliminating the private graph coordinates
maps `B` to `H0-U=F0`, so it has compressed the 90 selected diagonals to one
normal class without nullhomotoping that class.

The apparent final equality

\[
                         \sum_Mz_M=H_0=U                 \tag{5}
\]

uses two different kinds of equality.  The first equality follows from the
contractible graph equations.  The second is the physical source equation
`F0=0`.  Setting `B=0` in (4) is therefore base change by the very equation
whose underived source lift is sought.  Its connecting class is the pinned
nonzero conormal `[F0] in J/J^2`.

Thus complete occurrence symmetry gives a useful positive compression:
the next object is precisely the absolute Koszul/Tate normal cell for the
pair `(B,Eq)`.  It does not supply that cell's physical augmented
comparison.  The labelled-residue, anchor, ridge/word, terminal, parity,
and `C5` obligations remain.

## 1. Why the full simplex cannot kill `B`

Let `C0=Z^90` be the occurrence-vertex lattice.  The degree-one boundary of
the full occurrence simplex is

\[
                 \operatorname{im}d_1=\ker\epsilon,qquad
                 \epsilon(x)=\sum_Mx_M.                \tag{6}
\]

The 89 star edges `e_M-e_1` form an integral basis of this image: deleting
the first row gives the identity matrix.  Hence (6) is saturated.  Higher
simplex faces give relations among these edges and cannot enlarge their
image in `C0`.

In the target-augmented lattice with coordinates `(z_1,...,z_90,U)`, the
class

\[
                          B=(1,\ldots,1,-1)              \tag{7}
\]

is outside (6).  It is primitive: the negative `U` coordinate kills every
simplex edge and reads one on `B`.  The complete bar therefore kills all
occurrence differences but leaves the trivial occurrence representation
paired with the physical target.

Adding (7) as the augmentation equation makes the reduced simplex exact,
but that addition is exactly the physical Eq presentation.  It is not a
new bar face.

## 2. Coefficient scaling

Symmetrizing the 90 *selected one-graph cones* is not the same as (3).  Put

\[
                         K_M=r_0-a_Me_{\rm Eq}.          \tag{8}
\]

Then

\[
 d\sum_MK_M=89\sum_ME_M+90B,                           \tag{9}
\]

and the normalized average has

\[
 d\left({1\over90}\sum_MK_M\right)
       ={89\over90}\sum_ME_M+B.                        \tag{10}
\]

So averaging does not close the graph faces and still leaves `B`.  More
generally, if weights `c_M` sum to one so the coefficient of the physical
row remains one, then the coefficient of `E_M` is `1-c_M`.  Killing every
`E_M` would require every `c_M=1`, incompatible with `sum c_M=1`.

Nor does splitting the target help.  For weights `w_M` with `sum w_M=1`,

\[
               \sum_M(z_M-w_MU)=\sum_Mz_M-U=B.          \tag{11}
\]

Thus individual normalized diagonals sum to the original conormal rather
than cancel it.  The integral chain (3) is the unique useful compression:
it cancels all graph faces and isolates `B` with coefficient one.

## 3. Identification with the Koszul/Tate gate

The graph extension is an isomorphism after eliminating its private
coordinates, and

\[
                          [B]\longmapsto[F_0]\ne0
                          \quad\text{in }J/J^2.          \tag{12}
\]

The selected target-coordinate functional reads `-1` on this conormal.
Therefore evaluating `B=0` on the source is insufficient; a source chain
must lift before quotienting.

For the actual pair of equations `(B,Eq)`, the absolute Koszul cell

\[
 \theta=\epsilon_B\wedge\epsilon_{\rm Eq},qquad
 d\theta=B\epsilon_{\rm Eq}-\operatorname{Eq}\epsilon_B \tag{13}
\]

does give `-B e_Eq` after relative base change by `Eq=0`.  This is the
canonical unaugmented continuation of (4).  The pinned physical audit shows
why it is not yet `K_Eq(beta)`: the nearest old representative has the
right Eq boundary and zero target/`W`, but carries labelled ordinary residue
`+Y`.  A second primitive separator is `pure Eq + ainc`.  Ridge, source
word, private, terminal, and physical `q` rows are not assigned by the
Koszul universal property.

Full occurrence symmetrization has therefore reduced the problem to the
already exact next lemma:

> Construct the augmented comparison from the symmetric normal Koszul cell
> to the complete physical homotopy fibre, cancelling its labelled-residue
> and `Eq+ainc` classes in the literal repeated grade.

## 4. Odd/even projections do not collapse

Occurrence symmetrization and the endpoint involution `rho` act on separate
tensor factors.  The required common source datum is still a regular orbit

\[
                    \mathbf Q\{C,\rho C\},qquad
                    C_-=C-\rho C,quad C_+=C+\rho C.    \tag{14}
\]

The symmetric class `B` survives in both coefficient projections:

```text
odd:          -B,
generic even: +2 D B tensor v,
beta special: +B.
```

The even coefficient has the expected eight nonzero `+/-1` entries, but
this is only coefficient typing.  Occurrence symmetry does not construct
`C,rho C`.  For the nearest physical Tate representatives, the labelled
ordinary-residue values remain

\[
                 \operatorname{ores}(C_-)=(1,-1),qquad
                 \operatorname{ores}(C_+)=(1,1).       \tag{15}
\]

The odd aggregate in (15) sums to zero, but its labelled row is not zero.
Thus symmetrization commutes with both parity projectors while preserving
their two independent physical obstruction lines.  One parity still does
not imply the other.

## 5. The `C5` aggregate remains

The five transported endpoint/rootless comparison edges have the oriented
`C5` incidence matrix, of rank four in five.  Tensoring with the symmetric
occurrence class `B` does not change this rank or cokernel.  Tensoring also
with the regular `rho` orbit gives two block copies: rank eight in ambient
rank ten.  Hence one primitive comparison aggregate survives in each parity
line.

So complete occurrence symmetry eliminates the need to choose an individual
matching diagonal, but it does not eliminate the later component aggregate.
A physical augmented comparison must still land nontrivially on that
aggregate after the reduced-Eq edge faces are supplied.

## Scope and verification

Proved here:

- the exact integral symmetric chain (3)--(4);
- the saturated occurrence-simplex augmentation obstruction;
- the failure of raw, normalized, and target-split averaging;
- identification of `B` with the pinned conormal/Koszul-Tate gate;
- survival of both parity obstruction lines and both `C5` aggregates.

Not proved: the augmented Tate-to-physical comparison or
`K_Eq(beta)` itself.

Run

```text
python3 computations/verify_h3_reduced_eq_full_occurrence_simplex_symmetrization_gate.py
python3 -O computations/verify_h3_reduced_eq_full_occurrence_simplex_symmetrization_gate.py
python3 -I -S computations/verify_h3_reduced_eq_full_occurrence_simplex_symmetrization_gate.py
```

All modes print ledger digest
`78ecc59aa828bfb9d423a568d3ae694bad8c8630f1f17f43989ac654544175a9`.
