/*
    AppShell

    Shared application layout used by every page.

    Responsibilities:
    - Render the desktop sidebar.
    - Render the mobile bottom navigation.
    - Display the mobile More menu.
    - Provide the main content area where pages are displayed.
*/

import { useState } from "react";

import { Ellipsis } from "lucide-react";

import { Outlet } from "react-router-dom";

import MoreMenu from "../components/MoreMenu";
import NavigationItem from "../components/NavigationItem";

import {
    desktopNavigationItems,
    mobileNavigationItems,
} from "../navigation/navigation";

function AppShell() {

    /*
        Tracks whether the mobile
        More menu is currently open.
    */
    const [isMoreMenuOpen, setIsMoreMenuOpen] =
        useState(false);

    return (

        /*
            Overall application layout.

            Contains:
            - Desktop sidebar
            - Main content area
            - Mobile navigation
            - Mobile More menu
        */
        <div
            className="
                min-h-screen
                bg-slate-50
                md:flex
            "
        >

            {/*
                Desktop sidebar.

                Hidden on mobile devices and displayed
                only on medium screens and larger.
            */}
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

                {/* Display the application name. */}
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

               {/*
                    Render the desktop navigation.

                    The navigation items are defined in
                    navigation/navigation.ts.
                */}
                <nav
                    className="
                        flex-1
                        space-y-2
                        p-4
                    "
                >

                    {desktopNavigationItems.map((item) => (

                        <NavigationItem
                            key={item.to}
                            to={item.to}
                            label={item.label}
                            icon={item.icon}
                        />

                    ))}

                </nav>

            </aside>

           {/*
                Main content area.

                <Outlet /> is provided by React Router
                and renders whichever page matches the
                current URL.

                Examples:
                    /log-today
                    /body-measurements
                    /settings
            */}
            <main
                className="
                    flex-1
                    pb-20
                "
            >
                <Outlet />
            </main>

            {/*
                Mobile bottom navigation.

                Hidden on desktop and displayed only
                on smaller screens.
            */}
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

                {mobileNavigationItems.map((item) => {

                    /*
                        "More" is not a navigation route.

                        Instead of navigating to another page,
                        it opens the More bottom sheet.
                    */
                    if (item.label === "More") {

                        return (

                            <button
                                key="more"
                                type="button"
                                onClick={() =>
                                    setIsMoreMenuOpen(true)
                                }
                                className="
                                    flex
                                    flex-1
                                    flex-col
                                    items-center
                                    gap-1
                                    py-3
                                    text-xs
                                    text-slate-500
                                    transition-colors
                                    hover:text-blue-600
                                "
                            >

                                <Ellipsis size={20} />

                                <span>More</span>

                            </button>

                        );

                    }

                    /*
                        Render a normal navigation item.

                        NavigationItem is responsible for
                        handling navigation and highlighting
                        the active page.
                    */
                    return (

                        <NavigationItem
                            key={item.to}
                            to={item.to}
                            label={item.shortLabel}
                            icon={item.icon}
                            mobile
                        />

                    );

                })}

            </nav>

            {/*
                Mobile More menu.

                The visibility of this component is
                controlled by the isMoreMenuOpen state.
            */}
            <MoreMenu
                isOpen={isMoreMenuOpen}
                onClose={() =>
                    setIsMoreMenuOpen(false)
                }
            />

        </div>

    );

}

export default AppShell;