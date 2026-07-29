# Arbitrary annihilators exclude a four-site witness union

## 1. Outcome

Let `B` have eight vertices, suppose

\[
 H_B(A)=\Delta_{B,3},                                    \tag{1}
\]

and fix `p,q` with `A_pq` invertible.  On the six outside vertices put

\[
 C_{u,r}=A_{pu}K_rA_{qu}^T,
 \qquad S_r=\{u:C_{u,r}=0\}.                             \tag{2}
\]

The one-hole identities give `|S_r|>=2`, and the reversed-star argument in
[`n8-minimal-witness-union-obstruction.md`](n8-minimal-witness-union-obstruction.md)
gives `|S_0 union S_1 union S_2|>=4`.  Here we exclude equality.

**Theorem 1 (five-site witness-union bound).**  Every invertible edge in an
eight-site realization satisfies

\[
             |S_0\cup S_1\cup S_2|\ge5.                 \tag{3}
\]

The new point is to distinguish a zero cross coordinate from a zero which
actually kills that coordinate for every arbitrary common annihilator.
This removes the one-sided triple-zero loophole and reduces the equality
case to twelve finite incidence patterns.  Nine die by one `2 by 2`
determinant; the remaining three die by an anchor rectangle or by
independence of two annihilator monomials.

## 2. Hard witnesses over the incidence function field

Write

\[
 g=\alpha^TA_{pq}\beta,
 \qquad K=\operatorname {Frac}
   \bigl(\mathbb C[\alpha,\beta]/(g)\bigr).              \tag{4}
\]

This is a field because the rank-three bilinear form `g` is irreducible.
At an outside site put

\[
 x_u=A_{pu}^T\alpha,
 \qquad y_u=A_{qu}^T\beta,
 \qquad N_u=\{z:x_u^Tz=y_u^Tz=0\}\subset K^3.           \tag{5}
\]

Call `u` a **hard witness** for color `r` when

\[
                         N_u\subset e_r^\perp.           \tag{6}
\]

Equivalently, every common annihilator at the generic point of `g=0`
kills target coordinate `r`.

**Lemma 2.1 (two hard witnesses per color).**  For each color `r`, at
least two outside sites are hard `r`-witnesses.

**Proof.**  Leave a site `w` open in the arbitrary common-annihilator
identity.  On `g=0`, its `r` coordinate is

\[
       \alpha_r\beta_r\prod_{u\ne w}z_{u,r}=0
       \qquad(z_u\in N_u).                               \tag{7}
\]

The classes `alpha_r,beta_r` are nonzero in `K`.  If at most one site were
hard, omit that site (or any site if there is none).  At every remaining
site the coordinate functional `z -> z_r` is a nonzero functional on
`N_u`; independent choices make their product in (7) nonzero.  This is a
contradiction. `QED`

Let

\[
                         W_u=\{r:C_{u,r}=0\}.             \tag{8}
\]

The hard capacity of a site is determined exactly unless it is a triple
zero.

**Lemma 2.2 (hard-capacity rule).**

* If `|W_u|=0,1,2`, the hard colors at `u` are exactly the colors in
  `W_u`.
* If `|W_u|=3`, at most one color is hard.  A hard color `r` occurs exactly
  when the generic span of `x_u,y_u` is the coordinate line `K e_r`.

**Proof.**  In `K^3`,

\[
              x_u\mathbin\times y_u
       =\bigl(\alpha^TC_{u,r}\beta\bigr)_{r=0}^2.        \tag{9}
\]

A class on the right vanishes in `K` exactly when its coefficient matrix
is proportional to `A_pq`; rank at most two versus rank three makes this
equivalent to `C_(u,r)=0`.  If fewer than three coordinates vanish, the
cross product is nonzero and `N_u` is its span.  Condition (6) is then
equivalent to the vanishing of its `r` coordinate, proving the first
bullet.

If all coordinates vanish, `x_u,y_u` are dependent and
`N_u=(span\{x_u,y_u\})^perp` has dimension at least two.  It lies in the
coordinate plane `e_r^perp` exactly when the opposite span contains
`e_r`.  That span has dimension at most one, so it must equal `K e_r`.
It cannot equal two different coordinate lines. `QED`

