/*
    TextArea

    A reusable textarea component.

    It wraps the standard HTML <textarea> element
    and accepts all normal HTML textarea attributes.
*/

import type { TextareaHTMLAttributes } from "react";

/*
    Extend the standard HTML textarea attributes.

    This automatically supports:
    - rows
    - cols
    - placeholder
    - defaultValue
    - disabled
    - required
    - ...etc.
*/
interface TextAreaProps
    extends TextareaHTMLAttributes<HTMLTextAreaElement> {

    // Text displayed above the textarea
    label: string;

}

function TextArea({

    label,

    ...textAreaProps

}: TextAreaProps) {

    return (

        <div>

            {/* Label */}
            <label htmlFor={textAreaProps.id}>
                {label}
            </label>

            {/* Text Area */}
            <textarea
                {...textAreaProps}
            />

        </div>

    );

}

export default TextArea;