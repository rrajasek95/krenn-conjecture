# Independent audit of the one-multiterm common-power obstruction

## 1. Verdict

The theorem in
[the primary note](one-multiterm-monomial-common-power-obstruction.md) is
sound over \(\mathbb C\).  In its exact scope, let \(U\) be a six-set and
let each \(V_u\) contain independent displayed vectors
\(e_0^{(u)},e_1^{(u)},e_2^{(u)}\).  For a pair \(P\subset U\), put

\[
 E_i(P)=\bigotimes_{u\notin P}e_i^{(u)},
 \qquad X_i=\bigotimes_{u\in U}e_i^{(u)}.
\]

Suppose \(A\ne B\), all four displayed coefficients are nonzero, and

\[
 F=\alpha E_0(A)+\beta E_0(B)+\gamma E_1(C)+\delta E_2(D).       \tag{A1}
\]

Allow the six rows \(p_i,s_j\) to have arbitrary components at arbitrary
sites and impose the full response table

\[
 p_i s_jF=\delta_{ij}X_i.                                      \tag{A2}
\]

Then no quadratic \(q\) satisfies

\[
 q^{[2]}=F,\qquad q^{[3]}=0.                                  \tag{A3}
\]

The hand proof that (A2) forces \(A,B,C,D\) to be distinct is valid.  The
target-preserving normalization of all four coefficients is valid without
extracting roots.  The asserted kernels of \(qF=0\) are complete: they have
dimension \(1\) on the two special blocks when \(A,B\) are disjoint and
dimension \(3\) when they are adjacent, giving total dimensions \(100\)
and \(102\), respectively.  Finally, a clean-room enumeration again finds
exactly \(25\) support orbits, and separately ordered unsaturated ideals
over \(\mathbb Q\) have reduced basis \([1]\) in all \(25\) cases.

The standalone
[independent checker](../computations/audit_one_multiterm_common_power_obstruction_independent.py)
does not import the primary program.  It uses lexicographically maximal
orbit representatives, a different orbit order, reverse edge order, the
colour order \((2,0,1)\), kernel variables last, a different matching order,
and a reversed coefficient stream.

## 2. The literal products force four distinct pairs

Work in the site-square-zero algebra

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
 \qquad V_uV_u=0.                                             \tag{A4}
\]

If \(P=\{a,b\}\), only the components of the two star rows on its two
missing sites survive multiplication by \(E_k(P)\).  The complete local
response tensor is therefore

\[
 B_{ij}(P)=p_{i,a}\otimes s_{j,b}
             +s_{j,a}\otimes p_{i,b}.                         \tag{A5}
\]

Both endpoint orders occur in (A5).  For fixed lift colour \(k\), its
full-support response lies in

\[
 W_k(P)=
 \left(\bigotimes_{u\in P}V_u\right)
 \otimes
 \left(\bigotimes_{u\notin P}\mathbb C e_k^{(u)}\right).       \tag{A6}
\]

The coordinate-word supports of \(W_k(P)\) and \(W_\ell(Q)\) are disjoint
when \(k\ne\ell\): the union of two pairs occupies at most four of the six
sites, and at every remaining site the fixed coordinate is \(e_k\) in one
space and \(e_\ell\) in the other.  Thus different lift colours separate
coefficientwise even though terms of the same colour may cancel.

Apply (A2) to row \((1,1)\).  Its colour-one and colour-two components give

\[
 B_{11}(C)=\gamma^{-1}e_1^{\otimes C},
 \qquad B_{11}(D)=0.                                         \tag{A7}
\]

If \(C=D\), the same literal tensor (A5) is both nonzero and zero.  The
colour-zero component is

\[
 \alpha\,\iota_A B_{11}(A)+\beta\,\iota_B B_{11}(B)=0,        \tag{A8}
\]

where \(\iota_P\) inserts \(e_0\) outside \(P\).  If, for example,
\(C=A\), then (A7) makes the first term of (A8) have a nonzero coefficient
on the word which is \(e_1\) at both endpoints of \(A\) and \(e_0\)
elsewhere.  Since \(A\ne B\), some endpoint of \(A\) is outside \(B\);
every word in the second response space is fixed to \(e_0\) there.  Hence
the displayed coefficient cannot cancel.  The case \(C=B\) is the same.

Row \((2,2)\), with \(e_2\) in place of \(e_1\), proves that \(D\) is
different from \(A\) and \(B\).  Together with the first sentence after
(A7), this proves that \(A,B,C,D\) are all distinct.  The checker enumerates
all

\[
 \binom{15}{2}\,15^2=23{,}625
\]

initial supports and records the following disjoint decision census:

