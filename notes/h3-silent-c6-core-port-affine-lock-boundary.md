# Core-port completion of the silent C6 reduces to one Hall/Fitting lock

## Result

Continue after the fixed-port closure `b4d8568`. Allow arbitrary endpoint
components on the four core residual ports `0,1,3,4`, while retaining the
already reduced branch:

```text
PS=q04=q13=0,
no outside endpoint term,
no nonanchor offdiagonal q mate.
```

The complete core-port expansion of each of the nine private coefficients
from `b4d8568` has exactly two terms:

1. its fixed endpoint orientation; and
2. the endpoint-swapped orientation on the **identical** nonzero $q$ tail.

There are no further core-port terms **in these selected private fine
coefficients**. At a synchronized minimum-support representative, the exact
split for the endpoint pairs appearing there is

\[
\boxed{\text{proportional complete column: absorb to fixed ports}}
\quad\text{or}\quad
\boxed{\text{nonproportional two-port Hall/Fitting lock}.}       \tag{1}
\]

The second box has two explicit orbits:

```text
6 records: reciprocal orientation on core hole 04 (K2,2 lock),
3 records: diagonal orientation on core hole 01 (bright reselection).
```

The first is the smallest surviving core-port affine lock. Its common-tail
cofactor matrix is

\[
K_T=\begin{pmatrix}0&T\\T&0\end{pmatrix},
\qquad \det K_T=-T^2\ne0.                               \tag{2}
\]

Both endpoint complete-column pairs are nonproportional, so the committed
common-covector theorem supplies a source-valid Fitting quotient. What is
not automatic is deleted-star rank three: (2) lands exactly in the existing
affine/Hall accessibility interface, rather than directly in the fixed-port
unit.

Checker:
`computations/verify_h3_silent_c6_core_port_affine_lock_boundary.py`.

## Exact two-term expansion

For the first two $X_1$ bright tails, the private rows are

```text
A1=23|45: G12[101120], common tail 15:00|23:11,
A2=24|35: G12[100121], common tail 12:00|35:11.
```

After all prior routes, their complete core-port coefficient is

\[
T\bigl(p_{1,0}^{11}s_{2,4}^{22}
       +p_{1,4}^{12}s_{2,0}^{21}\bigr)=0.               \tag{3}
\]

The fixed product is nonzero and $T\ne0$, so both reciprocal extra cells in
the second product are nonzero. The two physical endpoint orientations use
the same hole `04`; the same-site corners `00` and `44` vanish. This gives
(2) and the localized permanent-null relation

\[
p_{1,0}^{11}s_{2,4}^{22}
 +p_{1,4}^{12}s_{2,0}^{21}=0.                           \tag{4}
\]

For the third $X_1$ tail,

```text
A3=25|34: G11[110110], common tail 25:00|34:11,
```

and the only two core terms are

\[
T\bigl(p_{1,0}^{11}s_{1,1}^{11}
       +p_{1,1}^{11}s_{1,0}^{11}\bigr)=0.               \tag{5}
\]

Again the fixed product and $T$ are nonzero. Equations (3) and (5) are
literal coefficients of the full response rows with the selected unary and
bright tails retained; they are not formal cofactor variables.

The checker enumerates all 105 augmented perfect matchings for each of the
nine bright-tail pairs. Restricting endpoint ports to the four core sites
and retaining every allowed decorated $q$ cell gives exactly the two terms
above in every record.

## Complete-column reduction

Fix $q$ and the opposite endpoint rows. Two components of one $p_i$ row
define complete columns

\[
L_s(z)=\bigl(zs_1q^{[2]},zs_2q^{[2]}\bigr),             \tag{6}
\]

and similarly on the $s$ side. If an extra column is proportional to a
selected one, the exact one-sided update from `1a2713d` deletes the extra
component and preserves every response tensor. Both cells share the same
coordinate endpoint, so neither is a mutual anchor; the update is
$\nu$-safe even if it also cancels the selected coefficient. Minimum support
therefore excludes proportionality.

In the remaining branch both endpoint pairs in (4), or in (5), are
nonproportional. Their determinant maps are two nonzero functionals on the
common output dual. By the committed characteristic-zero selection theorem,
one of $e_P+c e_S$, $c=0,1,2$, detects both minors. Hence the core lock has a
source-valid common Fitting covector; no literal-word synchronization is
missing.

This does **not** promote the Fitting class to a good active pair. The
missing datum is precisely rank/line accessibility through the selected
Hall graph.

## The diagonal orbit reselects the bright hole

Equation (5) is the endpoint factor multiplying every pure-$1$ matching in
the selected response hole `01`. Therefore its contribution to the pure
$X_1$ target is

\[
\bigl(p_{1,0}^{11}s_{1,1}^{11}
      +p_{1,1}^{11}s_{1,0}^{11}\bigr)H_{01}^{1111}=0.  \tag{7}
\]

Since the complete diagonal response equals $X_1$, another ordered endpoint
hole must contribute nontrivially. On the four core sites the possible
physical holes other than `01` are

```text
03, 04, 13, 14, 34.
```

Every one meets the selected $X_2$ hole `34`. Thus the replacement bright
term is automatically in the star/triangle/$K_{2,2}$ Hall normal form. If
it leaves the core sites, the already committed outside-component theorem
gives exact deletion or a free active carrier instead.

## Consequence and scope

Combining the exact branches gives the strongest current reduction:

1. proportional full columns absorb to the fixed-port packet and `b4d8568`
   closes it;
2. the diagonal swapped orientation forces a Hall-colliding bright
   reselection;
3. the reciprocal swapped orientation is the nondegenerate hole-`04`
   permanent-null/Fitting carrier (2).

Thus the first unavoidable core-port packet is one nonproportional
reciprocal two-port lock trapped in the four-core-site Hall graph. The
remaining implication is exactly the global
affine/Hall accessibility theorem: turn its common Fitting carrier into
deleted-star rank three, an anchor-preserving relation, or an already-closed
Hall branch.

This note does not claim that every triangle/$K_{2,2}$ Hall accessibility
case is globally closed. Nor does it prove that surplus nonproportional
endpoint columns absent from the selected private word are deletable; those
columns may enlarge the same Hall/Fitting module. It identifies the first
forced landing and does not reopen support enumeration.

## Verification

```text
python3 computations/verify_h3_silent_c6_core_port_affine_lock_boundary.py
python3 -O computations/verify_h3_silent_c6_core_port_affine_lock_boundary.py
python3 -I -S computations/verify_h3_silent_c6_core_port_affine_lock_boundary.py
```

Frozen ledger SHA-256:

```text
6936556a3c9ec116a8250954d0b9afff3749cf99ec223ac8046d22c7adbef6fa
```
