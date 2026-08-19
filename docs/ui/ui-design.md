# UI Design

This document captures the UX and UI decisions for the Personal Assistant application.

The goal is to create a clean, modern, mobile-first interface that is enjoyable to use every day.

---

# Design Principles

The application should follow these principles throughout.

## Mobile First

The application will be designed for mobile devices first.

Desktop and tablet layouts will naturally expand from the mobile design using responsive layouts.

There will be a single responsive UI rather than separate mobile and desktop applications.

---

## Fast Daily Logging

The application will be used every day.

The most common tasks should require the least amount of effort.

Information that is entered frequently should always be easy to access.

---

## Clean and Minimal

The UI should focus on clarity rather than decoration.

Design inspiration includes:

- Apple Health
- Notion
- Linear

The application should use:

- Plenty of whitespace
- Clear typography
- Rounded cards
- Minimal colours
- Simple icons
- Consistent spacing

---

## Progressive Disclosure

The user should never feel overwhelmed.

Only the most important information should be immediately visible.

Additional details should appear only when required.

---

# Log Today Page

## Overall Layout

The Log Today page will use **collapsible cards**.

The Daily Summary will always remain visible.

All other sections can be expanded or collapsed.

```text
Header

Daily Summary

▶ Workout

▶ Body

▶ Activity

▶ Nutrition

▶ Hydration

▶ Sleep

▶ Notes

Save Button
```

### Why this approach?

Pros:

- Cleaner interface
- Less scrolling
- Better mobile experience
- Scales well as additional fields are added in future versions

---

# Header

## Layout

```text
Log Today

◀  Friday, 15 August  ▶

✓ Saved
```

---

## Behaviour

### Date Navigation

The previous and next arrows navigate between Daily Logs.

```text
◀ Previous Day

Current Day

Next Day ▶
```

Selecting another day immediately loads that day's Daily Log.

---

### Date Selection

Tapping the date opens the calendar picker.

Example:

```text
◀ Friday, 15 August ▶
```

---

### Save Status

The header displays the current save status.

Possible states include:

- ✓ Saved
- ● Unsaved Changes
- Saving...
- Save Failed

The save status updates automatically based on user actions.

---

# Daily Summary

## Purpose

The Daily Summary provides a quick overview of today's progress.

It answers the question:

> "How am I doing today?"

The Summary is **always visible** and is **not collapsible**.

Users do not edit values directly in the Summary. It is a read-only dashboard that displays information entered elsewhere on the page.

---

## Mobile Layout

```text
Today's Summary

┌─────────────┐ ┌─────────────┐
│ ⚖️ Weight   │ │ 💪 Protein  │
│ 79.5 kg     │ │110 /130 g   │
│ ██████░░░░  │ │████████░░   │
└─────────────┘ └─────────────┘

┌─────────────┐ ┌─────────────┐
│ 💧 Water    │ │ 😴 Sleep    │
│2.8 /3.0 L   │ │7h 42m       │
│█████████░   │ │███████░░░   │
└─────────────┘ └─────────────┘

┌─────────────┐ ┌─────────────┐
│ 👣 Steps    │ │ 🔥 Calories │
│10,452       │ │620 kcal     │
│██████████   │ │             │
└─────────────┘ └─────────────┘
```

The cards are displayed as a **2 × 3 grid** on mobile devices.

On larger screens, the cards will automatically reflow to make better use of the available space.

---

## Metrics

The Daily Summary displays the following six metrics:

- ⚖️ Weight
- 💪 Protein
- 💧 Water
- 😴 Sleep
- 👣 Steps
- 🔥 Calories Burnt

---

## Progress Bars

The following metrics display progress towards a goal:

| Metric | Goal |
|---------|------|
| ⚖️ Weight | Target Weight |
| 💪 Protein | Daily Protein Goal |
| 💧 Water | Daily Water Goal |
| 😴 Sleep | Daily Sleep Goal |
| 👣 Steps | 10,000 Steps |

Calories Burnt is displayed as an informational metric and does not include a progress bar.

---

## Goal Calculations

The Summary calculates progress as follows:

