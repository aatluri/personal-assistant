import {
    afterEach,
    beforeEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import {
    getBodyMeasurement,
    saveBodyMeasurement,
} from "./bodyMeasurements";

import {
    createEmptyBodyMeasurements,
} from "../utils/createEmptyBodyMeasurements";


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


describe("Body Measurements API", () => {

    /*
    Verify that Body Measurements are correctly
    retrieved and converted from the backend
    snake_case model into the frontend model.
    */
    test("returns BodyMeasurements", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: true,

            status: 200,

            json: vi.fn().mockResolvedValue({

                weight_kg: 80.5,
                body_mass_index: 26.9,

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

            weight: 80.5,
            bodyMassIndex: 26.9,

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


    /*
    Verify that null is returned when the backend
    indicates that no Body Measurements exist.
    */
    test("returns null for 404", async () => {

        vi.mocked(fetch).mockResolvedValue({

            ok: false,

            status: 404,

        } as Response);

        const bodyMeasurements =
            await getBodyMeasurement("2026-08-27");

        expect(bodyMeasurements).toBeNull();

    });


    /*
    Verify that an error is thrown when the backend
    returns an unexpected server error.
    */
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


    /*
    Verify that saveBodyMeasurement converts the
    frontend model into the correct backend request.
    */
    test("sends correct Body Measurements request", async () => {

        const bodyMeasurements =
            createEmptyBodyMeasurements();

        bodyMeasurements.weight = 80.5;
        bodyMeasurements.bodyMassIndex = 26.9;

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

            "http://localhost:8000/health/body-measurements",

            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({

                    date: "2026-08-27",

                    weight_kg: 80.5,
                    body_mass_index: 26.9,

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


    /*
    Verify that empty numeric values are converted
    to null before being sent to the backend.
    */
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

        expect(requestBody.weight_kg).toBeNull();
        expect(requestBody.body_mass_index).toBeNull();

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


    /*
    Verify that an error is thrown when
    saving Body Measurements fails.
    */
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