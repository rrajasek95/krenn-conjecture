# The physical terminal component is not tangent-accessible from the GHZ target

## Outcome

Let (A) be the physical eight-site zero-target terminal packet of
`b72402c`.  The complete Jacobian

\[
             dH_8|_A:\mathbb C^{28\cdot9}\longrightarrow
                         (\mathbb C^3)^{\otimes8}
\]

has exact rational rank (131).  Adjoining the ternary GHZ target raises
the rank to (132):

\[
                         \boxed{\Delta_{8,3}\notin\operatorname {im}dH_8|_A.}
\]

The smallest integral left separator is not a large Fredholm functional.
It is evaluation at the pure word (0^8).  Every one of the (252)
Jacobian columns has zero coefficient there, whereas
([0^8]\Delta_{8,3}=1).  Evaluation at (1^8) is a second independent
support separator.  The pure-(2) target direction does lie in the
Jacobian image.

Thus the homogeneous terminal counterguard cannot be translated toward
the GHZ fibre by an ordinary first-order deformation.  This is an exact
anchor-dependent obstruction, not a positive construction of the missing
rootless comparison.  It also explains why an anchor-blind overlap
identity failed: the missing anchors enter this component at higher and
different deformation orders.

## 1. Exact complete Jacobian

For a physical coordinate (E_{xy}^{ab}), the derivative column is the
literal deleted-pair matching tensor

\[
 [w]dH_8|_A(E_{xy}^{ab})
  =\mathbf1_{w_x=a,w_y=b}\,
       H_{[8]\setminus\{x,y\}}(A)(w|_{[8]\setminus\{x,y\}}). \tag{1}
\]

The checker constructs (1) for all (28\cdot9=252) coordinates and all
(3^8=6561) output words.  The sparse matrix has

\[
 \#\operatorname {supp}_{\rm rows}=501,\qquad
 \#\operatorname {supp}_{\rm entries}=999,qquad
 \operatorname {rank}_{\mathbb Q}=131.                 \tag{2}
\]

The augmented ranks for the three individual pure target words are

\[
 \operatorname {rank}(dH_8,e_{0^8})=132,
 \quad
 \operatorname {rank}(dH_8,e_{1^8})=132,
 \quad
 \operatorname {rank}(dH_8,e_{2^8})=131.               \tag{3}
\]

Equations (2)--(3) are computed over exact rationals, not inferred from a
finite-field rank.

## 2. The support reason and nonlinear boundary

On the pure-(0) specialization of (A), the only nonzero base edges are
(01) and (67).  A pure-(0) perfect matching therefore needs at least
two perturbation edges.  On the pure-(1) specialization, only edge (67)
is present, so at least three perturbation edges are needed.  In contrast,
the pure-(2) base has cancelling complete matchings and a nonzero first
derivative.  The first possible anchor orders are consequently

\[
                             (2,3,1).                    \tag{4}
\]

This does not exclude a nonlinear or weighted degeneration from the
terminal component into the GHZ fibre.  It proves only that such a route
cannot be an ordinary tangent lift and cannot yield the desired relative
anchor comparison at first order.  Any positive use of this component must
compare the order-two pure-(0), order-three pure-(1), and order-one
pure-(2) faces in one source-labelled filtered construction.  That is a
strictly stronger datum than the homogeneous two-chart identities frozen
in `b72402c`.

## 3. Proof impact

The result supplies the requested first anchor-dependent Fredholm
obstruction:

* the target-free complete rows and overlap retain (chi=-12);
* the GHZ target is not a tangent value at that packet; and
* the obstruction is already detected before any selector or Macaulay
  quotient, by the two missing pure-word rows.

Therefore the physical separator cannot itself be promoted to a nearby
rootless countermodel.  Conversely, it does not construct the missing
source-valid annihilator.  The remaining positive theorem must be proved
on the nonzero-anchor fibre itself, or through a genuinely weighted
higher-order degeneration which synchronizes the onset orders (4).

Run

```text
python3 computations/verify_h3_two_chart_terminal_anchor_jacobian_obstruction.py
python3 -O computations/verify_h3_two_chart_terminal_anchor_jacobian_obstruction.py
python3 -I -S computations/verify_h3_two_chart_terminal_anchor_jacobian_obstruction.py
```

The checker imports the committed physical packet by pinned digest and
uses exact sparse Gaussian elimination over (mathbb Q).
