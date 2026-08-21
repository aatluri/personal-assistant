/*
    SaveButton

    Sticky action bar used to save
    the Daily Log.
*/

import Button from "../../../components/Button";

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
        Determine the button text based
        on the current save state.
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

            <div
                className="
                    mx-auto
                    max-w-3xl
                "
            >

                <Button
                    onClick={onClick}
                    disabled={
                        saveStatus === "saving" ||
                        (!isDirty && saveStatus !== "failed")
                    }
                >
                    {getButtonText()}
                </Button>

            </div>

        </div>

    );

}

export default SaveButton;