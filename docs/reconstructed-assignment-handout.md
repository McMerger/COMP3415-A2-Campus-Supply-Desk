# Assignment 2
## Campus Supply Desk - reconstructed working handout

UNOFFICIAL RECONSTRUCTION - prepared November 8, 2026 with AI assistance.
This is a working guide assembled from the assignment announcement supplied
in chat, the starter README and functional specification, and the supplied
CR-01. It is not the instructor's original handout and carries no authority
to set deadlines, marks, academic-integrity policy or submission rules.

### Assignment purpose - confirmed by the supplied announcement

Work with an existing software application to develop meaningful tests,
identify code smells, refactor code, and verify preservation of existing
functionality. Implement client change request CR-01 and critically evaluate
AI-generated recommendations. Improve the existing application rather than
replacing it with an unrelated rewrite.

### Starter and setup - confirmed by the repository

Repository: https://github.com/iiConick/COMP3415-A2-Campus-Supply-Desk

Clone the shared repository, follow its README to run the application, and
maintain the work in your own repository. The starter uses Python 3.10 or
newer and requires no additional application packages or database.

```sh
git clone https://github.com/iiConick/COMP3415-A2-Campus-Supply-Desk.git
cd COMP3415-A2-Campus-Supply-Desk
python --version
python -m supplydesk
python -m unittest discover -s tests -v
```

### Two separate submissions - confirmed by the announcement

Checkpoint A is an independent baseline analysis submitted to its designated
D2L folder. It contains a system understanding note, five identified code
problems and an initial testing strategy. The starter README requires submission
of Checkpoint A before using generative AI.

The final assignment follows Checkpoint A and includes the complete PDF report,
own GitHub repository link and testing evidence record in the final A2 D2L
folder. Do not combine the two submissions. Leave a meaningful interval to
demonstrate subsequent development; no precise interval was supplied.

The user states that Checkpoint A is already submitted. Its original contents
and submission timestamp were not available for this reconstruction.

<!-- pagebreak -->

## Post-checkpoint work

The activities below follow the supplied task description. The suggested
documentation details are practical guidance, not invented grading criteria.

### Understand and document the application

Explain the application's purpose, components, execution flow and persistence.
The service owns business rules; menu and command adapters expose its operations;
JSON storage preserves stock and history. Use the functional specification as
the expected-behavior reference, because the starter is intentionally imperfect.

### Develop meaningful tests

Exercise important normal behavior, boundaries, invalid input and saved state.
Demonstrate whether the original implementation satisfies expected behavior.
Retain tests that detect defects as regression tests after fixes. Record actual
commands and results; distinguish initial failures from final failures.

Suggested risk areas include merchandise discounts and rounding, delivery
thresholds, duplicate item stock, invalid-request non-mutation, ID sequencing,
quote non-reservation, saved snapshots and repeated cancellation. Test public
adapters when changing their supported choices or displayed information.

No official minimum test count, coverage percentage or required testing tool
was present in the available assignment announcement.

### Identify problems and refactor

The baseline checkpoint requires five identified code problems. For subsequent
work, explain the relevant smell or defect with source evidence and its effect.
Describe the chosen refactoring and why it suits this small application.
Separate structural changes from intentional bug fixes where practical, and
verify the required behavior after each meaningful change.

Keep meaningful Git history. Preserve valid existing behavior while addressing
demonstrated defects and CR-01. Do not add payments, authentication, taxes,
addresses or shipping workflows. Concurrent writers, arbitrary manual save
edits, schema migration and crash recovery are outside the initial specification.

### Critically evaluate AI recommendations

Explain which AI recommendations were accepted, adapted or rejected and why.
Compare recommendations with the requirements and test evidence; identify
incorrect assumptions and unnecessary complexity. Review AI-generated code
and claims rather than treating plausible output as proof.

Suggested records include the recommendation, decision, rationale, affected
source and verification. Any required prompt transcript, disclosure wording or
specific AI policy must be obtained from the original course instructions;
those details were not supplied here.

<!-- pagebreak -->

## CR-01: Express delivery

