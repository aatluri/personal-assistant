# Dashboard design: Overview and Explore

Status: **Overview built** (November 2026; Explore not started). Visual mockup:
[`overview-mockup.html`](overview-mockup.html) (open it in a browser; all numbers are sample
data). The mockup is the original sketch: the built page also has a date picker on the period
label, a Today button and a Refresh button, and shows highlights as goal rings and record badges
rather than the mockup's chips.

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

- `Day | Week | Month` segmented control, plus ‹ › arrows to step through periods, from the first
  period with data (`data_from`) up to the current one.
- Clicking the period label opens the browser's date picker (limited to `data_from` … today).
  Picking any date shows the day, week or month containing it, so distant periods are one pick
  away. A **Today** button, shown only away from the current period, returns to it.
- Calendar periods: Mon–Sun weeks, calendar months. A current period shows "so far"
  ("Week so far · 4 of 7 days").
- "Data through …" shows the latest date that has any data (a date, no time), because imports
  run behind real time. The exact import time is not read back from the Sheet.

### Layout (top to bottom)

1. **Highlights** (goal rings and record badges): goal progress (Day), or goal hit rates, a step streak and bests for the
   period (Week/Month). See Highlights below.
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

- Days with no data are shown as gaps, never as zeros, and averages ignore them. A recorded 0
  also counts as no data for steps, sleep, calories, water, the recovery values and body values
  (weight, body fat, waist): none of these is ever really 0.
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

### Highlights

The rules live in their own file, `backend/app/modules/health/dashboard/highlights.py`, because
they are the part most likely to change. Each highlight is a small rule function; `DAY_RULES` and
`PERIOD_RULES` list them in display order, so adding, removing or reordering one is a one-line
change. **Every highlight that has data is shown** (there is no limit), and a rule with no data
shows nothing (never "0/0").

The backend writes every part of a highlight: a **topic** (`steps`, `sleep`, `protein`, `water`,
`streak`, `best`), a **value** (e.g. `12/31`, `8h 00m`, `5 days`), a **caption** and optional
**detail** (e.g. `days ≥ 10k steps`; `best sleep` · `May 14`), **progress** (0–1 for goals, none
for records), whether the **goal was met**, and the whole highlight as a **sentence** (the
wording below, used as its name for screen readers). The page only draws them, in two groups:

- **Goal rings** (highlights with progress: Day goal progress, Week/Month hit rates): a ring filled
  to the share completed, with the percentage inside, the value, and the caption with a small
  topic icon (steps teal, sleep purple, protein amber, water blue) below. The ring's colour shows
  how complete the goal is, by the percentage shown in the ring (rounded):

  | Completion | Colour |
  |---|---|
  | 0% | empty ring, red "0%" |
  | above 0, up to 30% | red |
  | above 30, up to 50% | orange |
  | above 50, up to 70% | amber |
  | above 70, up to 90% | light green |
  | above 90% | green |

  A fully met goal (the day's goal reached, or met on every day) shows a tick instead of the
  percentage. The bands are `COMPLETION_BANDS` in
  `frontend/src/pages/Overview/components/Highlights.tsx`.
- **Record badges** (highlights without progress: the step streak and the bests): gold pills,
  "caption · **value** · detail", with a flame for the streak and a medal for bests.

Both groups wrap onto more lines when needed; an empty group is left out.

| View | Highlights, in order (as sentences) |
|---|---|
| Day | `Steps 8,240 of 10,000`, `Protein 92 of 140 g`, `Water 2.1 of 3 L`, `Sleep 7h 12m · goal 7h met` |
| Week / Month | Goal hit rates over days with data: `Steps goal met 5 of 7 days`, `Protein goal met 3 of 4 logged days`, `Sleep goal met 2 of 4 nights`, `Water goal met 3 of 5 days`; then the step streak; `Best sleep Tue · 7h 48m`; `Most steps Sat · 14,320`; `Furthest workout · Outdoor Run 8.2 km on Oct 18` |

- **Step streak**: consecutive days reaching the steps goal; a day with no data breaks it. A
  period in progress shows the current streak, ending on its last day with data
  (`10k steps · 2-day streak`); a finished period shows its longest
  (`Longest 10k streak · 6 days`). Not shown below 2 days.
- **Bests** need at least two days to compare. On a tie, the earlier day wins. Days are named by
  weekday in a week ("Tue") and by date in a month ("Oct 18").
- **Furthest workout** falls back to the **longest** workout when no workout has a distance
  (e.g. only strength training).
- Only stored values are used: pace-based bests such as "best 5k" are not possible, because
  workouts have no split times.

## Backend design

- **Combined daily table**: one row per date with every metric as a column, built in the backend
  from the existing services. Workouts and HR notifications are rolled up per day, and sleep is
  placed by the sleep-date rule above. No Sheet changes are needed.
- `GET /health/dashboard/summary?period=day|week|month&date=YYYY-MM-DD&refresh=true` returns
  the period's values, what they are compared with, per-day series for the small charts,
  coverage counts, highlights, and the data range (`data_from`, `data_through`). `date` defaults
  to today; `refresh=true` reloads the cache first.
- A `DashboardService` in `app/modules/health/dashboard/` holds the combining rules above. It
  reads the worksheets through the shared cache below, which reads them through the existing
  services, following API → Service → Repository. Goals are in `goals.py` and the highlight
  rules in `highlights.py`, in the same module.
- **Cache**: each request needs all six worksheets (about 12 Sheets requests), so the full
  worksheets are kept in memory by `DataCache` (`backend/app/data_cache.py`). It is shared:
  Explore will read the same cache, and other sources (such as labs) can be added as named
  entries when a page needs them.
  - loaded in the background when the backend starts (a failure is printed, and the next
    request tries again);
  - each worksheet is read again after 12 hours;
  - every save through the API marks that worksheet as stale, so it is read again on the next
    Overview request (imports go through the API too, so they show straight away);
  - a **Refresh** button reloads everything, for edits made directly in Google Sheets;
  - every read prints a line in the backend's terminal, and `GET /health/dashboard/cache` shows
    each worksheet's state (loaded, rows, read time, expiry, stale), to check that it works.

  Only the dashboards (Overview, and later Explore) use the cache. The log pages always read the
  Sheet, because they are used for editing and must show what is actually stored.

## Frontend design

- The page is at `/` (`src/pages/Overview/`), and the navigation calls it "Overview" (it replaced
  the Dashboard placeholder). Only `src/api/dashboard.ts` calls the backend.
- Charts are hand-written, with no chart library (`src/components/charts/`): daily bars with gaps
  and a stacked bar are plain elements sized by percentage (so each bar can be a button), and the
  weight sparkline is SVG. Explore will probably need Recharts.
- Icons come from `lucide-react`, which the app already uses.

## Decisions

All open decisions are settled (November 2026): goals, sleep date, chart library, Day-view
activity bars, "Data through" as a date, highlights from stored data only (in their own file,
all shown, drawn as rings and badges), the shared 12-hour cache with Refresh, the date picker,
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
