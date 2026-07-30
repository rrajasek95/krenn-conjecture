# Hamming-one full-nine rows force a fixed-label second-polar lift

## 1. Outcome

The pure-slice routing theorem can be extended one Hamming layer without
cancelling a common matching power.  Work on \(W\), \(|W|=2h\), \(h\ge2\),
with the literal nine rows

\[
 a_{ij}q^{[h]}+p_is_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\le i,j\le2.                                      \tag{1}
\]

Fix a physical colour \(d\).  Let \(I\) and \(J\) be the fixed-label
channels having a nonzero \(d\)-component in the two endpoint stars, put

\[
 F_d=[q^{[h]}]_{d^W},\qquad M_d=E_{dd}-F_da,
\]

and compress the direct matrix to \(I^c\times J^c\).

**Theorem 1.1 (Hamming-one compression and second-polar trichotomy).**
If

\[
                              a_{I^c,J^c}\ne0,                \tag{2}
\]

then every one-defect hafnian coefficient is zero:

\[
 [q^{[h]}]_{(e\text{ at }x,\ d\text{ off }x)}=0
 \qquad(x\in W,\ e\ne d).                                    \tag{3}
\]

Equivalently, the literal cohafnian covector at every residual site is

\[
 \sum_{e=0}^2\sum_{y\ne x}
   q_{xy}(e,d)\operatorname{haf}
     (Q_d[W\setminus\{x,y\}])e_e
                         =F_de_d.                            \tag{4}
\]

Moreover, for every \(x\), at least one of the following holds:

\[
 \boxed{
 \operatorname{rank}P_x\le |I|,\quad
 \operatorname{rank}S_x\le |J|,\quad\text{or}\quad
 \Gamma_x(e)=\delta_{ed}M_d\ \text{for every }e.}             \tag{5}
\]

Here \(\Gamma_x\) is the fixed-label second polar of the *same* off-\(x\)
quadratic, defined explicitly in Section 3.  Thus the residual pure-slice
exit is no longer an unspecified deconcentrated packet.  Either:

1. the support of \(a\) lies in the channel cross
   \((I\times[3])\cup([3]\times J)\); or
2. every residual site belongs to the union of three classes: a low-rank
   \(P\)-spoke, a low-rank \(S\)-spoke, or a site where the literal second
   polar carries \(M_d\) only in physical label \(d\).

A complementary incident-curvature lemma proves that every off-diagonal
entry of \(a\) forces a singular residual spoke at both endpoints.  If all
three columns, or all three rows, are non-coordinate in the precise sense
of Section 6, the corresponding endpoint has at least two singular spokes.

These statements close every residual model with a nonzero quotient
compression, a nonzero one-defect hafnian, and no low-rank or fixed-label
second-polar lift.  They do not yet produce an active clean cap: simultaneous
\(\Gamma\)-lifts and the low-rank spoke cover must still be compared through
the nonflat second chart.

## 2. Fixed-label support at Hamming distance one

Say \(i\in I\) when some local coefficient \(p_{i,x}(e_d)\) is nonzero,
and define \(J\) from the \(s\)-star analogously.  At the pure word,

\[
                         M_d=E_{dd}-F_da
\]

is exactly the scalar response matrix, so

\[
                         \operatorname{supp}M_d\subseteq I\times J.
                                                                    \tag{6}
\]

For \(x\in W\) and a physical label \(e\), let \(\omega_{x,e}\) be \(e\)
at \(x\) and \(d\) elsewhere.  In a response matching at this word, if the
\(p\)-star does not occupy \(x\), its label belongs to \(I\); if the
\(s\)-star does not occupy \(x\), its label belongs to \(J\).  At most one
of them can occupy \(x\).  Consequently its coefficient matrix
\(M_{x,e}\) satisfies

\[
 \operatorname{supp}M_{x,e}
       \subseteq([3]\times J)\cup(I\times[3]).                 \tag{7}
\]

For \(e\ne d\), the target word is mixed and (1) gives

\[
                         M_{x,e}=-F_{x,e}a,\qquad
 F_{x,e}=[q^{[h]}]_{\omega_{x,e}}.                            \tag{8}
\]

Projecting (7)--(8) to \(I^c\times J^c\) proves the exact compression
identity

\[
                         \boxed{F_{x,e}a_{I^c,J^c}=0.}         \tag{9}
\]

Hypothesis (2) therefore proves (3).

## 3. Exact Taylor expansion before the common power

Fix \(x,e\) and scalarize all off-\(x\) sites at \(d\).  In the resulting
site-square-zero algebra write