| reason or survivor | count |
|---|---:|
| \(C=D\) | 1,575 |
| \(C\in\{A,B\}\), after excluding \(C=D\) | 2,940 |
| \(D\in\{A,B\}\), after the preceding cases | 2,730 |
| all four pairs distinct | 16,380 |

The counts sum to \(23{,}625\).  This is only a finite audit of the case
split; the preceding coefficient argument is the proof for arbitrary local
spaces and arbitrary star rows.

## 3. Projection and target-preserving weight normalization

At each site choose a projection

\[
 V_u\longrightarrow
 \langle e_0^{(u)},e_1^{(u)},e_2^{(u)}\rangle
\]

which fixes the three displayed axes.  Extending it by the identity on the
scalar summand gives an algebra homomorphism in (A4), because every product
of two positive-degree elements at one site is zero.  Tensoring over the six
sites preserves (A1)--(A3).  Therefore any solution in larger local spaces
would project to a solution with exactly three local coordinates.  The
later affine ideals lose no branch by making this projection.

For completeness, the four coefficient normalizations can be made while
fixing every \(X_i\).  Scale the displayed axes by nonzero scalars

\[
 e_i^{(u)}\longmapsto t_{i,u}e_i^{(u)},
 \qquad \prod_{u\in U}t_{i,u}=1.                              \tag{A9}
\]

Then the new coefficient of \(E_i(P)\) is

\[
 \lambda\prod_{u\notin P}t_{i,u}
   =\frac{\lambda}{\prod_{u\in P}t_{i,u}}.                   \tag{A10}
\]

For colour zero, choose \(u_A\in A\setminus B\) and
\(u_B\in B\setminus A\) when the pairs meet, and choose any one endpoint
of each pair when they are disjoint.  Set

\[
 t_{0,u_A}=\alpha,qquad t_{0,u_B}=\beta,
\]

set the other factors initially to one, and at a site
\(r\notin A\cup B\) set \(t_{0,r}=(\alpha\beta)^{-1}\).  This gives total
product one and pair products \(\alpha\) on \(A\) and \(\beta\) on \(B\).
Such an \(r\) exists because two pairs occupy at most four sites.  For
colour one, put \(\gamma\) at one endpoint of \(C\) and \(\gamma^{-1}\)
at a site outside \(C\); do the analogous thing with \(\delta,D\) in
colour two.  Thus all four target coefficients become one by explicit
products, with no genericity and no root extraction.

The map (A9) is an algebra automorphism.  It fixes each \(X_i\), carries the
rows and \(q\) with it, and commutes with bracket powers.  It therefore
preserves the exact right side of (A2), not merely its support.  The checker
independently verifies these exponent recipes for every position of the
relevant pair or pair-pair configuration.

## 4. Complete kernel of \(qF=0\)

After normalization, the divided-power identity

\[
 q q^{[2]}=3q^{[3]}                                      \tag{A11}
\]

shows that (A3) implies \(qF=0\).  Only the block \(q_P\) can fill the two
holes of \(E_i(P)\); every other edge block repeats an occupied site and
vanishes.  Separation of the three fixed-colour coordinate supports first
gives

\[
 q_C=q_D=0.                                                \tag{A12}
\]

It remains to solve exactly

\[
 \iota_A(q_A)+\iota_B(q_B)=0.                              \tag{A13}
\]

Here is a decomposition which makes completeness transparent.  Write

\[
 V_u=\mathbb C e_0^{(u)}\oplus T_u
\]

and, for every colour-zero missing edge \(uv\), expand

\[
 q_{uv}=c_{uv}e_0^{(u)}e_0^{(v)}
       +a_{u\mid v}e_0^{(v)}
       +e_0^{(u)}a_{v\mid u}
       +d_{uv},                                           \tag{A14}
\]

with \(a_{u\mid v}\in T_u\) and
\(d_{uv}\in T_u\otimes T_v\).  More generally, in an equation
\(\sum_{uv}\lambda_{uv}\iota_{uv}(q_{uv})=0\), separation by the number
and locations of transverse factors gives exactly

\[
 d_{uv}=0,
 \qquad
 \sum_{v:uv\text{ occurs}}\lambda_{uv}a_{u\mid v}=0,
 \qquad
 \sum_{uv}\lambda_{uv}c_{uv}=0.                           \tag{A15}
\]

Indeed, a double-transverse component at \(u,v\) belongs to only that edge;
a single-transverse component at \(u\) receives precisely the incident-edge
terms; and the last equation is the all-\(e_0\) word.  These coordinate
subspaces are a direct sum, so (A15) omits no cancellation.

For two disjoint edges, every single-transverse equation has one summand.
All \(a\)'s and \(d\)'s vanish, leaving one scalar relation between
\(c_A,c_B\).  The kernel on the two special blocks has dimension \(1\):

\[
 q_A=z e_0^{\otimes A},\qquad q_B=-z e_0^{\otimes B}.       \tag{A16}
\]

