/*
    Navigation

    Defines the application's navigation structure.

    Responsibilities:
    - List all available pages.
    - Provide the labels displayed in the navigation.
    - Specify the icon for each page.
    - Allow desktop and mobile navigation to have
      different layouts.
*/

import {
    BarChart3,
    CalendarDays,
    ClipboardPen,
    Ellipsis,
    Ruler,
    Settings,
} from "lucide-react";

/*
    Navigation items displayed in the
    desktop sidebar.

    Desktop has enough space to display
    all available pages.
*/
export const desktopNavigationItems = [
    {
        to: "/",
        label: "Dashboard",
        shortLabel: "Dashboard",
        icon: BarChart3,
    },
    {
        to: "/log-today",
        label: "Log Today",
        shortLabel: "Log",
        icon: ClipboardPen,
    },
    {
        to: "/body-measurements",
        label: "Body Measurements",
        shortLabel: "Body",
        icon: Ruler,
    },
    {
        to: "/history",
        label: "History",
        shortLabel: "History",
        icon: CalendarDays,
    },
    {
        to: "/settings",
        label: "Settings",
        shortLabel: "Settings",
        icon: Settings,
    },
];

/*
    Navigation items displayed in the
    mobile bottom navigation.

    Since mobile has limited space, only the
    most frequently used pages are displayed.

    Additional pages are accessed through
    the "More" menu.
*/
export const mobileNavigationItems = [
    {
        to: "/",
        label: "Dashboard",
        shortLabel: "Dashboard",
        icon: BarChart3,
    },
    {
        to: "/log-today",
        label: "Log",
        shortLabel: "Log",
        icon: ClipboardPen,
    },
    {
        to: "/history",
        label: "History",
        shortLabel: "History",
        icon: CalendarDays,
    },
    {
        /*
            "More" is not a route.

            It is handled specially by AppShell,
            which opens the More bottom sheet
            instead of navigating to another page.
        */
        to: "#",
        label: "More",
        shortLabel: "More",
        icon: Ellipsis,
    },
];