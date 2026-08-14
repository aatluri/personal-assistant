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

## How the Frontend Works

When the application is opened in the browser, the following sequence occurs:

```text
Browser
    │
    ▼
index.html
    │
    ▼
src/main.tsx
    │
    ▼
<App />
    │
    ▼
React Router
    │
    ▼
Selected Page
    │
    ▼
Page Components
```

### 1. Browser

The user opens:

```
http://localhost:5173
```

The browser first loads `index.html`.

---

### 2. index.html

The `index.html` file contains the root element where the React application will be rendered.

```html
<div id="root"></div>
```

Nothing is displayed yet.

---

### 3. main.tsx

`main.tsx` is the application's entry point.

Its responsibility is to start React and render the root component.

```tsx
createRoot(document.getElementById("root")!).render(
    <App />
);
```

---

### 4. App.tsx

`App.tsx` is the root component of the application.

Its responsibility is to configure application-wide features such as:

- Routing
- Authentication (future)
- Global layouts (future)

Currently it contains only the router.

---

### 5. React Router

React Router examines the current URL.

Example:

```
/
```

It matches this route:

```tsx
<Route path="/" element={<LogToday />} />
```

React Router therefore renders the `LogToday` page.

---

### 6. Page Component

The page component (`LogToday.tsx`) is responsible for assembling the page.

Example:

```
LogToday
│
├── LogTodayHeader
├── AchievementBanner
├── Scoreboard
└── ...
```

The page itself contains very little logic.

---

### 7. Child Components

Each child component is responsible for rendering one section of the page.

Example:

```
LogTodayHeader
```

renders only the page header.

```
AchievementBanner
```

renders only the achievement banner.

This keeps components small, readable and maintainable.


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

## React Rendering Flow

The following steps describe what happens when the user opens:

```
http://localhost:5173/
```

### 1. Vite serves the application

The browser loads the React application and executes `src/main.tsx`.

---

### 2. `main.tsx` renders the root component

```tsx
createRoot(document.getElementById("root")!).render(
    <App />
);
```

`App` becomes the root of the application.

---

### 3. React Router determines the page

React Router examines the URL.

```
http://localhost:5173/
```

and loads the `LogToday` page.
It knows because you mapped the / route to the LogToday component in the App.tsx file.

---

### 4. `LogToday` executes

React runs the `LogToday` component.

This component:

- Creates the `dailyLog` state using `useState()`.
- Renders all page sections.
- Passes the required data to each section as props.
- LogToday also

Example:

```tsx
<WorkoutSection
    dailyLog={dailyLog}
    setDailyLog={setDailyLog}
/>
```

---

### 5. `WorkoutSection` executes

React runs the `WorkoutSection` component.

It receives:

- `dailyLog`
- `setDailyLog`

through props.

It then displays values from the shared state.

Example:

```tsx
value={dailyLog.workoutDuration}
```

---

### 6. User changes a value

Suppose the user changes:

```
Workout Duration
58 → 60
```

The `onChange` event fires.

```tsx
setDailyLog((previousDailyLog) => ({
    ...previousDailyLog,
    workoutDuration: 60,
}));
```

React updates the `dailyLog` state.

---

### 7. React re-renders

Because the state changed:

- `LogToday` runs again.
- `WorkoutSection` runs again.
- The updated value is passed to the input.
- React updates only the changed parts of the page.

---

### Summary

```
User opens page
        │
        ▼
main.tsx
        │
        ▼
App
        │
        ▼
React Router
        │
        ▼
LogToday
        │
        ▼
Creates dailyLog state
        │
        ▼
Passes state to WorkoutSection
        │
        ▼
WorkoutSection displays the values
        │
        ▼
User changes a value
        │
        ▼
setDailyLog(...)
        │
        ▼
React re-renders the page
```

### Benefits

- A single source of truth for the page.
- The parent always has access to all form data.
- Easier to validate data before saving.
- Easier to send the complete form to the backend.
- Child components remain reusable and focused on displaying the UI.