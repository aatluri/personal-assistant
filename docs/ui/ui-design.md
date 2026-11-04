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

# Save Action Bar

## Purpose

The Save Action Bar provides the primary action for saving the current page's data.

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

Selecting the button saves the page's changes.

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