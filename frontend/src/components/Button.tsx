/*
    Button

    Reusable button component used throughout the application.

    Responsibilities:
    - Provide a consistent look and feel for all buttons.
    - Support all standard HTML button attributes.
    - Allow pages to add additional styling when required.
*/

import type { ButtonHTMLAttributes } from "react";

/*
    By extending ButtonHTMLAttributes, this component
    automatically supports all normal HTML button properties
    such as:
    - onClick
    - disabled
    - type
    - title
    - ...etc.
*/
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {}

/*
    children
        The content displayed inside the button.

    className
        Optional additional Tailwind classes supplied
        by the caller.

    buttonProps
        Collects all remaining HTML button attributes
        and passes them directly to the underlying
        <button> element.
*/
function Button({
    children
    ,className = ""
    ,...buttonProps
    }: ButtonProps) {

    return (
         /*
            Spread all standard HTML button attributes
            onto the native button element.

            Example:
                disabled
                onClick
                type
        */
        <button
            {...buttonProps}
            /*
                Apply the application's default button styling.

                Any classes supplied by the caller are appended,
                allowing page-specific styling when needed.
            */
            className={`
                w-full
                h-12
                rounded-xl
                bg-blue-600
                text-white
                font-medium
                shadow-sm
                transition-all
                duration-200

                hover:bg-blue-700
                hover:shadow-md
                hover:-translate-y-0.5

                active:translate-y-0
                active:scale-[0.98]

                disabled:bg-slate-200
                disabled:text-slate-500
                disabled:shadow-none
                disabled:translate-y-0
                disabled:cursor-not-allowed

                ${className}
            `}
        >
            {/* Display the content supplied by the caller. */}
            {children}
        </button>
    );

}

export default Button;