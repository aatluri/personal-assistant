// App.tsx

// Import the BrowserRouter component.
// This enables routing (navigation) throughout the application.
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Import our Log Today page.
// This is the page we want to display when the user visits "/".
import LogToday from "./pages/LogToday/LogToday";

function App() {
  return (
    /*
      BrowserRouter is the root router for the application.

      It listens to the browser URL and decides
      which page (component) should be displayed.
    */
    <BrowserRouter>

      {/*
        Routes acts as a container for all the routes
        in the application.
      */}
      <Routes>

        {/*
          path="/" means the application's home page.
          element={<LogToday />} tells React to render the LogToday component whenever the URL is "/".
        */}
        <Route
          path="/"
          element={<LogToday />}
        />

      </Routes>

    </BrowserRouter>
  );
}

// Export App so that main.tsx can render it.
export default App;