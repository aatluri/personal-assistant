/*
    NutritionSection

    Displays and updates the user's
    meals and nutritional information.

    Responsibilities:
    - Display meal and nutrition fields.
    - Update the DailyLog state when values change.
    - Keep the UI focused only on nutrition data.

    The page state is owned by LogToday.
*/

import type { Dispatch, SetStateAction } from "react";

import TextArea from "../../../components/TextArea";
import TextInput from "../../../components/TextInput";
import type { DailyLog } from "../../../types/DailyLog";

/*
    dailyLog
        The current Daily Log displayed on the page.

    setDailyLog
        Callback used to update the page state.
*/
interface NutritionSectionProps {

    // Complete Daily Log state
    dailyLog: DailyLog;

    // Function used to update the Daily Log
    setDailyLog: Dispatch<SetStateAction<DailyLog>>;

}

function NutritionSection({

    dailyLog,

    setDailyLog,

}: NutritionSectionProps) {

    /*
        Display the Nutrition section.

        This section contains:
        - Meals
        - Macronutrients
        - Calories
    */

    return (

        <section>

            <div
            className="
                    space-y-6
                "
            >
               {/* Meals */}

                <TextArea
                    label="Breakfast"
                    id="breakfast"
                    name="breakfast"
                    rows={3}
                    placeholder="Enter breakfast"
                    value={dailyLog.nutrition.breakfast}
                    /*
                        Update only the Breakfast value while
                        preserving the rest of the DailyLog.
                    */
                    onChange={(event) => {

                        const newBreakfast = event.target.value;

                        setDailyLog((previousDailyLog) => ({

                            ...previousDailyLog,

                            nutrition: {

                                ...previousDailyLog.nutrition,

                                breakfast: newBreakfast,

                            },

                        }));

                    }}
                />

                <TextArea
                    label="Lunch"
                    id="lunch"
                    name="lunch"
                    rows={3}
                    placeholder="Enter lunch"
                    value={dailyLog.nutrition.lunch}
                    /*
                        Update only the lunch value while
                        preserving the rest of the DailyLog.
                    */
                    onChange={(event) => {

                        const newLunch = event.target.value;

                        setDailyLog((previousDailyLog) => ({

                            ...previousDailyLog,

                            nutrition: {

                                ...previousDailyLog.nutrition,

                                lunch: newLunch,

                            },

                        }));

                    }}
                />

                <TextArea
                    label="Dinner"
                    id="dinner"
                    name="dinner"
                    rows={3}
                    placeholder="Enter dinner"
                    value={dailyLog.nutrition.dinner}
                    /*
                        Update only the Dinner value while
                        preserving the rest of the DailyLog.
                    */
                    onChange={(event) => {

                        const newDinner = event.target.value;

                        setDailyLog((previousDailyLog) => ({

                            ...previousDailyLog,

                            nutrition: {

                                ...previousDailyLog.nutrition,

                                dinner: newDinner,

                            },

                        }));

                    }}
                />

                <TextArea
                    label="Snacks"
                    id="snacks"
                    name="snacks"
                    rows={3}
                    placeholder="Enter snacks"
                    value={dailyLog.nutrition.snacks}
                    /*
                        Update only the Snacks value while
                        preserving the rest of the DailyLog.
                    */
                    onChange={(event) => {

                        const newSnacks = event.target.value;

                        setDailyLog((previousDailyLog) => ({

                            ...previousDailyLog,

                            nutrition: {

                                ...previousDailyLog.nutrition,

                                snacks: newSnacks,

                            },

                        }));

                    }}
                />

                {/* Macronutrients                */}
                <div
                    className="
                        grid
                        grid-cols-1
                        md:grid-cols-2
                        gap-4
                    "
                >
                    <TextInput
                        label="Protein (g)"
                        id="protein"
                        name="protein"
                        type="number"
                        min={0}
                        value={dailyLog.nutrition.protein}
                        /*
                            Update only the Protein value while
                            preserving the rest of the DailyLog.
                        */
                        onChange={(event) => {
                            const newProtein = event.target.value === ""? "": Number(event.target.value);
                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                nutrition: {
                                    ...previousDailyLog.nutrition,
                                    protein: newProtein,
                                },
                            }));
                        }}
                    />

                    <TextInput
                        label="Carbs (g)"
                        id="carbs"
                        name="carbs"
                        type="number"
                        min={0}
                        value={dailyLog.nutrition.carbs}
                        /*
                            Update only the Carbs value while
                            preserving the rest of the DailyLog.
                        */
                        onChange={(event) => {
                            const newCarbs = event.target.value === ""? "": Number(event.target.value);
                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                nutrition: {
                                    ...previousDailyLog.nutrition,
                                    carbs: newCarbs,
                                },
                            }));
                        }}
                    />
                </div>

                <div
                    className="
                        grid
                        grid-cols-1
                        md:grid-cols-2
                        gap-4
                    "
                >
                    <TextInput
                        label="Fat (g)"
                        id="fat"
                        name="fat"
                        type="number"
                        min={0}
                        value={dailyLog.nutrition.fat}
                        /*
                            Update only the Fat value while
                            preserving the rest of the DailyLog.
                        */
                        onChange={(event) => {
                            const newFat = event.target.value === ""? "": Number(event.target.value);
                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                nutrition: {
                                    ...previousDailyLog.nutrition,
                                    fat: newFat,
                                },
                            }));

                        }}
                    />

                    <TextInput
                        label="Fibre (g)"
                        id="fibre"
                        name="fibre"
                        type="number"
                        min={0}
                        value={dailyLog.nutrition.fibre}
                        /*
                            Update only the Fibre value while
                            preserving the rest of the DailyLog.
                        */
                        onChange={(event) => {
                            const newFibre = event.target.value === ""? "": Number(event.target.value);
                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                nutrition: {
                                    ...previousDailyLog.nutrition,
                                    fibre: newFibre,
                                },
                            }));
                        }}
                    />
                </div>

                <div
                    className="
                        grid
                        grid-cols-1
                        md:grid-cols-2
                        gap-4
                    "
                >

                    <TextInput
                        label="Sugar (g)"
                        id="sugar"
                        name="sugar"
                        type="number"
                        min={0}
                        value={dailyLog.nutrition.sugar}
                        /*
                            Update only the Sugar value while
                            preserving the rest of the DailyLog.
                        */
                        onChange={(event) => {
                            const newSugar = event.target.value === ""? "": Number(event.target.value);
                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                nutrition: {
                                    ...previousDailyLog.nutrition,
                                    sugar: newSugar,
                                },
                            }));
                        }}
                    />

                    <TextInput
                        label="Calories Consumed"
                        id="calories-consumed"
                        name="caloriesConsumed"
                        type="number"
                        min={0}
                        value={dailyLog.nutrition.caloriesConsumed}
                        /*
                            Update only the Calories Consumed value while
                            preserving the rest of the DailyLog.
                        */
                        onChange={(event) => {
                            const newCaloriesConsumed = event.target.value === ""? "": Number(event.target.value);
                            setDailyLog((previousDailyLog) => ({
                                ...previousDailyLog,
                                nutrition: {
                                    ...previousDailyLog.nutrition,
                                    caloriesConsumed: newCaloriesConsumed,
                                },
                            }));
                        }}
                    />
                </div>
            </div>

        </section>

    );

}

export default NutritionSection;