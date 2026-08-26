/*
    MoreMenu

    Mobile bottom sheet used to display
    secondary navigation options.

    Responsibilities:
    - Display navigation items that do not fit
      in the mobile bottom navigation.
    - Allow the user to navigate to additional pages.
    - Close automatically when the user selects
      an option or taps outside the menu.
*/

import {
    Ruler,
    Settings,
    X,
} from "lucide-react";

import { Link } from "react-router-dom";


/*
    isOpen
        Determines whether the menu is visible.

    onClose
        Callback used to close the menu.
*/
interface MoreMenuProps {
    isOpen: boolean;
    onClose: () => void;
}

function MoreMenu({
    isOpen,
    onClose,
}: MoreMenuProps) {

    /*
        Do not render the component when
        the menu is closed.

        Returning null tells React that
        nothing should be displayed.
    */
    if (!isOpen) {
        return null;
    }

    return (

        <>
            {/*
                Semi-transparent background shown behind
                the bottom sheet.

                Clicking the overlay closes the menu.
            */}
            <div
                className="
                    fixed
                    inset-0
                    z-[60]
                    bg-black/30
                    md:hidden
                "
                onClick={onClose}
            />

            {/*
                Bottom sheet containing the additional
                navigation options.

                This is displayed only on mobile devices.
            */}
            <div
                className="
                    fixed
                    bottom-0
                    left-0
                    right-0
                    z-[70]
                    rounded-t-3xl
                    bg-white
                    px-4
                    pb-6
                    pt-4
                    shadow-xl
                    md:hidden
                "
            >

                {/* Menu header */}
                <div
                    className="
                        mb-4
                        flex
                        items-center
                        justify-between
                        px-2
                    "
                >

                    <h2
                        className="
                            text-xl
                            font-semibold
                            tracking-tight
                            text-slate-900
                        "
                    >
                        More
                    </h2>

                    {/*
                        Close button.

                        Executes the callback supplied
                        by the parent component.
                    */}
                    <button
                        type="button"
                        onClick={onClose}
                        className="
                            rounded-full
                            p-2
                            text-slate-500
                            transition-colors
                            hover:bg-slate-100
                        "
                    >
                        <X size={22} />
                    </button>

                </div>

                 {/* Additional navigation options */}
                <div className="space-y-2">

                    {/*
                        Navigate to the Body Measurements page.

                        The menu is automatically closed after
                        navigation.
                    */}
                    <Link
                        to="/body-measurements"
                        onClick={onClose}
                        className="
                            flex
                            items-center
                            gap-4
                            rounded-2xl
                            px-4
                            py-4
                            transition-colors
                            hover:bg-slate-50
                        "
                    >

                        <Ruler
                            size={24}
                            className="text-violet-600"
                        />

                        <div>

                            <p
                                className="
                                    font-medium
                                    text-slate-900
                                "
                            >
                                Body Measurements
                            </p>

                            <p
                                className="
                                    text-sm
                                    text-slate-500
                                "
                            >
                                Log body measurements
                            </p>

                        </div>

                    </Link>

                    {/*
                        Navigate to the Settings page.

                        The menu is automatically closed after
                        navigation.
                    */}
                    <Link
                        to="/settings"
                        onClick={onClose}
                        className="
                            flex
                            items-center
                            gap-4
                            rounded-2xl
                            px-4
                            py-4
                            transition-colors
                            hover:bg-slate-50
                        "
                    >

                        <Settings
                            size={24}
                            className="text-slate-600"
                        />

                        <div>

                            <p
                                className="
                                    font-medium
                                    text-slate-900
                                "
                            >
                                Settings
                            </p>

                            <p
                                className="
                                    text-sm
                                    text-slate-500
                                "
                            >
                                Manage goals and preferences
                            </p>

                        </div>

                    </Link>

                </div>

            </div>

        </>

    );

}

export default MoreMenu;