# A top scalar-unit selector forces one oriented adjacent-power coefficient

## 1. Outcome

Work in the exact intrinsic scalar-unit chart on \(2h\) residual sites,
\(h\geq3\), from the
[full-nine radial target lock](scalar-unit-radial-locus-full-nine-target-lock.md).
Write

\[
 A=\alpha E_{aa},\qquad Q=q^{[h]},\qquad
 R_{jk}=p_js_k,\qquad \alpha\ne0,                       \tag{1}
\]

and suppose that a literal top functional \(\nu\) has been sourced with

\[
 \nu(Q)=0,\qquad
 \nu\bigl(R_{jk}q^{[h-1]}\bigr)=\delta_{ij}\delta_{ik}.
                                                                  \tag{2}
\]

The matrix on the right of (2) is \(E_{ii}\in\operatorname {Mat}_{3}\):
its row and column indices are the endpoint colours \(j,k\), not residual
sites or local probe colours.

The Euler decomposition suggested by (2) is correct, with exactly one
factor \(h-1\).  For one-site forms \(u,v\),

\[
 \boxed{
 B_\nu(u,v):=\nu\bigl(uvq^{[h-1]}\bigr)
   ={1\over h-1}\sum_fq_f
       \nu\bigl(uvf q^{[h-2]}\bigr).}                  \tag{3}
\]

Here \(f\) runs once over **unordered decorated cells**.  Formula (3)
alone only detects a star--star cofactor and does not put the star product
on the same cell as an oriented curvature coefficient.  There is,
however, a stronger exact consequence of the same selector.

Choose an order on the residual physical sites.  At an unordered decorated
cell \(e=((r,c),(s,d))\), \(r<s\), let

\[
 \begin{aligned}
 H_e(j,k)&=(p_j)_{r,c}(s_k)_{s,d},\\
 G_e(j,k)&=(p_j)_{s,d}(s_k)_{r,c},                       \tag{4}\\
 K_e^\rightarrow&=Aq_e-H_e,\qquad
 K_e^\leftarrow=Aq_e-G_e.
 \end{aligned}
\]

Thus \(H_e+G_e\) is the coefficient matrix of \((R_{jk})\) at \(e\),
and the selected diagonal entries are the literal oriented curvatures

\[
 \begin{aligned}
 \kappa_e^\rightarrow
   &=\alpha\delta_{ia}q_e-(p_i)_{r,c}(s_i)_{s,d},\\
 \kappa_e^\leftarrow
   &=\alpha\delta_{ia}q_e-(p_i)_{s,d}(s_i)_{r,c}.        \tag{5}
 \end{aligned}
\]

Put

\[
                         \gamma_{ef}
       =\nu\bigl(efq^{[h-2]}\bigr).                     \tag{6}
\]

Then the exact oriented two-cell identity is

\[
 \boxed{
 \sum_{e,f}q_f\gamma_{ef}
          \bigl(K_e^\rightarrow+K_e^\leftarrow\bigr)
                  =-(h-1)E_{ii}.}                       \tag{7}
\]

Taking the \((i,i)\)-entry and expanding the two orientations proves:

> **Theorem 1.1 (oriented two-cell localization).**  There are unordered
> decorated cells \(e,f\) and an orientation
> \({\rm or}\in\{\rightarrow,\leftarrow\}\) such that
>
> \[
> \boxed{
> q_f\ne0,\qquad
> \kappa_e^{\rm or}\ne0,\qquad
> \nu\bigl(efq^{[h-2]}\bigr)\ne0.}                     \tag{8}
> \]
>
> The cells \(e,f\) use four distinct residual physical sites.  If
> \(\nu\) is written as its finite linear combination of literal top-word
> coefficient restrictions, at least one constituent restriction has the
> corresponding nonzero \(efq^{[h-2]}\)-coefficient.

Thus the source-provenant selector does force a nonzero literal oriented
curvature against an adjacent \(q^{[h-2]}\)-cofactor.  This is genuinely
stronger than the star--star detection in (3): it closes the local
orientation/occupancy selection gate for this selector.

The physical roles of the two cells are different.  The original endpoints
together with the sites of \(e\) carry the ordinary oriented four-cut
minor (5).  The supported cell \(f\), disjoint from \(e\), is the next
literal coefficient restriction which lowers the remaining matching power
to \(q^{[h-2]}\).  Thus (8) is an oriented four-cut **with an adjacent-power
coefficient exposed**, not a claim that \(e\) and \(f\) are one curvature
cell.

The conclusion is still not

\[
                \kappa_e^{\rm or}(H_a)_{\rm comp}\ne0,  \tag{9}
\]

