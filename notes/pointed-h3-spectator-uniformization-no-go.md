# The pointed \(h=3\) comparison has no bare spectator uniformization

## Outcome

Grant the complete pointed, \(k[\beta]\)-linear, \(\rho\)-equivariant
comparison-or-terminal theorem at \(h=3\). There is still no functorial
deduction of its all-order analogue from any combination of:

1. tensoring with a fixed disjoint spectator matching;
2. scalar base change and divided-power suspension; or
3. canonical contraction to a local eight-site packet.

This is a sharp no-go for the **bare** constructions: linear and natural in
the binary clean-line parameter, with spectators carrying no new clean-line
covariant. It does not exclude a source-dependent nonlinear construction or
a direct all-\(h\) pointed comparison.

The three obstructions are independent.

* A fixed spectator matching suspends a selected word-sector cycle, but it
  does not preserve the full GHZ target.
* Even on that special word sector, parameter-trivial spectators cannot
  promote the nonzero rootless terminal readout from binary order five to
  order \(2h-1\).
* Contracting spectators and replacing their effect by pair blocks commutes
  with the matching tensor exactly after the higher cap error vanishes. That
  is active cleanliness, the hypothesis the global bridge is meant to
  produce.

Thus the first genuinely new uniform datum is not another \(h=3\) row. It is
an order-dependent source comparison, such as the common-Hankel transfer
\(\operatorname{Tr}_h\), together with its inactive and terminal
counterparts.

## Exact no-go theorem

Let \(U\) be the two-dimensional clean-line parameter space over a
characteristic-zero field. Suppose a proposed functor from the pointed
\(h=3\) comparison to the order-\(h\) physical comparison has the following
properties.

1. It is linear and \(SL(U)\)-natural.
2. Its added spectator matching and scalar extension are trivial as
   \(SL(U)\)-representations.
3. It preserves the complete GHZ target and the physical source
   differential.
4. On the rootless branch it transports the nonzero \(h=3\) terminal
   functional to the required nonzero common Macaulay functional at order
   \(h\).
5. If it removes spectator sites, it does so by the canonical pair-cap
   elimination of the exact descent theorem, without assuming an additional
   clean-cap result.

**Theorem.** For every \(h>3\), no such functor exists.

The statement deliberately does not forbid extra source-derived
representations, adaptive choices justified by a separate theorem, or a
comparison constructed directly on the all-\(h\) source complex.

## 1. A disjoint spectator block does not preserve the target

The simplest suspension attaches \(h-3\) disjoint two-site identity blocks
to an eight-site packet. On output words this produces

\[
 \Delta_{8,3}\otimes
 \prod_{j=1}^{h-3}
   \left(e_0e_0+e_1e_1+e_2e_2\right).                    \tag{1}
\]

The colour on each spectator pair is independent of the colour on the
eight-site core. Hence (1) has

\[
                              3^{h-2}                     \tag{2}
\]

nonzero word sectors, whereas \(\Delta_{2h+2,3}\) has exactly three. At the
first step, \(\Delta_{8,3}\otimes I\) has nine sectors rather than the three
sectors of \(\Delta_{10,3}\).

No different single disjoint two-site block \(B\) fixes this. If the core
colour is \(c\), target preservation demands

\[
                  B_{ij}=\begin{cases}1&i=j=c,\\0&\text{otherwise}.
                              \end{cases}                 \tag{3}
\]

For each diagonal entry \(B_{aa}\), the core choice \(c=a\) demands one,
while either other core colour demands zero. Thus (3) is inconsistent.

What remains valid is the narrower statement already used in the static
colon-cycle audit: a **fixed coefficient word** can be tensored by a fixed
spectator word. Divided powers give coefficient one for the unique complete
spectator matching. This constructs a static cycle on a specially suspended
packet; it is not a functor from arbitrary exact sources to exact sources.

## 2. The rootless terminal degree cannot be suspended naturally

At \(h=3\), the rootless terminal/Hankel readout has binary order five:

\[
                    \Theta_3\in\operatorname{Sym}^{5}U.
\]

At order \(h\), the required common Macaulay readout has order \(2h-1\):

\[
                    \Theta_h\in\operatorname{Sym}^{2h-1}U.       \tag{4}
\]

A spectator word has clean-line parameter degree zero. Therefore a natural
linear prolongation using only that word would give an intertwiner

\[
 \operatorname{Sym}^{5}U\longrightarrow
 \operatorname{Sym}^{2h-1}U.                                  \tag{5}
\]

Binary symmetric powers are irreducible. An intertwiner sends a highest
weight vector either to zero or to a highest weight vector of the same
weight. The source and target weights in (5) agree only for \(h=3\).
Consequently

\[
 \operatorname{Hom}_{SL(U)}
 \left(\operatorname{Sym}^{5}U,
       \operatorname{Sym}^{2h-1}U\right)=0
 \qquad(h>3).                                                  \tag{6}
\]

The same argument rules out a bare clean-error degree reduction
\(\operatorname{Sym}^{h}U\to\operatorname{Sym}^{3}U\). Ordinary scalar base
change does not alter these representation types, and site divided powers
alter site degree rather than clean-line parameter degree.

