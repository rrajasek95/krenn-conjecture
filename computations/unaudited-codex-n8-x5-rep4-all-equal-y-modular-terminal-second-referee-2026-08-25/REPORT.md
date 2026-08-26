# Rep4 modular terminal second referee

Status: **exact unit transcript verified; zero accepted proof coverage**.

Raw result `03b0ea43...` records return code 0, empty stderr, 91 variables, 6,577 generators, Groebner basis size 1, unit remainder 0, and `UNIT_IDEAL` in 7.404693 seconds. No Q lane, second lane, or relaunch occurred.

The resource certificate is invalid: it reports both peak RSS and peak process-group members as zero while Singular was live. Static source inspection confirms the `proc_listpgrppids` count was incorrectly divided by `sizeof(int)`. The arithmetic transcript is preserved but proves nothing under the frozen resource contract.

A corrected runner could logically generate new admissible evidence, but not under this consumed one-lane/no-relaunch clearance. It would require explicit superseding manager authorization, a wholly distinct fresh package/clearance, corrected fail-closed telemetry, and independent audit; reuse or automatic rerun is forbidden.
