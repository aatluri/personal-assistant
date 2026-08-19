# Tailwind Implementation Guidelines

## General Principles

- Follow a mobile-first approach.
- Use Tailwind CSS utility classes instead of writing custom CSS wherever possible.
- Follow the Design System for colours, spacing, typography and component styling.

---

## Responsive Design

Always implement the mobile layout first.

Enhance the layout for larger screens using Tailwind's responsive modifiers.

Example:

```tsx
className="grid grid-cols-1 md:grid-cols-2"
```

---

## Reusable Components

Prefer reusable React components over repeating Tailwind classes.

Examples:

- Card
- Button
- TextInput
- TextArea
- Select
- LoadingSpinner

If the same group of Tailwind classes appears multiple times, consider creating a reusable component.

---

## Utility Classes

Keep Tailwind utility classes organised and readable.

Group classes in the following order where practical:

1. Layout
2. Flex/Grid
3. Spacing
4. Sizing
5. Typography
6. Colours
7. Borders
8. Effects
9. Transitions

Example:

```tsx
className="
flex
items-center
justify-between
p-6
text-base
font-medium
bg-white
border
rounded-2xl
shadow-sm
"
```

---

## Spacing

Always use the spacing values defined in the Design System.

Avoid arbitrary spacing values unless there is a specific design requirement.

Preferred examples:

```text
p-2
p-4
p-6
p-8

gap-2
gap-4
gap-6
gap-8
```

---

## Colours

Use only colours defined in the Design System.

Avoid introducing new colours within individual components.

---

## Typography

Use the typography scale defined in the Design System.

Avoid arbitrary font sizes and font weights.

---

## Inline Styles

Avoid inline styles.

Prefer Tailwind utility classes whenever possible.

Use inline styles only when a value cannot reasonably be expressed using Tailwind.

---

## Semantic HTML

Use semantic HTML elements whenever appropriate.

Examples:

- `<header>`
- `<main>`
- `<section>`
- `<article>`
- `<nav>`
- `<button>`
- `<form>`
- `<label>`

Avoid unnecessary `<div>` elements where a semantic element is more appropriate.

---

## Consistency

Do not restyle components on individual pages.

Instead, reuse the shared components defined by the application.

Examples:

- Card
- Button
- TextInput
- TextArea
- Select
- LoadingSpinner

A component should have a single visual style throughout the application unless there is a documented reason to introduce a variant.