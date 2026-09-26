# Independent audit of the stronger-results certification package

**Verdict: PASS for repository admission of the explicitly scoped results.**
Date: 2026-09-26. Independent auditor: `/root/stronger_results_package_audit`.
Package author and admission editor: `/root`. I did not author the submitted
analytic proofs, package verifier, certificate generator, or theorem assembly.
I independently reconstructed the load-bearing mathematical arguments and
reviewed the executable checks. Historical PASS labels and the author's
acceptance were not premises of this verdict.

The final audited payload is
[`stronger-results-2026-09-26`](../stronger-results-2026-09-26/README.md), with
manifest SHA-256
`17f127b063e844a100e68c4a6463dd323f1e94dbc48d3a4a92e56dae79b8a940`.
This verdict applies to those bytes and the scopes in `nodes.json` and
`THEOREMS.md`. The append-only supersession ledger performs admission; this
report does not modify the frozen baseline or claim admission by itself.

## Scope accepted

For an ordinary complex quadratic on distinct pairs of an even number of
physical sites, multiplication is commutative and every repeated-site product
is zero. Each site has the three fixed target coordinates. The hypothesis is
the **whole** matching-tensor equality to three nonzero pure target tensors,
with arbitrary nonzero amplitudes. Cancellation among matching contributions
is allowed throughout.

I accept the package's following conclusions:

1. At every even order at least four, every off-color cell is zero in the
   original target bases. Each remaining color matrix satisfies
   `M_h C_h = tau_h I`, where `C_h` is its actual zero-diagonal matrix of
   deleted-pair hafnians. The source problem is exactly the stated weighted
   diagonal hafnian-cancellation system.
2. At order `n=2m>=6`, each single-color degree lies between one and `m-2`.
   Degree two is impossible, and every degree-one vertex belongs to an
   isolated edge. Neighborhood cofactor zeros have the stated scope.
3. No source under these hypotheses exists on eight or ten sites. Local
   projection extends these two exclusions to more than three nonzero
   designated diagonal target terms.

The twelve admitted proof nodes include the intermediate identities specified
in the package inventory. No other corollary is admitted merely because its
historical file is copied into the package. This is ordinary mathematical
repository certification with an independent research-agent audit. It is not
Lean verification or human peer review. General even orders at least twelve
remain open under this package; neither universal descent nor the old
clean-point bridge is proved here.

## Independent reconstruction of the analytic chain

### CF and BM: reflection and polynomial cancellation

For fixed actual quadratic `R` and row `L`, the Wick functional is defined by
finite sums over labeled pairings; positivity or an inverse covariance is
unnecessary. Giving an auxiliary variable zero self-covariance and covariance
`L` with the physical variables makes its `d` labeled occurrences pair with
`d` distinct physical variables. The resulting `d!` assignments exactly match
the raw row power `L^d`; the remaining pairings give the divided power of `R`.

Two independent identical replicas have covariance preserved by the displayed
rational orthogonal reflection. It fixes `s g_1+t g_2` and reverses each local
determinant, including site-dependent color pairs. At odd physical order the
product reverses sign, so its finite Wick expectation vanishes. This is an
identity over `C(s,t)` whose original expression is polynomial, permitting
coefficient extraction without a specialization at a pole.

The constant-palette specialization with one original response gives
`f_b t_a=f_a t_b`. Two independent target linear forms are coprime in the
polynomial ring of the actual row space, giving the unique common homogeneous
factor for all three pure responses. The proof works on the supplied linear
row subspace as well as the entire diagonal-response space.

For a mixed word omitting an active color `h`, pair its local color with `h`
at each site. The only complementary diagonal word is the pure `h` word.
Thus `f_h(L) H_p(L)[w]=0` is a polynomial identity; cancellation proves its
vanishing even where a particular value of `f_h` is zero. This requires an
active omitted color, exactly as specified. Full polarization is legitimate
over `C` and supplies the multiple-row forms.

### HP: the finite mean has no higher pure terms

