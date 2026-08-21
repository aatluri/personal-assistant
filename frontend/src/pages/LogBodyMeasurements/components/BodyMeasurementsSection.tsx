/*
    BodyMeasurementsSection

    Displays and edits the user's
    body measurements.
*/

import type { Dispatch, SetStateAction } from "react";

import TextInput from "../../../components/TextInput";
import type { BodyMeasurements } from "../../../types/BodyMeasurements";

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
        Update the notes field.
    */
    function updateNotes(
        value: string,
    ) {

        setBodyMeasurements((previous) => ({

            ...previous,

            notes: value,

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

                {/* Body Fat */}
                <TextInput
                    label="Body Fat (%)"
                    id="bodyFat"
                    name="bodyFat"
                    type="number"
                    min={0}
                    step={0.1}
                    value={bodyMeasurements.bodyFat}
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