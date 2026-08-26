# Rep4 modular pilot terminal audit

The sole authorized lane produced an exact `F_32003` unit transcript in 7.405 s:
91 variables, 6,577 generators, basis size 1, `reduce(1)=0`, return code 0, and
empty stderr. Raw result SHA-256: `03b0ea43...`.

The lane is nevertheless **fail-closed with zero accepted coverage**. The pinned
runner divided the integer count returned by `proc_listpgrppids` by
`sizeof(int)`, so its live one-process census became zero and it reported peak
RSS/process count `0/0`. That invalidates the promised resource observation.

The exact arithmetic transcript is retained as diagnostic evidence only. No Q
lane, second chart, automatic relaunch, or same-lane rerun is authorized.
