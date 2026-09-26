# Complete independent audit of scalar-pencil and scalar-degree consequences

**Verdict: COMPLETE INDEPENDENT PASS.** Auditor:
`/root/audit_global_foundation`, 2026-09-20. All mathematical claims in the
frozen source pass with their stated hypotheses and scope. No correction
is required. Neither the source nor this audit resolves the remaining
weighted diagonal ternary system.

## 1. Frozen source, complete reads, and provenance

The complete reviewed object is
[SCALAR-PENCIL-STAR-INVARIANCE-AND-NEIGHBORHOOD-RANK.md](SCALAR-PENCIL-STAR-INVARIANCE-AND-NEIGHBORHOOD-RANK.md),
269 lines, 12287 bytes, SHA256
`4ad27d6f2c4d3dae187d51a70e9d53d47875203c0b7f12fbba248c47b723f7a0`.
The complete source and its 226-line checker were read, along with the
dependency record, frozen output, and freeze receipt. No frozen file was
modified. The source's reference to the related strict-degree proof as
pending is explicitly its status at freezing, not a mathematical premise.

The exact freeze receipt is `scalar_pencil_star_invariance_freeze_receipt.json`,
SHA256 `cd78e4251db121699672a02f65a19cebac8c599c2699b2939f854e3adb4ab50e`.
Every hash, byte count, and line count of its four frozen records was verified,
as were all seven records in `scalar_pencil_star_invariance_dependencies.json`,
SHA256 `d6655564a28cbc13a234328fc6e73634ad725d1673ced1e41a1acf0a96e40955`.
This is an eleven-record check, not a claim to audit the whole repository.

The actual proof dependencies are the following current texts in
`../unaudited-codex-higher-common-power-bridge-2026-09-05/`:

| Text | SHA256 |
| --- | --- |
| `UNIFORM-GLOBAL-EDGE-MONOCHROMATICITY-AND-COFACTOR-INVERSE.md` | `4e140eb5cd74a4e0d9869f76e975ce2f7d46c8d7d1ba9be332a8128424082e89` |
| `UNIFORM-THREE-ACTIVE-COLOR-HIGHER-PURE-RESPONSE-VANISHING.md` | `14811c0332c217e1a5520bd619482f641573b9456783404f48a93dbc3542b190` |
| `UNIFORM-ALL-ODD-TWO-COLOR-MIXED-VANISHING-AND-KERNEL-PENCIL.md` | `03edf88285ca2a0d1dda8354d266b5d3e329be05149129e8843b2bb2dd9a12e1` |

These complete texts and their load-bearing reflection/finite-mean chain
were read and independently reconstructed in the immediately preceding
[foundation re-audit](GLOBAL-EDGE-FOUNDATION-READ-AUDIT.md), SHA256
`67eb44a90dd7d22fd6fdc40140b41596d2eb13d020be145c3c47338bb2143d7a`.
Their present hashes still agree. Existing companion audit hashes in the
record provide provenance; their PASS labels are not the reason the present
argument is accepted. The separate strict-degree result is not used below.

## 2. Original root domain and scalar-pencil projection

The full source has even order `n=2m`, all three target amplitudes nonzero,
and actual ordinary quadratic edge blocks. Global monochromaticity gives
the three scalar matrices in the original target bases, with their actual
compatible cofactor inverses. Diagonal edge blocks make each color-word
amplitude exactly the product of the three corresponding principal
hafnians, including all internal cancellations.

Deleting a root leaves `2m-1` sites. Thus the higher odd theorem applied to
its three original rows has residual exponent `m-r-1`, with exactly the
range `1<=r<=m-1` stated in source (4). These are rows on the same original
core. The whole binary-palette conclusion, rather than pure vanishing
alone, is needed and is supplied by the three active target functions.

For fixed colors `a,b`, the local maps `a_q -> x_q`, `b_q -> z_q x_q`,
`c_q -> 0` are homomorphisms of the physical-site algebra. They send the
core to the scalar restriction of `L=M_a+D M_b D`, and the actual row
`X_a+z_p X_b` to its original scalar star. The coefficient of its raw
`2r+1` row product is `(2r+1)!` times the set sum `s_(p,r)`. The remaining
divided power contributes one copy per matching. Thus whole binary
vanishing gives every higher scalar-star identity in (7).

