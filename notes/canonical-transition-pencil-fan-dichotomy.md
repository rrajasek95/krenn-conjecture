# Canonical transition pencils: flat good fans are centre-dark

## 1. Outcome

The physical transition forms in
[the pair-cap connection](overlapping-pair-cap-bianchi-connection.md)
already give a sharp fan dichotomy, without choosing representatives
modulo a Hessian annihilator.

Fix a fan centre \(p\), a set \(F\subseteq B\setminus\{p\}\) of at least
three good neighbours, and one centre colour \(a\). For \(q\in F\), let

\[
 d_q^a(b)=A_{pq}(a,b),\qquad
 S_q(b)=S_{q,b}\in{\cal R}_1(B\setminus\{p,q\}).                  \tag{1}
\]

On a common complement, the canonical transition is

\[
 D_{qr}^a(b,c)=d_q^a(b)S_r(c)-d_r^a(c)S_q(b).                    \tag{2}
\]

If all transitions (2) vanish, the projective Čech equations have only
two possibilities for this fixed \(a\):

1. every direct row \(d_q^a\) is zero; or
2. exactly one direct row, at \(r_a\), is nonzero, and every other full
   star map \(S_q\) is supported only at \(r_a\).

The apparent third possibility—two or more nonzero direct rows—would make
the normalized stars \(S_q/d_q^a\) glue to one global linear form, forcing
each good \(q\)-star map to have rank at most one.

Apply this simultaneously to \(a=0,1,2\). All nonempty selector branches
must choose one common \(r_*\). In an exact ternary source that branch is
impossible: for \(q\ne r_*\), the whole block \(A_{pq}\) is zero and the
entire \(q\)-star is supported at \(r_*\). The same complementary matching
tensor would then have to be proportional to each of the three independent
pure tensors \(X_0,X_1,X_2\). Consequently:

\[
 \boxed{\quad
 D_{qr}^a(b,c)=0\ \hbox{for every }a,b,c,q,r
 \quad\Longrightarrow\quad
 A_{pq}=0\ \hbox{for every }q\in F.
 \quad}                                                          \tag{3}
\]

Thus a standard good fan gives the canonical alternative

\[
 \boxed{\text{some physical transition }D\ne0
 \quad\text{or}\quad
 \deg_{\rm block}(p)\le |B\setminus(\{p\}\cup F)|\le6.}           \tag{4}
\]

A full good fan cannot be flat.

The nonzero branch also has an exact coordinate-free description. Every
coefficient of \(D\) at a fourth site is the scalar curvature
\(AU-BF\); equivalently, it is a \(2\times2\) minor of a two-channel
matrix pencil. A nonzero minor gives an inverse two-flag selector and
guarantees a nonzero direct block. The latter supplies an explicit affine
cap line with a nonempty Zariski-open active subset. What it does not
supply is a zero of the vector-valued clean-cap error. An existing literal
eight-site cap model has nonzero transition curvature and a whole active,
target-compatible cap six-plane, yet every point of that plane is dirty.
At least one endpoint star map of each displayed pair has rank one, so it
is not a good-fan model. It therefore guards only the bare implication
from curvature, activity, and the displayed cap rows; it does not rule
out using good-fan injectivity together with the full transverse target
system of one exact source.

## 2. Coordinate-free transition data

Put

\[
 U=B\setminus\{p\},\qquad W_q=U\setminus\{q\},\qquad
 K_{qr}=U\setminus\{q,r\}.                                      \tag{5}
\]

Let \(E_q\simeq\mathbb C^3\) denote the colour-row space at \(q\).
For a fixed centre covector \(a\), contraction of the physical block
\(A_{pq}\) gives

\[
                         d_q^a:E_q\longrightarrow\mathbb C.       \tag{6}
\]

The physical \(q\)-star into \(W_q\) is

\[
                         S_q:E_q\longrightarrow{\cal R}_1(W_q).  \tag{7}
\]

Goodness of the pair \(\{p,q\}\) says, in particular, that (7) is
injective. Endpoint order is retained in both maps.

