# Representative 3 diagonal-incidence closure

Status: **representative 3 is now genuinely closed in all ranks over `Q`.** This supersedes the earlier pairing-only result; no transport to another support is claimed.

The exact nonzero branch uses the independently source-oriented substitution `A36=-A37 A26^T`, all 6,561 full-X5 equations, the 18 entries of `A06 A37^T=0` and `(I-A17 A26)A37^T=0`, and the six incidence equations

`A06 x=e_i`, `A35 y+A37 z=e_i`.

For `A37` nonzero, choose a nonzero entry. Simultaneous `S3` color symmetry sends `i` to zero; the residual swap of colors 1 and 2 leaves exactly five entry orbits: `(0,0)`, `(0,1)`, `(1,0)`, `(1,1)`, `(1,2)`. Every one of the five saturated ideals is a terminal unit ideal first modulo 32003 and then over exact `Q`. Thus for every `i`, `e_i` cannot lie in both `P=Col(A06)` and `Q=ColSpan(A35,A37)`. All three diagonal functionals are live. Since the guard also makes `P` proper, the fixed-`I` cap pairing is live, so cap03/star4 is active.

If `A37=0`, the guard forces `A36=0`; then `L67=0`, and nonzero full-family `A67` makes cap67 active. Hence ranks 0 through 3 are covered.

The generated parent equation digest and term census reproduce byte-pinned semantic data. Each chart was run sequentially under 8 GiB, with 60-second modular and 120-second exact-Q watchdogs. This package closes representative 3 only; the other representatives and the 16 non-full-family records remain separate obligations.
