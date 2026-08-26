# Rep5 post-timeout guard-pivot quotient referee

Status: **PASS / exact three-chart design, zero solves**.

Writing `b_h=sum_l A26[h,l]A37[p,l]`, the surviving `j=p,i=q` guard expresses the saturated nonzero entry `A37[p,q]` as `sum_h A17[q,h]b_h`; therefore the three opens `b_k!=0` cover the parent chart. On open `k`, substituting `A17[i,k]=N_i P sat` makes each removed guard exactly `N_i(1-P*b_k*sat)`, which vanishes under the combined saturation `P*b_k*sat-1`. The stated forward and reverse saturation maps are mutually inverse.

Each pinned Q source independently parses as 88 variables and 6,574 distinct nontrivial generators: 6,561 full-X5 equations, twelve surviving guards, and one combined saturation. The sources remove `A17[:,0]`, `A17[:,1]`, and `A17[:,2]` respectively. The producer summary's singular `variables_removed` display leaked the final loop index `k=2`; this is a reporting defect only, corrected by the literal source census here.

No source was run, and no runtime, performance, relaunch, closure, or rep5-completion claim is accepted. The smallest recommended held diagnostic is one p=32003 `k=0` lane only, with 240/250 seconds, 8 GiB, direct-libproc/atomic guards, and stop-after-any-outcome; it remains unlaunched and unauthorized.
