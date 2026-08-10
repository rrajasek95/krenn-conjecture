# The 24-cell Segre leading face is response-empty

## Exact result

Take the fixed fourteen-cell Segre--(K_4) quadratic (H), make all
twenty-four mixed cells in the off-`01` anchor zero class mandatory and
nonzero,

```text
02:02 02:10 02:12 02:20  03:01 03:10 03:20 03:21
04:02 04:10 04:12 04:20  05:01 05:10 05:20 05:21
12:02 13:01 14:02 15:01  23:21 25:21 34:12 45:21,
```

and allow arbitrary support and coefficients on all forty-five diagonal
`00`, `11`, `22` cells and all twenty-four endpoint-star coordinates of
(p_1,p_2,s_1,s_2).  There is no complex point satisfying

\[
 q^{[3]}=X_0,qquad
 p_i s_j q^{[2]}=\delta_{ij}X_i\quad(i,j\in\{1,2\}).
\]

The checker
`computations/verify_n8_one_bad_segre_24cell_response_shadow_unit.py`
proves this by an exact support shadow, ordinary polynomial circuit clauses,
and an independently replayed deletion-free RUP certificate.

## Universal two-row factors

On the maximal allowed face, each diagonal response has a literal two-term
mixed row for every unordered pair of star sites (r<s).  Each has the
form

\[
              g_{rs}=Q_{rs}(p_r s_s+p_s s_r),          \tag{1}
\]

where (Q_{rs}) is one supported two-edge (q)-matching monomial.  The
checker reconstructs the complete source expansion before accepting (1);
there are at least three such rows for each of the fifteen site pairs in
each diagonal response.

For example, three actual (p_1s_1) rows are

\[
\begin{aligned}
g_{200112}&=x_{05}^{22}x_{12}^{00}
 (p_{1,3}s_{1,4}+p_{1,4}s_{1,3}),\\
g_{201012}&=x_{05}^{22}x_{13}^{00}
 (p_{1,2}s_{1,4}+p_{1,4}s_{1,2}),\\
g_{201102}&=x_{05}^{22}x_{14}^{00}
 (p_{1,2}s_{1,3}+p_{1,3}s_{1,2}).
\end{aligned}                                           \tag{2}
\]

These are physical response coefficients, not consequences in an abstract
quotient.

## Ordinary odd-triangle identity

For a triangle (r<s<t), put

\[
 A=p_r, B=p_s, C=p_t,qquad a=s_r, b=s_s, c=s_t
\]

and write

\[
 f_{st}=Bc+Cb,qquad f_{rt}=Ac+Ca,qquad f_{rs}=Ab+Ba.
\]

Direct expansion gives the integral identity

\[
\boxed{
2ABCabc=(Ca)(Ab)f_{st}-(Cb)(Ab)f_{rt}+(Cb)(Ac)f_{rs}.}
                                                               \tag{3}
\]

If (g_e=Q_e f_e), multiplication of (3) by
(Q_{st}Q_{rt}Q_{rs}) gives an ordinary source-row certificate.  Thus the
six star coordinates and the three matching factors cannot all be nonzero
over characteristic zero.  Every circuit clause in the Boolean formula is
reconstructed from this identity; no division or phase heuristic is used.

## Exhaustive support certificate

The Boolean variables are the optional diagonal (q)-cells, optional star
coordinates, and Tseitin variables for physical source monomials.  The
formula imposes the following necessary conditions on a coefficient point.

- The unary target fibre and the two diagonal response target fibres are
  nonempty.
- Every other top or response coefficient has either zero or at least two
  live physical monomials.
- Every activated universal odd triangle obeys (3).

Before the circuit clauses, this complete top-plus-four-response support
shadow is satisfiable.  Thus the result is genuinely coefficient-algebraic,
not a unique-matching support kill.  After the circuit clauses the exact
formula has

```text
6,399 variables
68,147 clauses
```

Glucose emits a proof whose deletion-free part has 2,316 additions ending
in the empty clause.  A fresh CaDiCaL instance checks every addition by
reverse unit propagation.  The pinned digests are

```text
formula 779e7df5f8060a570c7671cf03f391c50c73439d465d67e0ca71d0a12e842d07
proof   ea3237a755bceca5adb0b28208607508be120653369a1ab6e16f324f07cd1a9e
ledger  bdc82c6acf94a372b2890e30b0212a31ea1415367899c296ec5da07f63712365
```

## Scope

This closes the face on which all twenty-four displayed mixed cells are
mandatory nonzero.  Source ideals are not hereditary under adding or
removing cells, so the theorem does not automatically close every proper
subset of the twenty-four-cell face.  The previously checked minimal
two-cell packets and the present maximal face are separate exact results;
any remaining chart-cover argument must connect the intermediate supports
by source-faithful circuit clauses or a normalization theorem.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_segre_24cell_response_shadow_unit.py
.venv/bin/python -O computations/verify_n8_one_bad_segre_24cell_response_shadow_unit.py
```