The shifted Wick mean has exactly the factorial-normalized finite expansion
`Psi(L)=sum H_(2r+1)(L)/(2r+1)!`. CF and BM make its binary restriction
`G(L)(f_a(L) P_a+f_b(L) P_b)`, when `f_a,f_b` are independent and the third
target is active. The latter premise is used to remove binary mixed words.

A determinant-one rotation of two ordinary replicas preserves their complete
covariance and the product of local alternating contractions. Consequently
the contraction of `Psi(L),Psi(M)` is rotation invariant. Its binary value
contains the nonzero polynomial
`Delta=f_a(L)f_b(M)-f_b(L)f_a(M)`, which is cancelled **before** setting `M=0`.
The 45-degree rotation then gives `G(L/sqrt(2))^2=G(L)`. Finiteness, evenness,
and constant term one force `G=1`: a nonconstant highest degree would double
on the left. Distinct homogeneous degrees and polarization finish HP.
No assertion that all-three-color higher responses vanish is needed.

### EV: omission keeps the original row component

Writing the actual omission as `R=Q+sum h_q V_h` and
`L=U+sum d_h(L)h_q`, direct expansion gives
`[h_q]Psi_R(L)=d_h(L)E(U)+partial_(V_h)E(U)`. The first term must be retained;
the second has precisely the derivative factorial. HP makes its binary
projection `f_h(L) h^S`.

At even retained order, the alternating product pairing is symmetric.
Ordinary-replica rotation yields
`B(E(U),E(U))=B(E(sqrt(2)U),F)`. Rotating `(U,U+tV)` and differentiating
uses `E'(0)=0` and gives
`B(E(U),partial_V E(U))=B(F,partial_V E(sqrt(2)U))/sqrt(2)`.
Here `V` is arbitrary; the original star `V_h` need not lie in the restricted
row space. Substitution at both `L` and `sqrt(2)L` scales both `d_h` and `f_h`.
The `d_h` terms cancel, leaving `f_h(L)[k^S](E(U)-F)=0`. Cancellation,
homogeneous separation, and polarization give the stated all-even omission
identity. The two-site retained boundary uses no negative divided power.

### GD: actual cofactors, ordered pairs, and ordinary inversion

At every root of the full source, the three original rows have three
independent pure responses. Thus EV applies after every second omission to
two rows from the **same** root family. For a fixed receiving color, a
diagonal entry of `B_ih C_h` is exactly a whole one-defect word. Off-diagonal
entries expand the cofactor at its retained root, producing the ordered pair
sum equal to that same-family quadratic response. The two orders occur on
both sides even when the rows coincide; no factor of one half belongs here.

It follows that `B_ih C_h=delta_(i,h) tau_h I`. Taking `i=h` first makes
`C_h` invertible as an ordinary complex matrix. The other equations then
force every off-color cell to vanish. There is no cancellation of an element
in the site-square-zero algebra. The four-site boundary uses the empty
hafnian one. Finally, after diagonality the coefficient of a color partition
is the product of its three actual restricted hafnians, preserving all
possible internal cancellation and proving the exact reformulation.

### RV and BC: whole binary cofactors, not individual coefficients

For a decomposable third tensor, contracting it with the local ternary
determinants leaves a product of alternating bilinear forms. Ordinary
two-replica mean rotation applies. Comparing degree four gives
`B(F,H4(L,L,L,L))=3 B(beta(L,L),beta(L,L))`; polarization supplies the three
pairings in RV's four-row identity, each with coefficient one. Linearity in
the third tensor extends it to all whole tensors. At retained order two,
the absent quartic term is zero and the argument remains valid.

For BC, deletion on the larger shore gives the exact slice
`y_h F+beta(Y_0,U_h)=tau_h h^S`. Bipartite occupancy makes
`beta(Y_0,Y_0)=0`. If `F=0`, applying RV to `Y_0,Y_0,U_a,U_b` against the
unused pure third coordinate gives `0=2 tau_a tau_b`, a contradiction.
Projection onto the active two-dimensional local planes commutes with the
actual source construction and repeats the argument, establishing **whole**
active-plane cofactor nonvanishing. Deleting a root from a balanced binary
source supplies the requisite larger-shore row by summing its two pure root
rows. The empty cofactor at shore size one is handled separately. No use
below upgrades this theorem to nonzero individual pure coefficients.

