# Archive audit: chart-26 normalized `t`-saturation beyond degree seven

## Terminal outcome

No archived computation proves either `t^8` membership or `t^8`
nonmembership for the frozen 49-row class in the same 240-variable normalized
chart-26 ideal.  The only pre-existing degree-eight artifact in that exact
ring is an initial-boundary exporter: it records the same 190 new columns,
146 violations, and 10,440 top rows, then states that its full relative
closure exceeded the combined two-million-row / 200,000-column guard before
a rank test.

The new bounded first-shell audit improves that frontier but is still not a
saturation decision.  A literal diagonal `146 x 146` private-row packet
repairs all 190 first-boundary columns, after which 252 columns cross the
extended functional.  Its logical digest is
`cf37fd401cd2b53cfe7e0fe45132f9e409960e6bb617ce86574e49119cba9cdb`.

## Strict provenance table

| provenance | artifact | exact result | may be imported into the 252-column boundary? |
|---|---|---|---|
| **Same ideal**: `Q[y_1,...,y_240,t]`, all 6,558 normalized mixed generators homogenized to degree four | [`n8-chart26-normalized-degree7-critical-closure.md`](../../notes/n8-chart26-normalized-degree7-critical-closure.md) | Exact 49-row dual, digest `b0f137c8...`, proving only `t^7` nonmembership for the contracted constant class | **Yes; this is the class being prolonged.** |
| **Same ideal** | [`results_degree8_initial_core.json`](../unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/results_degree8_initial_core.json) and [`audit_degree8_dual_extension.py`](../unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/audit_degree8_dual_extension.py) | Exact 190/146/10,440 initial boundary; subsequent closure hit its size guard; no result file for the attempted extension | **Yes as a frozen seed only.** It contains no degree-eight dual, solution, or closure certificate. |
| **Same ideal** | [`n8-chart26-complete-degree5-buchberger.md`](../../notes/n8-chart26-complete-degree5-buchberger.md) | All 84,005 original-original degree-five cells are exact, source-labelled, mutually reduced transports | **Yes as syzygy/exchange cells.** Exact incidence below shows they touch 218/252 crossings. |
| **Same ideal** | [`n8-chart26-first-degree6-compatibility.md`](../../notes/n8-chart26-first-degree6-compatibility.md) and [`n8-chart26-cross-vertex-bianchi.md`](../../notes/n8-chart26-cross-vertex-bianchi.md) | Three exact degree-six cells and the four-corner Bianchi identity; not a complete degree-six layer | **Potentially**, but no archived contraction of these cells against the 252-column shell exists. They cannot be credited as closure. |
| **Related filtration, not the same module**: original 252-variable balanced port degree, off-support `K`-adic filtration | [`n8-full-source-degree6-bockstein.md`](../../notes/n8-full-source-degree6-bockstein.md) | Exact 100-row exponent-one dual in one balanced multidegree | **No dual import.** After support normalization it has 903 violating columns among 1,091 incident columns; six columns already contract its target to `1+Tail`. |
| **Related filtration, same raw chart support** | [`anchor-k Rust report`](../unaudited-codex-anchor-k-rust-2026-08-20/REPORT.md), chart-26 cutoff-eight structure | Chart 26 is exact through `K^7`; cutoff eight closes to 2,248,460 rows / 4,137,457 columns and peels to one 680,620 x 935,795 core, with no certificate or dual | **Columns may be reconstructed**, but the matrix fixes a balanced support-exponent representative. No frozen map quotients it to the normalized `t`-homogeneous shell, so no row/dual is presently reusable. |
| **Different support chart and stabilizer** | Same report, orbit-0 cutoff eight/nine | Exact `K^8` identity and exact `K^9` obstruction for the maximally symmetric orbit-0 chart | **No.** This is a different twelve-cell support chart, quotient group, target residual, and filtration. Shared word labels do not transport coefficients. |
| **Proper quotient/face of the same normalized chart** | [`n8-chart26-terminal-triangular-exposure.md`](../../notes/n8-chart26-terminal-triangular-exposure.md), [`n8-chart26-augmented-terminal-chain.md`](../../notes/n8-chart26-augmented-terminal-chain.md), [`n8-chart26-terminal-pure-anchor-bypass.md`](../../notes/n8-chart26-terminal-pure-anchor-bypass.md) | Exact tangent identity minor and exact one-spoke / 96-coordinate / five-row identities after setting many other coordinates to zero | **Only as candidate labels.** These polynomial equalities are face-local and acquire extra terms in the full 240-variable ring. |
| **Different chart/source quotient** | [`n8-literal-hafnian-hpl-local-no-go.md`](../../notes/n8-literal-hafnian-hpl-local-no-go.md) and chart-25 Schur/Bockstein notes | Exact chart-25 four-dimensional relative obstruction and HPL provenance no-go | **No.** The abstract Schur criterion is reusable, not its rows or dual. |
| **Different 45-parameter branch; no proved coordinate map** | [`n8-p5-degree8-mixed-components.md`](../../notes/n8-p5-degree8-mixed-components.md) and [`n8-p5-generic-L-nakayama-prefix.md`](../../notes/n8-p5-generic-L-nakayama-prefix.md) | Exact P5 strict jets through degree eight on selected components; the notes explicitly deny a map to normalized chart 26 | **No.** Neither tails nor dual-number reductions live in the normalized chart-26 ring. |

