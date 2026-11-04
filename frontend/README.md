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

The following sequence describes what happens from the moment the user opens a metric page until its data is saved. The Nutrition Metrics page is used as the example; the other metric pages follow the same pattern.

```text
User opens:
http://localhost:5173/nutrition-metrics
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
LogNutritionMetrics.tsx
(Page State & Business Logic)
        │
        ▼
api/nutritionMetrics.ts
(Calls Backend APIs)
        │
        ▼
Backend
        │
        ▼
LogNutritionMetrics.tsx
(Updates React State)
        │
        ▼
Shared Components
(PageHeader, DateSection, TextInput, Cards...)
        │
        ▼
Tailwind CSS
(index.css + component classes)
        │
        ▼
Browser UI
```
#### Example Workflow - Loading the Nutrition Metrics Page

Assume the user opens:

```text
http://localhost:5173/nutrition-metrics
```

The following sequence describes what happens inside the frontend before the page is displayed.

1. **React starts the application**
   - **File:** `src/main.tsx`
   - React bootstraps the application by rendering the root `App` component into the browser.

2. **Application routing is configured**
   - **File:** `src/App.tsx`
   - React Router examines the requested URL (`/nutrition-metrics`) and determines which page should be loaded.

3. **The shared application layout is loaded**
   - **File:** `src/layouts/AppShell.tsx`
   - The shared layout is rendered, including the desktop sidebar, mobile navigation, and the main content area where pages are displayed.

4. **The Nutrition Metrics page is loaded**
   - **File:** `src/pages/LogNutritionMetrics/LogNutritionMetrics.tsx`
   - React Router loads the `LogNutritionMetrics` component because the URL matches `/nutrition-metrics`.

5. **The page state is initialized**
   - **File:** `LogNutritionMetrics.tsx`
   - The page creates its React state using `useState()`.
   - This includes `selectedDate`, `nutritionMetrics`, `isLoading`, `isDirty`, `saveStatus`, and `loadError`.

6. **The Nutrition Metrics are requested**
   - **File:** `LogNutritionMetrics.tsx`
   - The `useEffect()` hook runs automatically when the page loads, and again whenever `selectedDate` changes.
   - Since `selectedDate` is initialized to today's date, it calls:
     ```text
     getNutritionMetric(selectedDate)
     ```

7. **The frontend calls the backend**
   - **File:** `src/api/nutritionMetrics.ts`
   - The `getNutritionMetric()` function sends:
     ```text
     GET /health/nutrition-metrics/{selectedDate}
     ```
   - to the backend, then converts the backend's `snake_case` fields into the frontend's `camelCase` model.

8. **The backend returns the Nutrition Metrics**
   - The backend retrieves the record from Google Sheets and returns it as a JSON response, or `404` if no record exists for that date.

9. **The page state is updated**
   - **File:** `LogNutritionMetrics.tsx`
   - If a record exists:
     - `setNutritionMetrics()` stores the returned data in the page state.
   - Otherwise:
     - `createEmptyNutritionMetrics()` creates an empty record for the selected date.

10. **React re-renders the page**
    - Since the `nutritionMetrics` state has changed, React automatically re-renders the page.

11. **The page renders its shared and page-specific components**
    - **File:** `LogNutritionMetrics.tsx`
    - `PageHeader` shows the page title and save status.
    - `DateSection` lets the user change `selectedDate`.
    - The `nutritionMetrics` state is passed to `NutritionMetricsSection`.

12. **The section renders its portion of the UI**
    - **File:** `src/pages/LogNutritionMetrics/components/NutritionMetricsSection.tsx`
    - The section displays the nutrition fields.
    - When the user edits a value, the section updates the page's `nutritionMetrics` state using `setNutritionMetrics()`.

13. **Shared UI components are rendered**
    - **Files:** `src/components/*`
    - Reusable components such as `PageHeader`, `DateSection`, `TextInput`, `CollapsibleCard`, `PageContainer`, and `SaveButton` render the application's user interface.

14. **Tailwind CSS styles the page**
    - **Files:** `src/index.css` and the Tailwind `className` values defined throughout the components.
    - Tailwind applies the styling that determines the final appearance of the page.

15. **The completed page is displayed**
    - The fully rendered **Nutrition Metrics** page is now visible to the user and ready for interaction.

#### Example Workflow - Saving Nutrition Metrics

Assume the user updates a few fields and clicks **Save**.

The following sequence describes what happens inside the frontend until the data is persisted.

1. **The user updates a value**
   - **File:** `src/pages/LogNutritionMetrics/components/NutritionMetricsSection.tsx`
   - For example, the user changes Protein.
   - The input's `onChange()` handler is triggered.

2. **The shared page state is updated**
   - **File:** `src/pages/LogNutritionMetrics/LogNutritionMetrics.tsx`
   - The section calls the `setNutritionMetrics` prop, which is the page's `updateNutritionMetrics()` function.
   - `updateNutritionMetrics()` updates the `nutritionMetrics` state.
   - The page is marked as dirty (`isDirty = true`) indicating there are unsaved changes.

