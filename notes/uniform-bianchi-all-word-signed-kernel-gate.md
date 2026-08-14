# Full GHZ word rows see only the diagonal of the Bianchi chart kernel

## 1. Outcome

Let (h\geq3), and let the scalar-unit cap packet come from an exact source
on

\[
                         N=2h+2                                      \tag{1}
\]

physical sites.  The two overlapping pair charts do not give two different
full-word equations.  For every global colour word they are two partitions
of the same hafnian coefficient.  Consequently all (3^N) GHZ equations,
including all three normalized pure targets, factor through the **diagonal
chart quotient**.

This completely answers what the strict all-word rows do to the tagged
Bianchi kernel from
[`uniform-physical-horizontal-moment-saturation-bridge.md`](uniform-physical-horizontal-moment-saturation-bridge.md):

\[
 \boxed{
 \text{strict all-word and pure-target rows do not kill the chart-sign
 kernel.}}                                                   \tag{2}
\]

For each word (\omega), if (T_{pq,\omega}) and (T_{pr,\omega}) are
the two tagged presentations, then

\[
 \widehat\beta_{h,\omega}
      =T_{pq,\omega}-T_{pr,\omega}                          \tag{3}
\]

has zero common physical coefficient.  This is true on a mixed word because
both target values are zero, and on a pure word because the same normalized
target occurs twice:

\[
 \boxed{
 \operatorname {res}_{c^N}widehat\beta_{h,c^N}
       =X_c-X_c=0.}                                      \tag{4}
\]

Equation (4) is the sharp structural pure-word restriction identity.  It
annihilates the class after ordinary reinsertion, but not in the
source-labelled presentation.  There it lands in the chart-sign summand.
An antisymmetric chart covector detects it, while every readout descended
from the common global coefficient kills it.

There is a useful positive identity, but it applies to a smaller object.
If a tagged obstruction has first been factored into a genuine physical
matching-exchange minor (\Delta^{MN}_{cd}), the pure normalization
(H_c=1) gives the undivided source boundary

\[
 \boxed{
 \Delta^{MN}_{cd}
   =b_cP^M_{cd}-a_cP^N_{cd}.}                           \tag{5}
\]

Thus a pure word kills physical exchange **curvature** without localization.
It does not by itself identify the two chart tags in (3).  The shortest
remaining positive theorem is therefore a source-labelled factorization of
(\widehat\beta) through the E2/E3 exchange complex, together with primitive
common-core saturation.  The exact local (C_4) three-cell supplies the
coherence; the existing primitive-colon counterguard proves that saturation
cannot be assumed.

No exact full GHZ source or Krenn counterexample is constructed here.  The
smallest completed object below is a **full-output-row presentation packet**:
it contains every GHZ word and pure target in both charts, but it does not
realize those rows by one set of physical edge blocks.  The result rules out
closing the horizontal bridge by merely appending all coefficient equations.
It isolates the necessary new face as a chart-odd relative/Rees,
Hasse--Schmidt, or Bianchi contraction.

## 2. Uniform chart partition

Let (B) be the (N)-site set, and let (\mathcal M(B)) be its perfect
matchings.  Fix a colour word (\omega\in\{0,1,2\}^B).  Its global hafnian
row is

\[
 H_\omega=\sum_{M\in\mathcal M(B)}m_M(\omega),           \tag{6}
\]

where (m_M(\omega)) is the physical matching monomial using the colour
specified by (\omega) at every site.

For a deleted pair (p,q), partition the matching set as

\[
 \mathcal M(B)=
 \{M:pq\in M\}\;\sqcup\;\{M:pq\notin M\}.              \tag{7}
\]

The first part is the direct sector of the (pq) chart.  In the second
part, (p) and (q) are matched to two distinct residual sites; it is the
two-star sector.  Hence

\[
 H_\omega=H^{\mathrm{dir}}_{pq,\omega}
             +H^{\mathrm{star}}_{pq,\omega}.             \tag{8}
\]

The identical partition for (p,r) gives

