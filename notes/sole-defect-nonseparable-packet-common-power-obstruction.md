# An SDR remains impossible with one deficient local frame

## 1. Exact theorem

Let \(U\) be a six-set with a distinguished site \(o\), and put
\(G=U\setminus\{o\}\). At each good site \(v\in G\), choose three
independent vectors

\[
                 a_0^{(v)},a_1^{(v)},a_2^{(v)}.
\]

At \(o\), choose three arbitrary nonzero vectors whose span has dimension
at most two. For a field \(r\) and pair \(P\in\binom U2\), write

\[
                 A_r(P)=\bigotimes_{u\notin P}a_r^{(u)}.         \tag{1}
\]

Let \(H_0,H_1,H_2\subseteq\binom U2\) be nonempty and give every active
lift an arbitrary nonzero complex coefficient:

\[
                 F=\sum_{r=0}^2\sum_{P\in H_r}
                         \lambda_{rP}A_r(P).                    \tag{2}
\]

**Theorem 1.1 (sole-defect SDR obstruction).** If the three active
families possess a system of distinct representatives

\[
                 P_r\in H_r,\qquad P_0,P_1,P_2
                 \text{ pairwise distinct},                    \tag{3}
\]

then there is no quadratic \(q\) in the site-square-zero algebra satisfying

\[
                         q^{[2]}=F,\qquad q^{[3]}=0.             \tag{4}
\]

The endpoint blocks of \(q\) are arbitrary tensors. The theorem permits
arbitrary local dimensions, both endpoint orders, zero blocks, parallel
aggregate terms, and complex cancellation. It is power-only and does not
use response rows.

Together with the response singleton lemma and the
[sole-defect two-pair obstruction](sole-defect-two-pair-common-power-obstruction.md),
this closes the coherent three-line-field branch having exactly one
deficient local frame. The response implication is written explicitly in
Section 6; it is not folded into the computational claim.

## 2. From an arbitrary SDR to isolated lifts and anchored packets

Fix the representatives (3) and put

\[
                         K=\{r:o\in P_r\}.                       \tag{5}
\]

At a good site \(v\), independence of the three field vectors gives a
linear map \(\phi_v\) which acts on their span by

\[
 \phi_v(a_r^{(v)})=
 \begin{cases}
 0,&v\in P_r,\\
 a_r^{(v)},&v\notin P_r.
 \end{cases}                                                     \tag{6}
\]

Use the identity at \(o\), extend the maps arbitrarily off the field spans,
and let \(\Phi\) be the resulting unital algebra endomorphism. For an
active lift \(A_r(P)\), every good site in \(P_r\) is a killed field factor.
Consequently

\[
       \Phi(A_r(P))\ne0
       \quad\Longleftrightarrow\quad
       P_r\setminus\{o\}\subseteq P.                            \tag{7}
\]

There are only two cases.

* If \(P_r=\{a,b\}\subset G\), both good sites must lie in the two-set
  \(P\), so \(P=P_r\). Field \(r\) is reduced to its selected, isolated
  lift.
* If \(P_r=\{o,a\}\), then \(a\in P\), so the surviving pairs are

  \[
        \{o,a\}\quad\text{and some of}\quad
        \{a,w\},\qquad w\in G\setminus\{a\}.                    \tag{8}
  \]

  The selected incident lift survives, and the other possible survivors
  are its four good arms.

Thus an incident representative produces an **anchored packet**

\[
  \mathcal P(a,B)=\{\{o,a\}\}\cup
                  \{\{a,w\}:w\in B\},
  \qquad B\subseteq G\setminus\{a\}.                            \tag{9}
\]

The selected coefficients remain nonzero. Since \(\Phi\) commutes with
bracket powers,

\[
 q'=\Phi(q),\quad F'=\Phi(F)
 \quad\Longrightarrow\quad
 q'^{[2]}=F',\qquad q'^{[3]}=0.                                 \tag{10}
\]

