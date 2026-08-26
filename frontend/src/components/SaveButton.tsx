/*
    SaveButton

    Sticky action bar displayed at the bottom
    of logging pages.

    Responsibilities:
    - Provide a consistent location for saving data.
    - Display the current save status.
    - Prevent unnecessary or duplicate saves.
*/

import Button from "./Button";

/*
    onClick
        Callback executed when the Save button
        is clicked.

    isDirty
        Indicates whether the page contains
        unsaved changes.

    saveStatus
        Represents the current state of the
        save operation.
*/
interface SaveButtonProps {
    onClick: () => void;
    isDirty: boolean;
    saveStatus: "idle" | "saving" | "saved" | "failed";
}

function SaveButton({
    onClick,
    isDirty,
    saveStatus,
}: SaveButtonProps) {

    /*
        Determine the button text based on
        the current save status.
    */
    function getButtonText() {

        switch (saveStatus) {

            case "saving":
                return "Saving...";

            case "failed":
                return "⚠ Save Failed - Try Again";

            case "saved":
                return "✓ All Changes Saved";

            default:
                return "Save Changes";

        }

    }

    return (
        /*
            Sticky container displayed at the bottom
            of the page.

            The position is adjusted on mobile to sit
            above the bottom navigation bar.
        */
        <div
            className="
                fixed
                bottom-16
                md:bottom-0
                left-0
                right-0
                z-50
                border-t
                border-slate-200
                bg-white
                px-4
                py-3
                shadow-[0_-2px_8px_rgba(0,0,0,0.05)]
            "
        >
            {/*
                Centre the Save button and align it
                with the rest of the page content.
            */}
            <div
                className="
                    mx-auto
                    max-w-3xl
                "
            >

                <Button
                    onClick={onClick}
                    /*
                        Disable the button when:
                        - A save is already in progress.
                        - There are no unsaved changes
                          (unless the previous save failed,
                          in which case the user can retry).
                    */
                    disabled={
                        saveStatus === "saving" ||
                        (!isDirty && saveStatus !== "failed")
                    }
                >
                    {/* Display the appropriate button text. */}
                    {getButtonText()}
                </Button>

            </div>

        </div>

    );

}

export default SaveButton;