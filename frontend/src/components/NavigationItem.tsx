/*
    NavigationItem

    Reusable navigation link used by both the
    desktop sidebar and the mobile navigation.

    Responsibilities:
    - Display the navigation icon and label.
    - Navigate to the requested page.
    - Highlight the currently active page.
    - Apply different layouts for desktop and mobile.
*/

import type { LucideIcon } from "lucide-react";
import { NavLink } from "react-router-dom";


/*
    to
        The route this navigation item points to.

    label
        The text displayed beside (or below) the icon.

    icon
        The Lucide icon displayed for the navigation item.

    mobile
        Determines whether the mobile or desktop
        navigation layout should be used.
*/

interface NavigationItemProps {
    to: string;
    label: string;
    icon: LucideIcon;
    mobile?: boolean;
}

function NavigationItem({
    to,
    label,
    icon: Icon,
    mobile = false,
}: NavigationItemProps) {

    return (
        /*
            NavLink automatically determines whether
            this route is currently active.

            The isActive property is then used to
            apply the appropriate styling.
        */

        <NavLink
            to={to}
            className={({ isActive }) =>

                /*
                    Use a compact vertical layout for
                    the mobile bottom navigation.
                */
                mobile

                    ? `
                        flex
                        flex-1
                        flex-col
                        items-center
                        gap-1
                        py-3
                        text-xs
                        transition-colors
                        ${
                            isActive
                                ? "text-blue-600"
                                : "text-slate-500"
                        }
                    `
                    /*
                        Use a wider horizontal layout for
                        the desktop sidebar navigation.
                    */
                    : `
                        flex
                        items-center
                        gap-3
                        rounded-xl
                        px-4
                        py-3
                        transition-colors
                        ${
                            isActive
                                ? "bg-blue-50 text-blue-700 font-semibold"
                                : "text-slate-700 hover:bg-slate-100"
                        }
                    `
            }
        >
            {/* Display the navigation icon. */}
            <Icon size={20} />
            {/* Display the navigation label. */}
            <span>{label}</span>

        </NavLink>

    );

}

export default NavigationItem;