- **Weight** – Progress from the starting weight towards the target weight.
- **Protein** – Current protein consumed ÷ daily protein goal.
- **Water** – Current water consumed ÷ daily water goal.
- **Sleep** – Current sleep duration ÷ daily sleep goal.
- **Steps** – Current steps ÷ 10,000 (capped at 100%).

---

## Future Enhancements

For V1, the goals may use sensible default values.

In a future version, all goals will be configurable through the **Settings** module so each user can personalise the Summary based on their own targets.

# Workout

## Purpose

The Workout section captures all workout-related information for the selected day.

It is the most frequently used section of the Daily Log and is designed to make workout entry as quick and intuitive as possible.

The Workout section is **collapsible**.

---

## Collapsed State

When collapsed, the section displays a quick summary of the workout.

Example:

```text
🏋️ Workout

HIIT • 58 min • 620 kcal
```

This allows the user to quickly understand the workout without expanding the section.

---

## Expanded Layout

```text
🏋️ Workout

────────────────────────

Workout Type

[ HIIT ▼ ]

────────────────────────

Duration            Calories Burnt

[ 58 min ]          [ 620 kcal ]

Volume              Sets

[14,525 kg]         [98]

Average Heart Rate

[140 bpm]

────────────────────────

Workout Summary

┌──────────────────────────┐
│ Battle Rope - 5 min      │
│ Rowing - 1.25 km         │
│ Push-ups - 70            │
│ ...                      │
└──────────────────────────┘
```

---

## Layout

The Workout section is divided into three logical groups.

### Workout Type

Allows the user to select the workout type.

Example:

- HIIT
- Strength
- Cardio
- Mobility
- Rest

---

### Workout Metrics

Displays the key workout metrics.

Fields:

- Duration
- Calories Burnt
- Volume
- Sets
- Average Heart Rate

Related fields are displayed on the same row to reduce vertical scrolling.

Example:

```text
Duration            Calories Burnt

[58]                [620]

Volume              Sets

[14525]             [98]
```

Average Heart Rate is displayed on its own row.

---

### Workout Summary

A multi-line text area used to capture the workout performed.

This section allows the user to record exercises, distances, repetitions or any other workout notes.

---

## Mobile Layout

The Workout section is optimised for mobile devices.

- Workout Type occupies a full row.
- Duration and Calories Burnt share one row.
- Volume and Sets share one row.
- Average Heart Rate occupies a full row.
- Workout Summary occupies the remaining width.

---

## Desktop Layout

The same logical layout is maintained.

Additional horizontal space is used to provide larger inputs and increased spacing between fields.

---

## Future Enhancements

The Workout Summary may eventually be populated automatically from:

- Apple Health
- Workout templates
- AI-generated workout summaries
- Voice input

The overall layout should remain unchanged as these capabilities are added.


# Body

## Purpose

The Body section captures the user's daily body measurements.

For V1, only **Weight** is recorded since it is the only body metric tracked daily.

The Body section is **collapsible**.

---

## Collapsed State

When collapsed, the section displays the current weight.

Example:

```text
⚖️ Body

79.5 kg
```

---

## Expanded Layout

```text
⚖️ Body

Current Weight

[ 79.5 kg ]
```

---

## Layout

The Body section contains a single field.

### Current Weight

Allows the user to enter their current body weight.

---

## Mobile Layout

The section occupies the full width of the screen.

The weight input spans the available width to make editing easy on mobile devices.

---

## Desktop Layout

The same layout is retained.

The additional screen width simply provides a larger input field.

---

## Future Enhancements

Additional body measurements will not be added to the Daily Log.

Instead, they will belong to the dedicated **Body Measurements** module.

Examples include:

- Body Fat %
- Muscle Mass
- Waist
- Chest
- Arms
- Thighs
- Progress Photos

Keeping these measurements separate ensures the Daily Log remains quick and simple to complete.



# Activity

## Purpose

The Activity section captures whole-day activity metrics.

These values are separate from the Workout section because they represent activity across the entire day rather than only the workout session.

The Activity section is **collapsible**.

---

## Collapsed State

When collapsed, the section displays a quick summary.

Example:

```text
🚶 Activity

10,452 steps • 2,450 kcal
```

---

## Expanded Layout

