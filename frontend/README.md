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

## Frontend Setup

### Prerequisites

- Node.js (v20 or later recommended)
- npm

---

### First Time Setup

#### 1. Navigate to the Frontend Directory

From the project root:

```bash
cd frontend
```

---

#### 2. Install Dependencies

```bash
npm install
```

This installs all packages listed in `package.json`.

---

#### 3. Start the Development Server

```bash
npm run dev
```

Vite will start the development server.

Example output:

```text
VITE v8.x.x ready in xxx ms

➜  Local:   http://localhost:5173/
```

---

#### 4. Verify the Frontend

Open your browser and navigate to:

```
http://localhost:5173
```

The application should load successfully.

---

#### 5. Frontend–Backend Communication

The frontend communicates with the FastAPI backend.

Before using the application, ensure the backend server is also running.

From the `backend` directory:

```bash
fastapi dev app/main.py
```

The backend should be available at:

```
http://127.0.0.1:8000
```

The frontend uses this API to load and save data.



## Project Structure

```text
frontend/
│
├── src/
│   ├── api/           # Functions responsible for communicating with the backend APIs.
│   ├── components/    # Reusable UI components shared across multiple pages.
│   ├── layouts/       # Shared application layouts (e.g. AppShell).
│   ├── navigation/    # Navigation configuration used by the application.
│   ├── pages/         # Individual application pages and their page-specific components.
│   ├── types/         # Shared TypeScript interfaces and type definitions.
│   ├── utils/         # Helper functions used throughout the application.
│   ├── App.tsx        # Configures routing and loads the application layout.
│   └── main.tsx       # Application entry point that bootstraps React.
│
├── public/            # Static assets served directly by Vite.
├── package.json       # Project dependencies and npm scripts.
├── tsconfig.json      # TypeScript compiler configuration.
├── vite.config.ts     # Vite build and development server configuration.
└── README.md          # Frontend documentation.
```
---

## Front End Flow

The following sequence describes what happens from the moment the user opens the application until a Daily Log is saved.

```text
User opens:
http://localhost:5173/log-today
        │
        ▼
main.tsx
(Bootstraps React)
        │
        ▼
App.tsx
(Configures Routes)
        │
        ▼
AppShell.tsx
(Shared Layout & Navigation)
        │
        ▼
LogToday.tsx
(Page State & Business Logic)
        │
        ▼
api/health.ts
(Calls Backend APIs)
        │
        ▼
Backend
        │
        ▼
LogToday.tsx
(Updates React State)
        │
        ▼
Shared Components
(TextInput, Cards, Buttons...)
        │
        ▼
Tailwind CSS
(index.css + component classes)
        │
        ▼
Browser UI
```
#### Example Workflow - Loading the Log Today Page

Assume the user opens:

```text
http://localhost:5173/log-today
```

The following sequence describes what happens inside the frontend before the page is displayed.

1. **React starts the application**
   - **File:** `src/main.tsx`
   - React bootstraps the application by rendering the root `App` component into the browser.

2. **Application routing is configured**
   - **File:** `src/App.tsx`
   - React Router examines the requested URL (`/log-today`) and determines which page should be loaded.

3. **The shared application layout is loaded**
   - **File:** `src/layouts/AppShell.tsx`
   - The shared layout is rendered, including the desktop sidebar, mobile navigation, and the main content area where pages are displayed.

4. **The Log Today page is loaded**
   - **File:** `src/pages/LogToday/LogToday.tsx`
   - React Router loads the `LogToday` component because the URL matches `/log-today`.

5. **The page state is initialized**
   - **File:** `LogToday.tsx`
   - The page creates its React state using `useState()`.
   - This includes `selectedDate`, `dailyLog`, `isLoading`, `isDirty`, and `saveStatus`.

6. **The Daily Log is requested**
   - **File:** `LogToday.tsx`
   - The `useEffect()` hook runs automatically when the page loads.
   - Since `selectedDate` is initialized to today's date, it calls:
     ```text
     getDailyLog(selectedDate)
     ```

7. **The frontend calls the backend**
   - **File:** `src/api/health.ts`
   - The `getDailyLog()` function sends:
     ```text
     GET /health/daily-logs/{selectedDate}
     ```
   - to the backend.

8. **The backend returns the Daily Log**
   - The backend retrieves the record from Google Sheets and returns it as a JSON response.

9. **The page state is updated**
   - **File:** `LogToday.tsx`
   - If a Daily Log exists:
     - `setDailyLog()` stores the returned data in the page state.
   - Otherwise:
     - `createEmptyDailyLog()` creates an empty Daily Log for the selected date.

10. **React re-renders the page**
    - Since the `dailyLog` state has changed, React automatically re-renders the page.

11. **The page passes data to each section**
    - **File:** `LogToday.tsx`
    - The `dailyLog` state is passed to each page section, for example:
      - `BodySection`
      - `WorkoutSection`
      - `NutritionSection`
      - `HydrationSection`
      - `SleepSection`
      - `NotesSection`

12. **Each section renders its portion of the UI**
    - **Files:** `src/pages/LogToday/components/*`
    - Each section displays only the fields it is responsible for.
    - When the user edits a value, the section updates the shared `dailyLog` state using `setDailyLog()`.

