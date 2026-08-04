/*
    SleepSection

    Captures the user's sleep start and end times.
*/

import TextInput from "../../../components/TextInput";

function SleepSection() {
  return (
    <section>
      {/* Section heading */}
      <h2>Sleep</h2>

      {/* Time the user went to sleep */}
      <TextInput
        label="Sleep Start Time"
        id="sleep-start-time"
        name="sleepStartTime"
        type="time"
        defaultValue="23:15"
      />

      {/* Time the user woke up */}
      <TextInput
        label="Sleep End Time"
        id="sleep-end-time"
        name="sleepEndTime"
        type="time"
        defaultValue="06:57"
      />
    </section>
  );
}

export default SleepSection;