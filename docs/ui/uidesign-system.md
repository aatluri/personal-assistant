# Design System

This document defines the visual identity of the Personal Assistant application.

The objective is to create a premium, modern and timeless design that remains consistent across all modules.

---

# Design Philosophy

The Personal Assistant is not a fitness application.

It is a personal productivity platform that will eventually include:

- Health
- Email
- Calendar
- Tasks
- Finance
- AI Assistant
- Additional personal modules

The visual design should therefore feel like a premium productivity application rather than a sports or fitness application.

---

# Design Inspiration

The design language draws inspiration from:

- Apple Health
- Notion
- Linear
- Raycast

These applications share several common characteristics:

- Clean layouts
- Excellent typography
- Plenty of whitespace
- Minimal visual clutter
- Consistent spacing
- Soft colours
- Rounded cards
- Subtle shadows

---

# Design Principles

The interface should feel:

- Modern
- Premium
- Calm
- Clean
- Fast
- Easy to scan
- Pleasant to use every day

The interface should avoid unnecessary decoration.

Every visual element should have a purpose.

---

# Design Approach

The application will use a **mobile-first responsive design**.

A single responsive UI will adapt to:

- Mobile
- Tablet
- Desktop

The layout should naturally expand on larger screens while maintaining the same visual identity.

---

# Visual Style

The overall visual style should emphasise:

- Soft backgrounds instead of pure white.
- Floating cards rather than boxed sections.
- Rounded corners.
- Subtle shadows.
- A single primary accent colour.
- Minimal use of colour.
- Clean iconography.
- Smooth but restrained animations.

The interface should feel lightweight rather than decorative.

---

# Visual Elements to Avoid

The following styles should not be used:

- Heavy gradients
- Neon colours
- Glassmorphism
- Skeuomorphic effects
- Heavy shadows
- Excessive animations

The design should prioritise clarity and longevity over visual trends.

# Spacing System

## Purpose

The application uses a consistent spacing system to create a clean, balanced and professional interface.

Consistent spacing improves readability, creates visual rhythm and ensures every page feels like part of the same application.

The Personal Assistant follows an **8px spacing system**.

---

## Base Unit

The base spacing unit is:

```text
8px
```

All margins, padding and gaps should be multiples of this value wherever practical.

---

## Standard Spacing Scale

| Size | Usage |
|------|-------|
| 4px | Very small spacing between closely related elements |
| 8px | Small spacing |
| 16px | Standard spacing between related controls |
| 24px | Internal padding inside cards |
| 32px | Space between sections |
| 48px | Large page spacing |
| 64px | Hero or major layout spacing |

---

## Card Padding

All cards should use consistent internal spacing.

Recommended padding:

```text
24px
```

This provides enough whitespace without making cards feel oversized.

---

## Section Spacing

The vertical spacing between major sections should be:

```text
32px
```

This clearly separates content while maintaining a comfortable reading flow.

---

## Form Controls

Spacing between related form fields:

```text
16px
```

Spacing between logical groups within a section:

```text
24px
```

Example:

```text
Workout Type

[ HIIT ]

────────────────────────

Duration          Calories

[58]              [620]

Volume            Sets

[14525]           [98]
```

The divider and additional spacing help visually separate logical groups.

---

## Tailwind CSS Mapping

The design system aligns naturally with Tailwind CSS.

| Tailwind Class | Spacing |
|----------------|---------|
| `p-1`, `m-1`, `gap-1` | 4px |
| `p-2`, `m-2`, `gap-2` | 8px |
| `p-4`, `m-4`, `gap-4` | 16px |
| `p-6`, `m-6`, `gap-6` | 24px |
| `p-8`, `m-8`, `gap-8` | 32px |
| `p-12`, `m-12`, `gap-12` | 48px |
| `p-16`, `m-16`, `gap-16` | 64px |

---

## Design Principle

Whitespace should be considered an important part of the interface rather than unused space.

