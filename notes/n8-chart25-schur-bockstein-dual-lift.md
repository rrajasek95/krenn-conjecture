# The chart-25 four-row obstruction is an exact lifted Schur--Bockstein cochain

This note identifies the frozen chart-25 degree-four dual with the literal
two-layer Schur--Bockstein construction. It also corrects the normalization
of its target pairing. The obstruction remains nonzero, so the exact
nonmembership result is unchanged.

This is a finite \(n=8\), chart-25 statement. The final section states the
source-faithful comparison still needed to transport the class to the
full-nine curvature/adjacent-power residue; that comparison is not yet
constructed here.

## 1. Exact dual lift

Write the filtered source matrix through degree four as

\[
 M=\begin{pmatrix}A&0\\T&B\end{pmatrix}.
 \tag{1}
\]

Here \(A\) is the complete degree-two/three source block, \(T\) is the
degree-four tail of those same individually labelled source columns, and
\(B\) is the leading part of the minimum-degree-four columns. Let \(U\) be
the lower row space and \(V\) the degree-four row space.

The exact invariant-quotient functional has three lower coordinates and one
leading coordinate:

\[
 \ell=(-2,-1,-1\mid 1).
 \tag{2}
\]

Put

\[
       \mu=(2,1,1)\in U^*,\qquad
       \lambda=(1)\in V^*.
 \tag{3}
\]

Thus \(\ell=(-\mu,\lambda)\). The support-local exact audit gives

\[
                  \lambda B=0,
       \qquad     \lambda T=\mu A.                       \tag{4}
\]

Equation (4) is checked on every source orbit which can meet the cochain:
there are nine canonical source-column orbits. Four have
\((\mu A,\lambda T)=(1,1)\), and five have value \((2,2)\). Every other
source orbit misses the support term by term. Hence (4) holds on all
59,488 older and 913,608 degree-four source-column orbits.

More importantly, (4) is not an artifact of invariant quotienting. Expanding
the cochain gives 20 actual rows. On them, \(-\mu\) has value \(-1/4\) on
each of the 16 lower rows and \(\lambda\) has value \(+1/4\) on each of the
four leading rows. All 56 individually labelled incident source columns
satisfy

\[
                  \mu A=\lambda T=\frac14.               \tag{5}
\]

Thus (2) is literally the lifted leading cochain in the
[Schur--Bockstein criterion](n8-filtered-macaulay-bockstein-schur-criterion.md),
not merely a dual found after forgetting source provenance.

## 2. The source-provenant target pairing is one

Use the residual convention

\[
                 b+Ax=0,\qquad c+Tx+By=0.                \tag{6}
\]

On the support of (3), the raw residual has

\[
                   b=(-1,0,0),\qquad c=-1.               \tag{7}
\]

Consequently

\[
       \mu b=-2,\qquad \lambda c=-1,
       \qquad \boxed{\lambda c-\mu b=1}.                 \tag{8}
\]

The frozen degree-three certificate \(x_0\) solves \(Ax_0=-b\). Direct
replay of all 1,634 orbit-columns through the two cochains gives

\[
                    \mu Ax_0=\lambda Tx_0=2.             \tag{9}
\]

Therefore the reduced leading residual is

\[
              \lambda(c+Tx_0)=-1+2=1,                   \tag{10}
\]

exactly equal to (8). Equivalently, the full lifted cochain pairs with the
single raw filtered target as

\[
                 (-\mu,\lambda)(b,c)=1.                 \tag{11}
\]

This is the source-relative target obstruction.

The earlier four-row note displayed the number

\[
       (-\mu)b+\lambda(c+Tx_0)=2+1=3.                   \tag{12}
\]

Formula (12) is a hybrid diagnostic: it pairs the lower part of the lifted
cochain with the raw lower residual but pairs \(\lambda\) with the *already
reduced* degree-four residual. It therefore includes the transferred tail
twice. Indeed

\[
       3-1=\lambda Tx_0=2.                              \tag{13}
\]

The correction from three to one changes no conclusion: both values are
nonzero, and (8)--(11) are the properly typed Schur calculation proving the
degree-four lift is inconsistent.

## 3. The local \(4D\) class is exactly the secondary residual

On the common-factor fibre, write the five actual rows as

\[
                       A_1,A_2,A_3,A_4,D.                \tag{14}
\]