### NB and SD: strict degree and the scalar component restriction

The HP cubic binary response at root `p` gives
`2 M_h[p,u] M_h[p,v] C_k[u,v]=0`. The ordinary two-site mixed word supplies
`M_h[p,u] C_k[p,u]=0`. Hence a closed color neighborhood is a totally
isotropic coordinate subspace for each other invertible cofactor matrix,
so its size is at most `m`.

If its size is `m`, the square cross block of either other cofactor is
invertible; inversion makes that other adjacency zero on the complementary
shore. Its binary projected top therefore uses only crossing edges and is
an actual balanced binary source. BC and the original two-site mixed slice
force the first color to have no crossing edges. Its nonzero hafnian then
factors over the two shores. Odd shore size is impossible. For even `m>=4`,
the higher odd root response of order `m-1` has the unique nonzero pure
coefficient `(m-1)!` times the product of all neighborhood weights times the
opposite-shore hafnian. HP contradicts it. At four sites this is an original
response, not a higher response, so the exception is correctly retained.

SD section 5 assumes only the actual scalar cofactor relation. For a leaf of
weight `a`, the retained-partner expansion gives
`(MC)[r,q]=2a C[p,q]`; the inverse relation then isolates its incident edge.
For a degree-two root, each relevant off-diagonal entry is `2ab` times the
same four-deletion hafnian. Their vanishing makes both incident cofactors
zero by another retained-vertex expansion, contradicting the nonzero
diagonal entry. Neither argument uses unadmitted scalar-pencil identities.

### TR and CR: cubic triangles and the crown boundary

At a cubic root, an off-diagonal scalar inverse entry is `2bc` times the
hafnian deleting the root and its three neighbors. Its vanishing makes all
cofactors between those neighbors zero. Two adjacent cubic vertices with a
common neighbor have, when their other neighbors differ, the exact identity
`(MC)[p,t]=2 M[p,q] C[q,t]`. The coincident-neighbor case is already covered
by the preceding zeros. All four nonshared incident cofactors vanish, so
`M[p,q] C[p,q]=tau`. A cubic common neighbor forces this cofactor zero,
contradicting `tau!=0`. The excluded degree-at-least-four corollary is unused.

For CR, I verified the complementary-nullity isomorphism explicitly:
`M(0,x)=(y,0)` implies `C(y,0)=tau(0,x)`, with the converse from `MC=tau I`.
It gives the stated rank and boundary-injectivity relations. The Schur
complement formula in the nonsingular case is also correctly scaled by
`tau`; it does not assert a hafnian Schur factorization.

In the crown-plus-edge case, neighborhood zeros make the internal other-color
cross block diagonal. The two mixed words using the exterior edge give both
exterior adjacency and cofactor blocks zero. Complementary nullity then
forces exactly one zero diagonal pair internally. The cofactor matrix in
the remaining/pair/exterior ordering has an invertible pair-to-exterior
block. Its inverse equations force each exterior adjacency row to have
neighbors only in that pair, hence degree at most two. SD makes these two
isolated matching edges; the remaining inverse block is a matching on the
other missing crown pairs. Both other colors consequently share at least
`r-2>=1` matching edges. Their corresponding mixed word has a unique nonzero
term. The entire argument needs both other colors; the scalar crown control
does not contradict it. CR's unused spanning corollary is not an input.

## Eight- and ten-site assembly

At eight sites NB bounds degrees by two and SD forces each color to be a
perfect matching. A shared edge between two colors immediately gives a
unique nonzero mixed coefficient. For the edge-disjoint case, fixing the
first matching is justified by arbitrary vertex relabeling. The verifier's
least-vertex recurrence enumerates every labeled perfect matching exactly
once. It checks all eligible ordered pairs and requires exactly one supplied
case per pair; missing, duplicated, or ineligible cases fail.

