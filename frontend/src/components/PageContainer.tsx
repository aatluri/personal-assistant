/*
    PageContainer

    Provides the standard page layout used
    throughout the application.

    Responsibilities:
    - Render the main page container.
    - Provide a consistent page background.
    - Limit the maximum content width.
    - Apply consistent spacing around page content.
*/

import type { ReactNode } from "react";

/*
    children
        The page content to be displayed
        inside the standard application layout.
*/
interface PageContainerProps {
    children: ReactNode;
}

function PageContainer({
    children,
}: PageContainerProps) {
    return (

        /*
            Outer page container.

            Responsible for the overall page
            appearance, including:
            - Background colour
            - Minimum page height
            - Page padding
        */
        <main
            className="
                min-h-screen
                bg-slate-50
                px-4
                py-8
            "
        >
            {/*
                Centre the page content and
                limit its maximum width.

                All pages rendered using this
                component automatically share
                the same overall layout.
            */}
            <div
                className="
                    mx-auto
                    max-w-3xl
                "
            >
                {/* Display the page content supplied by the caller. */}
                {children}
            </div>
        </main>
    );
}

export default PageContainer;