The design should feel open, calm and easy to scan.

Wherever possible, increase whitespace before adding visual separators such as borders or lines.

# Typography

## Font Family

The application uses **Inter** as the primary font.

Reasons:

- Designed for user interfaces.
- Highly readable on mobile and desktop.
- Modern and minimal.
- Excellent support in Tailwind CSS.

---

## Font Scale

| Usage | Size | Weight |
|--------|------|--------|
| Page Title | 32px | Bold (700) |
| Section Title | 20px | Semibold (600) |
| Card Title | 16px | Semibold (600) |
| Labels | 14px | Medium (500) |
| Input Text | 16px | Regular (400) |
| Body Text | 16px | Regular (400) |
| Helper Text | 14px | Regular (400) |
| Caption | 12px | Regular (400) |

---

## Font Weights

Only the following font weights should be used:

- 400 – Regular
- 500 – Medium
- 600 – Semibold
- 700 – Bold

---

## Alignment

- Text should be left aligned.
- Numeric values inside summary cards may be centre aligned.

---

## Line Height

- Headings: 1.2
- Body Text: 1.5

---

## Design Principles

- Keep typography simple and consistent.
- Use whitespace and typography to create hierarchy instead of excessive colours or decorations.
- Minimise the number of font sizes and weights used throughout the application.

# Color Palette

## Design Principles

- Use a minimal colour palette.
- Colours should guide attention rather than decorate the interface.
- Avoid bright or saturated colours except for status indicators.

---

## Primary Colors

| Purpose | Color |
|----------|-------|
| Primary | Deep Blue |
| Background | Soft Off-White |
| Surface (Cards) | White |
| Border | Light Grey |

---

## Text Colors

| Purpose | Color |
|----------|-------|
| Primary Text | Near Black |
| Secondary Text | Medium Grey |
| Disabled Text | Light Grey |

---

## Status Colors

| Purpose | Color |
|----------|-------|
| Success | Green |
| Warning | Amber |
| Error | Red |
| Information | Primary Blue |

---

## Usage Guidelines

- Use the **Primary Blue** for primary actions, links and active states.
- Use **Green** only for successful operations (e.g. Saved).
- Use **Amber** for warnings or unsaved changes.
- Use **Red** only for errors or destructive actions.
- Keep backgrounds neutral to maintain a clean and calm interface.

---

## Future Theme Support

The colour palette should be defined using design tokens so that future themes (e.g. Dark Mode) can be introduced without changing component implementations.

# Cards

## Purpose

Cards are the primary container used throughout the application.

Each major section of the application is displayed within a card.

Examples include:

- Workout
- Body
- Activity
- Nutrition
- Hydration
- Sleep
- Notes

Cards provide visual separation while maintaining a clean and minimal interface.

---

## Visual Style

Cards should have the following appearance:

| Property | Value |
|----------|-------|
| Background | White |
| Border Radius | 16px |
| Border | 1px Light Grey |
| Shadow | Very subtle |
| Padding | 24px |

Cards should appear light and clean without excessive visual effects.

---

## Collapsed State

When collapsed, a card displays:

- Section Icon
- Section Title
- Expand / Collapse Indicator

Example:

```text
🏋️ Workout                         >
```

The entire header acts as the touch target.

---

## Expanded State

When expanded, the card displays all fields belonging to that section.

The card retains the same visual appearance while increasing its height.

---

## Interaction

### Mobile

- Entire card header is tappable.
- Large touch target.
- Smooth expand/collapse animation.

### Desktop

- Same interaction as mobile.
- Subtle hover effect to indicate interactivity.

---

## Spacing

Cards follow the application spacing system.

- Internal Padding: 24px
- Space Between Cards: 32px
- Space Between Related Fields: 16px
- Space Between Logical Groups: 24px

---

## Design Principles

- Use whitespace before borders.
- Use borders before shadows.
- Shadows should remain subtle.
- Cards should feel lightweight and uncluttered.
- All cards should maintain a consistent appearance throughout the application.