where \(H_a\) is the full divided-difference carrier in the scalar-unit
normal jet.  Nor does (7) give an annihilating four-cut row, a common
restriction--insertion lift, a clean cap, or the exceptional label
\(i=a\).  The existing carrier-torsion and source-lift guards therefore
remain operative.  This note advances one sharply bounded selection
step; it does not close the intrinsic scalar-unit branch or Krenn's
conjecture.

## 2. Decorated-cell and divided-power normalization

Let \({\cal A}\) be the residual site-square-zero algebra.  Index a basis
quadratic by

\[
 e=((r,c),(s,d)),\qquad r<s,                              \tag{10}
\]

and use \(e\) also for its commutative cell monomial.  The physical
aggregate convention is

\[
                         q=\sum_eq_e e.                  \tag{11}
\]

Each unordered decorated cell occurs once.  The reverse aggregate block
is its transpose and is not a second term of (11).  Parallel source
contributions which aggregate to the same decorated cell are already
summed in \(q_e\).

There are nevertheless two endpoint-star assignments at a cell.  Direct
multiplication of the one-site forms gives

\[
       [p_js_k]_e
        =(p_j)_{r,c}(s_k)_{s,d}
          +(p_j)_{s,d}(s_k)_{r,c}
        =H_e(j,k)+G_e(j,k).                              \tag{12}
\]

There is no factor \(1/2\) in (12).  The two summands are two physical
assignments of the distinct endpoint stars, even if their numerical
values happen to agree.  Consequently

\[
            (R_{jk})=\sum_e(H_e(j,k)+G_e(j,k))e.         \tag{13}
\]

The divided-power convention is

\[
             q^{[m]}={q^m\over m!},\qquad
             q q^{[m]}=(m+1)q^{[m+1]}.                  \tag{14}
\]

Apply (14) with \(m=h-2\), expand only the single ordinary factor \(q\)
by (11), and then apply \(\nu\):

\[
\begin{aligned}
 (h-1)B_\nu(u,v)
   &=\nu\bigl(uvq q^{[h-2]}\bigr)\\
   &=\sum_fq_f\nu\bigl(uvf q^{[h-2]}\bigr).
                                                               \tag{15}
\end{aligned}
\]

This proves (3).  No additional factorial belongs to a decorated
coefficient.  If instead one writes a redundant ordered sum over
\(r\ne s\), a compensating \(1/2\) must be put into that definition of
\(q\); mixing that convention with (11) doubles (15).

For later use, put

\[
 \omega_e=\nu\bigl(e q^{[h-1]}\bigr).                   \tag{16}
\]

The same calculation with the cell \(e\) already inserted gives the local
Euler identity

\[
 \boxed{(h-1)\omega_e=\sum_fq_f\gamma_{ef}.}            \tag{17}
\]

If \(e\) and \(f\) share a physical site, their product is zero in
\({\cal A}\), so

\[
                  \gamma_{ef}\ne0
       \quad\Longrightarrow\quad
       e,f\text{ occupy four distinct physical sites}.  \tag{18}
\]

This is a literal site-occupancy assertion, not a genericity claim.

## 3. The oriented coefficient-span identity

Package (2) as a matrix equality.  Expanding \(R=(R_{jk})\) in the
decorated basis gives

\[
             \boxed{\sum_e\omega_e(H_e+G_e)=E_{ii}.}    \tag{19}
\]

The other selector condition and \(q q^{[h-1]}=hQ\) give

\[
             \boxed{\sum_eq_e\omega_e=h\nu(Q)=0.}      \tag{20}
\]

Equations (19)--(20) immediately imply the one-cell oriented span

\[
\begin{aligned}
 \sum_e\omega_e(K_e^\rightarrow+K_e^\leftarrow)
   &=2A\sum_eq_e\omega_e
        -\sum_e\omega_e(H_e+G_e)\\
   &=-E_{ii}.                                             \tag{21}
\end{aligned}
\]

This already forces a nonzero oriented curvature against a literal
\(q^{[h-1]}\)-complement.  Substitute (17) into (21) to obtain (7).

For comparison with the raw catalecticant decomposition, define for each
decorated cell \(f\)

\[
\begin{aligned}
 C_f&=\nu\bigl(Rf q^{[h-2]}\bigr)
       =\sum_e\gamma_{ef}(H_e+G_e),\\
 D_f&=\nu\bigl(qf q^{[h-2]}\bigr)
       =\sum_eq_e\gamma_{ef},                            \tag{22}\\
 O_f^\rightarrow&=\nu\bigl(K^\rightarrow f q^{[h-2]}\bigr),
 \qquad
 O_f^\leftarrow=\nu\bigl(K^\leftarrow f q^{[h-2]}\bigr),
\end{aligned}
\]

