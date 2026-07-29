# The sharp centered rank-one mask needs nonminimal overlap cancellation

## 1. Outcome

Consider the sharp rank-one local mask from Section 5.2 of
[the centered rank tradeoff](centered-low-degree-rank-tradeoff.md).  In
the normalized notation there, `r,u` are the deleted endpoints, `x,y` are
internal sites,

\[
 A_{r\mid x}=I_3,qquad A_{x\mid y}=e_0e_0^{\mathsf T},              \tag{1}
\]

and at `y`

\[
 A_{r\mid y}=(e_1+e_2)\otimes e_0,qquad
 A_{u\mid y}=-(e_1+e_2)\otimes e_0.                  \tag{2}
\]

The second deleted star at `x` has rows

\[
                         e_0,\qquad e_0+e_2,\qquad e_0+e_1.      \tag{3}
\]

This note asks whether this **specific sharp mask** can extend through the
complete overlap equations with `y` exposed.  It proves three exact facts.

1. The 27 equations compress to four common cofactors on the two-plane
   `L=span{f=e_0,h=e_1-e_2}`.
2. The compressed packet has an exact five-site common-`q` relaxation at
   `N=8`; raw cofactor multiplication is therefore insufficient.
3. No minimal three-private-edge coordinate packet has the shared-star
   provenance required by an actual source, even modulo the annihilator of
   `q`.

Thus the recorded sharp mask is excluded on the entire minimal private
coordinate stratum.  The surviving rank-one gate must use extra cells,
non-coordinate or multisite endpoint forms, nonzero mixed cofactors killed
by all three `y`-stars, or genuine cancellation among multiple origins.
This is not yet an elimination of every rank-one spoke mask.

## 2. The exact four-cofactor compression

Put

\[
                         Y=B\setminus\{r,u,y\},qquad |Y|=2m-3,    \tag{4}
\]

and let `q` be the quadratic internal to `Y`.  Let `p_l,s_k` be the
restrictions to `Y` of the `r,u` stars contracted by `l,k in L`, and let
`t_e` be colour row `e` of the `y`-star into `Y`.  Define

\[
 F_{lk}=(l^{\mathsf T}A_{r\mid u}k)q^{[m-2]}
                    +p_ls_kq^{[m-3]}.                  \tag{5}
\]

**Theorem 2.1 (contracted overlap packet).**  The complete 27 equations
imply

\[
 \boxed{
                         t_eF_{lk}=l_ek_eX_e^Y
       \quad(l,k\in\{f,h\},\ 0\le e\le2).}             \tag{6}
\]

Equivalently,

\[
\begin{array}{c|ccc}
 &t_0&t_1&t_2\\ \hline
F_{ff}&X_0&0&0\\
F_{fh}&0&0&0\\
F_{hf}&0&0&0\\
F_{hh}&0&X_1&X_2.
\end{array}                                             \tag{7}
\]

**Proof.**  The common-complement triple equation is

\[
\begin{aligned}
 &(A_{r\mid u}(c,d)t_e+A_{r\mid y}(c,e)s_d
          +A_{u\mid y}(d,e)p_c)q^{[m-2]}\\
 &\hspace{35mm}+p_cs_dt_e q^{[m-3]}
       =\delta_{c=d=e}X_c^Y.                            \tag{8}
\end{aligned}
\]

Both `f,h` lie in the left kernels of the two blocks in (2).  Contracting
(8) by `l_c k_d` therefore kills exactly its second and third direct-star
terms and factors the remaining terms as `t_e F_lk`.  The target contracts
to `l_e k_e X_e`, proving (6).

At the distinguished site `x`, equations (1)--(3) give

\[
\begin{aligned}
 &p_{f,x}=s_{f,x}=f,\qquad p_{h,x}=h,\qquad s_{h,x}=-h,\\
 &t_{0,x}=f,\qquad t_{1,x}=t_{2,x}=0.                  \tag{9}
\end{aligned}
\]

These shared local preimages are the information absent from a raw table
of four arbitrary cofactors.

## 3. An exact common-quadratic relaxation

At `N=8`, label

\[
                         Y=\{x,z_1,z_2,a,b\}=\{0,1,2,3,4\}.        \tag{10}
\]

