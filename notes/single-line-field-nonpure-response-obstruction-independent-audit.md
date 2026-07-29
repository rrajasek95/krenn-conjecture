# Independent audit of the one-/two-line-field response obstruction

## Verdict

This is a clean-room adversarial audit of
[the primary line-field note](single-line-field-nonpure-response-obstruction.md).
The one- and two-line-field theorem is correct.  In particular, the passage
from the three-site quotient to plane incidence, the equality case of the
incidence count, the omission-pair quotient, the rank-one flattening, the
four-site Segre secant argument, and the final pigeonhole contradiction all
remain valid with arbitrary coefficients, arbitrary complex cancellation,
and arbitrary multi-site response rows.

The conditional three-field alignment lemma and the direct-sum statement are
also correct.  The audit found one wording-level scope ambiguity, now repaired
in the primary note: the alignment conclusion uses only the three diagonal
equations, but the full display (24) uses the additional six off-diagonal
equations.  This does not affect Theorem 1.1 or Lemma 6.1.

The standalone
[independent checker](../computations/audit_single_line_field_nonpure_response_obstruction_independent.py)
imports neither the primary checker nor project code.  It uses bit masks,
an exhaustive Cartesian-box test rather than the primary dynamic program,
an exact finite-field flattening audit, and both symbolic and finite-field
checks of the Segre secant.

## 1. Response-space inclusion

Use the local square-zero algebra

\[
 A_u=\mathbb C\oplus V_u,\qquad V_u^2=0,
 \qquad \mathcal R_U=\bigotimes_{u\in U}A_u.            \tag{A1}
\]

Let \(P=\{v,w\}\).  The four-site tensor \(A(P)\) has an \(L_u\)
factor at every site outside \(P\).  In \(p_i s_jA(P)\), a row component
at a site outside \(P\) collides with that fixed positive-degree factor and
vanishes.  Two row components at the same site also vanish.  Therefore every
surviving term puts its two arbitrary factors precisely at \(v,w\), in either
endpoint order.  It follows, without restricting the supports of the rows,
that

\[
 p_i s_jA(P)\in
 \left(V_v\otimes V_w\right)
 \otimes\bigotimes_{u\notin P}L_u.                    \tag{A2}
\]

The analogous statement holds for \(B(P)\) and \(M\).  Summing all pairs and
all aggregate coefficients gives

\[
                  p_i s_jF\in\mathcal O_2(L)+\mathcal O_2(M).     \tag{A3}
\]

This is a subspace containment, so coincident descriptions, zero aggregate
coefficients, and cancellation between pairs or fields do not change it.
No termwise noncancellation claim is being made.

## 2. The three-site quotient and incidence equality

Put \(W_u=L_u+M_u\).  Suppose a nonzero pure tensor

\[
                         x=\bigotimes_{u\in U}x_u
       \in\mathcal O_2(L)+\mathcal O_2(M)                         \tag{A4}
\]

has \(x_u\notin W_u\) on a three-set \(T\).  Apply \(V_u\to V_u/W_u\)
at those three sites.  Every summand in either osculating space has at most
two moving sites.  At least one site of \(T\) therefore retains a fixed
factor in \(L_u\) or \(M_u\), and that summand is killed.  The image of \(x\),
however, is a tensor product of nonzero factors and is nonzero.  This
contradiction proves that \(x_u\in W_u\) on at least four sites.

For the three independent targets define

\[
                 S_i=\{u:e_i^{(u)}\in W_u\}.                       \tag{A5}
\]

The quotient lemma gives

\[
             \sum_i|S_i|\ge12.                                    \tag{A6}
\]

At a fixed site, the plane \(W_u\) can contain at most two of the three
independent target axes.  Summing this local upper bound gives the reverse
inequality.  Equality is consequently forced in every constituent bound:

\[
 |S_i|=4\quad(i=0,1,2),\qquad
 \dim W_u=2,
 \quad W_u\text{ contains exactly two target axes at every }u.    \tag{A7}
\]

Each site therefore omits exactly one target colour, while each colour is
omitted at exactly two sites.  Hence

\[
                       P_i=U\setminus S_i                           \tag{A8}
\]

are disjoint pairs partitioning \(U\).  Moreover, \(\dim W_u=2\) forces
\(L_u\ne M_u\) at every site.  Thus no coincident-line exceptional case
survives the equality count.  If only one field were present, the total
local incidence capacity would be at most six, so the same argument would
already give a contradiction.

