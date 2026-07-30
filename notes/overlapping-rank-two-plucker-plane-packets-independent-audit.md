# Independent audit: overlapping rank-two Plucker plane packets

## 1. Verdict

The block reduction in
[`overlapping-rank-two-plucker-plane-packets.md`](overlapping-rank-two-plucker-plane-packets.md)
is **sound with the local scope and quantifier repairs now incorporated**.
Lemmas 2.1--2.2,
Theorem 3.1, Corollaries 3.2 and 3.4, Theorem 4.1, and Proposition 5.1
all survive direct tensor and defect-component checks.  No new diffuse
overlapping-row branch was found.

Three qualifications were checked and are now explicit in the routed
proof theorem.

1. The outcome retains the setup hypothesis that the six E2 primitives
   span the three-dimensional defect space.  Gauge rigidity and defect three
   alone do not state this; the existing coefficient-rank theorem supplies it
   on the dense six-row locus.
2. Corollary 3.3 uses the aligned-diagonal propagation lemma proved in
   Section 4 below; it is not being inferred from Theorem 3.1 alone.
3. On the all-balanced stratum the complement-sum locus equals `K(D)`, but
   the multiresponse theorem constrains rather than eliminates that core.
   The primary note now states that this is not a closure.

These are local repairs; none changes the four alternatives in Theorem 3.1.

## 2. Audit of the tensor lemmas

For Lemma 2.1, a rank-two tensor

\[
 x_i\otimes y_j+y_i\otimes x_j
\]

cannot have either endpoint factor pair dependent.  Its two flattening
images are therefore exactly the displayed two-planes.  This uses neither a
coordinate choice nor any hidden nonvanishing assumption.

For Lemma 2.2, the first zero product and nonzero `(Z_bb)_ij` force both
components of `s_b` to be nonzero.  Rank-one tensor uniqueness then gives

\[
 s_{b,i}=\gamma p_{a,i},\qquad s_{b,j}=-\gamma p_{a,j}.
\]

The reverse product similarly gives

\[
 p_{b,i}=\beta s_{a,i},\qquad p_{b,j}=-\beta s_{a,j}.
\]

Substitution yields exactly
`(Z_bb)_ij=-beta gamma (Z_aa)_ij`.  The signs and endpoint order are correct.
The assumption that all four colour-`a` components are nonzero is used
exactly here.

## 3. Exhaustiveness of Theorem 3.1

If two diagonals align, their nonzero proportionality constants and
`rank(q_ij)=2` give alternative 1 by Lemma 2.1.  Otherwise at least two
diagonals, say `b,c`, escape.  With `a` the remaining colour,

\[
 R_b+R_c
 =\operatorname{span}\{\alpha_{ac},\alpha_{ca},
                         \alpha_{ab},\alpha_{ba}\}=P.
\]

Diagonal escape makes `h_ij` vanish on `P`.

* If `P=D`, this is the complement-sum alternative.
* If `P` is proper and `sigma|P` is nonzero, one of its four displayed
  generators has nonzero `sigma`.  Since `h_ij=0` there, its response is the
  same nonzero scalar multiple of `q_ij`, giving the mixed physical planes.
* If `sigma|P=0`, then `ell_ij|P=0` and all four mixed blocks through `a`
  vanish.  An endpoint hole is alternative 4.  With no hole, Lemma 2.2
  makes the escaped `(Z_bb)_ij` a nonzero multiple of `(Z_aa)_ij`, so the
  latter escapes as well.  Diagonal escape kills `R_a`; the explicit
  hypothesis that all six primitives span `D` gives `P+R_a=D`, hence the
  complement-sum alternative.

This covers every alignment count and does not assume independence inside
an individual reverse space.  In particular, zero-, one-, and two-
dimensional reverse spaces are all included.

Corollary 3.4 also checks endpoint by endpoint.  For example,
`p_(a,i)=0`, `p_(a,j)!=0`, and the two vanished outgoing blocks force
`s_(b,i)=s_(c,i)=0`; the other three cases follow by endpoint reversal and
interchanging `p` with `s`.

## 4. The Corollary 3.3 repair

