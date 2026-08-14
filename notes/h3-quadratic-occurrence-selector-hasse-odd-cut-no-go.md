# The quadratic occurrence selector first fails on an odd lower cut

## Outcome

The coefficient identity

\[
 Q_{(0,1)}X_{23}=Q_{(0,1)}X_{45}=e_f,
 \qquad f=P0\mid S1\mid23\mid45,                     \tag{1}
\]

does not lift through the currently implemented physical
restriction/reinsertion/Hasse operations.  The first finite obstruction is
already present on either marked residual-edge cut.  Restricting the
centered pointed class

\[
                         c_f=90e_f-\mathbf1_{90}       \tag{2}
\]

along `23` or `45` has the forced endpoint-role-odd component

\[
                    45(e_{\bar f}-e_{\tau\bar f}).     \tag{3}
\]

Every current complete lower row and residual-`q` selector is
endpoint-role even.  Site/root Cartan commutes with endpoint-role
transposition, and the available constant theta transport has zero boundary
on (3).  Granting the entire endpoint-even lower space, not merely the named
rows, leaves an integral dual which reads `90` on the required restriction.

The two cuts are distinct labelled instances of one missing lower generator
type.  Even after granting both missing odd fillers, the independent
selected-`db01` flag obstruction remains: the old rank `181 -> 182` becomes
`183 -> 184` after adding the two direct-sum fillers.

Thus the quadratic feature formula shortens the coefficient selector, but
not the physical source packet.  A positive construction requires a new
two-stage nonlinear Hasse family: one lower odd occurrence cell type on both
cuts and one top pointed cell carrying the selected `db01` and every
augmented face.

Exact checker:
[`verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py`](../computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py).

## 1. Why the quadratic formula retains four physical faces

On the 90 direct-free occurrences, the supports are

```text
Q_(0,1)       3
X_23         12
X_45         12
Q_(0,1)X_23   1.
```

Inside the endpoint fibre `(0,1)`, either tail edge forces its complementary
edge, which proves (1).  The selected physical top is nevertheless the
four-factor squarefree monomial

```text
P0^11 | S1^11 | q23^00 | q45^00
```

in response word `11110000 = 11:110000`.  Its first source faces remain

```text
d(P0):  S1|23|45       d(S1):  P0|23|45
d(q23): P0|S1|45       d(q45): P0|S1|23.
```

Choosing `X_23` rather than `X_45` in (1) cannot erase the `d(q45)` face.
It only forgets that label after coefficient evaluation.  A physical
principal-parts differential differentiates every factor of the selected
top.

## 2. Exact odd component on either marked cut

Delete one of the marked residual edges.  The lower occurrence module has
12 elements.  If `bar f` is the marked lower occurrence and `tau` exchanges
the endpoint roles, then

\[
 c_{\bar f}=12e_{\bar f}-\mathbf1_{12}
 =\bigl[6(e_{\bar f}+e_{\tau\bar f})-\mathbf1_{12}\bigr]
  +6(e_{\bar f}-e_{\tau\bar f}).                      \tag{4}
\]

The exact restriction/insertion formula at order three is

\[
 D_e c_f={15\over2}c_{\bar f}+{13\over2}\mathbf1_{12}.\tag{5}
\]

Combining (4) and (5) gives

\[
 D_e c_f=
 {15\over2}\bigl[6(e_{\bar f}+e_{\tau\bar f})-
                         \mathbf1_{12}\bigr]
 +45(e_{\bar f}-e_{\tau\bar f})
 +{13\over2}\mathbf1_{12}.                           \tag{6}
\]

For the two labelled cuts this is

```text
delete q23:  P0|S1|45  versus  P1|S0|45,
delete q45:  P0|S1|23  versus  P1|S0|23.
```

Let

\[
                    \omega=e_{\bar f}^*-e_{\tau\bar f}^*.\tag{7}
\]

It kills the entire six-dimensional endpoint-even subspace of the lower
12-space and reads

\[
                         \omega(D_e c_f)=90.           \tag{8}
\]

This is stronger than testing the presently named lower rows.  The checker
grants every possible endpoint-even lower column.  Their rank is six; adding
the required restriction raises it to seven.  On both cut blocks the ranks
are

```text
all endpoint-even rows          12
one signed combined top face    13    (for either relative sign)
both labelled odd faces         14.
```

The odd class is a coefficient obstruction, not yet a physical terminal.
To prevent external bookkeeping from being mistaken for a repair, the
countermodel also grants arbitrary unit columns on

```text
target, private B, reduced Eq, M, ainc, q, W, P_f,
labelled ordinary residue, ridge, eta, sigma.
```

The rank still rises `24 -> 25` on either cut, and (7), extended by zero,
kills all those grants.  Therefore no choice of protected readout values can
replace the missing lower occurrence component.

## 3. The selected `db01` obstruction is independent

The matching projection of the pointed top obeys

\[
                 (A+I)c_f=3c_{01},
 \qquad c_{01}=30b_{01}-R.                            \tag{9}
\]

Its first selected principal-parts projection is the six-term `db01` packet.
The existing full-label guard has 180 response flags, 180 carrier flags, all
180 monic termwise reinsertion graphs, and both complete rows.  Its boundary
rank is `181`; adjoining selected `db01` raises it to `182`.

Now grant two completely free lower odd fillers in new direct-sum
coordinates.  The old rank becomes `183`, while selected `db01` still raises
it to `184`.  The centered flag dual

```text
29 on the selected six flags in both blocks,
-1 on every other flag in both blocks
```

kills every old column and both odd fillers and reads `174` on `db01`.
Consequently (3) is the first restriction obstruction, but filling it does
not automatically construct the top pointed/endpoint-fibre carrier.

## 4. Smallest positive source packet

A successful lift needs two generator types.

1. One source-valid endpoint-role-odd order-two occurrence cell
   `W_odd`, instantiated on `q23` and `q45`.  The top-word stabilizer
   `(2 5)(3 4)` relates the instances, but does not identify their labelled
   boundary slots.
2. One top quadratic pointed Hasse cell whose coefficient shadow is (1).
   Its boundary must contain the scalar/target correction `-90 f(x)`, the
   two endpoint faces, both labelled tail faces, and the selected six-term
   `db01` projection after matching spread.

Both types must retain word `11110000`, the occurrence and removed-edge
fine labels, and their reinsertion parents.  The top totalization must also
carry physical target, private/reduced-`Eq`, `M`, `ainc/q`, `W`, pointed
`P_f`, labelled residue, ridge, eta, and sigma readouts.  None of those
requirements is supplied by the pointwise identity (1).

This is a sharp no-go for composition of the named current operations, not
a nonexistence theorem for the displayed new two-stage packet in a larger
physical resolution.

## Reproduction

```bash
python3 computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py --mode all
python3 computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py --mode selector
python3 computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py --mode odd
python3 computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py --mode flags
python3 -O computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py --mode all
python3 -I -S computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py --mode all
```

Frozen ledger:

```text
99a3365c86b8e421a80503209a664ef1857af86c6ded183d399a93e2ada535ed
```
