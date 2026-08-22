/*
    AppShell

    Shared application layout.

    Responsibilities:
    - Desktop sidebar
    - Mobile bottom navigation
    - Mobile More menu
    - Main content area
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
        Controls whether the mobile
        More bottom sheet is visible.
    */
    const [isMoreMenuOpen, setIsMoreMenuOpen] =
        useState(false);

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

                {/* App Name */}
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

                {mobileNavigationItems.map((item) => {

                    /*
                        More is not a route.

                        It opens the mobile bottom sheet
                        instead of navigating to another page.
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
                        Normal mobile navigation item.
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

            {/* Mobile More Bottom Sheet */}
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