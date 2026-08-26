/*
    HydrationSection

    Displays and updates the user's
    daily water intake.

    Responsibilities:
    - Display hydration-related fields.
    - Update the DailyLog state when values change.
    - Keep the UI focused only on hydration data.

    The page state is owned by LogToday.
*/


import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    water
        Current water intake displayed
        on the page.

    setDailyLog
        Callback used to update the page state.
*/
interface HydrationSectionProps {

    // Current water intake
    water: number | "";

    // Function used to update the complete DailyLog object
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;

}

function HydrationSection({
    water,
    setDailyLog,
}: HydrationSectionProps) {

    return (

        /*
            Display the Hydration section.
        */
        <section>

            <div
                className="
                    space-y-6
                    md:w-1/2
                "
            >

                <TextInput
                    label="Water (ml)"
                    id="water"
                    name="water"
                    type="number"
                    min={0}
                    step={100}
                    value={water}
                    /*
                        Update only the Water value while
                        preserving the rest of the DailyLog.
                    */
                    onChange={(event) => {

                        const newWater =
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value);

                        /*
                            Copy the existing Daily Log
                            and update only the water field.
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

            </div>

        </section>

    );

}

export default HydrationSection;