# Form Controls

## Purpose

Form controls provide a consistent way for users to enter and edit data throughout the application.

The same styles should be used across all modules to create a familiar and predictable user experience.

---

## Supported Controls

The design system includes the following controls:

- Text Input
- Number Input
- Text Area
- Select (Dropdown)
- Date Picker
- Time Picker

---

## Labels

- Labels are displayed above the control.
- Labels are left aligned.
- Labels use the standard label typography defined in the Typography section.

Example:

```text
Weight

[ 79.5 ]
```

---

## Appearance

All form controls should have a consistent appearance.

| Property | Value |
|----------|-------|
| Height | 48px (Text Inputs, Number Inputs, Selects, Date Pickers, Time Pickers) |
| Border Radius | 12px |
| Border | 1px Light Grey |
| Background | White |
| Padding | 12px Horizontal |
| Width | 100% of available space |

Text Areas should use the same styling while allowing vertical expansion.

---

## Placeholder Text

Placeholder text should:

- Use the secondary text colour.
- Clearly indicate the expected input.
- Never replace labels.

---

## Focus State

When a control receives focus:

- Border changes to the Primary colour.
- A subtle focus ring is displayed.
- No browser default outline should be shown.

---

## Disabled State

Disabled controls should:

- Use a lighter background.
- Use muted text.
- Clearly indicate that editing is not available.

---

## Error State

Validation errors should:

- Display a red border.
- Display a short error message below the control.
- Never rely on colour alone to communicate the error.

---

## Layout

- Controls occupy the full available width unless intentionally grouped.
- Related numeric fields may be displayed side-by-side.
- Labels should remain aligned for consistent scanning.

Example:

```text
Duration            Calories

[ 58 ]              [ 620 ]
```

---

## Design Principles

- Keep controls simple and familiar.
- Prioritise readability over decoration.
- Maintain consistent spacing and sizing across all controls.
- Use consistent behaviour for every input throughout the application.


# Buttons

## Purpose

Buttons represent the primary actions a user can perform within the application.

The same button styles should be used consistently across all modules.

---

## Button Types

The design system includes the following button types:

- Primary
- Secondary
- Destructive

---

## Primary Button

Used for the main action on a page.

Examples:

- Save Changes
- Create
- Submit

Appearance:

| Property | Value |
|----------|-------|
| Background | Primary Color |
| Text | White |
| Border Radius | 12px |
| Height | 48px |

---

## Secondary Button

Used for less prominent actions.

Examples:

- Cancel
- Back
- Close

Appearance:

| Property | Value |
|----------|-------|
| Background | White |
| Border | 1px Light Grey |
| Text | Primary Text |
| Border Radius | 12px |
| Height | 48px |

---

## Destructive Button

Used only for destructive actions.

Examples:

- Delete
- Remove
- Reset

Appearance:

| Property | Value |
|----------|-------|
| Background | Error Color |
| Text | White |
| Border Radius | 12px |
| Height | 48px |

---

## States

### Default

Button is enabled and ready for interaction.

### Disabled

- Muted background.
- Muted text.
- No hover effect.
- Not clickable.

### Loading

- Displays a loading spinner.
- Temporarily disabled until the action completes.

---

## Mobile Layout

Buttons should:

- Be easy to tap.
- Have a minimum height of 48px.
- Occupy the full available width for primary page actions.

---

## Desktop Layout

Buttons may size to their content unless they represent the primary action for the page.

---

## Design Principles

- Keep button styles consistent throughout the application.
- Clearly distinguish primary actions from secondary actions.
- Use destructive buttons only for irreversible actions.
- Avoid using multiple primary buttons within the same view.


# Icons

## Purpose

Icons provide visual cues that improve navigation and make the interface easier to scan.

Icons should complement the UI rather than distract from it.

---

## Icon Library

The application uses **Lucide React** as the standard icon library.

Reasons:

