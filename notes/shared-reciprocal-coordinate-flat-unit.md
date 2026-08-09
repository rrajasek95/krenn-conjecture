# The three coordinate-flat budget-thirteen signatures have a three-row unit

## 1. Result

The three coordinate signatures left by
[`shared-reciprocal-budget13-projective-compatibility.md`](shared-reciprocal-budget13-projective-compatibility.md)
are coefficient-empty.  In fact their budget-thirteen incidence data are no
longer needed: any two shared reciprocal rank-one arms with a flat canonical
transition and distinct outgoing target colours give an ordinary polynomial
unit using three full-output coefficients.

The proof is deletion-stable.  It does not localize every cell in a maximal
support and it does not branch on smaller supports.  Consequently it closes
the complete downsets of the `(0,0)`, `(0,1)`, and `(5,5)` coordinate
signatures.

The accompanying checker nevertheless reconstructs the full maximal-envelope
systems as an independent source audit.  After the exact flat-star
substitution there are nine head refinements:

```text
signature 0: 3 systems, 136 cells, 124 variables, 6,561 rows each
signature 1: 3 systems, 136 cells, 124 variables, 6,561 rows each
signature 2: 3 systems, 137 cells, 125 variables, 6,561 rows each
```

All nine systems are killed by each of the six ordered choices of two target
colours, for 54 independently checked three-row certificates.

## 2. Flat-star normal form

Let the shared endpoint be `p`, the outer endpoints be `q,r`, and let `C`
be the remaining sites.  Factor the direct arms in endpoint order as

\[
 A_{pq}=x\otimes y_q,\qquad A_{pr}=x\otimes y_r,
 \qquad y_q\in\langle e_a\rangle,
 \quad y_r\in\langle e_c\rangle,\quad a\ne c.       \tag{1}
\]

The flat-star lemma from the projective checker gives a common output
\(z\in\bigoplus_{u\in C}V_u\) such that

\[
 A_{qu}=y_q\otimes z_u,\qquad
 A_{ru}=y_r\otimes z_u.                              \tag{2}
\]

Thus every block incident with `q`, except the chord `qr`, has its `q` row
on the single target line \(e_a\).  Every non-chord block incident with `r`
has its `r` row on the distinct line \(e_c\).

For the three canonical signatures the outer colours normalize to
`a=1,c=2`.  The shared `p` colour is arbitrary.  Writing the two direct
coefficients as `L,M`, the complete maximal-envelope substitution used by
the checker is

\[
 A_{pq}=L e_b e_1^{\mathsf T},\qquad
 A_{pr}=M e_b e_2^{\mathsf T},\qquad
 A_{qu}=L e_1z_u^{\mathsf T},\qquad
 A_{ru}=M e_2z_u^{\mathsf T}.                        \tag{3}
\]

The `p-C`, `qr`, and admissible `C-C` coefficients remain independent.
Equation (3) is substituted before combining equal matching monomials, so
the frozen rows are coefficient-complete rather than a Boolean support
shadow.

## 3. Equal-colour slices force the chord

Delete `q,r` and call the remaining even set

\[
                         R=\{p\}\cup C.
\]

Let \(F_i\) be the coefficient of the pure word \(i^R\) in the hafnian of
the induced aggregate matrix on `R`, and put

\[
                         D_{ii}=A_{qr}[i,i].          \tag{4}
\]

Fix any target colour `i`.  In a matching contributing to the slice with
`q=r=i`, suppose `q` and `r` are not matched to each other.  The edge at `q`
then requires `i=a`, while the edge at `r` requires `i=c`.  This is
impossible because `a!=c`.  Therefore `qr` is forced term by term, before
any coefficient cancellation.

For two distinct target colours `i,j`, exactness supplies the following
three original source generators:

\[
\begin{aligned}
 G_i       &=D_{ii}F_i-1,\\
 G_{i\mid j}&=D_{ii}F_j,\\
 G_j       &=D_{jj}F_j-1.                            \tag{5}
\end{aligned}
\]

Here `G_i,G_j` are the two pure full words.  The middle row is the mixed
word whose colours at `q,r` are `i` and whose colours at every residual site
are `j`.  The same residual coefficient \(F_j\) occurs literally in the
middle and last rows.

## 4. Ordinary unit certificate

The three rows (5) satisfy over the integers

\[
\begin{aligned}
 D_{jj}G_{i\mid j}-D_{ii}G_j &=D_{ii},\\
 F_i\bigl(D_{jj}G_{i\mid j}-D_{ii}G_j\bigr)-G_i&=1.
                                                               \tag{6}
\end{aligned}
\]

Thus

\[
 \boxed{
  1=F_i\left(D_{jj}G_{i\mid j}-D_{ii}G_j\right)-G_i
 }                                                             \tag{7}
\]

is an ordinary Nullstellensatz certificate.  There are no negative
exponents, divisions, saturation assumptions, or characteristic guards.
It is valid over every commutative ring.

If any admissible envelope cells are deleted, the residual polynomials
\(F_i,F_j\) merely lose matching monomials.  The forced-chord factorization
(5) and the identity (7) remain unchanged.  This proves the promised
deletion stability without enumerating faces.

## 5. Complete maximal-envelope audit

For signatures 0 and 1 the exact row-term histogram, including zero rows,
is

```text
terms: 0     3     4    9    15   45  60
rows:  1458  3237  3    405  1296 108 54
```

For signature 2 it is

```text
terms: 0     3     4    9    15   45  60
rows:  1701  2589  3    324  1728 144 72
```

The three four-term rows are the pure equations: a constant `-1` plus three
matching monomials.  The checker hashes all 6,561 sparse polynomials for
each of the nine head refinements, then reconstructs all 54 instances of
(7) from the original matching expansion.

Run

```bash
python3 computations/verify_shared_reciprocal_coordinate_flat_unit.py
python3 -O computations/verify_shared_reciprocal_coordinate_flat_unit.py
```

Both modes reproduce ledger

```text
63d01c3b76ca9bfcc7018f705347dfad917d042d202858ef494f8a50a550c1b7
```

## 6. Proof consequence

The projective compatibility theorem gave

\[
 \text{flat budget-thirteen state}
 \Longrightarrow (0,0),(0,1),\text{ or }(5,5).
\]

Identity (7) eliminates all three, including every support degeneration.
Hence the shared-reciprocal budget-thirteen gate has no flat coefficient
survivor.

The argument is actually independent of `N=8` and of budget thirteen.  For
any even order and any palette with at least two target colours, two flat
shared reciprocal arms with distinct outgoing target lines yield the same
three-row unit after deleting their outer endpoints.  This is a uniform
coefficient lemma available to the reciprocal descent, not merely a finite
frontier computation.
