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
  weight: number;

  // Function used to update the complete dailyLog object
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
          const newWeight = Number(event.target.value);

          /*
              Copy the existing daily log values,
              then update only the weight.
          */
          setDailyLog((previousDailyLog) => ({
            ...previousDailyLog,
            weight: newWeight,
          }));
        }}
      />
    </section>
  );
}

export default BodySection;