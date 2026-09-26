# Independent audit: original-frame monochromaticity and cofactor inversion

**Verdict: COMPLETE PASS without source correction.**
Independent auditor: `/root/audit_tree_chords`, 2026-09-13.
All 222 frozen source lines and all 79 receipt lines were read. Every
matrix identity, its actual-source input, and the exact remaining
weighted characterization were reconstructed independently.
This audit accepts the stated research composition; it does not certify
an all-order exclusion or alter a formal registry status.

## 1. Exact source and reviewed inputs

The audited [source](/tmp/krenn_global_edge_monochromaticity_and_cofactor_inverse_20260913.md)
has 222 lines, 10304 bytes, SHA256
`2d04542fdbd6d772e5487e5276db8ba724df047cd6027b96f68c54c1848359f2`.
The [author receipt](/tmp/krenn_global_edge_monochromaticity_and_cofactor_inverse_20260913_freeze_receipt.json)
has 79 lines, 3819 bytes, SHA256
`cb81eccd5a946a03a307d4a18293e2078f1c1a422674dab9c9eac2b502d0d0d3`.
Both remain unchanged.

The complete [all-even omission theorem](/Users/rishi/workplace/krenn-conjecture/computations/unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-ALL-EVEN-OMISSION-PURE-RESPONSE-VANISHING.md)
was reread: 211 lines, SHA256
`450f75c2c6280c601e2d012c1ae892d1f18f14f62aae8ec5dd448c3a157b7688`.
Its complete [independent audit](/Users/rishi/workplace/krenn-conjecture/computations/unaudited-codex-higher-common-power-bridge-2026-09-05/UNIFORM-ALL-EVEN-OMISSION-PURE-RESPONSE-VANISHING-AUDIT.md)
was also reread: 207 lines, SHA256
`bfc395daa25032cb31238a4a7a81288db4a4762054cc613a37020a7b4ded977b`.
Only its positive-even degree-two instance is required by the new proof.

I read the entire separate [adversarial reconstruction](/tmp/krenn_all_even_omission_covariance_adversarial_recheck_20260913.md),
177 lines, SHA256
`d50c57c450af70366a209ba9887345f0beef6ecac51d6d48b04f5ea27f90a279`.
It is explicitly the original author's additional challenge, not a
substitute for independent reasoning. Its finite controls were read,
not rerun or used as an extrapolation establishing arbitrary order.
I also fully read the historical [conditional 167-line deduction](/tmp/krenn_conditional_scalar_cofactor_inverse_and_monochromaticity_20260913.md),
SHA256 `ec3e811e3846c640c5d450fe56b06483692e16a1f70942a864e923383e6ea08c`.
That source and its receipt remain immutable.

## 2. Source-relative use of EV1 and its foundation

For an actual full source on n=2m+2>=4 sites, deleting p leaves an
odd ordinary core on 2m+1 sites. The three original p rows, INCLUDING
their components at q, have whole responses tau_i i^(V minus p).
All three coefficients are nonzero, and these pure tensors are linearly
independent. The resulting row space has response rank three and all
three target functionals active. Thus it satisfies the actual premises
of the all-even theorem; no auxiliary binary or rank-one target example
is being substituted for this full source.

Omitting q from that same odd core leaves Q=A restricted off p,q.
Restriction of its original p rows gives exactly X_i^(p,q). The degree
two omission response is X_i^(p,q) X_h^(p,q) Q^[m-1]. Both rows belong
to ONE original p family. EV1 therefore applies to every p!=q and every
i,h, with the claimed power, even if the direct pq block is nonzero.
This use neither mixes p and q families nor assumes a whole response zero.

The reread of the reviewed foundation confirms the precise cancellation.
On the omitted even core, put E(U)=sum_r U^(2r)Q^[m-r]/(2r)! and F=E(0).
Exact occupancy of the omitted site in the original finite odd mean is

    d_h(L)E(U(L))+partial_(V_h)E(U(L)).

