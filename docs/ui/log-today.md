# Log Today Screen

## Purpose

The Log Today screen is the primary data entry screen for the Health module.

Unlike a traditional form, the screen is designed to celebrate the user's progress while making daily logging quick and enjoyable.

The target is for a user to complete their daily log in under **2 minutes**.

---

# Objectives

- Make logging feel rewarding rather than administrative.
- Surface today's achievements before asking for input.
- Minimize scrolling.
- Provide an Apple-quality experience.
- Support future integration with Apple Health and AI.

---

# User Flow
- Open Log Today.
- Review today's achievement banner and scoreboard.
- Enter workout details.
- Enter body metrics.
- Enter meal timing.
- Enter nutrition.
- Enter water intake.
- Enter sleep times.
- Press Save.
- See confirmation and updated scoreboard.


---

# Screen Layout

```
Header
│
├── Achievement Banner
│
├── Today's Scoreboard
│
├── Workout
│
├── Body
│
├── Meal Timing
│
├── Nutrition
│
├── Hydration
│
├── Sleep
│
└── Save Button
```

---

# Header

Displays:

- Greeting
- Current date
- Challenge Day (optional)
- Save Status

Example

```
Good Evening

Friday, July 31

Day 24 / 90

✓ Saved
```

---

# Achievement Banner

Purpose

Celebrate today's progress.

Examples

```
🔥 Great session today!

620 calories burned.

You're on Day 24 of your challenge.
```

Future versions may use AI-generated summaries.

---

# Today's Scoreboard

Displays today's most important metrics.

## Cards

### Weight

Displays

- Current Weight

Example

```
80.3 kg
```

---

### Protein

Displays

- Protein Consumed
- Goal Progress

Example

```
110 / 130 g
```

---

### Water

Displays

- Water Consumed

Example

```
2.7 L
```

---

### Sleep

Displays

- Total Sleep

Example

```
7h 42m
```

---

### Steps

Displays

- Total Steps

---

### Calories

Displays

- Calories Burned
- Calories Consumed

---

# Workout Section

Purpose

Primary focus of the page.

Fields

| Field | Editable |
|---------|----------|
| Workout Type | Yes |
| Duration | Yes |
| Calories Burnt | Yes |
| Volume | Yes |
| Sets | Yes |
| Average Heart Rate | Yes |
| Workout Summary | Yes |

Future

Automatically imported from Apple Health or Garmin.

---

# Body Section

Fields

| Field | Editable |
|---------|----------|
| Weight | Yes |

Future

Automatically update body trend charts.

---

# Meal Timing

Fields

| Field | Editable |
|---------|----------|
| First Meal Time | Yes |
| Last Meal Time | Yes |

Future

Eating Window and Fasting Window calculated automatically.

---

# Nutrition

Fields

| Field | Editable |
|---------|----------|
| Breakfast | Yes |
| Lunch | Yes |
| Dinner | Yes |
| Snacks | Yes |
| Protein | Yes |
| Carbs | Yes |
| Fat | Yes |
| Fibre | Yes |
| Sugar | Yes |
| Calories Consumed | Yes |

Future

Meal descriptions automatically converted into nutrition values using AI.

---

# Hydration

Fields

| Field | Editable |
|---------|----------|
| Water (ml) | Yes |

---

# Sleep

Fields

| Field | Editable |
|---------|----------|
| Sleep Start Time | Yes |
| Sleep End Time | Yes |

Future

Sleep duration calculated automatically.

---

# Save

Primary Button

```
Save Daily Log
```

After save

```
✓ Daily Log Saved
```

---

# Field Mapping

| UI Field | Google Sheet Column |
|-----------|---------------------|
| Weight | Weight (kg) |
| Workout Type | Workout Type |
| Workout Summary | Workout Summary |
| Workout Duration | Workout Duration (min) |
| Workout Calories | Workout Calories Burnt |
| Steps | Steps |
| Total Calories Burnt | Total Calories Burnt |
| Breakfast | Breakfast |
| Lunch | Lunch |
| Dinner | Dinner |
| Snacks | Snacks |
| Protein | Protein(g) |
| Carbs | Carbs(g) |
| Fibre | Fibre(g) |
| Fat | Fat(g) |
| Sugar | Sugar(g) |
| Calories Consumed | Calories Consumed |
| Water | Water(ml) |
| First Meal Time | First Meal Time |
| Last Meal Time | Last Meal Time |
| Sleep Start | Sleep Start Time |
| Sleep End | Sleep End Time |
| Notes | Notes |

---

# Future Enhancements

## Apple Health

Automatically populate:

- Weight
- Steps
- Sleep
- Calories Burnt
- Workout Duration

---

## AI

Generate:

- Workout summary
- Nutrition estimate
- Daily insights
- Suggestions
- Motivation

---

## Analytics

Display:

- Weekly trends
- Monthly trends
- Streaks
- Goal completion
- Personal bests

---

# Success Criteria

The screen should:

- Feel premium.
- Require fewer than 2 minutes for manual entry.
- Be usable without reading instructions.
- Scale naturally as new features are added.
- Follow the UI Design Philosophy.