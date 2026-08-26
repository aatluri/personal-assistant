/*
    Card

    Reusable container component used throughout the application.

    Responsibilities:
    - Provide a consistent card appearance.
    - Wrap related content into a visually grouped section.
    - Ensure all pages follow the application's design system.
*/

import type { ReactNode } from "react";


/*
    children
        The content displayed inside the card.

    Using ReactNode allows the card to contain
    any valid React content, such as:
    - Text
    - Input fields
    - Buttons
    - Other components
    - Entire page sections
*/
interface CardProps {
    children: ReactNode;
}

function Card({
    children,
}: CardProps) {
    return (
         /*
            Render the card using the application's
            standard styling.

            Any content passed into the component is
            displayed inside this container.
        */
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
            {/* Display the content supplied by the caller. */}
            {children}
        </section>
    );
}

export default Card;