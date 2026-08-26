# Representative 2: exhaustive carrier closure

Status: **superseded/retracted: rep2 is closed only when `A57=0`; nonzero ranks have pairing activity only.** The earlier all-rank claim omitted the three separate diagonal-functional conditions.

The verifier regenerates all 105 perfect matchings and the 13 supported matchings of rep2, then enumerates every supported cap and each of its six star centers: 90 carrier configurations. The exact term-count histogram is `2:8, 3:14, 4:28, 5:8, 6:12, 7:12, 8:4, 9:2, 10:2`. All eight minimum two-term carriers reproduce the expanded sealed ledger literally.

The frozen 64-to-13 best record used cap03/star2 with common factor `A35`; its left space `RowSpan(A04^T,A06^T)` is not forced proper when `A06` is singular. Exhaustive enumeration exposes the needed non-best cap03/star4 carrier. Its two distinct source-labelled response matrices are

`R26(K)=A06^T K A23^T` and `R56(K)=A06^T K A35`,

so the response row space is `P tensor Q` with `P=Row(A06^T)=Col(A06)` and `Q=ColSpan(A23^T,A35)`. All 18 coordinate expansions are stored and hashed.

If `A57=0`, the guard forces `A56=0`, so the cap67 response map vanishes and nonzero full-family `A67` makes cap67 active. If `A57` is nonzero, `A06 A57^T=0` makes `A06` singular, hence `P` proper. Since the cap block `A03=I`, its pairing cannot lie in `P tensor Q`. This is only pairing activity: each `Kii` needs the extra exclusion `not(e_i in P and e_i in Q)`.

The verifier includes the compatible local countermodel `A57=E11`, `A56=-E11`, `A06=A23=A35=E00`, `A17=A26=I`. The guard holds and trace pairing is live, but `E00=A06^T E00 A35` lies in the response row space, so `K00` is dead. Nonzero ranks remain open.

The exhaustive carrier census remains valid; only its activity conclusion is retracted. This package makes no claim for the other representatives or non-full-family support strata.
