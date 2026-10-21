#!/usr/bin/env python3
"""Source-bound logarithmic template at PR4416's unchanged conditional kappa.

All 41 dependency files are authenticated before the original complete
verifier runs. The new potential and finite rank use rational arithmetic.
The finite native/tensor/compiled words and inherited analytic premises
remain written proof obligations; this is not a formal theorem prover.

Apache-2.0. Native sources: PR4359 and PR4416; integer flow: PR4268;
outer parameter ledger: PR4405. See PROOF.md for scope and attribution.
"""
from fractions import Fraction as Q
from functools import cache
from hashlib import sha1, sha256
from pathlib import Path, PurePosixPath
import argparse
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_REPOSITORY = "1337isnot1337/integer-mult-bounds"
SOURCE_COMMIT = "e9058860b5c850760fdf970e796a96aefcdb1d98"
SOURCE_PACKAGE = "research/pr4359-p7-padding"
SCHEMA = "pr4416-strict-logarithmic-uniform-template/1"
LOG_TERMS = 128
RECEIPT_BITS = 256
TESTED = Q("0.00268648")
UNIFORM = Q(376107, 140000000)
KAPPA = Q("0.00268647")

# Immutable original Git blobs, byte lengths and SHA-256 digests at SOURCE_COMMIT.
SOURCES = {
    "research/pr4359-p7-padding/ENDPOINT.md": {
        "bytes": 7791,
        "git_blob": "8667482f630867090a57e9c870925cd411b71838",
        "sha256": "e7056020bb9757d45fdf1a8eea9e811040ce72d53bc16e7f90f72a5e712fa3e9"
    },
    "research/pr4359-p7-padding/EXPORTED-SOURCES.json": {
        "bytes": 10730,
        "git_blob": "439a06e9bcbf44fc7b1e95ae2e005e0c21d0c15b",
        "sha256": "0305d4730e2dfede834a241099aa6ceeee29444f305dfeb25ae9a1bb8b2df0b6"
    },
    "research/pr4359-p7-padding/FOLLOWUP.json": {
        "bytes": 135263,
        "git_blob": "0ef5700a7020b43d94adb2e1b227553ba80695ea",
        "sha256": "385ce4c0c03fec4089ff51013cc03b63fab0a8c2ebe01e24a08c28f0483eac41"
    },
    "research/pr4359-p7-padding/FOLLOWUP.md": {
        "bytes": 1807,
        "git_blob": "60e4ae9c816ac958d1c7dc359197c7694fe047ba",
        "sha256": "3c33135d6ed23cacd631c3111406f9d32c70cfbab731842aa549b7e2a888b5df"
    },
    "research/pr4359-p7-padding/NATIVE.md": {
        "bytes": 8718,
        "git_blob": "394d9a03c165336d1cfbcd41921c93741042393b",
        "sha256": "26bf9312cdb496b1113c9ddd8aa0fa922ed9e480005703212942af358394183d"
    },
    "research/pr4359-p7-padding/P7-FACTOR.json": {
        "bytes": 65844,
        "git_blob": "04c7ef620e760cc8f1764bbf0ccd7f32c6a5bd86",
        "sha256": "6f96f6be5d8441f71cbe6ebb1657c69b543eb085b848b92b591b7ac01d6e6598"
    },
    "research/pr4359-p7-padding/README.md": {
        "bytes": 5247,
        "git_blob": "0edbc3a10124b99d7de14fef256183168223a37b",
        "sha256": "4066815a754406ea03951b6d5afcd3a1d659d9935be015c4e2c97e32ac61bfed"
    },
    "research/pr4359-p7-padding/RESULT.json": {
        "bytes": 14055,
        "git_blob": "ebb30a9b3b94fb159a316350f7da57bde4a30c25",
        "sha256": "9b814be97e3b45fcc28eafa8a65694897a7387f71a14d44796c6aadf303d7fab"
    },
    "research/pr4359-p7-padding/SOURCES.json": {
        "bytes": 584,
        "git_blob": "fcfba8aa31e2b15be7abeb2191c9e35fa0d7919b",
        "sha256": "49fb3e2b5f8909ccb5edc2f2193aeacdc88bf8d1c63b2b1d25f2dd008f39ed93"
    },
    "research/pr4359-p7-padding/TASK.json": {
        "bytes": 6355,
        "git_blob": "b02a5ae81b2c48cfa234c70ad7241a4508359c74",
        "sha256": "ad84da8be3e5e85cfb5cb29107812396d20ac1c66d445fb93d431e1436147c56"
    },
    "research/pr4359-p7-padding/TENSOR.md": {
        "bytes": 10388,
        "git_blob": "8ecfd3e4d0bcb449ecb1e150c4f1f4fbb39ca656",
        "sha256": "b2eba86cb979b4dc2a045f2e74bbd29e4d9e5ec87d6a2bc23ba7b54f1f58e3e3"
    },
    "research/pr4359-p7-padding/VERIFY.json": {
        "bytes": 883,
        "git_blob": "b00ce132dabebe0ad1aa09c626a7312032a57bb6",
        "sha256": "ca2d2aabfcb6a199f577621e4e45d0da8f1aa664684e4cd1b2f4535663102870"
    },
    "research/pr4359-p7-padding/dependencies/compiler-refill/endpoint.py": {
        "bytes": 11603,
        "git_blob": "340e1f0ffb8a1a9c38fbbd9119580b6d23e01b59",
        "sha256": "d097e55f06c3f244f2074ffd7c1a0a5f3c4b4b6a6accf9619d1dde5c0ae85e15"
    },
    "research/pr4359-p7-padding/dependencies/compiler-refill/template_bound.py": {
        "bytes": 6511,
        "git_blob": "ddc852c4fa2bb0739af01cdac6dd65e0c049f756",
        "sha256": "25d409726cd867f7584fbd52e1b846335debdab42d24377e00c5653aaf12c0fb"
    },
    "research/pr4359-p7-padding/dependencies/tensor-strictification/native_inventory.py": {
        "bytes": 10249,
        "git_blob": "417fefe5fb13e695bb5c551ac98be422b93b0258",
        "sha256": "e1ba009d546981e75f0e6468723b9af4c065f5eb6e08390084fbbf9a579cedf1"
    },
    "research/pr4359-p7-padding/endpoint.py": {
        "bytes": 6742,
        "git_blob": "32d24821b04e8250f1191b85d14dd973e2772c16",
        "sha256": "94a5c600184e23e50d9ae8d8001a25164bd3279c4cefac4c15bbf8f6995624a4"
    },
    "research/pr4359-p7-padding/factor_receipt.py": {
        "bytes": 2897,
        "git_blob": "e17133b81e28bb133122526cd285418f8660bdeb",
        "sha256": "422a4cf41df758f996ac2abd343932daee3ac34609b92516d262f4479ffdc7a3"
    },
    "research/pr4359-p7-padding/native_inventory.py": {
        "bytes": 15510,
        "git_blob": "8d2d96e3998254c2333c43fe47cdfd074cbd811e",
        "sha256": "65539acaf45bdfe8c5aee6830f9c9b3d1107c442a60842ef803fdd7688de8f32"
    },
    "research/pr4359-p7-padding/scan.py": {
        "bytes": 5366,
        "git_blob": "bae64f0b669f69683ddc3e7660245bd7f7db8540",
        "sha256": "30caf3b8d64862ba32c3b708b52c88db10ff1eeb4f68f1624f2ff488869b6cdc"
    },
    "research/pr4359-p7-padding/source/research/kappa-0023-productive-jobs/dependencies/kappa-next-regime/bit-compression/carrier-reuse/reference/joint_pair_dag.py": {
        "bytes": 29992,
        "git_blob": "8b40135a84e7f0f0cd44bed69655801310b916a7",
        "sha256": "8a0de761642d21919e969475c3f13e5d01a4bae7343c1e1f37c586d94b676a85"
    },
    "research/pr4359-p7-padding/source/research/kappa-0023-productive-jobs/dependencies/kappa-next-regime/direct-decoder/sources/DATA-PHASES.json": {
        "bytes": 814141,
        "git_blob": "d9a4f84211182ca200c081ea061d724c8a2cfb70",
        "sha256": "c5916ff312678f12aba403847643fbbc29f643acec60bdf836fa56cd3e8251fa"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/architecture/FINITE-PRECOMPILATION.md": {
        "bytes": 15898,
        "git_blob": "4badb40f0919c515823cb07e44c6470d4d6469ca",
        "sha256": "4cb32f6b8e388ecf6ed41b5bbdeeb4539cb40c8424f194974afea58f7e0921e8"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/architecture/identity_mixed_certificate.py": {
        "bytes": 7318,
        "git_blob": "f4b51b358eff3cc43ea200503d16e7b75f67c7bc",
        "sha256": "e1795294fa4d3100352bfda787ecb1efc2468ff11cbcbaca2476eb642b8d2a0a"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/architecture/mixed_forest_search.py": {
        "bytes": 16190,
        "git_blob": "9b5213bf3f164664a36f81592740801f79b3c97d",
        "sha256": "2dcec76840b437c67125af5b6d3529577f8c38851c792d0ffd9fa928c473e23b"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/architecture/mixed_target_probe.py": {
        "bytes": 12298,
        "git_blob": "4fc05ab08138218ba9f09e5c89b649afae7c914e",
        "sha256": "011c3c9d0cf81103dc84d709a0e36793eb7c5ae3f23c85eac27650ef13afa04a"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/bit/BIT-ALLSIZE-PARAMETERS.json": {
        "bytes": 4138,
        "git_blob": "fbe6da7241357d89cf5c55b2e7ce2d0d046be32a",
        "sha256": "edb273f59a27356ad89f38791590c3c806b228c3510eb508e01e89f2caba95ef"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/bit/complex_controller_factor.py": {
        "bytes": 12901,
        "git_blob": "cb0cff7c8be5f38f2ee52201d9d0907f9dfd7947",
        "sha256": "1de9aaf918e6a4f2f5448754c1f3c3da3b85e6257849ebd097af09859c4e5497"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/bit/mixed_productive_bit.py": {
        "bytes": 28173,
        "git_blob": "9c7a8bd5d3ae4c19952648c815031858d6627b96",
        "sha256": "b32291b0db7fc0d332ec444c70746ab0fb03351d2e50546f8bcb64060e3ff95e"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/complex/fresh-certificates/THREE-base-HELPER-BOUNDARIES.json.gz": {
        "bytes": 25720,
        "git_blob": "1dae5193bad6e7467eb13434fd1a2e971f2a4cba",
        "sha256": "f90517e395bde58c72cacd5d3481c4ea31d459fe4535384ac16547ac40460555"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/complex/full-identity-certificates/RESULT.json": {
        "bytes": 75462,
        "git_blob": "c6edcbdc43bf36bb11201235027d0ec170d07fc8",
        "sha256": "943d5fad2fc529f470df05a35446e07ecaef7344abfce450d2c2eb2c9b3798f6"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-CANONICAL.json.gz": {
        "bytes": 82793,
        "git_blob": "4a8c4ed26e53a72362d571c972e65aff546be784",
        "sha256": "6418ec3da24d548a57f5c3fe5b9062c26c9478e638504a61c387f5cfb5f4ed61"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/complex/full-identity-certificates/THREE-base-FULL-IDENTITY-NATIVE.json.gz": {
        "bytes": 198063,
        "git_blob": "b46d44c6ee624968dd57be928b0c15d9d45f3b2c",
        "sha256": "c54b0a3e129d28e6dbf74fa731fc3bb70fe3c6705f07256750fbecddcc842d39"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/complex/full_identity_rebuild.py": {
        "bytes": 9996,
        "git_blob": "7cff9bff0f61e9b387ade5128dfeab9265efe6d9",
        "sha256": "9af2ffbb0038c92e2a7d281081b0daaeadce75b11b566e5427845dc1af91e33d"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/controller/P3-NATIVE-COVER.json.gz": {
        "bytes": 176694,
        "git_blob": "51a09b3952a491f06780bf6ce5f69b385f026b21",
        "sha256": "facfc6d6ecde151afb7e6a167776f3fdaac1c816e785a21a39f7f0bfd9140f3f"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/controller/p3_native_cover.py": {
        "bytes": 16380,
        "git_blob": "8756693610a8dc8352629d8270cb4c6aed087cb8",
        "sha256": "fae71fcbbd20b9ee73b049cf6f43ea1d048217fb15feb6055a007e47da3363fe"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/transfer-audit/FINITE-TEMPLATE-CLOSURE.md": {
        "bytes": 15369,
        "git_blob": "9917ac5543608047fd368e5e75f0851310f53584",
        "sha256": "3f8508c63862dd83968bd30df91b08ba5afcee1e10db15ca546cdff0caef95d9"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/transfer-audit/OUTER-TRANSFER-AUDIT.md": {
        "bytes": 20800,
        "git_blob": "e8b7ef8956ece5bd493cbf52113916e5dc288535",
        "sha256": "67569961d068633c6ff3ac9dfde47a0c17f0da6d20432799dcc920cff92b5779"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/transfer-audit/p3_cover_audit.py": {
        "bytes": 10467,
        "git_blob": "d9b44b662a3cfdbc634222590acd9098eb92b9df",
        "sha256": "a0fe9a26f77556e83b31b0c91fea909d6f3d8209d0f9f7ad4e5bc1375d33615e"
    },
    "research/pr4359-p7-padding/source/research/kappa-rebuild/transfer-audit/p3_native_audit.py": {
        "bytes": 14209,
        "git_blob": "0f3a4067a4b4e20d0e6ca0f84f41851c5168f76d",
        "sha256": "5504a55a50546418d10c522984438cdeedb44993f7c1dab7bd4aa1ae0515d902"
    },
    "research/pr4359-p7-padding/strictification.py": {
        "bytes": 7129,
        "git_blob": "a96c9855352a6252430aee4287112c47148c4ff7",
        "sha256": "1f3c2a38b34d9dad7266be212ca5d0225827d8e05bda4831e6c25c5713f624f0"
    },
    "research/pr4359-p7-padding/verify.py": {
        "bytes": 4930,
        "git_blob": "e491e49d5a585526e88165f67891e9d61ba35154",
        "sha256": "e305bf8962e7e803e39993929bb7f057903a4e0fcec8c06b4a6d160736532161"
    }
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def encode(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(item) for item in value]
    return value


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "Python source loader")
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


