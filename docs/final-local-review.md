# Local review notes

November 8, 2026

## Code and evidence

The report was checked against the original commit, development history and test
logs. The three bugs have failing tests before their fixes. The shared-code
refactor was committed separately and kept the same failing cases before those
corrections.

The final pricing follows the supplied rules: the student discount starts at
$50, half cents round upward, standard delivery uses the total after discount,
and express always costs $12. Orders check stock before saving. Cancelling an
already cancelled order does not restore stock again.

All 49 test methods pass. The seven selected wrong changes are caught in separate
copies. PDFs were rendered and checked for readable text and page breaks.

## Documents and repository

The report is three pages. The testing record and separate AI evaluation are one
page each. The AI evaluation contains the brief provenance note and explains
which suggestions were used, adapted or rejected.

Repository: https://github.com/McMerger/COMP3415-A2-Campus-Supply-Desk

The repository is public, on main. Assignment commits use Mailles Machiana as
author and committer. The instructor starter keeps its original author.

The submission folder contains the report, testing record, repository link and
an evidence ZIP. Source and Git-history backups are kept separately. D2L has not
been submitted. The reconstructed handout remains unofficial supporting material.
