# Manifest

* Checker: `audit_orbit0_k14_interface.py`
* Result: `results_orbit0_k14_interface.json`
* K16 cover checker: `audit_k16_anchor_cover.py`
* K16 cover result: `results_k16_anchor_cover.json`
* Checker SHA-256: `7a9891d5fc4d8964518147c0202e0f29b7393e7bed3a7651beb053eb4402c19a`
* Result SHA-256: `a67a08fd97c5cd10cfb5e7dd72db2502971c16408bd058dce4d12cbbb2f0adb3`
* Logical SHA-256: `9d5e7a8148220b16ff7306ad29a3635fd9cadd79204e02a7569d95e197886311`
* K16 cover checker SHA-256: `b338ce0c08ea94107ae148f03a89ff5183d55eb28fc58bb1aedfdaaa8f20a4cd`
* K16 cover result SHA-256: `5efffe78e3fd9c42ca91be2a6a10bb7d4d4cc0fa13d986ca411cc692c999dfdf`
* K16 cover logical SHA-256: `a411a1c11d40b950e86556d63d82596db2f9fcfe21e7a67cbe39bae1d9208920`
* Frozen interface checker SHA-256: `faeb01b43c9c2643d71382d98747350d8f08a10797e8061c6d6738bffaf4949b`
* Frozen sparse `R8'` input SHA-256: `62013c8a8453ffe68e6ef08740859db6efecaf825f121c19dc885b6afa7feb4b`
* Replay modes: standard, optimized (`-O`), isolated (`-I -S`); both checkers PASS with mode-independent logical digests.
* Finite cover solver: Z3 4.16.0, with exact rational inconsistency cores checked independently in Python.
