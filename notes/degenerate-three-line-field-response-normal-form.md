# Degenerate three-line fields have a sharp response normal form

## 1. Setup and result

Let \(U\) be a six-set and work in the site-square-zero algebra

\[
 {\cal R}_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_u^2=0.
\]

At every site choose three nonzero field vectors \(a_r^{(u)}\),
\(r=0,1,2\), and put

\[
 L_r^{(u)}=\mathbb C a_r^{(u)},\qquad
 W_u=L_0^{(u)}+L_1^{(u)}+L_2^{(u)}.                 \tag{1}
\]

For a pair \(P\in\binom U2\), write

\[
 A_r(P)=\bigotimes_{u\notin P}a_r^{(u)},\qquad
 F=\sum_{r=0}^2\sum_{P\in\binom U2}\lambda_{rP}A_r(P). \tag{2}
\]

The coefficients in (2) are aggregate complex coefficients and may vanish
after arbitrary cancellation.  Let \(e_0^{(u)},e_1^{(u)},e_2^{(u)}\) be
independent target vectors and \(X_i=\bigotimes_u e_i^{(u)}\).  Assume
arbitrary multi-site rows satisfy all nine responses

\[
                         p_i s_jF=\delta_{ij}X_i.       \tag{3}
\]

No common-power hypothesis is needed for the following theorem.  It may
therefore be combined without loss with \(F=q^{[2]},q^{[3]}=0\).

**Theorem 1.1 (incidence and the all-deficient boundary).**  Define

\[
                         D_i=\{u:e_i^{(u)}\in W_u\}.    \tag{4}
\]

Then

\[
             |D_i|\ge4\quad(i=0,1,2),\qquad
             D_0\cup D_1\cup D_2=U.                  \tag{5}
\]

In particular, a deficient space \(W_u\) contains at least one target
axis.  If every \(W_u\) has dimension at most two, then all six have
dimension two and there are disjoint pairs \(B_0,B_1,B_2\) partitioning
\(U\) such that

\[
 W_u=\operatorname {span}\{e_j^{(u)}:j\ne i\}
                   \quad\Longleftrightarrow\quad u\in B_i.       \tag{6}
\]

Thus three fields do not evade the coordinate-plane omission-pair boundary;
at the response-incidence level what remains is exactly three arbitrary
lines inside each of the six forced coordinate planes.

**Corollary 1.2 (the all-deficient common-power branch is empty).**  Add
\(F=q^{[2]}\) and \(q^{[3]}=0\).  If every \(\dim W_u\le2\), equations
(2)--(3) have no solution.

Indeed, choose a linear projection \(\pi_u:V_u\to W_u\) which fixes \(W_u\),
and extend \(\Pi=\bigotimes_u\pi_u\) to a unital algebra endomorphism.  Every
occupied factor of every term in (2) belongs to its local \(W_u\), so
\(\Pi(F)=F\).  Therefore

\[
 q'=\Pi(q)\quad\Longrightarrow\quad
 q'^{[2]}=F,\qquad q'^{[3]}=0,\qquad
 q'_{uv}\in W_u\otimes W_v.                              \tag{7}
\]

Nothing is projected in the response equations.  The multiplier itself is
fixed, so the original rows \(p_i,s_j\), the original target tensors \(X_i\),
and all nine literal equalities (3) remain unchanged.  In particular, this
argument does not apply a projection to (3) and then infer anything
termwise.

