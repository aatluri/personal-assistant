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