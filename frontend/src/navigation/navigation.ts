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
    Apple,
    BarChart3,
    BellRing,
    CalendarDays,
    Dumbbell,
    Ellipsis,
    HeartPulse,
    Moon,
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
        label: "Overview",
        shortLabel: "Overview",
        icon: BarChart3,
    },
    {
        to: "/body-measurements",
        label: "Body Measurements",
        shortLabel: "Body",
        icon: Ruler,
    },
    {
        to: "/workout-metrics",
        label: "Workout Metrics",
        shortLabel: "Workout",
        icon: Dumbbell,
    },
    {
        to: "/sleep-metrics",
        label: "Sleep Metrics",
        shortLabel: "Sleep",
        icon: Moon,
    },
    {
        to: "/nutrition-metrics",
        label: "Nutrition Metrics",
        shortLabel: "Nutrition",
        icon: Apple,
    },
    {
        to: "/health-metrics",
        label: "Health Metrics",
        shortLabel: "Health",
        icon: HeartPulse,
    },
    {
        to: "/heart-rate-notifications",
        label: "Heart Rate Notifications",
        shortLabel: "HR Alerts",
        icon: BellRing,
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
        label: "Overview",
        shortLabel: "Overview",
        icon: BarChart3,
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