# A surviving pointed tangent first meets the second Hasse obstruction

## Verdict

Let `A` be the evaluated full `h=3` endpoint-plus-simultaneous-`q`
Jacobian on its literal `171` columns.  On the physical affine chart,
`H=P_f`.  Therefore

\[
                H\notin\operatorname{row}(A)
\]

gives, by exact Fredholm duality, a tangent

\[
             \xi\in\ker A,\qquad H(\xi)=1.           \tag{1}
\]

That is the entire unconditional consequence.  It gives neither an
anchor-safe support deletion nor a physical Macaulay terminal.

The first genuinely new source datum is

\[
        \boxed{\mathfrak o_2(\xi)=
        [F_{[2],x}(\xi)]\in\operatorname{coker}(A)}.  \tag{2}
\]

If (2) vanishes, choose a second jet and continue the formal-arc equations.
If it is nonzero, a local physical output covector detects it.  That
covector becomes the accepted Fredholm/Macaulay terminal only after a
separate augmented extension test.

Checker:

```text
computations/verify_h3_occurrence_kernel_integrability_terminal_gate.py
```

Frozen ledger SHA-256:

```text
9251bc70062d6362cdcaa247013d694747e17b9c0ab205b8e1b7213911c3bf5a
```

## What the localized coloop packet already gives

The alpha-localized `U`-bright and `V`-bright coloop charts have the exact
quotient

\[
                 k[\alpha^{\pm1},d,C,f]
\]

and the algebraic action

\[
                    f\longmapsto f+t,
             \qquad g\longmapsto g-t.              \tag{3}
\]

Thus the occurrence redistribution is not merely a tangent on the local
aggregate packet: it integrates there, and its transverse Fitting minor is
exactly `r_g-r_f`.  In particular, the aggregate coloop equations themselves
do not obstruct isolation.

The missing step is narrower and genuinely source-level.  One must lift (3)
through every complete physical source equation represented by the full
`171`-column Jacobian and retain the protected anchors at `t=-f`.  The first
nonlinear obstruction to that lift is precisely (2).  If the all-order lift
and anchor clause hold, `t=-f` deletes the marked occurrence.  Neither follows
from the localized chart alone.

## Why minimum support does not delete anything

The exact fibre

\[
                              xy=1                  \tag{4}
\]

is the sharp source-level guard.  Every point has both scalar coordinates
nonzero, so occupied support `2` is minimum.  At `(1,1)`, with marked
function `f=x`,

\[
 d(xy-1)=(1,1),\qquad \xi=(1,-1),\qquad df(\xi)=1.   \tag{5}
\]

Moreover the tangent integrates to the exact formal curve

\[
                  x=1+t,\qquad y=(1+t)^{-1}.         \tag{6}
\]

Both coordinates remain units in `k[[t]]`, so support remains exactly two.
Thus even an integrable, marked-occurrence-changing tangent at a
minimum-support point need not approach a support boundary.

For a deletion argument one needs stronger physical typing: an exact
kernel line on already occupied scalar columns, usually in one fixed
endpoint row, together with proof that its boundary specialization
preserves the protected anchors.  This is precisely why the committed
same-row kernel theorem works and an arbitrary `171`-column tangent does
not.

## The first nonlinear integrability equation

For a formal source arc written in divided-power/Hasse coordinates,

\[
             x(t)=x+t\xi+t^2\xi_2+\cdots,
\]

the first two equations are

\[
          A\xi=0,
       \qquad A\xi_2=-F_{[2],x}(\xi).                \tag{7}
\]

Hence (2) is exactly the obstruction to a second-order lift.  The checker
freezes two local source germs with identical `A=0`, identical `H=1`, and
identical tangent `xi=1`:

```text
smooth germ:       no equation in z; xi integrates,
doubled germ:      (z-1)^2=0; F_[2](xi)=1 and xi does not lift.
```

So the complete first-order packet cannot decide integrability.

There is a useful stronger criterion for a literal straight line.  Every
`h=3` unary or fixed-right response coefficient has moving degree at most
three.  Therefore

\[
 F(x+t\xi)=F(x)
\]

holds identically precisely when

\[
 A\xi=0,\qquad F_{[2]}(\xi)=0,
                  \qquad F_{[3]}(\xi)=0.             \tag{8}

The scalar restriction `t^2+t^3` is the minimal warning: its first
coefficient is zero, but it is not an exact source line.

Even (7) is not by itself a lexicographic support deletion.  One still
needs an occupied scalar coordinate that reaches zero and an anchor-safe
specialization.

## The exact second-order fork

If the right side of (6) lies in `im(A)`, select `xi_2` and pass to the next
arc equation.  This does not yet produce a boundary point or reduce
support.

If it does not lie in `im(A)`, finite-dimensional duality gives

\[
              \psi A=0,
       \qquad \psi(F_{[2]}(\xi))\ne0.                \tag{9}

This is an honest covector on the physical output equations used to define
`A`.  It is not automatically the final Macaulay terminal, because the
accepted terminal lives on a larger augmented codomain retaining the
word/fine/repeated, target, residue, anchor, `q`, `W`, and eta/sigma rows.

## The terminal-extension equation

Let `i:Y_loc -> Y_aug` include the local output grade and let `J_aug` be the
complete augmented source map.  Extending (8) means finding

\[
 i^*\widetilde\psi=\psi,
 \qquad J_{aug}^*\widetilde\psi=0,                  \tag{10}
\]

with the normalized physical terminal value.  The annihilation part of
(9) is solvable exactly when

\[
       \psi\bigl(i(Y_{loc})\cap\operatorname{im}J_{aug}\bigr)=0. \tag{11}
\]

The smallest guard uses local basis `e1,e2` and `psi=e2^*`.

```text
good augmented image:  <e1, e2+T>
good extension:        psi_tilde=e2^*-T^*

bad augmented image:   <e1, e2+T, T>
bad intersection:      e2=(e2+T)-T
```

Both packets have the same local `A` and `psi`; only the second blocks the
extension.  Therefore the local Hessian dual cannot be called a physical
terminal before (11), terminal normalization, and the six-term/`W`
identification are proved.  Failure of (10) is an augmented relative class,
not already a contradiction.

## Shortest source-level theorem

At the selected pointed occurrence, the exact branch is:

```text
H=P_f survives modulo row(A)
        |
        v
xi in ker(A), H(xi)=1
        |
        +-- o2=0 in coker(A)
        |       -> choose xi2 and continue all arc equations
        |       -> deletion only after an anchor-safe boundary theorem
        |
        `-- o2!=0
                -> local output covector psi
                -> physical terminal only after augmented extension (9).
```

Thus the highest-leverage next calculation is the literal class (2) in the
selected word/fine/repeated grade and its augmented Spencer image.  It is
the first place where the full source equations can force either a genuine
lift or a source-provenant obstruction.

## Scope

The Hasse equations and extension criterion are exact.  The torus, doubled
germ, and three-dimensional terminal packets are sharp logical guards, not
complete GHZ source points.  This result neither constructs an all-order
source arc nor promotes the local output dual to the final physical
terminal.
