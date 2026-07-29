# A common-beta extra plane is impossible at every live size

## 1. Outcome

Continue from
[live-three-zero-extra-singular-shared-star-reduction.md](live-three-zero-extra-singular-shared-star-reduction.md).
Assume there is exactly one additional nonzero singular site (e).  The
only type which can give the shared zero (z_0) a rank-three neighbour is

\[
                 \operatorname {im}P_e=\langle e_0,e_1\rangle .  \tag{1}
\]

Let the live shore have arbitrary even size (2r\ge2), as parity requires,
and suppose every live site has the common centre beta value (mu).

**Theorem 1.1 (common-beta extra-plane injectivity).**  The vanishing
cyclic response at (z_0) forces

\[
                         q_{i z_0}=0                               \tag{2}
\]

at every residual nonzero site (i).  Hence (z_0) has no rank-three
neighbour, contradicting the connected-spanning hypothesis on (G_3(q)).

The case (r=1) is the all-common minimal calculation in
[live-three-zero-minimal-extra-plane-common.md](live-three-zero-minimal-extra-plane-common.md).
The proof below is uniform for (r\ge2).  It does not choose a kernel chart
for (P_e); the arbitrary source-side row plane is retained throughout.

## 2. Normal form

Put

\[
 {cal O}=U\sqcup\{c,d\},\qquad |U|=2r,\qquad |{cal O}|=2r+2,    \tag{3}
\]

where (c,d) are the two residual type-(10) centres.  The standard local
normalization gives

\[
 P_i=I\ (i\in U),\qquad P_c=P_d=D=\operatorname {diag}(1,1,0),
 \qquad
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad
 \mu=1.                                                          \tag{4}
\]

Every internal beta is therefore (1), so

\[
                          q_{ij}={1\over2}P_iHP_j^{\mathsf T}.    \tag{5}
\]

An output change at (e) makes the third row of (P_e) zero.  Its two
nonzero rows span an arbitrary plane

\[
                R=\operatorname {row}P_e\subset\mathbb C^3.      \tag{6}
\]

Contracting the output at (e) by a covector (eta) produces an arbitrary
row

\[
                         p=\eta^{\mathsf T}P_e=(p_0,p_1,p_2)\in R.\tag{7}
\]

Fix one coordinate at (z_0), and write (Z_{i,j}) for the corresponding
entry in output row (j) of (q_{i z_0}).  On binary output rows, every
site of ({\cal O}) behaves identically: an internal edge has weight
(1/2) between opposite colours and zero between equal colours.  All rows
used below have a diagonal source.  The direct quadratic, supported on
(01), therefore contributes zero exactly.

## 3. Two subset transforms kill the binary coordinate rows

Let (S\subset{cal O}) have size (r+1).  Give (S) output colour (0),
give its complement colour (1), contract (e) to (p), and read source
(11).  Exact matching expansion leaves only stars at the sites of (S):

\[
 K_r\bigl((r+2)p_1+rp_2\bigr)
                  \sum_{i\in S}Z_{i,0}=0,qquad
 K_r={(r+1)r!\over2^r}\ne0.                                    \tag{8}
\]

There are two contributions to its scalar.  If the marked pair consists
of two ordinary colour-(1) sites, (e) must pair with a colour-(0)
site and contributes (pHe_0^{\mathsf T}=p_1+p_2).  If (e) is marked,
it contributes (p_1).  Counting the choices gives exactly (8).

There is a second uncontaminated family.  For (|S|=r+3), use the same
binary word and source (00).  Since (r\ge2), this is again a proper
nonempty subset size.  Now (e) cannot occur in the marked pair of a
surviving term, and

\[
 L_r(p_1+p_2)\sum_{i\in S}Z_{i,0}=0,qquad
 L_r={(r+2)(r+1)r!\over2^r}\ne0.                                \tag{9}
\]

The two linear forms in (8)--(9) cannot both vanish identically on the
two-plane (R).  Indeed, if (p_1+p_2) vanishes on (R), then
(R=\ker(p_1+p_2)), while the first form restricts to (2p_1), which is
not identically zero there.  Choose a (p\in R) on which one form is
nonzero and use the corresponding family for every subset (S).