The \(A_i\) are lower-filtration alternating-\(C_4\) rows and \(D\) is the
leading parallel-pair row. The 14 individually labelled source columns
project to four kinds of edge,

\[
                         \partial e_i=A_i+D.              \tag{15}
\]

The local lifted cochain is

\[
       \mu(A_i)=\frac14,\qquad \lambda(D)=\frac14,       \tag{16}
\]

so (15) gives \(\lambda T(e_i)=\mu A(e_i)=1/4\) before any
orbit collapse.

Now take the quotient packet as a filtered residual

\[
       q=(b,c)=-A_1-A_2-A_3+D.                           \tag{17}
\]

Solving its lower component uses \(x_0=e_1+e_2+e_3\). Equations (15) and
(17) give

\[
      b+Ax_0=0,
      \qquad c+Tx_0=D+3D=4D.                             \tag{18}
\]

Its secondary pairing is therefore

\[
 \lambda c-\mu b
   =\frac14-\left(-\frac34\right)
   =1
   =\lambda(4D).                                         \tag{19}
\]

Thus the relative vector \(4D\) isolated in the previous literal-source
audit is **exactly** the reduced Schur residual of the quotient packet. The
literal HPL packet

\[
                       -A_1-A_2-A_3-3D                  \tag{20}
\]

has pairing zero, and (17) minus (20) is \(4D\), with pairing one. This
simultaneously explains why the ordinary source HPL packet is augmentation
zero and why the quotient class belongs on the obstruction side of the
curvature--Bockstein dichotomy.

## 4. Source-faithful cochain transfer template

The useful construction does not require a quotient HPL correction. For a
literal filtered source block (1), define

\[
  Z_B=\ker B^*,\qquad
  \partial(\lambda)=[\lambda T]\in X^*/\operatorname{row}A. \tag{21}
\]

For \(\lambda\in\ker\partial\), choose \(\mu\) with
\(\lambda T=\mu A\), and set

\[
       \operatorname{Lift}(\lambda)=(-\mu,\lambda),
       \qquad
       \mathfrak b_{(b,c)}(\lambda)=\lambda c-\mu b.     \tag{22}
\]

These formulas have four properties needed by the uniform proof.

1. **Source annihilation.** Equation (22) annihilates every labelled old
   and new source column, not only its orbit projection.
2. **Lift independence.** If \(\mu\) is changed by a cochain annihilating
   \(\operatorname{im}A\), its value on \(b\in\operatorname{im}A\) does not
   change.
3. **Solution independence.** For any \(x_0\) with \(Ax_0=-b\),
   \(\mathfrak b(\lambda)=\lambda(c+Tx_0)\); changing \(x_0\) by
   \(\ker A\) does not change the value because \(\lambda T=\mu A\).
4. **No false correction.** A nonzero value of (22) is an obstruction. It
   cannot be inserted as an extra source boundary without also deriving a
   target component.

For more than two filtration layers, (22) iterates. If \(M_{ij}\) is the
block from source filtration \(j\) to row filtration \(i\), start with a top
cochain \(\ell_d\) and solve, downward in \(j\),

\[
                \sum_{i\ge j}\ell_iM_{ij}=0.             \tag{23}
\]

The resulting source-provenant secondary value is
\(\sum_i\ell_i r_i\) on the **raw** target layers. Using a reduced target at
one layer while retaining unreduced lower layers would repeat the
double-counting in (12).

## 5. Exact comparison required for the full-nine residue

Let primes denote the synchronized full-nine/adjacent-power blocks. A
comparison carrying the chart-25 class to the proposed curvature residue
must construct literal cochains \((M,\Lambda)\), before physical label or
orbit identification, satisfying

\[
       \Lambda B'=0,
       \qquad \Lambda T'=M A',                           \tag{24}
\]

and whose restriction to the selected alternating-\(C_4\)/collision fibre is
the cochain (16). The target comparison must then prove, rather than define,

\[
       \boxed{\Lambda c'-M b'
          =\kappa\,R_{\mathrm{adj}}},                    \tag{25}
\]

where \(\kappa\) is the selected physical curvature minor and
\(R_{\mathrm{adj}}\) is the admitted nonzero adjacent-power residue.

Equations (24)--(25) are a compact source-faithful interface for the missing
comparison map:

