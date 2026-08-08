# N=8 P5 strict-transform prefix

## Result

The exact checker
`computations/verify_n8_p5_strict_transform_prefix.py` follows the 39
normal-eliminated mixed equations at a deterministic rational point of the
exceptional Ferrers branch P5.  With the 45 coordinates tangent to P5 held
fixed, the eleven transverse coordinates solve uniquely through original
mixed degree five.  At degree six the canonical section has a nonzero
compatibility, one order before the degree-seven eight-term H0 class.

This does **not** yet prove that P5 is killed.  A genuine lifted arc may bend
in the 45 free P5 coordinates.  What is certified is the maximal constant-free
section prefix and the first exact place where those bends must be included.

## Exact setup and ledger

Write the 39 normal-eliminated equations as

\[
 Q_i(z)=Q_i^{(2)}(z)+Q_i^{(3)}(z)+\cdots
\]

and put $z=t(v_0+t v_1+t^2v_2+\cdots)$.  After dividing by $t^2$,
strict-transform order $r$ uses the original homogeneous pieces through
degree $r+2$.  The checker uses

\[
 (v_0)_j=j+2,
 \quad z_{12}=z_{13}=z_{14}=z_{17}=\cdots=z_{23}=0,
 \quad z_{15}=z_{16}.
\]

The P5 normal variables are

\[
 z_{12},z_{13},z_{14},z_{15},z_{17},z_{18},z_{19},z_{20},z_{21},z_{22},z_{23}.
\]

At $v_0$, the 39-by-11 quadratic Jacobian has exact rank 11.  A frozen
independent row set is equations

\[
 1,4,7,12,14,15,23,25,26,27,39.
\]

The retained exact tangent pieces have total term counts

| original degree | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|
| terms in 39 equations | 68 | 535 | 2239 | 7749 |

Solving the pivot equations gives zero compatibility at strict orders 1, 2,
and 3, hence through original mixed degrees 3, 4, and 5.  The checker records
all eleven rational transverse corrections at each order.

Constructing all degree-six tangent polynomials directly exceeded the local
memory budget (the exploratory run passed roughly 3.7 GB before it was
stopped).  Only their values at $v_0$ are needed at strict order 4.  The
checker evaluates those values directly from the factorized ambient
corrections.  This terminal evaluation is exact because every eliminated
linear normal form vanishes on the ambient tangent vector.

After the order-4 pivot solve, only equations 30 and 33 retain compatibility:

\[
 C_{30}(v_0)=170841150,
 \qquad C_{33}(v_0)=-41001876.
\]

Thus the canonical section does not extend through original degree six.

The eight-term H0 initial class is

\[
 R=z_{16}^2z_{41}(z_{44}+z_{45})(z_{53}-z_{51})
   (z_9z_{25}-z_{11}z_{46}),
\]

and $R(v_0)=-847372104\ne0$.  This confirms that the chosen point is in the
generic H0-surviving part of P5, but it does not put that point on a genuine
mixed lift.

The frozen checker ledger has SHA-256
`afd0341d0704ddcd45c578859851b415c147660e7dc7a31cdce9a8fa3f40c99c`.

## Precise next calculation

The next object is the symbolic degree-six compatibility ideal on P5, with
free-coordinate bends retained.  A memory-bounded implementation should:

1. represent each $Q_i^{(6)}|_{P5}$ as a stream of products of separately
   P5-restricted multiplier and equation factors;
2. solve strict orders 1--3 over the P5 coordinate ring, keeping the 45 free
   coefficients, and project order 4 modulo the eleven pivot rows;
3. reduce $R$ modulo the resulting compatibility ideal (and its relevant
   saturated/radical components).

If every surviving degree-six component forces $R=0$, the apparent H0
escape is killed before it can lift.  If an exact point has compatibility
zero, $R\ne0$, and the same rank-11 pivot, then the next step is original
degree seven.  That step additionally needs the degree-six normal quotients
or, more economically, their values and first directional contractions along
the selected P5 bend.  Those data are the smallest artifact not produced by
the present terminal evaluator.
