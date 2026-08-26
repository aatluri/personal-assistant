/*
    App

    Root component of the application.

    Responsibilities:
    - Configure application routing.
    - Load the shared AppShell.
    - Define which page is displayed for each URL.
*/

import { BrowserRouter, Route, Routes } from "react-router-dom";

import AppShell from "./layouts/AppShell";

import Dashboard from "./pages/Dashboard/Dashboard";
import History from "./pages/History/History";
import LogToday from "./pages/LogToday/LogToday";
import Settings from "./pages/Settings/Settings";
import LogBodyMeasurements from "./pages/LogBodyMeasurements/LogBodyMeasurements";


function App() {

    return (

        /*
            BrowserRouter enables client-side routing.

            It watches the browser URL and ensures
            the correct page is rendered without
            refreshing the browser.
        */

        <BrowserRouter>

            {/* Define all application routes. */}

            <Routes>
                 {/*
                    All pages are rendered inside
                    the shared AppShell.

                    AppShell provides the common layout,
                    including the navigation and page
                    content area.
                */}

                <Route
                    element={<AppShell />}
                >

                    <Route
                        path="/"
                        element={<Dashboard />}
                    />

                    <Route
                        path="/log-today"
                        element={<LogToday />}
                    />

                    <Route
                        path="/body-measurements"
                        element={<LogBodyMeasurements />}
                    />

                    <Route
                        path="/history"
                        element={<History />}
                    />

                    <Route
                        path="/settings"
                        element={<Settings />}
                    />

                </Route>

            </Routes>

        </BrowserRouter>

    );

}

export default App;