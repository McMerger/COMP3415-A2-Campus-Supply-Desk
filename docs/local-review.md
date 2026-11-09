# Submission files

For the final A2 folder in D2L, use the report PDF, testing record and your
repository link:

https://github.com/McMerger/COMP3415-A2-Campus-Supply-Desk

The repository is public. The ready-to-upload files are in
`output/submission/submit-to-d2l/`. The testing record refers to logs supplied
inside the evidence ZIP. The separate AI note expands on the section already
included in the report.

The outer submission package also keeps the source snapshot, Git bundle and
offline verification log as backup. The reconstructed handout is unofficial
background material, not a submission requirement. Keep Checkpoint A separate.
Nothing has been uploaded to D2L.

Run `python -m unittest discover -s tests -v` to check the code. Use
`python scripts/verify.py` for the seven extra mistake checks. Report PDFs can be
rebuilt with `scripts/build_report.py` using ReportLab; the application itself
needs only Python's standard library.