* (24) is the full-nine analogue of the 56 exact labelled equalities (5);
* the kernel-independence in (22) supplies zero lift indeterminacy;
* restriction to (18) forces the collision component to be \(4D\), so a
  putative comparison cannot silently use the augmentation-zero literal HPL
  packet instead; and
* (25), together with \(\kappa\ne0\) and \(R_{\mathrm{adj}}\ne0\), turns the
  surviving class into the required contradiction.

The missing theorem is now sharply typed: construct (24) as a map of the
literal full-nine source complex and prove (25). A mapping-cylinder cell
\(4D-\tau\) is not enough, because it supplies (25) by definition rather than
deriving its target component from the source-labelled comparison.

### The existing \(h=3\) candidate

The selected \(h=3\) cap calculation already supplies the target-side
covectors expected in (24). With

\[
 D_{\mathrm{cap}}=\begin{pmatrix}A&B\\F&U\end{pmatrix},
 \qquad \kappa=AU-BF,
\]

the two adjugate covectors obey

\[
 (-F,A)\binom AF=0,\qquad
 (-F,A)\binom BU=\kappa,
 \tag{26}
\]

and symmetrically for \((U,-B)\). Thus an adjugate line is the natural
candidate for \(\Lambda\): it kills the connection/normal column and reads
the physical curvature column as \(\kappa\). Tensoring this readout with the
adjacent-power cap class would make (25) specialize to

\[
                     \Lambda c'-M b'=-\kappa Y_0.        \tag{27}
\]

There is an exact target-side factorization behind this expectation. In the
selected cap quotient, with coordinates
\((w_v,\operatorname{tgt},\operatorname{ores})\), the existing columns are

\[
             T_v=(-Y,1,0)^{\mathsf T},\qquad
             \rho_v=(1,0,1)^{\mathsf T}.                 \tag{28}
\]

Their left kernel is generated by

\[
                         \omega=(1,Y,-1).                \tag{29}
\]

For the missing split-cap column \(p_v=(\kappa Y,0,0)^{\mathsf T}\),

\[
 \omega(p_v)=\kappa Y
   =\underbrace{\lambda_{25}(4D)}_{1}\,
    \underbrace{(-F,A)\binom BU}_{\kappa}\,
    \underbrace{Y}_{\text{adjacent power}}.              \tag{30}
\]

The checker verifies (26), (28)--(30) on four exact rational packets,
including the direct-free case. Thus the chart-25 class has precisely the
normalization needed by the full-nine curvature/cap obstruction: no unknown
scalar remains.

The existing \(h=3\) audits prove (26), the formal residue
\(-\kappa Y_0\), and the separate augmented-Jacobian membership criterion
\(\widehat J\zeta=-\widehat H(\xi,\eta)\). They do **not** construct the
literal lower cochain \(M\) or prove the source equality
\(\Lambda T'=MA'\). In Schur language, the known work supplies the proposed
leading covector and target value but not its source-provenant lift. This is
the same missing comparison previously described as the map from the polar
class \(h_vY_0\) to the split-cap class \(\kappa Yw_v\).

Equation (30) is only the target-side tensor factorization; it is not the
missing source comparison. It also gives a practical test for a proposed
comparison: build its literal
filtered columns, solve the dual equation in (24), and check (27) on the raw
augmented target. If the dual equation has no solution, the proposed polar
does not descend source-faithfully; if it does and (27) holds, the chart-25
\(4D\) class and the full-nine adjacent-power residue are instances of the
same secondary operation.

## 6. Exact verification

Run

~~~text
python3 computations/verify_n8_chart25_schur_bockstein_dual_lift.py
python3 -O computations/verify_n8_chart25_schur_bockstein_dual_lift.py
python3 -I computations/verify_n8_chart25_schur_bockstein_dual_lift.py
python3 -S computations/verify_n8_chart25_schur_bockstein_dual_lift.py
~~~

The checker verifies (4)--(5), replays the entire frozen degree-three
certificate through \(\mu A\) and \(\lambda T\), distinguishes the three
exact target pairings (8), (10), and (12), and reconstructs (18)--(20) on the
five-row actual fibre. Its frozen ledger digest is
086bc864911aef6b62d020c2a16ed82203e6ad3ca87005444e942162fd2a7ed4.
