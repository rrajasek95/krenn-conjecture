# A direct permanent-null cap closes both fixed-star one-bad packets

## Theorem

Relabel the unary top colour as `0` and the two binary response colours as
`1,2`.  In either fixed-star orientation, suppose the six-site residual
quadratic `q` satisfies

\[
 q^{[3]}=X_0,
 \qquad p_i s_j q^{[2]}=\delta_{ij}X_i
 \quad(i,j\in\{1,2\}).                                  \tag{1}
\]

Here every `p_i,s_j` is the literal one-site coordinate port encoded by the
fixed star.  Then no such packet exists.  Indeed, put

\[
 K=\begin{pmatrix}1&1\\-1&1\end{pmatrix},
 \qquad R_K=\sum_{i,j=1}^2K_{ij}p_i s_j.                 \tag{2}
\]

The diagonal of `K` is `(1,1)`, while

\[
 \det K=2,
 \qquad \operatorname{perm}K=1-1=0.                    \tag{3}
\]

The exact divided-power expansion is

\[
 (q+R_K)^{[3]}
 =q^{[3]}+R_Kq^{[2]}+R_K^{[2]}q+R_K^{[3]}.              \tag{4}
\]

The complete response matrix in (1) gives

\[
                         R_Kq^{[2]}=X_1+X_2.             \tag{5}
\]

Both higher terms in (4) vanish source-coefficientwise.  Consequently

\[
                         (q+R_K)^{[3]}
                         =X_0+X_1+X_2=\Delta_{6,3}.      \tag{6}
\]

This contradicts the committed arbitrary-complex six-site theorem.  Hence
both fixed-star one-bad orientations are empty.

The exact checker is
`computations/verify_n8_one_bad_direct_permanent_null_descent.py`.

## Literal source provenance

For the first orientation the response ports, listed by colours `(1,2)`, are

```text
p-sites = (3,2),     s-sites = (5,4).
```

Thus (2) adds the four endpoint-coloured source cells

```text
35:11 =  1,    34:12 =  1,
25:21 = -1,    24:22 =  1.
```

The two perfect matchings of these four port sites have the same endpoint
word `(site2,site3,site4,site5)=(2,1,2,1)`.  Their coefficients are

```text
(35:11)(24:22) =  1,
(34:12)(25:21) = -1.
```

They cancel literally, proving `R_K^[2]=0` as a full decorated tensor—not
merely after an output contraction.  Since `R_K` touches only sites
`2,3,4,5`, it has no three-edge perfect matching on all six residual sites,
so `R_K^[3]=0`.  The first defect in (4) is therefore zero for arbitrary
unknown cells of `q`:

\[
                         R_K^{[2]}q=0.                   \tag{7}
\]

In the second orientation the colour-2 ports are reversed:

```text
p-sites = (3,4),     s-sites = (5,2).
```

The two port matchings are now `35|24` and `23|45`; they carry the same
decorated word and coefficients `1,-1`, so the identical cancellation holds.
Endpoint order is retained in both cases.

## Why the full response block is essential

Equation (5) uses both diagonal response rows and both off-diagonal zeros.
If an off-diagonal response survives, its coefficient is multiplied by a
nonzero off-diagonal entry of `K` and the first insertion is already dirty.
This is exactly why the sharp seven-cell packets, whose cross rows contain
private unit monomials, do not contradict the theorem.

The one-site nature of the four ports is equally load-bearing.  For arbitrary
multi-site star forms, products such as `p_1^2 s_1s_2` need not be site-zero;
then permanent zero cancels only the distinct-row/distinct-column sector and
higher defects can survive, as in the OO one-anchor counterguard.  The present
theorem applies because the fixed-star normalization has already supplied
four distinct literal ports.

## Consequence for the five tensor identities

In the original colour convention, the first fixed-star packet is

\[
 H_{0124}=X_0,\quad H_{0135}=X_1,\quad
 H_{0125}=H_{0134}=0,\quad H_{012345}=X_2.
\]

Relabel `(2,0,1)` as `(0,1,2)` and the construction above applies verbatim.
For the second orientation the two zero cofactors are `H0145,H0123`; reversing
the colour-2 ports gives the second literal cancellation described above.

Thus the permanent-null cap supplies the compact algebraic identity that the
response-only flattening did not: it uses the fifth top equation in the
constant term of (4), and all four response tensors in its linear term.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_direct_permanent_null_descent.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_direct_permanent_null_descent.py
```

Both modes freeze the ledger digest printed by the checker and pin the
arbitrary-complex six-site terminal theorem.
