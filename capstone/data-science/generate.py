#!/usr/bin/env python3
"""Generate a synthetic, labeled Harborlight incident dataset.

Every value comes from a seeded random generator, so the same seed always
writes the same file (check with sha256sum). No real names or customer data.

Usage: python generate.py [--seed 4031] [--out data/generated.csv]
"""
import argparse
import csv
import math
import random
from datetime import datetime, timedelta

END = datetime(2026, 11, 15)   # fixed end date, so the output never depends on "today"
DAYS = 120                     # covers more than the 90 days criterion 1 asks for

# category: (share of incidents, median hours to resolve, spread of the long tail)
CATEGORIES = {
    "scanners and handhelds": (0.30, 4.0, 0.9),
    "dispatch app":           (0.22, 8.0, 1.0),
    "printers and labels":    (0.20, 2.5, 0.7),
    "logins and access":      (0.16, 1.5, 0.8),
    "network":                (0.12, 12.0, 1.1),
}

TITLES = {
    "scanners and handhelds": ["Handheld scanner will not sync", "Scanner battery drains in an hour",
                               "Barcode reader misses labels", "Handheld frozen on login screen",
                               "Scanner shows wrong depot", "Device will not charge in cradle"],
    "dispatch app":           ["Dispatch app crashes on route list", "Driver stops not updating",
                               "Route optimizer times out", "Dispatch board shows old loads",
                               "Cannot assign driver to load", "App slow during morning dispatch"],
    "printers and labels":    ["Label printer jams", "Shipping labels print blank",
                               "Printer offline at dock", "Labels print with wrong address",
                               "Printer out of ribbon", "Bill of lading will not print"],
    "logins and access":      ["Password reset needed", "Account locked after shift change",
                               "New hire cannot log in", "Two-factor code not arriving",
                               "Access denied to depot reports", "Certificate warning on login page"],
    "network":                ["Depot Wi-Fi drops", "VPN disconnects for drivers",
                               "Slow connection at warehouse", "Dock door access point down",
                               "Internet outage at depot", "Cannot reach shared drive"],
}
# A few titles that could belong to more than one category, so the title does not always give the answer away.
AMBIGUOUS = ["Device cannot connect", "Error message at depot", "Something is slow today"]

DEPOTS = [f"Depot {n}" for n in range(1, 9)]
# Busier on weekdays (Mon=0) and during working hours.
WEEKDAY_FACTOR = [1.15, 1.10, 1.05, 1.05, 1.0, 0.45, 0.35]
HOUR_WEIGHT = [1, 1, 1, 1, 2, 4, 8, 10, 11, 11, 10, 9, 8, 9, 10, 9, 8, 6, 4, 3, 2, 2, 1, 1]
BASE_PER_DAY = 92
GROWTH_PER_WEEK = 0.02         # the planted trend: about 2% more incidents each week


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=4031)
    ap.add_argument("--out", default="data/generated.csv")
    args = ap.parse_args()
    rng = random.Random(args.seed)

    names = list(CATEGORIES)
    shares = [CATEGORIES[c][0] for c in names]
    start = END - timedelta(days=DAYS)
    rows = []
    for d in range(DAYS):
        day = start + timedelta(days=d)
        expected = BASE_PER_DAY * (1 + GROWTH_PER_WEEK) ** (d / 7) * WEEKDAY_FACTOR[day.weekday()]
        n = max(0, round(expected * rng.uniform(0.85, 1.15)))
        for _ in range(n):
            hour = rng.choices(range(24), weights=HOUR_WEIGHT)[0]
            created = day + timedelta(hours=hour, minutes=rng.randrange(60), seconds=rng.randrange(60))
            cat = rng.choices(names, weights=shares)[0]
            title = rng.choice(AMBIGUOUS) if rng.random() < 0.05 else rng.choice(TITLES[cat])
            title = f"{title} at {rng.choice(DEPOTS)}"
            _, median_h, sigma = CATEGORIES[cat]
            hours = round(rng.lognormvariate(math.log(median_h), sigma), 2)  # skewed: most fast, a few take days
            resolved = created + timedelta(hours=hours)
            age_days = (END - created).total_seconds() / 86400
            # Older incidents are almost all closed; the most recent ones are often still open.
            if resolved <= END and rng.random() < min(0.98, 0.55 + age_days * 0.15):
                status, res_at, res_h = "closed", resolved.isoformat(sep=" "), hours
            else:
                status, res_at, res_h = rng.choice(["open", "in_progress"]), "", ""
            rows.append([created, title, cat, status, res_at, res_h])

    rows.sort(key=lambda r: r[0])
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["id", "title", "category", "status", "created_at", "resolved_at", "resolution_hours"])
        for i, (created, title, cat, status, res_at, res_h) in enumerate(rows, 1):
            w.writerow([i, title, cat, status, created.isoformat(sep=" "), res_at, res_h])
    print(f"wrote {len(rows)} rows to {args.out} (seed {args.seed})")


if __name__ == "__main__":
    main()
