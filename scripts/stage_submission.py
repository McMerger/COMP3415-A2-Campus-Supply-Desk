"""Stage local submission artifacts and verify a full-history offline restore.

Requires Git and Python; does not contact GitHub or D2L. Run after committing.
"""

import hashlib
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED


ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "output" / "submission"
BRANCH = "assignment-a2/local-improvements"


def git(*arguments):
    return subprocess.check_output(["git", *arguments], cwd=ROOT, text=True).strip()


def main():
    if git("status", "--porcelain"):
        raise SystemExit("Commit reviewed changes before staging.")
    if git("branch", "--show-current") != BRANCH:
        raise SystemExit(f"Switch to {BRANCH} before staging.")
    STAGE.mkdir(parents=True, exist_ok=True)
    files = {
        "output/pdf/Campus-Supply-Desk-A2-Report.pdf": "01-Assignment-Report.pdf",
        "docs/testing-evidence.md": "02-Testing-Evidence.md",
        "output/pdf/Testing-Record.pdf": "02-Testing-Record.pdf",
        "output/pdf/AI-Evaluation.pdf": "supporting/AI-Evaluation.pdf",
        "output/pdf/GitHub-Link.pdf": "03-GitHub-Link.pdf",
        "docs/ai-interactions.md": "05-AI-Use-Record.md",
        "docs/cr01-notes.md": "supporting/CR-01-Planning-Record.md",
        "docs/final-local-review.md": "supporting/Local-Review.md",
        "docs/ai-review.md": "supporting/AI-Evaluation.md",
        "output/Campus-Supply-Desk-A2-local-review.zip": "Campus-Supply-Desk-Source.zip",
    }
    for source, destination in files.items():
        target = STAGE / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, target)
    for obsolete in ("04-Local-Review.md", "05-AI-Evaluation.md", "supporting/Unofficial-Reconstructed-Handout.pdf"):
        old_copy = STAGE / obsolete
        if old_copy.exists():
            old_copy.unlink()
    shutil.copytree(ROOT / "evidence", STAGE / "evidence", dirs_exist_ok=True)
    pending = STAGE / "03-GitHub-Link-PENDING.txt"
    if pending.exists():
        pending.unlink()
    (STAGE / "03-GitHub-Link.txt").write_text(
        "https://github.com/McMerger/COMP3415-A2-Campus-Supply-Desk\n\n"
        "Mailles Machiana | COMP3415 Assignment 2\n"
        "Public repository, main branch.\n",
        encoding="utf-8")
    (STAGE / "READ-ME-FIRST.txt").write_text(
        "Assignment 2 submission files\n\n"
        "The submit-to-d2l folder has the report, testing record, repository link\n"
        "and evidence ZIP, plus the required 05-AI-Use-Record.md.\n"
        "The report answers Tasks 1-6. The separate AI summary is under supporting.\n"
        "Other files here are backups, not extra report requirements.\n"
        "The original handout has now been checked. Keep Checkpoint A separate.\n\n"
        "Restore the backup Git history with:\n"
        f"git clone -b {BRANCH} Campus-Supply-Desk.bundle Campus-Supply-Desk\n"
        "Then run: python -m unittest discover -s tests -v\n\n"
        "GitHub publication is complete. D2L submission has not been performed.\n",
        encoding="utf-8")
    upload = STAGE / "submit-to-d2l"
    upload.mkdir(exist_ok=True)
    for name in ("01-Assignment-Report.pdf", "02-Testing-Record.pdf", "03-GitHub-Link.pdf", "03-GitHub-Link.txt", "05-AI-Use-Record.md"):
        shutil.copyfile(STAGE / name, upload / name)
    with ZipFile(upload / "04-Test-Evidence.zip", "w", ZIP_DEFLATED) as archive:
        for path in sorted((STAGE / "evidence").rglob("*")):
            if path.is_file():
                archive.write(path, "evidence/" + path.relative_to(STAGE / "evidence").as_posix())
    bundle = STAGE / "Campus-Supply-Desk.bundle"
    git("bundle", "create", str(bundle), BRANCH)
    verified = subprocess.run(["git", "bundle", "verify", str(bundle)], cwd=ROOT,
                              capture_output=True, text=True, timeout=30)
    if verified.returncode:
        raise RuntimeError(verified.stdout + verified.stderr)
    with tempfile.TemporaryDirectory(prefix="campus-final-restore-") as directory:
        checkout = Path(directory) / "restored"
        cloned = subprocess.run(["git", "clone", "-b", BRANCH, str(bundle), str(checkout)],
                                capture_output=True, text=True, timeout=30)
        if cloned.returncode:
            raise RuntimeError(cloned.stdout + cloned.stderr)
        result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                                cwd=checkout, capture_output=True, text=True, timeout=60)
        log = (f"Source commit: {git('rev-parse', 'HEAD')}\n"
               f"Restored branch: {BRANCH}\n"
               "Bundle verification:\n" + verified.stdout + verified.stderr +
               "\nTests from restored offline checkout:\n" + result.stdout + result.stderr +
               f"\nExit status: {result.returncode}\n")
        (STAGE / "06-Offline-Restore-Verification.txt").write_text(log, encoding="utf-8")
        if result.returncode:
            raise RuntimeError("Restored checkout tests failed; see verification log.")
        count = re.search(r"Ran (\d+) tests", result.stdout + result.stderr)
        if not count:
            raise RuntimeError("Cannot determine restored test count.")
        test_count = int(count[1])
    paths = sorted(p for p in STAGE.rglob("*") if p.is_file() and p.name != "SHA256SUMS.json")
    hashes = {p.relative_to(STAGE).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    (STAGE / "SHA256SUMS.json").write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
    output = ROOT / "output" / "Campus-Supply-Desk-A2-submission-local.zip"
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in sorted(STAGE.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(STAGE).as_posix())
    with ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Submission archive integrity check failed.")
        for path, digest in hashes.items():
            if hashlib.sha256(archive.read(path)).hexdigest() != digest:
                raise RuntimeError(f"Submission archive checksum mismatch: {path}")
    upload_zip = ROOT / "output" / "Campus-Supply-Desk-A2-submit-to-d2l.zip"
    with ZipFile(upload_zip, "w", ZIP_DEFLATED) as archive:
        for path in sorted(upload.iterdir()):
            if path.is_file():
                archive.write(path, path.name)
    print(f"Offline restore: {test_count} test methods passed; archive checksums verified.")
    print(output)
    print(upload_zip)


if __name__ == "__main__":
    main()
