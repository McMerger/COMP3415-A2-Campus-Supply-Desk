"""Reproduce final tests and targeted mutations without editing the checkout.

Run from any directory with Python 3.10+: python scripts/verify.py
Only standard-library modules are required. Evidence files are overwritten.
"""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
COMMAND = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]

# Each mutation is deliberately wrong according to a named requirement.
# A mutation is detected only if its isolated tests fail (no syntax errors).
MUTATIONS = [
    ("discount_excludes_50_dollars", "supplydesk/service.py",
     "subtotal_cents >= STUDENT_DISCOUNT_THRESHOLD_CENTS", "subtotal_cents > STUDENT_DISCOUNT_THRESHOLD_CENTS",
     "tests.test_pricing"),
    ("duplicate_stock_checked_per_line", "supplydesk/service.py",
     'if requested_quantities[product_id] > product["stock"]:', 'if quantity > product["stock"]:',
     "tests.test_validation"),
    ("repeat_cancel_restores_twice", "supplydesk/service.py",
     'if order["status"] == "cancelled":', 'if False:', "tests.test_lifecycle"),
    ("express_fee_waived_at_100_dollars", "supplydesk/service.py",
     'elif fulfillment == "express":',
     'elif fulfillment == "express" and subtotal_cents - discount_cents < FREE_DELIVERY_THRESHOLD_CENTS:',
     "tests.test_express"),
    ("express_fee_discounted", "supplydesk/service.py",
     'delivery_cents = EXPRESS_DELIVERY_CENTS',
     'delivery_cents = EXPRESS_DELIVERY_CENTS * (90 if customer_type == "student" else 100) // 100',
     "tests.test_express"),
    ("discount_rounds_half_cent_down", "supplydesk/service.py",
     'subtotal_cents * STUDENT_DISCOUNT_PERCENT + 50', 'subtotal_cents * STUDENT_DISCOUNT_PERCENT + 49',
     "tests.test_pricing"),
    ("cli_express_choice_removed", "supplydesk/cli.py",
     'choices=("pickup", "delivery", "express")', 'choices=("pickup", "delivery")',
     "tests.test_interfaces.CommandTests"),
]


def run(command, cwd):
    return subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=60)


def main():
    EVIDENCE.mkdir(exist_ok=True)
    result = run(COMMAND, ROOT)
    (EVIDENCE / "07-final-tests.txt").write_text(result.stdout, encoding="utf-8")
    if result.returncode:
        print(result.stdout)
        return result.returncode
    mutations = []
    for name, filename, original, replacement, test_module in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix="campus-mutation-") as directory:
            checkout = Path(directory)
            for folder in ("supplydesk", "tests"):
                shutil.copytree(ROOT / folder, checkout / folder,
                                ignore=shutil.ignore_patterns("__pycache__"))
            path = checkout / filename
            source = path.read_text(encoding="utf-8")
            if source.count(original) != 1:
                raise RuntimeError(f"Mutation target is ambiguous or missing: {name}")
            mutated = source.replace(original, replacement)
            compile(mutated, filename, "exec")
            path.write_text(mutated, encoding="utf-8")
            checked = run([sys.executable, "-m", "unittest", test_module, "-v"], checkout)
            detected = checked.returncode == 1 and "FAIL:" in checked.stdout
            mutations.append({"mutation": name, "test_module": test_module,
                              "detected": detected, "exit_code": checked.returncode,
                              "output": checked.stdout})
    (EVIDENCE / "08-targeted-mutations.json").write_text(
        json.dumps(mutations, indent=2) + "\n", encoding="utf-8")
    metadata = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": sys.platform,
        "command": COMMAND,
        "suite_exit_code": result.returncode,
        "targeted_mutations_detected": sum(m["detected"] for m in mutations),
        "targeted_mutations_total": len(mutations),
        "sha256": {str(p.relative_to(ROOT)).replace("\\", "/"):
                   hashlib.sha256(p.read_bytes()).hexdigest()
                   for folder in ("supplydesk", "tests")
                   for p in sorted((ROOT / folder).glob("*.py"))},
    }
    (EVIDENCE / "09-verification-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(result.stdout.splitlines()[-4:])
    print(f"Detected {metadata['targeted_mutations_detected']}/{len(mutations)} targeted mutations.")
    return 0 if all(m["detected"] for m in mutations) else 1


if __name__ == "__main__":
    raise SystemExit(main())
