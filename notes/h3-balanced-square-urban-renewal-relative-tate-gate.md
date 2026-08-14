# Urban renewal preserves the balanced-square `H0` class

## Verdict

The ordinary four-terminal square move is exact, but it cannot supply the
missing Gate-II cross-grade cone.

Let the four fully labelled chart vertices be

```text
A_[D|Q] = D*q01*H,  grade Hasse[2](D,Q01), ordered D|Q
A_[Q|D] = D*q01*H,  grade Hasse[2](D,Q01), ordered Q|D
B       = p0*s1*H,  grade Hasse[2](P0,S1)
C       = p1*s0*H,  grade Hasse[2](P1,S0)
```

on the fixed window `2345`, with

\[
 H=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.            \tag{1}
\]

The balanced face is

\[
 Z=A_{[D|Q]}+A_{[Q|D]}-B-C.                            \tag{2}
\]

Identifying the two ordered direct copies sends (2) to
`2*A-B-C=L01`.  The four formal mate rows form a `K2,2` and have rank
three; the normalized dual

\[
                  \psi_Z={1\over4}(1,1,-1,-1)          \tag{3}
\]

kills them and reads one on `Z`.

For cyclic square weights `a,b,c,d`, urban renewal is defined on

\[
                       \Delta=ac+bd\ne0                \tag{4}
\]

and replaces the weights by

\[
                  (a',b',c',d')={1\over\Delta}(c,d,a,b). \tag{5}
\]

This is a birational boundary-signature equivalence.  It only replaces the
four edge-incidence columns by the same four edge-incidence columns with new
coefficients.  After the shore-sign gauge, their image is the kernel of
vertex augmentation, while `Z` becomes the constant vertex class.  Hence no
urban-renewal column has nonzero `Z` augmentation, even on `D(Delta)`.

There is one formal relative Tate construction:

\[
                          dG=t-\Delta Z.                \tag{6}
\]

It preserves `H0` and has nonzero `Z` component on `D(Delta)`, but it retains
the carrier `t`.  The dual (3) extends uniquely by

\[
                          \psi_Z(t)=\Delta.             \tag{7}
\]

Thus (6) transports the obstruction; it does not fill it.  A separate
physical column `dE=t` would give `Delta*Z=t-dG` and close the square only
after inverting `Delta`.

On `Delta=0`, (6) reduces to `dG=t` and leaves `Z` unchanged.  The four
edge-graph equations have a sharp degeneration:

```text
Delta=0 and some old edge is nonzero -> no point in the edge graph;
a=b=c=d=0                           -> edge-graph closure has an A4 fibre.
```

The full normalized boundary-signature move has no finite point in either
case, because it additionally requires `Delta*Delta'=1`.  The `A4` is an
excess fibre of the non-flat edge-graph closure, not a valid renewed square.

Consequently neither the birational move nor its relative Tate closure is a
physical balanced-square saturation theorem.  The shortest positive datum is
a labelled absolute preimage for `t` on `D(Delta)`, plus a separate theorem
on the zero-denominator branch.

Exact checker:
[`verify_h3_balanced_square_urban_renewal_relative_tate_gate.py`](../computations/verify_h3_balanced_square_urban_renewal_relative_tate_gate.py).

## 1. The universal four-terminal identity

Take a cycle on terminals `0,1,2,3` with edge weights

```text
a on 01, b on 12, c on 23, d on 30.
```

For a subset `R` of terminals removed by external matches, let `Sig(R)` be
the perfect-matching sum of the remaining local vertices.  The nonzero
values are

\[
\begin{array}{c|c}
R&\operatorname {Sig}_{\rm old}(R)\\ \hline
\varnothing&ac+bd=\Delta\\
\{2,3\}&a\\
\{0,3\}&b\\
\{0,1\}&c\\
\{1,2\}&d\\
\{0,1,2,3\}&1.
\end{array}                                            \tag{8}
\]

All odd and opposite-pair states vanish.  Substitution of (5) gives the
exact complementary-state identity

\[
             \operatorname {Sig}_{\rm old}(R)
       =\Delta\operatorname {Sig}_{\rm new}(V\setminus R)             \tag{9}
\]