There is a small but essential bookkeeping point. In an isolated field,
the retained lift omits both killed good sites. In an anchored packet,
every retained lift in (8) omits its killed anchor \(a\). Hence every zero
vector introduced in (6) is unused by \(F'\). Replace each such unused
zero by its original field vector. This leaves \(F'\) literally unchanged
and restores three independent declared field vectors at every good site.
The bad-site vectors were never changed. Therefore \(F'\) is exactly in
the local setup of Theorem 1.1, with isolated families or packets (9).

If (3) is locally separable at \(o\), the bad-site selector from the
[distinct-lift theorem](sole-defect-distinct-lift-common-power-obstruction.md)
reduces \(F\) directly to three distinct nonzero lifts, which is impossible.
Suppose instead that (3) is locally nonseparable. If the packet system
\(F'\) has any other locally separable SDR, apply the same distinct-lift
selector to \(F'\); it is again impossible. It remains only to classify
packet systems for which **every** SDR is locally nonseparable.

## 3. Exhaustive packet census

Up to a bad-site linear change of coordinates, field-vector gauges, and
the field symmetries preserving the bad matroid, the nonseparable incident
sets are

| bad-site matroid | locally nonseparable \(K\) |
|---|---|
| three distinct lines in a plane | \(|K|=2\) |
| \(L_0^{(o)}=L_2^{(o)}\ne L_1^{(o)}\) | \(\{0\},\{2\},\{0,1\},\{1,2\}\) |
| rank one | every nonempty proper \(K\subset\{0,1,2\}\) |

There are therefore five cases modulo symmetry:

\[
 \text{circuit }K_2,\quad
 \text{coincident }K_1,\quad
 \text{coincident }K_2,\quad
 \text{rank-one }K_1,\quad
 \text{rank-one }K_2.                                          \tag{11}
\]

For \(|K|=1\), normalize the selected pairs to

\[
                 P_0=\{o,1\},\qquad P_1=E_1,\qquad P_2=E_2,     \tag{12}
\]

where \(E_1,E_2\in\binom G2\) are distinct. There are
\(16\cdot10\cdot9=1440\) labelled packet supports. For \(|K|=2\), use

\[
                 P_0=\{o,1\},\qquad P_1=\{o,2\},\qquad P_2=E,   \tag{13}
\]

giving \(16^2\cdot10=2560\) labelled supports.

The filter for an alternative locally separable SDR also has a direct
description. Write \(A_r\) for the good arms in the packet of field \(r\).

* For \(K_1\), every arm must equal one of \(E_1,E_2\); any other arm,
  together with the two isolated pairs, gives an all-good separable SDR.
* For circuit \(K_2\), \(A_0,A_1\subseteq\{E\}\). Switching either packet
  to a different arm would give a separable \(K_1\) SDR.
* For coincident \(K_2=\{0,1\}\), only the field-zero packet is constrained:
  \(A_0\subseteq\{E\}\). Switching field one alone leaves the allowed
  nonseparable set \(K=\{0\}\).
* For rank-one \(K_2\), put \(A'_r=A_r\setminus\{E\}\). An all-good SDR
  exists exactly when one can choose distinct arms from \(A'_0,A'_1\).
  Hence its absence is equivalent to one of \(A'_0,A'_1\) being empty, or
  to both being the same singleton.

The script nevertheless tests every representative choice directly rather
than relying only on these descriptions. Canonicalization under the
appropriate good-site and field stabilizers gives the exact census

| type | initial support orbits | no separable SDR | coefficient-normalizable | one-parameter |
|---|---:|---:|---:|---:|
| circuit \(K_2\) | 294 | 6 | 6 | 0 |
| coincident \(K_1\) | 85 | 14 | 14 | 0 |
| coincident \(K_2\) | 560 | 64 | 58 | 6 |
| rank-one \(K_1\) | 51 | 9 | 9 | 0 |
| rank-one \(K_2\) | 294 | 64 | 58 | 6 |
| **total** | **1284** | **157** | **145** | **12** |

This proves that the ideal calculation below has no omitted support type.

## 4. Arbitrary coefficients reduce to 145 constant and 12 one-parameter cases

First standardize the three bad-site lines to one of

\[
 \begin{array}{c|c}
 \text{type}&(a_0^{(o)},a_1^{(o)},a_2^{(o)})\\ \hline
 \text{circuit}&((1,0),(0,1),(1,1)),\\
 \text{coincident}&((1,0),(0,1),(1,0)),\\
 \text{rank one}&((1),(1),(1)).
 \end{array}                                                     \tag{14}
\]

Changing a representative on a bad-site line merely changes the active
lift coefficients, so no coefficient restriction is introduced. All
subsequent normalization uses only good-site field scalings, independently
for the three fields.

An isolated lift occupies at least three good sites, so one occupied good
axis normalizes its coefficient. Consider instead a packet anchored at
\(a\). Write \(\lambda_0\ne0\) for the coefficient of \(\{o,a\}\) and
\(\lambda_w\ne0\) for the coefficient of an active arm \(\{a,w\}\).
Scale the field axis at each \(w\in G\setminus\{a\}\) by \(t_w\ne0\), and
put

\[
                         T=\prod_{w\ne a}t_w.                    \tag{15}
\]

The incident and arm coefficients become, respectively,

\[
                         \lambda_0T,\qquad
                         \lambda_wT/t_w.                         \tag{16}
\]

Set \(T=\lambda_0^{-1}\). To normalize an active arm, set

\[
                         t_w=\lambda_w/\lambda_0.                \tag{17}
\]

If at most three arms are active, at least one of the four scales is still
free; choose it so that their product is the required \(T\). Thus every
coefficient is one, with no root extraction.

If all four arms are active, use (17) on any three arms and use the fourth
scale to impose \(T=\lambda_0^{-1}\). The remaining arm coefficient is

\[
                         \mu=
             \frac{\prod_{w\ne a}\lambda_w}{\lambda_0^3}
                         \in\mathbb C^*.                         \tag{18}
\]

Conversely, every \(\mu\ne0\) occurs. Choosing a different distinguished
arm merely moves the same invariant to that arm. In the 157-orbit census,
exactly twelve supports have a full packet, and each has exactly one; they
are the six coincident \(K_2\) and six rank-one \(K_2\) cases in the final
column of the table. All coefficients in every other field normalize
independently. Therefore the 145 constant cases and the twelve
\(\mu\in\mathbb C^*\) cases exhaust all arbitrary nonzero coefficient
assignments in (2).

## 5. Exact ideals and the nonzero-parameter localization

Project each good space onto its three field axes and the bad space onto
their one- or two-dimensional span. There are 120 endpoint-ordered
coordinates of an arbitrary \(q\) in the circuit and coincident cases and
105 in rank one. From (4) and

\[
                         q q^{[2]}=3q^{[3]},                     \tag{19}
\]

every solution satisfies the necessary linear equation

\[
                              qF=0.                              \tag{20}
\]

For the 145 constant cases, the checker collects equal six-site coordinate
words in (20), computes exact rational RREF, substitutes a complete kernel
basis into every coefficient of \(q^{[2]}-F\), and asks Singular for the
unsaturated Gröbner basis over \(\mathbb Q\). Every ideal is the unit ideal.

For a full packet, the entries of (20) lie in \(\mathbb Q[\mu]\). The
checker performs sparse RREF over \(\mathbb Q(\mu)\), but records and
audits every pivot before division. Across all twelve cases every inverted
pivot is literally \(1\) or \(\mu\). Hence all row operations are valid
already over the Laurent ring

\[
                         A=\mathbb Q[\mu,\mu^{-1}],              \tag{21}
\]

and no polynomial such as \(\mu-1\), or any other exceptional factor, is
inverted.

The checker realizes (21) exactly as

\[
             \mathbb Q[\mu,z]/(\mu z-1)\ \cong\
             \mathbb Q[\mu,\mu^{-1}],\qquad z\mapsto\mu^{-1}.   \tag{22}
\]

Every Laurent kernel expression is rendered in \(\mathbb Q[\mu,z]\), and
the ideal contains the additional generator \(\mu z-1\). All twelve
resulting ideals are unit ideals. This loses no nonzero specialization:
for each \(\mu\in\mathbb C^*\) there is exactly one point
\(z=\mu^{-1}\), while every point of \(\mu z-1=0\) has \(\mu\ne0\).
The excluded value \(\mu=0\) is precisely forbidden by the nonzero active
coefficients. Thus the calculation is uniform over all of
\(\mathbb C^*\), not merely generic in \(\mu\).

The frozen combined ledgers are

| class | type | orbits | combined ledger SHA-256 |
|---|---|---:|---|
| normalized | circuit \(K_2\) | 6 | 0469cf5512cd43e33bb5d8a1c645fc35cae0a34ced35d5c2d627c453e96331aa |
| normalized | coincident \(K_1\) | 14 | c9db1b099b249d534ee94a3063f5c1fd5a4e55dbd49f2a92f68d388cd904a68e |
| normalized | coincident \(K_2\) | 58 | e97b5045642a2715e670cf503c24d0543b36bfe849966edd5a5bfe3e422eeddc |
| normalized | rank-one \(K_1\) | 9 | 97a703257591444e12fcc364ddf6e87e7c17b449b3199deefabc401b8169542d |
| normalized | rank-one \(K_2\) | 58 | c31e02b0af67b5c10eedbdc91d21921a49b4897147a61a115a7722f1e4ec6aa3 |
| parameter | coincident \(K_2\) | 6 | ad85e0d56bacd618338483baabb9da62bd427960e6feb8548fafaebc31537874 |
| parameter | rank-one \(K_2\) | 6 | 3c69d3157bd1ea0a09d2876531ef6faeab5aa53b5edc235ad6ca9a4f0f794700 |

The global ordered stream of all 157 per-case ledgers has SHA-256

    7e766f3e56aee47b3b623dcbc1c5db60ac145deaa735c543746507a5fe1295f4

Each per-case ledger contains the canonical families, ordered \(q\)-cells,
all collected \(qF\) rows, the complete RREF, and every nonzero quadratic
generator. Parameter ledgers also contain the full inverted-pivot list.
This proves Theorem 1.1.

## 6. Line-by-line consequence for the response branch

Assume now the coherent three-line-field response setup and all nine
response equations from the
[degenerate response normal form](degenerate-three-line-field-response-normal-form.md),
together with \(F=q^{[2]}\) and \(q^{[3]}=0\), and suppose exactly one local
field frame is deficient.

1. The five-good-site module split shows that every active family \(H_r\)
   is nonempty.
2. The response singleton lemma excludes
   \(H_r=H_s=\{P\}\) for distinct fields \(r,s\).
3. Suppose the three families had no SDR. Hall failure cannot occur on one
   family because all are nonempty. It cannot occur on two families,
   because two nonempty families with union of size less than two would be
   the forbidden equal singleton. Therefore Hall failure occurs only on
   all three families, with

   \[
                     |H_0\cup H_1\cup H_2|\le2.                 \tag{23}
   \]

   The union cannot have size one by the same singleton lemma, so it is
   exactly two distinct physical pairs. The only possible family-size
   profiles are \((2,2,2),(2,2,1),(2,1,1)\), and in the last profile the two
   singleton fields use different pairs.
4. The sole-defect two-pair obstruction says every common-power ideal in
   those profiles is the unit ideal. Hence the active families must have
   an ordinary SDR.
5. Theorem 1.1 says a common-power multiplier with such an SDR is
   impossible.

Therefore:

**Corollary 6.1 (sole-defect response closure).** A coherent three-line
field satisfying all nine responses and the common-power equations cannot
have exactly one deficient local frame.

No bridge-specific assumption is used in the last step: axial and bridge
normal forms both feed the same three nonempty active families into the
argument above.

## 7. Reproduction and scope

The primary replay is

    uv run python computations/verify_sole_defect_nonseparable_packet_common_power.py

with
[verify_sole_defect_nonseparable_packet_common_power.py](../computations/verify_sole_defect_nonseparable_packet_common_power.py).
It reconstructs all 1,284 canonical packet supports, filters the 157 having
no locally separable SDR, rebuilds all exact kernels and ideals, verifies
all 157 unit results, and checks every frozen component and global ledger.
The fast replay omits only the Singular calls:

    uv run python computations/verify_sole_defect_nonseparable_packet_common_power.py --ledger-only

The constituent scripts are the
[support census](../computations/explore_sole_defect_nonseparable_packet_orbits.py),
[145-case normalized checker](../computations/verify_sole_defect_nonseparable_normalizable_packets.py),
and
[12-case parameter checker](../computations/verify_sole_defect_nonseparable_parameter_packets.py).

The theorem closes exactly one deficient site. It does not claim that the
same packet reduction survives with two or more deficient sites, where the
five independent good frames and the local separability table both change.
It also does not replace the coordinate-plane theorem for the all-deficient
boundary. The only use of \(q^{[3]}=0\) in the ideal construction is the
necessary consequence \(qF=0\); impossibility of this weaker necessary
system is enough for (4).
