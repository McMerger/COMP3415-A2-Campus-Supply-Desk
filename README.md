# Campus Supply Desk

COMP3415 Assignment 2. This is the campus merchandise program with the tests,
fixes and express delivery change added.

Repo: https://github.com/McMerger/COMP3415-A2-Campus-Supply-Desk

## Report and notes

[Download the submission files](output/Campus-Supply-Desk-A2-submit-to-d2l.zip).
This ZIP has the report, testing notes, repository link, test evidence and AI-use record.

- [Report](output/pdf/Campus-Supply-Desk-A2-Report.pdf)
- [Testing notes](output/pdf/Testing-Record.pdf)
- [AI suggestion notes](output/pdf/AI-Evaluation.pdf)
- [Repository link](output/pdf/GitHub-Link.pdf)
- [AI-use record](docs/ai-interactions.md)

The editable text is in `docs/`. Test output is in `evidence/`.
Checkpoint A is a separate submission.

## Run it

Use Python 3.10 or newer. The program doesn't need extra packages or a database.

```sh
python -m supplydesk
```

You can also run one command at a time:

```sh
python -m supplydesk catalog
python -m supplydesk quote --item notebook:2
python -m supplydesk quote --customer student --fulfillment express --item hoodie:2
```

The express example totals 8400 cents ($84). Pickup is free. Standard delivery
costs $6 and is free at $100 after discount. Express always costs $12.

The menu asks before placing or cancelling an order. Single commands act straight
away and return JSON. Typed quantities are converted to integers; prices in JSON
are whole cents.

## Check the tests

```sh
python -m unittest discover -s tests -v
python scripts/verify.py
```

There are 50 passing test methods. The second command also checks seven wrong
changes in temporary copies. It leaves the working code alone and updates logs
07-09. Older logs keep the before-and-after results.

## Main changes

Quote and order calculations share the same helper now. The $50 student discount
boundary is fixed, duplicate item lines can't oversell stock, and cancelling an
order twice doesn't add stock twice. Express works through the service, commands
and menu. Saved orders keep their original prices and delivery fee.

## Saves and files

Orders and stock go in `.supplydesk/state.json`. Quotes don't save or reserve
anything. For a separate practice save:

```sh
python -m supplydesk --data .supplydesk/practice.json
```

Using that filename again loads the same practice data. Use a new filename for a
fresh session, and don't run two writers against the same save.

Business rules are in `supplydesk/service.py`; `cli.py` and `menu.py` handle input
and output. `storage.py` handles JSON. See `FUNCTIONAL_SPEC.md` and `docs/CR-01.md`
for the expected behavior.

The [instructor starter](https://github.com/iiConick/COMP3415-A2-Campus-Supply-Desk)
is kept in the history with its original credit. The original README is available
at commit `82ed75e`.
