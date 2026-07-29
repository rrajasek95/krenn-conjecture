# The wedge equality stratum has no common-power lift

## 1. Result

This note closes the last rank-budget-twelve geometry left by
[`rank-budget-path-triangle-exposed-grid-obstruction.md`](rank-budget-path-triangle-exposed-grid-obstruction.md).
Unlike the earlier conditional argument in
[`wedge-equality-coordinate-oriented-obstruction.md`](wedge-equality-coordinate-oriented-obstruction.md),
none of the three omission-pair blocks of the quadratic is assumed to
vanish.

Let

\[
 U=\{a,b,c,d,e,f\},\qquad B_0=ab,\quad B_1=bc,\quad B_2=de,
                                                               \tag{1}
\]

and suppose the incident endpoint spaces are the equality-budget spaces

\[
\begin{array}{c|cccccc}
u&a&b&c&d&e&f\\ \hline
W_u&\langle e_1,e_2\rangle&\langle e_2\rangle&
\langle e_0,e_2\rangle&\langle e_0,e_1\rangle&
\langle e_0,e_1\rangle&\langle e_0,e_1,e_2\rangle .
\end{array}                                                \tag{2}
\]

Work in the site-square-zero tensor algebra.  Let

\[
 q=\sum_{u<v}q_{uv},\qquad q_{uv}\in W_u\otimes W_v,
 \qquad F=q^{[2]},                                        \tag{3}
\]

where the bracket power is the unordered matching sum.  Write \(F_{uv}\)
for the four-site component supported on \(U\setminus\{u,v\}\).

The three target cofactors are

\[
\begin{aligned}
F_{ab}&=\lambda _0e_0^{(c)}e_0^{(d)}e_0^{(e)}e_0^{(f)},\\
F_{bc}&=\lambda _1e_1^{(a)}e_1^{(d)}e_1^{(e)}e_1^{(f)},\\
F_{de}&=\lambda _2e_2^{(a)}e_2^{(b)}e_2^{(c)}e_2^{(f)},
\end{aligned}
\qquad \lambda _0\lambda _1\lambda _2\ne0,             \tag{4}
\]

and the typed response grid forces

\[
             F_{ac}=F_{ae}=F_{be}=F_{bd}=F_{cd}=0.       \tag{5}
\]

**Theorem 1.1 (unconditional wedge obstruction).**  Equations
(2)--(5) are incompatible with

\[
                              q^{[3]}=0.                 \tag{6}
\]

In particular, \(q_{ab},q_{bc},q_{de}\) are arbitrary tensors throughout;
they are not zero hypotheses.  The proof keeps every matching summand and
all complex cancellation.  It uses only tensor flattening, quotient
projections, and exact cofactor identities.

Together with the path and triangle obstruction, Theorem 1.1 eliminates
every rank-budget equality type having a rank-three site.  It says nothing
about endpoint-rank budget strictly greater than twelve.

## 2. Why the five cofactor zeros are support-independent

For completeness, we restate the quotient-grid argument which supplies
(5).  It is important that this argument acts on the complete cofactor
\(F_P\), not on individual perfect-matching terms.

At the rank-one and rank-two sites, let

\[
 A_0,\quad B_0,B_1,\quad C_1,\quad D_2,\quad E_2       \tag{7}
\]

denote the exposed missing-colour modes.  If \(x=(P,S)\) and
\(y=(P',S')\), put

