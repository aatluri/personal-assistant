# Dashboard design: Overview and Explore

Status: **design agreed, not built yet.** Visual mockup: [`overview-mockup.html`](overview-mockup.html)
(open it in a browser; all numbers are sample data).

This replaces the dashboard parts of the older `docs/ui/` documents.

## What the user wants

1. **One place to see today's data**: sleep, recovery, activity, nutrition, workouts and body,
   at a glance.
2. **The same view for a week or a month**, to see how a whole period went, not only a single day.
3. **Trends and correlations**: see how metrics change over time and find relationships between
   them (for example, sleep against next-day HRV).

## Page structure

Two pages, because they serve different jobs:

| Page | Job | Feel |
|---|---|---|
| **Overview** | "How did I do?" for a day, week or month | Read at a glance; few controls |
| **Explore** (later) | "What's changing, and what affects what?" | Interactive: trends, correlations, insights |

Work starts with **Overview**.

## Overview page

### Controls

- `Day | Week | Month` segmented control, plus ‹ › arrows to step through periods.
- Calendar periods: Mon–Sun weeks, calendar months. A current period shows "so far"
  ("Week so far · 4 of 7 days").
- "Data through …" shows the latest date that has any data (a date, no time), because imports
  run behind real time. The exact import time is not read back from the Sheet.

### Layout (top to bottom)

1. **Highlight chips**: goal hit rate, streaks, and bests for the period, using only stored
   values (most steps, longest sleep, longest workout, furthest distance). Pace-based bests such
   as "best 5k" are not possible: workouts have no split times.
2. **Four headline numbers**: steps, sleep, resting HR, workouts. Each is compared with your
   usual (Day) or with the previous period (Week/Month).
3. **Six cards** (2 columns on desktop, 1 on mobile):
   - **Sleep**: duration, stage split (deep/core/REM/awake), bar per night. Day view shows the
     night that ended that morning (see Sleep date below).
   - **Recovery**: resting HR, HRV, blood oxygen, respiratory rate, each against your baseline.
   - **Activity**: steps and active energy. Day view shows the last 7 days as daily bars with the
     selected day highlighted; steps are stored once per day, so hourly bars are not possible.
     Week/Month show daily bars.
   - **Nutrition**: calories, protein and water against goal, macro split, logging coverage
     (logged days; nutrition is stored as one total per day, not per meal).
   - **Training**: session list (Day/Week) or totals by workout type (Month).
   - **Body**: latest weight, change over the period, trend line, body fat, waist.
4. **Alert strip**: heart rate notifications, shown only when there are any.

### How each metric is combined over a period

| Metric | Day | Week / Month |
|---|---|---|
| Steps, active kcal | value | daily average, plus total |
| Workouts | the day's sessions | count, total minutes, kcal |
| Sleep | the night that ended that morning | nightly average over nights with data |
| RHR, HRV, SpO₂, respiratory rate | value | average (never a total) |
| Calories, protein, macros | value | average over **logged** days only |
| Weight, body fat, waist | latest value and how many days old it is | change from start to end of period |
| HR notifications | count | count |

### Rules

- Days with no data are shown as gaps, never as zeros, and averages ignore them.
  Show coverage ("Logged 5 of 7 days").
- Compare each number with something: your 30-day baseline (Day) or the previous period
  (Week/Month).
- Tapping a day in a Week/Month chart switches to Day view for that date.
- Each section keeps one color: sleep purple, heart coral, activity teal, nutrition amber.

### Sleep date

A night of sleep belongs to **the day you woke up**, the same as Health Auto Export and the
Sleep log page. Overview uses the stored Sleep_Metrics `date` as it is. Sleep from Nov 5 23:00
to Nov 6 07:00, or from Nov 6 01:00 to 07:00, shows under **Nov 6**.

- **Evidence**: a read-only check of Sleep_Metrics (610 rows, Jan 2022 – Sep 2023) found the
  stored date is always the wake-up day when bedtime and wake-up fall on different days.
- **Day view** shows the night that ended that morning ("last night" for today), once the
  morning's export has been imported.
- **Week / Month** include the nights whose wake-up day falls in the period.
- **Naps**: Health Auto Export folds a day's naps into that date's single row, so there is
  never more than one row per date.
- **Total of 0** counts as no data (a gap), not as zero sleep. 399 rows currently have a total
  of 0 (a known backfill item).
- **Correlations (Explore)**: "sleep" on a date is the night before it, so sleep against
  same-day HRV compares a night with the day that follows it.

### Goals

| Goal | Value |
|---|---|
| Steps | 10,000 per day |
| Protein | 140 g per day |
| Sleep | 7 hours per night |
| Water | 3 litres per day |

Goals live in a backend constants file, because the backend computes goal hit rates and
streaks. Moving them to Settings later needs a new worksheet, which is a Sheet structure change
and needs explicit approval.

## Backend design

- **Combined daily table**: one row per date with every metric as a column, built in the backend
  from the existing services. Workouts and HR notifications are rolled up per day, and sleep is
  placed by the sleep-date rule above. No Sheet changes are needed.
- `GET /health/dashboard/summary?period=day|week|month&date=YYYY-MM-DD` returns the period's
  values, the previous period's values, per-day series for the small charts, coverage counts
  and highlights.
- A `DashboardService` in `app/modules/health/dashboard/` holds the combining rules above and
  reads through the existing services, following API → Service → Repository. Goals are in
  `goals.py` in the same module.
- A 60-second in-memory cache inside the dashboard service only, because each request reads
  whole worksheets. Edits made on the log pages show on Overview within a minute.

## Frontend design

- The page stays at `/`; the navigation label changes from "Dashboard" to "Overview".
- Charts are hand-written SVG (daily bars with gaps, a stacked bar, a sparkline). Explore will
  probably need Recharts.
- Icons come from `lucide-react`, which the app already uses.

## Decisions

All open decisions are settled (November 2026): goals, sleep date, chart library, Day-view
activity bars, "Data through" as a date, highlights from stored data only, the 60-second cache,
and the endpoint and navigation names. Details are in the sections above.

## Explore page (later)

- **Trends**: pick metrics and a range; show daily values plus a 7-day average, with your normal
  range shaded; overlay two metrics; weekday patterns.
- **Correlations**: a heatmap of metric pairs (Spearman) with click-through to a scatter plot;
  a lag setting (same day, next day, +2 days, +7 days); sample size shown; pairs with fewer
  than ~20 shared days hidden.
- **Insights**: a short automatic list of the strongest relationships, labelled as
  "worth a look", not proven.
- Endpoints: `GET /analytics/daily?from=&to=&metrics=` and
  `GET /analytics/correlations?from=&to=&lag=`.