- Clean and modern appearance.
- Consistent design language.
- Lightweight.
- Excellent React support.

---

## Standard Size

| Usage | Size |
|--------|------|
| Default | 20px |
| Small | 16px |
| Large | 24px |

Icons should maintain consistent sizing throughout the application.

---

## Colour

- Icons should use the primary text colour by default.
- Status icons may use the corresponding status colour (Success, Warning or Error).
- Icons should not use decorative colours.

---

## Usage Guidelines

Icons should be used to:

- Identify sections.
- Indicate actions.
- Improve readability.

Examples:

- 🏋️ Workout
- ⚖️ Body
- 🚶 Activity
- 🍽️ Nutrition
- 💧 Hydration
- 😴 Sleep
- 📝 Notes

Icons should always be accompanied by text and should never be relied upon as the only way to communicate meaning.

---

## Design Principles

- Keep icon usage consistent throughout the application.
- Use icons to improve recognition, not decoration.
- Avoid mixing multiple icon libraries.
- Maintain consistent icon sizes and spacing.


# Responsive Behaviour

## Design Approach

The application follows a **mobile-first** responsive design.

The mobile experience is the primary design target, with the layout expanding naturally for tablets and desktops.

A single responsive UI will be used across all devices.

---

## Breakpoints

The application uses the standard Tailwind CSS breakpoints.

| Device | Layout |
|----------|--------|
| Mobile | Single-column layout |
| Tablet | Improved spacing with selected multi-column layouts |
| Desktop | Wider layouts with increased spacing and maximum content width |

---

## Layout Behaviour

### Mobile

- Single-column layout.
- Cards stacked vertically.
- Full-width form controls by default.
- Sticky Save Action Bar remains visible.

### Tablet

- Increased spacing.
- Selected numeric fields may be displayed side-by-side.

### Desktop

- Content is centred on the page.
- Maximum content width is applied.
- Cards remain stacked vertically.
- Numeric fields continue to use two-column layouts where appropriate.

---

## Form Controls

- Inputs occupy the full available width unless intentionally grouped.
- Related numeric fields may be displayed side-by-side.
- Touch targets remain large enough for comfortable interaction on mobile devices.

---

## Cards

Cards maintain a consistent appearance across all screen sizes.

Only spacing and width should change between devices.

---

## Design Principles

- Design for mobile first.
- Avoid creating separate mobile and desktop interfaces.
- Expand layouts only where additional screen space improves usability.
- Maintain consistent behaviour across all devices.


# Animations

## Purpose

Animations should provide visual feedback and improve the overall user experience.

Animations should feel smooth and responsive without becoming distracting.

---

## Design Principles

- Keep animations subtle.
- Prioritise responsiveness over visual effects.
- Use animations to communicate state changes.
- Avoid excessive or decorative animations.

---

## Card Expansion

Collapsible cards should animate smoothly when expanding or collapsing.

The transition should feel quick and natural.

---

## Button Interaction

Buttons should provide immediate feedback when pressed.

Examples include:

- Slight colour change.
- Subtle scale effect.
- Disabled state after activation where appropriate.

---

## Form Controls

Form controls should animate smoothly when receiving or losing focus.

Examples include:

- Border colour transition.
- Focus ring appearance.

---

## Loading States

Loading indicators should use a simple spinner.

Loading animations should be clean and unobtrusive.

---

## Save State

Transitions between save states should be smooth.

Examples:

- Save Changes
- Saving...
- ✓ Saved

The user should always understand the current save state.

---

## Hover Effects

Desktop-only hover effects may be used for interactive elements.

Examples include:

- Cards
- Buttons
- Navigation items

Hover effects should remain subtle.

---

## Animation Duration

Most UI animations should complete within **150–250 milliseconds**.

Long animations should be avoided to keep the interface responsive.

---

## Design Principles

- Every animation should communicate a purpose.
- Avoid animations that delay user interaction.
- Consistency is more important than visual complexity.