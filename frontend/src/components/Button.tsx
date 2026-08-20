/*
    Button

    Reusable button component used
    throughout the application.
*/

import type { ButtonHTMLAttributes } from "react";

interface ButtonProps
    extends ButtonHTMLAttributes<HTMLButtonElement> {}

function Button({
    children,
    className = "",
    ...buttonProps
}: ButtonProps) {

    return (
        <button
            {...buttonProps}
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
            {children}
        </button>
    );

}

export default Button;