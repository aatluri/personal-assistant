/*
    NutritionSection

    Displays today's meals and nutritional information.

    All input fields are built using the reusable
    TextInput component.
*/

import TextInput from "../../../components/TextInput";
import TextArea from "../../../components/TextArea";

function NutritionSection() {
    return (

        <section>

            {/* Section Heading */}
            <h2>Nutrition</h2>

            {/* ----------------------------- */}
            {/* Meals                         */}
            {/* ----------------------------- */}

           <TextArea
                label="Breakfast"
                id="breakfast"
                name="breakfast"
                rows={3}
                placeholder="Enter breakfast"
            />

            <TextArea
                label="Lunch"
                id="lunch"
                name="lunch"
                rows={3}
                placeholder="Enter lunch"
            />

            <TextArea
                label="Dinner"
                id="dinner"
                name="dinner"
                rows={3}
                placeholder="Enter dinner"
            />

            <TextArea
                label="Snacks"
                id="snacks"
                name="snacks"
                rows={3}
                placeholder="Enter snacks"
            />

            {/* ----------------------------- */}
            {/* Macronutrients                */}
            {/* ----------------------------- */}

            <TextInput
                label="Protein (g)"
                id="protein"
                name="protein"
                type="number"
                min={0}
                defaultValue={110}
            />

            <TextInput
                label="Carbs (g)"
                id="carbs"
                name="carbs"
                type="number"
                min={0}
                defaultValue={130}
            />

            <TextInput
                label="Fat (g)"
                id="fat"
                name="fat"
                type="number"
                min={0}
                defaultValue={65}
            />

            <TextInput
                label="Fibre (g)"
                id="fibre"
                name="fibre"
                type="number"
                min={0}
                defaultValue={30}
            />

            <TextInput
                label="Sugar (g)"
                id="sugar"
                name="sugar"
                type="number"
                min={0}
                defaultValue={12}
            />

            <TextInput
                label="Calories Consumed"
                id="calories-consumed"
                name="caloriesConsumed"
                type="number"
                min={0}
                defaultValue={2100}
            />

        </section>

    );
}

export default NutritionSection;