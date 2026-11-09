"""Package tracked working files with their original verified bytes."""

import hashlib
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED


ROOT = Path(__file__).resolve().parents[1]


def main():
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT)
    if dirty.strip():
        raise SystemExit("Commit or review outstanding changes before packaging.")
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    output = ROOT / "output" / "Campus-Supply-Desk-A2-local-review.zip"
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for relative in paths:
            if relative:
                archive.write(ROOT / relative, relative)
    with ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Archive integrity check failed.")
        metadata = json.loads(archive.read("evidence/09-verification-metadata.json"))
        for path, expected in metadata["sha256"].items():
            if hashlib.sha256(archive.read(path)).hexdigest() != expected:
                raise RuntimeError(f"Archived source hash mismatch: {path}")
        pdf = "output/pdf/Campus-Supply-Desk-A2-Report.pdf"
        if archive.read(pdf) != (ROOT / pdf).read_bytes():
            raise RuntimeError("Archived PDF differs from visually reviewed PDF.")
        print(f"Verified {len(archive.namelist())} archived files and all source/test hashes.")
    print(output)


if __name__ == "__main__":
    main()
