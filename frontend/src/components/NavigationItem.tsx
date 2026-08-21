/*
    NavigationItem

    Reusable navigation link used by the
    desktop sidebar and mobile bottom navigation.
*/

import type { LucideIcon } from "lucide-react";
import { NavLink } from "react-router-dom";

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

        <NavLink
            to={to}
            className={({ isActive }) =>

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

            <Icon size={20} />

            <span>{label}</span>

        </NavLink>

    );

}

export default NavigationItem;