for all sixteen boundary states.  Moreover

\[
                 a'c'+b'd'=\Delta^{-1},                \tag{10}
\]

so applying the move twice returns `(a,b,c,d)`.  The checker verifies (9)
universally in `Q(a,b,c,d)`, by exact polynomial cross multiplication, not
by numerical sampling.

This is the full positive content of urban renewal: it is a birational
equivalence of coefficient presentations relative to four terminals.  It
does not add a terminal vertex cone or a degree-one restriction/insertion
cell.

## 2. Why the balanced augmentation cannot appear

In vertex order

```text
A_[D|Q], A_[Q|D], B, C,
```

the four formal mate columns are

\[
\begin{aligned}
 e_{00}&=(1,0,1,0),& e_{01}&=(1,0,0,1),\\
 e_{10}&=(0,1,1,0),& e_{11}&=(0,1,0,1).                \tag{11}
\end{aligned}
\]

They are signless `K2,2` incidences.  Put

\[
 z=(1,1,-1,-1).                                       \tag{12}
\]

Then `z*e_ij=0` for each edge, the edge rank is three, and adjoining `z`
raises it to four.

Multiplication by the shore sign `diag(1,1,-1,-1)` turns (11) into the
ordinary oriented incidence matrix and turns (12) into

\[
                         (1,1,1,1).                    \tag{13}
\]

The image of an ordinary connected-graph incidence matrix is exactly the
kernel of vertex augmentation.  An urban renewal keeps the same four
terminals and replaces the four cycle-edge weights by opposite-edge rational
weights.  It neither changes this incidence image nor adds a vertex column.
Therefore its gauged augmentation is identically zero.

This is a chain-level obstruction, not a complaint about a particular
formula.  An ordinary square two-cell fills the one-dimensional **cycle** in
the edge module.  It cannot fill the constant **H0** class in the vertex
module.  Any square move constructed solely from old/new edge mapping
cylinders has the same limitation.

There is also a prior physical typing gate.  Each edge in (11) connects a
`DQ` ordered vertex to a `PS` endpoint vertex.  The pinned joint-cobar audit
constructs their formal coefficient shadow but no physical
`DQ <-> PS` chart-switch cell.  Urban renewal assumes these four edges as
input; it cannot manufacture them by mutating their coefficients.

## 3. The localized graph preserves `H0`

The graph of (5) has equations

\[
\begin{aligned}
 \Delta a'-c&=0,&\Delta b'-d&=0,\\
 \Delta c'-a&=0,&\Delta d'-b&=0.                       \tag{14}
\end{aligned}
\]

After inverting `Delta`, these are four monic equations in the four renewed
weights.  Hence

\[
 \mathbf Q[a,b,c,d,a',b',c',d',\Delta^{-1}]/(14)
       \cong \mathbf Q[a,b,c,d,\Delta^{-1}].            \tag{15}
\]

The fixed-point linear shadow has eight degree-zero coordinates, four graph
columns of rank four, and quotient dimension four.  Thus the birational
mapping cylinder preserves the old coefficient `H0` on `D(Delta)`.

That preservation is exactly why it cannot cone (13).  An added column with
nonzero vertex augmentation would reduce the square `H0` dimension from one
to zero; a relative graph equivalence must leave it one.

## 4. The only presentation-safe relative cone

Adjoin one retained carrier `t` and one graph generator `G` with (6).  In
the five coordinates `(A_[D|Q],A_[Q|D],B,C,t)`, the old four edge columns
still have rank three and (6) raises the rank to four.  Therefore

\[
          4-3=5-4=1,                                  \tag{16}
\]

so `H0` is unchanged.

The `Z` component of (6) has gauged augmentation `-4*Delta`.  It is nonzero
on the urban-renewal chart, but (7) shows why that is not a filler.  The
extended dual is

\[
              \widetilde\psi=(z/4,\Delta),             \tag{17}
\]

and it kills every old edge and `t-Delta*Z` while retaining
`psi(Z)=1`.

Now suppose a physical absolute column `dE=t` is supplied.  On
`D(Delta)`,