where \(K^{\rm or}=\sum_eK_e^{\rm or}e\).  The three exact ledgers are

\[
\begin{aligned}
 O_f^\rightarrow+O_f^\leftarrow&=2AD_f-C_f,             \tag{23}\\
 \sum_fq_fC_f&=(h-1)E_{ii},                              \tag{24}\\
 \sum_fq_fD_f
   &=\nu\bigl(q^2q^{[h-2]}\bigr)
     =h(h-1)\nu(Q)=0.                                    \tag{25}
\end{aligned}
\]

Combining (23)--(25) is exactly (7).  This pinpoints what was missing from
the first reading of (3).  One may not identify \(C_f\) coefficientwise
with curvature: the direct double-internal term \(2AD_f\) is generally
present.  Its **weighted total** vanishes by \(\nu(Q)=0\), which is enough
for oriented localization but not for a coefficientwise equality at a
prescribed \(f\).

There is no cancellation issue in the existence conclusion.  The
\((i,i)\)-entry of (7), with the two orientations written separately, is

\[
 \sum_{e,f}q_f\gamma_{ef}\kappa_e^\rightarrow
  +\sum_{e,f}q_f\gamma_{ef}\kappa_e^\leftarrow
       =-(h-1)\ne0.                                      \tag{26}
\]

If every displayed scalar summand were zero, the left side would be zero.
Hence one summand is nonzero.  Its three factors are all nonzero, and
(18) gives \(e\ne f\) and four distinct residual sites.  This proves
Theorem 1.1 without selecting a summand from a zero or cancelling a
matching power.

## 4. Sharp same-cell and carrier guards

The two distinct cells in Theorem 1.1 are essential.  There is a uniform
literal site-square-zero packet showing why the \(q\)-supported cell found
directly from (3) need not itself carry curvature.

Use one local colour on sites \(0,1,\ldots,2h-1\), put

\[
 f_t=x_{2t}x_{2t+1}\quad(1\leq t\leq h-1),\qquad
 q=\sum_{t=1}^{h-1}f_t,                                  \tag{27}
\]

and let \(\nu\) select the full word \(x_0x_1\cdots x_{2h-1}\).  Take the
selected endpoint stars and direct coefficient to be

\[
 p=x_0+\sum_{r=2}^{2h-1}x_r,\qquad
 s=x_1+\sum_{r=2}^{2h-1}x_r,\qquad A_{ii}=1.             \tag{28}
\]

All other selector channels may be taken \(\nu\)-invisible.  Then

\[
 q^{[h]}=0,\qquad
 \nu\bigl(psq^{[h-1]}\bigr)=1,                           \tag{29}
\]

and for every supported \(f_t\),

\[
 \nu\bigl(psf_tq^{[h-2]}\bigr)=1.                       \tag{30}
\]

Thus every term in the raw Euler sum is detected.  But both endpoint
assignments at \(f_t\) equal its direct coefficient:

\[
                    \kappa_{f_t}^\rightarrow
                     =\kappa_{f_t}^\leftarrow=0.         \tag{31}
\]

The oriented identity instead uses

\[
 e=x_0x_1,\qquad q_e=0,\qquad
 \kappa_e^\rightarrow=-1,\quad
 \kappa_e^\leftarrow=0,                                 \tag{32}
\]

and any \(f_t\) supplies
\(\nu(ef_tq^{[h-2]})=1\).  The \(h-1\) resulting terms sum to the
right side of (26).  This packet proves that the correction from (3) to
(7) is substantive: polarization cannot simply relabel the detected
\(q\)-cell as the curvature cell.

Even the nonzero leading adjacent coefficient in (8) need not survive in
the full normal-jet carrier.  At \(h=3\), take \(i=a\), \(\alpha=1\), and
put

\[
 q=x_2x_3+x_4x_5,\qquad
 p=x_0+x_2+x_4,\qquad
 s=x_1-2x_3-2x_5,\qquad r=R_{aa}=ps.                    \tag{33}
\]

For the normalized first divided-difference carrier

\[
                         H_0=q+{1\over2}r,               \tag{34}
\]

take \(e=x_0x_1\), \(f=x_2x_3\), and the full-word coefficient
functional.  The forward curvature is \(-1\), and

\[
 \kappa_e^\rightarrow\nu(efq)=-1,
 \qquad
 \kappa_e^\rightarrow\nu(efH_0)=0.                     \tag{35}
\]

