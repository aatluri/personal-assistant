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