\[
 H_\omega=H^{\mathrm{dir}}_{pr,\omega}
             +H^{\mathrm{star}}_{pr,\omega}.             \tag{9}
\]

Equations (8)--(9) are literal partitions of one set of matching monomials,
not equalities inferred from the GHZ target.  They remain true after any
global block specialization, provided the same vanished matching monomials
are removed in both charts.

The uniform term counts before specialization are

\[
 \#\mathcal M(B)=(2h+1)!!,
 \qquad
 \#\mathcal M(B\setminus\{p,q\})=(2h-1)!!,              \tag{10}
\]

so a chart has ((2h-1)!!) direct and
((2h+1)!!-(2h-1)!!) two-star terms.  At (h=3), these are (15) and
(90) out of (105).  In the exact direct-free specialization audited in
the repository, the (pr) direct sector vanishes globally; the surviving
ninety terms split as (15+75) in the (pq) chart and (0+90) in the
(pr) chart for every one of the (6561) words.

The target of (6) is

\[
 \operatorname {tar}(H_\omega)=
 \begin{cases}
 X_c,&\omega=c^N,\\
 0,&\text{otherwise}.
 \end{cases}                                             \tag{11}

Since (8) and (9) both equal (6), their target is literally the same.  This
proves (4) uniformly.

## 3. The full-output signed-kernel theorem

Let (W_h) be the vector space with basis (e_\omega) over all (3^N)
global words.  Retain the two chart tags:

\[
 P_h=W_h^{pq}\oplus W_h^{pr}.                            \tag{12}
\]

The strict common-coefficient map is

\[
 \Pi_h:P_h\longrightarrow W_h,
 \qquad
 \Pi_h(e_\omega^{pq})=e_\omega,
 \qquad
 \Pi_h(e_\omega^{pr})=e_\omega.                        \tag{13}

It has the canonical diagonal/sign decomposition

\[
 P_h=W_h^+\oplus W_h^-,
 \qquad
 W_h^+=\langle e_\omega^{pq}+e_\omega^{pr}\rangle,
 \qquad
 W_h^-=\langle e_\omega^{pq}-e_\omega^{pr}\rangle,     \tag{14}
\]

and

\[
 \operatorname {rank}\Pi_h=3^N,
 \qquad
 \ker\Pi_h=W_h^-,
 \qquad
 \dim W_h^-=3^N.                                       \tag{15}

> **Theorem 3.1 (strict all-word blindness).**  Every strict source readout
> obtained from the complete global coefficient rows factors through
> (\Pi_h), and hence vanishes on (W_h^-).  Appending all mixed rows and
> all pure target rows does not reduce (15).  A source operation can kill or
> detect (\widehat\beta_{h,\omega}) only if it is genuinely relative to
> the chart tags and does not factor through the common coefficient.

**Proof.**  Equations (8)--(9) show that both chart presentations map to
the same basis vector in every word grade, proving (13).  The kernel and
rank in (15) are the direct sum, over all words, of the elementary map

\[
                    \mathbb K^2\to\mathbb K,
                    \qquad(a,b)\mapsto a+b.             \tag{16}
\]

Its kernel is (\mathbb K(1,-1)).  Every strict row functional is a
linear functional on (W_h) pulled back along (\Pi_h), so it kills that
kernel.  The target vector (11) is one such functional and therefore does
not change the conclusion.  \(\square\)

This theorem concerns strict coefficient rows and their polynomial
multiples.  A relative mapping cone can have a differential from a new
chart-changing cell (\Gamma_{h,\omega}) with

\[
                         d\Gamma_{h,\omega}
                              =\widehat\beta_{h,\omega}. \tag{17}

Such a cell kills the sign summand precisely because it does not factor
through (13).  Hasse--Schmidt polars can also change fine degree and land in
that cone.  The theorem does not exclude them; it proves they are necessary.

## 4. Relation with the local polynomial (\beta_k)

For the two physical overlapping coordinate-cap charts, put

\[
 \Delta=At-By,
 \qquad
 \kappa=AU-BF,
 \qquad
 k=h-1.                                                 \tag{18}

The expanded difference of the two target presentations is

\[
\begin{aligned}
 \beta_k={}&(\Delta v+\kappa z)z^{[k-1]}
       +\Delta zvz^{[k-2]}\\
 &\quad-k\bigl(\kappa z^{[k]}
                  +\Delta vz^{[k-1]}\bigr).             \tag{19}
\end{aligned}

The matching identities

\[
 zz^{[k-1]}=kz^{[k]},
 \qquad
 zz^{[k-2]}=(k-1)z^{[k-1]}                              \tag{20}

make the (\kappa)- and (\Delta)-coefficients of (19) vanish
separately.  Thus (\beta_k=0) as a global matching polynomial before any
GHZ row is imposed.

This explains the apparent paradox.  The polynomial (\beta_k) is already
zero, while its source-labelled lift (\widehat\beta) can be nonzero: the
lift remembers which chart supplied each presentation.  Adding more
coefficient equations cannot see information which was forgotten by the
map from (3) to (19).

For a fixed mixed word, (11) reads (0-0).  For a fixed pure word it reads
(X_c-X_c).  The all-word completion therefore produces one signed kernel
line per word; it does not couple them.  A word-changing boundary or a
chart-changing boundary such as (17) is the first operation capable of
doing so.

## 5. The pure-target E2 boundary is positive but narrower

There is an exact physical operation which should be used after a
source-labelled factorization is found.  Fix two base matchings (M,N),
and for a colour state (c) write

\[
 a_c=m_M(c),
 \qquad b_c=m_N(c),
 \qquad H_c=\text{the complete hafnian coefficient}.    \tag{21}

Define the undivided transports and exchange minor

\[
 P^M_{cd}=a_cH_d-a_dH_c,
 \qquad
 P^N_{cd}=b_cH_d-b_dH_c,
 \qquad
 \Delta^{MN}_{cd}=a_cb_d-a_db_c.                       \tag{22}

The exact endpoint determinant identity is

\[
 b_cP^M_{cd}-a_cP^N_{cd}
       =\Delta^{MN}_{cd}H_c.                            \tag{23}

At a normalized pure word, (H_c=1), so no division or localization is
needed and (23) becomes (5).  At the opposite endpoint one likewise has

\[
 b_dP^M_{cd}-a_dP^N_{cd}
       =\Delta^{MN}_{cd}H_d.                            \tag{24}

Equations (23)--(24), their E3 Bianchi determinant, and their E4
tetrahedral coherence are literal identities in the full aggregate
polynomial ring.  They give the following conditional positive route.

> **Corollary 5.1 (pure-word exchange contraction).**  If a
> source-provenant map sends the tagged chart-sign class
> (\widehat\beta_{h,\omega}) to a sum of genuine exchange minors
> (\Delta^{MN}_{c d}), with all common matching cores retained, then the
> normalized pure row (H_c=1) sends that image into the undivided physical
> transport-boundary module by (5).

The hypothesis is load-bearing.  A chart tag is not itself a matching
minor.  Also, cancelling a common matching core after applying (5) requires
primitive source saturation.  The exact local (C_4) audit constructs E2,
E3, and E4 before cancellation, while the primitive-colon audit exhibits
nonzero classes after the common core is removed.  Therefore neither the
factorization nor saturation follows from determinant coherence alone.

## 6. The smallest all-word presentation guard

The smallest linear completion retaining both charts and the exact GHZ
target is

\[
 P_h=W_h^{pq}\oplus W_h^{pr},
 \qquad
 \text{target}=(G_h,G_h),
 \qquad
 G_h=\sum_{c=0}^2e_{c^N}.                               \tag{25}

It contains every global output word, all three pure target coefficients
equal to one in both charts, and every mixed target coefficient equal to
zero.  Its common coefficient quotient is exact, but its signed kernel is
the full (W_h^-) in (15).  A signed chart functional

\[
 \lambda_\omega(e_\omega^{pq})=1,
 \qquad
 \lambda_\omega(e_\omega^{pr})=-1                     \tag{26}

vanishes on the diagonal target (25) and reads (2) on
(\widehat\beta_{h,\omega}).

This is the exact finite terminal alternative at the presentation level:
either a new relative boundary kills (\widehat\beta), or a chart-sign
dual survives.  The covector (26) becomes a **physical** terminal only if
it annihilates every additional word, fine/repeated, anchor, terminal,
physical-(q), target, and higher-cell boundary in the completed decorated
source.  The packet (25) does not check that.

In particular, (25) is not an exact tensor (A) with

\[
                         \operatorname {Haf}(A)=
                            \sum_{c=0}^2e_c^{\otimes N}. \tag{27}

It is the row presentation any such tensor would induce after the two chart
tags are retained.  No edge blocks, pure target matchings, or cancellation
of mixed matching monomials are constructed.  It is therefore a
counterguard to a proof inference, not a Krenn counterexample.

At (h=3), the exact direct-free full-nine audit is a physical polynomial
instance of the same phenomenon.  It enumerates all (6561) words, retains
the same ninety global matching monomials in both charts, and finds an
anti-diagonal doubled-chart kernel.  The physical target and all strict
readouts factoring through the common global coefficient vanish on that
kernel.  Its five exact second polars identify the first possible
word/fine-changing relative symbols; ordinary strict rows do not supply
them.

## 7. Exact remaining full-source test

Let (D_{\mathrm{full},h}) be the boundary matrix of the complete decorated
source complex, not merely the strict all-word row matrix.  Include all
word, fine/repeated, anchor, terminal, physical-(q), protected target, and
relative comparison cells.  Let (B_h) be the columns representing the
tagged Bianchi classes (3).  Full-source completion kills them exactly when

\[
 \boxed{
 \operatorname {rank}D_{\mathrm{full},h}
   =\operatorname {rank}[D_{\mathrm{full},h}\mid B_h].} \tag{28}
\]

If (28) fails, finite duality gives a decorated covector (\lambda) with

\[
 \lambda D_{\mathrm{full},h}=0,
 \qquad
 \lambda B_h\ne0.                                      \tag{29}

Unlike (26), such a (\lambda) is a genuine physical terminal because the
matrix is complete.  This yields the sharp dichotomy requested by the
horizontal bridge:

\[
 \boxed{
 \text{chart-changing boundary}
 \quad\text{or}\quad
 \text{full decorated signed terminal}.}               \tag{30}
\]

The coefficient equations contribute only the diagonal block to (28).
The first viable new columns are:

1. a chart-odd Bianchi two-cell with boundary (17);
2. the all-word Hasse--Schmidt second-polars already isolated at (h=3);
3. a factorization through E2/E3 exchange minors followed by a proof of
   common-core saturation; or
4. a physical occurrence/endpoint word-changing cell whose signed face is
   (3).

An active-cap or Laurent-unit exit can still occur while constructing one
of these columns.  It cannot be inferred from the diagonal GHZ target rows
alone, because the minimal pure-normalized source-labelled guard already
allows its primitive (C_4) boundary mates to wander between physical
stars.

## Verification

Run

```text
python3 computations/verify_uniform_bianchi_all_word_signed_kernel_gate.py
python3 -O computations/verify_uniform_bianchi_all_word_signed_kernel_gate.py
python3 -I -S computations/verify_uniform_bianchi_all_word_signed_kernel_gate.py
```

The dependency-free checker pins the physical moment-saturation bridge,
the exact (h=3) all-word doubled-chart audit, the physical
curvature-square identity, and the local E2/E3/E4 coherence ledgers.  It
verifies the uniform matching counts, the diagonal/sign dimensions, the
three pure targets at (N=8), the separate cancellation of the
(\Delta)- and (\kappa)-parts of (19), and the pure-target identities
(5) and (24).  The proof of the chart partition and signed-kernel theorem is
uniform; finite heights are only arithmetic smoke tests.