In particular, a site with zero-witness multiplicity `0,1,2,3` has hard
capacity respectively `0,1,2,1`.

## 3. The twelve capacity survivors

Assume the union in (3) has four vertices, relabeled `0,1,2,3`; the other
two outside sites have no witness.  Up to permutations of the four sites
and the three colors, there are 23 triples `(S_0,S_1,S_2)` with
`|S_r|>=2` and union four.  Lemmas 2.1--2.2 leave exactly the following
twelve.  A string such as `012` denotes the vertex set `{0,1,2}`.

\[
\begin{array}{c|ccc|c}
 &S_0&S_1&S_2&\text{disposition}\\ \hline
1&01&01&23&\text{anchor rectangle}\\
2&01&012&023&\text{determinant}\\
3&01&012&23&\text{determinant}\\
4&01&0123&0123&\text{two monomials}\\
5&01&0123&023&\text{determinant}\\
6&01&0123&23&\text{determinant}\\
7&01&02&123&\text{determinant}\\
8&01&02&13&\text{determinant}\\
9&01&023&023&\text{two monomials}\\
10&01&023&123&\text{determinant}\\
11&012&0123&013&\text{determinant}\\
12&012&013&023&\text{determinant}
\end{array}                                               \tag{10}
\]

For rows 11--12 there is more than one possible assignment of a hard
color to a triple-zero site; every assignment has the indicated
determinant witness.  The exact orbit and hard-assignment enumeration is
audited by the checker in Section 7.

## 4. The two-hole determinant

We use the following local identity.  Fix generic `alpha,beta` on `g=0`.
Suppose a hole `u` is an exact double witness whose missing color is `s`.
Then its two star vectors span `e_s^perp`, and

\[
             (x_u\mathbin\times y_u)_s\ne0.              \tag{11}
\]

Let `r` be one of its hard colors and let `a` be the other coordinate in
`e_s^perp`.  For a second exact-double hole `v`, with missing color `t`,
let `b` be the other coordinate in `e_t^perp`.  Restrict the two-hole star
correction

\[
                  R_{uv}=x_uy_v^T+y_ux_v^T               \tag{12}
\]

to rows `(r,a)` at `u` and columns `(r,b)` at `v`.  The elementary
two-by-two determinant identity gives

\[
 \det R_{uv}[(r,a),(r,b)]
  =\det\!\begin{pmatrix}x_{u,r}&y_{u,r}\\x_{u,a}&y_{u,a}\end{pmatrix}
    \det\!\begin{pmatrix}y_{v,r}&x_{v,r}\\y_{v,b}&x_{v,b}\end{pmatrix}
  \ne0.                                                   \tag{13}
\]

Up to harmless signs, the last two determinants are precisely the two
nonzero cross coordinates in (11).

Now suppose the hard set for a color `r` is exactly `{u,v}`, both sites are
exact double witnesses, and every other color has a hard site outside
`{u,v}`.  Use `u,v` as holes.  At every contracted site choose a generic
vector in `N_z`.  The `r` coordinate of each such vector is nonzero, while
each other target color is killed at one of its outside hard sites.
Therefore the arbitrary-annihilator two-hole identity over a purely
transcendental extension of `K` has the form

\[
                       t_rE_{rr}=hR_{uv},
 \qquad t_r\ne0.                                         \tag{14}
\]

It makes `h` nonzero and forces every entry of (12) outside `(r,r)` to
vanish.  The submatrix in (13) would then have determinant zero, a
contradiction.  This excludes the nine determinant rows of (10).

## 5. The two independent-monomial rows

Consider row 4 of (10):

\[
                  S_0=\{u,v\},\qquad S_1=S_2=\{u,v,a,b\}.
                                                               \tag{15}
\]

The only possible hard `0`-sites are the triple-zero sites `u,v`.
Lemma 2.1 makes both of them coordinate common-line sites of color zero,
so

\[
                         N_u=N_v=e_0^\perp.              \tag{16}
\]

The sites `a,b` are exact double witnesses for colors `1,2`.  Use them as
holes, choose independent arbitrary `z_u,z_v in e_0^perp`, and use the
cross-product lines at the two nonwitness sites.  The two-hole identity is