The incidence matrix of fixed-size proper nonempty subsets against points
has full column rank in characteristic zero.  Hence

\[
                              Z_{i,0}=0\qquad(i\in{cal O}).       \tag{10}
\]

Interchanging binary colours gives the two forms

\[
                 (r+2)p_0+rp_2,qquad p_0+p_2.                   \tag{11}
\]

Their coefficient vectors again have determinant (2), so the identical
argument gives

\[
                              Z_{i,1}=0\qquad(i\in{cal O}).       \tag{12}
\]

## 4. The extra star and the two centre rows

Give (r+2) sites of ({\cal O}) colour (0), the remaining (r) sites
colour (1), contract (e) by an arbitrary (eta), and use source
(00).  If the star is at (e), the marked pair removes two zeros and the
remaining binary cofactor is balanced.  Every other star term contains a
variable from (10)--(12).  The response is therefore

\[
                         L_r\,\eta^{\mathsf T}q_{e z_0}=0.        \tag{13}
\]

Since (eta) is arbitrary, this kills the entire extra block.

It remains to kill row (2) at (c,d).  Fix one of them, say (c), and
give it output row (2).  Then (P_c[2,*]=0), so every term except the
star at (c) vanishes.  Choose a nonzero
(p\in R\cap\{p_0=0\}).  If (p_1+p_2\ne0), give (r+2) of the other
(2r+1) coordinate sites colour (0), give the rest colour (1), and
use source (00).  The coefficient of (Z_{c,2}) is

\[
                              L_r(p_1+p_2)\ne0.                   \tag{14}
\]

If (p_1+p_2=0), then (p_2\ne0).  Instead use (r+1) zeros and (r)
ones; the coefficient becomes

\[
                   M_rp_2,qquad M_r={r(r+1)r!\over2^r}\ne0.    \tag{15}
\]

Thus (Z_{c,2}=0), and the same argument kills (Z_{d,2}).

## 5. The live third rows

First suppose (R\not\subset\{p_2=0\}).  Choose (p\in R) with
(p_2\ne0).  For any two distinct live sites (i,j), give both output
colour (2); give (r) of the remaining coordinate sites colour (0)
and the other (r) colour (1); contract (e) to (p); and use source
(22).  For the star at (i), the marked pair is forced to be (e,j),
and symmetrically for the star at (j).  All other star variables have
already vanished.  Hence

\[
             {r!p_2\over2^{r-1}}(Z_{i,2}+Z_{j,2})=0.              \tag{16}
\]

There are at least four live sites because (r\ge2).  The pair-sum
equations for all (i\ne j) force every (Z_{i,2}) to vanish.

Finally suppose (R\subset\{p_2=0\}).  Both are planes, so

\[
                         R=\langle e_0,e_1\rangle .               \tag{17}
\]

After an output change (P_e=D).  Thus (e) is simply a third
binary-coordinate centre.  For any live (i), give it colour (2), give
(r+2) of the other (2r+2) sites colour (0), give the rest colour
(1), and use source (00).  All off-star variables have vanished, while
the coefficient of (Z_{i,2}) is (L_r\ne0).  The same row also kills
the third row at each singular site when that site is chosen as the unique
ternary letter.  This closes (17).

Repeating Sections 3--5 for the three coordinates at (z_0) proves (2).
The two removed type-(22) ports are singular and the zero--zero blocks
vanish by beta parity.  Thus (z_0) has no incident rank-three block,
proving Theorem 1.1.

## 6. Exact audit

[verify_live_three_zero_extra_plane_common_all_orders.py](../computations/verify_live_three_zero_extra_plane_common_all_orders.py)
enumerates the complete marked matching response behind (8)--(16) over
(\mathbb Q(p_0,p_1,p_2)) for (r=2,3,4).  It verifies every factorial,
all asserted zero supports, both fixed-subset incidence ranks, the centre
singletons, the noncoordinate pair sums, and the coordinate-plane final
row.  The displayed counting proof is independent of the finite audit.