For \(A=\{x,a\}\) and \(B=\{x,b\}\), the unique endpoints kill the
transverse components there, while the shared-site equation relates the
two vectors in \(T_x\).  Together with the scalar relation this is one
arbitrary vector \(v\in V_x\), a three-dimensional kernel:

\[
 q_A=v\otimes e_0^{(a)},
 \qquad q_B=-v\otimes e_0^{(b)}.                            \tag{A17}
\]

There are eleven further, unrestricted edge blocks.  Hence the full kernel
inside the \(15\cdot 3^2=135\) coordinates of \(q\) has dimension

\[
 11\cdot9+1=100\quad\text{or}\quad 11\cdot9+3=102,          \tag{A18}
\]

and the corresponding ranks are \(35\) and \(33\).  The independent code
constructs the full coefficient matrix of \(qF\), performs rational sparse
elimination with the opposite pivot convention from the primary checker,
checks these ranks for every representative, and verifies both spanning and
linear independence of the parameter bases (A16)--(A17).

## 5. Independent support census and exact ideals

With all four pairs distinct, the labelled support count is

\[
 \binom{15}{2}\,13\,12=16{,}380.                            \tag{A19}
\]

The independent program constructs this set directly and takes orbits
under site permutations, \(A\leftrightarrow B\), and the simultaneous swap
of \(C,D\) and colours \(1,2\).  It does not start from the primary list of
representatives.  It finds \(25\) disjoint orbits whose sizes sum to
\(16{,}380\).  Its ordered representative-and-size ledger has SHA-256

```text
b1c5d4bade10cede0c2616f9a64891610b637417d4bda5a606a5152e5eeb4965
```

After substituting the complete kernel (A16)--(A17), the coefficient on a
four-set \(\{u_0,u_1,u_2,u_3\}\), with local colour word
\((r_0,r_1,r_2,r_3)\), is the sum over its three perfect matchings:

\[
 \begin{aligned}
 &(q_{u_0u_1})_{r_0r_1}(q_{u_2u_3})_{r_2r_3}
 +(q_{u_0u_2})_{r_0r_2}(q_{u_1u_3})_{r_1r_3}\\
 &\qquad +(q_{u_0u_3})_{r_0r_3}(q_{u_1u_2})_{r_1r_2}
 -[F]_{\{u_0,u_1,u_2,u_3\},(r_0,r_1,r_2,r_3)}.             \tag{A20}
 \end{aligned}
\]

The checker emits every nonzero instance of (A20).  It retains endpoint
order by transposing local indices when an edge is traversed backwards.
No equation is selected by rank or support heuristics.

The following table is the complete independent run.  A pair \(\{u,v\}\)
is abbreviated to \(uv\); the support column is \((A,B;C,D)\).  The
variables column is the full \(qF\)-kernel dimension.  Each final column is
the SHA-256 of that orbit's independently ordered generator stream.

