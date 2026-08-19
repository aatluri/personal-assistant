/*
    PageContainer

    Provides the standard page layout used
    throughout the application.

    Responsibilities:
    - Page background
    - Maximum content width
    - Responsive horizontal padding
    - Vertical spacing
*/

import type { ReactNode } from "react";

interface PageContainerProps {
    children: ReactNode;
}

function PageContainer({
    children,
}: PageContainerProps) {
    return (
        <main
            className="
                min-h-screen
                bg-slate-50
                px-4
                py-8
            "
        >
            <div
                className="
                    mx-auto
                    max-w-3xl
                "
            >
                {children}
            </div>
        </main>
    );
}

export default PageContainer;