Indeterminate `z_p` causes no change of row domain: every complex value
gives a linear combination of the original two rows, and the result is
a polynomial identity in all the site parameters. No nonzero-parameter
assumption is used. Independently expanding the colors of matching edges
gives `haf(L)=tau_a+tau_b product z_v`; the only surviving vertex-color
partitions are the two pure ones. The equation `s_(p,0)=haf(L)` is the
ordinary hafnian expansion at the root, valid for every scalar matrix.

For the third-color constraint, project the original tensor to `c` at
exactly `u,v` and to `a,b` elsewhere. Diagonality forces these two `c`
vertices to match to each other, leaving precisely
`M_c[u,v] C(L)[u,v]`. All original words in this slice are mixed because
`n>=4`. Their vanishing proves the entire cofactor polynomial is zero
when the original third-color edge is nonzero. Neither a pure-cofactor
assumption nor a determinant substitution is hidden here.

## 3. Cubic matrix identity and all rank-one update coefficients

In `(L C(L) L)[p,p]`, terms with repeated cofactor indices vanish by the
defined zero diagonal of `C`, and terms containing `p` vanish by `L[p,p]=0`.
The remaining cofactor retains `p`. Expanding it at `p` gives ordered,
pairwise distinct vertices `r,s,t`, with weight
`L[p,r] L[p,s] L[p,t] haf(L off p,r,s,t)`.
Each unordered triple appears six times, proving precisely `6 s_(p,1)`.
At order four the residual hafnian is one, so the same factor persists.

For an update `L+t v_p v_p^T`, selecting exactly `j` updated matching
edges chooses a set `U` of `2j` vertices. A rank-one matrix has hafnian
`(2j-1)!! product_(u in U) (v_p)_u` on that set. Since `(v_p)_p=0`, a
contributing `U` omits `p`. Expanding the complementary old hafnian at
`p` adds one vertex `q`, and every fixed set `T=U union {q}` has `2j+1`
such choices. The resulting coefficient is exactly
`(2j+1)!! s_(p,j) = raw_response/(2^j j!)`.

This formula applies for `1<=j<=m-1`. The top update coefficient at
`j=m` includes `(v_p)_p` and is zero; there is no higher degree. Hence
the higher scalar-star identities make the full finite hafnian polynomial
constant in `t`. The derivative is the sum over unordered edges,
`(1/2) v_p^T C(L) v_p=3 s_(p,1)`, consistent with the cubic computation.
No diagonal entries are matched by a hafnian, so the possibly nonzero
diagonal of the updated matrix does not invalidate the calculation.

When `L` is invertible, direct rank-one inversion gives
`(L^(-1)-t E_pp)^(-1)=L+t v_p v_p^T`: its denominator is identically
`1-t L[p,p]=1`. The identity is valid for every `t` at that fixed initial
matrix. The source correctly does not iterate it at other roots, claim
the resulting full ternary tensor is unchanged, or assert the scalar
pencil itself obeys `L C(L)=haf(L)I`.

## 4. Every nonempty even subset of one color neighborhood

Take `U` of size `2r` in the actual color-`h` neighborhood of `p` and
use `2r` copies of `X_h` and one `X_k` in the original higher response.
To obtain the specified word on the odd core, all `h` rows must occupy
exactly `U`, in `(2r)!` orders. These rows fill every requested `h` site,
so all remaining edges and the last row must have color `k`.

The remaining sum is precisely the expansion of the actual `k` hafnian
on `V without U` at its retained root `p`. Therefore its coefficient
is source (14), including its factorial and original star weights. Every
weight indexed by `U` is nonzero by the neighborhood definition. The
word has both colors: `U` is nonempty and has even size inside the odd
set `V without p`, so a `k` site remains. Its degree is allowed since
`2r<=n-2`. Thus division by the nonzero scalar product is legitimate,
and the complementary principal hafnian vanishes.

For `|U|=2`, this gives the stated neighbor-neighbor cofactor zero. The
root-neighbor cofactor zeros follow separately from the original mixed
two-site color words; the diagonal entries are zero by definition. These
are exactly all entries of the closed-neighborhood principal cofactor
block. No claim about ordinary determinant minors or arbitrary vertex
subsets is imported. The additional rank and strict-degree consequences
of this block vanishing belong to the separately linked proof.