\[
                         Z=\Delta^{-1}(t-dG)            \tag{18}
\]

is a boundary.  Globally, however, the two columns only make `Delta*Z` a
boundary.  The residual invariant quotient is

\[
                         (R/(\Delta))Z.                 \tag{19}

This is the exact denominator/Tor branch.  Equation (6) is useful as a
relative interface, but writing it down is equivalent to adjoining the
missing cross-grade datum; it is not derived from (9).

## 5. Exact zero-denominator classification

At `Delta=0`, equations (14) become

\[
                         0=(c,d,a,b).                   \tag{20}

Therefore a point of the four-equation **edge-graph closure** exists only if

\[
                         a=b=c=d=0.                     \tag{21}

For example,

\[
                         (a,b,c,d)=(1,1,1,-1)           \tag{22}

has `Delta=0` and no finite lift.  This includes the dense cancellation
branch where both square matchings are nonzero but cancel.

At the origin, all four equations in (14) vanish for every renewed tuple.
The edge-graph closure has an affine-four-space fibre and is not flat or
unique there.

This excess fibre does not satisfy the complete boundary-signature move.
The removed-all state in (9), equivalently (10), imposes

\[
                            \Delta\Delta'=1.            \tag{22a}
\]

No finite `Delta'` satisfies (22a) at `Delta=0`, including at the origin.
Thus the genuine urban-renewal correspondence has no finite point anywhere
on the zero-denominator divisor.  A projective limit may send renewed
weights to infinity, but that is a boundary degeneration, not a finite
source cell.

The relative Tate graph (6) is regular at `Delta=0`, but becomes simply

\[
                              dG=t.                     \tag{23}

Its `Z` component vanishes, its extended dual has `psi(t)=0`, and the
balanced class survives unchanged.  Thus the zero-denominator branch is not
silently closed by the presentation-safe homogenization.

## 6. First PP/reinsertion faces

Even on `D(Delta)`, termwise naturality differentiates the denominator:

\[
 d_{PP}\Delta=(d a)c+a(d c)+(d b)d+b(d d).             \tag{24}

Applying the same derivation to (6) gives

\[
 d_{PP}(dG)=d_{PP}t-(d_{PP}\Delta)Z
                        -\Delta d_{PP}Z.                \tag{25}

The last term contains the already isolated residual-tail and DQ/PS
direction faces on the fixed `H_2345`.  The middle term contains four new
denominator-factor faces.  Equivalently,

\[
 d_{PP}(c/\Delta)
   ={(dc)\Delta-c(d\Delta)\over\Delta^2},               \tag{26}

and similarly for the other three renewed weights.

Thus coefficient mutation does not supply PP-natural cross-grade maps.  It
requires them, and worsens their denominator order.  No `q`, anchor,
target, `W`, ordinary-residue, or ridge face follows from (9) alone.

## 7. Shortest positive datum

The urban-renewal route reduces to a precise two-branch theorem:

```text
Delta != 0:
    construct a physical cross-grade carrier t and an absolute source
    column dE=t, with all PP/reinsertion and augmented faces;

Delta = 0:
    construct an independent filler/terminal theorem, since the finite
    square move is absent and the relative graph has zero Z-component.
```

A physical cell with direct nonzero gauged vertex augmentation would bypass
the denominator entirely and is strictly shorter.  Without it, urban
renewal is only a coefficient reparametrization of the already known
balanced square.

## Verification

Run

```text
python3 computations/verify_h3_balanced_square_urban_renewal_relative_tate_gate.py
python3 -O computations/verify_h3_balanced_square_urban_renewal_relative_tate_gate.py
python3 -I -S computations/verify_h3_balanced_square_urban_renewal_relative_tate_gate.py
```

The checker verifies the universal sixteen-state signature identity, the
involution, full chart/Hasse labels, incidence augmentation, localized graph
rank, the edge-closure/full-signature zero-denominator split, the relative Tate `H0`
rank and forced dual, the localized absolute-saturation fork, and the first
PP product-rule faces.

Frozen ledger digest:

```text
d6eb23ef7b715c02eb933f98f957250c4b2bfdf205bb7bd8362cfa1545ace000
```
