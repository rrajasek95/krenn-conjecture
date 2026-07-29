# The residual \(p=18\), \(a=3,b=6\) two-simple Schubert coupling

## 1. Scope and result

The sole residual three-triple equality family is

\[
                              3^3 2^6 1^{h-1},
                    \qquad 13\leq h\leq17.                       \tag{1}
\]

Its two useful formal selections are

\[
\begin{array}{c|c}
(d,t)&\text{complement}\\ \hline
(2,0)&3^3 2^4 1,\\
(2,1)&3^2 2^5 1^2.
\end{array}                                                       \tag{2}
\]

The first selection gives the sharp one-simple Schubert cubic already
derived in the
[three-triple frontier](live-three-zero-higher-split-p18-three-triple-overlap-frontier.md).
This note computes the exact two-simple Schubert image for the neighboring
selection and couples its Robin slopes to the same endpoint baseline.

The result is a genuine new invariant, but not a global closure.  On the
generic slope chart, eliminating the second simple-root slope gives an
essential degree-eleven condition.  Two singular charts must also be
retained.  After the actual moving-singleton substitution, their degree
budget is larger than the available number of singleton values.  The one
uniform consequence is that, when \(h=17\), a hypothetical configuration
in (1) cannot contain a zero singleton value.

## 2. The shared endpoint baseline

Let \(D\) be the six double values, \(X\) the three triple values, and
\(Y\) the \(h-1\) singleton values.  At a fixed singleton \(r\), put

\[
 \Omega_r={k\over r+\mu}
 +\sum_{y\in Y\setminus\{r\}}{1\over r+y}
 -4\sum_{x\in X}{1\over r-x}
 -3\sum_{v\in D}{1\over r-v}.                                  \tag{3}
\]

For an endpoint selection whose selected double pair is \(Q\subset D\),
the actual Robin slope is

\[
 \beta^{\rm end}_{r,Q}=\Omega_r+\sum_{u\in Q}\phi_u(r),
 \qquad
 \phi_u(r)={3\over r-u}+{2\over r+u}
            ={5r+u\over r^2-u^2}.                               \tag{4}
\]

All fifteen selected pairs must satisfy the endpoint cubic.  In the
critical-point form of that cubic,

\[
 \sum_{v\in D\setminus Q}
 {1\over \beta^{\rm end}_{r,Q}+4/(r-v)}=0.                       \tag{5}
\]

Now use the neighboring selection: select one double \(u\), one triple
\(x\), and all but two singleton values \(r,s\).  Its slope at \(r\) is

\[
\begin{split}
 \beta^{\rm nbr}_{r;u,x,s}
  ={}&\Omega_r+\phi_u(r)+\psi_x(r)
       -{1\over r+s}-{2\over r-s},\\
 \psi_x(r)={}&{4\over r-x}+{3\over r+x}
              ={7r+x\over r^2-x^2}.                             \tag{6}
\end{split}
\]

Thus (5) and the neighboring Schubert conditions below use exactly the
same \(\Omega_r\).  Equations (4) and (6), not two unrelated accessory
parameters, are the concrete coupling between the selections in (2).

## 3. The normalized two-simple Wronski image

Normalize the simple roots \(r,s\) to \(0,1\), and write \(b,g\) for the
correspondingly scaled Robin slopes.  Their joint kernel in
\(\mathbb C[z]_{\leq5}\) is four-dimensional.  On the chart

\[
                              \delta=bg+b-g\ne0,                  \tag{7}
\]

one convenient basis is, for \(m=2,3,4,5\),

\[
                  P_m(z)=\delta z^m-(bg+mb)z+g+m.                \tag{8}
\]

Every three-space inside this four-space is a hyperplane.  The four
coordinate Wronskians are divisible by \(z^2(z-1)^2\), and their
quotients span a rank-four subspace of the six-dimensional quintics.
Consequently a monic target

\[
                V(z)=z^5-e_1z^4+e_2z^3-e_3z^2+e_4z-e_5          \tag{9}
\]

obeys two exact linear conditions in its coefficients.  The checker
constructs the coefficient matrix directly and gives two polynomial
left-null covectors, denoted \(F(b,g;e)=0\) and \(G(b,g;e)=0\).
Eliminating \(g\) factors as

\[
 \operatorname {Res}_g(F,G)
  =C\bigl(be_5-3e_4+10e_5\bigr)^2
       \mathcal R_{11}(b;e_1,\ldots,e_5),                         \tag{10}
\]