3. **React re-renders the page**
   - The updated value is immediately reflected in the UI.
   - The Save button becomes enabled.

4. **The user clicks Save**
   - **Files:**
     - `src/components/SaveButton.tsx`
     - `src/pages/LogNutritionMetrics/LogNutritionMetrics.tsx`
   - `SaveButton` executes the `onClick` callback provided by `LogNutritionMetrics`.
   - `handleSaveNutritionMetrics()` is executed.

5. **The frontend calls the backend**
   - **File:** `src/api/nutritionMetrics.ts`
   - `saveNutritionMetric(selectedDate, nutritionMetrics)` sends:
     ```text
     PUT /health/nutrition-metrics
     ```
   - The current `nutritionMetrics` object, converted to the backend's field names, is sent in the request body. Empty fields are sent as `null`.

6. **The backend saves the Nutrition Metrics**
   - The backend updates the existing record or creates a new one if it does not already exist.
   - When updating, fields sent as `null` keep their existing values in the Sheet.

7. **The save completes**
   - **File:** `src/pages/LogNutritionMetrics/LogNutritionMetrics.tsx`
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
src/pages/LogNutritionMetrics/components/NutritionMetricsSection.tsx
src/pages/LogBodyMeasurements/components/BodyMeasurementsSection.tsx
```

If a visual change should affect only one section, change the Tailwind classes in that specific component rather than modifying a shared component.


## Adding a New Field to the Frontend

Assume a new Nutrition field called **Sodium (mg)** has already been exposed by the backend APIs.

The following frontend changes are required:

1. **Update the TypeScript model**
   - **File:** `src/types/NutritionMetrics.ts`
   - Add the new field to the `NutritionMetrics` interface.

2. **Update the empty model**
   - **File:** `src/utils/createEmptyNutritionMetrics.ts`
   - Add a default value for the new field.

3. **Update the API layer**
   - **File:** `src/api/nutritionMetrics.ts`
   - Map the backend field (for example `sodium_mg`) to the frontend field (for example `sodiumMg`) in both directions: when loading and when saving.
   - The frontend uses `camelCase` and the backend uses `snake_case`, so this mapping is always required.

4. **Add the field to the UI**
   - **File:** The appropriate page section.
   - Example:
     ```text
     src/pages/LogNutritionMetrics/components/NutritionMetricsSection.tsx
     ```
   - Add the corresponding `TextInput` or other UI component.

5. **Bind the field to the page state**
   - **File:** The page that owns the state.
   - Example:
     ```text
     src/pages/LogNutritionMetrics/LogNutritionMetrics.tsx
     ```

   - The page typically owns the complete model as state:
     ```tsx
     const [nutritionMetrics, setNutritionMetrics] =
         useState<NutritionMetrics>(
             createEmptyNutritionMetrics()
         );
     ```

   - If the page already passes the complete model and state updater to the appropriate section:
     ```tsx
     <NutritionMetricsSection
         nutritionMetrics={nutritionMetrics}
         setNutritionMetrics={updateNutritionMetrics}
     />
     ```
     then **no change to the page-level component is normally required** when adding another field to that existing section.

   - Once the new field has been added to:
     - the TypeScript model,
     - the empty model,
     - the API mapping, and
     - the section component,

     it automatically becomes part of the object held by the page state.

   - A change to the page-level component **is required** when:
     - the field must be passed individually to the section rather than as part of the complete model, or
     - an entirely new section/card is being added to the page.

   - For example, `LogNutritionMetrics.tsx` already passes the complete `nutritionMetrics` object to `NutritionMetricsSection`, so adding a new field such as `Sodium (mg)` inside that section does not require a change to `LogNutritionMetrics.tsx`.

   - This is the case for LogBodyMeasurments.tsx. When we added weight and body mass index, we didnt have to touch LogBodyMeasurements.tsx.

   - However, if a completely new section/card is introduced, the page component must be updated to render the new section and pass it the required state.

6. **Test the page**
   - Update the component tests to verify the new field is rendered.
   - Update the supplied-values test to verify an existing value is displayed correctly.
   - Add a test to verify changing the field correctly updates the page state.
   - Run the affected component test suite.
   - Run the complete frontend test suite to ensure existing functionality is not affected.
   - Manually verify the field loads correctly from the backend.
   - Manually change and save the value.
   - Reload the page and confirm the saved value is persisted.


## Adding a New Page

Assume we want to add a new page called **Body Measurements**.

The following frontend changes are required:

1. **Create the TypeScript model**
   - **File:**
     ```text
     src/types/BodyMeasurements.ts
     ```
   - Create the interface that represents the page's data model.

2. **Create the empty model**
   - **File:**
     ```text
     src/utils/createEmptyBodyMeasurements.ts
     ```
   - Create a helper that returns a new empty `BodyMeasurements` object.

3. **Create the API layer**
   - **File:**
     ```text
     src/api/<pageName>.ts
     ```
   - Create the API methods required by the page.
   - The API layer is responsible for:
     - Sending requests to the backend.
     - Converting backend models into frontend models.
     - Converting frontend models into backend request models.
   - Example:
     - `getSleepMetric()`
     - `saveSleepMetric()`

4. **Create the page**
   - **File:**
     ```text
     src/pages/LogBodyMeasurements/LogBodyMeasurements.tsx
     ```
   - Create the page that owns the React state.
   - Implement the page lifecycle:
     - Load data from the backend.
     - Manage page state.
     - Handle saving.
     - Pass state to the page sections.

5. **Create the page sections**
   - **Files:**
     ```text
     src/pages/LogBodyMeasurements/components/*
     ```
   - Create the components responsible for rendering each section of the page.
   - Keep page-specific UI inside these components.

6. **Register the page with React Router**
   - **File:**
     ```text
     src/App.tsx
     ```
   - Add a new route so React Router can load the page.

7. **Update the navigation**
   - **Desktop Navigation:**
     ```text
     src/navigation/navigation.ts
     ```
   - Add the page to `desktopNavigationItems`.

   - **Mobile More Menu (if applicable):**
     ```text
     src/components/MoreMenu.tsx
     ```
   - Add secondary pages to the mobile More menu.

8. **Test the page**
   - Verify the page loads correctly.
   - Verify data is retrieved from the backend.
   - Verify changes update the page state.
   - Verify data is saved successfully.
   - Reload the page and confirm the saved values are displayed.


## Testing

The frontend is tested at multiple levels. Each level verifies a different part of the application.

### Utility Tests

Utility tests verify small helper functions and calculations.

Example:
- `calculateSleepDuration()` returns the correct sleep duration.
- `createEmptyNutritionMetrics()` returns a correctly initialised object.

### Reusable Component Tests

Reusable component tests verify that shared UI components render correctly and respond to user interactions.

For reusable component tests, we:
- Render the component into a virtual DOM (provided by React Testing Library + JSDOM).
- Verify what the user would see (text, labels, values, buttons, etc.).
- Simulate user interactions (typing, clicking, selecting).
- Verify the component responds correctly (calls callbacks, updates rendered output, becomes disabled, etc.).

We generally don't inspect the raw HTML. Instead, we query the DOM the same way a user or assistive technology would (e.g., getByLabelText, getByRole, getByText). This makes the tests more realistic and less fragile.

Example:
- `TextInput` displays the supplied value and calls `onChange()` when the user types.
- `Button` calls the supplied `onClick()` callback when clicked.

### Section Component Tests

Section component tests verify that each section correctly displays data and updates the shared page state.

For Section Component Tests, we still render the component into a virtual DOM, but the focus is on state updates rather than just rendering.
- Render the section with some initial page state.
- Verify the fields display the supplied values.
- Simulate user interactions (typing, selecting, etc.).
- Verify that the section requests the correct state update by checking the setNutritionMetrics/setBodyMeasurements callback and ensuring only the intended field changes while the rest of the state is preserved.

So, reusable component tests answer "Does this component work?", while section component tests answer "Does this section correctly update the page state?"

Example:
- `NutritionMetricsSection` updates the water value when the user changes the input field.
- `NutritionMetricsSection` updates only the changed field without affecting the rest of the `NutritionMetrics` state.

### Page Tests

Page tests verify that complete pages render correctly and that all sections, page state, and backend interactions work together as expected.

- We render the entire page into a virtual DOM
- mock the backend API
- simulate user interactions
- verify that the page renders correctly and updates its state and calls the backend with the correct data.

Example:
- `LogSleepMetrics` loads data from the backend and displays the page correctly.
- `LogBodyMeasurements` updates the page state when measurements change and saves the updated data to the backend.

### Routing Tests

Routing tests verify that the application's routing is configured correctly and that the correct page is displayed for each URL.
This is the testing for the src\App.tsx

Example:
- Navigating to `/nutrition-metrics` displays the `LogNutritionMetrics` page.
- Navigating to `/body-measurements` displays the `LogBodyMeasurements` page.


### API Layer Tests

API layer tests verify that the frontend communicates with the backend correctly.
This is the testing for the files in src\api\ (for example src\api\nutritionMetrics.ts)

We:
- Mock the browser's `fetch()` function.
- Verify the correct HTTP request is sent.
- Verify backend responses are converted into frontend models.
- Verify errors are handled correctly.

Example:
- `getNutritionMetric()` retrieves Nutrition Metrics and converts them into a `NutritionMetrics` object.
- `saveBodyMeasurement()` sends the correct request payload to the backend.

#### Running Tests

Run all frontend tests:

```bash
npm test -- --run
```

Run a specific test file:

```bash
npx vitest src/components/TextInput.test.tsx -- --run
```

Run all tests with code coverage:

```bash
npm run test:coverage
```

Run a single test by name
```bash
npx vitest --run -t "saves successfully"
```

Run all tests matching a pattern
```bash
npx vitest --run LogBodyMeasurements
```