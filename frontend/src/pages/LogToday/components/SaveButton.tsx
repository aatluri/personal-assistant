/*
    SaveButton

    Sticky action bar used to save
    the Daily Log.

    The button is enabled only when
    there are unsaved changes.
*/

import Button from "../../../components/Button";

interface SaveButtonProps {
    onClick: () => void;
    isDirty: boolean;
}

function SaveButton({
    onClick,
    isDirty,
}: SaveButtonProps) {

    return (
        <div
            className="
                fixed
                bottom-0
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
                    disabled={!isDirty}
                >
                    {isDirty
                        ? "Save Changes"
                        : "✓ All Changes Saved"}
                </Button>
            </div>
        </div>
    );

}

export default SaveButton;