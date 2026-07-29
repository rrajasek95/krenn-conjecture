# The rational five-hole point fails the first two-hole lift test

## 1. Outcome

The exact mixed-basis point in
[`five-hole-factorization-counterexample.md`](five-hole-factorization-counterexample.md)
does not lift to the six-site incidence row of an eight-site solution.  The
failure occurs before the arbitrary entries in the sixth-site stars can play
any role: five scalar four-site hafnians formed only from the ten displayed
internal edge blocks are required to vanish, and all five are nonzero.

This remains true for every permutation of the three factor families
`X,Y,D`.  Thus no choice of two families as the two uncontracted stars, and
no nonmonomial completion of the remaining edge-matrix rows, can turn this
particular rational point into 28 simultaneous edge matrices for `n=8`.

## 2. A necessary two-hole condition

Let `U={0,1,2,3,4}` be the five displayed sites and let `k` be the sixth
outside site.  Before contracting `k`, an incidence row of a putative
eight-site solution has the form

\[
 \sum_{r=0}^2\lambda_r e_r^{\otimes6}
       =\left[XY{Q^2\over2}\right]_{1^6}.              \tag{1}
\]

Contracting `k` by `x_k cross y_k` produces the five-hole response
`[X Y D Q]`.  In particular, `x_k,y_k` are independent.  Choose any one of
the three pairs of factor families at the rational point as `X,Y`, and put

\[
                 n_j=x_j\mathbin\times y_j,
 \qquad q_{ab}=n_a^TA_{ab}n_b\quad(a,b\in U).           \tag{2}
\]

For a fixed `i in U`, leave `k,i` open in (1) and contract every site in
`U minus {i}` by its `n_j`.  The target side becomes

\[
 \sum_{r=0}^2\lambda_r
       \left(\prod_{j\ne i}n_{j,r}\right)e_r\otimes e_r. \tag{3}
\]

At the rational point every product in (3) is zero.  On the source side,
the `X,Y` factors must occupy the two open sites, while the two `Q` edges
pair the other four sites.  Hence the contraction is

\[
 H_i\,(x_k\otimes y_i+y_k\otimes x_i),                 \tag{4}
\]

where

\[
 H_i=\operatorname {Haf}(q|_{U\setminus\{i\}}).        \tag{5}
\]

Both local pairs in (4) are independent, so its rank-two response is
nonzero.  Equations (3)--(4) therefore give the necessary condition

\[
                              H_i=0                    \tag{6}
\]

for every `i in U`.  Notice that (6) involves no edge incident to `k`.

## 3. Exact failure at the rational point

For the named pair `(X,Y)`, the five normal zero masks in the displayed
colour order are `(3,3,4,4,4)`.  The ten scalar edge values in (2) are

\[
\begin{array}{c|rrrrrrrrrr}
ab&01&02&03&04&12&13&14&23&24&34\\ \hline
q_{ab}&1/3&-1/6&-1/8&-3/16&-1/18&-1/24&-1/16&1/12&1/8&3/32.
\end{array}                                             \tag{7}
\]

Direct rational evaluation of (5) gives

\[
 (H_0,H_1,H_2,H_3,H_4)
       =\left(-{1\over64},-{3\over64},{3\over64},
                    {1\over16},{1\over24}\right).      \tag{8}
\]

Thus all five necessary equations (6) fail, rather than merely one.

The bracket `[X Y D Q]` is symmetric in its three linear factor families,
so a lift could try a different assignment of the displayed families to
the two stars.  The complete audit is:

\[
\begin{array}{c|c|ccccc}
\text{star pair}&\text{normal zero masks}&H_0&H_1&H_2&H_3&H_4\\ \hline
X,Y&(3,3,4,4,4)&-1/64&-3/64&3/64&1/16&1/24\\
X,D&(5,2,5,2,2)&-1/64&3/64&-3/64&1/16&1/24\\
Y,D&(6,1,1,6,1)&-4/81&4/27&4/27&-16/81&32/243.
\end{array}                                             \tag{9}
\]

Each mask row is `11166` after a colour relabeling.  Consequently all three
target contractions (3) vanish for all five choices of the open displayed
site, while every cofactor in (9) is nonzero.

## 4. Relation to the full square obstruction

The general proof in
[`n8-011166-full-row-square-obstruction.md`](n8-011166-full-row-square-obstruction.md)
first shows that all scalar four-site hafnians except the cofactor
complementary to the two exact-double sites must vanish.  Equations (8)--(9)
locate this particular five-hole point strictly before that proof's later
four-factor permanent obstruction: it violates the initial two-hole
vanishing conditions themselves.

This is a point-specific nonlift certificate.  It does not invalidate the
exact five-hole identity, nor does it by itself exclude other mixed-basis
five-hole factorizations.

## 5. Exact audit

Run

```text
.venv/bin/python computations/verify_five_hole_factorization_two_hole_nonlift.py
```

The checker reconstructs the rational local bases and all ten transformed
edge blocks, rechecks the 243 coefficients of the five-hole identity, and
then verifies the 15 zero target contractions and 15 nonzero hafnians in
(9), entirely over `Q`.
