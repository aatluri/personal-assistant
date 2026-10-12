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

import HealthMetricsSection from "./HealthMetricsSection";

import type { HealthMetrics } from "../../../types/HealthMetrics";
import { createEmptyHealthMetrics } from "../../../utils/createEmptyHealthMetrics";


/*
Clean up the rendered components after each test.

This ensures each test starts with
a clean virtual DOM.
*/
afterEach(() => {
    cleanup();
});


/*
HealthMetricsSection Tests

The tests verify:
- All Health Metrics fields are rendered correctly.
- Existing Health Metrics values are displayed correctly.
- Updating each field calls setHealthMetrics().
- The correct Health Metrics property is updated.
*/


describe("HealthMetricsSection", () => {

    // Verify that all Health Metrics fields are displayed.
    test("renders Health Metrics fields", () => {

        const healthMetrics =
            createEmptyHealthMetrics();

        render(
            <HealthMetricsSection
                healthMetrics={healthMetrics}
                setHealthMetrics={vi.fn()}
            />
        );

        expect(
            screen.getByLabelText("Step Count")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Flights Climbed")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Active Energy (kcal)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Resting Energy (kcal)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Physical Effort (kcal/hr·kg)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Heart Rate Min (bpm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Heart Rate Max (bpm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Resting Heart Rate (bpm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Heart Rate Variability (ms)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Cardio Recovery (bpm)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Blood Oxygen Saturation (%)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Respiratory Rate (breaths/min)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Breathing Disturbances")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Atrial Fibrillation Burden (%)")
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText("Source")
        ).toBeInTheDocument();

    });


    // Verify that supplied Health Metrics values are displayed.
    test("renders supplied values", () => {

        const healthMetrics =
            createEmptyHealthMetrics();

        healthMetrics.stepCount = 10000;
        healthMetrics.flightsClimbed = 8;

        healthMetrics.activeEnergyKcal = 650;
        healthMetrics.restingEnergyKcal = 1800;
        healthMetrics.physicalEffortKcalHrKg = 4.2;

        healthMetrics.heartRateMinBpm = 42;
        healthMetrics.heartRateMaxBpm = 175;
        healthMetrics.restingHeartRateBpm = 52;
        healthMetrics.heartRateVariabilityMs = 55;
        healthMetrics.cardioRecoveryBpm = 32;

        healthMetrics.bloodOxygenSaturationPercent = 98;
        healthMetrics.respiratoryRateBpm = 15;
        healthMetrics.breathingDisturbancesCount = 2;
        healthMetrics.atrialFibrillationBurdenPercent = 0;

        healthMetrics.source = "Apple Health";


        render(
            <HealthMetricsSection
                healthMetrics={healthMetrics}
                setHealthMetrics={vi.fn()}
            />
        );


        expect(
            screen.getByLabelText("Step Count")
        ).toHaveValue(10000);

        expect(
            screen.getByLabelText("Flights Climbed")
        ).toHaveValue(8);

        expect(
            screen.getByLabelText("Active Energy (kcal)")
        ).toHaveValue(650);

        expect(
            screen.getByLabelText("Resting Energy (kcal)")
        ).toHaveValue(1800);

        expect(
            screen.getByLabelText("Physical Effort (kcal/hr·kg)")
        ).toHaveValue(4.2);

        expect(
            screen.getByLabelText("Heart Rate Min (bpm)")
        ).toHaveValue(42);

        expect(
            screen.getByLabelText("Heart Rate Max (bpm)")
        ).toHaveValue(175);

        expect(
            screen.getByLabelText("Resting Heart Rate (bpm)")
        ).toHaveValue(52);

        expect(
            screen.getByLabelText("Heart Rate Variability (ms)")
        ).toHaveValue(55);

        expect(
            screen.getByLabelText("Cardio Recovery (bpm)")
        ).toHaveValue(32);

        expect(
            screen.getByLabelText("Blood Oxygen Saturation (%)")
        ).toHaveValue(98);

        expect(
            screen.getByLabelText("Respiratory Rate (breaths/min)")
        ).toHaveValue(15);

        expect(
            screen.getByLabelText("Breathing Disturbances")
        ).toHaveValue(2);

        expect(
            screen.getByLabelText("Atrial Fibrillation Burden (%)")
        ).toHaveValue(0);

        expect(
            screen.getByLabelText("Source")
        ).toHaveValue("Apple Health");

    });


    /*
    Helper used by the numeric field tests.

    It verifies that changing an input updates
    the correct property in HealthMetrics.
    */
    function testNumericField(
        testName: string,
        label: string,
        field: keyof HealthMetrics,
        inputValue: string,
        expectedValue: number,
    ) {

        test(testName, () => {

            const healthMetrics =
                createEmptyHealthMetrics();

            const setHealthMetrics = vi.fn();


            render(
                <HealthMetricsSection
                    healthMetrics={healthMetrics}
                    setHealthMetrics={setHealthMetrics}
                />
            );


            fireEvent.change(
                screen.getByLabelText(label),
                {
                    target: {
                        value: inputValue,
                    },
                }
            );


            expect(
                setHealthMetrics
            ).toHaveBeenCalled();


            const updateFunction =
                setHealthMetrics.mock.calls[0][0] as (
                    healthMetrics: HealthMetrics
                ) => HealthMetrics;


            const previousHealthMetrics =
                createEmptyHealthMetrics();


            const updatedHealthMetrics =
                updateFunction(previousHealthMetrics);


            expect(
                updatedHealthMetrics[field]
            ).toBe(expectedValue);

        });

    }


    testNumericField(
        "updates step count",
        "Step Count",
        "stepCount",
        "10000",
        10000
    );


    testNumericField(
        "updates flights climbed",
        "Flights Climbed",
        "flightsClimbed",
        "8",
        8
    );


    testNumericField(
        "updates active energy",
        "Active Energy (kcal)",
        "activeEnergyKcal",
        "650.5",
        650.5
    );


    testNumericField(
        "updates resting energy",
        "Resting Energy (kcal)",
        "restingEnergyKcal",
        "1800.5",
        1800.5
    );


    testNumericField(
        "updates physical effort",
        "Physical Effort (kcal/hr·kg)",
        "physicalEffortKcalHrKg",
        "4.2",
        4.2
    );


    testNumericField(
        "updates minimum heart rate",
        "Heart Rate Min (bpm)",
        "heartRateMinBpm",
        "42",
        42
    );


    testNumericField(
        "updates maximum heart rate",
        "Heart Rate Max (bpm)",
        "heartRateMaxBpm",
        "175",
        175
    );


    testNumericField(
        "updates resting heart rate",
        "Resting Heart Rate (bpm)",
        "restingHeartRateBpm",
        "52",
        52
    );


    testNumericField(
        "updates heart rate variability",
        "Heart Rate Variability (ms)",
        "heartRateVariabilityMs",
        "55.5",
        55.5
    );


    testNumericField(
        "updates cardio recovery",
        "Cardio Recovery (bpm)",
        "cardioRecoveryBpm",
        "32",
        32
    );


    testNumericField(
        "updates blood oxygen saturation",
        "Blood Oxygen Saturation (%)",
        "bloodOxygenSaturationPercent",
        "98.5",
        98.5
    );


    testNumericField(
        "updates respiratory rate",
        "Respiratory Rate (breaths/min)",
        "respiratoryRateBpm",
        "15.5",
        15.5
    );


    testNumericField(
        "updates breathing disturbances",
        "Breathing Disturbances",
        "breathingDisturbancesCount",
        "2.5",
        2.5
    );


    testNumericField(
        "updates atrial fibrillation burden",
        "Atrial Fibrillation Burden (%)",
        "atrialFibrillationBurdenPercent",
        "1.5",
        1.5
    );


    // Verify that changing Source updates HealthMetrics.
    test("updates source", () => {

        const healthMetrics =
            createEmptyHealthMetrics();

        const setHealthMetrics = vi.fn();


        render(
            <HealthMetricsSection
                healthMetrics={healthMetrics}
                setHealthMetrics={setHealthMetrics}
            />
        );


        fireEvent.change(
            screen.getByLabelText("Source"),
            {
                target: {
                    value: "Apple Health",
                },
            }
        );


        expect(
            setHealthMetrics
        ).toHaveBeenCalled();


        const updateFunction =
            setHealthMetrics.mock.calls[0][0] as (
                healthMetrics: HealthMetrics
            ) => HealthMetrics;


        const previousHealthMetrics =
            createEmptyHealthMetrics();


        const updatedHealthMetrics =
            updateFunction(previousHealthMetrics);


        expect(
            updatedHealthMetrics.source
        ).toBe("Apple Health");

    });

});