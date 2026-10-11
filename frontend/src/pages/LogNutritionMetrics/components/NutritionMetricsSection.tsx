/*
NutritionMetricsSection

Displays and updates the user's
Nutrition Metrics.

Responsibilities:
- Display Nutrition Metrics fields.
- Update the NutritionMetrics state when values change.
- Keep the UI focused only on Nutrition Metrics data.

The page state is owned by LogNutritionMetrics.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { NutritionMetrics } from "../../../types/NutritionMetrics";


interface NutritionMetricsSectionProps {

    nutritionMetrics: NutritionMetrics;

    setNutritionMetrics: Dispatch<
        SetStateAction<NutritionMetrics>
    >;

}


function NutritionMetricsSection({

    nutritionMetrics,
    setNutritionMetrics,

}: NutritionMetricsSectionProps) {

    /*
    Update a single Nutrition Metrics field.
    */
    function updateNutritionMetric(
        key: keyof NutritionMetrics,
        value: string | number | "",
    ) {

        setNutritionMetrics((previous) => ({

            ...previous,

            [key]: value,

        }));

    }


    return (

        <section>

            <div
                className="
                    grid
                    gap-6
                    md:grid-cols-2
                "
            >

                {/* Dietary Energy */}
                <div className="md:col-span-2">

                    <TextInput
                        label="Dietary Energy (kcal)"
                        id="dietaryEnergyKcal"
                        name="dietaryEnergyKcal"
                        type="number"
                        min={0}
                        step={1}
                        value={nutritionMetrics.dietaryEnergyKcal}
                        onChange={(event) =>
                            updateNutritionMetric(
                                "dietaryEnergyKcal",
                                event.target.value === ""
                                    ? ""
                                    : Number(event.target.value)
                            )
                        }
                    />

                </div>


                {/* Protein */}
                <TextInput
                    label="Protein (g)"
                    id="proteinG"
                    name="proteinG"
                    type="number"
                    min={0}
                    step={0.1}
                    value={nutritionMetrics.proteinG}
                    onChange={(event) =>
                        updateNutritionMetric(
                            "proteinG",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Carbohydrates */}
                <TextInput
                    label="Carbohydrates (g)"
                    id="carbohydratesG"
                    name="carbohydratesG"
                    type="number"
                    min={0}
                    step={0.1}
                    value={nutritionMetrics.carbohydratesG}
                    onChange={(event) =>
                        updateNutritionMetric(
                            "carbohydratesG",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />


                {/* Fiber */}
                <TextInput
                    label="Fiber (g)"
                    id="fiberG"
                    name="fiberG"
                    type="number"
                    min={0}
                    step={0.1}
                    value={nutritionMetrics.fiberG}
                    onChange={(event) =>
                        updateNutritionMetric(
                            "fiberG",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Sugar */}
                <TextInput
                    label="Sugar (g)"
                    id="sugarG"
                    name="sugarG"
                    type="number"
                    min={0}
                    step={0.1}
                    value={nutritionMetrics.sugarG}
                    onChange={(event) =>
                        updateNutritionMetric(
                            "sugarG",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />


                {/* Total Fat */}
                <TextInput
                    label="Total Fat (g)"
                    id="totalFatG"
                    name="totalFatG"
                    type="number"
                    min={0}
                    step={0.1}
                    value={nutritionMetrics.totalFatG}
                    onChange={(event) =>
                        updateNutritionMetric(
                            "totalFatG",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Saturated Fat */}
                <TextInput
                    label="Saturated Fat (g)"
                    id="saturatedFatG"
                    name="saturatedFatG"
                    type="number"
                    min={0}
                    step={0.1}
                    value={nutritionMetrics.saturatedFatG}
                    onChange={(event) =>
                        updateNutritionMetric(
                            "saturatedFatG",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />


                {/* Polyunsaturated Fat */}
                <TextInput
                    label="Polyunsaturated Fat (g)"
                    id="polyunsaturatedFatG"
                    name="polyunsaturatedFatG"
                    type="number"
                    min={0}
                    step={0.1}
                    value={nutritionMetrics.polyunsaturatedFatG}
                    onChange={(event) =>
                        updateNutritionMetric(
                            "polyunsaturatedFatG",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Monounsaturated Fat */}
                <TextInput
                    label="Monounsaturated Fat (g)"
                    id="monounsaturatedFatG"
                    name="monounsaturatedFatG"
                    type="number"
                    min={0}
                    step={0.1}
                    value={nutritionMetrics.monounsaturatedFatG}
                    onChange={(event) =>
                        updateNutritionMetric(
                            "monounsaturatedFatG",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />


                {/* Water */}
                <TextInput
                    label="Water (fl oz)"
                    id="waterFlOzUs"
                    name="waterFlOzUs"
                    type="number"
                    min={0}
                    step={0.1}
                    value={nutritionMetrics.waterFlOzUs}
                    onChange={(event) =>
                        updateNutritionMetric(
                            "waterFlOzUs",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Cholesterol */}
                <TextInput
                    label="Cholesterol (mg)"
                    id="cholesterolMg"
                    name="cholesterolMg"
                    type="number"
                    min={0}
                    step={0.1}
                    value={nutritionMetrics.cholesterolMg}
                    onChange={(event) =>
                        updateNutritionMetric(
                            "cholesterolMg",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />


                {/* Source */}
                <div className="md:col-span-2">

                    <TextInput
                        label="Source"
                        id="source"
                        name="source"
                        type="text"
                        value={nutritionMetrics.source}
                        onChange={(event) =>
                            updateNutritionMetric(
                                "source",
                                event.target.value
                            )
                        }
                    />

                </div>

            </div>

        </section>

    );

}

export default NutritionMetricsSection;