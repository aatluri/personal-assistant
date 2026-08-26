/*
    CollapsibleCard

    Reusable card component whose contents can be
    expanded or collapsed by the user.

    Responsibilities:
    - Display a section heading with an icon.
    - Show or hide the section content.
    - Provide a consistent appearance for expandable
      sections throughout the application.
*/

import { useState } from "react";
import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";
import { ChevronDown } from "lucide-react";


/*
    title
        Text displayed in the card header.

    icon
        Lucide icon displayed beside the title.

    iconColor
        Tailwind class used to style the icon.

    children
        The content displayed when the card
        is expanded.
*/

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


    /*
        Tracks whether the card is currently
        expanded or collapsed.

        The card starts in the expanded state.
    */
    const [expanded, setExpanded] = useState(true);

    return (

        /*
            Render the outer card using the
            application's standard card styling.
        */
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
            {/*
                Card header.

                Clicking anywhere on the header
                toggles the expanded state.
            */}
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
                {/*
                    Chevron icon that rotates to indicate
                    whether the card is expanded.
                */}
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
            {/*
                Expandable content area.

                The content always exists in the DOM,
                but CSS is used to smoothly expand
                and collapse it.
            */}

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
                {/* Display the content supplied by the caller. */}
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