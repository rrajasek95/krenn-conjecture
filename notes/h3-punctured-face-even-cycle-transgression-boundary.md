# Punctured faces need a single surviving transgression

## Result

The target-augmented punctured-face certificate from `5a01b0a` has a
uniform algebraic extension to any two matching bases.  It does **not**
generically force the distance-three chord which shortens a `C6` or `C8`.
The failure is already exact on the canonical `C6`: the shortening base has
four signed face terms, not the single pure-target term isolated in the
target-coloop `C4`.

This leaves a sharp source theorem rather than another cycle census:

> In the complete unary/four-response packet, select a first nonzero
> punctured-face transgression.  Every competing term must either route, or
> the selected transgression must have only its pure-target face.  Then its
> matching base is forced and joins/shortens the flat base components.

Checker:
`computations/verify_h3_punctured_face_even_cycle_transgression_boundary.py`.

## 1. Universal punctured functional

Let `M,N` be two matching products and vary sites `0,2` on the face

```text
t=(1,1,1,...), x=(0,1,1,...),
y=(1,1,2,1,...), z=(0,1,2,1,...).
```

For any third matching base `Q`, put

\[
D_Q=M_zQ_t-M_yQ_x+N_xQ_y-N_tQ_z.                    \tag{1}
\]

The two rank-one products have zero face determinant, hence

\[
                         D_M+D_N=0.                  \tag{2}
\]

If the complete response row is `H=sum_Q Q`, applying the same literal
row combination used in `5a01b0a` gives, modulo its four response rows,

\[
 U\sum_{Q\ne M,N}D_Q=a_2M_z.                         \tag{3}

Here `U` is the selected endpoint product and the right side is the target
constant at `t`.  Thus the algebra is fully source-labelled once the four
words share one endpoint-response block.

## 2. Exact sufficient theorem

Equation (3) forces a matching base `K` under four precise hypotheses:

1. all four words use one common endpoint-response block;
2. selected bridge words make `M_z` and the needed face pivots units;
3. every `D_Q` except `D_K` vanishes or is already routed; and
4. the mixed faces of `K` vanish or route, so

   \[
                              D_K=V K_t              \tag{4}
   \]

   with `V` a unit.

Then (3) forces `K_t` nonzero.  If `M triangle K` is one `C4`, this gives a
typed base-graph edge.  For the standard shortening base it gives the chord
which replaces `C_(2r)` by `C4+C_(2r-2)`.

This is exactly why `5a01b0a` succeeds: every mixed face of its third
matching `04|15` is an off-anchor off-diagonal exit, leaving only `G_t`.

## 3. Canonical C6 obstruction

Take

```text
M=01|23|45,        N=05|12|34,
K=03|12|45.
```

The base `K` is the desired shortening: `M triangle K=C4`, while
`K triangle N=C4`.  Nevertheless its exact transgression is

\[
\begin{aligned}
D_K={}&q_{01}^{01}q_{03}^{11}q_{12}^{11}q_{23}^{21}
       (q_{45}^{11})^2\\
 &-q_{01}^{11}q_{03}^{01}q_{12}^{11}q_{23}^{21}
       (q_{45}^{11})^2\\
 &-q_{03}^{01}q_{05}^{11}q_{12}^{11}q_{12}^{12}
       q_{34}^{11}q_{45}^{11}\\
 &+q_{03}^{11}q_{05}^{01}q_{12}^{11}q_{12}^{12}
       q_{34}^{11}q_{45}^{11}.                       \tag{5}
\end{aligned}
\]

The first summand contains the pure target monomial `K_t`; the other three
are mixed faces.  They are distinct source monomials.  Setting every
displayed variable to one gives the signed cancellation

```text
D_K=0,             K_t=1.
```

Hence the punctured identity alone cannot force the chord.  It must first
route or kill the extra mixed face.  This counterguard is local coefficient
algebra, not a full one-bad source.

Among the thirteen third perfect matchings on the six cycle vertices, the
punctured transgressions have term histogram

```text
2 terms: 4,       4 terms: 9.
```

Four third bases differ by a `C6` from both `M` and `N`, so even a forced
base need not immediately create a typed `C4` edge.

## 4. C8 is strictly less selective

For `C8`, the 103 third matching bases split as

```text
2-term transgression: 28,
4-term transgression: 75.
```

Seventy-nine have no single-`C4` side to either input matching.  The
standard shortening base `03|12|45|67` again has four transgression terms;
the three mixed-face obstructions acquire the appropriate unchanged tails.
Thus a longer cycle does not repair the failure found at `C6`.

## Consequence

The next bounded proof target is not another Hilbert/support enumeration.
It is a **first-transgression selection theorem**: use the other diagonal,
crossed, and unary coefficients to make every mixed face of one shortening
base routed or zero, and eliminate the competing `D_Q`.  Once that input is
available, (3)--(4) give the chord and the connected flat-base theorem
finishes the coefficient propagation.

## Scope

This note proves the universal source-row functional, the exact sufficient
hypotheses, and the complete `C6/C8` boundary.  It does not construct a full
source packet realizing the cancellation guard, and it does not refute a
stronger selection theorem using all five tensors.

Run

```text
python3 computations/verify_h3_punctured_face_even_cycle_transgression_boundary.py
python3 -O computations/verify_h3_punctured_face_even_cycle_transgression_boundary.py
python3 -I -S computations/verify_h3_punctured_face_even_cycle_transgression_boundary.py
```

Frozen ledger SHA-256:

```text
ca97e92948392f236fbf99f699f2210e5b94287b3a59f34968033bd755de3370
```