The smallest possible repair to (5) is additional source-derived data of
order \(2h-6\),

\[
                  \varrho_{2h-6}\in\operatorname{Sym}^{2h-6}U,  \tag{7}
\]

followed by the Cartan product
\(\Theta_3\varrho_{2h-6}\). But (7) is not supplied by a parameter-trivial
spectator word, and its existence is still not enough: one must prove the
single common system

\[
             \mu_{\mathcal E_h}^{*}
                  (\Theta_3\varrho_{2h-6})=0.                    \tag{8}
\]

The suspended full-27 scalar guard persists even when the formal clean
forms are \(s^h,t^h\), whose Macaulay shifts span all of
\(\operatorname{Sym}^{2h-1}U^*\). Its dual kernel is then zero. This proves
that the static divided-power identities do not imply (8). A positive
theorem must use physical decorated-source provenance, precisely as the
proposed transfer \(\operatorname{Tr}_h\) does.

The \(k[\beta]\)-Bockstein adds no escape from (6). Once an all-\(h\)
comparison exists, its \(\beta=0\) connecting morphism is functorial; scalar
extension alone does not create the comparison or the missing
order-\(2h-6\) covariant.

## 3. Local eight-site restriction is the clean bridge in disguise

Eliminating one pair \(p,q\) by a cap \(K\) gives the exact identity

\[
 K\mathbin{\lrcorner}H_B(A)
       =[(s+r)\exp(x)]_U.                                      \tag{9}
\]

When \(s\ne0\), the canonical effective pair array is

\[
                              y=x+r/s.
\]

The exact descent theorem proves

\[
 sH_U(y)-K\mathbin{\lrcorner}H_B(A)
   =\sum_{k=2}^{h}s^{1-k}
        \left[\frac{r^k}{k!}\exp(x)\right]_U.                  \tag{10}
\]

After clearing denominators, the right side is the homogeneous cap error
\({\cal E}_{p,q}(K)\). Therefore the canonical local restriction lands in
an exact pair-only source precisely when

\[
       {\cal E}_{p,q}(K)=0,\qquad
       s\kappa_0\kappa_1\kappa_2\ne0.                          \tag{11}
\]

Condition (11) is exactly active cleanliness. Repeatedly reducing an
arbitrary \(2h+2\)-site source to eight sites would require an active clean
cap at each preceding order. That is SP-CLEAN-BRIDGE, not a consequence of
the \(h=3\) comparison.

The failure is visible before any conjectural source is assumed. On eight
remaining scalar sites take

\[
\begin{aligned}
 x&=e_{01}+e_{23}+e_{45}+e_{67},\\
 r&=e_{02}+e_{13},\qquad s=1.
\end{aligned}                                                \tag{12}
\]

Then \([(s+r)\exp x]_{0\cdots7}=1\): the response edges cannot be completed
by \(x\). But \(H_8(x+r)=2\), from the two matchings
\(01|23|45|67\) and \(02|13|45|67\). Thus the square “cap, then replace by
effective pairs” versus “replace, then take the hafnian” has defect one.
Exact-target purity alone does not remove this universal higher-cumulant
term; a physical proof of (11) must.

An all-at-once contraction of many spectators has the same issue in a
larger form: integrating a quadratic matching model over spectator sites
produces higher even interactions on the retained sites. A pair-only local
packet exists only after those higher cumulants are killed or supplied with
new physical generators.

## Sharp remaining positive target

The no-go leaves two honest routes.

1. Construct \(\mathsf{PAComp}(h)\) directly on the complete all-\(h\)
   physical source complex, including its intrinsic order-\(h\) faces,
   physical \(q\), and terminal quotient.
2. Construct a genuinely source-derived uniformization. At minimum it must
   provide the clean-line comparison and \(\varrho_{2h-6}\) (or directly
   \(\operatorname{Tr}_h\)), prove the common-Hankel equation (8), and
   transport the even, Bockstein, anchor, inactive, face-zero, and terminal
   branches in the same physical complex.

Using adaptive local restriction is a third description only if it
independently proves (11) at every step; in that case it has proved the
global clean bridge rather than reduced it to \(h=3\).

## Verification

Run

~~~text
python3 computations/verify_pointed_h3_spectator_uniformization_no_go.py
python3 -O computations/verify_pointed_h3_spectator_uniformization_no_go.py
python3 -I -S computations/verify_pointed_h3_spectator_uniformization_no_go.py
~~~

The checker pins the \(h=3\) master, uniform-prolongation, cap-descent,
full-27 suspension, and covariant-naturality artifacts. It verifies:

* the spectator/GHZ word counts and the inconsistent single-block
  factorization;
* the complete \(\mathfrak{sl}_2\) intertwiner equations for the displayed
  symmetric powers through \(h=8\), including the one-dimensional
  equal-degree controls; and
* the cap defect-one example (12) by exact rational hafnian enumeration.

The highest-weight and cap identities above prove the corresponding
statements for every \(h>3\); the finite loops are implementation audits.

Frozen ledger SHA-256:

~~~text
eb09bb5f826383e53b85d9309254ba04806244da1b74407a598be1491dfe04bf
~~~
