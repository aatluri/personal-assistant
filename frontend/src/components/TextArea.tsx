/*
    TextArea

    A reusable textarea component.

    It wraps the standard HTML <textarea> element
    and accepts all normal HTML textarea attributes.
*/

import type { TextareaHTMLAttributes } from "react";

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