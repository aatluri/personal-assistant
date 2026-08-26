/*
    BodyMeasurementsSection

    Displays and updates the user's
    body measurements.

    Responsibilities:
    - Display body measurement fields.
    - Update the BodyMeasurements state when values change.
    - Keep the UI focused only on body measurement data.

    The page state is owned by LogBodyMeasurements.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { BodyMeasurements } from "../../../types/BodyMeasurements";


/*
    bodyMeasurements
        The current Body Measurements
        displayed on the page.

    setBodyMeasurements
        Callback used to update the page state.
*/
interface BodyMeasurementsSectionProps {

    bodyMeasurements: BodyMeasurements;

    setBodyMeasurements: Dispatch<
        SetStateAction<BodyMeasurements>
    >;

}

function BodyMeasurementsSection({

    bodyMeasurements,
    setBodyMeasurements,

}: BodyMeasurementsSectionProps) {

    /*
        Update a single numeric measurement.

        This helper is shared by all numeric
        measurement fields to avoid repeating
        the same update logic.
    */
    function updateMeasurement(

        key: keyof BodyMeasurements,
        value: number | "",

    ) {

        setBodyMeasurements((previous) => ({

            ...previous,

            [key]: value,

        }));

    }

    /*
        Update only the Notes field while
        preserving the rest of the
        BodyMeasurements object.
    */
    function updateNotes(
        value: string,
    ) {

        setBodyMeasurements((previous) => ({

            ...previous,

            notes: value,

        }));

    }
    /*
        Display the Body Measurements section.
    */
    return (

        <section>

            <div
                className="
                    grid
                    gap-6
                    md:grid-cols-2
                "
            >

                {/* Body Fat */}
                <TextInput
                    label="Body Fat (%)"
                    id="bodyFat"
                    name="bodyFat"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.bodyFat}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "bodyFat",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Muscle Mass */}
                <TextInput
                    label="Muscle Mass (%)"
                    id="muscleMass"
                    name="muscleMass"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.muscleMass}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "muscleMass",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Visceral Fat */}
                <TextInput
                    label="Visceral Fat (%)"
                    id="visceralFat"
                    name="visceralFat"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.visceralFat}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "visceralFat",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                <div />

                {/* Neck */}
                <TextInput
                    label="Neck (cm)"
                    id="neck"
                    name="neck"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.neck}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "neck",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Chest */}
                <TextInput
                    label="Chest (cm)"
                    id="chest"
                    name="chest"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.chest}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "chest",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />
                                {/* Waist */}
                <TextInput
                    label="Waist (cm)"
                    id="waist"
                    name="waist"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.waist}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "waist",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Stomach */}
                <TextInput
                    label="Stomach (cm)"
                    id="stomach"
                    name="stomach"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.stomach}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "stomach",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Left Arm */}
                <TextInput
                    label="Left Arm (cm)"
                    id="leftArm"
                    name="leftArm"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.leftArm}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "leftArm",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Right Arm */}
                <TextInput
                    label="Right Arm (cm)"
                    id="rightArm"
                    name="rightArm"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.rightArm}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "rightArm",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Left Forearm */}
                <TextInput
                    label="Left Forearm (cm)"
                    id="leftForearm"
                    name="leftForearm"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.leftForearm}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "leftForearm",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Right Forearm */}
                <TextInput
                    label="Right Forearm (cm)"
                    id="rightForearm"
                    name="rightForearm"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.rightForearm}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "rightForearm",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Left Thigh */}
                <TextInput
                    label="Left Thigh (cm)"
                    id="leftThigh"
                    name="leftThigh"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.leftThigh}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "leftThigh",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Right Thigh */}
                <TextInput
                    label="Right Thigh (cm)"
                    id="rightThigh"
                    name="rightThigh"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.rightThigh}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "rightThigh",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Left Calf */}
                <TextInput
                    label="Left Calf (cm)"
                    id="leftCalf"
                    name="leftCalf"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.leftCalf}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "leftCalf",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Right Calf */}
                <TextInput
                    label="Right Calf (cm)"
                    id="rightCalf"
                    name="rightCalf"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.rightCalf}
                    /*
                        Update only the selected measurement
                        while preserving the rest of the
                        BodyMeasurements object.
                    */
                    onChange={(event) =>
                        updateMeasurement(
                            "rightCalf",
                            event.target.value === ""
                                ? ""
                                : Number(event.target.value)
                        )
                    }
                />

                {/* Hips */}
                <div className="md:col-span-2">
                    <TextInput
                        label="Hips (cm)"
                        id="hips"
                        name="hips"
                        type="number"
                        min={0}
                        step={0.1}
                        value={bodyMeasurements.hips}
                        /*
                            Update only the selected measurement
                            while preserving the rest of the
                            BodyMeasurements object.
                        */
                        onChange={(event) =>
                            updateMeasurement(
                                "hips",
                                event.target.value === ""
                                    ? ""
                                    : Number(event.target.value)
                            )
                        }
                    />
                </div>

                {/* Notes */}
                <div className="md:col-span-2">
                    <TextInput
                        label="Notes"
                        id="notes"
                        name="notes"
                        type="text"
                        value={bodyMeasurements.notes}
                        /*
                            Update only the Notes field.
                        */
                        onChange={(event) =>
                            updateNotes(event.target.value)
                        }
                    />
                </div>

            </div>

        </section>

    );

}

export default BodyMeasurementsSection;