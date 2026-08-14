# Pure normalization and the full q-Jacobian do not cone the balanced square

## Verdict

Let

\[
                    z=(1,1,-1,-1)
\]

be the balanced-square class of `0ffc23a`, in vertex order
`A0,A1,B0,B1`.  Multiplication by the shore sign
`diag(1,1,-1,-1)` turns the four signless `K2,2` columns into ordinary
oriented incidence columns and sends `z` to

\[
                         \mathbf 1=(1,1,1,1).
\]

Thus the obstruction really is the constant `H0` class.  Since the ordinary
incidence image is exactly the kernel of vertex augmentation, an extra
square-output column kills it if and only if its augmentation is nonzero.
In particular, a cell with `dE=z` has gauged augmentation `4` and would finish
this local square.

Neither proposed shortcut supplies such a column.

1. Physical pure-target normalization dehomogenizes `u=1`, hence `du=0`.
   It removes the radial target-scale tangent but does not construct the
   pointed conormal `P_f`, much less a degree-one relative square cell.
2. The full simultaneous-`q` calculation supplies the genuine `171`-column
   scalar-source Jacobian and the three-term product-rule anchor conormal.
   Those are respectively a map into unary/response coefficient rows and a
   row on its source domain.  No restriction/insertion face from that map to
   the relative chart-operation square has been constructed.

The distinction is not merely formal.  The smallest complete four-corner
packet retaining one copy of every presently named cap--Cartan column family
still has an exact balanced detector after both normalized pure-target
columns are adjoined.  This is a minimality statement for that named family
inventory, not for every possible abstract linear presentation.  Therefore
the shortest remaining input is one source-valid cross-grade cone cell, not
another ordinary `q` derivative or normalization identity.

Exact checker:

```text
computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py
```

## 1. The exact cone criterion

The four signless edge columns are

\[
 e_{A0}+e_{B0},\quad e_{A0}+e_{B1},\quad
 e_{A1}+e_{B0},\quad e_{A1}+e_{B1}.
\]

They have rank three and are annihilated by `z`.  After the shore-sign gauge
they become the four oriented `K2,2` incidences.  Their image has rank three
and lies in

\[
           \ker(\epsilon),\qquad
           \epsilon(x_0,x_1,x_2,x_3)=\sum_i x_i.
\]

The two spaces have the same dimension, so they are equal.  Consequently,
for any proposed extra column `c`,

```text
epsilon(c)=0      -> c is already an ordinary incidence boundary;
epsilon(c)!=0     -> incidence plus c has rank four and kills H0.
```

This is the useful source-level test.  It avoids searching blindly for the
exact vector `z`: one pointed vertex column of augmentation one is already
enough, because the old incidence columns correct it to any other desired
representative.

## 2. What fixed pure-target normalization actually gives

On the physical affine source fibre the pure equations are

\[
                       H_{\rm pure}-1=0.
\]

Thus the homogeneous target coordinate is fixed and `du=0`.  For the
90-occurrence centered face, this gives the already checked identity

\[
                         \gamma_c=90P_f-B.
\]

This is a positive reduction only **after** a physical pointed `P_f` is
granted.  Normalization itself is not `P_f`: the status of that conormal
remains open in the complete word/fine/`q`/anchor comparison.

The four-word target audit reaches the same conclusion.  In the order

```text
mixed c|i, mixed i|c, pure i, pure c,
```

the square defect is `(1,1,-1,-1)`, while the two normalized pure rows span
only the last two coordinates.  They cannot cancel the two mixed components.
Constants on their right-hand sides add no mixed cotangent row.

## 3. What the full simultaneous-q calculation gives

The checker reruns the universal physical calculation:

```text
36 endpoint columns + 135 decorated q columns = 171 columns;
729 unary rows + 2916 response rows;
10,935 generic unary q entries with 32,805 terms;
43,740 generic response q entries with 524,880 terms.
```

Every `q` column is checked twice: by the cofactor formula and by literal
differentiation of every matching occurrence.  For the marked occurrence

\[
 p_1[0,1]s_1[1,1]q_{23}^{00}q_{45}^{00},
\]

the anchor row is the exact product-rule differential

\[
 H=s_1q_{23}q_{45}\,dp_1
   +p_1s_1q_{45}\,dq_{23}
   +p_1s_1q_{23}\,dq_{45}.
\]