Write `ij_cc=e_c^(i)e_c^(j)` and set

\[
 q=34_{00}+24_{11}+13_{22},                            \tag{11}
\]

\[
 Z_{ff}=12_{00},\qquad Z_{fh}=Z_{hf}=0,qquad
 Z_{hh}=03_{11}+04_{22},                               \tag{12}
\]

\[
 t_0=e_0^{(0)},\qquad t_1=e_1^{(1)},\qquad
 t_2=e_2^{(2)}.                                        \tag{13}
\]

Then, exactly,

\[
 Z_{ff}q=X_0^{Y\setminus\{0\}},qquad
 Z_{hh}q=X_1^{Y\setminus\{1\}}+X_2^{Y\setminus\{2\}},           \tag{14}
\]

and every wrong product vanishes by a shared physical site.  Consequently
`F_lk=Z_lk q` satisfies all twelve equations (7).

This model has one literal common quadratic and no cancellation or
factorial ambiguity.  It is **not** a source or pair-chart counterexample:
at `m=4`, put
\(\beta_{lk}=l^{\mathsf T}A_{r\mid u}k\).  Actual provenance would require
the congruences

\[
 Z_{lk}-{\beta_{lk}\over2}q-p_ls_k\in\operatorname{Ann}(q)
                         \qquad(l,k\in\{f,h\}).                    \tag{15}
\]

for the same four endpoint forms with the fixed `x`-components (9).  The
displayed representatives already fail literal equality: every `xj` block
of `p_hs_h` has its `x`-image in `C h`, whereas the two blocks
`03_11,04_22` have independent `e_1,e_2` factors at `x`.  That observation
alone does not exclude an annihilator correction; Theorem 4.1 does so for
the full minimal private-coordinate class by comparing the products with
`q` directly.

## 4. The full minimal private-coordinate obstruction

The preceding example is one member of a natural sharp class.  We now
exclude the class without choosing representatives modulo `Ann(q)`.

Let `Y` have five sites and fix distinct private ports

\[
                         v_0=x,qquad v_1,qquad v_2.    \tag{16}
\]

For each colour `c`, choose nonzero coordinate cells

\[
                         Q_c=\mu_cE^c_{T_c},qquad
                         Z_c=\nu_cE^c_{D_c},            \tag{17}
\]

where `D_c,T_c` are two-sets partitioning `Y\setminus{v_c}`.  Assume the
privacy incidence

\[
                         D_c\cap T_d\ne\varnothing
                         \qquad(c\ne d),                \tag{18}
\]

so `Z_cQ_d=0` for `c!=d`, while `Z_cQ_c` is the nonzero pure cofactor
missing `v_c`.  Put

\[
 q=Q_0+Q_1+Q_2,qquad
 R_{ff}=Z_0q,\qquad R_{fh}=R_{hf}=0,\qquad
 R_{hh}=(Z_1+Z_2)q.                                    \tag{19}
\]

**Theorem 4.1 (no minimal private shared-star lift).**  There are no
linear forms `p_f,p_h,s_f,s_h` with the `x`-components (9), and no scalars
`beta_lk`, such that

\[
                         R_{lk}=\beta_{lk}q^{[2]}+p_ls_kq
                         \qquad(l,k\in\{f,h\}).         \tag{20}
\]

The conclusion permits arbitrary changes `Z_lk -> Z_lk+H_lk` with
`H_lk q=0`, because its proof uses only the products `R_lk`.  It also
permits cancellation by the direct coefficients `beta_lk`; those scalars
are **not** forced to vanish.

For the proof, orient every block with its first named endpoint first and
write

\[
 K_{lk,i\mid j}=p_{l,i}\otimes s_{k,j}
                    +s_{k,i}\otimes p_{l,j}.            \tag{20a}
\]

### 4.1 A colour-one or colour-two cap through `x`

Suppose `x in D_c` for `c=1` or `2`, and write `D_c={x,j}`.  Compare the
all-colour-`c` word on `Y\setminus{v_c}` with the word obtained by changing
only the colour at `x` to the other member `bar c` of `{1,2}`.

