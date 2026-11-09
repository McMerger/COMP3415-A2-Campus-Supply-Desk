# Local review handoff

This checkout contains post-Checkpoint-A work for Campus Supply Desk. All
changes are local on `assignment-a2/local-improvements`. Do not push to the
instructor repository. The user has requested approval before any push.

## Start here

1. Read `output/pdf/Campus-Supply-Desk-A2-Report.pdf`.
2. Review `docs/testing-evidence.md` and `docs/ai-review.md`.
3. Run `python -m unittest discover -s tests -v` (49 methods should pass).
4. Run `python scripts/verify.py` to reproduce final logs and 7 targeted mutations.
5. Inspect `git diff 82ed75e -- supplydesk tests` and `git log --oneline`.

## Before final submission

- Compare the original assignment handout to the local report and evidence.
  The handout was not available in this chat.
- Review the AI-assisted analysis and add the student's own critical assessment
  and any required identity fields or AI-use disclosures/transcripts.
- Keep Checkpoint A separate; its contents were not regenerated here.
- Obtain the user's explicit approval before creating/publishing a student-owned
  remote repository. Record its actual URL in the final report after publication.
- Submit the reviewed PDF, repository link and evidence to the final A2 D2L
  folder. No submission action has occurred.

## Archive

`output/Campus-Supply-Desk-A2-local-review.zip` is a snapshot of tracked files
at the packaging commit, including the PDF, source, tests and evidence. It
excludes `.git`, temporary PDF images, runtime data and the ZIP itself. Use
the original local checkout to inspect the actual development commit history.
Recreate it from a clean checkout with `python scripts/package_review.py`.
The packager preserves working-file bytes and validates all recorded source
hashes and the archived PDF against the reviewed original.

## Report rendering

The app and tests need only Python's standard library. PDF regeneration uses
ReportLab: `python -m pip install reportlab`, then `python scripts/build_report.py`.
ReportLab is a reporting dependency and is not imported by the application.
