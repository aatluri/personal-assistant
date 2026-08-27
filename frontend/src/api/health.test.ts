import {
    afterEach,
    beforeEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import {
    getDailyLog,
    saveDailyLog,
    getBodyMeasurement,
    saveBodyMeasurement,
} from "./health";

import { createEmptyDailyLog } from "../utils/createEmptyDailyLog";
import { createEmptyBodyMeasurements } from "../utils/createEmptyBodyMeasurements";

/*
    Mock the browser's fetch() function.

    The Health API communicates with the backend
    using fetch().

    During unit testing we replace the real fetch()
    implementation with a mock so that:
    - No real HTTP requests are made.
    - We can control the responses returned by
      the backend.
    - We can verify that the correct requests
      were sent.
*/
globalThis.fetch = vi.fn();

/*
    Clean up after each test.

    This removes any mock call history so that
    each test starts with a clean environment.
*/
afterEach(() => {

    vi.clearAllMocks();

});

/*
    Configure the default fetch() behaviour.

    Unless a test overrides it, every HTTP request
    returns a successful (200 OK) response with
    an empty JSON object.
*/
beforeEach(() => {

    vi.mocked(fetch).mockResolvedValue({

        ok: true,

        status: 200,

        json: vi.fn().mockResolvedValue({}),

        text: vi.fn(),

    } as unknown as Response);

});

/*
    Health API Tests

    Each test follows the same sequence:

    1. Arrange the mock HTTP response.
    2. Call the Health API function.
    3. Verify the returned data or request.
    4. Verify any errors are handled correctly.

    The tests verify:
    - Daily Logs are loaded correctly.
    - Daily Logs are saved correctly.
    - Body Measurements are loaded correctly.
    - Body Measurements are saved correctly.
    - Backend models are converted into frontend models.
    - Frontend models are converted into backend request models.
    - Error responses are handled correctly.
*/

describe("Health API", () => {

    // Verify that a Daily Log is correctly
    // retrieved and converted into the
    // frontend DailyLog model.
    test("returns DailyLog", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: true,

            status: 200,

            json: vi.fn().mockResolvedValue({

                weight_kg: 80.5,

                workout_type: "HIIT",

                workout_duration_min: 60,

                workout_calories_burnt: 700,

                workout_summary: "Push-ups",

                steps: 10000,

                total_calories_burnt: 2500,

                breakfast: "Eggs",

                lunch: "Chicken",

                dinner: "Fish",

                snacks: "Nuts",

                protein_g: 120,

                carbs_g: 150,

                fat_g: 60,

                fibre_g: 25,

                sugar_g: 20,

                calories_consumed: 2200,

                water_ml: 3000,

                first_meal_time: "2026-08-27T08:30:00",

                last_meal_time: "2026-08-27T20:00:00",

                sleep_start_time: "2026-08-26T23:00:00",

                sleep_end_time: "2026-08-27T07:00:00",

                notes: "Feeling good",

            }),

        } as unknown as Response);

        const dailyLog =
            await getDailyLog("2026-08-27");

        expect(dailyLog).toEqual({

            body: {
                weight: 80.5,
            },

            workout: {
                workoutType: "HIIT",
                workoutDuration: 60,
                workoutCalories: 700,
                workoutVolume: 0,
                workoutSets: 0,
                averageHeartRate: 0,
                workoutSummary: "Push-ups",
            },

            activity: {
                steps: 10000,
                totalCaloriesBurnt: 2500,
            },

            mealTiming: {
                firstMealTime: "08:30",
                lastMealTime: "20:00",
            },

            nutrition: {
                breakfast: "Eggs",
                lunch: "Chicken",
                dinner: "Fish",
                snacks: "Nuts",
                protein: 120,
                carbs: 150,
                fat: 60,
                fibre: 25,
                sugar: 20,
                caloriesConsumed: 2200,
            },

            hydration: {
                water: 3000,
            },

            sleep: {
                sleepStartTime: "23:00",
                sleepEndTime: "07:00",
            },

            notes: {
                notes: "Feeling good",
            },

        });

    });


    // Verify that null is returned when
    // the backend indicates that no
    // Daily Log exists.
    test("returns null for 404", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 404,

        } as Response);

        const dailyLog =
            await getDailyLog("2026-08-27");

        expect(dailyLog).toBeNull();

    });


    // Verify that an error is thrown when
    // the backend returns an unexpected
    // server error.
    test("throws on server error", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

        } as Response);

        await expect(

            getDailyLog("2026-08-27")

        ).rejects.toThrow(

            "Failed to load Daily Log"

        );

    });

    // Verify that saveDailyLog sends the correct request to the backend.
    test("sends correct Daily Log request", async () => {

        const dailyLog =
            createEmptyDailyLog();

        dailyLog.body.weight = 80.5;

        dailyLog.workout.workoutType = "HIIT";
        dailyLog.workout.workoutSummary = "Push-ups";
        dailyLog.workout.workoutDuration = 60;
        dailyLog.workout.workoutCalories = 700;

        dailyLog.activity.steps = 10000;
        dailyLog.activity.totalCaloriesBurnt = 2500;

        dailyLog.nutrition.breakfast = "Eggs";
        dailyLog.nutrition.lunch = "Chicken";
        dailyLog.nutrition.dinner = "Fish";
        dailyLog.nutrition.snacks = "Nuts";

        dailyLog.nutrition.protein = 120;
        dailyLog.nutrition.carbs = 150;
        dailyLog.nutrition.fibre = 25;
        dailyLog.nutrition.fat = 60;
        dailyLog.nutrition.sugar = 20;
        dailyLog.nutrition.caloriesConsumed = 2200;

        dailyLog.hydration.water = 3000;

        dailyLog.mealTiming.firstMealTime = "08:30";
        dailyLog.mealTiming.lastMealTime = "20:00";

        dailyLog.sleep.sleepStartTime = "23:00";
        dailyLog.sleep.sleepEndTime = "07:00";

        dailyLog.notes.notes = "Feeling good";

        await saveDailyLog(
            "2026-08-27",
            dailyLog
        );

        expect(fetch).toHaveBeenCalledWith(
            "http://localhost:8000/health/daily-logs/2026-08-27",
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({

                    date: "2026-08-27",

                    weight_kg: 80.5,

                    workout_type: "HIIT",
                    workout_summary: "Push-ups",
                    workout_duration_min: 60,
                    workout_calories_burnt: 700,

                    steps: 10000,
                    total_calories_burnt: 2500,

                    breakfast: "Eggs",
                    lunch: "Chicken",
                    dinner: "Fish",
                    snacks: "Nuts",

                    protein_g: 120,
                    carbs_g: 150,
                    fibre_g: 25,
                    fat_g: 60,
                    sugar_g: 20,
                    calories_consumed: 2200,

                    water_ml: 3000,

                    first_meal_time:
                        "2026-08-27T08:30:00",

                    last_meal_time:
                        "2026-08-27T20:00:00",

                    sleep_start_time:
                        "2026-08-27T23:00:00",

                    sleep_end_time:
                        "2026-08-27T07:00:00",

                    notes: "Feeling good",

                }),
            }
        );

    });


    // Verify that empty numeric and time values
    // are converted to null before being sent.
    test("converts empty Daily Log values to null", async () => {

        const dailyLog =
            createEmptyDailyLog();

        await saveDailyLog(
            "2026-08-27",
            dailyLog
        );

        expect(fetch).toHaveBeenCalledTimes(1);

        const fetchOptions =
            vi.mocked(fetch).mock.calls[0][1];

        const requestBody =
            JSON.parse(
                fetchOptions?.body as string
            );

        expect(requestBody.weight_kg).toBeNull();

        expect(
            requestBody.workout_duration_min
        ).toBeNull();

        expect(
            requestBody.workout_calories_burnt
        ).toBeNull();

        expect(requestBody.steps).toBeNull();

        expect(
            requestBody.total_calories_burnt
        ).toBeNull();

        expect(requestBody.protein_g).toBeNull();
        expect(requestBody.carbs_g).toBeNull();
        expect(requestBody.fibre_g).toBeNull();
        expect(requestBody.fat_g).toBeNull();
        expect(requestBody.sugar_g).toBeNull();

        expect(
            requestBody.calories_consumed
        ).toBeNull();

        expect(requestBody.water_ml).toBeNull();

        expect(
            requestBody.first_meal_time
        ).toBeNull();

        expect(
            requestBody.last_meal_time
        ).toBeNull();

        expect(
            requestBody.sleep_start_time
        ).toBeNull();

        expect(
            requestBody.sleep_end_time
        ).toBeNull();

    });


    // Verify that an error is thrown when
    // saving the Daily Log fails.
    test("throws on Daily Log save failure", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

            text: vi.fn().mockResolvedValue(
                "Server error"
            ),

        } as unknown as Response);

        const dailyLog =
            createEmptyDailyLog();

        await expect(

            saveDailyLog(
                "2026-08-27",
                dailyLog
            )

        ).rejects.toThrow(

            "Failed to save Daily Log"

        );

    });

    // Verify that Body Measurements are correctly
    // retrieved and converted into the frontend
    // BodyMeasurements model.
    test("returns BodyMeasurements", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: true,

            status: 200,

            json: vi.fn().mockResolvedValue({

                body_fat_percent: 18.5,
                muscle_mass_percent: 42.3,
                visceral_fat: 8,

                neck_cm: 38,
                chest_cm: 102,
                waist_cm: 84,
                stomach_cm: 86,
                hips_cm: 96,

                left_arm_cm: 34,
                right_arm_cm: 35,

                left_forearm_cm: 29,
                right_forearm_cm: 30,

                left_thigh_cm: 56,
                right_thigh_cm: 57,

                left_calf_cm: 37,
                right_calf_cm: 38,

                notes: "Feeling strong",

            }),

        } as unknown as Response);

        const bodyMeasurements =
            await getBodyMeasurement("2026-08-27");

        expect(bodyMeasurements).toEqual({

            date: "2026-08-27",

            bodyFat: 18.5,
            muscleMass: 42.3,
            visceralFat: 8,

            neck: 38,
            chest: 102,
            waist: 84,
            stomach: 86,
            hips: 96,

            leftArm: 34,
            rightArm: 35,

            leftForearm: 29,
            rightForearm: 30,

            leftThigh: 56,
            rightThigh: 57,

            leftCalf: 37,
            rightCalf: 38,

            notes: "Feeling strong",

        });

    });


    // Verify that null is returned when the backend
    // indicates that no Body Measurements exist.
    test("returns null for 404", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 404,

        } as Response);

        const bodyMeasurements =
            await getBodyMeasurement("2026-08-27");

        expect(bodyMeasurements).toBeNull();

    });


    // Verify that an error is thrown when the backend
    // returns an unexpected server error.
    test("throws on server error", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

        } as Response);

        await expect(

            getBodyMeasurement("2026-08-27")

        ).rejects.toThrow(

            "Failed to load Body Measurements"

        );

    });


    // Verify that saveBodyMeasurement sends the correct
    // request to the backend.
    test("sends correct Body Measurements request", async () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        bodyMeasurements.bodyFat = 18.5;
        bodyMeasurements.muscleMass = 42.3;
        bodyMeasurements.visceralFat = 8;

        bodyMeasurements.neck = 38;
        bodyMeasurements.chest = 102;
        bodyMeasurements.waist = 84;
        bodyMeasurements.stomach = 86;
        bodyMeasurements.hips = 96;

        bodyMeasurements.leftArm = 34;
        bodyMeasurements.rightArm = 35;

        bodyMeasurements.leftForearm = 29;
        bodyMeasurements.rightForearm = 30;

        bodyMeasurements.leftThigh = 56;
        bodyMeasurements.rightThigh = 57;

        bodyMeasurements.leftCalf = 37;
        bodyMeasurements.rightCalf = 38;

        bodyMeasurements.notes = "Feeling strong";

        await saveBodyMeasurement(
            "2026-08-27",
            bodyMeasurements
        );

        expect(fetch).toHaveBeenCalledWith(
            "http://localhost:8000/health/body-measurements/2026-08-27",
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({

                    date: "2026-08-27",

                    body_fat_percent: 18.5,
                    muscle_mass_percent: 42.3,
                    visceral_fat: 8,

                    neck_cm: 38,
                    chest_cm: 102,
                    waist_cm: 84,
                    stomach_cm: 86,
                    hips_cm: 96,

                    left_arm_cm: 34,
                    right_arm_cm: 35,

                    left_forearm_cm: 29,
                    right_forearm_cm: 30,

                    left_thigh_cm: 56,
                    right_thigh_cm: 57,

                    left_calf_cm: 37,
                    right_calf_cm: 38,

                    notes: "Feeling strong",

                }),
            }
        );

    });


    // Verify that empty numeric values are
    // converted to null before being sent.
    test("converts empty Body Measurement values to null", async () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        await saveBodyMeasurement(
            "2026-08-27",
            bodyMeasurements
        );

        expect(fetch).toHaveBeenCalledTimes(1);

        const fetchOptions =
            vi.mocked(fetch).mock.calls[0][1];

        const requestBody =
            JSON.parse(
                fetchOptions?.body as string
            );

        expect(requestBody.body_fat_percent).toBeNull();
        expect(requestBody.muscle_mass_percent).toBeNull();
        expect(requestBody.visceral_fat).toBeNull();

        expect(requestBody.neck_cm).toBeNull();
        expect(requestBody.chest_cm).toBeNull();
        expect(requestBody.waist_cm).toBeNull();
        expect(requestBody.stomach_cm).toBeNull();
        expect(requestBody.hips_cm).toBeNull();

        expect(requestBody.left_arm_cm).toBeNull();
        expect(requestBody.right_arm_cm).toBeNull();

        expect(requestBody.left_forearm_cm).toBeNull();
        expect(requestBody.right_forearm_cm).toBeNull();

        expect(requestBody.left_thigh_cm).toBeNull();
        expect(requestBody.right_thigh_cm).toBeNull();

        expect(requestBody.left_calf_cm).toBeNull();
        expect(requestBody.right_calf_cm).toBeNull();

    });


    // Verify that an error is thrown when
    // saving Body Measurements fails.
    test("throws on Body Measurements save failure", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 500,

            text: vi.fn().mockResolvedValue(
                "Server error"
            ),

        } as unknown as Response);

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        await expect(

            saveBodyMeasurement(
                "2026-08-27",
                bodyMeasurements
            )

        ).rejects.toThrow(

            "Failed to save Body Measurements"

        );

    });

});