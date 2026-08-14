/*
    Select

    A reusable dropdown component.

    It wraps the standard HTML <select> element
    and accepts all normal HTML select attributes.
*/

import type { ReactNode,SelectHTMLAttributes,} from "react";

/*
    Extend the standard HTML select attributes.

    This automatically supports:
    - defaultValue
    - disabled
    - required
    - multiple
    - onChange
    - ...etc.
*/
interface SelectProps
    extends SelectHTMLAttributes<HTMLSelectElement> {

    // Text displayed above the dropdown
    label: string;

    // The options displayed inside the dropdown
    children: ReactNode;

}

function Select({

    label,

    children,

    ...selectProps

}: SelectProps) {

    return (

        <div>

            {/* Label */}
            <label htmlFor={selectProps.id}>
                {label}
            </label>

            {/* Dropdown */}
            <select {...selectProps}>

                {children}

            </select>

        </div>

    );

}

export default Select;