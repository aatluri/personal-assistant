/*
    BodySection

    Displays and updates the user's
    body-related information.

    Responsibilities:
    - Display body-related fields.
    - Update the DailyLog state when values change.
    - Keep the UI focused only on body data.

    The page state is owned by LogToday.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    weight
        Current weight displayed on the page.

    setDailyLog
        Callback used to update the page state.
*/
interface BodySectionProps {
    // Current weight value
    weight: number | "";

    // Function used to update the complete DailyLog object
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;
}

function BodySection({
    weight,
    setDailyLog,
}: BodySectionProps) {

    return (
        /*
            Display the Body section.
        */
        <section>

            <div
                className="
                    space-y-6
                    md:w-1/2
                "
            >

                {/* Weight field */}
                <TextInput
                    label="Weight (kg)"
                    id="weight"
                    name="weight"
                    type="number"
                    min={0}
                    step={0.1}
                    value={weight}
                    /*
                        Update only the Weight value while
                        preserving the rest of the DailyLog.
                    */
                    onChange={(event) => {
                        const newWeight =
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value);

                        /*
                            Triggered whenever the user changes the Weight input.

                            Steps:
                            1. Read the new weight value.
                            2. Copy the existing DailyLog.
                            3. Copy the body object.
                            4. Update only the weight field.
                            5. React stores the updated DailyLog and re-renders the UI.
                        */
                        setDailyLog((previousDailyLog) => ({
                            ...previousDailyLog,
                            body: {
                                ...previousDailyLog.body,
                                weight: newWeight,
                            },
                        }));
                    }}
                />

            </div>

        </section>
    );
}

export default BodySection;