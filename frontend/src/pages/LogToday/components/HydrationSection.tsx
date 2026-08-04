/*
    HydrationSection

    Displays the user's water intake for the day.
*/

import TextInput from "../../../components/TextInput";

function HydrationSection() {
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
                defaultValue={2700}
            />

        </section>

    );
}

export default HydrationSection;