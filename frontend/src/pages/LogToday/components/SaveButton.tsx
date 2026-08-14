/*
    SaveButton

    Reusable button used to save
    the Daily Log.
*/

import Button from "../../../components/Button";

interface SaveButtonProps {
    onClick: () => void;
}

function SaveButton({ onClick }: SaveButtonProps) {
    return (
        <Button onClick={onClick}>
            Save Daily Log
        </Button>
    );
}

export default SaveButton;