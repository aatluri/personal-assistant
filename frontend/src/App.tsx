/*
    App

    Root component of the application.

    Responsibilities:
    - Configure routing
    - Load the shared AppShell
    - Display pages inside the AppShell
*/

import { BrowserRouter, Route, Routes } from "react-router-dom";

import AppShell from "./layouts/AppShell";

import Dashboard from "./pages/Dashboard/Dashboard";
import History from "./pages/History/History";
import LogToday from "./pages/LogToday/LogToday";
import Settings from "./pages/Settings/Settings";

function App() {

    return (

        <BrowserRouter>

            <Routes>

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