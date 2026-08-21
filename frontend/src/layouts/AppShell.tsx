/*
    AppShell

    Shared application layout.

    Responsibilities:
    - Desktop sidebar
    - Mobile bottom navigation
    - Main content area
*/

import { Outlet } from "react-router-dom";

import NavigationItem from "../components/NavigationItem";
import { navigationItems } from "../navigation/navigation";

function AppShell() {

    return (

        <div
            className="
                min-h-screen
                bg-slate-50
                md:flex
            "
        >

            {/* Desktop Sidebar */}
            <aside
                className="
                    hidden
                    w-64
                    border-r
                    border-slate-200
                    bg-white
                    md:flex
                    md:flex-col
                "
            >

                {/* Logo */}
                <div
                    className="
                        border-b
                        border-slate-200
                        p-6
                    "
                >

                    <h1
                        className="
                            text-2xl
                            font-bold
                            text-slate-900
                        "
                    >
                        Health Tracker
                    </h1>

                </div>

                {/* Desktop Navigation */}
                <nav
                    className="
                        flex-1
                        space-y-2
                        p-4
                    "
                >

                    {navigationItems.map((item) => (

                        <NavigationItem
                            key={item.to}
                            to={item.to}
                            label={item.label}
                            icon={item.icon}
                        />

                    ))}

                </nav>

            </aside>

            {/* Main Content */}
            <main
                className="
                    flex-1
                    pb-20
                "
            >
                <Outlet />
            </main>

            {/* Mobile Bottom Navigation */}
            <nav
                className="
                    fixed
                    bottom-0
                    left-0
                    right-0
                    z-50
                    flex
                    border-t
                    border-slate-200
                    bg-white
                    md:hidden
                "
            >

                {navigationItems.map((item) => (

                    <NavigationItem
                        key={item.to}
                        to={item.to}
                        label={item.shortLabel}
                        icon={item.icon}
                        mobile
                    />

                ))}

            </nav>

        </div>

    );

}

export default AppShell;