def source_path(root, relative):
    rel = PurePosixPath(relative)
    require(not rel.is_absolute() and ".." not in rel.parts and str(rel) == relative,
            "canonical dependency path")
    path = root
    for part in rel.parts:
        path /= part
        require(not path.is_symlink(), "no aliased dependency path")
    return path


def authenticate_bytes(data, expected, label):
    require(len(data) == expected["bytes"], "source byte length: " + label)
    require(sha256(data).hexdigest() == expected["sha256"], "source SHA-256: " + label)
    blob = sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    require(blob == expected["git_blob"], "original Git blob: " + label)


def authenticated_source(source_root):
    """Return the normalized complete source replay after authentication.

    No caller-supplied receipt can replace source execution. All source
    scripts, written proofs, manifests, compressed artifacts and saved
    receipts at the pinned PR head are checked before the first import.
    """
    source_root = Path(source_root).resolve()
    require(len(SOURCES) == 41, "complete pinned PR4416 file inventory")
    for relative, expected in SOURCES.items():
        require(relative.startswith(SOURCE_PACKAGE + "/"), "pinned package scope")
        path = source_path(source_root, relative)
        authenticate_bytes(path.read_bytes(), expected, relative)
    package = source_root / SOURCE_PACKAGE
    upstream = module("pr4416_complete_authenticated_verifier", package / "verify.py")
    replay = json.loads(json.dumps(upstream.verify(), sort_keys=True))
    require(replay == json.loads((package / "RESULT.json").read_text()),
            "exact full native, tensor, compiler and outer source replay")
    require(replay["status"] == "PASS_SOURCE_BOUND_CONDITIONAL_P7_PAID_PADDING_IMPROVEMENT",
            "expected source status")
    return replay


