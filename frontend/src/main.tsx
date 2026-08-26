/*
    main.tsx

    Entry point of the React application.

    Responsibilities:
    - Create the React application.
    - Load global CSS.
    - Render the root App component.
*/

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";


/*
    Find the HTML element with id="root"
    (defined in index.html) and mount
    the React application into it.
*/
createRoot(document.getElementById("root")!).render(
  /*
        StrictMode helps identify potential
        problems during development.

        It performs additional checks but
        has no effect in production.
  */
  <StrictMode>
    {/* Root component of the application. */}
    <App />
  </StrictMode>,
);