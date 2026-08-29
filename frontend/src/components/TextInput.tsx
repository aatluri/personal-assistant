/*
    TextInput

    Reusable input component used throughout
    the application.

    Responsibilities:
    - Provide a consistent look and feel for all input fields.
    - Support all standard HTML input attributes.
    - Display a label above the input.
*/


import type { InputHTMLAttributes } from "react";

/*
    By extending InputHTMLAttributes, this component
    automatically supports all normal HTML input
    properties such as:
    - value
    - onChange
    - min
    - max
    - step
    - placeholder
    - required
    - disabled
    - defaultValue
    - ...etc.
*/

/*This tells TypeScript: “Our component should support everything a normal HTML <input> supports.”*/
interface TextInputProps extends InputHTMLAttributes<HTMLInputElement> {


    /*
        label
            Text displayed above the input field.
    */
    label: string;

}

/*
    Receive the label separately.
    Everything else is collected into "inputProps".
*/
function TextInput({

    label,

    ...inputProps

}: TextInputProps) {
    return (

        <div>

            {/* Display the label for the input field. */}
            <label
                htmlFor={inputProps.id}
                className="
                    block
                    mb-2
                    text-sm
                    font-medium
                    text-slate-700
                "
            >
                {label}
            </label>

            {/*
                Render the HTML <input> element.

                Spread all remaining HTML input
                attributes onto the element.

                Example:
                    value
                    onChange
                    placeholder
                    min
                    max
                    step
                    disabled
            */}
            <input
                {...inputProps}
                className="
                    w-full
                    h-12
                    rounded-xl
                    border
                    border-slate-300
                    bg-white
                    px-4
                    text-base
                    text-slate-900
                    placeholder:text-slate-400
                    focus:border-blue-600
                    focus:ring-2
                    focus:ring-blue-100
                    focus:outline-none
                    transition
                "
            />

        </div>

    );

}

export default TextInput;