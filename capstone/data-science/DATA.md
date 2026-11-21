# Data decision: Applied Data Science track

## The choice
The live `tickets` table has only id, title, status, description and created_at, with no category and no resolution time, and the Week 10 seeded rows cover about one week. Instead of changing the schema of the running app, I generate a synthetic, labeled dataset with `generate.py` and analyze the CSV directly with pandas (the README's "analyze outside the database" path). This keeps the live app and its database untouched, and anyone can recreate the exact same file from the seed.

Command: `~/data-science-venv/bin/python generate.py --seed 4031` writes `data/generated.csv`. Running it twice gives the same sha256.

## Columns
| Column | Meaning |
| --- | --- |
| id | Row number, ordered by created_at |
| title | Incident title from a per-category list, plus a depot name (Depot 1 to 8) |
| category | One of 5: scanners and handhelds, dispatch app, printers and labels, logins and access, network |
| status | closed, open or in_progress |
| created_at | When the incident was filed, 2026-07-18 to 2026-11-14 (120 days) |
| resolved_at | When it was closed (closed rows only) |
| resolution_hours | resolved_at minus created_at in hours (closed rows only) |

## What I planted (so the analysis has something real to find)
- Growth: about 2% more incidents each week.
- Weekly and daily rhythm: weekdays are 2 to 3 times busier than weekends, and most incidents arrive from 6:00 to 17:00.
- Category mix: scanners 30%, dispatch app 22%, printers 20%, logins 16%, network 12%.
- Resolution time is skewed (lognormal): medians of about 1.5 h (logins), 2.5 h (printers), 4 h (scanners), 8 h (dispatch) and 12 h (network), with long tails.
- Status: older incidents are almost all closed; the most recent ones are often still open or in progress, like a real queue.
- Noise: 5% of titles are ambiguous ("Device cannot connect") and do not reveal their category.

## Limits
- All data is synthetic. It contains no real names, employees or customers.
- The analysis can only find what I planted, so it shows that the method works, not what Harborlight's real desk looks like.
- Resolution time is how long an incident stayed open, not how long an agent worked on it. The staffing model will need a separate handling-time assumption.
- The dataset does not include the live tickets table, so it does not reflect anything users typed into the app.