The reviewed higher-odd result kills every higher binary output sector,
so its h,k projection equals f_h(L)h^S. It is the whole binary conclusion
that is used here, not pure-coefficient vanishing alone. In ordinary
replicas, the quadratic sum and local alternating differential operators
are invariant under SO2. Physical extraction is performed AFTER that
ordinary calculation, not rotated inside the site-square-zero quotient.
For the even-site product pairing B this gives

    B(E(U),E(U))=B(E(sqrt(2)U),F),
    B(E(U),partial_V E(U))
        =B(F,partial_V E(sqrt(2)U))/sqrt(2).

The second identity follows by differentiating the means (U,U+tV);
E'(0)=0 removes the second rotated derivative. It holds for the actual
star direction V_h even when V_h is outside the restricted row space.
At sqrt(2)L, BOTH d_h and f_h scale by sqrt(2). Substitution cancels
the entire d_h bracket by the first identity. The remaining relation is
f_h(L)[k^S](E(U(L))-F)=0. Cancel the nonzero polynomial f_h in C[D],
separate degree two, and polarize. This is EV1. No cofactor division,
positive weight, invertible covariance, or omitted direct-row term enters.
The composition does not require re-proving the separately reviewed
higher-odd theorem or any assertion about all-three-color mixed words.

## 3. Scalar definitions and diagonal matrix entries

M_h is the actual symmetric same-color n-by-n matrix with zero diagonal.
C_h[r,q] is its actual hafnian after deleting DISTINCT r,q. Its diagonal
is set to zero by definition and is not a repeated-deletion cofactor.
B_ih[p,r]=A_pr(i,h), p!=r, has zero diagonal. It need not be symmetric:
reversing vertices also reverses colors, so B_ih^T=B_hi, not B_ih in
general. No unjustified symmetry of these off-color matrices is used.

For the p,p entry, expansion by the unique partner r of p gives

    (B_ih C_h)[p,p]
      =sum_(r!=p) A_pr(i,h) haf(M_h[V minus p,r]).

This is the ENTIRE coefficient of the word i at p and h elsewhere.
When i=h it is tau_h; otherwise it is a mixed word and is zero.
All matching terms are present exactly once. This step uses only the
original whole source equation, with no EV1 or individual-cofactor
nonvanishing premise. In particular haf(M_h)=tau_h already holds.

## 4. Off-diagonal entries and the ordered-pair normalization

For p!=q, matrix multiplication first sums over r. Its r=p term is
zero from the diagonal of B_ih; its r=q term is zero from the DEFINED
diagonal of C_h. For all remaining r, the core defining C_h[r,q]
contains p. Expand this scalar hafnian at that retained p, whose
partner s lies outside p,q,r. This gives exactly

    (B_ih C_h)[p,q]
      =sum_(r,s in V minus p,q; r!=s)
          A_pr(i,h) A_ps(h,h)
          haf(M_h[V minus p,q,r,s]).

Every ordered r,s term is also exactly one placement in the raw product
X_i^(p,q) X_h^(p,q). Repeated-site placements vanish physically. The
remaining sites number n-4=2m-2, and their pure-h coefficient in
Q^[m-1] is the same actual scalar hafnian. Thus the displayed sum is
precisely [h^S]X_i^(p,q)X_h^(p,q)Q^[m-1], which vanishes by EV1.

There is no factor 1/2: the matrix calculation distinguishes r, the
partner chosen in its first sum, from s in the subsequent expansion.
The row product likewise distinguishes its two row factors. If i=h,
both sides count each unordered placement twice. The only divided
power is that of the residual quadratic, counting each residual
matching once. This check includes the empty residual matching at n=4.

## 5. Inversion and elimination of every original off-color cell

Combining the diagonal and off-diagonal calculations yields

    B_ih C_h=delta_ih tau_h I_n,    M_h C_h=tau_h I_n.

The second equality is between square scalar matrices over C, with
nonzero tau_h. Its determinant implies both factors invertible, and
C_h=tau_h M_h^(-1). This is ordinary finite-dimensional matrix
cancellation, unrelated to zero divisors in the physical algebra.
The first equality then gives B_ih=0 for every i!=h.
For an arbitrary original cell A_pr(i,j) with i!=j, take h=j:
it is an entry of B_ij and is therefore zero. This exhausts all six
off-color cells in every original 3-by-3 block, in the FIXED target
bases. There is no coordinate change or extremal representative.

