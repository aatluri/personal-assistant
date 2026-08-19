/*
    CollapsibleCard

    A reusable card that can be
    expanded and collapsed.

    Used for sections on the
    Log Today page.
*/

import { useState } from "react";
import type { ReactNode } from "react";

interface CollapsibleCardProps {
    title: string;
    children: ReactNode;
}

function CollapsibleCard({
    title,
    children,
}: CollapsibleCardProps) {

    const [expanded, setExpanded] = useState(true);

    return (

        <section
            className="
                bg-white
                rounded-2xl
                border
                border-slate-200
                shadow-sm
            "
        >

            <button
                type="button"
                onClick={() => setExpanded(!expanded)}
                className="
                    w-full
                    flex
                    items-center
                    justify-between
                    p-6
                    text-left
                "
            >

                <h2
                    className="
                        text-xl
                        font-semibold
                        text-slate-900
                    "
                >
                    {title}
                </h2>

                <span
                    className="
                        text-slate-500
                        text-xl
                        select-none
                    "
                >
                    {expanded ? "⌄" : "›"}
                </span>

            </button>

            {expanded && (

                <div
                    className="
                        px-6
                        pb-6
                    "
                >
                    {children}
                </div>

            )}

        </section>

    );

}

export default CollapsibleCard;