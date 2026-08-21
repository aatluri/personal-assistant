import {
    BarChart3,
    CalendarDays,
    ClipboardPen,
    Settings,
} from "lucide-react";

export const navigationItems = [
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