The transition is the bilinear map

\[
\begin{aligned}
 D_{qr}^a:E_q\times E_r&\longrightarrow{\cal R}_1(K_{qr}),\\
 D_{qr}^a(\beta,\gamma)
   &=d_q^a(\beta)\,S_r(\gamma)|_{K_{qr}}
     -d_r^a(\gamma)\,S_q(\beta)|_{K_{qr}}.                       \tag{8}
\end{aligned}
\]

In colour coordinates, (8) is exactly \(A_{pq}(a,b)S_{r,c}
-A_{pr}(a,c)S_{q,b}\). It is the physical \(D=At-By\) in the connection
note.

## 3. The scalar projective Čech lemma

The basic gluing statement does not need colours.

**Lemma 3.1 (projective deletion cover).** Let \(|F|\ge3\). For each
\(q\in F\), let \(a_q\in\mathbb C\) and
\(T_q\in{\cal R}_1(W_q)\), and assume

\[
              a_qT_r|_{K_{qr}}=a_rT_q|_{K_{qr}}
                         \qquad(q\ne r\text{ in }F).               \tag{9}
\]

Then:

1. if every \(a_q\ne0\), there is a unique
   \(H\in{\cal R}_1(U)\) with
   \[
                         T_q=a_qH|_{W_q}\qquad(q\in F);            \tag{10}
   \]
2. if \(a_q=0\) and \(a_r\ne0\), then \(T_q\) is supported only at \(r\);
3. if \(a_q=0\) and two distinct \(a_r,a_s\) are nonzero, then \(T_q=0\).

If every \(a_q=0\), equation (9) has no content.

**Proof.** In the first case, the forms \(H_q=T_q/a_q\) agree on every
pairwise overlap. They therefore glue site by site. To recover a component
at \(i\in W_q\), choose \(r\in F\setminus\{q,i\}\), possible because
\(|F|\ge3\); this also proves (10), including components at fan sites.

If \(a_q=0\) and \(a_r\ne0\), (9) gives
\(T_q|_{U\setminus\{q,r\}}=0\), so only its component at \(r\) may remain.
Applying this with two distinct active sites leaves no component.
\(\square\)

This is the exact gluing hypothesis and its sharp sparse guard. No
nonvanishing component of a star form is divided out; only the displayed
scalar \(a_q\) is normalized on its nonzero branch.

## 4. Full-row flatness on a good fan

Using every neighbour colour upgrades Lemma 3.1 from selected forms to
physical star maps.

**Theorem 4.1 (flat-row classification).** Fix a centre colour \(a\).
Assume \(|F|\ge3\), every map \(S_q\) in (7) is injective, and

\[
                         D_{qr}^a=0\qquad(q\ne r\text{ in }F).     \tag{11}
\]

Then the set

\[
                         I_a=\{q\in F:d_q^a\ne0\}                 \tag{12}
\]

has size at most one. If \(I_a=\{r_a\}\), then

\[
               \operatorname{supp}_s S_q\subseteq\{r_a\}
                         \qquad(q\in F\setminus\{r_a\}).           \tag{13}
\]

**Proof.** Suppose first that \(I_a\) contains distinct \(r,s\) and that
some \(q\notin I_a\). Choose \(\gamma_r,\gamma_s\) on which the respective
direct rows are nonzero. Equation (8), first with \(r\) and then with
\(s\), says for every \(\beta\in E_q\) that \(S_q(\beta)\) is supported
only at \(r\) and only at \(s\). Hence \(S_q=0\), contrary to injectivity.
Thus \(|I_a|\ge2\) would force \(I_a=F\).

Assume then that every \(d_q^a\ne0\). Choose
\(\beta_q\in E_q\) with \(d_q^a(\beta_q)=1\) and put
\(H_q=S_q(\beta_q)\). Equation (8) says the \(H_q\)'s agree on overlaps,
so Lemma 3.1 glues them to \(H\in{\cal R}_1(U)\). For arbitrary
\(\beta\in E_q\), a site \(i\in W_q\), and
\(r\in F\setminus\{q,i\}\), equation (8) with \(\beta_r\) gives

