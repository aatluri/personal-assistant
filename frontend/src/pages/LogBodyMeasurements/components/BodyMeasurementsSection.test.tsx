import {
    cleanup,
    fireEvent,
    render,
    screen,
} from "@testing-library/react";

import {
    afterEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import BodyMeasurementsSection from "./BodyMeasurementsSection";

import type { BodyMeasurements } from "../../../types/BodyMeasurements";
import { createEmptyBodyMeasurements } from "../../../utils/createEmptyBodyMeasurements";

/*
    Clean up the rendered components after each test.

    This ensures each test starts with
    a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});

/*
    BodyMeasurementsSection Tests

    Each test follows the same sequence:

    1. Render the BodyMeasurementsSection component.
    2. Provide the required props.
    3. Simulate user interaction if needed.
    4. Verify that the BodyMeasurementsSection behaves as expected.

    The tests verify:
    - All body measurement fields are rendered correctly.
    - Existing measurement values are displayed correctly.
    - Updating a measurement calls setBodyMeasurements().
    - Only the relevant measurement field is updated while
      the rest of the BodyMeasurements object is preserved.
*/

describe("BodyMeasurementsSection", () => {
    // Verify that all Body Measurement fields are displayed.
    test("renders measurement fields", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={vi.fn()}
            />
        );

        expect(
            screen.getByLabelText("Body Fat (%)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Muscle Mass (%)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Visceral Fat (%)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Neck (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Chest (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Waist (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Stomach (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Left Arm (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Right Arm (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Left Forearm (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Right Forearm (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Left Thigh (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Right Thigh (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Left Calf (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Right Calf (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Hips (cm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Notes")
        ).toBeInTheDocument();

    });


    // Verify that the supplied measurement values are displayed.
    test("renders supplied values", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        bodyMeasurements.bodyFat = 18.5;
        bodyMeasurements.muscleMass = 42.3;
        bodyMeasurements.visceralFat = 8;
        bodyMeasurements.neck = 38;
        bodyMeasurements.chest = 102;
        bodyMeasurements.waist = 86;
        bodyMeasurements.stomach = 90;
        bodyMeasurements.leftArm = 34;
        bodyMeasurements.rightArm = 34.5;
        bodyMeasurements.leftForearm = 29;
        bodyMeasurements.rightForearm = 29.5;
        bodyMeasurements.leftThigh = 58;
        bodyMeasurements.rightThigh = 58.5;
        bodyMeasurements.leftCalf = 39;
        bodyMeasurements.rightCalf = 39.5;
        bodyMeasurements.hips = 98;
        bodyMeasurements.notes = "Feeling stronger";

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={vi.fn()}
            />
        );

        expect(
            screen.getByDisplayValue("18.5")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("42.3")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("8")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("38")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("102")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("86")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("90")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("34")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("34.5")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("29")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("29.5")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("58")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("58.5")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("39")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("39.5")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("98")
        ).toBeInTheDocument();

        expect(
            screen.getByDisplayValue("Feeling stronger")
        ).toBeInTheDocument();

    });

    // Verify that changing Body Fat updates the BodyMeasurements.
    test("updates body fat", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Body Fat (%)"),
            {
                target: {
                    value: "18.5",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.bodyFat
        ).toBe(18.5);

    });


    // Verify that changing Muscle Mass updates the BodyMeasurements.
    test("updates muscle mass", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Muscle Mass (%)"),
            {
                target: {
                    value: "42.3",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.muscleMass
        ).toBe(42.3);

    });


    // Verify that changing Visceral Fat updates the BodyMeasurements.
    test("updates visceral fat", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Visceral Fat (%)"),
            {
                target: {
                    value: "8",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.visceralFat
        ).toBe(8);

    });


    // Verify that changing Neck updates the BodyMeasurements.
    test("updates neck", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Neck (cm)"),
            {
                target: {
                    value: "38",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.neck
        ).toBe(38);

    });


    // Verify that changing Chest updates the BodyMeasurements.
    test("updates chest", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Chest (cm)"),
            {
                target: {
                    value: "102",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.chest
        ).toBe(102);

    });


    // Verify that changing Waist updates the BodyMeasurements.
    test("updates waist", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Waist (cm)"),
            {
                target: {
                    value: "86",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.waist
        ).toBe(86);

    });


    // Verify that changing Stomach updates the BodyMeasurements.
    test("updates stomach", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Stomach (cm)"),
            {
                target: {
                    value: "90",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.stomach
        ).toBe(90);

    });


    // Verify that changing Left Arm updates the BodyMeasurements.
    test("updates left arm", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Left Arm (cm)"),
            {
                target: {
                    value: "34",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.leftArm
        ).toBe(34);

    });


    // Verify that changing Right Arm updates the BodyMeasurements.
    test("updates right arm", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Right Arm (cm)"),
            {
                target: {
                    value: "34.5",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.rightArm
        ).toBe(34.5);

    });


    // Verify that changing Left Forearm updates the BodyMeasurements.
    test("updates left forearm", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Left Forearm (cm)"),
            {
                target: {
                    value: "29",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.leftForearm
        ).toBe(29);

    });


    // Verify that changing Right Forearm updates the BodyMeasurements.
    test("updates right forearm", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Right Forearm (cm)"),
            {
                target: {
                    value: "29.5",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.rightForearm
        ).toBe(29.5);

    });


    // Verify that changing Left Thigh updates the BodyMeasurements.
    test("updates left thigh", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Left Thigh (cm)"),
            {
                target: {
                    value: "58",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.leftThigh
        ).toBe(58);

    });


    // Verify that changing Right Thigh updates the BodyMeasurements.
    test("updates right thigh", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Right Thigh (cm)"),
            {
                target: {
                    value: "58.5",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.rightThigh
        ).toBe(58.5);

    });


    // Verify that changing Left Calf updates the BodyMeasurements.
    test("updates left calf", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Left Calf (cm)"),
            {
                target: {
                    value: "39",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.leftCalf
        ).toBe(39);

    });


    // Verify that changing Right Calf updates the BodyMeasurements.
    test("updates right calf", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Right Calf (cm)"),
            {
                target: {
                    value: "39.5",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.rightCalf
        ).toBe(39.5);

    });


    // Verify that changing Hips updates the BodyMeasurements.
    test("updates hips", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Hips (cm)"),
            {
                target: {
                    value: "98",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.hips
        ).toBe(98);

    });


    // Verify that changing Notes updates the BodyMeasurements.
    test("updates notes", () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        const setBodyMeasurements = vi.fn();

        render(
            <BodyMeasurementsSection
                bodyMeasurements={bodyMeasurements}
                setBodyMeasurements={setBodyMeasurements}
            />
        );

        fireEvent.change(
            screen.getByLabelText("Notes"),
            {
                target: {
                    value: "Feeling stronger",
                },
            }
        );

        expect(setBodyMeasurements).toHaveBeenCalled();

        const updateFunction =
            setBodyMeasurements.mock.calls[0][0] as (
                bodyMeasurements: BodyMeasurements
            ) => BodyMeasurements;

        const previousBodyMeasurements =
            createEmptyBodyMeasurements();

        const updatedBodyMeasurements =
            updateFunction(previousBodyMeasurements);

        expect(
            updatedBodyMeasurements.notes
        ).toBe("Feeling stronger");

    });

});