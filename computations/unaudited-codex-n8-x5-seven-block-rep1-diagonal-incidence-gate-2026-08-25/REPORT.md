# Representative 1 diagonal-incidence gate

Status: **input/orientation census PASS; first modular chart hit its bounded wall, so zero mathematical coverage.** Representative 1 remains open.

The source system is independently regenerated from frozen representative 1: added blocks `{06,13,17,25,26,46,47}`, 12 supported matchings, and parent full-X5 digest `61640fb492640847a58cf9f5e2f1dbc3f381736d7909325f35b2dfffb211d5eb`. Its stored-edge guard is

`A06 A47^T=0`, `A47^T+A17 A46^T=0`, `A26 A47^T+A46^T=0`,

so `A46=-A47 A26^T` and the retained equations are `A06 A47^T=0`, `(I-A17 A26)A47^T=0`. The exact non-best cap03/star4 carrier census gives the two distinct response terms with factorization `A06^T K[A13^T|A35]`. Thus the only diagonal obstruction is `e_i in Col(A06) intersection ColSpan(A13^T,A35)`. The generated incidence system imposes that obstruction for `i=0`, together with full X5, the guard, and a saturated nonzero `A47` entry.

Simultaneous color symmetry reduces all 27 triples `(i,p,q)` to five entry charts `(00,01,10,11,12)`; the exact case ledger is retained. Each chart has 100 variables and 6,586 equations: 6,561 X5, 18 guard, 6 incidence, and 1 saturation. Before reconfiguration, all ten sealed rep3 inputs are reproduced byte-for-byte.

Only modular chart `p00` ran, with direct `libproc` RSS accounting and no subprocess process-list probe. It hit `WALL_CAP_60` after 60.14 seconds at 2,326,388,736 bytes observed peak RSS. Singular emitted only `INPUT_GENERATORS=6586`; neither unit nor nonunit status landed. Exact Q and all later charts were therefore barred. This is a fail-closed feasibility result, not evidence for or against the incidence stratum and not a transport claim.