## 5. Scalar leaves and degree two, without other colors

Assume only the actual scalar hypotheses `haf(M)=tau!=0` and
`M C=tau I`, with `M,C` symmetric and with zero diagonals as stated.
Symmetry also gives `C M=tau I`; this is legitimate ordinary matrix
multiplication. A zero-degree vertex would make the hafnian zero.

For a leaf `p` with unique neighbor `r` of weight `a`, and `q` outside
that pair, expanding `C[p,q]` at retained `r` gives the source's sum.
In `(M C)[r,q]`, the summand with index `p` contributes `a C[p,q]`.
Every other nonzero summand retains `p`, whose forced match to `r`
contributes exactly a second `a C[p,q]`. Indices `r` and `q` contribute
zero by the appropriate diagonal definitions. Thus all `C[p,q]=0`
outside the pair. Expansion of `haf(M)` at the leaf gives
`C[p,r]=tau/a!=0`. Row `p` of `C M=tau I` now forces all other entries
in row `r` of `M` to be zero. The pair is an isolated component.

For a vertex `p` with exactly two neighbors `r,s` of nonzero weights
`a,b`, each cofactor in `(M C)[p,q]`, for `q` outside the triple,
retains `p` and deletes one of its neighbors. The other neighbor is
therefore forced, yielding `2ab haf(M off p,q,r,s)=0`. Expanding
`C[p,r]` at retained `s` expresses it as a sum of these same zero
hafnians; expanding `C[p,s]` at retained `r` does likewise. The diagonal
entry `(M C)[p,p]=a C[p,r]+b C[p,s]` is then zero, contradicting `tau`.
At the smallest possible degree-two order, four, the residual hafnian
is the empty value one and the contradiction remains valid.

It follows that a component containing a leaf is an isolated matching
edge; every other component has minimum degree at least three. A global
upper bound of two forces matching components, while an upper bound of
three forces each remaining component to be cubic. No scalar argument
in this section forbids cubic components, and the control explicitly
demonstrates why such a stronger conclusion would be false.

## 6. Exact controls and independent convention checks

The source checker, SHA256
`17e73e07a75e0ef2a2d2614b0954c7fc7498ad81ac45ad1fa68dcca41d03b197`,
was read completely and rerun using `--output` with a new path. It performs
actual recursive hafnian sums, exhaustive stated color partitions, direct
permanent sums, and rational matrix inversion. The new output
[scalar_pencil_independent_auditor_controls.json](scalar_pencil_independent_auditor_controls.json)
is byte-identical to the frozen output, with SHA256
`14ee06352f7449a040d44721eaa1ed92fd91bc3d548c483ed7fe994f3d31bb9b`.
Its checks include all 81 four-site color words, nine scalar pencils,
108 rank-one updates, all 254 mixed binary partitions of the eight-site
control, both actual cofactor inverse identities, the nonzero binary
star responses, and the exact cubic scalar example.

The binary example genuinely satisfies only two active target equations;
its nonzero cubic and quintic scalar responses therefore refute the
unjustified removal of the third-target premise. The cubic scalar example
has off-diagonal bipartite block `W`, actual cofactor matrix equal to `M`,
and `M C=3I`, while all eight degrees are three. The program checks actual
cofactors, rather than fitting an unrelated inverse matrix.

I also wrote an independent [explicit-matching checker](verify_scalar_pencil_auditor_conventions.py),
105 lines, SHA256
`cbe0898e16179c06ee17bafca80cd82c86fa178a4ec260b62687249a24a9753f`.
It materializes perfect matchings and multiplies their full update
polynomials, independently of the source checker's hafnian recurrence.
On arbitrary integer matrices of orders 4, 6, and 8 it checked 54 cubic
identities, all 228 rank-one polynomial coefficients, 36 generic leaf
expansion identities, and 27 generic degree-two expansion identities.
Every check passed exactly. These finite controls test conventions;
the source's all-order conclusions rest on the arguments above.

All frozen source, checker, output, dependency, receipt, and canonical
dependency hashes were preserved. The new artifacts are this audit,
the fresh checker output, and the auditor's additional convention script.
The remaining general weighted diagonal cancellation problem is open.
