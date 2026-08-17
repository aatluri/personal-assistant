/*
    HydrationSection

    Displays the user's water intake for the day.
*/

import type { Dispatch, SetStateAction } from "react";
import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    Props received from the parent component.
*/
interface HydrationSectionProps {

    // Current weight
    water: number | "";
    // Function used to update the complete dailyLog object
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;

}

function HydrationSection({
    water,
    setDailyLog,
}: HydrationSectionProps) {
    return (

        <section>

            {/* Section Heading */}
            <h2>Hydration</h2>

            <TextInput
                label="Water (ml)"
                id="water"
                name="water"
                type="number"
                min={0}
                step={100}
                value={water}
/*
    Triggered whenever the user changes the Water input.

    Steps:
    1. Read the new water value entered by the user and store it in newWater.
    2. React provides the current DailyLog object.
    3. Copy the entire DailyLog using the spread operator.
    4. Copy the hydration object.
    5. Update only the water field.
    6. React stores the updated DailyLog and re-renders the UI.
*/
                onChange={(event) => {
                const newWater = event.target.value === ""? "": Number(event.target.value);

/*
    Copy the existing daily log values,then update only the water. For example the weight, workout section etc..
*/
                setDailyLog((previousDailyLog) => ({
                    ...previousDailyLog,
                    hydration: {
                        ...previousDailyLog.hydration,
                        water: newWater,
                    },
                }));
                }}
            />

        </section>

    );
}

export default HydrationSection;