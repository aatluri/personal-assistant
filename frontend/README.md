# Frontend

## Overview

This is the React + TypeScript frontend for the Personal Assistant application.

The frontend provides the user interface for logging, viewing and managing health, nutrition and fitness data. It communicates with the FastAPI backend through REST APIs.

---

## Technology Stack

- React
- TypeScript
- Vite
- React Router
- ESLint

---

## Folder Structure

```text
frontend/
├── public/
├── src/
│   ├── assets/
│   ├── pages/
│   │   └── LogToday/
│   │       ├── LogToday.tsx
│   │       └── components/
│   │           └── LogTodayHeader.tsx
│   ├── services/
│   ├── types/
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── vite.config.ts
└── README.md
```

---

## Architecture Principles

- Build one feature at a time.
- Keep pages responsible for composing the UI.
- Keep page-specific components inside the page folder.
- Move only truly reusable components into the shared `components` folder.
- Separate UI, business logic and API communication.

## React Concepts Learned

### Components
- Components are reusable pieces of UI.
- A page is composed of multiple components.

### JSX
- JSX allows us to write HTML-like syntax inside JavaScript.

### React Router
- React Router maps URLs to page components.

### Imports
- `import` is used to use code from another file.

### Forms

#### `<input>`
- Used for single-line input.
- `type="number"` creates a numeric field.
- `type="time"` Unlike type="number" or type="text", the browser automatically provides a time picker (its appearance depends on the browser and operating system).
- `defaultValue` sets the initial value.
- `min` specifies the minimum allowed value.
- `step` controls the increment (e.g. `0.1` for decimals, `100` for increments of 100 like for water ).
Examples:
- Weight
- Calories
- Duration

#### `<select>`
- Used for dropdown lists.
- `defaultValue` specifies the initially selected option.
Example:
- Workout Type

#### `<textarea>`
- Used for multi-line text input.
- `rows` controls the initial height.
Example:
- Workout Summary
- Notes

#### `<label>`
Used to describe a form field.
A label should always be associated with an input using the `htmlFor` attribute.

```tsx
<label htmlFor="workout-duration">
    Duration
</label>
<input
    id="workout-duration"
    type="number"
/>
```
The value of `htmlFor` **must match** the `id` of the input.
This allows:
- Clicking the label to focus the input.
- Better accessibility for screen readers.


### Reusable Components

One of React's biggest strengths is the ability to build reusable UI components.

Instead of repeating the same HTML multiple times, we build the UI once and reuse it by passing different values (props).

#### Before

Without a reusable component, we would repeat the following code for every field:

```tsx
<div>
    <label htmlFor="protein">
        Protein (g)
    </label>

    <input
        id="protein"
        name="protein"
        type="number"
        min={0}
        defaultValue={110}
    />
</div>
```

The same structure would then be duplicated for:

- Carbs
- Fat
- Fibre
- Sugar
- Calories
- Weight
- Water
- etc.

---

#### After

Instead, we created a reusable `TextInput` component.

```tsx
<TextInput
    label="Protein (g)"
    id="protein"
    name="protein"
    type="number"
    min={0}
    defaultValue={110}
/>
```

The same component can now be reused for any input simply by changing the props.

Example:

```tsx
<TextInput
    label="Weight (kg)"
    id="weight"
    name="weight"
    type="number"
    step={0.1}
    defaultValue={80.3}
/>

<TextInput
    label="Water (ml)"
    id="water"
    name="water"
    type="number"
    step={100}
    defaultValue={2700}
/>
```

---

#### How Props Work

Props are similar to parameters in a JavaScript function.

JavaScript example:

```javascript
function greet(name) {
    return `Hello ${name}`;
}

greet("Adarsh");
greet("John");
```

React works in the same way.

```tsx
<TextInput label="Protein" />

<TextInput label="Carbs" />

<TextInput label="Fat" />
```

The same component behaves differently depending on the values passed to it.

---

#### How `TextInput` Works

Our reusable component accepts a custom `label` along with all normal HTML `<input>` attributes.

```tsx
interface TextInputProps
    extends InputHTMLAttributes<HTMLInputElement> {

    label: string;

}
```

By extending `InputHTMLAttributes`, the component automatically supports attributes such as:

- id
- name
- type
- min
- max
- step
- placeholder
- defaultValue
- required
- disabled

without having to define each one manually.

---

#### The Spread Operator

Inside the component we use:

```tsx
<input {...inputProps} />
```

The spread operator forwards every remaining property to the underlying HTML `<input>`.

For example:

```tsx
<TextInput
    id="weight"
    type="number"
    min={0}
    step={0.1}
/>
```

is equivalent to writing:

```tsx
<input
    id="weight"
    type="number"
    min={0}
    step={0.1}
/>
```

---

#### Reusable Components Created

Current reusable components:

```text
src/components/
├── Button.tsx
├── TextArea.tsx
└── TextInput.tsx
```

These components can be reused across multiple pages, including:

- Log Today
- Body Measurements
- Blood Work
- Settings

This avoids duplication, keeps the code consistent, and makes future maintenance much easier.


### React State (`useState`)

- State is data that React remembers.
- Updating state causes React to re-run the component.
- React compares the new UI with the previous UI and updates only the parts that changed.

Flow:

```text
User Action
      ↓
onChange
      ↓
setState(...)
      ↓
Component Re-runs
      ↓
React compares old and new UI
      ↓
Browser updates only the changed elements
```

## State Ownership

