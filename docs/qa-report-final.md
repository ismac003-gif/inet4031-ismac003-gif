# QA Report: Applied Data Science Track

Author and tester: Idiris Ismacil (Local VM, individual)

| ID | Test | Expected result | Status |
| --- | --- | --- | --- |
| TC-01 | Run `generate.py` twice with seed 4031 and compare sha256sum | Both hashes are identical | Pass (2026-11-21) |
| TC-02 | Run `data_quality.py` | row_count >= 10000, days_covered >= 90, category_count >= 4, closed_rows_missing_resolution = 0, exit code 0 | Pass (2026-11-21) |
| TC-03 | Search generated.csv for real names or emails | None found; all depots are "Depot 1" to "Depot 8" | Pass (2026-11-21) |
| TC-04 | Run the one-command pipeline from a clean `output/` folder | Three analysis CSVs and three PNGs are created | Pending |
| TC-05 | Open each PNG | Each has a title, labeled axes, and units | Pending |
| TC-06 | Compare weekly volume CSV with the planted growth | Slope is positive and p-value < 0.05 | Pending |
| TC-07 | Compare median resolution per category with DATA.md | Order matches the planted medians (logins fastest, network slowest) | Pending |
| TC-08 | Count words in report.md and read the last section | Two pages or less, ends with a number or range of agents and the hours or categories to cover | Pending |
| TC-09 | Rebuild on a fresh VM following only the README | Pipeline runs and row counts match data_quality.csv | Pending |