13. **Shared UI components are rendered**
    - **Files:** `src/components/*`
    - Reusable components such as `TextInput`, `Select`, `Button`, `CollapsibleCard`, `PageContainer`, and `SaveButton` render the application's user interface.

14. **Tailwind CSS styles the page**
    - **Files:** `src/index.css` and the Tailwind `className` values defined throughout the components.
    - Tailwind applies the styling that determines the final appearance of the page.

15. **The completed page is displayed**
    - The fully rendered **Log Today** page is now visible to the user and ready for interaction.

#### Example Workflow - Saving the Daily Log

Assume the user updates a few fields and clicks **Save**.

The following sequence describes what happens inside the frontend until the data is persisted.

1. **The user updates a value**
   - **Files:** `src/pages/LogToday/components/*`
   - For example, the user changes the Workout Duration.
   - The component's `onChange()` handler is triggered.

2. **The shared page state is updated**
   - **File:** `src/pages/LogToday/LogToday.tsx`
   - The component calls `updateDailyLog()`.
   - `updateDailyLog()` updates the `dailyLog` state.
   - The page is marked as dirty (`isDirty = true`) indicating there are unsaved changes.

3. **React re-renders the page**
   - The updated value is immediately reflected in the UI.
   - The Save button becomes enabled.

4. **The user clicks Save**
   - **Files:**
     - `src/components/SaveButton.tsx`
     - `src/pages/LogToday/LogToday.tsx`
   - `SaveButton` executes the `onClick` callback provided by `LogToday`.
   - `handleSaveDailyLog()` is executed.

5. **The frontend calls the backend**
   - **File:** `src/api/health.ts`
   - `saveDailyLog(selectedDate, dailyLog)` sends:
     ```text
     PUT /health/daily-logs/{selectedDate}
     ```
   - The current `dailyLog` object is sent in the request body.

6. **The backend saves the Daily Log**
   - The backend updates the existing record or creates a new one if it does not already exist.

7. **The save completes**
   - **File:** `src/pages/LogToday/LogToday.tsx`
   - The save status is updated to `"saved"`.
   - `isDirty` is reset to `false`.
   - The Save button changes to **"✓ All Changes Saved"**.

---

## Frontend Styling

The frontend primarily uses **Tailwind CSS classes directly inside React components**.

This means most visual changes are made in the component that renders that part of the UI rather than in a separate CSS file.

#### Global Styling

**File:**

```text
src/index.css
```

Use this file for styles that apply to the application globally, such as:

- Tailwind setup/imports
- Global page defaults
- Base HTML/body styling

Most component-specific styling should not be added here.

---

#### Page Layout

**File:**

```text
src/components/PageContainer.tsx
```

Controls the overall page appearance, including:

- Page background
- Maximum content width
- Horizontal padding
- Vertical page padding

If the whole application feels too wide, narrow, or needs a different page background, start here.

---

#### Application Navigation / Shell

**File:**

```text
src/layouts/AppShell.tsx
```

Controls:

- Desktop sidebar
- Mobile bottom navigation
- Main content area
- Navigation borders/backgrounds
- Overall application shell layout

For styling individual navigation links, see:

```text
src/components/NavigationItem.tsx
```

---

#### Cards and Collapsible Sections

**File:**

```text
src/components/CollapsibleCard.tsx
```

Controls the styling shared by sections such as:

- Workout
- Body
- Nutrition
- Sleep
- Body Measurements

This includes:

- Card border
- Background
- Border radius
- Shadow
- Header spacing
- Divider
- Icons
- Expand/collapse animation

---

#### Text Inputs

**File:**

```text
src/components/TextInput.tsx
```

Controls styling for standard input fields throughout the application.

Examples:

- Weight
- Protein
- Water
- Body measurements
- Numeric fields

Changing the input height, border, focus style, font size, or padding here affects all `TextInput` fields.

---

#### Text Areas

**File:**

```text
src/components/TextArea.tsx
```

Controls styling for larger text-entry fields such as:

- Workout Summary
- Meals
- Notes

---

#### Select / Dropdown Fields

**File:**

```text
src/components/Select.tsx
```

Controls the styling of dropdowns such as Workout Type.

---

#### Buttons

**File:**

```text
src/components/Button.tsx
```

Controls the base styling used by reusable buttons, including:

- Primary blue color
- Hover state
- Disabled state
- Button height
- Rounded corners
- Press animation

---

#### Save Action Bar

**File:**

```text
src/components/SaveButton.tsx
```

Controls the fixed Save area shown at the bottom of logging pages.

This includes:

- Sticky positioning
- Background
- Top border
- Shadow
- Spacing around the Save button

The actual button appearance comes from `Button.tsx`.

---

#### Mobile More Menu

**File:**

```text
src/components/MoreMenu.tsx
```

Controls the styling of the mobile bottom sheet shown when the user selects **More**.

---

#### Page-Specific Styling

Some styling belongs only to a particular page or section and therefore lives directly in that component.

Examples:

```text
src/pages/LogToday/components/DateSection.tsx
src/pages/LogToday/components/WorkoutSection.tsx
src/pages/LogBodyMeasurements/components/BodyMeasurementsSection.tsx
```

If a visual change should affect only one section, change the Tailwind classes in that specific component rather than modifying a shared component.