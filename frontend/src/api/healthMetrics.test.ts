import {
    afterEach,
    beforeEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import {
    getHealthMetric,
    saveHealthMetric,
} from "./healthMetrics";

import {
    createEmptyHealthMetrics,
} from "../utils/createEmptyHealthMetrics";


/*
Mock the browser's fetch() function.

No real HTTP requests are made during
these API unit tests.
*/
globalThis.fetch = vi.fn();


/*
Clean up mock call history after each test.
*/
afterEach(() => {

    vi.clearAllMocks();

});


/*
Configure the default fetch response.

Individual tests can override this response
when required.
*/
beforeEach(() => {

    vi.mocked(fetch).mockResolvedValue({

        ok: true,

        status: 200,

        json: vi.fn().mockResolvedValue({}),

        text: vi.fn(),

    } as unknown as Response);

});


describe("Health Metrics API", () => {

    /*
    Verify that Health Metrics are correctly
    retrieved and converted from the backend
    snake_case model into the frontend model.
    */
    test("returns Health Metrics", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: true,

            status: 200,

            json: vi.fn().mockResolvedValue({

                date: "2026-08-27",

                step_count: 10000,

                active_energy_kcal: 650,
                resting_energy_kcal: 1800,

                atrial_fibrillation_burden_percent: 0,

                blood_oxygen_saturation_percent: 98,

                breathing_disturbances_count: 2,

                cardio_recovery_bpm: 32,

                flights_climbed: 8,

                heart_rate_min_bpm: 42,
                heart_rate_max_bpm: 175,

                heart_rate_variability_ms: 55,

                physical_effort_kcal_hr_kg: 4.2,

                respiratory_rate_bpm: 15,

                resting_heart_rate_bpm: 52,

                source: "Apple Health",

            }),

        } as unknown as Response);


        const healthMetrics =
            await getHealthMetric(
                "2026-08-27"
            );


        expect(healthMetrics).toEqual({

            date: "2026-08-27",

            stepCount: 10000,

            activeEnergyKcal: 650,
            restingEnergyKcal: 1800,

            atrialFibrillationBurdenPercent: 0,

            bloodOxygenSaturationPercent: 98,

            breathingDisturbancesCount: 2,

            cardioRecoveryBpm: 32,

            flightsClimbed: 8,

            heartRateMinBpm: 42,
            heartRateMaxBpm: 175,

            heartRateVariabilityMs: 55,

            physicalEffortKcalHrKg: 4.2,

            respiratoryRateBpm: 15,

            restingHeartRateBpm: 52,

            source: "Apple Health",

        });


        /*
        Verify that the selected date is
        included in the GET endpoint.
        */
        expect(fetch).toHaveBeenCalledWith(

            "http://localhost:8000/health/health-metrics/2026-08-27"

        );

    });


    /*
    Verify that null is returned when no
    Health Metrics record exists for the date.
    */
    test("returns null for 404", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 404,

        } as Response);


        const healthMetrics =
            await getHealthMetric(
                "2026-08-27"
            );


        expect(healthMetrics).toBeNull();

    });


    /*
    Verify that an unexpected backend error
    causes the API function to throw.
    */
    test("throws on server error", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

        } as Response);


        await expect(

            getHealthMetric(
                "2026-08-27"
            )

        ).rejects.toThrow(

            "Failed to load Health Metrics"

        );

    });


    /*
    Verify that saveHealthMetric converts
    the frontend model into the correct
    backend request model.
    */
    test("sends correct Health Metrics request", async () => {

        const healthMetrics =
            createEmptyHealthMetrics();


        healthMetrics.stepCount = 10000;

        healthMetrics.activeEnergyKcal = 650;
        healthMetrics.restingEnergyKcal = 1800;

        healthMetrics.atrialFibrillationBurdenPercent = 0;

        healthMetrics.bloodOxygenSaturationPercent = 98;

        healthMetrics.breathingDisturbancesCount = 2;

        healthMetrics.cardioRecoveryBpm = 32;

        healthMetrics.flightsClimbed = 8;

        healthMetrics.heartRateMinBpm = 42;
        healthMetrics.heartRateMaxBpm = 175;

        healthMetrics.heartRateVariabilityMs = 55;

        healthMetrics.physicalEffortKcalHrKg = 4.2;

        healthMetrics.respiratoryRateBpm = 15;

        healthMetrics.restingHeartRateBpm = 52;

        healthMetrics.source = "Apple Health";


        await saveHealthMetric(
            "2026-08-27",
            healthMetrics
        );


        expect(fetch).toHaveBeenCalledWith(

            "http://localhost:8000/health/health-metrics",

            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({

                    date: "2026-08-27",

                    step_count: 10000,

                    active_energy_kcal: 650,
                    resting_energy_kcal: 1800,

                    atrial_fibrillation_burden_percent: 0,

                    blood_oxygen_saturation_percent: 98,

                    breathing_disturbances_count: 2,

                    cardio_recovery_bpm: 32,

                    flights_climbed: 8,

                    heart_rate_min_bpm: 42,
                    heart_rate_max_bpm: 175,

                    heart_rate_variability_ms: 55,

                    physical_effort_kcal_hr_kg: 4.2,

                    respiratory_rate_bpm: 15,

                    resting_heart_rate_bpm: 52,

                    source: "Apple Health",

                }),
            }
        );

    });


    /*
    Verify that empty numeric and source
    values are converted to null before
    being sent to the backend.
    */
    test("converts empty Health Metrics values to null", async () => {

        const healthMetrics =
            createEmptyHealthMetrics();


        await saveHealthMetric(
            "2026-08-27",
            healthMetrics
        );


        expect(fetch).toHaveBeenCalledTimes(1);


        const fetchOptions =
            vi.mocked(fetch).mock.calls[0][1];


        const requestBody =
            JSON.parse(
                fetchOptions?.body as string
            );


        expect(
            requestBody.step_count
        ).toBeNull();

        expect(
            requestBody.active_energy_kcal
        ).toBeNull();

        expect(
            requestBody.resting_energy_kcal
        ).toBeNull();

        expect(
            requestBody.atrial_fibrillation_burden_percent
        ).toBeNull();

        expect(
            requestBody.blood_oxygen_saturation_percent
        ).toBeNull();

        expect(
            requestBody.breathing_disturbances_count
        ).toBeNull();

        expect(
            requestBody.cardio_recovery_bpm
        ).toBeNull();

        expect(
            requestBody.flights_climbed
        ).toBeNull();

        expect(
            requestBody.heart_rate_min_bpm
        ).toBeNull();

        expect(
            requestBody.heart_rate_max_bpm
        ).toBeNull();

        expect(
            requestBody.heart_rate_variability_ms
        ).toBeNull();

        expect(
            requestBody.physical_effort_kcal_hr_kg
        ).toBeNull();

        expect(
            requestBody.respiratory_rate_bpm
        ).toBeNull();

        expect(
            requestBody.resting_heart_rate_bpm
        ).toBeNull();

        expect(
            requestBody.source
        ).toBeNull();

    });


    /*
    Verify that an error is thrown when
    saving Health Metrics fails.
    */
    test("throws on Health Metrics save failure", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

            text: vi.fn().mockResolvedValue(
                "Server error"
            ),

        } as unknown as Response);


        const healthMetrics =
            createEmptyHealthMetrics();


        await expect(

            saveHealthMetric(
                "2026-08-27",
                healthMetrics
            )

        ).rejects.toThrow(

            "Failed to save Health Metrics"

        );

    });

});