C_h is not an arbitrary fitted inverse; its entries are the compatible
hafnian cofactors used in the retained-p expansion. The proof does not
assume invertibility in advance. Matrix invertibility also does not say
every individual cofactor entry is nonzero: the four-site control has
many zero entries in its invertible matching cofactor matrices.

## 6. Exact residual characterization and converse

After the proved diagonality, a word with color classes S_a,S_b,S_c
can receive a nonzero matching contribution only from edges internal
to each class. Such a contributing perfect matching is uniquely a
triple of matchings, one on each S_h. Conversely every such triple
is a contributing matching of V. Therefore its whole coefficient is

    haf(M_a[S_a]) haf(M_b[S_b]) haf(M_c[S_c]).

All cancellations within any factor are retained. Empty parts have
hafnian one, and odd parts have hafnian zero. The constant words give
haf(M_h)=tau_h!=0. Every mixed word is precisely a partition with at
least two nonempty parts, so demanding its displayed product zero is
both necessary and sufficient for the entire target equation.

Conversely, any three symmetric complex zero-diagonal matrices with
these partition conditions define the literal physical quadratic
sum_(p<q,h) M_h[p,q]h_p h_q. The same matching bijection proves its
whole top equals the required target. Thus source (12), together with
the new theorem, is an exact all-order reformulation, not merely a
relaxation or coefficient fit. The inverse identities are consequences
of any such actual source and need not be independent hypotheses of
this converse.

This leaves the complex weighted diagonal system. A vanishing hafnian
can be a cancellation of nonzero monomials; the proof has not converted
that condition into PMValid support or absence of individual mixed
matchings. It has also not converted hafnian restrictions into ordinary
rank tests. No unrestricted diagonal-source exclusion is proved here.

## 7. Endpoints, finite-order citations and actual scope

At n=4, m=1. The two retained vertices supply r,s, and the remaining
hafnian is haf(empty)=1. EV1 uses Q^[0]=1; no negative power occurs.
The displayed K4 quadratic has exactly three perfect matchings and
whole top a^4+b^4+c^4. Each same-color matrix is a disjoint matching,
and with the displayed unit weights its cofactor matrix is its inverse.
The factor two for coincident row choices is consistent on both sides.
No n=2 application of positive-even omission is asserted.

Each original local space is explicitly C^3. No conclusion about
unlisted extra departure or receiving directions is smuggled into the
all-cells claim. The field is C; the all-even polarization does not
supply an arbitrary-characteristic extension of this composition.

I inspected the statements and scope sections of the cited
[finite diagonal proof](/Users/rishi/workplace/krenn-conjecture/proofs/eight-site-diagonal-obstruction.md),
1097 lines, SHA256
`04a46e1c802e5453a104a6e1841f4e806d919a0a285d256fc944aa94318217ce`.
They cover nonzero unequal pure amplitudes at the stated finite orders
and explicitly withdraw a uniform n>=10 extension. Those certificates
were not rerun or re-registered. This audit adds no formal certification,
new registry status or all-order nonexistence result. It accepts the
mathematical reduction to that separately studied weighted system.

## 8. Preservation and final verdict

All 389 actual canonical texts, SHA256 values and line counts, including
188 audits, match [the authoritative manifest](/tmp/krenn_inactive_minor_and_operation_rigidity_synthesis_20260913_final.json),
SHA256 `4864beef8189e94e5c2d4016f0eb6c920a0c5889f1f1ad92dbf77346883c1020`.
The new source and receipt, its two direct foundation files, the challenge
note, both historical conditional files, and the finite scope citation
were checked against their frozen sizes, hashes and line counts.
All seven records in the latest local frozen inventory were also checked
as complete texts, hashes and line counts, with no mismatches. This is
not a claim of a new check of every historical frozen inventory.
Only this new companion was written; canonical and prior frozen files
remain unchanged. Absolute local links were checked on final readback.

**Final verdict: COMPLETE PASS.** The original-frame diagonality,
actual scalar cofactor inverse, and exact weighted partition-hafnian
reformulation follow from the whole source equation and the reviewed
positive-even omission input. No extra source-compatibility premise,
PMValid reduction, general weighted exclusion or formal closure is used.