Equation (6) identifies these spaces with the three coordinate planes on
three omission pairs.  The independently audited
[coordinate-plane mixed-packet obstruction](coordinate-plane-mixed-packet-obstruction.md)
and its
[independent audit](coordinate-plane-mixed-packet-obstruction-independent-audit.md)
then contradict all nine responses.  That theorem retains arbitrary mixed
four-site packets and in fact does not need \(q'^{[3]}=0\).

There is a much sharper classification when only one local frame is
deficient.

**Theorem 1.3 (sole-defect axial/bridge dichotomy).**  Suppose there is a
site \(o\in U\) such that

\[
 a_0^{(v)},a_1^{(v)},a_2^{(v)}
       \text{ are linearly independent for every }v\in G:=U\setminus\{o\}.
                                                               \tag{8}
\]

No independence is assumed at \(o\).  For each target \(i\), exactly one of
the following alternatives holds.

1. **Axial.**  There is a unique field \(r\) such that

   \[
              e_i^{(u)}\in L_r^{(u)}
              \quad\text{at at least four sites }u\in U.         \tag{9}
   \]

2. **Binary bridge.**  There are unique distinct fields \(r,s\) such that,
   at every good site,

   \[
                 e_i^{(v)}\in L_r^{(v)}+L_s^{(v)},               \tag{10}
   \]

   the target agrees with \(L_r\) at at most two good sites and with
   \(L_s\) at at most two good sites, and

   \[
                 L_r^{(o)}=L_s^{(o)}=\mathbb C e_i^{(o)}.        \tag{11}
   \]

There is at most one bridge target.  The axial targets are assigned to
distinct fields.  If a bridge exists, it cannot join the two fields assigned
to the other two (axial) targets.  Consequently, after relabelling, the only
sole-defect residuals are

* three axial targets assigned bijectively to the three fields; or
* axial targets assigned to fields \(0,1\), and one bridge target between
  fields \(0,2\), with \(L_0^{(o)}=L_2^{(o)}\).

In particular, if the three lines at the deficient site are pairwise
distinct (a three-line circuit in a plane), the bridge case is impossible
and all three targets are axial.

The bridge alternative also forces many aggregate supports.  Put

\[
\begin{aligned}
 R&=\{v\in G:e_i^{(v)}\in L_r^{(v)}\},\\
 S&=\{v\in G:e_i^{(v)}\in L_s^{(v)}\},\\
 M&=G\setminus(R\cup S).
\end{aligned}                                                   \tag{12}
\]

Then \(|R|,|S|\le2\), every site of \(M\) is a genuine nonzero mixture of
the two field directions, and

\[
\begin{aligned}
 S\subseteq P\subseteq S\cup M, |P|=2&\quad\Longrightarrow\quad
                                      \lambda_{rP}\ne0,\\
 R\subseteq Q\subseteq R\cup M, |Q|=2&\quad\Longrightarrow\quad
                                      \lambda_{sQ}\ne0.
\end{aligned}                                                   \tag{13}
\]

The two forced pair families in (13) are nonempty and have distinct
representatives.  This is the concrete support input left for the
common-power equations.

## 2. Four-cover and site cover

For a line field \(L_r=(L_r^{(u)})\), let

\[
 {\cal O}_2(L_r)=\sum_{P\in\binom U2}
   \left(\bigotimes_{u\in P}V_u\right)
   \otimes\left(\bigotimes_{u\notin P}L_r^{(u)}\right).           \tag{14}
\]

Multiplying a term \(A_r(P)\) by two rows leaves arbitrary factors only at
the two missing sites.  Hence (3) gives

\[
                         X_i\in\sum_{r=0}^2{\cal O}_2(L_r).       \tag{15}
\]

If \(e_i^{(u)}\notin W_u\) at three sites, quotient by \(W_u\) at those
three sites.  Every summand on the right of (15) has only two moving sites
and is killed, while the pure target has a nonzero quotient.  Thus each
target lies in \(W_u\) at least four times, proving the first part of (5).

For the site cover, fix \(u\), choose
\(\eta\in W_u^\perp\), and contract every other site by covectors
\(\ell_v\).  Only terms whose missing pair contains \(u\) survive.  Keeping
the two endpoint orders gives a \(3\times3\) scalar matrix of the form

\[
                         M=xR^{\mathsf T}+Cy^{\mathsf T},          \tag{16}
\]

where

\[
 x_i=\eta(p_{i,u}),\qquad y_j=\eta(s_{j,u}),                     \tag{17}
\]

and \(C_i,R_j\) are the complete contracted sums with the other row at the
second endpoint.  Thus \({\rm rank}\,M\le2\), with all aggregate
cancellation retained.  Equation (3), on the other hand, says

\[
 M=\operatorname {diag}\left(
   \eta(e_0^{(u)})\prod_{v\ne u}\ell_v(e_0^{(v)}),
   \eta(e_1^{(u)})\prod_{v\ne u}\ell_v(e_1^{(v)}),
   \eta(e_2^{(u)})\prod_{v\ne u}\ell_v(e_2^{(v)})\right).       \tag{18}
\]

Choose the \(\ell_v\)'s nonzero on all target factors.  If all three target
vectors lay outside \(W_u\), a covector \(\eta\in W_u^\perp\) could be
chosen nonzero on all three: finitely many proper hyperplanes do not cover a
complex vector space.  Then (18) would have rank three, contradicting (16).
This proves the site cover.

If every \(\dim W_u\le2\), the three row bounds in (5) give at least twelve
target-axis incidences, while the six local dimensions allow at most twelve.
Equality holds everywhere.  Every \(W_u\) is therefore a coordinate plane,
each colour is omitted twice, and each site omits one colour.  This is (6).

## 3. Five good sites separate the response modules

At a good site \(v\in G\), extend
\(a_0^{(v)},a_1^{(v)},a_2^{(v)}\) to a basis of \(V_v\).  For a good-site
coordinate word \(w\), write \(d(w,r^5)\) for the number of positions not
equal to the field symbol \(r\).  The shadow on \(G\) of
\({\cal O}_2(L_r)\) is contained in

\[
                         {\cal B}_r=\{w:d(w,r^5)\le2\}.            \tag{19}
\]

These three balls are disjoint, because a common word would imply

\[
       5=d(r^5,s^5)\le d(r^5,w)+d(w,s^5)\le4.                    \tag{20}
\]

Expand \(e_i^{(v)}\) in the chosen basis and let \(T_v\) be its nonzero
coordinate support.  The good-site support of the pure tensor \(X_i\) is the
full Cartesian box \(\prod_{v\in G}T_v\).  Equations (15) and (19) imply

\[
                         \prod_{v\in G}T_v
                         \subseteq{\cal B}_0\cup{\cal B}_1\cup{\cal B}_2.
                                                                    \tag{21}
\]

We use the following elementary five-site box lemma.

**Lemma 3.1 (axial or binary).**  If a Cartesian box on five sites satisfies
(21), then either

* \(T_v=\{r\}\) at at least three sites for one \(r\); or
* for a pair \(r\ne s\), every \(T_v\subseteq\{r,s\}\), with at most two
  singleton supports \(\{r\}\) and at most two singleton supports \(\{s\}\).

The alternatives are disjoint and the field or field pair is unique.

**Proof.**  Seek a word in the box using each of the three field symbols at
most twice.  Give every field two capacity slots, and give a private slot to
each site whose support contains a transverse basis symbol.  Join a site to
the slots represented in its support.  If Hall fails on a site set, delete
the sites having private slots.  The remaining set has size greater than
twice the number of field symbols in its union.  A one-symbol union gives
three singleton \(\{r\}\) sites.  A two-symbol union can fail only on all five
sites, giving the binary alternative.  A three-symbol union has capacity
six and cannot fail.  If Hall does not fail, its matching gives a word with
no field occurring three times, contrary to (21).  The stated singleton
bounds and uniqueness are immediate.  \(\square\)

In the first alternative every word belongs to the single ball
\({\cal B}_r\).  In the second, words occur in both \({\cal B}_r\) and
\({\cal B}_s\), and in no third ball.

## 4. Boundary words force alignment or coincidence

Suppose first that \(T_v=\{r\}\) at at least three good sites.  If this
happens at four sites, (9) already holds.  Otherwise it happens at exactly
three sites.  Choose a non-\(r\) coordinate from each of the other two target
factors.  The resulting good word has distance exactly two from \(r^5\).
By (20), only the \(r\)-field module can produce it.  Its two deviations
force the missing pair in (2) to be exactly those two good sites.  The local
factor left at \(o\) on the response side is therefore \(a_r^{(o)}\), while
the nonzero target coefficient has local factor \(e_i^{(o)}\).  Hence

\[
                         e_i^{(o)}\in L_r^{(o)},                   \tag{22}
\]

which supplies the fourth agreement in (9).

Now take the binary alternative \(r,s\).  To form a word at distance exactly
two from \(r^5\), choose the \(s\)-coordinate at two sites, including every
singleton-\(s\) site, and the \(r\)-coordinate elsewhere.  Such a choice is
always possible because each singleton class has size at most two.  The same
boundary-word argument gives \(e_i^{(o)}\in L_r^{(o)}\).  Interchanging
\(r,s\) gives \(e_i^{(o)}\in L_s^{(o)}\), proving (11).

The argument applies to every supported boundary word.  For an \(r\)-centred
word, its two \(s\)-sites are exactly the pairs \(P\) in the first line of
(13).  Its target coefficient is nonzero, so the unique contributing
aggregate coefficient \(\lambda_{rP}\) is nonzero.  The second line is
symmetric.  The two families are nonempty.  A pair in the first contains
\(S\) and avoids \(R\), while a pair in the second contains \(R\) and avoids
\(S\).  They are distinct unless \(R=S=\varnothing\); in that case \(M=G\)
and either family contains all ten good-site pairs, so distinct
representatives can again be chosen.

Finally, two bridge targets would both lie at \(o\) on coincident field
lines.  Any two pairs among three field labels intersect, so the two
coincidence relations force the same local line; the two target vectors
would be proportional.  Thus at most one target bridges.  Two axial targets
cannot be assigned the same field because two four-site agreement sets
intersect.  If a bridge joined the fields assigned to the two axial targets,
their good-site agreement sets, each of size at least three, would intersect
at a site where all three target vectors lie in the same two-plane.  This
contradicts target independence and completes Theorem 1.3.

## 5. Singleton collisions and the exact active-family residual

Put

\[
\begin{aligned}
 H_r&=\{P:\lambda_{rP}\ne0\},\\
 J_r&=H_r\cap\binom G2,\\
 I_r&=H_r\cap\{\{o,v\}:v\in G\}.
\end{aligned}                                                    \tag{23}
\]

Thus \(J_r\) is the good-pair layer and \(I_r\) is the bad-site star
layer.  The disjointness (20) splits the response equations into their
three field modules after restricting only the five good coordinates.
Every \(H_r\) is nonempty.  In the bridge case the two boundary components
of the bridge target are both nonzero, as witnessed by the two forced
families in (13).

We first retain the response input which removes the spurious two-family
Hall failure.

**Lemma 5.1 (singleton collisions).**  For distinct fields \(r,s\), one
cannot have

\[
                            H_r=H_s=\{P\}.                         \tag{24}
\]

More generally, let target \(t\) be axial on field \(s\), and put

\[
                  D_t^{(s)}=\{u:e_t^{(u)}\notin L_s^{(u)}\}.
\]

If \(D_t^{(s)}=P\), then one cannot have

\[
                 H_r=\{P\},\qquad P\in H_s,\qquad r\ne s.         \tag{25}
\]

**Proof.**  For (24), choose a diagonal target row whose component in one
of the two singleton field modules is nonzero and whose component in the
other is zero.  In the bridge normal form, the axial field-zero target
separates fields zero and two; the other comparisons use an axial target
directly.  The nonzero singleton equation says \(B_{tt}(P)\ne0\), while
the zero singleton equation says \(B_{tt}(P)=0\).

For (25), the singleton \(r\)-module gives \(B_{tt}(P)=0\).  Quotient the
\(s\)-module diagonal equation at the two sites of \(P=D_t^{(s)}\) by the
two field lines \(L_s\).  Every missing pair other than \(P\) is killed,
whereas the target quotient is a nonzero pure tensor.  Hence
\(B_{tt}(P)\ne0\), a contradiction.  Both arguments take place after the
good-site module split and retain all aggregate cancellation.  \(\square\)

The power inputs are the exact
[sole-defect distinct-lift obstruction](sole-defect-distinct-lift-common-power-obstruction.md)
and the
[sole-defect two-pair obstruction](sole-defect-two-pair-common-power-obstruction.md).
Their field-selection consequences say that \(H_0,H_1,H_2\) have an
ordinary system of distinct representatives, but no locally separable one.
At the bad site there are only three local matroids:

\[
\begin{array}{c|c}
\text{bad-site matroid}&\text{nonseparable incident-field sets }K\\ \hline
\text{three distinct lines in a plane}&|K|=2,\\
L_0^{(o)}=L_2^{(o)}\ne L_1^{(o)}
  &\{0\},\{2\},\{0,1\},\{1,2\},\\
\text{rank one}&\varnothing\ne K\ne\{0,1,2\}.
\end{array}                                                       \tag{26}
\]

Here \(K=\{r:o\in P_r\}\).  Combining the two power theorems with Lemma 5.1
gives the closed ordinary-Hall alternative and the exact remaining
active-family incidence list below.  “No SDR” means no system of pairwise
distinct representatives of the displayed families; an empty displayed
family automatically has no SDR.

1. **Ordinary SDR is forced.**  In every bad-site matroid, ordinary Hall
   failure and (24) would force

   \[
           H_0\cup H_1\cup H_2=\{P,Q\},\qquad P\ne Q.              \tag{27}
   \]

   Up to field relabelling, the only cardinality profiles are

   \[
                         (2,2,2),\qquad(2,2,1),\qquad(2,1,1),      \tag{28}
   \]

   and in the last profile the two singleton fields use different pairs.
   All 65 resulting degenerate power ideals are unit ideals by the
   sole-defect two-pair obstruction.  Thus (27)--(28) are closed, and every
   survivor belongs to one of the nonseparable-SDR cases below.

2. **All axial, three-line circuit.**  Every ordinary SDR must use exactly
   two bad-site-star pairs.  Equivalently,

   \[
   (J_0,J_1,J_2),\quad(I_0,I_1,I_2),\quad
   (I_r,J_s,J_t)\quad(\{r,s,t\}=\{0,1,2\})                         \tag{29}
   \]

   all have no SDR.  At least one of
   \((J_r,I_s,I_t)\) has an SDR; these are precisely the surviving
   \(K\)-sets of size two.

3. **All axial, one coincident pair.**  Relabel the equal fields as zero
   and two.  Every ordinary SDR must choose exactly one of its field-zero
   and field-two pairs from the bad-site star.  Equivalently,

   \[
                         (J_0,H_1,J_2),\qquad(I_0,H_1,I_2)         \tag{30}
   \]

   have no SDR.  At least one of
   \((I_0,H_1,J_2)\) and \((J_0,H_1,I_2)\) has an SDR.

4. **All axial, rank one.**  Every ordinary SDR is mixed between the two
   layers.  Equivalently,

   \[
                         (J_0,J_1,J_2),\qquad(I_0,I_1,I_2)         \tag{31}
   \]

   have no SDR.  At least one of the six nonempty proper
   choices of star fields has an SDR.

Conditions (29)--(31), together with (24)--(25), are a finite Hall
description: whenever all three displayed families are nonempty, “no SDR”
is exactly the disjunction that two of them are the same singleton or that
their total union has size at most two.

The bridge branch sharpens further.  Use the normal form in which fields
zero and two bridge, fields zero and one carry the axial targets, and
\(L_0^{(o)}=L_2^{(o)}\).

**Corollary 5.2 (bridge active-family census).**

1. If the bad-site span has dimension two, then

   \[
   I_1=\varnothing,\qquad
   I_0=\varnothing\ \text{or}\ I_2=\varnothing\
       \text{or}\ I_0=I_2=\{\{o,v\}\}\text{ for some }v,           \tag{32}
   \]

   Here \(I_0\) and \(I_2\) are not both empty.  Moreover, at least one of
   the following good-layer Hall alternatives holds
   (the alternatives may overlap):

   \[
   J_0=H_1=\{P\},\qquad
   H_1=J_2=\{P\},\qquad
   |J_0\cup H_1\cup J_2|\le2.                                    \tag{33}
   \]

   In the first alternative \(I_0\ne\varnothing\), and in the second
   \(I_2\ne\varnothing\), by (24).

   Moreover, the bridge profile (12) must obey

   \[
                              |R|=2\quad\text{or}\quad |S|=2.      \tag{34}
   \]

   Thus only the five profiles

   \[
     (|R|,|S|,|M|)\in
     \{(2,0,3),(2,1,2),(2,2,1),(0,2,3),(1,2,2)\}                 \tag{35}
   \]

   survive, accounting for \(10+30+30+10+30=110\) of the 141
   labelled bridge boxes for the fixed field pair.

   The 110 boxes split into three exact active-family strata:

   * if \(|S|=2\) and \(|R|<2\) (40 boxes), then
     \(J_0=H_1=\{S\}\) and \(I_0\ne\varnothing\);
   * if \(|R|=2\) and \(|S|<2\) (40 boxes), then
     \(H_1=J_2=\{R\}\) and \(I_2\ne\varnothing\);
   * if \(|R|=|S|=2\) (30 boxes), then

     \[
       J_0=H_1=\{S\},\quad\text{or}\quad
       H_1=J_2=\{R\},\quad\text{or}\quad
       J_0\cup H_1\cup J_2=\{R,S\}.                              \tag{35a}
     \]

   The incident layers in all three strata are still exactly those in
   (32), with at least one nonempty.

2. If the bad-site span has dimension one, then

   \[
                         (J_0,J_1,J_2),\qquad(I_0,I_1,I_2)         \tag{36}
   \]

   have no SDR.  The forced good families \(J_0,J_2\) have distinct
   representatives.  If \(J_1\ne\varnothing\), its exact Hall alternatives
   are the three in (33), with \(H_1\) replaced by \(J_1\), and (34)
   follows.  If \(|R|,|S|\le1\), necessarily \(J_1=\varnothing\) and
   \(I_1\ne\varnothing\).  At least one mixed-layer triple has an SDR.

**Proof.**  In the dimension-two coincident matroid, (26) says that a
separable SDR is exactly one in which the field-zero and field-two
representatives are both good or both incident.  The forced families in
(13) give distinct good representatives for \(J_0,J_2\).  Hence an
incident member of \(H_1\) would immediately give a separable SDR, proving
\(I_1=\varnothing\).  Hall applied to \((J_0,H_1,J_2)\) gives (33), since
\(J_0,J_2\) already have distinct representatives.  Applying the same
argument to \((I_0,H_1,I_2)\), and observing that a good \(H_1\)-pair is
different from every incident pair, gives (32).  The two-pair obstruction
forces an ordinary SDR, so the two incident families cannot both be empty.

The first forced family in (13) is a singleton exactly when \(|S|=2\);
the second is a singleton exactly when \(|R|=2\).  If neither is a
singleton, their union has more than two pairs, so none of the Hall
alternatives (33) can hold.  If only the first forced family is a
singleton, the other forced family together with it contains at least
three pairs, so only the first alternative in (33) remains; the case with
the fields swapped is symmetric.  If both are singletons, they are the
distinct pairs \(S,R\), and (33) becomes exactly (35a).  This proves
(34)--(35a).  In rank one, (26) forbids exactly the all-good and
all-incident SDRs, giving (36); the same Hall calculation gives the
remaining assertions.  \(\square\)

## 6. Sole-defect closure and scope

The theorem preserves arbitrary endpoint order, multi-site rows, parallel
aggregate terms, transverse local directions, and complex cancellation.  It
does not assume that a zero sum vanishes termwise.

For one deficient site, the two-pair branch (27)--(28) is closed, so every
survivor has an ordinary SDR.  The
[sole-defect packet obstruction](sole-defect-nonseparable-packet-common-power-obstruction.md)
now closes every such SDR.  Its good-site selectors turn a selected good
pair into one isolated lift and a selected incident pair into an anchored
packet with at most four good arms.  Any packet support with a locally
separable alternative SDR reduces to the distinct-lift theorem.  The exact
remaining census consists of 157 locally nonseparable packet orbits:
145 coefficient-normalizable cases and twelve one-parameter full-packet
families.  Every corresponding common-power ideal is the unit ideal,
uniformly over the nonzero parameter.

Consequently, the layer-Hall types (29)--(31) and the 110 bridge boxes
(32)--(36) are intermediate audited classifications, not open cases:

**Corollary 6.1.**  A coherent three-line field satisfying all nine
responses and the common-power equations cannot have exactly one deficient
local frame.

With two or more deficient sites the five-letter balls no longer give the
separation (20); the universally valid information is (5), together with
the complete coordinate-plane form (6) when all six sites are deficient.

The standalone checker
[verify_degenerate_three_line_field_response_normal_form.py](../computations/verify_degenerate_three_line_field_response_normal_form.py)
audits the incidence equality, the rank-two contraction, every five-site
support box after collapsing arbitrary transverse directions to one symbol,
all binary bridge patterns, the forced-pair statement, the local
separability table (26), the 110-box bridge reduction, and the finite
agreement-set and Hall consequences.