```text
🚶 Activity

Steps

[ 10,452 ]

────────────────────────

Total Calories Burnt

[ 2,450 ]
```

---

## Metrics

The Activity section contains two fields for V1.

### Steps

The total number of steps completed during the day.

### Total Calories Burnt

The total calories burnt across the entire day.

This is different from **Workout Calories Burnt**, which represents only calories burnt during the workout session.

---

## Mobile Layout

Both fields occupy the full available width and are stacked vertically.

This keeps the section simple and easy to edit on a mobile device.

---

## Desktop Layout

The same structure can be retained or the two fields may be displayed side-by-side if additional horizontal space is available.

---

## Future Enhancements

Activity metrics may eventually be populated automatically from Apple Health or another health data source.

Future metrics could include:

- Active Calories
- Walking / Running Distance
- Floors Climbed
- Exercise Minutes

These should only be added if they provide useful information without making the Daily Log unnecessarily complex.

# Nutrition

## Purpose

The Nutrition section captures the user's meals and nutritional intake for the selected day.

The Nutrition section is **collapsible**.

Unlike the Daily Summary, this section is intended for data entry rather than displaying progress.

---

## Collapsed State

When collapsed, only the section title is displayed.

Example:

```text
🍽️ Nutrition
```

---

## Expanded Layout

```text
🍽️ Nutrition

Meals

────────────────────────

Breakfast

┌──────────────────────────┐
│                          │
└──────────────────────────┘

Lunch

┌──────────────────────────┐
│                          │
└──────────────────────────┘

Dinner

┌──────────────────────────┐
│                          │
└──────────────────────────┘

Snacks

┌──────────────────────────┐
│                          │
└──────────────────────────┘

────────────────────────

Nutrition

Protein            Carbs

[110]              [130]

Fat                Fibre

[65]               [30]

Sugar              Calories

[12]               [2100]
```

---

## Layout

The Nutrition section is divided into two logical groups.

### Meals

The meals group contains four multi-line text areas.

- Breakfast
- Lunch
- Dinner
- Snacks

These fields allow the user to record the food consumed during the day.

---

### Nutrition Metrics

The nutrition metrics group contains the following fields:

- Protein
- Carbs
- Fat
- Fibre
- Sugar
- Calories Consumed

Related fields are displayed side-by-side to reduce vertical scrolling.

Example:

```text
Protein            Carbs

[110]              [130]

Fat                Fibre

[65]               [30]

Sugar              Calories

[12]               [2100]
```

---

## Mobile Layout

- Meal text areas occupy the full available width.
- Nutrition metrics are displayed as two columns.
- The layout is optimised for quick data entry with minimal scrolling.

---

## Desktop Layout

The same logical layout is retained.

Additional horizontal space is used to provide larger text areas and increased spacing between fields.

---

## Future Enhancements

Future versions may support:

- Automatic nutrition calculation from meals.
- AI-generated meal summaries.
- Barcode scanning.
- Photo-based meal recognition.
- Integration with nutrition databases.

The overall layout should remain unchanged as these capabilities are added.

# Hydration

## Purpose

The Hydration section captures the user's daily water intake.

For V1, only water intake is tracked since it is the primary hydration metric recorded each day.

The Hydration section is **collapsible**.

---

## Collapsed State

When collapsed, only the section title is displayed.

Example:

```text
💧 Hydration
```

---

## Expanded Layout

```text
💧 Hydration

Water

[ 2,800 ml ]
```

---

## Layout

The Hydration section contains a single field.

### Water

Allows the user to enter the total amount of water consumed during the day.

The value is entered in **millilitres (ml)**.

---

## Mobile Layout

The water input occupies the full available width to make editing easy on mobile devices.

---

## Desktop Layout

The same layout is retained.

Additional horizontal space simply provides a larger input field.

---

## Future Enhancements

Future versions may support additional hydration metrics such as:

- Coffee
- Tea
- Soft Drinks
- Alcohol
- Electrolytes

These should only be introduced if they provide meaningful value while keeping the Daily Log quick and simple to complete.

# Sleep

## Purpose

The Sleep section captures the user's sleep timings for the selected day.

