/*
    MoreMenu

    Mobile bottom sheet used to display
    secondary navigation options.

    This is shown when the user taps
    "More" in the mobile bottom navigation.
*/

import {
    Ruler,
    Settings,
    X,
} from "lucide-react";

import { Link } from "react-router-dom";

interface MoreMenuProps {
    isOpen: boolean;
    onClose: () => void;
}

function MoreMenu({
    isOpen,
    onClose,
}: MoreMenuProps) {

    /*
        Do not render anything when
        the menu is closed.
    */
    if (!isOpen) {
        return null;
    }

    return (

        <>
            {/* Background overlay */}
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

            {/* Bottom Sheet */}
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

                {/* Header */}
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

                {/* Menu Items */}
                <div className="space-y-2">

                    {/* Body Measurements */}
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

                    {/* Settings */}
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