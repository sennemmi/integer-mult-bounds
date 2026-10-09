#!/usr/bin/env python3
"""Independently replay PR200's certified bit word with the frozen frame descent."""

from collections import Counter, defaultdict
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "research/paired-cube-diagonal-bit-168"
BIT = UPSTREAM / "bit"
if sys.flags.optimize:
    raise SystemExit("run without -O")
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
try:
    import resource  # noqa: F401
except ImportError:
    resource = types.ModuleType("resource")
    resource.RUSAGE_SELF = 0
    resource.getrusage = lambda _: types.SimpleNamespace(ru_maxrss=0)
    sys.modules["resource"] = resource
sys.path.insert(0, str(BIT))
sys.path.insert(0, str(UPSTREAM / "arithmetic"))

from word import Candidate, need
from prove import certify, js
from prime_witnesses import certificate as prime_certificate
from terminal import prove as prove_terminal


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def source_pins():
    manifest = read(OUT / "SOURCE.json")
    actual = {name: digest(ROOT / name) for name in manifest["files"]}
    need(actual == manifest["files"], "frame-descent source pins changed")
    upstream_verifier = load_module("pr200_original_verifier", UPSTREAM / "verify.py")
    need(upstream_verifier.pins(), "PR200 source closure pins changed")
    return actual


def add_frozen_frames(word, records):
    C = word.C
    for raw_id, raw_rows in sorted(records.items(), key=lambda item: int(item[0])):
        frame = int(raw_id)
        need(frame not in C.B and frame not in C.A and frame not in C.dimf,
             "new frame identifier collides with the PR200 frame table")
        reduced, _ = word.module.reduce_rows(raw_rows, word.h)
        rows = tuple(sorted(map(tuple, reduced), key=lambda row: next(i for i, x in enumerate(row) if x)))
        need([list(row) for row in rows] == raw_rows, "frozen frame rows are not canonical")
        dual, _ = word.module.kernel(rows, word.h)
        C.B[frame], C.A[frame], C.dimf[frame] = rows, dual, len(rows)


def physical_chain_operations(word):
    entries = {role: [] for role in range(word.R)}
    for operation in word.phase1 + word.rest:
        a, b, _ = word.ops[operation]
        entries[a].append(operation)
        entries[b].append(operation)
    recipient = {donor: birth for birth, donor in word.pairs}
    chains = []
    for role in range(word.R):
        if role in word.donor:
            continue
        chain = list(entries[role])
        if role in recipient:
            birth = recipient[role]
            chain.extend(entries[birth])
        chains.append(chain)
    return chains


def physical_operation_contexts(word):
    """Return both actual predecessor/successor frames for every physical write."""
    entries = {role: [] for role in range(word.R)}
    for operation in word.phase1 + word.rest:
        a, b, _ = word.ops[operation]
        entries[a].append(("op", operation))
        entries[b].append(("op", operation))
    for j, role in enumerate(word.w["rootroles"]):
        entries[role].append(("frame", word.w["root_frame"][j]))

    # Candidate.pairs stores (birth role, donor role), matching word.row().
    birth_for_donor = {donor: birth for birth, donor in word.pairs}
    start = {role: word.w["source_frame"][node] for node, role in word.source.items()}
    start.update({role: item["frame"] for role, item in word.gauge.items()})
    contexts = {operation: [] for operation in range(len(word.ops))}
    for role in range(word.R):
        if role in word.donor:
            continue
        chain = list(entries[role])
        if role in birth_for_donor:
            birth = birth_for_donor[role]
            chain.append(("frame", word.gauge[birth]["frame"]))
            chain.extend(entries[birth])
        chain.append(("frame", word.w["full_frame"]))
        previous = start.get(role)
        for index, (kind, value) in enumerate(chain):
            frame = word.opframe[value] if kind == "op" else value
            if kind == "op":
                next_kind, next_value = chain[index + 1]
                next_frame = word.opframe[next_value] if next_kind == "op" else next_value
                contexts[value].append((previous, next_frame, role))
            previous = frame
    need(all(len(contexts[i]) == 2 for i in contexts),
         "each physical write has both port contexts")
    return contexts


