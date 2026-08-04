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
            <label htmlFor={inputProps.id}>
                {label}
            </label>

            {/* Input */}
            <input
                {...inputProps}
            />

        </div>

    );

}

export default TextInput;