where \(C\ne0\) is irrelevant and \(\mathcal R_{11}\) has degree eleven
in \(b\).

The squared linear factor in (10) comes from the singular chart \(g=-5\)
and is not sufficient there.  Direct recomputation gives the two
conditions

\[
\begin{split}
 be_5-3e_4+10e_5&=0,\\
 { (4b-5)^3\over225}e_5
 -{(4b-5)^2\over75}e_3
 +{2(4b-5)\over15}e_2-e_1&=0.                                  \tag{11}
\end{split}
\]

The basis chart divisor \(\delta=0\), equivalently
\(g=b/(1-b)\), is separate as well.  One of its two exact conditions is

\[
                         4b-5-(b-2)e_1=0.                        \tag{12}
\]

The checker also treats the intersection \((b,g)=(5/4,-5)\) directly.
Hence no slope solution is lost by the chart decomposition.

## 4. The exact moving-singleton degree barrier

Fix \(r,u,x\), put \(d=s-r\), and let \(E_j\) be the elementary
symmetric functions of the five fixed offsets \(v-r\),
\(v\in D\setminus\{u\}\).  Under the normalization in Section 3,

\[
                 e_j={E_j\over d^j}.                             \tag{13}
\]

If \(C=\Omega_r+\phi_u(r)+\psi_x(r)\), equation (6) gives

\[
 b=d\beta^{\rm nbr}_{r;u,x,s}
   ={Cd^2+(2rC+1)d+4r\over d+2r}.                               \tag{14}
\]

Substitute (13)--(14) into the three chart conditions.  After removing
the collision factor \(d=0\) and clearing only structurally protected
denominators, the generic essential polynomial has degree seventeen in
\(d\); the \(g=-5\) and \(\delta=0\) chart conditions each contribute a
polynomial of degree at most two.  But after fixing \(r\), only

\[
                          |Y|-1=h-2\in\{11,12,13,14,15\}          \tag{15}
\]

moving singleton values remain.  Thus the current union-of-charts root
count cannot close (1).

There is one useful endpoint restriction.  If \(r=0\), the three degree
bounds improve to eleven, one, and two.  The degree-eleven polynomial has
nonzero constant term proportional to \(-E_5^3\); the degree-one chart
has nonzero constant term proportional to \(E_5\); and (12) cannot become
an identity.  Their union contains at most fourteen values.  For \(h=17\),
(15) supplies fifteen.  Therefore

\[
 \boxed{\text{a hypothetical }h=17,\ b=6\text{ configuration has no
 zero singleton value}.}                                       \tag{16}
\]

This is a structural subcase closure, not closure of the symbolic family.

## 5. The compact fifteen-pair elimination target

For a nonzero fixed singleton \(r\), introduce

\[
 t_v={2(r+v)\over r-v},\qquad
 a(t)={3t\over4}+{2\over t},\qquad K=r\Omega_r+7.                \tag{17}
\]

Then all fifteen endpoint equations (5) become

\[
 \boxed{\qquad
 \sum_{k\notin\{i,j\}}
 {1\over K+a(t_i)+a(t_j)+t_k}=0,
 \qquad 1\leq i<j\leq6.
 \qquad}                                                        \tag{18}
\]

This seven-variable rational system is the smallest exact target left by
the endpoint selection.  Bounded numerical reconnaissance has not found a
finite compatible point, but that receives no proof credit.  The next
useful step is either an exact saturated elimination of (18), or a
selected-double exchange between (18) and one of the two conditions
\(F=G=0\) before eliminating the second simple slope.  Eliminating that
slope first is precisely what creates the degree barrier in Section 4.

## 6. Exact audit

Run

```text
uv run python computations/verify_live_three_zero_higher_split_p18_b6_two_simple_schubert_coupling.py
```

The checker constructs (8), the four coordinate Wronskians, the rank-four
quintic image, both generic null covectors, the factorization (10), both
singular charts and their intersection, the actual exchange formulas
(4), (6), the degree bounds after (13)--(14), and the fifteen endpoint
equations (18).

The expected output is

```text
p=18 b=6 neighboring Schubert coupling PASS
normalized Wronski image: rank 4 in quintics (codimension 2)
generic eliminated slope degree: 11
general moving-singleton degree barrier: 17 + 2 + 2 charts
endpoint selected-pair equations retained: 15
```