\[
                         \Phi(x,y)=P(S')^{\mathsf T}
                                      +P'S^{\mathsf T}. \tag{8}
\]

The complete typed grids on \(AB\) and \(BC\) contain the two nonzero
target corners

\[
 \Phi(A_0,B_0)\in\mathbb F^*E_{00},\qquad
 \Phi(B_1,C_1)\in\mathbb F^*E_{11},                    \tag{9}
\]

and the crossed zero corners

\[
                         \Phi(A_0,B_1)=\Phi(B_0,C_1)=0. \tag{10}
\]

The crossed-target lemma makes all four modes pure.  After globally
interchanging \(P,S\), take \(A_0,B_1\) to be \(P\)-pure and \(B_0,C_1\)
to be \(S\)-pure.  Hence

\[
                              \Phi(A_0,C_1)\ne0.         \tag{11}
\]

For a non-omission pair \(P\), the double-quotient response equation is

\[
                              N_P\otimes F_P=0.          \tag{12}
\]

Evaluating (12) at the modes in (11) gives \(F_{ac}=0\).

If \(F_{bd}\ne0\), the two evaluations of (12) at
\((B_0,D_2)\) and \((B_1,D_2)\) would make \(D_2\) have zero \(\Phi\)-pairing
with nonzero pure points of both types.  Thus both components of \(D_2\)
would vanish, contradicting the nonzero \(DE\) target.  Therefore
\(F_{bd}=0\), and the identical argument gives \(F_{be}=0\).

Finally, at least one of
\(P_{D_2}S_{E_2}^{\mathsf T}\) and
\(P_{E_2}S_{D_2}^{\mathsf T}\) is nonzero.  Interchange \(d,e\) if
necessary so the first is nonzero.  Then

\[
                         \Phi(C_1,D_2)\ne0,
                         \qquad \Phi(A_0,E_2)\ne0.      \tag{13}
\]

Equation (12) on \(CD\) and \(AE\) gives \(F_{cd}=F_{ae}=0\).
This proves all five zeros in (5) without making any assertion about the
support of \(q\).

## 3. The rank-one star allows at most one adjacent hole block

Every perfect matching has a unique edge incident with \(b\).  Consequently
(6) gives the literal star expansion

\[
 q_{ab}F_{ab}+q_{bc}F_{bc}+q_{bd}F_{bd}
             +q_{be}F_{be}+q_{bf}F_{bf}=0.             \tag{14}
\]

Because \(W_b=\mathbb F e_2^{(b)}\), write

\[
 q_{ab}=e_2^{(b)}x_a,\qquad q_{bc}=e_2^{(b)}y_c,
 \qquad q_{bf}=e_2^{(b)}z_f.                           \tag{15}
\]

Using (4)--(5), remove the common nonzero factor at \(b\) from (14):

\[
 \lambda _0x_ae_0^{(c)}e_0^{(d)}e_0^{(e)}e_0^{(f)}
 +\lambda _1e_1^{(a)}y_ce_1^{(d)}e_1^{(e)}e_1^{(f)}
 +F_{bf}z_f=0.                                         \tag{16}
\]

If \(x_a,y_c\ne0\), the sum of the first two terms has flattening rank
two across

\[
                       W_f\mid(W_a\otimes W_c\otimes W_d\otimes W_e).
                                                               \tag{17}
\]

Indeed, its \(e_0^{(f)}\)- and \(e_1^{(f)}\)-coefficient tensors are
nonzero and independent already at site \(d\).  The last term of (16) has
rank at most one across (17), a contradiction.  Hence

\[
                              q_{ab}=0\quad\hbox{or}\quad q_{bc}=0.
                                                               \tag{18}
\]

## 4. A single adjacent hole block is also impossible

Suppose first

\[
                              q_{ab}=0,\qquad q_{bc}\ne0. \tag{19}
\]

Equation (16) is now an equality between one nonzero completely
decomposable tensor and \(F_{bf}z_f\).  Uniqueness of tensor factor lines
gives

\[
 q_{bc}=e_2^{(b)}y_c,\qquad
 q_{bf}=\beta e_2^{(b)}e_1^{(f)},qquad
 F_{bf}=\gamma e_1^{(a)}y_ce_1^{(d)}e_1^{(e)},         \tag{20}
\]

with \(\beta\gamma\ne0\).

The \(F_{de}\) equation is

\[
                         q_{ac}q_{bf}+q_{af}q_{bc}
 =\lambda _2e_2^{(a)}e_2^{(b)}e_2^{(c)}e_2^{(f)}.      \tag{21}
\]

Projecting site \(f\) modulo \(\mathbb Fe_1^{(f)}\) shows that
\(y_c=\alpha e_2^{(c)}\) for some \(\alpha\ne0\).  Projecting site \(c\)
modulo \(\mathbb Fe_2^{(c)}\) then shows that
\(q_{ac}=x_ae_2^{(c)}\).  Equation (21) becomes

\[
 q_{af}=\frac{\lambda _2}{\alpha}e_2^{(a)}e_2^{(f)}
                    -\frac{\beta}{\alpha}x_ae_1^{(f)}. \tag{22}
\]

Write \(q_{be}=e_2^{(b)}E_e\).  The zero \(F_{cd}=0\) expands to

\[
                         \beta q_{ae}e_1^{(f)}+q_{af}E_e=0. \tag{23}
\]

Projecting (23) at \(f\) modulo \(e_1^{(f)}\), and using the nonzero
\(e_2^{(f)}\) term in (22), gives \(E_e=0\).  Equation (23) then gives

\[
                              q_{be}=q_{ae}=0.           \tag{24}
\]

There are two possibilities for \(q_{de}\).

If \(q_{de}=0\), expansion of the already known nonzero tensor \(F_{bf}\)
in (20) gives

\[
 q_{ad}q_{ce}=F_{bf}\ne0.                              \tag{25}
\]

Thus factor-line uniqueness makes \(q_{ad}\) pure on the
\(e_1^{(a)}e_1^{(d)}\) lines and \(q_{ce}\) pure on the
\(e_2^{(c)}e_1^{(e)}\) lines.  The target equation \(F_{bc}\) then says

\[
 q_{ad}q_{ef}=\lambda _1e_1^{(a)}e_1^{(d)}e_1^{(e)}e_1^{(f)}, \tag{26}
\]

so \(q_{ef}\) is pure on \(e_1^{(e)}e_1^{(f)}\).  But \(F_{bd}=0\)
reads

\[
                         q_{ac}q_{ef}+q_{af}q_{ce}=0.   \tag{27}
\]

Modulo \(e_1^{(f)}\), its second term is the nonzero tensor obtained from
the first term of (22) and \(q_{ce}\ne0\), while its first term vanishes.
This contradicts (27).

If \(q_{de}\ne0\), write \(q_{bd}=e_2^{(b)}D_d\).  The zero \(F_{ac}=0\)
and (24) give

\[
                         D_dq_{ef}+\beta q_{de}e_1^{(f)}=0. \tag{28}
\]

It follows that \(D_d\ne0\) and that \(q_{ef}\) has its \(f\)-factor on
the line \(\mathbb Fe_1^{(f)}\): apply the quotient of \(W_f\) by that
line to (28), then use injectivity of tensoring by \(D_d\ne0\).
Now project the target equation

\[
                         q_{ad}q_{ef}+q_{af}q_{de}
 =\lambda _1e_1^{(a)}e_1^{(d)}e_1^{(e)}e_1^{(f)}       \tag{29}
\]

through the same quotient.  The first term and the target vanish, whereas
the first term of (22) times \(q_{de}\ne0\) survives.  This is again a
contradiction.

Thus (19) is impossible.  The involution

\[
 a\leftrightarrow c,\qquad d\leftrightarrow e,
 \qquad 0\leftrightarrow1                              \tag{30}
\]

preserves (2), the target equations, and the set of five zeros (5), while
interchanging \(q_{ab}\) and \(q_{bc}\).  The opposite single-survivor
case is impossible as well.  Combining this with (18) yields

\[
                              q_{ab}=q_{bc}=0.           \tag{31}
\]

## 5. The remaining block \(q_{de}\) is killed by an exact syzygy

With (31), the \(F_{de}\) target has only one matching term:

\[
                         q_{ac}q_{bf}
 =\lambda _2e_2^{(a)}e_2^{(b)}e_2^{(c)}e_2^{(f)}.      \tag{32}

\]

Consequently, for nonzero \(\alpha,\beta\),

\[
 q_{ac}=\alpha e_2^{(a)}e_2^{(c)},\qquad
 q_{bf}=\beta e_2^{(b)}e_2^{(f)},qquad
 \alpha\beta=\lambda _2.                              \tag{33}
\]

The \(b\)-star identity (14) now reduces to \(q_{bf}F_{bf}=0\).
Tensoring by the nonzero \(q_{bf}\) is injective on its disjoint four-site
factor, so

\[
                              F_{bf}=0.                 \tag{34}
\]

For \(i\in\{d,e,f\}\), decompose the two cross blocks uniquely as

\[
\begin{aligned}
 q_{ai}&=e_1^{(a)}A_i+e_2^{(a)}U_i,\\
 q_{ci}&=e_0^{(c)}C_i+e_2^{(c)}V_i,
\end{aligned}
\qquad A_i,U_i,C_i,V_i\in W_i.                         \tag{35}
\]

The three four-site supports \(acde,acdf,acef\) carry respectively
\(F_{bf},F_{be},F_{bd}\), all zero by (5) and (34).  For every distinct
\(i,j\in\{d,e,f\}\), their common expansion is

\[
             q_{ac}q_{ij}+q_{ai}q_{cj}+q_{aj}q_{ci}=0. \tag{36}

\]

Comparing its \(e_1^{(a)}e_2^{(c)}\) and
\(e_2^{(a)}e_2^{(c)}\) coefficients gives

\[
\begin{aligned}
 A_iV_j+A_jV_i&=0,\\
 \alpha q_{ij}+U_iV_j+U_jV_i&=0.
\end{aligned}                                          \tag{37}
\]

No summand in (36) has been set to zero; equations (37) are literal
coordinate coefficients of the complete cancelling cofactor.

Take the \(e_1^{(a)}\)-coefficient of the \(F_{bc}\) target.  It must be

\[
 H:=A_dq_{ef}+A_eq_{df}+A_fq_{de}
       =\lambda _1e_1^{(d)}e_1^{(e)}e_1^{(f)}\ne0.     \tag{38}
\]

On the other hand, substitute the second line of (37) and regroup by the
site carrying \(U\):

\[
\begin{aligned}
 \alpha H={}&-U_d(A_eV_f+A_fV_e)
              -U_e(A_dV_f+A_fV_d)\\
             &-U_f(A_dV_e+A_eV_d)=0,                  \tag{39}
\end{aligned}
\]

where each parenthesis vanishes by the first line of (37).  Since
\(\alpha\ne0\), (39) contradicts (38).  Notice that \(q_{de}\) was never
assumed zero; it is one of the three arbitrary blocks eliminated through
(37)--(39).  This completes the proof of Theorem 1.1.

## 6. Exact audit

The standalone checker
[`verify_wedge_equality_hole_block_resolution.py`](../computations/verify_wedge_equality_hole_block_resolution.py)

* reconstructs every four-site cofactor and the full fifteen-term cubic;
* verifies the unique-\(b\)-edge identity (14) without imposing any hole
  block zero;
* audits the five typed-grid pairs and the symmetry (30);
* checks the normalized single-survivor projection ledger; and
* verifies the polynomial syzygy (39) exactly, before imposing its three
  zero relations.

The checker is supplementary.  The arbitrary-tensor implications,
including flattening ranks, quotient injectivity, and uniqueness of the
factor lines of a nonzero pure tensor, are proved above.
