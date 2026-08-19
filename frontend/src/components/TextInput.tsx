/*
    TextInput

    A reusable input component that wraps the
    standard HTML <input> element.

    It accepts all normal HTML input attributes,
    along with a custom label.
*/

import type { InputHTMLAttributes } from "react";

/*
    Create our own props by extending the standard
    HTML input props.

    This means our component automatically supports:
    - min
    - max
    - step
    - placeholder
    - required
    - disabled
    - defaultValue
    - ...and many more.
*/

/*This tells TypeScript: “Our component should support everything a normal HTML <input> supports.”*/
interface TextInputProps extends InputHTMLAttributes<HTMLInputElement> {


    // Text displayed above the input
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

            {/* Label */}
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

            {/* Input */}
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