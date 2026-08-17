/*
    BodySection

    Displays the user's body-related
    measurements for the day.

    The state is owned by the parent
    LogToday component and passed here
    through props.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    Props received from the parent component.
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
        <section>

            {/* Section heading */}
            <h2>Body</h2>

            {/* Weight field */}
            <TextInput
                label="Weight (kg)"
                id="weight"
                name="weight"
                type="number"
                min={0}
                step={0.1}
                value={weight}
                onChange={(event) => {
                    const newWeight =event.target.value === ""? "": Number(event.target.value);

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

        </section>
    );
}

export default BodySection;