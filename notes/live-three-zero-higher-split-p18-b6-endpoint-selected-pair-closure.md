# The \(p=18\), \(a=3,b=6\) endpoint selected-pair closure

## 1. Result

On the no-extra-singular live-three-zero stratum, with

\[
                         h+k=18,\qquad 13\leq h\leq17,            \tag{1}
\]

the last three-triple equality family is impossible:

\[
              \boxed{\qquad 3^3 2^6 1^{h-1}
                                  \text{ is impossible}.\qquad} \tag{2}
\]

The proof uses all fifteen ways to select two of the six double values.
It upgrades the sharp one-fibre Schubert cubic from the
[three-triple frontier](live-three-zero-higher-split-p18-three-triple-overlap-frontier.md)
to one common quadratic contradiction.  The neighboring
[two-simple Schubert coupling](live-three-zero-higher-split-p18-b6-two-simple-schubert-coupling.md)
is an independently audited compatibility invariant, but it is not needed
for this closure.

## 2. The endpoint cubic is a polynomial critical equation

Fix a singleton value \(r\), a selected double pair \(Q\), and let
\(B=D\setminus Q\) be the four complementary doubles.  If

\[
                         H_{B,r}(\beta)
                 =\prod_{v\in B}\left(\beta+{4\over r-v}\right), \tag{3}
\]

then the Schubert cubic \(P_{V,r}(\beta)\) from the three-triple frontier
satisfies the exact polynomial identity

\[
 P_{V,r}(\beta)
   ={1\over4}\prod_{v\in B}(r-v)\,H_{B,r}'(\beta).               \tag{4}
\]

Every factor in front of the derivative is structurally nonzero.  Thus
the endpoint condition is

\[
                              H_{B,r}'(\beta_{r,Q})=0,            \tag{5}
\]

including the cases in which a reciprocal presentation of the critical
equation would be undefined.

Choose \(r\ne0\).  Such a singleton exists because there are
\(h-1\geq12\) singleton values and at most one is zero.  For each double
value \(v\), put

\[
 t_v={2(r+v)\over r-v},\qquad
 a(t)={3t\over4}+{2\over t},\qquad K=r\Omega_r+7.                \tag{6}
\]

Distinctness and nonoppositeness make the six \(t_v\)'s finite, nonzero,
and pairwise distinct.  The exact identities

\[
 {4r\over r-v}=t_v+2,qquad
 r\left({3\over r-v}+{2\over r+v}\right)
       ={5\over2}+a(t_v)                                        \tag{7}
\]

turn (5), for every selected pair \(\{i,j\}\), into

\[
 {d\over dX}\prod_{k\notin\{i,j\}}(X+t_k)=0,
              \qquad X=K+a(t_i)+a(t_j).                          \tag{8}
\]

This is the polynomial form of the fifteen-pair system; no denominator in
(8) needs to be inverted.

## 3. Symmetric pair compression

Let \(E_m\) denote the global elementary symmetric functions of
\(t_1,\ldots,t_6\).  For one selected pair, write

\[
                         p=t_i+t_j,\qquad q=t_it_j.               \tag{9}
\]

The first three elementary symmetric functions of the four complementary
values are

\[
\begin{aligned}
 c_1&=E_1-p,\\
 c_2&=E_2-q-pc_1,\\
 c_3&=E_3-qc_1-pc_2.
\end{aligned}                                                    \tag{10}
\]

Since \(a(t_i)+a(t_j)=3p/4+2p/q\), equation (8) is

\[
 4X^3+3c_1X^2+2c_2X+c_3=0,
              \qquad X=K+{3p\over4}+{2p\over q}.                \tag{11}
\]

Multiplication by \(q^3\) clears all denominators.

Fix \(i\), write \(x=t_i\), and replace the partner value by an
indeterminate \(y\).  Substitute \(p=x+y\), \(q=xy\) in the cleared
left side of (11), and call the resulting sextic \(F_x(y)\).  Exact
expansion gives only the following three coefficients:

\[
\begin{aligned}
 [y^6]F_x&={x^3\over2},\\
 [y^5]F_x&={x^2\over16}
       \bigl(19E_1x+68Kx+32x^2+136\bigr),\\
 [y^0]F_x&=32x^3.
\end{aligned}                                                    \tag{12}
\]

For the five choices \(j\ne i\), equation (11) says
\(F_x(t_j)=0\).  Because those five values are distinct and \(x\ne0\),
there is a sixth root \(\rho_x\) such that

\[
             F_x(y)={x^3\over2}
                 \prod_{j\ne i}(y-t_j)(y-\rho_x).               \tag{13}
\]

Let \(E_6=\prod_jt_j\ne0\).  Comparing constant coefficients in
(12)--(13) gives

\[
                              \rho_x={64x\over E_6}.              \tag{14}
\]

Comparing the coefficients of \(y^5\), and substituting (14), yields

\[
 \boxed{\quad
 \left(24+{512\over E_6}\right)x^2
       +(27E_1+68K)x+136=0.
 \quad}                                                         \tag{15}
\]

The same equation holds for every \(x=t_1,\ldots,t_6\).  Its left side
is a polynomial of degree at most two and is nonzero because its constant
coefficient is \(136\).  It cannot have six distinct roots in
characteristic zero.  This contradiction proves (2).

## 4. Consequence for the \(p=18\) equality ledger

Sections 6, 9--11 of the three-triple frontier close \(b=0,1,2,3,4,5\),
and (15) closes \(b=6\).  Hence all seven three-triple equality families
are now closed.  Together with the earlier four-, five-, and six-triple
overlap theorems, every \(p=18\) equality family having at least three
triple values is impossible.

## 5. Exact audit

Run

```text
uv run python computations/verify_live_three_zero_higher_split_p18_b6_endpoint_selected_pair_closure.py
```

The checker verifies the polynomial identity (4), the transformation
(6)--(8), the symmetric complement formulas (10), every coefficient in
(12), and the comparison leading to the nonzero quadratic (15).

The expected output is

```text
p=18 b=6 endpoint selected-pair closure PASS
selected-pair equations audited: 15
six transformed doubles forced onto one nonzero quadratic
remaining a=3 families: none
```