| no. | support | orbit size | variables | equations | independent SHA-256 |
|---:|---|---:|---:|---:|---|
| 1 | `(35,45;34,25)` | 360 | 102 | 1,107 | `ed2c3b9885bf733a444003d00a79d47e6c8e78846ea02ce6b1c7abc0725d26e4` |
| 2 | `(35,45;34,24)` | 720 | 102 | 1,089 | `d2d80b7210ef530ea21e988f6dabde898bb6395694708768e4ddae0d89911302` |
| 3 | `(35,45;34,12)` | 360 | 102 | 1,108 | `069c7d04b4c02d48c8081bd061abc0b0bf24dd43ff364c498138e06b6d0e372e` |
| 4 | `(35,45;25,24)` | 720 | 102 | 1,053 | `cdf9009f7a8738b1a1c294ee87c66c579206db74fd0695d1d686cf3020b15f4f` |
| 5 | `(35,45;25,15)` | 360 | 102 | 1,035 | `4039323fa3006f8e6d478bde1e28d4a651febd401c6e79490afae1956d19cd4f` |
| 6 | `(35,45;25,14)` | 1,440 | 102 | 1,179 | `553cd60a368974d5f74fb2f87d0eb5879237b0cfbdd7fc75090645186610bd61` |
| 7 | `(35,45;25,12)` | 720 | 102 | 1,179 | `6825a655da90b8a88d436d4d315c4b5d4df23b528cf69314bf60f9456f99c449` |
| 8 | `(35,45;25,01)` | 360 | 102 | 1,180 | `beb5f39cf2561fa9cdf5cffcf68a22b9ca8f2c2d34897602d06d38ec561df592` |
| 9 | `(35,45;24,23)` | 360 | 102 | 1,215 | `e87ba2081ab9d413faf33afecbb3bc7655c5160c91ec04b7a691540ece0ec2cd` |
| 10 | `(35,45;24,14)` | 720 | 102 | 1,161 | `6b9e8c4543bcc5e6fa7893933efa32aafea05c1d25f6999bd925202c677846d9` |
| 11 | `(35,45;24,13)` | 720 | 102 | 1,215 | `455e5b8238f72c92466a15d715fe255dd8c16deb8073a72b7e1ad8d9779bd3b1` |
| 12 | `(35,45;24,12)` | 1,440 | 102 | 1,215 | `531dfe8c34d64ba1f596ff96f23305666741026564f70b3bbb3df74ce0e07fce` |
| 13 | `(35,45;24,01)` | 720 | 102 | 1,215 | `aa739d30a9e0a00c856c6d4bddb8d03b92e264ebf5282a5d125d3ae1ce277529` |
| 14 | `(35,45;12,02)` | 360 | 102 | 1,215 | `dce315d5d155c2d7c6526e5259243d43a7ab76f8758398cc9a719502e244f85f` |
| 15 | `(25,34;45,35)` | 360 | 100 | 991 | `d52d604c91e72ebfbb23ba363da13e7f4fc442c6f53343f4d68f2bc1a83da0d2` |
| 16 | `(25,34;45,23)` | 180 | 100 | 1,215 | `4633659a7e7e09011aec7131f5cbf6c7c2cf85ec935207fe6e1e2132e3aa64ae` |
| 17 | `(25,34;45,15)` | 1,440 | 100 | 1,143 | `34b0788e29774837c19b2a3baf62d34e4af5e2cc43ac49df2c7d3d68e56cdbbb` |
| 18 | `(25,34;45,13)` | 1,440 | 100 | 1,215 | `f1712ad531a2ba973f0e44445b791c1b34259d7ae241287a0f13ed1b57a02955` |
| 19 | `(25,34;45,01)` | 360 | 100 | 1,215 | `0ebca208567537374f5edbcde869f8c2a6e86d88d22bb591ee08e97f9c4f21cc` |
| 20 | `(25,34;15,14)` | 720 | 100 | 1,215 | `96d6950b1da9f3ef1b8831c6acbcea386ded3fa21a20af9f1def6a53ecbe8870` |
| 21 | `(25,34;15,12)` | 360 | 100 | 999 | `ac0645122e21c42b21a50f9476f62034e551f5083a01f821e3444288ab6c1abb` |
| 22 | `(25,34;15,05)` | 360 | 100 | 1,143 | `59482eb20e65a8e3bc4f5af13bd6448dfa699d43512cf2518fca39cf3dfc3950` |
| 23 | `(25,34;15,04)` | 720 | 100 | 1,215 | `9360790ec3e659c761d1578d1ea77d92f1d0efda2112d4023179bd6775c207be` |
| 24 | `(25,34;15,02)` | 360 | 100 | 1,215 | `818cc5983194534d168caf96cedde216c82bfb81ad23130d40c82045eeac68e8` |
| 25 | `(25,34;15,01)` | 720 | 100 | 1,215 | `3c27dc166b7b6883c6c9c02e25dff66fb9e78c8735146b5fed5545335be99699` |

Singular over \(\mathbb Q\) returns the reduced basis \([1]\) for every
row.  These are full affine ideals: the calculation introduces no inverse,
nonzero declaration, localization, or saturation.  Therefore it includes
all zero coordinates, rank drops, degenerations, and complex cancellation
strata.  Since \(1\) belongs to each ideal already over \(\mathbb Q\), the
same ideals have no common zero over \(\mathbb C\).

The hash of the ordered ledger containing orbit number, representative,
variable count, equation count, and individual generator hash is

```text
10b8a308e580332722b54a6fdab9a3220810fec64135427af0b94da76a1ab4f9
```

Both ledger hashes and all \(25\) individual hashes are asserted on every
full replay.

## 6. Scope and audit conclusion

The product part retains all nine equations, both endpoint orders, arbitrary
multi-site rows, arbitrary complex cancellation, and arbitrary original
local dimensions.  The common-power part uses every coefficient of
\(q^{[2]}-F\) after a proved complete linear parametrization of \(qF=0\).
The weights \(\alpha,\beta,\gamma,\delta\) need only be nonzero.

The restrictive hypothesis is exactly the pure four-term multiplicity
profile \((2,1,1)\): two distinct pure monomials in one target colour and
one pure monomial in each of the other two colours.  This audit says nothing
about profiles \((3,1,1)\) or \((2,2,1)\), non-pure four-site target
tensors, or the global descent from arbitrary even order.  Thus it validates
the advertised bounded obstruction but is not itself a proof of Krenn's
conjecture.

The full independent replay completed with all \(25\) unit ideals and
printed

```text
independent one-multiterm common-power audit: PASS
```