def apply_plan(word, plan, selection):
    selected = plan["selected_operations"]
    need(plan["selected_count"] == len(selected), "selected-operation count")
    indices = [item["operation"] for item in selected]
    need(len(indices) == len(set(indices)), "duplicate selected operation")
    sink_roles = {word.w["rootroles"][item["root"]] for item in selection}
    sink_ops = {operation for role in sink_roles for operation in word.role_ops[role]}
    need(not (set(indices) & sink_ops), "a terminal-sink write was changed")
    contexts = physical_operation_contexts(word)

    add_frozen_frames(word, plan["new_frame_records"])
    for item in selected:
        operation = item["operation"]
        need(word.opframe[operation] == item["old_frame"], "selected operation parent frame")
        need(word.C.dimf[item["old_frame"]] == item["old_dimension"], "old frame dimension")
        need(word.C.dimf[item["new_frame"]] == item["new_dimension"], "new frame dimension")
        operation = item["operation"]
        _, _, node = word.ops[operation]
        rows = []
        for predecessor, successor, _role in contexts[operation]:
            if predecessor is not None:
                rows.extend(word.C.B[predecessor])
        bits = word.C.sup[node]
        while bits:
            low = bits & -bits
            bits -= low
            rows.append(word.C.chi[low.bit_length() - 1])
        reduced, _ = word.module.reduce_rows(rows, word.h)
        canonical = tuple(sorted(map(tuple, reduced), key=lambda row: next(i for i, x in enumerate(row) if x)))
        need(word.C.B[item["new_frame"]] == canonical,
             "replacement frame is not the exact join of both predecessors and the value span")
        need(all(predecessor is None or word.C.sub(predecessor, item["new_frame"])
                 for predecessor, _successor, _role in contexts[operation]),
             "replacement frame omits an actual predecessor")
        need(all(word.C.sub(item["new_frame"], successor)
                 for _predecessor, successor, _role in contexts[operation]),
             "replacement frame is outside an actual successor cap")
        word.opframe[operation] = item["new_frame"]

    chosen = set(indices)
    for chain in physical_chain_operations(word):
        for left, right in zip(chain, chain[1:]):
            need(not (left in chosen and right in chosen),
                 "selected endpoint moves conflict on a physical role chain")

    word.w["op_frame"] = word.opframe[:]
    word.changed_frames = [i for i, (old, new) in enumerate(zip(word.original_opframe, word.opframe))
                           if old != new]
    return selected


