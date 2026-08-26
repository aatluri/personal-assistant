/*
    TextArea

    Reusable multi-line text input component used
    throughout the application.

    Responsibilities:
    - Provide a consistent look and feel for all text areas.
    - Support all standard HTML textarea attributes.
    - Display a label above the text area.
*/

import type { TextareaHTMLAttributes } from "react";


/*
    By extending TextareaHTMLAttributes, this component
    automatically supports all normal HTML textarea
    properties such as:
    - value
    - onChange
    - placeholder
    - rows
    - disabled
    - required
    - ...etc.
*/
interface TextAreaProps
    extends TextareaHTMLAttributes<HTMLTextAreaElement> {

    /*
        label
            Text displayed above the text area.
    */
    label: string;
}

function TextArea({
    label,
    ...textAreaProps
}: TextAreaProps) {

    return (
        <div>
            {/* Display the label for the text area. */}
            <label
                htmlFor={textAreaProps.id}
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
                Render the HTML <textarea> element.

                Spread all remaining HTML textarea
                attributes onto the element.

                Example:
                    value
                    onChange
                    placeholder
                    rows
                    disabled
            */}
            <textarea
                {...textAreaProps}
                className="
                    w-full
                    rounded-xl
                    border
                    border-slate-300
                    bg-white
                    px-4
                    py-3
                    text-base
                    text-slate-900
                    placeholder:text-slate-400
                    focus:border-blue-600
                    focus:ring-2
                    focus:ring-blue-100
                    focus:outline-none
                    transition
                    resize-y
                "
            />

        </div>
    );
}

export default TextArea;