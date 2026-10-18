#!/usr/bin/env python3
"""Adversarial controls for the exact hypotheses and the public replay."""

from fractions import Fraction as F
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model
import odd_flags
from source import authenticate
from verify import rank

HERE = Path(__file__).resolve().parent


def rejected(function, message):
    try:
        function()
    except ValueError as exc:
        model.need(message in str(exc), "wrong rejection: " + str(exc))
        return
    raise ValueError("invalid control accepted: " + message)


def run():
    authenticate()
    t = (1, 1)
    rejected(lambda: model.check_fitting(6, [t], [[0]]), "nonzero")
    # Repeated physical ports cannot be deduplicated: the all-ones matrix has
    # rank one, but the two distinct positions require zero cross coefficients.
    rejected(lambda: model.check_fitting(6, [t, t], [[1, 1], [1, 1]]), "forbidden")
    model.check_fitting(6, [t, t], [[1, 0], [0, 1]])
    rejected(lambda: model.weighted_bound(6, {t: -1}), "nonnegative")
    model.need(model.dot(3, 5) == 1, "even-type control has a valid diagonal pairing")
    rejected(lambda: model.weighted_bound(6, {(3, 5): 1}), "inadmissible")
    chosen = list(model.selector(6)[0])
    bad = next(x for x in model.types(6) if x not in chosen and
               any(not model.dot(w, x[0]) for _, w in chosen[:-1]))
    rejected(lambda: model.check_selector(6, chosen[:-1] + [bad]), "not triangular")
    # Omitting the h5 exceptional type loses its entire orbit. One cannot keep
    # the 1/9 bound merely from the other three orbit fractions.
    truncated = set(model.selector(5)[0][:-1])
    smallest = min(F(len(truncated.intersection(o)), len(o)) for o in model.orbit_partition(5))
    model.need(smallest == 0, "missing exceptional-orbit control")
    # Identity is essential to the trace corollary. Two scalar idempotents
    # sum to D=[2], not I=[1]; normalizing D makes both terms non-idempotent.
    x1 = x2 = F(1)
    diagonal = x1 + x2
    model.need(x1*x1 == x1 and x2*x2 == x2 and diagonal != 1,
               "nonidentity diagonal fixture")
    normalized = x1 / diagonal
    model.need(normalized*normalized != normalized, "normalization lost idempotency")
    # A zero-charge rectangle contributes zero to B .* N and may be removed.
    ports = [(1, 1), (2, 2)]
    with_free = [[1, 7], [0, 1]]
    without_free = [[1, 0], [0, 1]]
    model.check_fitting(6, ports, with_free)
    model.check_fitting(6, ports, without_free)
    model.need(all(model.dot(ports[i][1], ports[j][0]) * with_free[i][j]
                   == without_free[i][j] for i in range(2) for j in range(2)),
               "zero-charge removal changed the endpoint")
    # The two valid flags need their exact rational mixture, not equal weights.
    rejected(lambda: odd_flags.check_mixture(5, F(1, 2)), "does not balance")
    low, _, _ = odd_flags.selector(5, "low")
    rejected(lambda: odd_flags.check_selector(5, "high", low), "wrong flag orbit counts")
    rejected(lambda: odd_flags.check_selector(5, "low", tuple((w, q) for q, w in low)),
             "not triangular")
    # Lift the binary bit 1+<x,y>, not the integer expression 1+<x,y>.
    j = 31
    (e, f), _ = odd_flags.symplectic_pairs(5)
    mask_ports = [(j ^ e, j), (j, j ^ f)]
    model.check_fitting(5, mask_ports, [[1, 0], [1, 1]])
    model.need(model.dot(e, f) == 1 and model.dot(mask_ports[1][1], mask_ports[0][0]) == 0,
               "symplectic-to-binary mask fixture")
    model.need(1 + model.dot(e, f) == 2, "integer-lift mutant differs from the binary bit")
    # Exact rank addition must work even when the remaining core is singular.
    peel_ports = [(j, j)]*2 + [(j ^ e, j)]*2 + [(j, j ^ f)]*2 + [(j ^ e, j ^ e), (j ^ f, j ^ f)]
    peel_matrix = [[int(i == h) if model.dot(w, q) else (2*i + 3*h) % 5 - 2
                    for h, (q, _) in enumerate(peel_ports)] for i, (_, w) in enumerate(peel_ports)]
    for i in (6, 7):
        for h in (6, 7):
            peel_matrix[i][h] = 1
    for i in range(6):
        peel_matrix[i][i] = -1 if i % 2 else 1
    model.check_fitting(5, peel_ports, peel_matrix)
    for prime in (None, 2, 3, 5, 7):
        model.need(rank(peel_matrix, prime) == 7, "exact peeling rank with a singular core")
    # Exercise the real optimized CLI's source gate, not just an in-memory predicate.
    with tempfile.TemporaryDirectory(prefix="odd-unit-controls-") as folder:
        corrupt = Path(folder) / "source.tar"
        raw = bytearray((HERE / "inputs/small-unit-source.tar").read_bytes())
        raw[len(raw)//2] ^= 1
        corrupt.write_bytes(raw)
        for script in ("verify.py", "odd_flags.py"):
            proc = subprocess.run([sys.executable, "-I", "-O", "-Werror", "-B",
                                   str(HERE / script), "--source-archive", str(corrupt)],
                                  capture_output=True, text=True, timeout=30)
            model.need(proc.returncode != 0 and "comparison archive SHA256 mismatch" in proc.stderr,
                       "optimized CLI accepted changed comparison source: " + script)
    return {"status": "PASS_ODD_UNIT_RANK_CONTROLS", "controls": 14,
            "scope": "Baseline plus flag-mixture, orientation, binary-lift and exact special-port rank boundaries."}


if __name__ == "__main__":
    model.need(len(sys.argv) == 1, "unknown control arguments")
    print(json.dumps(run(), sort_keys=True))
