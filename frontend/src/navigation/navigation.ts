import {
    BarChart3,
    CalendarDays,
    ClipboardPen,
    Ellipsis,
    Ruler,
    Settings,
} from "lucide-react";

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
        to: "#",
        label: "More",
        shortLabel: "More",
        icon: Ellipsis,
    },
];