This section restates the supplied CR-01 acceptance requirements. It introduces
no new delivery promises, service integrations or payment requirements.

### Acceptance requirements

- Accept `express` for quotes and orders through the service API, individual
  commands and interactive menu.
- Always charge 1,200 cents ($12.00 CAD) for express. Never waive the fee,
  including orders eligible for free standard delivery.
- Preserve student-discount eligibility and half-up rounding. Apply discounts
  to merchandise only, excluding the delivery charge.
- Preserve pickup and standard delivery behavior, including free standard
  delivery at the existing post-discount threshold.
- Keep quote and order pricing consistent. Express orders retain fulfillment,
  original items, delivery fee, discount and total through retrieval, reopening
  from a save file and cancellation.
- Preserve validation, stock, order numbering, history and cancellation rules.
  Reject unsupported fulfillment values.
- Update menu prompts, command help and relevant documentation so express is
  discoverable. Preserve regular-customer and pickup defaults.

### Examples from the client request

| Request | Calculation in CAD | Expected total |
| --- | --- | --- |
| Regular, two notebooks, express | $10 merchandise + $12 fee | $22 |
| Student, two hoodies, express | $80 merchandise - $8 discount + $12 fee | $84 |
| Regular, three hoodies, standard delivery | $120 merchandise + $0 fee | $120 |
| Regular, three hoodies, express | $120 merchandise + $12 fee | $132 |

```sh
python -m supplydesk quote --customer student --fulfillment express --item hoodie:2
```

Expected `total_cents`: 8400. The original request is preserved separately at
`docs/CR-01.md` for comparison.

### Existing business rules to preserve

All calculations use integer cents. Students receive 10% off at merchandise
subtotal 5,000 cents or more, with half cents rounded upward. Pickup is free.
Standard delivery costs 600 cents and is free at 10,000 cents after merchandise
discount. Each quantity must be an integer from 1 through 99, excluding booleans;
combined duplicate quantities must fit current stock. Quotes must not save or
reserve stock. Cancellation restores units once and preserves the original
order snapshot in history.

<!-- pagebreak -->

## Final submission and review outcome

### Confirmed final deliverables

- A complete PDF report.
- A link to the student's own GitHub repository containing the work.
- A testing evidence record.
- Submission through the final Assignment 2 D2L folder, separate from Checkpoint A.

Suggested report organization: system context, problem analysis, testing
strategy and evidence, refactoring rationale and preservation checks, CR-01
implementation and acceptance evidence, critical AI evaluation, and limitations.
This organization is recommended for clarity; the original template is unknown.

### Current local package compared with known requirements

| Area | Observed local outcome |
| --- | --- |
| System understanding and problems | Report explains components and six evidenced problems; original independent checkpoint was not recreated. |
| Meaningful tests and verification | 49 test methods pass; baseline failures and later corrections are recorded. Seven targeted defective mutations are detected. |
| Refactoring | Shared quote construction, order lookup and inventory adjustment; separate local commits distinguish structure, fixes and express support. |
| CR-01 | Service, commands and menu support fixed-fee express; pricing, persistence, cancellation, discoverability and defaults are tested. |
| PDF report and evidence | Local review report, editable source, AI review and testing evidence record exist. Student review remains pending. |
| Own GitHub repository link | Not published. Everything remains local pending the user's approval to push. |
| Final D2L submission | Not performed. |

### Details that cannot be reconstructed reliably

Deadline and timezone; grading weights; official report length/template; naming
and identity requirements; minimum numbers or types of tests/refactorings;
coverage targets; required screenshots or evidence format; AI-use policy and
transcript requirements; repository visibility; team rules; and the exact
minimum interval between submissions were not supplied. No marks or predicted
grade can responsibly be assigned from this reconstruction.

### Basis for this reconstruction

Sources: the assignment announcement pasted by the user; starter README and
functional specification at baseline `82ed75e0714e50c086a13ee491f51b349814d8a4`;
and the supplied `CR-01 (1).md`, preserved as `docs/CR-01.md`. Current local
outcomes refer to the recorded final tests and report, not to instructor feedback.
The original official handout takes precedence whenever it becomes available.
