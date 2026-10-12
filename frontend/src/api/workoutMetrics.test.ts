import {
    afterEach,
    beforeEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import {
    getWorkoutMetricsByDate,
    saveWorkoutMetric,
} from "./workoutMetrics";

import {
    createEmptyWorkoutMetrics,
} from "../utils/createEmptyWorkoutMetrics";


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

        json: vi.fn().mockResolvedValue([]),

        text: vi.fn(),

    } as unknown as Response);

});


describe("Workout Metrics API", () => {

    /*
    Verify that Workout Metrics are correctly
    retrieved and converted from the backend
    snake_case model into the frontend model.
    */
    test("returns Workout Metrics for a date", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: true,

            status: 200,

            json: vi.fn().mockResolvedValue([

                {
                    date: "2026-08-27",

                    workout_type: "Running",

                    workout_start_time:
                        "2026-08-27T07:30:00",

                    workout_end_time:
                        "2026-08-27T08:15:00",

                    workout_duration: "45 min",

                    total_energy_kcal: 500,
                    active_energy_kcal: 420,

                    max_heart_rate_bpm: 175,
                    avg_heart_rate_bpm: 150,

                    distance_mi: 3.1,
                    avg_speed_mph: 6.5,
                },

            ]),

        } as unknown as Response);


        const workouts =
            await getWorkoutMetricsByDate(
                "2026-08-27"
            );


        expect(workouts).toEqual([

            {
                date: "2026-08-27",

                workoutType: "Running",

                workoutStartTime: "07:30:00",
                workoutEndTime: "08:15:00",

                workoutDuration: "45 min",

                totalEnergyKcal: 500,
                activeEnergyKcal: 420,

                maxHeartRateBpm: 175,
                avgHeartRateBpm: 150,

                distanceMi: 3.1,
                avgSpeedMph: 6.5,
            },

        ]);


        /*
        Also verify that the selected date was
        sent to the backend as a query parameter.
        */
        expect(fetch).toHaveBeenCalledWith(

            "http://localhost:8000/health/workout-metrics?workout_date=2026-08-27"

        );

    });


    /*
    A date can legitimately have no workouts.

    The backend returns an empty array in this case,
    which should remain an empty array in the frontend.
    */
    test("returns empty array when no workouts exist", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: true,

            status: 200,

            json: vi.fn().mockResolvedValue([]),

        } as unknown as Response);


        const workouts =
            await getWorkoutMetricsByDate(
                "2026-08-27"
            );


        expect(workouts).toEqual([]);

    });


    /*
    Verify that an error is thrown when the backend
    returns an unsuccessful response.
    */
    test("throws on server error", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

        } as Response);


        await expect(

            getWorkoutMetricsByDate(
                "2026-08-27"
            )

        ).rejects.toThrow(

            "Failed to load Workout Metrics"

        );

    });


    /*
    Verify that saveWorkoutMetric converts the
    frontend WorkoutMetrics model into the
    correct backend request.

    Times should be converted into complete
    date-time values.
    */
    test("sends correct Workout Metrics request", async () => {

        const workout =
            createEmptyWorkoutMetrics();


        workout.date = "2026-08-27";

        workout.workoutType = "Running";

        workout.workoutStartTime = "07:30:00";
        workout.workoutEndTime = "08:15:00";

        workout.workoutDuration = "45 min";

        workout.totalEnergyKcal = 500;
        workout.activeEnergyKcal = 420;

        workout.maxHeartRateBpm = 175;
        workout.avgHeartRateBpm = 150;

        workout.distanceMi = 3.1;
        workout.avgSpeedMph = 6.5;


        await saveWorkoutMetric(workout);


        expect(fetch).toHaveBeenCalledWith(

            "http://localhost:8000/health/workout-metrics",

            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({

                    date: "2026-08-27",

                    workout_type: "Running",

                    workout_start_time:
                        "2026-08-27T07:30:00",

                    workout_end_time:
                        "2026-08-27T08:15:00",

                    workout_duration: "45 min",

                    total_energy_kcal: 500,
                    active_energy_kcal: 420,

                    max_heart_rate_bpm: 175,
                    avg_heart_rate_bpm: 150,

                    distance_mi: 3.1,
                    avg_speed_mph: 6.5,

                }),
            }
        );

    });


    /*
    Verify that empty numeric and time values
    are converted to null before being sent
    to the backend.
    */
    test("converts empty Workout Metrics values to null", async () => {

        const workout =
            createEmptyWorkoutMetrics();

        workout.date = "2026-08-27";


        await saveWorkoutMetric(workout);


        expect(fetch).toHaveBeenCalledTimes(1);


        const fetchOptions =
            vi.mocked(fetch).mock.calls[0][1];


        const requestBody =
            JSON.parse(
                fetchOptions?.body as string
            );


        expect(
            requestBody.workout_start_time
        ).toBeNull();

        expect(
            requestBody.workout_end_time
        ).toBeNull();


        expect(
            requestBody.total_energy_kcal
        ).toBeNull();

        expect(
            requestBody.active_energy_kcal
        ).toBeNull();

        expect(
            requestBody.max_heart_rate_bpm
        ).toBeNull();

        expect(
            requestBody.avg_heart_rate_bpm
        ).toBeNull();

        expect(
            requestBody.distance_mi
        ).toBeNull();

        expect(
            requestBody.avg_speed_mph
        ).toBeNull();

    });


    /*
    Verify that an error is thrown when
    saving Workout Metrics fails.
    */
    test("throws on Workout Metrics save failure", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

            text: vi.fn().mockResolvedValue(
                "Server error"
            ),

        } as unknown as Response);


        const workout =
            createEmptyWorkoutMetrics();

        workout.date = "2026-08-27";


        await expect(

            saveWorkoutMetric(workout)

        ).rejects.toThrow(

            "Failed to save Workout Metrics"

        );

    });

    test("returns multiple workouts for the same date", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: true,

            status: 200,

            json: vi.fn().mockResolvedValue([

                {
                    date: "2026-08-27",
                    workout_type: "Running",
                    workout_start_time: "2026-08-27T07:00:00",
                    workout_end_time: "2026-08-27T08:00:00",
                    workout_duration: "60 min",
                },

                {
                    date: "2026-08-27",
                    workout_type: "Strength Training",
                    workout_start_time: "2026-08-27T18:00:00",
                    workout_end_time: "2026-08-27T19:00:00",
                    workout_duration: "60 min",
                },

            ]),

        } as unknown as Response);


        const workouts =
            await getWorkoutMetricsByDate(
                "2026-08-27"
            );


        expect(workouts).toHaveLength(2);

        expect(workouts[0].workoutType)
            .toBe("Running");

        expect(workouts[0].workoutStartTime)
            .toBe("07:00:00");

        expect(workouts[1].workoutType)
            .toBe("Strength Training");

        expect(workouts[1].workoutStartTime)
            .toBe("18:00:00");

    });

});