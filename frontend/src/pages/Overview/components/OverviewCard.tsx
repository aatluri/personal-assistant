/*
OverviewCard

The frame shared by the Overview's six cards: a heading
with an icon, an optional note on the right (what the
numbers cover, e.g. "avg per night"), and the content.

Unlike CollapsibleCard, it cannot be collapsed: the
Overview is read at a glance.
*/

import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";


/*
    title
        Card heading, e.g. "Sleep".

    icon, iconColor
        Lucide icon beside the title, and its Tailwind
        text colour (each section keeps one colour).

    note
        Optional text on the right of the heading.
*/
interface OverviewCardProps {
    title: string;
    icon: LucideIcon;
    iconColor: string;
    note?: string;
    children: ReactNode;
}

function OverviewCard({
    title,
    icon: Icon,
    iconColor,
    note,
    children,
}: OverviewCardProps) {

    return (

        <section
            aria-label={title}
            className="
                min-w-0
                rounded-2xl
                border
                border-slate-100
                bg-white
                p-5
                shadow-sm
            "
        >

            <div
                className="
                    mb-2
                    flex
                    items-center
                    gap-2
                    text-sm
                    text-slate-600
                "
            >
                <Icon size={18} aria-hidden="true" className={iconColor} />

                <h3 className="font-medium">
                    {title}
                </h3>

                {note && (
                    <span className="ml-auto text-right text-xs text-slate-400">
                        {note}
                    </span>
                )}
            </div>

            {children}

        </section>

    );

}

export default OverviewCard;