As written, a fixed condition `R_b+R_c=D` need not be the sum belonging to
the two escaped colours selected in the proof of Theorem 3.1.  The claimed
conclusion nevertheless follows after adding the following short tensor
fact.

**Aligned-diagonal propagation.**  On a rank-two block on which all six
off-diagonal responses are scalar multiples of `q_ij`, if one nonzero
diagonal `(Z_aa)_ij` is a scalar multiple of `q_ij`, then every diagonal is
a scalar multiple of `q_ij`.

To verify it, rescale and choose endpoint bases

\[
 (p_{a,i},s_{a,i}),\qquad (s_{a,j},p_{a,j})
\]

so that `q_ij=I_2`.  For another colour `b`, the two mixed response
identities first put all four colour-`b` vectors in these endpoint planes:
projecting `Z_ab` to either endpoint quotient kills the colour-`a` summand
and forces the corresponding `s_b` component into the plane, and `Z_ba`
does the same for `p_b`.  In the displayed bases the identities then have
the unique coordinate form

\[
\begin{aligned}
 s_{b,i}&=(t,\lambda), &s_{b,j}&=(\lambda,-t),\\
 p_{b,i}&=(\mu,u),     &p_{b,j}&=(-u,\mu).
\end{aligned}
\]

Consequently

\[
 (Z_{bb})_{ij}=(\lambda\mu-tu)I_2.
\]

The theorem's diagonal-liveness assumption makes this multiple nonzero.
Thus either all three diagonals align, or all three escape.  In the latter
case any fixed pair satisfying `R_b+R_c=D` consists of escaped colours, so
diagonal escape gives `h_ij|D=0`.  This proves Corollary 3.3 with its sharper
present quantifier, but the propagation lemma and this argument must be
stated.  The simpler alternative is to require `R_b+R_c=D` for every
distinct pair.

## 5. Plane gluing and packet labels

The diagonal packet gluing is exact: two subsets of a three-colour set,
each of size at least two, share a colour, and that common physical pair
identifies the two incident image planes.  Connected propagation therefore
defines the asserted sitewise plane bundle.

The mixed packet statement is also exact for a **fixed** space `P` and a
**fixed** physical generator `alpha_rs` with nonzero `sigma`.  Every
rank-two block satisfying `h_ij|P=0` has

\[
 (Z_{rs})_{ij}=\sigma(\alpha_{rs})q_{ij},
\]

so incident blocks use the same pair
`span{p_(r,i),s_(s,i)}`.  This does not by itself glue differently labelled
packets.  The final rank-one-incidence sentence is valid in the ternary
ambient spaces, where two distinct two-planes intersect in a line, but it
should be read as the next gate rather than as an already proved gluing
theorem.

## 6. Complement-sum component classification

For each bipartite rank-three component, direct evaluation on its shore
sign vector gives

\[
 h_{ij}(\zeta_C)=\Delta_C-\zeta_C(i)-\zeta_C(j).
\]

Since these vectors form a basis of `D`, equation (22) is necessary and
sufficient.  The three endpoint cases, including isolated vertices, follow
immediately.  A complement-sum pair can meet at most two disjoint
components, so whenever such a pair exists at most two of the three defect
components are imbalanced.  The phrase "at least one ... is balanced"
should retain this existence qualifier; the next sentence correctly says
that an all-imbalanced chart has empty complement-sum locus.

If all three components are balanced, `sigma|D=0` and hence

\[
 h_{ij}|D=0\iff\ell_{ij}|D=0\iff ij\in K(D).
\]

The two-imbalance and one-imbalance signatures listed afterward are
exhaustive.  In the latter case an endpoint outside the unique imbalanced
component cannot lie alone in a balanced bipartite component, so it must
lie in a nonbipartite component.

## 7. Exact scope retained by the audit

The result applies only to rank-two `q_ij`, assumes all three diagonal
blocks are nonzero, assumes the six E2 primitives span `D`, and uses the
audited differential-Plucker diagonal-escape implication.  Rank-zero or
rank-one source blocks, zero diagonal blocks, endpoint-hole propagation,
mixed-imbalance complement-sum blocks, and differently labelled packet
incidence remain open.  Within that scope, the local reduction is valid.
