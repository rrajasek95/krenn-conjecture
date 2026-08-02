# The bare full-nine polar has nonzero Schur connecting class

This is an exact source-labelled \(h=3\) no-go for the first proposed
full-nine realization of the chart-25 Schur class. It constructs the literal
two-chart source columns and their marked principal-parts tails before orbit
or physical-sector identification.

The outcome is sharp: the five polar cochains have source-relative connecting
matrix \(I_5\). Hence none admits a cochain lift

\[
                        \Lambda T'=M A'.                 \tag{1}
\]

The target-side scalar \(\kappa Y\) is therefore not yet a well-defined
Schur pairing for the bare polar construction. A denominator-marked
two-edge comparison cell must first cancel this connecting class.

This does not rule out that enlarged comparison and does not prove Krenn's
conjecture.

## 1. The ten literal source columns

Use the direct-free eight-site specialization

\[
 x=0,\qquad D=(1,2,3,4,5),\qquad p=6,\qquad q=7,\qquad r=3,
 \qquad A_{pr}=0,
\]

and the odd word \(m=12112\). For each \(v\in D\), let \(c_v\) be mixed on
\(D\setminus\{v\}\) and zero on \(x,v,p,q\). Explicitly,

\[
\begin{array}{c|ccccc}
v&1&2&3&4&5\\\hline
c_v&00211200&01011200&01201200&01210200&01211000.
\end{array}                                              \tag{2}
\]

Retain the two individually labelled chart rows

\[
                      r_v^{pq},\qquad r_v^{pr}.           \tag{3}
\]

Their physical lower boundaries are the same direct-free global hafnian:

\[
       A'(r_v^{pq})=A'(r_v^{pr})=H_{c_v}^{\mathrm{df}}.   \tag{4}
\]

Every column in (4) has 90 distinct labelled matching monomials. Exact
elimination on all ten columns gives

\[
        \operatorname{rank}A'=5,\qquad
        \ker A'=\left\langle
          k_v=r_v^{pq}-r_v^{pr}:v\in D
        \right\rangle.                                   \tag{5}
\]

No chart orbit has been collapsed in (3)--(5).

## 2. Their marked Rees tails

Mark the two physical variables

\[
                         a_{xv}^{00},\qquad a_{pq}^{00}. \tag{6}
\]

Literal differentiation of each labelled matching polynomial gives

\[
 {\partial^2H_{c_v}^{\mathrm{df}}\over
  \partial a_{xv}^{00}\partial a_{pq}^{00}}
     =h_v,                                               \tag{7}
\]

where \(h_v\) is the three-term hafnian on \(D\setminus\{v\}\). The chart
sector placement is also literal:

\[
\begin{aligned}
 T'(r_v^{pq})&=(h_v)_{pq,\mathrm{direct}},\\
 T'(r_v^{pr})&=(h_v)_{pr,\mathrm{two\text{-}star}}.
\end{aligned}                                            \tag{8}
\]

The other marked sector is zero in each line. The five supports of \(h_v\)
are disjoint as labelled face monomials.

Physical identification of the two sector copies would erase the difference
in (8), but it would also erase the very Rees symbol intended to land on the
curvature/cap residue. The Schur test must therefore be performed on (8),
before that identification.

## 3. Five leading cochains

Let \(V\) be the two marked sector copies in (8). For each \(v\), define
\(\Lambda_v\in V^*\) by assigning weight \(+1/6\) to each of the three
terms of \((h_v)_{pq,\mathrm{direct}}\), weight \(-1/6\) to the corresponding
three terms of \((h_v)_{pr,\mathrm{two\text{-}star}}\), and zero elsewhere.
Thus

\[
 \Lambda_v(h_v^{pq})=\frac12,\qquad
 \Lambda_v(h_v^{pr})=-\frac12.                           \tag{9}
\]

