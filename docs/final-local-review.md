# Final local review

Publication update: following this local review, the user explicitly authorized
creation and publication of their own GitHub repository. It is now available
at https://github.com/McMerger/COMP3415-A2-Campus-Supply-Desk (private, branch
`main`). Assignment commits are authored/committed as Mailles Machiana and
linked on GitHub to McMerger, without AI co-author trailers. The original
instructor commit keeps its original attribution. The remainder of this review
records the earlier local-only state; D2L submission remains unperformed.

Reviewed November 8, 2026 by Codex at the user's request. This is an additional
AI-assisted review of source, tests, report and AI evaluation. It does not
represent the student's personal assessment or approval to publish online.

## Report and implementation review

The report's baseline commit, staged test counts and local commit references
were compared with the repository history and recorded output. Three baseline
defects are supported by failing tests before fixes. The structural refactor
retains those failing cases, and the corrections have their own commit.

The service's inclusive discount threshold, integer half-up rounding,
post-discount standard-delivery threshold and unconditional express fee agree
with the available functional specification and supplied CR-01. Placement
validates current state before stock mutation; repeated cancellation returns
without another restoration or save. Public interface choices and defaults
match the documentation. Snapshot and invalid-request tests support the stated
persistence claims. No additional in-scope implementation defect was identified
in this review; this is not proof of exhaustive correctness.

The PDF report and reconstructed handout were rendered and visually inspected
during their creation. Both distinguish supplied requirements from unknown
rubric details. The reconstructed handout is explicitly unofficial and is
included only as a supporting working guide, not an instructor-issued document.

## AI evaluation review and correction

The critique correctly rejects floating-point ties-to-even rounding for the
specified half-up rule, applying standard delivery's waiver to express, and
unnecessary database/strategy-class replacement. Its acceptance of a shared
builder and preservation of separate duplicate lines is supported by tests.
Avoiding raw dictionary indexing on unvalidated IDs is a reasonable small-scope
choice; explicit type validation could also make dictionary lookup safe.

One documentation ambiguity was corrected: the AI record now explicitly
distinguishes the implementation-time shared-builder recommendation from
alternatives evaluated while writing the record. It must not be mistaken for
a full historical prompt transcript or independent student-authored critique.
No missing transcript or unavailable independent checkpoint was fabricated.

## Locally prepared submission

`scripts/stage_submission.py` prepares an ignored `output/submission/` folder
containing the report, evidence record, actual evidence files, review record,
source snapshot, full-history Git bundle and instructions. It verifies the
bundle, restores it to an isolated local checkout and runs the complete test
suite there. The resulting verification log records the actual outcome.
Checksums identify the staged files. A separate ZIP contains the staged folder.

The GitHub-link file explicitly says no live URL exists yet. It does not use
the instructor's repository as the student's submission link. A local Git
bundle is provided to preserve all implementation commits offline; it does
not replace the requirement for a live own-repository link at submission time.

## Remaining external actions and uncertainty

No GitHub repository creation, push, approval to push or D2L submission has
occurred. The user's instruction for this step is to do the preparation
locally. Publication approval and actual uploading therefore remain external
actions. Student review cannot be impersonated by an AI review.

The complete instructor handout is still unavailable. Compliance with its
unseen formatting, identity fields, evidence policy, AI policy, visibility,
deadlines and grading weights cannot be certified by this local review.