The dangerous-chart component/mate Gröbner calculations are still farther
away: they impose branch equations, localizers, fixed-left data, or mate
variables.  They are not linear source identities in the 240-variable
normalized ideal and contribute no degree-eight rows or dual weights here.

## Exact reusable-cell incidence

A read-only literal incidence audit compared the 252 crossings with the
complete degree-five chart-26 cell census.  For a crossing source column
`m H_w` of multiplier degree four, it checked every support-stabilizer
translate and every degree-five pair whose `H_w` leg has multiplier

```text
(LCM / LM(H_w)) * n,    degree(n)=3.
```

The result is:

```text
crossing columns                         252
crossings touched by a translated d5 cell 218
literal translated cell incidences       943
incidences whose companion also crosses  481
crossings untouched by the complete d5 layer 34
```

This makes the complete degree-five layer a genuine reusable exchange
packet.  It is not itself a solution: each cell is a source combination of
two original columns, and the archive contains no contracting homotopy or
coefficient solve showing that these 943 relations kill the boundary.

The 34-column remainder has profile census

```text
332:1, 422:1, 431:7, 44:1, 521:8,
53:3, 611:5, 62:5, 71:3.
```

Its exact canonical word/multiplier list is:

```text
00000002 2a6f7eb5
00000011 0788e3f2
00000012 072775a5   00000012 0775d8e1
00002002 0521b9f0   00002011 07617eec
00002012 0708d9ef   00002022 0708d0f2
00002102 0773d0ea   00012101 055086ea
01000000 2a6e7eb5
01000010 0e4950d5   01000010 2a6375da   01000010 335a75da
01010010 0e334abf
11000011 345e9ea6   11000212 345d95a6
11010011 345d88bf   11012111 0d4fd2ea
11111112 345d7ebe
12000000 0949dee1   12000000 88a7eaf4
12000002 1d2240c0
12002000 0949d8e1   12002000 0951b7ea
12011000 0d4ccdf7   12011010 0c4c8ad5
12012000 0e4cbaf6   12012111 0d4cd2ea
12111000 7e80b4ea   12111000 8084babd
12111100 808dc3f4
12111220 8084abba   12111220 808dc4e4
```

The named first Bianchi packet is much smaller than the full degree-five
family: of its original word codes `1,2,10,11`, only code `2`
(`00000002`) occurs, on four crossings.  Hence citing that single cell as
coverage of the 218 would be unsound; the exhaustive degree-five transport
family is load-bearing.

## Face-local overlaps and dual audit

Some face-local source labels do meet the second boundary:

```text
terminal one-spoke rows:  01000010 on 7 crossings; 01000111 on 1
five-row carrier bypass:  12012120 on 6 crossings
orbit-0 cutoff-8 words:   00000011 on 1 crossing
```

The first two overlaps are useful candidates for lifting their face
identities back to the full ring.  They are not current repairs, because the
face equations discard additional matching terms.  The orbit-0 overlap is
only a shared word label and has no chart-26 provenance.

No archived exact dual is reusable on the 252-column boundary:

1. the full-source 100-row dual fails immediately after normalization;
2. the orbit-0 cutoff-nine dual belongs to another chart and filtration;
3. chart-25/HPL duals belong to another quotient; and
4. the chart-26 cutoff-eight archive produced structure only, not a dual.

Therefore the smallest honest next interface is the 34-column complement
after adjoining the complete degree-five exchange packet, followed by the
three frozen degree-six cells and their stabilizer transports.  This is a
strictly smaller source-faithful target than either the abandoned full
relative closure or the 680,620-row K-adic core, but it is not yet an exact
membership test.
