# No flat shared reciprocal pair survives exactness

## 1. Uniform theorem

Let `pq` and `pr` be two literal rank-one witness arms sharing `p`.  Write

\[
 A_{pq}=x_q\otimes y_q,\qquad
 A_{pr}=x_r\otimes y_r,                              \tag{1}
\]

where the outer factors lie on distinct target lines

\[
 y_q\in\langle e_a\rangle,\qquad
 y_r\in\langle e_c\rangle,\qquad a\ne c.             \tag{2}
\]

For an exact GHZ hafnian source at any even order `N>=4`, the canonical
transition between these arms cannot be flat.

This strengthens
[`shared-reciprocal-coordinate-flat-unit.md`](shared-reciprocal-coordinate-flat-unit.md):
there are two flat-star cases according as the shared factors `x_q,x_r` are
proportional or independent, and the same three-row unit closes both.  No
budget-thirteen normal form, site-cover hypothesis, maximal support, or
localization is used.

## 2. The two flat-star cases

Let `C` be the sites other than `p,q,r`, and let `T_q,T_r` be the `q-C` and
`r-C` endpoint stars.

### Proportional shared factors

After normalizing `x_q=x_r=x`, flatness gives one common output
\(z\in\bigoplus_{u\in C}V_u\):

\[
 T_q=y_q\otimes z,\qquad T_r=y_r\otimes z.            \tag{3}
\]

Including the direct blocks to `p`, every non-chord edge at `q` has its
`q` factor on \(e_a\), while every non-chord edge at `r` has its `r` factor
on \(e_c\).  An equal-colour slice `q=r=i` could use `q,r` separately only
if `i=a=c`, contrary to (2).

### Independent shared factors

Flatness instead gives

\[
                         T_q=T_r=0.                  \tag{4}
\]

The only non-chord edge remaining at `q` is the direct arm `pq`, and the
only one at `r` is `pr`.  A perfect matching cannot use both separately,
because both would have to match the same site `p`.  This explicitly audits
the possible direct-arm escape: using `pq` leaves `r` with no live
non-chord partner, and using `pr` leaves `q` with none.

Thus in **both** cases every equal-colour `q=r=i` slice forces the chord
`qr` term by term.

## 3. The common ordinary unit

Let

\[
                         R=V\setminus\{q,r\}
\]

be the residual even site set.  Denote by \(F_i\) the pure-`i` coefficient
of the induced residual hafnian and by

\[
                         D_{ii}=A_{qr}[i,i]           \tag{5}
\]

the diagonal chord coefficient.  Choose any two distinct target colours
`i,j`.  The forced-chord statement gives three literal full-source rows:

\[
\begin{aligned}
G_i&=D_{ii}F_i-1,\\
G_{i\mid j}&=D_{ii}F_j,\\
G_j&=D_{jj}F_j-1.                                    \tag{6}
\end{aligned}
\]

The middle word has colour `i` at `q,r` and colour `j` at every site of
`R`.  As an identity over the integers,

\[
 \boxed{
  1=F_i\left(D_{jj}G_{i\mid j}-D_{ii}G_j\right)-G_i.
 }                                                     \tag{7}
\]

This is an ordinary polynomial certificate: it has no denominators,
negative exponents, determinant saturation, or characteristic restriction.
Deleting arbitrary cells only deletes terms from the residual polynomials
\(F_i,F_j\), so (6)--(7) remain valid.

## 4. Machine audit

The checker builds unrestricted `N=8` flat envelopes, not the three finite
budget signatures:

- proportional: the `q-C,r-C` stars are parametrized by the common `z`;
- independent: both stars are identically zero;
- all `p-C`, `qr`, and `C-C` cells remain arbitrary.

It reconstructs all 6,561 coefficient rows of one complete envelope in each
case.  It then audits all ternary head refinements and all ordered colour
pairs:

```text
case           heads   three-row units   non-chord route checks
proportional      18          108                  4860
independent       36          216                  9720
```

The route checks enumerate every perfect matching not using `qr`, including
every possible use of `pq` or `pr`.  The certificate checks expand the three
rows from the original matching source and reduce (7) to the constant one.

Run

```bash
python3 computations/verify_shared_reciprocal_flat_bicase_unit.py
python3 -O computations/verify_shared_reciprocal_flat_bicase_unit.py
```

Both modes reproduce

```text
f35f3089eec64c65ccef345ce6b434f79699612257094affad9dcfaf03dcfef6
```

The finite checker specializes to the ternary `N=8` source.  The proof of
(7) is dimension-free: it uses only two distinct target colours and the
residual hafnian after removing `q,r`.  Hence the theorem applies for every
even `N>=4` and every target palette of size at least two.

## 5. Exact remaining implication

For an exact source with shared literal rank-one witness arms and distinct
outer target lines, the dichotomy is now

\[
 \boxed{\text{the canonical transition is nonflat}.}         \tag{8}
\]

If both arms are good at both endpoints, (8) is precisely the hypothesis of
the existing curved rank-one overlap branch.  Such a pair is therefore a
forced curved overlap; no flat wedge or flat coordinate packet remains.

Without the four goodness conditions, the exact conclusion is only
nonflatness.  The complementary structural datum is then a named
rank-deficient deleted endpoint star (equivalently, an essential incidence),
which must be handled by the low-rank/cubic descent.  The unit theorem does
not silently promote a rank-deficient pair to the curved-good branch.
