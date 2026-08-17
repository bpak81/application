# Weekly Client Check-In

A weekly check-in form for coaching clients, delivered as a Google Sheet:
the client opens one link each week, fills in the new week's column, and the
coach sees the answers instantly — with a built-in mini-dashboard (latest
value, week-over-week change, and a trend sparkline for every metric).

## How it works

- **One live Google Sheet per client**, stored in the coach's Drive under
  `Client Check-Ins/`. The client is granted editor access by email, so the
  link Ben sends is all the client ever needs.
- **Questions run down column A** (form-style). **Each week is a column**
  starting at column E, headed by its Monday date (26 weeks pre-filled;
  extend by dragging the last date cell right).
- **Columns B–D are the coach dashboard**, computed automatically:
  - `Latest` — most recent answer for each metric
  - `Change vs last wk` — delta between the two most recent entries
  - `Trend` — sparkline across all entries so far

## Metrics tracked

| Section | Metrics |
| --- | --- |
| Training | Mobility sessions/wk, strength workouts/wk, total working sets/wk, mood before training (1–10), mood after training (1–10) |
| Body | Body weight (lb), waist (in) |
| Cardio | Sessions/wk, type, average session length (min) |
| Heart & recovery | Resting HR (bpm), HR recovery (bpm drop 1 min after peak) |
| Notes | Free-text wins/challenges for the coach |

## Files

- `generate_checkin_csv.py` — generates the template. Run
  `python3 generate_checkin_csv.py` to regenerate `checkin-template.csv`
  (edit `ROWS` to add/remove metrics, `NUM_WEEKS` for horizon, and the
  `DATE(...)` seed in the header for the first week).
- `checkin-template.csv` — the generated template. Uploading it to Google
  Drive with conversion enabled (the default) yields the live sheet:
  formulas (`LET`/`FILTER`/`INDEX`/`SPARKLINE`) and date headers convert
  intact.

## Setting up a new client

1. Regenerate the CSV if the metric list or start date changed.
2. Upload to Drive as a Google Sheet (into `Client Check-Ins/`), named
   `Weekly Check-In — <Client>`.
3. Share the sheet with the client's email as **editor** and send them the
   link. That's the whole loop.