This corrects the old endpoint-only selector, but it does not change
variance: `H` is a conormal row on the 171-dimensional scalar-source domain.
The desired `E` is a new source cell whose boundary has a component in the
four-dimensional relative operation-tag square.  A physical theorem must
construct a restriction/insertion map connecting these grades.  The formulas
above contain no such map.

## 4. The pure-safe augmented counterguard

Use the known cap--Cartan columns

\[
\begin{aligned}
 r0_j&=B_j+Eq_j+\operatorname{target}_j-M-\operatorname{ainc}
        +P_{f,j},\\
 T_j&=-W_j+\operatorname{target}_j,\\
 \rho_j&=W_j+\operatorname{ores}_j,\\
 K&=\sum_j\alpha_j\operatorname{ores}_j+\operatorname{ridge},
\end{aligned}
\]

where `q=M-ainc` is literal and

\[
                 \alpha=(-1,1,1,-1).
\]

There are thirteen named columns (`r0_j,T_j,rho_j,K`).  Adjoin, as actual
columns, the two normalized pure-target selectors `target_2` and `target_3`.
This is stronger than merely fixing their affine right-hand sides.

On these fifteen columns the following primitive integer dual vanishes:

```text
B                 ( 1,  1,-1,-1)
Eq                ( 0,  0, 1, 1)
target            (-1, -1, 0, 0)
W                 (-1, -1, 0, 0)
ordinary residue  ( 1,  1, 0, 0)
M, ainc, q, P_f    0,  0, 0, 0
ridge, eta, sigma  0,  0, 0, 0.
```

The cancellations are columnwise:

- on the two mixed corners, `B+target=0`;
- on the two pure corners, `B+Eq=0`;
- `T` and `rho` cancel through `target/W/ores`;
- `alpha dot (1,1,0,0)=0`, so `K` needs no ridge coefficient;
- arbitrary pointed-anchor values and literal `q=M-ainc` are invisible
  because the dual coefficients on `P_f,M,ainc,q` are zero.

The fifteen old columns have rank `15`; adjoining the balanced `B` face
raises the rank to `16`, and the displayed dual reads it as `4`.  Hence pure
normalization, anchor, physical `q`, ridge, eta and sigma are all compatible
with survival of the constant class in this exact named-row packet.

## 5. Why this is the sharp logical guard, not a source counterexample

The universal physical `q` Jacobian may be carried as a direct summand of
the augmented packet.  Extending the displayed detector by zero on that
summand still annihilates every `q`-Jacobian column and still reads the
balanced face as `4`.  Therefore separate availability of

```text
the balanced square,
the normalized pure rows,
the full physical q Jacobian and anchor differential,
and the named cap/Cartan/ridge packet
```

does not imply a cone cell.

This direct sum is not asserted to be a complete GHZ source tensor.  Its
purpose is to isolate exactly the missing gluing datum.  A physical source
may contain an additional cross-grade restriction/reinsertion square that
the direct sum omits; constructing that square is the positive route.

## 6. Shortest remaining theorem and terminal fork

The local positive statement is now:

> Construct one physical source cell `E`, in the identical
> word/fine/repeated/common-tail grade, whose projection to the gauged
> chart square has nonzero vertex augmentation.  Verify on that same cell
> the literal `q=M-ainc`, product-rule pointed anchor, and labelled ridge
> restriction/reinsertion faces.

If its square face is exactly `z`, this is `dE=z`; a one-vertex face is also
sufficient by the cone criterion.  Once the exhaustive same-grade physical
map is present, exact image/cokernel duality gives the final fork:

```text
balanced face in the full image     -> physical cone/filler dE=z;
balanced face outside the full image -> normalized augmented terminal.
```

The current primitive detector already extends through every named row.
To promote it to the terminal branch one must still prove that it annihilates
every additional literal response/block-projector and downstream word column
in the exhaustive same-grade source map, or correct it there without losing
its value on `z`.

## Scope and verification

This result is exact for canonical `h=3`, characteristic zero.  It reruns
the complete universal simultaneous-`q` polynomial Jacobian and proves the
15-column pure-safe augmented counterguard by exact rational rank.  It does
not construct a finite exact GHZ source or a counterexample to the Krenn
conjecture.

Run:

```text
python3 computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py
python3 -O computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py
python3 -I -S computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py
```

Frozen ledger SHA-256:

```text
721148070b0687f52e23f1c0ba36561a24a21892c552bd01d60802a6511edae7
```