\[
\begin{aligned}
 q&=q_0+z_x\ell_e,\\
 p_i&=\bar p_i+P_{x,i}(e)z_x,\\
 s_j&=\bar s_j+S_{x,j}(e)z_x,
\end{aligned}                                                \tag{10}
\]

where

\[
                         \ell_e=\sum_{y\ne x}q_{xy}(e,d)z_y.
\]

Put \(A=q_0^{[h-1]}\) and \(B=q_0^{[h-2]}\).  The quadratic \(q_0\)
lives on only \(2h-1\) sites, so \(q_0^{[h]}=0\), while
\((z_x\ell_e)^{[2]}=0\).  The divided-power binomial identity gives, with
coefficient one,

\[
\begin{aligned}
 (q_0+z_x\ell_e)^{[h]}&=z_x\ell_e A,\\
 (q_0+z_x\ell_e)^{[h-1]}&=A+z_x\ell_e B.                     \tag{11}
\end{aligned}
\]

There are no hidden factorials.  Expanding the response, the term
\(\bar p_i\bar s_jA\) has top degree on only \(2h-1\) sites and vanishes;
every term containing two copies of \(z_x\) also vanishes.  The three
survivors are

\[
 z_x\left(
 P_{x,i}(e)\bar s_jA+
 S_{x,j}(e)\bar p_iA+
 \ell_e\bar p_i\bar s_jB\right).                             \tag{12}
\]

Take the top \(d^{W\setminus x}\)-coefficient and define

\[
\begin{aligned}
 h_j&=[\bar s_jA]_{d^{W\setminus x}},\\
 g_i&=[\bar p_iA]_{d^{W\setminus x}},\\
 \Gamma_{ij}(e)&=[\ell_e\bar p_i\bar s_jB]_{d^{W\setminus x}}.
\end{aligned}                                                \tag{13}
\]

Then

\[
                  \boxed{
                  M_{x,e}=P_x(e)h^{\mathsf T}
                         +gS_x(e)^{\mathsf T}+\Gamma(e).}      \tag{14}
\]

In this fixed scalarization,

\[
 \operatorname{supp}g\subseteq I,\qquad
 \operatorname{supp}h\subseteq J,\qquad
 \operatorname{supp}\Gamma(e)\subseteq I\times J.             \tag{15}
\]

Equation (14) is the source-relative first-slice identity retained before
any multiplication or cancellation by \(A\).

## 4. Proof of the sitewise trichotomy

Assume (2).  Equations (8)--(9) make \(M_{x,e}=0\) for every \(e\ne d\).
Suppose \(h\ne0\), and choose \(j_0\in J\) with \(h_{j_0}\ne0\).  For
\(i\notin I\), (14)--(15) give

\[
                         0=(M_{x,e})_{ij_0}
                           =P_{x,i}(e)h_{j_0}\qquad(e\ne d).
\]

Also \(P_{x,i}(d)=0\) by the definition of \(I\).  Thus the complete local
row \(p_{i,x}\) vanishes for every \(i\notin I\), and

\[
                         \operatorname{rank}P_x\le |I|.       \tag{16}
\]

The transposed argument shows that \(g\ne0\) implies
\(\operatorname{rank}S_x\le|J|\).  If both ranks exceed the displayed
thresholds, then \(h=g=0\), so (14) gives

\[
                         \Gamma(e)=0\quad(e\ne d).
\]

At \(e=d\), formula (14) itself gives \(\Gamma(d)=M_d\); no assertion that
\(M_{x,d}\) vanishes was used.  This proves (5), including its \(e=d\)
boundary.

Finally, the first identity in (11) gives

\[
 F_{x,e}=\sum_{y\ne x}q_{xy}(e,d)
             \operatorname{haf}(Q_d[W\setminus\{x,y\}]).
\]

Together with \(F_{x,d}=F_d\), equation (3) is exactly (4).

## 5. Pure-slice applications

Compressing (6) gives, when \(F_d\ne0\),

\[
              a_{I^c,J^c}
                  =F_d^{-1}(E_{dd})_{I^c,J^c}.                \tag{17}
\]

Thus (2) is automatic when \(d\notin I\) and \(d\notin J\).  When
\(F_d=0\), equation (6) is \(M_d=E_{dd}\) and forces
\(d\in I\cap J\).

Two routed exits now have exact forms.

* **Aligned hafnian-zero singleton.**  If
  \(I=J=\{d\}\), \(F_d=0\), and \(a_{\alpha\beta}\ne0\) with
  \(\alpha,\beta\ne d\), then (2) holds, (4) is the zero covector, and
  every site obeys

  \[
   \operatorname{rank}P_x\le1,\quad
   \operatorname{rank}S_x\le1,\quad\text{or}\quad
   \Gamma_x(e)=\delta_{ed}E_{dd}.                             \tag{18}
  \]

