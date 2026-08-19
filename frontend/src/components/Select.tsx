/*
    Select

    A reusable dropdown component.

    It wraps the standard HTML <select> element
    and accepts all normal HTML select attributes.
*/

import type {
    ReactNode,
    SelectHTMLAttributes,
} from "react";

interface SelectProps
    extends SelectHTMLAttributes<HTMLSelectElement> {

    // Text displayed above the select
    label: string;

    // Options displayed inside the select
    children: ReactNode;
}

function Select({
    label,
    children,
    ...selectProps
}: SelectProps) {

    return (
        <div>

            <label
                htmlFor={selectProps.id}
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

            <select
                {...selectProps}
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
                    focus:border-blue-600
                    focus:ring-2
                    focus:ring-blue-100
                    focus:outline-none
                    transition
                "
            >
                {children}
            </select>

        </div>
    );
}

export default Select;