def _reduced_log(y, terms):
    """Positive atanh series with an exact geometric remainder upper bound."""
    require(isinstance(y, Q) and 1 <= y <= 2 and type(terms) is int and terms >= 1,
            "reduced logarithm arguments")
    z = (y - 1) / (y + 1)
    z2, power, total = z * z, z, Q(0)
    for j in range(terms):
        total += 2 * power / (2 * j + 1)
        power *= z2
    remainder = 2 * power / ((2 * terms + 1) * (1 - z2))
    return total, total + remainder


@cache
def log_interval(x, terms=LOG_TERMS):
    """Directed natural-log interval for a positive rational argument."""
    require(isinstance(x, Q) and x > 0 and type(terms) is int and terms >= 1,
            "positive rational logarithm argument")
    y, k = x, 0
    while y >= 2:
        y /= 2
        k += 1
    while y < 1:
        y *= 2
        k -= 1
    low, high = _reduced_log(y, terms)
    two_low, two_high = _reduced_log(Q(2), terms)
    if k >= 0:
        return low + k * two_low, high + k * two_high
    return low + k * two_high, high + k * two_low


def outward(pair, bits=RECEIPT_BITS):
    """Short dyadic receipt endpoints enclosing the full exact interval."""
    low, high = pair
    require(low <= high and type(bits) is int and bits >= 1, "ordered receipt interval")
    scale = 1 << bits
    low_scaled, high_scaled = low * scale, high * scale
    low_integer = low_scaled.numerator // low_scaled.denominator
    high_integer = -((-high_scaled.numerator) // high_scaled.denominator)
    result = Q(low_integer, scale), Q(high_integer, scale)
    require(result[0] <= low <= high <= result[1], "outward receipt rounding")
    return result


def rank_candidate(tested, uniform, binary_bound, gamma, j):
    require(isinstance(tested, Q) and isinstance(uniform, Q) and 0 < uniform < tested < 1,
            "strict tested-to-uniform saving gap")
    require(type(binary_bound) is int and binary_bound >= 2
            and type(gamma) is int and gamma >= 1 and type(j) is int and j >= 1,
            "positive integer rank-selection constants")
    threshold = (binary_bound * tested + gamma * j) / (tested - uniform)
    return max(binary_bound, 2, 2 ** (j - 1),
               threshold.numerator // threshold.denominator + 1)


def choose_rank(tested, uniform, binary_bound, gamma):
    """Unbounded J search; exponential growth dominates the affine threshold."""
    j = 1
    while True:
        h = rank_candidate(tested, uniform, binary_bound, gamma, j)
        if h < 2 ** j:
            return h, j
        j += 1


def derive_template(m_base, target_floor_base, cutoff_base, tensor_power,
                    tested_saving, uniform_saving, theta):
    """Certify a sufficient logarithmic template for a supplied strict rule.

    This utility verifies only the rank/potential interface. Its caller
    must establish the complete mixed moment and native rule semantics.
    Bounds refer to m=m_base^v, q=target_floor_base^v and r_max<=cutoff_base^v.
    """
    require(all(type(value) is int for value in
                (m_base, target_floor_base, cutoff_base, tensor_power)),
            "integral bases and tensor power")
    require(1 <= cutoff_base < target_floor_base <= m_base and tensor_power >= 1,
            "strict paid-target separation and ambient containment")
    require(isinstance(tested_saving, Q) and isinstance(uniform_saving, Q)
            and 0 < uniform_saving < tested_saving < 1,
            "fixed strict rational savings")
    require(isinstance(theta, Q) and 0 < theta < 1,
            "strict rational exit exponent")
    require(cutoff_base ** theta.denominator < target_floor_base ** theta.numerator,
            "exact paid-cutoff versus target-floor exit comparison")
    t = 1 - tested_saving
    log_base = log_interval(Q(m_base))
    log_t = log_interval(t)
    log_reciprocal_theta = log_interval(1 / theta)
    require(theta * tensor_power * log_base[0] > 1,
            "small-exit safeguard theta*log(m)>1")
    require(log_reciprocal_theta[0] > 0, "positive logarithmic contraction")
    debt = (tested_saving * tensor_power * log_base[0] - log_t[1],
            tested_saving * tensor_power * log_base[1] - log_t[0])
    ratio = debt[1] / log_reciprocal_theta[0]
    gamma = max(1, ratio.numerator // ratio.denominator + 1)
    potential_gap = (gamma * log_reciprocal_theta[0] - debt[1],
                     gamma * log_reciprocal_theta[1] - debt[0])
    require(potential_gap[0] > 0, "theta^gamma < t*m^(t-1)")
    ambient = m_base ** tensor_power
    binary_bound = ambient.bit_length()
    require(2 ** (binary_bound - 1) <= ambient < 2 ** binary_bound,
            "exact binary ambient bound")
    h, j = choose_rank(tested_saving, uniform_saving, binary_bound, gamma)
    final_gap = h * (tested_saving - uniform_saving) - binary_bound * tested_saving - gamma * j
    require(h >= max(binary_bound, 2) and h < 2 ** j and final_gap > 0,
            "strict sufficient uniform-rank bound")
    return {
        "m_base": m_base, "target_floor_base": target_floor_base,
        "cutoff_base": cutoff_base, "tensor_power": tensor_power,
        "m_encoding": str(m_base) + "^" + str(tensor_power),
        "q_encoding": str(target_floor_base) + "^" + str(tensor_power),
        "paid_max_bound_encoding": str(cutoff_base) + "^" + str(tensor_power),
        "tested_saving": tested_saving, "uniform_saving": uniform_saving,
        "t": t, "theta": theta, "gamma": gamma,
        "logarithm_terms": LOG_TERMS, "receipt_interval_bits": RECEIPT_BITS,
        "log_m_base_interval": outward(log_base),
        "log_t_interval": outward(log_t),
        "log_reciprocal_theta_interval": outward(log_reciprocal_theta),
        "negative_log_eta_interval": outward(debt),
        "potential_log_gap_interval": outward(potential_gap),
        "binary_ambient_bound": binary_bound, "H": h, "J": j,
        "N_encoding": "2^" + str(h), "strict_uniform_gap": tested_saving - uniform_saving,
        "final_strict_power_gap": final_gap,
        "materialized_tensor_or_uniform_word": False,
    }


def must_reject(action, label):
    try:
        action()
    except AssertionError:
        return True
    raise AssertionError("negative control did not reject: " + label)


def build(source_root):
    replay = authenticated_source(source_root)
    strict, endpoint = replay["strictification"], replay["endpoint"]
    native = strict["native_inventory"]
    require(strict["strict_moment_verified"] and
            Q(strict["strictification_gap_rational"]) == Q(13937, 10240638976),
            "complete paid tensor, splitting and completion gap")
    require((strict["exponent"], strict["cutoff_base"], strict["target_floor_base"])
            == (6240, 10, 11), "unchanged certified tensor recipe")
    require(Q(strict["tested_saving"]) == TESTED and Q(endpoint["kappa"]) == KAPPA,
            "unchanged tested saving and final conditional kappa")
    outer = endpoint["outer"]
    require(Q(outer["parameters"]["complex_uniform_saving"]) == UNIFORM,
            "uniform saving binds to the complete outer ledger")
    require(Q(outer["parameters"]["bit_saving"]) == Q("0.0027"),
            "unchanged ordinary BIT saving")
    require((len(outer["margins"]), len(outer["strict_checks"]),
             len(outer["functional_checks"])) == (9, 54, 3),
            "all current outer rows and guards")
    require(all(Q(value) > 0 for name in ("strict_checks", "functional_checks")
                for value in outer[name].values()), "all current strict and functional guards")
    minimum_outer_margin = min(Q(value) - KAPPA for value in outer["margins"].values())
    require(minimum_outer_margin == Q(524529867, 122500000000000000) > 0,
            "unchanged positive minimum outer cost margin")
    template = derive_template(121, 11, 10, 6240, TESTED, UNIFORM, Q(25, 26))
    h, j, b, gamma = (template[name] for name in ("H", "J", "binary_ambient_bound", "gamma"))
    require((h, j, b, gamma) == (66091190261265, 46, 43174, 2050),
            "specified new sufficient template")
    require(template["final_strict_power_gap"] == Q(1, 700000000),
            "exact new strict power margin")
    old_h = endpoint["compiler"]["H1"]
    require(old_h == 16201843136005340321 and h < old_h,
            "strict improvement over the replayed source rank")

    # A separated upper interval makes the preceding gamma a genuine failure
    # of this potential comparison, rather than an interval-resolution issue.
    ell = log_interval(Q(26, 25))
    log_m, log_t = log_interval(Q(121)), log_interval(1 - TESTED)
    debt_low = TESTED * 6240 * log_m[0] - log_t[1]
    prior_gamma_upper = (gamma - 1) * ell[1] - debt_low
    require(prior_gamma_upper < 0, "one lower gamma fails the actual log comparison")
    require(Q(template["potential_log_gap_interval"][0]) > Q("0.00488866717"),
            "reported lower potential margin")
    require((h - 1) * (TESTED - UNIFORM) <= b * TESTED + gamma * j,
            "one lower H fails the strict sufficient rank inequality")
    require(rank_candidate(TESTED, UNIFORM, b, gamma, j - 1) >= 2 ** (j - 1),
            "preceding logarithmic bin is insufficient")
    sample_path = SOURCE_PACKAGE + "/TENSOR.md"
    sample = source_path(Path(source_root).resolve(), sample_path).read_bytes()
    corrupted = bytes([sample[0] ^ 1]) + sample[1:]
    controls = {
        "one_lower_gamma_rejected": prior_gamma_upper < 0,
        "one_lower_gamma_log_gap_upper": outward((prior_gamma_upper, prior_gamma_upper))[1],
        "one_lower_H_rejected": True,
        "preceding_logarithmic_bin_rejected": True,
        "closed_uniform_gap_rejected": must_reject(
            lambda: derive_template(121, 11, 10, 6240, TESTED, TESTED, Q(25, 26)),
            "closed uniform gap"),
        "equal_paid_target_bases_rejected": must_reject(
            lambda: derive_template(121, 10, 10, 6240, TESTED, UNIFORM, Q(25, 26)),
            "equal paid and target bases"),
        "too_small_exit_exponent_rejected": must_reject(
            lambda: derive_template(121, 11, 10, 6240, TESTED, UNIFORM, Q(24, 25)),
            "too small exit exponent"),
        "small_exit_log_guard_rejected": must_reject(
            lambda: derive_template(2, 2, 1, 1, Q(1, 2), Q(1, 4), Q(3, 4)),
            "missing small-exit logarithm safeguard"),
        "changed_source_bytes_rejected": must_reject(
            lambda: authenticate_bytes(corrupted, SOURCES[sample_path], sample_path),
            "changed pinned source bytes"),
    }
    require(native["native_scalar_allowance"] == 2490856 and native["dimension"] == 121,
            "native source for fresh full-word constants")
    raw_targets = {int(k): value for k, value in native["targets"].items()}
    raw_paid = {int(k): value for k, value in native["paid"].items()}
    obstruction_n = native["dimension"] * min(raw_targets)
    require(obstruction_n == 605 and raw_targets[5] == 420 and raw_paid[8] > 0,
            "actual raw rank-five root point and rank-eight paid job")
    require(obstruction_n // native["dimension"] == 5
            and obstruction_n // (native["dimension"] * 8) == 0,
            "raw paid dilation has no consuming target point")
    return encode({
        "schema": SCHEMA,
        "status": "PASS_SAME_PR4416_KAPPA_WITH_SMALLER_LOGARITHMIC_TEMPLATE",
        "source_repository": SOURCE_REPOSITORY, "source_commit": SOURCE_COMMIT,
        "source_file_count": len(SOURCES), "source_package": SOURCE_PACKAGE,
        "source_result_sha256": SOURCES[SOURCE_PACKAGE + "/RESULT.json"]["sha256"],
        "producer_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256": sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
        "source_replay": replay, "template": template,
        "kappa": KAPPA, "outer": outer, "minimum_outer_margin": minimum_outer_margin,
        "incumbent_template": {"H": old_h, "N_encoding": "2^" + str(old_h),
                               "log2_rank_reduction_factor": Q(old_h, h)},
        "negative_controls": controls,
        "raw_flow_obstruction": {
            "n": obstruction_n, "root_target_bound": 5, "root_units": 420,
            "paid_rank": 8, "emitted_rank": 40, "child_target_bound": 0,
            "scope": "Exact two-class lattice arithmetic; no complete raw graph materialized.",
        },
        "fresh_full_word_constants": {
            "rank_encoding": template["N_encoding"],
            "raw_native_scalar_allowance": native["native_scalar_allowance"],
            "owned_banks": "O=U_raw, one bank per actual raw p7 instance",
            "coefficient_envelope": "G=2490856*U_raw+8*R",
            "field_inventory": "Z=W+O",
            "semantic_envelope": "E=64*(Z+N+P+G+1)^3",
            "leaf_and_semantic_cost": "B_cost=P+E",
            "precision_reserve": "C0=32*N*B_cost^2",
            "coordinate_movement_paid_separately": True,
            "actual_counts_materialized": False,
        },
        "scope": "Conditional logarithmic bound for the exact source compiler, with the full unchanged PR4416 native/tensor/padding/splitting and outer replay. All-column physical, spectator, whole-job, storage, precision, analytic, fixed-tape and recovery premises remain inherited; no expanded uniform word or full multiplication theorem is formally verified.",
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="compare the committed receipt")
    mode.add_argument("--out", type=Path, help="write a separate exact receipt")
    args = parser.parse_args()
    result = build(args.source_root)
    if args.out:
        args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        require(result == json.loads((HERE / "CERTIFICATE.json").read_text()),
                "exact saved logarithmic-template certificate replay")
    print(json.dumps({"status": result["status"], "kappa": result["kappa"],
                      "H": result["template"]["H"], "gamma": result["template"]["gamma"],
                      "strict_power_gap": result["template"]["final_strict_power_gap"],
                      "source_files": result["source_file_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