One of the core principles in React is:

> **The parent component owns the data. Child components display and update the data through props.**

This is often referred to as **lifting state up**.

### Why?

If every child component owns its own state, it becomes difficult for the parent component to access all the data.

For example, when the user clicks **Save Daily Log**, we need to send all the page data to the backend:

- Weight
- Workout
- Nutrition
- Hydration
- Sleep
- Notes

If each section owns its own state, the parent component has no easy way to collect everything.

Instead, the parent component owns the data and passes it down to the child components.

---

### Before Lifting State

```text
LogToday

    BodySection
        owns weight
```

`BodySection`

```tsx
const [weight, setWeight] = useState(80.3);
```

Only `BodySection` knows the current weight.

---

### After Lifting State

```text
LogToday
    owns weight
        │
        ▼
    BodySection
```

The state is moved to the parent.

`LogToday`

```tsx
const [weight, setWeight] = useState(80.3);
```

The parent then passes the state to the child:

```tsx
<BodySection
    weight={weight}
    setWeight={setWeight}
/>
```

The child component no longer owns the state.

Instead, it receives the current value and the function used to update it.

```tsx
interface BodySectionProps {

    weight: number;

    setWeight: Dispatch<SetStateAction<number>>;

}
```

The child uses these props when rendering the input.

```tsx
<TextInput
    label="Weight (kg)"
    value={weight}
    onChange={(event) => {

        const newWeight = Number(event.target.value);

        setWeight(newWeight);

    }}
/>
```

---

### Data Flow

```text
User types a new weight
        │
        ▼
BodySection
        │
        ▼
setWeight(...)
        │
        ▼
LogToday updates the state
        │
        ▼
React re-renders LogToday
        │
        ▼
The updated weight is passed back to BodySection
```

---

### Benefits

- A single source of truth for the page.
- The parent always has access to all form data.
- Easier to validate data before saving.
- Easier to send the complete form to the backend.
- Child components remain reusable and focused on displaying the UI.


## How the Frontend Works

The following sequence describes what happens from the moment the user opens the application until a Daily Log is saved.

```text
User opens page
        │
        ▼
main.tsx
        │
        ▼
App.tsx
        │
        ▼
React Router
        │
        ▼
LogToday.tsx
        │
        ▼
GET Daily Log
        │
        ▼
DailyLog State
        │
        ▼
Page Sections
        │
        ▼
User edits values
        │
        ▼
Save Button
        │
        ▼
PUT API
        │
        ▼
Backend
```

### 1. Application Starts

**Files involved**

- `src/main.tsx`
- `src/App.tsx`

The browser opens:

```text
http://localhost:5173
```

`main.tsx` starts the React application by rendering the `App` component.

`App.tsx` contains the application's routes. React Router examines the URL and loads the `LogToday` page.

---

### 2. LogToday Page Loads

**File involved**

- `src/pages/LogToday/LogToday.tsx`

When `LogToday` loads:

- `selectedDate` is initialized to today's date.
- `dailyLog` state is created.
- A `useEffect()` runs and requests the Daily Log for the selected date.

```text
selectedDate
        │
        ▼
GET Daily Log
```

---

### 3. Daily Log is Loaded

**Files involved**

- `src/api/health.ts`
- `src/pages/LogToday/LogToday.tsx`

The frontend calls:

```text
GET /health/daily-logs/{date}
```

If data exists:

- The backend response is converted into the frontend `DailyLog` model.
- `setDailyLog()` updates the page state.

If no data exists:

- An empty `DailyLog` is created.

The `dailyLog` state now becomes the single source of truth for the page.

---

### 4. The Page is Rendered

**Files involved**

- `src/pages/LogToday/LogToday.tsx`
- `src/pages/LogToday/components/*`

`LogToday` passes the `dailyLog` state to each section.

Example:

```tsx
<WorkoutSection
    dailyLog={dailyLog}
    setDailyLog={setDailyLog}
/>
```

Each section displays only the data it is responsible for.

---

### 5. User Updates a Value

**Files involved**

- `WorkoutSection.tsx`
- `NutritionSection.tsx`
- `BodySection.tsx`
- (and the other section components)

When the user changes a value:

- The component's `onChange()` handler is triggered.
- The component calls `setDailyLog()`.
- Only the relevant section of the `dailyLog` object is updated.
- React automatically re-renders the page with the updated values.

---

### 6. User Clicks Save

**Files involved**

- `SaveButton.tsx`
- `LogToday.tsx`

When the Save button is clicked:

- `SaveButton` calls the `onClick` function passed from `LogToday`.
- `LogToday` calls `saveDailyLog(selectedDate, dailyLog)`.

---

### 7. Daily Log is Saved

**File involved**

- `src/api/health.ts`

The API layer:

- Converts the frontend `DailyLog` model into the backend request model.
- Sends a PUT request to:

```text
PUT /health/daily-logs/{selectedDate}
```

The backend then updates (or creates) the Daily Log in Google Sheets.

---

### Summary

```text
Browser
    │
    ▼
main.tsx
    │
    ▼
App.tsx
    │
    ▼
React Router
    │
    ▼
LogToday.tsx
    │
    ▼
GET Daily Log
    │
    ▼
setDailyLog()
    │
    ▼
Page Sections
    │
    ▼
User edits values
    │
    ▼
setDailyLog()
    │
    ▼
SaveButton
    │
    ▼
saveDailyLog()
    │
    ▼
PUT API
    │
    ▼
Backend
```