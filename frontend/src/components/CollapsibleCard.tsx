/*
    CollapsibleCard

    A reusable card that can be
    expanded and collapsed.

    Used for sections on the
    Log Today page.
*/

import { useState } from "react";
import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";
import { ChevronDown } from "lucide-react";

interface CollapsibleCardProps {
    title: string;
    icon: LucideIcon;
    iconColor: string;
    children: ReactNode;
}

function CollapsibleCard({
    title,
    icon: Icon,
    iconColor,
    children,
}: CollapsibleCardProps) {

    const [expanded, setExpanded] = useState(true);

    return (

        <section
            className="
                overflow-hidden
                rounded-2xl
                border
                border-slate-100
                bg-white
                shadow-sm
                transition-shadow
                duration-200
                hover:shadow-md
            "
        >

            <button
                type="button"
                onClick={() => setExpanded(!expanded)}
                className="
                    flex
                    w-full
                    items-center
                    justify-between
                    rounded-t-2xl
                    border-b
                    border-slate-100
                    p-6
                    text-left
                    transition-colors
                    duration-200
                    hover:bg-slate-50
                    active:bg-slate-100
                "
            >

                <div
                    className="
                        flex
                        items-center
                        gap-4
                    "
                >

                    <Icon
                        size={24}
                        className={iconColor}
                    />

                    <h2
                        className="
                            text-xl
                            font-semibold
                            tracking-tight
                            text-slate-900
                        "
                    >
                        {title}
                    </h2>

                </div>

                <ChevronDown
                    size={22}
                    className={`
                        text-slate-500
                        transition-transform
                        duration-200
                        ${expanded ? "rotate-180" : ""}
                    `}
                />

            </button>

            <div
                className={`
                    overflow-hidden
                    transition-all
                    duration-300
                    ${
                        expanded
                            ? "max-h-[2000px] opacity-100"
                            : "max-h-0 opacity-0"
                    }
                `}
            >

                <div
                    className="
                        px-6
                        pt-6
                        pb-6
                    "
                >
                    {children}
                </div>

            </div>

        </section>

    );

}

export default CollapsibleCard;