The existing pure denominator faces \(g_s\) enter diagonally in the two
sector copies. Let \(B'\) be their five-column leading block. The exact
labelled monomials give

\[
                           \Lambda_vB'=0                 \tag{10}
\]

for all \(v\). This remains true if the relevant associated-grade leading
block is taken to be zero.

## 4. The Schur equation fails by an identity matrix

Evaluate the candidate tail cochains on the exact lower-kernel basis (5).
Equations (8)--(9) give

\[
       (\Lambda_vT')(k_w)=\delta_{vw}.                   \tag{11}
\]

Thus the source-relative connecting map on the five polar classes is

\[
 \partial:
 \langle\Lambda_1,\ldots,\Lambda_5\rangle
       \longrightarrow(\ker A')^*,
 \qquad
 [\partial]_{\Lambda,k}=I_5.                            \tag{12}
\]

In particular, suppose (1) held for some \(M\). Evaluation on \(k_w\) would
give

\[
       \delta_{vw}
        =(\Lambda_vT')(k_w)
        =(MA')(k_w)
        =M(A'k_w)
        =0,                                              \tag{13}
\]

a contradiction. Direct rational row-space elimination gives the same
answer:

\[
 \operatorname{rank}\operatorname{row}A'=5,\qquad
 \operatorname{rank}
   \bigl(\operatorname{row}A'+\langle\Lambda_vT'\rangle\bigr)=6
                                                               \tag{14}
\]

for every \(v\).

Therefore all five apparent leading polar classes are killed by their
nonzero source-relative connecting classes. This is the exact analogue of
the 153 apparent degree-five chart classes removed by the filtered Macaulay
Schur test, but here the connecting map is the identity.

## 5. Consequence for the curvature/adjacent-power target

The target side of the proposed comparison is already normalized. For

\[
 D_{\mathrm{cap}}=\begin{pmatrix}A&B\\F&U\end{pmatrix},
 \qquad \kappa=AU-BF,
\]

the adjugate covector reads the curvature column as \(\kappa\), while the
split-cap left kernel reads its missing column as \(\kappa Y\). The chart-25
class has \(\lambda_{25}(4D)=1\). Hence the desired scalar factorization is

\[
                         1\cdot\kappa\cdot Y=\kappa Y.   \tag{15}
\]

But multiplying (12) by this active scalar gives

\[
                       \partial_{\mathrm{active}}
                           =\kappa Y\,I_5,               \tag{16}
\]

which is still invertible after localizing at \(\kappa Y\). Target-side
curvature cannot repair the failed source lift. Consequently an expression
such as

\[
                         \Lambda c'-M b'=\pm\kappa Y     \tag{17}
\]

is not yet a legitimate Schur pairing: \(M\) does not exist for the bare
polar comparison.

The next cell must alter the source complex before (17) is evaluated. Its
tail on the five kernel vectors must contribute \(-I_5\). This recovers,
now as a forced Schur equation, the previously proposed
denominator-marked two-edge generator

\[
              [\,K_v;\ d_{v,m_v};\ a_{xv}^{00},a_{pq}^{00};
                    \sigma\,].                           \tag{18}
\]

If such a literal cell cancels (12), the corrected leading cochain will lie
in \(\ker\partial\); only then is the target test (17) well defined. A
mapping-cylinder target cell cannot perform this repair because it changes
the target bookkeeping without cancelling the source-side identity matrix.

## 6. Exact verification and scope

Run

~~~text
python3 computations/verify_h3_literal_full_nine_schur_polar_no_go.py
python3 -O computations/verify_h3_literal_full_nine_schur_polar_no_go.py
python3 -I computations/verify_h3_literal_full_nine_schur_polar_no_go.py
python3 -S computations/verify_h3_literal_full_nine_schur_polar_no_go.py
~~~

The checker reconstructs all ten labelled 90-term columns, all ten marked
three-term tails, the five-dimensional lower kernel, the diagonal old
pure-denominator block, the five cochains (9), and the identity matrix
(12). It also verifies that multiplying by four exact active
curvature/cap scalars leaves the connecting map full rank.

The frozen ledger digest is
6f33d533bb093d813aaa6a553d8d872ad7c397efa5c13849cd2c114a8edbd6bc.

The no-go applies to the bare marked principal-parts comparison with the
existing pure denominator leading block. It does not rule out the new
denominator-marked cell in (18), a larger source-provenant Hasse/Spencer
totalization, or a different literal operation whose added tail cancels
(12).
