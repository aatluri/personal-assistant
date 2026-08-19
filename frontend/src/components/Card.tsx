/*
    Card

    Reusable container used throughout
    the application.

    Follows the UI Design System.
*/

import type { ReactNode } from "react";

interface CardProps {
    children: ReactNode;
}

function Card({
    children,
}: CardProps) {
    return (
        <section
            className="
                bg-white
                rounded-2xl
                border
                border-slate-200
                shadow-sm
                p-6
            "
        >
            {children}
        </section>
    );
}

export default Card;