\[
                         S_q(\beta)_i=d_q^a(\beta)H_i.             \tag{14}
\]

Therefore \(S_q(\beta)=d_q^a(\beta)H|_{W_q}\). The image of \(S_q\) has
dimension at most one, again contradicting injectivity.

We have proved \(|I_a|\le1\). If \(I_a=\{r_a\}\), equation (8) with
\(q\ne r_a\) and a vector on which \(d_{r_a}^a\) is nonzero gives (13).
\(\square\)

The proof is a matrix-pencil rank argument expressed on a deletion cover.
It allows zero blocks, arbitrary complex cancellation, and completely
asymmetric endpoint matrices.

## 5. Exact ternary rows kill the one-sided selector branch

We first isolate the target obstruction used below.

**Lemma 5.1 (no one-neighbour star).** Let \(|B|\ge4\) and
\(H_B(A)=\Delta_{B,3}\). No site \(q\) has all its incident blocks zero
except possibly \(A_{qr}\) for one \(r\ne q\).

**Proof.** Delete \(q,r\) and put \(Z=A|_{B\setminus\{q,r\}}\).
If \(R_{q,c}\in V_r\) is the colour-\(c\) row of the sole block, the
one-site target equation is

\[
                  R_{q,c}\,Z^{[m-1]}
                    =e_{r,c}\otimes X_c^{B\setminus\{q,r\}}
                         \qquad(c=0,1,2).                          \tag{15}
\]

Every term using an edge of \(A|_{B\setminus\{q\}}\) incident with \(r\)
collides with \(R_{q,c}\), which justifies the common factor
\(Z^{[m-1]}\). The right sides are nonzero, so this one tensor would have
to be proportional to \(X_c^{B\setminus\{q,r\}}\) for all three \(c\).
Those pure tensors are independent. \(\square\)

**Theorem 5.2 (flat exact fan is centre-dark).** Let \(A\) be an exact
ternary source, let \(|F|\ge3\), and suppose every \(\{p,q\}\), \(q\in F\),
is good. If

\[
                  D_{qr}^a=0
      \qquad(a=0,1,2,\ q\ne r\text{ in }F),                       \tag{16}
\]

then

\[
                              A_{pq}=0\qquad(q\in F).               \tag{17}
\]

**Proof.** Apply Theorem 4.1 for each \(a\). If some \(I_a\) is nonempty,
write \(I_a=\{r_a\}\). Two nonempty sets cannot choose distinct sites:
if \(r_a\ne r_e\), choose
\(q\in F\setminus\{r_a,r_e\}\); then (13) supports the injective map
\(S_q\) at both distinct singleton sites, forcing \(S_q=0\).

Thus all nonempty \(I_a\)'s choose one common \(r_*\). For
\(q\in F\setminus\{r_*\}\), every row \(d_q^a\) is zero, hence
\(A_{pq}=0\), while (13), for any active \(a\), supports the entire
\(q\)-star into \(W_q\) only at \(r_*\). The full \(q\)-star is therefore
supported only at \(r_*\), contradicting Lemma 5.1.

No \(I_a\) is nonempty. Thus every row of every \(A_{pq}\), \(q\in F\),
is zero. \(\square\)

If \(F\) is the standard good fan, \(|F|\ge |B|-7\), equation (17) says
that the centre has at most six nonzero incident blocks. If \(F=U\), it
says the entire \(p\)-star is zero, contradicting the one-site target
rows. This proves (3)–(4).

## 6. Nonzero transition equals a rank-two curvature pencil

The scalar curvature is not additional information appended to \(D\);
it is precisely a coordinate of \(D\).

Fix a fourth site \(s\notin\{p,q,r\}\) and a covector
\(\delta\in V_s^*\). Define the two-channel map