The \(x_4x_5\)-coefficient \(1\) of \(q\) is cancelled by the coefficient
\(-2/2\) of \(r/2\).  This is a local sharpness packet, not a full exact
ternary source and not a clean-unary model.  The already certified
[carrier-torsion guard](scalar-unit-carrier-torsion-obstruction.md) is
stronger at the formal clean-carrier level: even granting both complete
oriented carrier annihilations does not yield the required response
vanishing.

## 5. Comparison with the existing frontier

The exact gain and its limit can now be separated.

1. The coefficient-span theorem in
   [full-cap carrier relocation](full-cap-carrier-resonance-relocation.md)
   places target diagonal matrices in the span of decorated coefficients
   of a completed cap.  Equations (21) and (7) are the scalar-unit
   catalecticant analogue with more structure: the target is the specific
   endpoint-colour unit \(E_{ii}\), the coefficients are split into the two
   physical orientations, and (7) retains an adjacent
   \(q^{[h-2]}\)-cofactor.  It applies to one sourced top selector, not to a
   whole varying cap family.
2. The
   [complementary-pivot four-cell packet](scalar-unit-complementary-pivot-essential-pair.md)
   proves a nonzero \(\kappa^{\rm or}H_{a,\rm comp}\) on its clean,
   minimum-support \(2\)-by-\(2\) equality branch.  Theorem 1.1 needs none
   of that support rigidity, but its carrier is only the leading
   \(q^{[h-2]}\) layer.  Neither theorem contains the other.
3. The
   [full normal-jet ledger](scalar-unit-full-normal-jet-unary-anchor-ledger.md)
   needs a source-faithful comparison on \(R_{ia}R_{aj}H_a\).  Equation
   (8) neither selects the exceptional label \(a\) nor replaces
   \(q^{[h-2]}\) by the full sum defining \(H_a\).  Formula (35) shows why
   that replacement is not formal.
4. The
   [oriented curvature torsion no-go](intrinsic-scalar-unit-oriented-curvature-torsion-no-go.md)
   and the carrier-torsion theorem remain untouched.  This note proves a
   nonzero evaluated coefficient; those theorems diagnose the missing
   annihilation, carrier faithfulness, and exceptional response deletion.
5. At \(h=3\), the
   [one-anchor selector guard](h3-one-anchor-selector-four-cut-guard-and-two-anchor-threshold.md)
   already shows that one literal diagonal four-cut coefficient does not
   lower the selector--Macaulay image.  More generally, the
   [Hilbert--Cauchy tower](scalar-unit-carrier-moment-tower-hilbert-cauchy.md)
   requires a compatible family of moments and legal \(q,r\)-multiplication,
   while the new
   [based-loop torsor](scalar-unit-moment-transgression-source-lift-based-loop-torsor.md)
   shows that evaluated/associated-graded rows do not choose a zero-residue
   source lift.  The single nonzero class (8) supplies neither datum.
6. The scalar-unit
   [full-isotropic packet guard](uncontracted-four-cut-scalar-unit-full-isotropic-packet-guard.md)
   and
   [80-of-81 guard](uncontracted-four-cut-scalar-unit-eighty-row-injective-guard.md)
   remain consistent with (7).  They show that isotropic contractions and
   endpoint injectivity do not reconstruct the exceptional uncontracted
   coefficient.  Here the top selector (2) is an explicit premise; (7)
   extracts one nonzero evaluated class from it but does not reconstruct a
   missing row or a complete 81-row annihilating packet.

Accordingly Theorem 1.1 is a genuine local theorem: the selector branch
cannot hide completely from every literal oriented adjacent-\(q\)-power
coefficient.  What remains is a filtered transport theorem which places
that coefficient on the full \(H_a\) carrier, retains the exceptional
target, synchronizes the needed cap family, and has zero lift
indeterminacy.  No clean cap or proof follows here.

## 6. Exact audit

The dependency-free
[checker](../computations/verify_scalar_unit_catalecticant_four_cut_localization.py)
implements the literal site-square-zero algebra and audits:

* \(q q^{[h-2]}=(h-1)q^{[h-1]}\) and
  \(q q^{[h-1]}=h q^{[h]}\);
* unordered decorated-cell coefficients and both endpoint orientations;
* (3), (7), and (22)--(26) for \(3\leq h\leq8\);
* explicit localization to distinct cells and one individual orientation;
* the uniform same-cell guard (27)--(32) and the \(H_0\) cancellation
  (33)--(35); and
* mutations of the Euler divisor, ordered-cell double counting, the
  direct factor two, and either omitted endpoint orientation.

All failures are explicit rather than Python assertions, so the checker
runs unchanged under optimized Python.  The finite range audits signs,
factors, and cell conventions; the proofs of (7) and (26) are
uniform in \(h\).