\[
 \operatorname {diag}
  \bigl(0,k_1z_{u,1}z_{v,1},k_2z_{u,2}z_{v,2}\bigr)
       =h(z_u,z_v)R_{ab},                                 \tag{17}
\]

with `k_1,k_2` nonzero in `K`.  By (13), the lower `2 by 2` block of
`R_ab` is invertible.  The off-diagonal equations in (17) first make this
block diagonal.  Its two diagonal equations then say that the independent
monomials `z_(u,1)z_(v,1)` and `z_(u,2)z_(v,2)` are proportional over
`K`, which is impossible.

Row 9 is identical with one plane replaced by a generic line.  In the
notation

\[
                  S_0=\{u,v\},\qquad S_1=S_2=\{u,a,b\}, \tag{18}
\]

the triple site `u` must be hard zero and has `N_u=e_0^perp`; the singleton
zero-witness site `v` has a one-dimensional annihilator whose `1,2`
coordinates are both nonzero.  Taking `a,b` as holes gives

\[
 \operatorname {diag}
  \bigl(0,k_1z_{u,1}z_{v,1},k_2z_{u,2}z_{v,2}\bigr)
       =h(z_u)R_{ab}.                                    \tag{19}
\]

After absorbing the two fixed nonzero coordinates of `z_v` into `k_1,k_2`,
the same argument would make the independent linear forms `z_(u,1)` and
`z_(u,2)` proportional.  This excludes row 9.

## 6. The last anchor rectangle

It remains to exclude row 1:

\[
                         S_0=S_1=\{u,v\},
 \qquad S_2=\{a,b\}.                                    \tag{20}
\]

Leave all four witness sites `u,v,a,b` open and contract the two
nonwitness sites by their cross-product covectors.  On `g=0` all three
target coefficients are nonzero.  Every surviving matching sends `p,q`
to two distinct open sites.  Grouping first by the partner of `p` writes
the target as four one-site slices; the one-slice covering lemma supplies,
for each color, a directed anchor from `p`.  An anchor outside `S_r` would
itself be an `r`-witness, so the color-zero and color-one anchors lie among
`u,v`, while the color-two anchor lies among `a,b`.  Grouping by the
partner of `q` gives the same statement at the other endpoint.

The color-zero and color-one anchors from `p` use different sites: one
nonzero matrix cannot have image in two different coordinate lines at its
outside endpoint.  The same holds at `q`.  If the color-zero anchors from
`p,q` used the same site, both star blocks there would have common row line
`C e_0`, making that site a triple-zero witness, contrary to (20).
Therefore the endpoint assignments are crossed.  After interchanging
`u,v`,

\[
                    A_{pu}=ae_0^T\ne0,
 \qquad A_{qv}=be_0^T\ne0.                              \tag{21}
\]

For the pair `u,v`, the exact-pair color set in the notation of Theorem
6.2 of
[`two-vertex-annihilation-identities.md`](two-vertex-annihilation-identities.md)
is `J(u,v)={0,1}`.  The anchor-rectangle alternative forces the two
opposite blocks to be nonzero directed color-one anchors.

For `S_2={a,b}`, the four-hole argument already supplies a color-two
anchor from each endpoint among `a,b`.  They cannot collide at one site,
because that site would then be triple zero rather than an exact singleton
witness.  Thus they too are crossed.  Here `J(a,b)={2}`.  The singleton
branch of the anchor-rectangle alternative
says that one opposite block vanishes or that both opposite blocks close
in color two.  In every case at least one of `a,b` becomes a triple-zero
site.  It would then also belong to `S_0,S_1`, contradicting (20).  This
excludes the final row and proves Theorem 1. `QED`

## 7. Exact audit

[`verify_n8_hard_witness_union_four.py`](../computations/verify_n8_hard_witness_union_four.py)
enumerates the 23 `S_4 times S_3` incidence orbits, every permissible hard
color assignment at triple-zero sites, the twelve rows (10), and the nine
rows satisfying the determinant criterion.  It also verifies the symbolic
determinant factorization (13) and the monomial nonproportionalities used in
(17)--(19).  The finite script is an audit of the incidence and scalar
algebra; the function-field and anchor arguments are proved above.