For V1, only the sleep start time and sleep end time are recorded.

The Sleep section is **collapsible**.

---

## Collapsed State

When collapsed, only the section title is displayed.

Example:

```text
😴 Sleep
```

---

## Expanded Layout

```text
😴 Sleep

Sleep Start

[ 11:15 PM ]

Sleep End

[ 07:57 AM ]
```

---

## Layout

The Sleep section contains two fields.

### Sleep Start

Allows the user to enter the time they went to sleep.

### Sleep End

Allows the user to enter the time they woke up.

---

## Mobile Layout

Both fields occupy the full available width and are stacked vertically.

This keeps the section simple and easy to edit on mobile devices.

---

## Desktop Layout

The same layout is retained.

The additional screen width simply provides larger input controls and improved spacing.

---

## Relationship with Daily Summary

The Sleep section is used only for data entry.

The **Daily Summary** is responsible for calculating and displaying the total sleep duration and progress towards the daily sleep goal.

This keeps editing separate from reporting.

---

## Future Enhancements

Future versions may support automatic synchronisation with Apple Health or other wearable devices.

Additional sleep metrics could include:

- Sleep Duration
- Sleep Quality
- Time in Bed
- REM Sleep
- Deep Sleep
- Sleep Score

These metrics belong to a dedicated Sleep module and should not increase the complexity of the Daily Log.

# Notes

## Purpose

The Notes section allows the user to record any additional information that does not naturally belong in the other sections of the Daily Log.

The Notes section is **collapsible**.

---

## Collapsed State

When collapsed, only the section title is displayed.

Example:

```text
📝 Notes
```

---

## Expanded Layout

```text
📝 Notes

Notes

┌────────────────────────────────┐
│                                │
│                                │
│                                │
│                                │
└────────────────────────────────┘
```

---

## Layout

The Notes section contains a single multi-line text area.

The text area allows the user to record any observations, reminders or comments about the day.

Examples include:

- Knee felt better today.
- Had low energy during the workout.
- Tried a new pre-workout.
- Felt stronger than usual.
- Slept poorly due to travel.

The Notes field is intentionally unstructured to allow maximum flexibility.

---

## Mobile Layout

The Notes text area occupies the full available width.

It should provide sufficient height to comfortably enter multiple lines of text without feeling cramped.

---

## Desktop Layout

The same layout is retained.

Additional horizontal space simply provides a larger text entry area.

---

## Future Enhancements

Future versions may support:

- AI-generated daily summaries.
- Voice-to-text note entry.
- Rich text formatting.
- Tags or categories.
- Search across historical notes.

The Notes section should remain simple and lightweight so that users can quickly capture thoughts without interrupting their daily logging workflow.

# Save Action Bar

## Purpose

The Save Action Bar provides the primary action for saving the Daily Log.

Unlike the other sections, it is **always visible** by remaining fixed to the bottom of the screen.

This ensures the user can save their changes at any time without needing to scroll to the bottom of the page.

---

## Layout

```text
────────────────────────────────

      [ Save Changes ]

────────────────────────────────
```

The Save Action Bar remains visible regardless of the user's scroll position.

---

## Behaviour

The Save button changes its appearance based on whether there are unsaved changes.

### Saved State

When there are no unsaved changes:

- The button is disabled.
- The button displays:

```text
✓ Saved
```

---

### Unsaved Changes

When the user edits any field:

- The button becomes enabled.
- The button displays:

```text
Save Changes
```

Selecting the button saves the Daily Log.

---

### After Saving

After a successful save:

- The button returns to the disabled state.
- The text changes back to:

```text
✓ Saved
```

---

## Mobile Layout

The Save Action Bar is fixed to the bottom of the screen.

It spans the full width of the display.

The button occupies most of the available width, making it easy to tap with one hand.

---

## Desktop Layout

The Save Action Bar remains fixed to the bottom of the browser window.

The button is centred and constrained to a comfortable maximum width.

---

## Future Enhancements

Future versions may include:

- Saving... state while a save is in progress.
- Save Failed state with retry support.
- Last Saved timestamp.
- Automatic background saving.

For V1, the Save Action Bar focuses on providing a simple, reliable and always-accessible save experience.