def build():
    pins = source_pins()
    plan = read(OUT / "frame-descent.json")
    need(plan["baseline_head"] == "a1175449f34d39ff933d9d8ab23ced1f32b290ec",
         "descent parent is not the pinned PR200 head")
    plan_without_digest = dict(plan)
    plan_digest = plan_without_digest.pop("plan_sha256")
    canonical_plan = json.dumps(plan_without_digest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    need(hashlib.sha256(canonical_plan).hexdigest() == plan_digest, "frame-descent plan digest")
    complex_certificate = read(ROOT / "research/source-assisted-v4/certificate.json")
    profile_bytes = json.dumps(complex_certificate["complex_profile"], sort_keys=True,
                               separators=(",", ":")).encode("utf-8")
    need(hashlib.sha256(profile_bytes).hexdigest() == plan["complex_profile_sha256"],
         "the pinned source-assisted complex profile changed")

    word = Candidate()
    word.exact_frames()
    before = word.row()
    before_internal = Counter({int(k): v for k, v in before["physical_internal_histogram"].items()})
    selection = read(UPSTREAM / "selected/bit/sinks.json")
    selected = apply_plan(word, plan, selection)
    word.exact_frames()
    after = word.row()
    after_internal = Counter({int(k): v for k, v in after["physical_internal_histogram"].items()})
    delta = after_internal.copy()
    delta.subtract(before_internal)
    delta = Counter({rank: count for rank, count in delta.items() if count})
    expected_delta = Counter({int(k): int(v) for k, v in plan["physical_internal_delta"].items() if int(v)})
    need(delta == expected_delta, "exact physical-chain rank histogram delta")
    need(after["changed_operation_frames"] == plan["changed_operation_frames"],
         "total changed operation-frame count")
    need(after["changed_operation_frames"] == before["changed_operation_frames"] + len(selected),
         "descent changed-frame accounting")

    # The bit word and algebra are unchanged; replay the complete source, target and dirty columns.
    formal = [word.formal(ring) for ring in (2, 0)]
    need(all(row["all_outputs"] and row["all_sources_and_dirty_restored"] for row in formal),
         "complete F2 and integer defining-decoder replay")
    terminal = prove_terminal(word, selection)
    terminal.pop("seconds", None)
    terminal.pop("maxrss", None)
    profile = terminal["profile"]
    coarse = certify(profile)
    need(str(coarse["coarse_saving"]) == plan["candidate_bit_coarse"],
         "exact paid moment differs from the descent receipt")
    need(terminal["profile"]["terminal_sinks"] == plan["terminal_sink_count"],
         "terminal sink count changed")

    pr184 = load_module("pr184_assemble_profiles", ROOT / "research/source-assisted/global/assemble_profiles.py")
    pricing = load_module("pr185_leaf_wrapper", ROOT / "research/source-assisted-v4/assemble.py")
    baseline_profile = read(UPSTREAM / "certificate.json")["bit"]["profile"]
    complex_row = pr184.select(pr184.normalize(complex_certificate["complex_profile"]))
    baseline_bit = pr184.select(pr184.normalize(baseline_profile), True)
    candidate_bit = pr184.select(pr184.normalize(profile), True)
    baseline_bit, _ = pricing.bootstrap_bit_leaf(baseline_bit)
    candidate_bit, bootstrap = pricing.bootstrap_bit_leaf(candidate_bit)
    bridge = ROOT / "research/source-assisted/global/FINITE_BRIDGE.txt"
    baseline_assembly = pr184.assemble(complex_row, baseline_bit, ROOT, bridge)
    candidate_assembly = pr184.assemble(complex_row, candidate_bit, ROOT, bridge)
    need(str(baseline_assembly["kappa"]) == plan["baseline_kappa"],
         "the pinned PR200 baseline assembly changed")
    need(str(candidate_assembly["kappa"]) == plan["candidate_kappa"],
         "exact composed kappa differs from the search receipt")
    need(candidate_assembly["kappa"] > baseline_assembly["kappa"],
         "frame descent did not improve the exact composed exponent")

    primes = prime_certificate(word)
    prime_path = OUT / "frame-prime-witnesses.json.gz"
    prime_bytes = gzip.compress((json.dumps(primes, sort_keys=True, separators=(",", ":")) + "\n").encode(),
                                mtime=0)
    prime_summary = {key: value for key, value in primes.items() if key != "frame_witnesses"}
    prime_summary.update(witness_file=prime_path.name, witness_sha256=hashlib.sha256(prime_bytes).hexdigest())
    certificate = dict(
        status="PASS exact physical frame descent and conditional bit profile",
        upstream_head=plan["baseline_head"],
        source_pins=pins,
        frame_descent_sha256=digest(OUT / "frame-descent.json"),
        bit=dict(profile=profile, coarse=coarse, terminal=terminal,
                 formal=formal, prime_witnesses=prime_summary,
                 foreign_producer_replays=0),
        exact_composition=dict(
            complex_saving=str(complex_row["saving"]),
            baseline_kappa=str(baseline_assembly["kappa"]),
            candidate_kappa=str(candidate_assembly["kappa"]),
            gain_over_pr200=str(candidate_assembly["kappa"] - baseline_assembly["kappa"]),
            gain_over_pr199=str(candidate_assembly["kappa"] - pr184.Q("1693287/2500000000")),
            bit_leaf_bootstrap=bootstrap,
            assembly_constraints=len(candidate_assembly["assembly"]["constraints"]),
            assembly_margins=len(candidate_assembly["assembly"]["margins"])),
        physical=dict(
            base_internal_histogram={str(k): v for k, v in sorted(before_internal.items())},
            candidate_internal_histogram={str(k): v for k, v in sorted(after_internal.items())},
            internal_histogram_delta={str(k): v for k, v in sorted(delta.items())},
            selected_operation_count=len(selected),
            changed_operation_frames=after["changed_operation_frames"],
            reused_registers=after["reused_registers"],
            terminal_sinks=profile["terminal_sinks"],
            endpoint_geometry="each selected frame is the join of its actual physical predecessors and value span, contained in both physical successors"),
        scope="Conditional finite witness; PR200 analytic/compiler interfaces, PR184 pricing and finite bridge, and PR185/PR199 finite ordinary-leaf wrapper remain proof dependencies.")
    return certificate, prime_bytes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Authoring mode: write exact certificate outputs")
    args = parser.parse_args()
    certificate, prime_bytes = build()
    cert_path = OUT / "certificate.json"
    prime_path = OUT / "frame-prime-witnesses.json.gz"
    if args.write:
        cert_path.write_text(json.dumps(js(certificate), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        prime_path.write_bytes(prime_bytes)
    else:
        need(json.loads(cert_path.read_text(encoding="utf-8")) == js(certificate),
             "canonical frame-descent certificate does not reproduce")
        need(prime_path.read_bytes() == prime_bytes, "canonical frame-prime witnesses do not reproduce")
    print(json.dumps({
        "status": certificate["status"],
        "kappa": certificate["exact_composition"]["candidate_kappa"],
        "gain_over_pr199": certificate["exact_composition"]["gain_over_pr199"],
        "selected_operations": certificate["physical"]["selected_operation_count"],
        "changed_operation_frames": certificate["physical"]["changed_operation_frames"],
        "coarse_bit_saving": str(certificate["bit"]["coarse"]["coarse_saving"]),
        "prime_witness_sha256": certificate["bit"]["prime_witnesses"]["witness_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