In both words, coloured divisibility and (18) leave `Q_c` as the unique
cell of `q` which can occur in the `p_hs_hq` term.  No product in `q^[2]`
has the required colours.  If `eta_1=1,eta_2=-1`, the two relevant
coefficients of the ordered block

\[
 K_{hh,xj}=p_{h,x}\otimes s_{h,j}+s_{h,x}\otimes p_{h,j}           \tag{21}
\]

are

\[
 \eta_c(s_{h,j,c}-p_{h,j,c}),qquad
 \eta_{\bar c}(s_{h,j,c}-p_{h,j,c}),                  \tag{22}
\]

which are exact negatives.  The first word has the nonzero target
coefficient `mu_c nu_c`; the colour-swapped word has coefficient zero.
This is impossible.

### 4.2 The two residual incidence designs

It remains to assume \(x\notin D_1\cup D_2\).  Then
\(x\in T_1\cap T_2\).  The privacy conditions force, up to swapping two residual sites
`a,b`,

\[
\begin{array}{c|cc}
c&D_c&T_c\\ \hline
0&\{a,b\}&\{v_1,v_2\}\\
1&\{v_2,b\}&\{x,a\}\\
2&\{v_1,a\}&\{x,b\}.
\end{array}                                             \tag{23}
\]

On the four-site support `Y\setminus{b}`, the mixed equation in (20) has
only the channels

\[
                         K_{lk,xa}Q_0,qquad
                         K_{lk,v_1v_2}Q_1,qquad
                         \beta_{lk}Q_0Q_1.              \tag{24}
\]

Coefficient comparison permits `K_fh,xa` only on the line
\(\mathbb C(e_1\otimes e_1)\).  But

\[
 K_{fh,xa}=e_0\otimes s_{h,a}-h\otimes p_{f,a}
              \in L\otimes V_a,qquad e_1\notin L.     \tag{25}
\]

Hence it is zero, so `s_h,a=p_f,a=0`.  The reversed mixed block

\[
                         K_{hf,xa}=h\otimes s_{f,a}
                                      +e_0\otimes p_{h,a}          \tag{26}
\]

similarly gives `s_f,a=p_h,a=0`.  Repeating the argument on
`Y\setminus{a}` with colour two gives

\[
                         s_{h,b}=p_{f,b}=s_{f,b}=p_{h,b}=0.         \tag{27}
\]

Thus `K_ff,ab=0`.  On the support `Y\setminus{x}`, however, the only
channel capable of producing the required nonzero `R_ff=Z_0Q_0` is
`K_ff,abQ_0`.  This contradiction proves Theorem 4.1.

There are 24 labelled incidence designs satisfying (18): 22 enter Section
4.1 and the remaining two are the two `a,b` orderings of (23).

## 5. Exact remaining gate

The common-`q` relaxation in Section 3 shows that even the full contracted
response table and one shared quadratic are insufficient.  Theorem 4.1
adds the shared-star provenance and closes every minimal monomial/private
incidence pattern.  A surviving extension of the sharp mask must therefore
have at least one of:

1. extra cells in `q` or in a cap representative;
2. non-coordinate or multisite private forms;
3. nonzero mixed cofactors in the common annihilator of all `t_e`; or
4. cancellation of a required word across multiple physical origins.

The subsequent
[two-star pure-response theorem](centered-rank-one-two-star-pure-response-obstruction.md)
does apply to all of these extensions.  Its two independent colour slices
show that every realization of this sharp mask has at least two additional
singular blocks incident with `y`; at \(N=8\), this forces
\(\deg_R(y)\le2\).  It does not eliminate the cancellation-rich extension
at higher order or classify other rank-one local masks, which may have
different common kernel planes and require their own orbit reduction.

## 6. Audit

The dependency-free checker
[`verify_centered_rank_one_overlap_packet.py`](../computations/verify_centered_rank_one_overlap_packet.py)
checks the contraction table, the exact twelve-cell common-`q` relaxation,
all 24 private incidence designs, the 22/2 case split, the unique coloured
channels in Section 4.1, and the two transversality tests used in Section
4.2.  The shared-star impossibility itself is the hand coefficient proof
above, independently reconstructed in
[the audit](centered-rank-one-overlap-packet-independent-audit.md).
