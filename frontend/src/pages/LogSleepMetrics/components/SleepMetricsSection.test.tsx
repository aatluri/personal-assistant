/*
SleepMetricsSection Tests

Purpose:
Test the SleepMetricsSection component in isolation.

These tests do not involve the page, backend, or API.
They only verify that the component correctly displays
Sleep Metrics and reports changes back to its parent.

Test Setup:

- React Testing Library is used to render the component
  and interact with its input fields.

- Vitest is used as the test framework and for creating
  mock functions.

- createEmptySleepMetrics() provides a standard empty
  SleepMetrics object for each test.

- setSleepMetrics is replaced with vi.fn().
  This lets us capture what the component sends back to
  the parent when the user changes a field.

- cleanup() runs after every test so each test starts
  with a fresh DOM.

What We Test:

1. All Sleep Metrics fields are rendered.

2. Existing Sleep Metrics values are displayed in the
   correct fields.

3. Sleep Start Time and Sleep End Time update the
   correct datetime properties.

4. Changing each numeric field updates the correct
   SleepMetrics property with a number.

5. Changing Source updates the source property as text.

6. Clearing a numeric field stores "" rather than
   converting the empty value to 0.

State Update Testing:

SleepMetricsSection calls setSleepMetrics() with a
React state updater function:

    previous => ({
        ...previous,
        [key]: value
    })

The tests capture this updater function, execute it
using a sample previous state, and verify that the
expected property was changed correctly.

Overall Flow Being Tested:

SleepMetrics data
        ↓
SleepMetricsSection displays the data
        ↓
User changes an input
        ↓
Component calls setSleepMetrics()
        ↓
Test verifies the correct field and value were updated
*/


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

import SleepMetricsSection from "./SleepMetricsSection";

import type {
    SleepMetrics,
} from "../../../types/SleepMetrics";

import {
    createEmptySleepMetrics,
} from "../../../utils/createEmptySleepMetrics";


/*
Clean up the rendered component after
every individual test.
*/
afterEach(() => {
    cleanup();
});


