/*
    Button

    A reusable button component.

    It wraps the standard HTML <button> element
    and supports all normal button attributes.
*/

import type { ButtonHTMLAttributes } from "react";

/*
    Extend the standard HTML button attributes.

    This automatically supports:
    - type
    - disabled
    - onClick
    - ...etc.
*/
interface ButtonProps
    extends ButtonHTMLAttributes<HTMLButtonElement> {

    // Text displayed inside the button
    children: React.ReactNode;

}

function Button({

    children,

    ...buttonProps

}: ButtonProps) {

    return (

        <button {...buttonProps}>

            {children}

        </button>

    );

}

export default Button;