The independent checker enumerates all \(7^6\) possible local target-axis
incidence masks of size at most two.  Exactly

\[
                         \frac{6!}{2!2!2!}=90                       \tag{A9}
\]

meet the three lower bounds, and every one has precisely the partition
described above.

## 3. The omission-pair quotient and rank-one flattening

Fix \(i\) and quotient by \(W_u\) at both sites of \(P_i\).  The target
survives because its two factors there lie outside \(W_u\).  A line-field
summand survives only if both quotient sites are among its at most two moving
sites.  Its moving pair is therefore exactly \(P_i\).  Grouping the surviving
\(L\)- and \(M\)-terms gives

\[
 \bar X_{i,P_i}\otimes X_{i,C_i}
       =Z_L\otimes L_{C_i}+Z_M\otimes M_{C_i},
 \qquad C_i=U\setminus P_i.                            \tag{A10}
\]

The right factors are independent.  Indeed, proportional decomposable
tensors have proportional local factors at every site, whereas (A7) gives
\(L_u\ne M_u\) at all four sites of \(C_i\).

Let \(Q\) be the quotient of the left flattening space by the line
\(\mathbb C\bar X_{i,P_i}\).  Applying \(Q\otimes\mathrm{id}\) to (A10)
yields

\[
 [Z_L]\otimes L_{C_i}+[Z_M]\otimes M_{C_i}=0.          \tag{A11}
\]

Independence of the two right factors forces both quotient classes to
vanish.  Thus \(Z_L=\alpha\bar X_{i,P_i}\) and
\(Z_M=\beta\bar X_{i,P_i}\).  Substitution into (A10), followed by
injectivity of tensoring with the nonzero vector \(\bar X_{i,P_i}\), gives

\[
                   X_{i,C_i}=\alpha L_{C_i}+\beta M_{C_i}.         \tag{A12}
\]

This proves the flattening step without assuming that either coefficient is
nonzero and without choosing a functional whose value might accidentally
vanish.  The independent checker also exhausts the same coefficient
separation in a \(3\)-by-\(4\) flattening over \(\mathbb F_5\), larger than
the minimal matrix used by the primary checker.

## 4. Secant rigidity and the final contradiction

Choose one site \(v\in C_i\) and flatten there against the other three.
The vectors spanning \(L_v,M_v\) are independent.  The remaining three-site
products are also independent because their local lines differ at every one
of those sites.  In bases beginning with these two factors, the combination
in (A12) has a \(2\)-by-\(2\) minor equal, up to nonzero basis factors, to

\[
                              \alpha\beta.              \tag{A13}
\]

If both coefficients were nonzero, the flattening would have rank two, while
the pure tensor \(X_{i,C_i}\) has rank one.  Hence one coefficient vanishes,
and proportionality of nonzero pure tensors then gives exactly one of

\[
 \begin{array}{ll}
 e_i^{(u)}\in L_u& (u\in C_i),\\
 \text{or}\qquad e_i^{(u)}\in M_u& (u\in C_i).
 \end{array}                                             \tag{A14}
\]

Assign each of the three target colours the field supplied by (A14).  Two
colours receive the same one of \(L,M\).  Their disjoint omission pairs have
four-site complements whose intersection has size two.  At either common
site, that single field line would contain two independent target axes.  This
is impossible and proves the two-field theorem.

The example in Section 5 of the primary note is a genuine warning, not a
counterexample to the proof.  When the fields differ only at one site, the
two coordinate terms of

\[
 (a_0+b_0)\otimes a_1\otimes a_2\otimes a_3\otimes t_4\otimes t_5          \tag{A15}
\]

lie in the two different radius-two spaces, while the Cartesian support of
the whole pure tensor is contained in neither one separately.  The
incidence-equality and pair-quotient steps are therefore genuinely needed.

## 5. Independent reconstruction of the three-frame lemma

Now assume the three lines \(L_u^{(0)},L_u^{(1)},L_u^{(2)}\) form a basis at
each site.  In this coordinate basis, \(\mathcal O_2(L^{(r)})\) is spanned by
the words at Hamming distance at most two from \(r^6\).  Let
\(x=\bigotimes_u x_u\) be pure and define the nonempty coordinate supports

\[
                    T_u=\{r:[L_u^{(r)}]x_u\ne0\}.       \tag{A16}
\]

The coordinate support of \(x\) is the full Cartesian box
\(\prod_uT_u\): every coefficient in that box is a product of nonzero local
coefficients.  If \(x\in\sum_r\mathcal O_2(L^{(r)})\), every word in the box
must therefore have some symbol occurring at least four times.

