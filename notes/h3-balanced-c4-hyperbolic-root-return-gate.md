# The balanced `C4` charge is an opposite-root return

## Outcome

The two profile-changing families now known to be necessary and sufficient
for Gate II have a single exact algebraic construction.  Put

\[
 x=(D,p_0,p_1),\qquad y=(q_{01},s_1,s_0),\qquad
 A_i=x_i y_iH_{2345}.
\]

On the hyperbolic response

\[
                 S=(x_0y_0+x_1y_1+x_2y_2)H_{2345}
\]

let

\[
 E_{ij}=x_i\partial_{x_j}-y_j\partial_{y_i}.
\]

Every `E_ij` annihilates `S` identically.  More importantly,

\[
 E_{10}E_{01}(A_0)=A_0-A_1,\qquad
 E_{20}E_{02}(A_0)=A_0-A_2,
\]

and therefore

\[
 E_{10}E_{01}(A_0)+E_{20}E_{02}(A_0)
       =(2Dq_{01}-p_0s_1-p_1s_0)H_{2345}.             \tag{1}
\]

Thus the balanced Gate-II class is not an arbitrary extra chart vector.  It
is the sum of two opposite-root returns in the natural hyperbolic `GL3`
action on the three operation slots.  The construction is division-free and
has coefficient one.

This hyperbolic action has a literal local matching origin.  In the ordered
four-terminal basis `(P,S,0,1)`, put the following entries in a skew matrix:

```text
PS=D,  P0=p0,  P1=p1,  S0=s0,  S1=-s1,  01=q01.
```

Then

\[
 \operatorname {Pf}=Dq_{01}-p_0(-s_1)+p_1s_0
                    =Dq_{01}+p_0s_1+p_1s_0.           \tag{2}
\]

The elementary root flow is the determinant-one congruence on the three
non-`P` terminals; in the Hodge-dual coordinates `(x,y)` it is

\[
 x_j\mapsto x_j+t x_i,\qquad y_i\mapsto y_i-t y_j.    \tag{3}
\]

It preserves (2) for every `t`.  Therefore the root-return mechanism is a
genuine local `K4` Pfaffian symmetry, not a guessed linear projector.  Its
failure to be a completed physical source map begins only when the selected
`K4` is reinserted into the full unsigned hafnian response and all other
incident matchings are restored.

Exact checker:
[`verify_h3_balanced_c4_hyperbolic_root_return_gate.py`](../computations/verify_h3_balanced_c4_hyperbolic_root_return_gate.py).

## The first proper faces

The first half of each root return is

\[
 E_{01}(A_0)=-D s_1H_{2345},\qquad
 E_{02}(A_0)=-D s_0H_{2345}.                           \tag{4}
\]

Reversing the root order instead passes through

\[
 p_0q_{01}H_{2345},\qquad p_1q_{01}H_{2345}.          \tag{5}
\]

These are precisely collision profiles: one augmented operation vertex is
missing and another is doubled.  The six oriented collision monomials
`x_i*y_j*H`, `i!=j`, are linearly independent from the three squarefree
chart monomials `x_i*y_i*H`.  Hence (1) does not rename an old chart column
or hide the balanced class in a Cartan action.  Diagonal hyperbolic
generators fix every `A_i` separately.

The two opposite-root orders agree after the second step.  Their difference
is the diagonal commutator, which acts trivially on the three `A_i`.  This is
the exact flatness required of a two-stage root-return square.

## Relation to the current frontier

The independent augmented-rank and recurrent-core audits show that the two
families

```text
DQ <-> P0S1,
DQ <-> P1S0
```

are jointly necessary and sufficient: either one alone leaves the balanced
dual, while both fill it.  Formula (1) constructs exactly their coefficient
tops from a common mechanism.  It therefore replaces the search for an
arbitrary four-coordinate column by the narrower problem of constructing
two collision Tate/root squares.

This does **not** yet give a physical source attachment.  The coordinates
`D,p0,p1` and `q01,s1,s0` have different operation, word, fine and repeated
grades.  A formal hyperbolic root mixes those roles.  Its collision faces
(4)--(5) are outside the existing squarefree response presentation, exactly
as the augmented-vertex unipotent-shear audit predicts.

A physical realization must therefore supply a chain map from both
root-return squares into the complete source complex, retaining:

1. the missing/doubled collision sectors;
2. their `C2+`, `C4` and `P2` principal-parts faces;
3. restriction and reinsertion labels;
4. target, Eq, physical `q`, anchor, `W`, ordinary residue and shifted ridge.

If those collision families land, (1) gives the balanced filler without any
additional scalar projector or localization.  If their exhaustive physical
map has no preimage, the already constructed balanced dual is the terminal
alternative.

## Verification

Run

```text
python3 computations/verify_h3_balanced_c4_hyperbolic_root_return_gate.py
python3 -O computations/verify_h3_balanced_c4_hyperbolic_root_return_gate.py
python3 -I -S computations/verify_h3_balanced_c4_hyperbolic_root_return_gate.py
```

The checker verifies the six infinitesimal symmetries, both orders of both
root returns, the exact sum (1), independence of all collision sectors, and
the failure of every diagonal hyperbolic action to produce the charge.

Frozen ledger digest:

```text
3419e7e4657384384ab3388f48dbc2c4119720c98fdf33ff7a12cf0232315219
```
