# UI Components

## Purpose

This document defines every reusable UI component used throughout the Personal Operating System.

The goal is consistency. Every page should be assembled from these components rather than creating new UI patterns.

---

# Design Principles

Every component should be:

- Reusable
- Responsive
- Accessible
- Dark Mode First
- Minimal
- Consistent

---

# Layout Components

## App Shell

### Purpose

Provides the overall application layout.

### Contains

- Sidebar
- Header
- Main Content Area

### Used In

Every page.

---

## Sidebar

### Purpose

Primary navigation.

### Navigation Items

- Dashboard
- Log Today
- Body Measurements
- Blood Work
- Workouts (Future)
- Nutrition (Future)
- Email (Future)
- Settings

### Future

Collapsible.

---

## Header

### Purpose

Displays page context.

### Contains

- Greeting
- Page Title
- Current Date
- Search (Future)
- Notifications (Future)
- User Menu

---

# Dashboard Components

## Achievement Banner

### Purpose

Celebrate the user's daily achievements.

### Example

```
🔥 Great workout today.

620 calories burned.

Day 24 / 90
```

### Props

| Property | Type |
|-----------|------|
| title | string |
| subtitle | string |
| icon | Icon |
| variant | success \| info |

---

## Metric Card

### Purpose

Display one important health metric.

### Used For

- Weight
- Protein
- Water
- Sleep
- Steps
- Calories

### Example

```
Protein

110 g

84%
```

### Props

| Property | Type |
|-----------|------|
| title | string |
| value | string |
| unit | string |
| progress | number |
| icon | Icon |
| accentColor | ThemeColor |

---

## Section Card

### Purpose

Container for one logical section.

### Examples

- Workout
- Nutrition
- Sleep
- Body

### Contains

- Title
- Icon
- Child Components

---

# Form Components

## Text Input

Used for:

- Breakfast
- Lunch
- Dinner
- Snacks
- Workout Summary

---

## Number Input

Used for:

- Weight
- Protein
- Water
- Calories
- Steps

---

## Dropdown

Used for:

- Workout Type

Future:

- Exercise Type
- Mood
- Energy

---

## Time Picker

Used for:

- Sleep Start
- Sleep End
- First Meal
- Last Meal

---

## Date Picker

Used for selecting log date.

---

## Primary Button

Purpose

Primary call-to-action.

Example

```
Save Daily Log
```

---

## Secondary Button

Examples

Cancel

Reset

Edit

---

# Feedback Components

## Success Toast

Example

```
✓ Daily Log Saved
```

---

## Loading Spinner

Shown while:

- Saving
- Syncing
- Loading Dashboard

---

## Empty State

Used when no data exists.

Example

```
No workout logged today.

Start by entering your workout.
```

---

# Data Components

## Progress Bar

Used For

- Protein
- Water
- Calories
- Challenge Progress

---

## Status Chip

Examples

```
Saved

Unsaved

Goal Achieved

In Progress
```

---

## Statistic Tile

Future dashboard component.

Displays:

- Weekly Average
- Monthly Average
- Personal Best
- Current Streak

---

# Modal Components

## Confirmation Dialog

Examples

Delete log?

Discard changes?

---

# Future AI Components

## AI Insight Card

Examples

```
Protein intake increased 15% this week.
```

---

## AI Recommendation Card

Examples

```
You averaged only 6 hours of sleep.

Try sleeping before 11 PM tonight.
```

---

# Future Charts

## Line Chart

Weight

Sleep

Calories

---

## Bar Chart

Weekly workouts

Protein

Water

---

## Calendar Heatmap

Workout streak

Daily logging

Challenge completion

---

# Component Naming Convention

Component names should be descriptive.

Examples

```
MetricCard

AchievementBanner

SectionCard

TimePicker

ProgressBar

StatusChip

PrimaryButton
```

Avoid names like:

```
Card1

CustomBox

Widget

Panel

Container2
```

---

# Component Hierarchy

```
AppShell
│
├── Sidebar
├── Header
│
└── LogToday
     │
     ├── AchievementBanner
     ├── MetricCard × 6
     ├── SectionCard
     │      ├── NumberInput
     │      ├── TextInput
     │      ├── Dropdown
     │      └── TimePicker
     │
     ├── SectionCard
     ├── SectionCard
     └── PrimaryButton
```