Suppose no symbol \(r\) has \(T_u=\{r\}\) at four sites.  Replace each of the
three symbols by three capacity slots and join site \(u\) to the slots whose
symbol lies in \(T_u\).  Hall can fail for a site set \(D\) only if

\[
                  |D|>3\left|\bigcup_{u\in D}T_u\right|.           \tag{A17}
\]

If the union has one symbol, all supports in \(D\) are that singleton and
the assumption gives \(|D|\le3\).  If the union has two symbols, its capacity
is six, at least the total number of sites.  If it has three, its capacity is
nine.  Hall consequently supplies a choice \(r_u\in T_u\) using every symbol
at most three times.  That is a word of the Cartesian box lying outside all
three osculating spaces, a contradiction.  Hence \(x_u\in L_u^{(r)}\) at
least four sites for some \(r\).

Apply this to the three independent targets.  Two target colours cannot be
assigned the same field: two four-site agreement sets overlap in at least
two sites, where one line would contain both target axes.  The assignments
are therefore a permutation.  This proves the conditional alignment lemma,
but it neither identifies nor couples the remaining two deviant sites.

The independent checker directly enumerates all \(7^6=117{,}649\) local
support boxes.  For each box it searches its Cartesian words, independently
checks the capacitated Hall inequalities, and verifies the exact equivalence

\[
 \begin{split}
 &\text{every box word has a symbol occurring at least four times}\\
 &\hspace{20mm}\Longleftrightarrow
 \text{some symbol is singleton-supported at least four sites}.
                                                                    \tag{A18}
 \end{split}
\]

There are \(1{,}731\) such boxes, agreeing with the separate count

\[
 3\left(\binom64 6^2+\binom65 6+1\right)=1{,}731.       \tag{A19}
\]

## 6. Direct-sum claim and its exact hypothesis

For distinct \(r,s\), the constant words \(r^6,s^6\) have Hamming distance
six.  A word in both radius-two balls would contradict

\[
 6=d(r^6,s^6)\le d(r^6,w)+d(w,s^6)\le4.                \tag{A20}
\]

Thus the three osculating spaces have disjoint coordinate bases and form a
direct sum.  Each ball contains

\[
                 1+2\binom61+2^2\binom62=73.                         \tag{A21}
\]

words, for total coordinate dimension \(219\).  A target aligned to field
\(r\) on four sites has its entire Cartesian support inside that ball and in
no other one.

Consequently the diagonal response \(p_i s_iF=X_i\) splits with \(X_i\) in
the component of its assigned field and zero in the other two components.
If one additionally assumes the six equations \(p_i s_jF=0\) for \(i\ne j\),
then those equations split componentwise as well, giving exactly display
(24) of the primary note.  Without the off-diagonal hypotheses, the
off-diagonal part of (24) is not asserted.

This is only a response-space normal form.  It does not show that a general
edge-block multiplier resolves into three line fields, and it does not close
the residual three-field case.  Any further contradiction must use the
common-power equations or another mechanism coupling the three field
components.

## 7. Reproduction

From the repository root, run

    .venv/bin/python -m py_compile \
        computations/verify_single_line_field_nonpure_response_obstruction.py \
        computations/audit_single_line_field_nonpure_response_obstruction_independent.py
    .venv/bin/python computations/verify_single_line_field_nonpure_response_obstruction.py
    .venv/bin/python computations/audit_single_line_field_nonpure_response_obstruction_independent.py

The clean replay on 2026-07-27 ended with both checkers passing.  The
independent summary was

    clean-room one-/two-line-field obstruction audit: PASS
    plane-incidence equality cases: 90
    finite-field rank-one flattenings: 3100
    four-site Segre secant: only its two endpoints are pure
    three-frame support boxes: 117649; trapped: 1731
    three radius-two balls: direct coordinate dimension 219
    scope: (24) uses all nine responses; the alignment lemma uses only three diagonals

After the scope clarification, the primary note and primary checker SHA256
hashes are respectively

    1e37c2754d7aea1f5d2566dc6875d2580cec09367fdb10c23611f1d310765a96
    4c8c2981a8530ba7f7c1d23d46091ed1add7fdde998febb26002f7023a27471a

The independent checker SHA256 is

    e623d7da83d403186ea1f840cb8b543a16a6cc751e3cba9f08418f371ef044ad

Control scans found no control characters, trailing whitespace, malformed
inline-TeX escape remnants, or overlong code lines in the audited artifacts.