\[
\begin{aligned}
 \Phi_q^{a;s,\delta}:E_q&\longrightarrow\mathbb C^2,\\
 \Phi_q^{a;s,\delta}(\beta)
   &=\left(d_q^a(\beta),\
       \langle\beta\otimes\delta,A_{qs}\rangle\right).             \tag{18}
\end{aligned}
\]

**Lemma 6.1 (curvature-minor identity).** For
\(\beta\in E_q,\gamma\in E_r\),

\[
 \left\langle\delta,\,
       (D_{qr}^a(\beta,\gamma))_s\right\rangle
   =\det\!\left(
       \Phi_q^{a;s,\delta}(\beta),\
       \Phi_r^{a;s,\delta}(\gamma)\right).                         \tag{19}
\]

For coordinate covectors \(a,b,c,d\), the right side is

\[
 A_{pq}(a,b)A_{rs}(c,d)
    -A_{pr}(a,c)A_{qs}(b,d)=AU-BF.                                \tag{20}
\]

**Proof.** Expand the component at \(s\) of (8). \(\square\)

Consequently \(D_{qr}^a\ne0\) if and only if some physical two-channel
pencil in (18) has rank two across a \(q\)-flag and an \(r\)-flag. If
\(v,w\in\mathbb C^2\) are the two columns and
\(\kappa=\det(v,w)\ne0\), the dual forms

\[
                \ell_v(x)=\frac{\det(x,w)}{\kappa},\qquad
                \ell_w(x)=\frac{\det(v,x)}{\kappa}                \tag{21}
\]

satisfy

\[
 \ell_v(v)=1,\quad\ell_v(w)=0,\qquad
 \ell_w(v)=0,\quad\ell_w(w)=1.                                   \tag{22}
\]

This is a canonical inverse two-flag selector. It lives in the
two-dimensional channel \(\mathbb Ce_{p,a}^*\oplus
\mathbb Ce_{s,\delta}^*\). It becomes a one-sided source selector only if
one proves that the corresponding channel covector annihilates the other
incident blocks as well. That global kernel statement is not contained in
one nonzero minor.

Equation (19) also identifies the first Bianchi relation with the ordinary
alternating compatibility among these physical minors. No annihilator
quotient or representative occurs.

## 7. Every nonzero transition supplies a generically active cap line

A nonzero determinant (20) has a nonzero entry in its first row. After
possibly replacing \(q\) by \(r\), fix

\[
                         A_{pq}(a,b)\ne0.                          \tag{23}
\]

Let

\[
 K_0=e_{p,a}^*\otimes e_{q,b}^*,\qquad
 K_\lambda=K_0+\lambda\sum_{i=0}^2
                  e_{p,i}^*\otimes e_{q,i}^*.                    \tag{24}
\]

For the pair cap at \(p,q\),

\[
\begin{aligned}
 \kappa_i(K_\lambda)
   &=\delta_{a,i}\delta_{b,i}+\lambda,\\
 s(K_\lambda)
   &=A_{pq}(a,b)+\lambda\sum_iA_{pq}(i,i).                         \tag{25}
\end{aligned}
\]

Thus, outside at most three scalar values of \(\lambda\),

\[
                 s(K_\lambda)\kappa_0(K_\lambda)
                    \kappa_1(K_\lambda)\kappa_2(K_\lambda)\ne0.   \tag{26}
\]

For an exact source, every such point has the correct capped target
\(\sum_i\kappa_i(K_\lambda)X_i\). Hence (24) is an explicit clean-cap
**candidate line**, with full physical provenance and generic activity.

Cleanliness is the remaining equation

\[
                         {\cal E}_{p,q}(K_\lambda)=0.              \tag{27}
\]

Its left side is a tensor-valued polynomial in \(\lambda\), not one scalar
polynomial. Nonzero curvature does not make its coordinates share a root.
The normalized diagonal rows establish activity in (26), but do not erase
the higher cap cumulants.