The witness is an extra perfect matching contained in the three-color union.
Each vertex has a unique incident edge of its specified color, so its induced
word has exactly one compatible matching. It is mixed because a pure witness
would be one of the original three. Arbitrary nonzero complex edge weights
therefore give one nonzero monomial, with no cancellation available. This is
a finite proof of the terminal matching lemma; the weighted-source reduction
is the analytic chain above.

At ten sites the only possible color components are isolated edges and cubic
components. I checked H10's arbitrary five-site common-isotropy argument:
inversion and BC force the remaining color to split across two odd shores,
contradicting its nonzero hafnian. Neighborhood zeros then bound the clique
number of every squared color graph by four and exclude five-cycles.
TR excludes cubic triangles. A shortest remaining odd cycle has length at
least seven and no chord. An exterior vertex with three cycle neighbors
would have an odd intervening arc of length at most `g-4`, producing a
shorter odd cycle. Thus every vertex has at most two neighbors on the cycle;
counting gives `3g<=2q<=20`, impossible. The cubic component is bipartite.

Its equal shores have sizes three, four, or five. Size three gives `K_(3,3)`
and an oversized square clique; size four gives precisely the crown with an
exterior isolated edge, excluded by CR; size five gives a five-site square
clique on either shore. Thus all colors are matchings. Any two matchings,
including shared edges, have a common balanced bipartition into five and
five. Their cofactor matrices vanish on one shore, contradicting the common
isotropy argument. This uses no graph census, six-site induction, or SAT claim.

## Executable audit and independent controls

I read `verify.py`, the separate certificate generator, and all three frozen
checker scripts. The generator filters four-edge subsets of the 28 edges.
The verifier does not import it and instead uses the least-vertex recurrence.
Its witness check examines all 105 matchings, as well as the support, color,
uniqueness, and complete ordered-pair coverage conditions.

The manifest check establishes integrity and a closed acyclic scoped node
inventory. It does not mechanically prove the semantics of the written
proofs or authorship of an audit. Its own manifest hash must remain bound by
this report and the admission record; replacing a manifest and all its files
would otherwise define a different package. The current-text source hashes
and surviving freeze hashes are both checked, and the report clearly
separates this integrity function from mathematical truth.

All new verifier checks raise explicit exceptions. Historical scripts use
`assert`; the wrapper's explicit `compile(..., optimize=0)` preserves these
checks under an optimized interpreter. The deliberate false rotation
identity is rejected under `-O`, so this is tested rather than merely assumed.
The other mutations reject a missing case, a pure substituted witness, and
a corrupt artifact hash. The RV replay extracts multilinear coefficients
by inclusion-exclusion from homogeneous mean degrees; its factorial
normalization and repeated-row cases agree with the proof.

I ran the **final** manifest in normal Python, `-O`, and `-I -S`. All three
outputs agreed byte for byte. The saved
[package replay](SUPERSESSION-2026-09-26-01-replay.json) records 43 pinned
artifacts, 12 nodes, 1,884 unique mixed witnesses, 58 reflection contractions,
six nonzero rational rotations, 54 homogeneous covariance checks, 1,044
matrix/cofactor comparisons, 132 triangle identities, and 12 RV comparisons
of which eight are nonzero. The four-site and scalar crown scope controls pass.
These bounded identity checks corroborate conventions; they do not prove
the all-order statements by sampling.

For additional independence I wrote
[a separate audit checker](SUPERSESSION-2026-09-26-01-check.py), importing no
proof-package code. It generates matchings by normalizing **all vertex
permutations**, a third enumeration method. It independently recovers 105
perfect matchings, 60 disjoint from the fixed red matching, and all 1,884
eligible ordered color pairs. It checks every extra matching, rather than
just the supplied witnesses: all **5,832** extra witnesses have unique mixed
words. The union matching-count distribution is:

| Matchings in the three-color union | Ordered color pairs |
| ---: | ---: |
| 5 | 864 |
| 6 | 384 |
| 7 | 432 |
| 9 | 204 |

This checker also verifies seven coefficientwise polynomial equalities over
`Z[s,t]`: the four entries of `N^T N=D^2 I`, `det(N)=-D^2`, and the two
entries of `(s,t)N=D(s,t)`. Its
[receipt](SUPERSESSION-2026-09-26-01-check.json) also agrees byte for byte in
normal, optimized, and isolated modes. Neither checker replaces the analytic
proof of why those small reflection matrices act on arbitrary-order Wick
moments.

## Provenance and corrections during review

I compared all five surviving freezes (NB, SD, TR, CR, H10) against their
current proof copies. Differences are status text, links, and integration
provenance; the mathematical arguments agree. The earlier temporary originals
are not claimed to have been recovered. The included foundation reconstruction
pins CF, BM, HP, EV, GD, and RV by current hashes; later H10 review pins BC.
My present reconstruction additionally reviews the current scoped arguments
directly, so the verdict does not rely on unavailable temporary bytes.

The initial candidate manifest was
`bafb0adaf78bb9cb2d6178e65b2e5c65f102f7b157e6521baba439ad33736114`.
I requested correction of a malformed hafnian expression in `THEOREMS.md`
and two overly broad section references. The final scope excludes EV's
contextual whole-cofactor nonvanishing sentence and other unused section-5
consequences, admitting only its source application (14); TR excludes the
degree-at-least-four corollary, which invokes SD. The author also narrowed BC
to exclude its unused later kernel discussion. These changes close literal
scope ambiguities without changing any frozen mathematical proof or audit.
I checked the final scopes and reran both checkers against the final manifest.
There is no unresolved mathematical or checker correction for the admitted
claims. I also reviewed the proposed ledger scope: it extends the terminal
frontier and restricts the remaining source domain without claiming to close
`SP-CLEAN-BRIDGE` or alter the established six-site proof.

## Hash anchors

The manifest inventories all 43 payload files, including every source and
historical audit. The following anchors identify the reviewed assembly and
the additional independent audit artifacts:

| Artifact | SHA-256 |
| --- | --- |
| Payload `manifest.json` | `17f127b063e844a100e68c4a6463dd323f1e94dbc48d3a4a92e56dae79b8a940` |
| Payload `nodes.json` | `d71bc3da2228ea6827567b3e20a03b0554b824b3e705b66b8e7aa9c15c2a7b4b` |
| Payload `THEOREMS.md` | `927d068ca4bc45108538f92350a1f72096747ee0aaf32f7a796ae2b9a4bfacf5` |
| Payload `verify.py` | `91bb19fc90f19e18d03f7bb10b982017e91d8ad892d4ec4c2f0fd589f17cc7d1` |
| Payload `build_matching_certificate.py` | `f00e25936bd012c5cdbd19f7b8e70f81b2d42fdd489aa3cc28c30407011a68ee` |
| Payload `matching8.json` | `f6f945edf09556bb1ff02c6645de83efb5ba30e50345be75b7e48be0b2484ae3` |
| Independent `SUPERSESSION-2026-09-26-01-check.py` | `22261e2e7978ae5e954e125974f839040851505ce7c493bd9e15d13a8e7102c6` |
| Independent `SUPERSESSION-2026-09-26-01-check.json` | `26d95df8bbc193d6e5758a903c42813dce73bf6082678bc7eabfcebd91e942b3` |
| Auditor's `SUPERSESSION-2026-09-26-01-replay.json` | `b9f47514ade5067e96a2cda05e8abee6e83d4ea0a6ef20b48da9c88cb854985b` |

**Final disposition:** the final payload has exact written proof artifacts,
an exhaustive finite matching certificate, reproducible bounded controls,
and this independent mathematical and checker audit. It meets the repository
baseline's stated certification standard for the scoped conclusions above.
