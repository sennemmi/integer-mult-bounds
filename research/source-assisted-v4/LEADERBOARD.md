# Live candidate comparison snapshot

Checked against open pull requests on 2026-10-09, with base `main` at
`3b6b66891c0ac888521cf591fe306c6286601d4f`. Exact values below are taken from
the PR bodies or recomputed from their stated rational certificates; titles are
not treated as evidence. “No checks” means GitHub reported no checks for that
head when queried. This is a snapshot; recheck the open queue before submission
and after CI.

| Rank | Candidate | Exact κ | Head commit | Dependencies and validation status |
| ---: | --- | ---: | --- | --- |
| 1 | This local frame-descent candidate | `1693453/2500000000` | not yet published at snapshot | PR200 finite bit word plus this exact 112-frame overlay; PR193/194 complex supplier; PR184 pricing/bridge; PR185 finite leaf and PR199 recurrence. Full certificate and CI pending. |
| 2 | [PR204](https://github.com/CrocSwap/integer-mult-bounds/pull/204) | `1693287/2500000000` | `2980318ff330a232dbf8415841cd45ddef68b6d7` | PR200 bit certificate + PR193/194 complex/assembly + PR185/199 wrapper. Open, ready; Actions runs ended `action_required` with zero jobs. Body says suppliers are priced, not rebuilt or replayed. |
| 2 | [PR199](https://github.com/CrocSwap/integer-mult-bounds/pull/199) | `1693287/2500000000` | `5c1fb8346615968844bc182a5376c399109670ca` | Same composed value using PR200 bit + PR194 complex + PR185/199 wrapper. Open, ready; Actions runs ended `action_required` with zero jobs. Body says PR200 certificate is vendored and priced, not replayed. |
| 4 | [PR197](https://github.com/CrocSwap/integer-mult-bounds/pull/197) | `135216063303877/200000000000000000` | `8c5e1cf07c23d843642bf2d4c76f882669edc43f` | Packed PR187 bit residuals + PR193 complex + finite leaf/bank construction. Open, ready; Actions runs ended `action_required` with zero jobs. Body records local verification and explicitly says no fresh full current-main `make verify`. |
| 5 | [PR202](https://github.com/CrocSwap/integer-mult-bounds/pull/202) | `6768823/10000000000` | `8d8d67bcf69c5ea67d3a29dbc64ba588156d6e8d` | PR200 bit + source-assisted complex + legacy leaf. Open, ready; no Actions run found for this exact head. |
| 6 | [PR200](https://github.com/CrocSwap/integer-mult-bounds/pull/200) | `166261725903847/250000000000000000` | `a1175449f34d39ff933d9d8ab23ced1f32b290ec` | New bit and complex supplier; its own complex side binds. [Exact-head full research workflow](https://github.com/CrocSwap/integer-mult-bounds/actions/runs/37944233306) had 52/52 successful jobs; separate bit-elimination and reuse workflows also succeeded. It is not the stronger composed candidate. |

The two highest public compositions reported the same exact κ. The new
candidate's exact improvement over either is `83/1250000000`. Every line remains
conditional on its inherited source and all-size contracts; open-PR claims are
not merged theorems. PR200's finite word is independently replayed by this
branch before it is combined with the new frame overlay.