At the exact \(K_4\) source, a colour-\(0\) one-factor gives
\(A=U=1\), \(B=F=0\), hence curvature \(1\). The line (24) is active for
generic \(\lambda\), and here \(h=1\), so the clean error has no
higher-cumulant terms and vanishes automatically. Thus \(K_4\) audits the
minor and active-line statements; it is not a negative guard. The
vector-valued common-root gap starts at the genuine higher-cumulant
boundaries.

## 8. A literal source-variable guard for the nonzero branch

The local eight-site model in
[the active dirty cap-plane note](n8-rank-one-clean-cap-local-torus-obstruction.md)
shows that the last warning is real while retaining literal common-edge
source data and exact capped target rows on the displayed cap space.

Use its sites \(p,q,0,\ldots,5\). The relevant blocks are

\[
 A_{pq}=3e_{p,0}e_{q,0},\qquad A_{p0}=0,\qquad
 A_{01}(1,0)=-1.                                                  \tag{28}
\]

Take the transition from the \(pq\) chart to the \(p0\) chart, with
colours

\[
                         a=0,\quad b=0,\quad c=1.
\]

At the fourth site \(1\), colour \(d=0\), equation (20) gives

\[
 \kappa
 =A_{pq}(0,0)A_{01}(1,0)
   -A_{p0}(0,1)A_{q1}(0,0)
 =3(-1)-0=-3.                                                     \tag{29}
\]

So the canonical physical transition is nonzero.

Nevertheless, on the seven-dimensional cap space

\[
                         {\cal L}=\{K:K_{00}=K_{11}=K_{22}\},
\]

every point with common diagonal value \(\lambda\ne0\) is active and has
the exact target-compatible contraction

\[
 K\mathbin{\lrcorner}H_8(A)
   =K\mathbin{\lrcorner}\Delta_{8,3}
   =\lambda\Delta_{6,3},                                         \tag{30}
\]

while

\[
 {\cal E}_{p,q}(K)
   =9\lambda^3\bigl(e_{100100}+6e_{201102}\bigr)\ne0.             \tag{31}
\]

This is a source-level connection and cap countermodel, not a formal
assignment of \(D\). It proves that nonzero transition curvature,
activity, and the three normalized diagonal cap rows on a large linear
family do not force cleanliness.

Its full eight-site tensor is not \(\Delta_{8,3}\) outside the cap space
\({\cal L}\). Moreover, (7) of the cited note makes the star at \(p\) of
each displayed pair factor through its colour-zero row, hence have rank
one; the displayed pairs are not good. Thus the model does not refute a
theorem using good-fan injectivity or every transverse target row of one
exact source. Those two inputs, coupled across the fan, remain available
mechanisms.

## 9. Corrected canonical gate and audit

The arbitrary homogeneous lift complex can be bypassed. On a good fan,
the canonical source data now give:

\[
\boxed{
\begin{array}{c}
\text{a centre supported on at most six exceptional neighbours;}\\
\text{or a nonzero physical }2\times2\text{ curvature minor,}\\
\text{an inverse two-flag selector, and a generically active cap line.}
\end{array}}                                                     \tag{32}
\]

To close the second branch, one must use the remaining exact-source data,
including good-fan injectivity and the full normalized diagonal and mixed
rows, to prove either:

1. one inverse channel selector in (21) annihilates all but the permitted
   incident blocks, giving the one-sided selector descent; or
2. the active open subset of line (24), possibly coupled to adjacent pair
   lines by the four-site identity, meets the clean-cap variety.

The first option is a kernel/factorization theorem for the physical
two-channel pencils. The second is a saturated common-edge theorem for the
tensor polynomials (27). Neither is a homogeneous-overlap acyclicity
claim.

No new checker is needed. Lemmas 3.1–6.1 are coefficientwise linear
identities. The exact dirty guard (28)–(31) is already audited by
[verify_n8_rank_one_clean_cap_local_torus_obstruction.py](../computations/verify_n8_rank_one_clean_cap_local_torus_obstruction.py),
including all \(3^6\) capped coefficients and the nonzero clean error.
