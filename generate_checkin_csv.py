#!/usr/bin/env python3
"""Generate the Weekly Client Check-In CSV template.

Layout: questions run down column A (form-style, easy to fill on any device);
each week is a column starting at E. Columns B-D are the coach dashboard:
Latest value, Change vs previous entry, and a sparkline Trend.
Formulas survive CSV -> Google Sheets conversion.
"""
import csv
import io

NUM_WEEKS = 26  # E .. AD
FIRST_COL_IDX = 5  # column E (1-indexed)


def col_letter(n: int) -> str:
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


FIRST_COL = col_letter(FIRST_COL_IDX)              # E
LAST_COL = col_letter(FIRST_COL_IDX + NUM_WEEKS - 1)  # AD

NUMERIC, TEXT, SECTION = "numeric", "text", "section"

ROWS = [
    (SECTION, "TRAINING"),
    (NUMERIC, "Mobility training — sessions completed this week"),
    (NUMERIC, "Strength workouts — sessions completed this week"),
    (NUMERIC, "Total working sets completed this week"),
    (NUMERIC, "Mood before training, on average (1–10)"),
    (NUMERIC, "Mood after training, on average (1–10)"),
    (SECTION, "BODY"),
    (NUMERIC, "Body weight (lb)"),
    (NUMERIC, "Waist measurement (in)"),
    (SECTION, "CARDIO"),
    (NUMERIC, "Cardio — sessions completed this week"),
    (TEXT,    "Cardio — type (walk / bike / row / etc.)"),
    (NUMERIC, "Cardio — average length of each session (min)"),
    (SECTION, "HEART & RECOVERY"),
    (NUMERIC, "Resting heart rate (bpm)"),
    (NUMERIC, "Heart rate recovery — bpm drop 1 min after peak effort"),
    (SECTION, "NOTES"),
    (TEXT,    "Wins, challenges, anything your coach should know"),
]


def week_range(row: int) -> str:
    return f"${FIRST_COL}{row}:${LAST_COL}{row}"


def latest_formula(row: int) -> str:
    r = week_range(row)
    return (f'=IFERROR(LET(v,FILTER({r},{r}<>""),'
            f'INDEX(v,1,COLUMNS(v))),"")')


def change_formula(row: int) -> str:
    r = week_range(row)
    return (f'=IFERROR(LET(v,FILTER({r},{r}<>""),n,COLUMNS(v),'
            f'IF(n<2,"",INDEX(v,1,n)-INDEX(v,1,n-1))),"")')


def trend_formula(row: int) -> str:
    r = week_range(row)
    return f'=IFERROR(SPARKLINE(FILTER({r},{r}<>"")),"")'


rows_out = []
rows_out.append(["WEEKLY CLIENT CHECK-IN"])
rows_out.append(["How it works: each week, find the column with this week's "
                 "date and answer every question down that column. Your coach "
                 "sees your answers the moment you enter them. Columns B–D "
                 "update automatically — leave them alone."])
rows_out.append([])

# Row 4: headers. Week dates are formulas so they format as real dates.
header = ["Question", "Latest", "Change vs last wk", "Trend"]
header.append("=DATE(2026,8,17)")  # Monday, Aug 17 2026
for i in range(1, NUM_WEEKS):
    prev = col_letter(FIRST_COL_IDX + i - 1)
    header.append(f"={prev}4+7")
rows_out.append(header)

row_num = 5
for kind, label in ROWS:
    if kind == SECTION:
        rows_out.append([label])
    else:
        latest = latest_formula(row_num)
        change = change_formula(row_num) if kind == NUMERIC else ""
        trend = trend_formula(row_num) if kind == NUMERIC else ""
        rows_out.append([label, latest, change, trend])
    row_num += 1

buf = io.StringIO()
writer = csv.writer(buf, lineterminator="\n")
for r in rows_out:
    writer.writerow(r)

csv_text = buf.getvalue()
with open("checkin-template.csv", "w") as f:
    f.write(csv_text)
print(csv_text)
