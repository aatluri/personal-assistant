/*
    Select

    Reusable dropdown component used throughout
    the application.

    Responsibilities:
    - Provide a consistent look and feel for all dropdowns.
    - Support all standard HTML select attributes.
    - Display a label above the dropdown.
*/

import type {
    ReactNode,
    SelectHTMLAttributes,
} from "react";

/*
    By extending SelectHTMLAttributes, this component
    automatically supports all normal HTML select
    properties such as:
    - value
    - onChange
    - disabled
    - required
    - ...etc.
*/
interface SelectProps
    extends SelectHTMLAttributes<HTMLSelectElement> {

    /*
        label
            Text displayed above the dropdown.
    */
    label: string;

    /*
        children
            The list of <option> elements displayed
            inside the dropdown.
    */
    children: ReactNode;
}

function Select({
    label,
    children,
    ...selectProps
}: SelectProps) {

    return (
        <div>
             {/* Display the label for the dropdown. */}
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
            {/*
                Render the HTML <select> element.

                Spread all remaining HTML select
                attributes onto the element.

                Example:
                    value
                    onChange
                    disabled
                    required
            */}
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
                {/* Display the options supplied by the caller. */}
                {children}
            </select>

        </div>
    );
}

export default Select;