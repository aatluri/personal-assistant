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
                transition
                hover:bg-blue-700
                active:scale-[0.98]
                disabled:bg-slate-300
                disabled:text-slate-500
                disabled:cursor-not-allowed
                ${className}
            `}
        >
            {children}
        </button>
    );

}

export default Button;