* **Curvature-routed singleton away from \(d\).**  If
  \(I=\{\alpha\}\), \(J=\{\beta\}\), \(\alpha\ne\beta\),
  \(F_d\ne0\), \(a_{\alpha\beta}\ne0\), and
  \(d\notin\{\alpha,\beta\}\), write
  \(M_d=mE_{\alpha\beta}\), where
  \(m=-F_da_{\alpha\beta}\ne0\).  Then

  \[
             a=F_d^{-1}(E_{dd}-mE_{\alpha\beta}),             \tag{19}
  \]

  equation (4) is \(F_de_d\), and every site obeys (18) with thresholds
  one and \(E_{dd}\) replaced by \(mE_{\alpha\beta}\).

In general, either \(a_{I^c,J^c}=0\), equivalently

\[
               \operatorname{supp}a
                 \subseteq(I\times[3])\cup([3]\times J),      \tag{20}
\]

or the complete packet (3)--(5) fires.

## 6. Incident curvature forces singular spokes

The following independent consequence uses the proved
[two-star pure-response lemma](centered-rank-one-two-star-pure-response-obstruction.md#2-a-two-star-pure-response-lemma).

**Lemma 6.1 (incident-curvature singular spoke).**  Let the deleted
\(P\)-star be

\[
             \lambda\longmapsto P(\lambda)=\sum_i\lambda_ip_i
\]

Fix a column \(c=a_{*j}\).  If \(c\) is not a nonzero multiple of \(e_j\),
with \(c=0\) included, then some residual local block \(P_x\) has rank at
most two.  If it is the unique singular \(P\)-block, then

\[
                         e_j^{(x)}\in\operatorname{im}P_x.     \tag{21}
\]

Consequently, if all three columns are of this bad type, at least two
\(P\)-blocks are singular.  The transposed statement holds for the rows of
\(a\) and the \(S\)-blocks.

**Proof.**  If \(P\) is not injective, every local map \(P_x\) has rank at
most two, and the first conclusion is immediate.  In that branch there
cannot be a unique singular local block because \(|W|\ge4\).  We may
therefore assume \(P\) is injective.

Choose independent \(\lambda,\mu\in c^\perp\) with
\(\lambda_j\ne0\) and \(\mu_j=0\).  Such a pair exists unless \(c\) is a
nonzero multiple of \(e_j\); for \(c=0\), take
\(\lambda=e_j\) and any \(e_k\), \(k\ne j\).  With
\(G=s_jq^{[h-1]}\), the fixed-column combinations of (1) are

\[
 P(\nu)G=\nu_jX_j-(\nu^{\mathsf T}c)q^{[h]}.                  \tag{22}
\]

After scaling \(\lambda\),

\[
                         P(\lambda)G=X_j,\qquad P(\mu)G=0.    \tag{23}
\]

The two-star pure-response lemma gives a site \(x\) where
\(P_x\lambda,P_x\mu\) are dependent.  The restriction of \(P_x\) to their
two-dimensional coefficient plane has rank at most one; the remaining
coefficient direction adds at most one, proving
\(\operatorname{rank}P_x\le2\).

If \(x\) is the unique singular block, every other local pair is
independent.  The singleton clause of the same lemma gives (21).  If all
three columns are bad but only one \(P\)-block were singular, (21) for
\(j=0,1,2\) would put all three coordinate axes in its image, contradicting
rank at most two.  This proves the column statement; transposition proves
the row statement.  \(\square\)

Any off-diagonal \(a_{\alpha\beta}\ne0\) makes column \(\beta\) and row
\(\alpha\) bad, so it forces at least one singular spoke at each endpoint.
More generally, any curvature-routed singleton with
\(I=\{\alpha\}\), \(J=\{\beta\}\), \(\alpha\ne\beta\), \(F_d\ne0\), and
\(M_d=mE_{\alpha\beta}\), \(m\ne0\), has the identity
\(a=F_d^{-1}(E_{dd}-mE_{\alpha\beta})\), without requiring
\(d\notin\{\alpha,\beta\}\).  If \(d=\beta\), all three columns are bad
and there are at least two singular \(P\)-spokes; if \(d=\alpha\), the
transposed conclusion gives at least two singular \(S\)-spokes.  If
\(d\notin\{\alpha,\beta\}\), there is at least one at each endpoint and
the Hamming-one packet also fires.