describe("SleepMetricsSection", () => {

    /*
    Verify that all Sleep Metrics fields
    are displayed.
    */
    test("renders Sleep Metrics fields", () => {

        const sleepMetrics =
            createEmptySleepMetrics();


        render(
            <SleepMetricsSection
                sleepMetrics={sleepMetrics}
                setSleepMetrics={vi.fn()}
            />
        );


        expect(
            screen.getByLabelText(
                "Sleep Start Time"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Sleep End Time"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Total Sleep Duration (hr)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Core Sleep (hr)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Deep Sleep (hr)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Awake (hr)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "REM Sleep (hr)"
            )
        ).toBeInTheDocument();

        expect(
            screen.getByLabelText(
                "Source"
            )
        ).toBeInTheDocument();

    });


    /*
    Verify that supplied Sleep Metrics
    values are displayed correctly.
    */
    test("renders supplied values", () => {

        const sleepMetrics =
            createEmptySleepMetrics();


        sleepMetrics.sleepStartTime =
            "2026-08-26T23:15";

        sleepMetrics.sleepEndTime =
            "2026-08-27T07:15";

        sleepMetrics.totalSleepDurationHr = 8;

        sleepMetrics.coreSleepHr = 4.5;

        sleepMetrics.deepSleepHr = 1.5;

        sleepMetrics.awakeHr = 0.5;

        sleepMetrics.remSleepHr = 1.5;

        sleepMetrics.source = "Apple Health";


        render(
            <SleepMetricsSection
                sleepMetrics={sleepMetrics}
                setSleepMetrics={vi.fn()}
            />
        );


        expect(
            screen.getByLabelText(
                "Sleep Start Time"
            )
        ).toHaveValue(
            "2026-08-26T23:15"
        );

        expect(
            screen.getByLabelText(
                "Sleep End Time"
            )
        ).toHaveValue(
            "2026-08-27T07:15"
        );

        expect(
            screen.getByLabelText(
                "Total Sleep Duration (hr)"
            )
        ).toHaveValue(8);

        expect(
            screen.getByLabelText(
                "Core Sleep (hr)"
            )
        ).toHaveValue(4.5);

        expect(
            screen.getByLabelText(
                "Deep Sleep (hr)"
            )
        ).toHaveValue(1.5);

        expect(
            screen.getByLabelText(
                "Awake (hr)"
            )
        ).toHaveValue(0.5);

        expect(
            screen.getByLabelText(
                "REM Sleep (hr)"
            )
        ).toHaveValue(1.5);

        expect(
            screen.getByLabelText(
                "Source"
            )
        ).toHaveValue(
            "Apple Health"
        );

    });


    /*
    Helper used for fields that store
    string values.

    This includes the datetime fields.
    */
    function testStringField(
        testName: string,
        label: string,
        field: keyof SleepMetrics,
        inputValue: string,
    ) {

        test(testName, () => {

            const sleepMetrics =
                createEmptySleepMetrics();

            const setSleepMetrics =
                vi.fn();


            render(
                <SleepMetricsSection
                    sleepMetrics={sleepMetrics}
                    setSleepMetrics={setSleepMetrics}
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
                setSleepMetrics
            ).toHaveBeenCalled();


            /*
            Capture the React state updater
            passed to setSleepMetrics().
            */
            const updateFunction =
                setSleepMetrics.mock.calls[0][0] as (
                    sleepMetrics: SleepMetrics
                ) => SleepMetrics;


            const previousSleepMetrics =
                createEmptySleepMetrics();


            const updatedSleepMetrics =
                updateFunction(
                    previousSleepMetrics
                );


            expect(
                updatedSleepMetrics[field]
            ).toBe(inputValue);

        });

    }


    /*
    Test the two datetime fields.
    */
    testStringField(
        "updates Sleep Start Time",
        "Sleep Start Time",
        "sleepStartTime",
        "2026-08-26T23:15"
    );


    testStringField(
        "updates Sleep End Time",
        "Sleep End Time",
        "sleepEndTime",
        "2026-08-27T07:15"
    );


    /*
    Helper used by the numeric field tests.

    Every numeric Sleep Metric uses the same
    update behaviour.

    Each call to this helper creates a
    separate Vitest test.
    */
    function testNumericField(
        testName: string,
        label: string,
        field: keyof SleepMetrics,
        inputValue: string,
        expectedValue: number,
    ) {

        test(testName, () => {

            const sleepMetrics =
                createEmptySleepMetrics();

            const setSleepMetrics =
                vi.fn();


            render(
                <SleepMetricsSection
                    sleepMetrics={sleepMetrics}
                    setSleepMetrics={setSleepMetrics}
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
                setSleepMetrics
            ).toHaveBeenCalled();


            const updateFunction =
                setSleepMetrics.mock.calls[0][0] as (
                    sleepMetrics: SleepMetrics
                ) => SleepMetrics;


            const previousSleepMetrics =
                createEmptySleepMetrics();


            const updatedSleepMetrics =
                updateFunction(
                    previousSleepMetrics
                );


            expect(
                updatedSleepMetrics[field]
            ).toBe(expectedValue);

        });

    }


    testNumericField(
        "updates total sleep duration",
        "Total Sleep Duration (hr)",
        "totalSleepDurationHr",
        "8",
        8
    );


    testNumericField(
        "updates core sleep",
        "Core Sleep (hr)",
        "coreSleepHr",
        "4.5",
        4.5
    );


    testNumericField(
        "updates deep sleep",
        "Deep Sleep (hr)",
        "deepSleepHr",
        "1.5",
        1.5
    );


    testNumericField(
        "updates awake time",
        "Awake (hr)",
        "awakeHr",
        "0.5",
        0.5
    );


    testNumericField(
        "updates REM sleep",
        "REM Sleep (hr)",
        "remSleepHr",
        "1.5",
        1.5
    );


    /*
    Verify that Source is updated as text.
    */
    test("updates source", () => {

        const sleepMetrics =
            createEmptySleepMetrics();

        const setSleepMetrics =
            vi.fn();


        render(
            <SleepMetricsSection
                sleepMetrics={sleepMetrics}
                setSleepMetrics={setSleepMetrics}
            />
        );


        fireEvent.change(
            screen.getByLabelText(
                "Source"
            ),
            {
                target: {
                    value: "Apple Health",
                },
            }
        );


        expect(
            setSleepMetrics
        ).toHaveBeenCalled();


        const updateFunction =
            setSleepMetrics.mock.calls[0][0] as (
                sleepMetrics: SleepMetrics
            ) => SleepMetrics;


        const previousSleepMetrics =
            createEmptySleepMetrics();


        const updatedSleepMetrics =
            updateFunction(
                previousSleepMetrics
            );


        expect(
            updatedSleepMetrics.source
        ).toBe("Apple Health");

    });


    /*
    Verify that clearing a numeric field
    stores an empty string.

    Without this behaviour, Number("")
    would result in 0.
    */
    test("keeps cleared numeric field empty", () => {

        const sleepMetrics =
            createEmptySleepMetrics();

        sleepMetrics.totalSleepDurationHr = 8;

        const setSleepMetrics =
            vi.fn();


        render(
            <SleepMetricsSection
                sleepMetrics={sleepMetrics}
                setSleepMetrics={setSleepMetrics}
            />
        );


        fireEvent.change(
            screen.getByLabelText(
                "Total Sleep Duration (hr)"
            ),
            {
                target: {
                    value: "",
                },
            }
        );


        const updateFunction =
            setSleepMetrics.mock.calls[0][0] as (
                sleepMetrics: SleepMetrics
            ) => SleepMetrics;


        const updatedSleepMetrics =
            updateFunction(
                sleepMetrics
            );


        expect(
            updatedSleepMetrics.totalSleepDurationHr
        ).toBe("");

    });

});