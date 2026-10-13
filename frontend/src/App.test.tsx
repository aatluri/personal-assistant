import {
    cleanup,
    render,
    screen,
} from "@testing-library/react";

import {
    afterEach,
    beforeEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import App from "./App";

import * as workoutMetricsApi from "./api/workoutMetrics";
import * as sleepMetricsApi from "./api/sleepMetrics";
import * as nutritionMetricsApi from "./api/nutritionMetrics";
import * as healthMetricsApi from "./api/healthMetrics";


vi.mock("./api/workoutMetrics", () => ({
    getWorkoutMetricsByDate: vi.fn(),
    saveWorkoutMetric: vi.fn(),
}));

vi.mock("./api/sleepMetrics", () => ({
    getSleepMetric: vi.fn(),
    saveSleepMetric: vi.fn(),
}));

vi.mock("./api/nutritionMetrics", () => ({
    getNutritionMetric: vi.fn(),
    saveNutritionMetric: vi.fn(),
}));

vi.mock("./api/healthMetrics", () => ({
    getHealthMetric: vi.fn(),
    saveHealthMetric: vi.fn(),
}));


afterEach(() => {
    cleanup();
});


beforeEach(() => {

    vi.clearAllMocks();

    // Workout Metrics can contain multiple records per date.
    vi.mocked(
        workoutMetricsApi.getWorkoutMetricsByDate
    ).mockResolvedValue([]);

    // These metric pages contain one record per date.
    vi.mocked(
        sleepMetricsApi.getSleepMetric
    ).mockResolvedValue(null);

    vi.mocked(
        nutritionMetricsApi.getNutritionMetric
    ).mockResolvedValue(null);

    vi.mocked(
        healthMetricsApi.getHealthMetric
    ).mockResolvedValue(null);

});


describe("App", () => {

    test("renders Dashboard route", () => {

        window.history.pushState(
            {},
            "",
            "/"
        );

        render(<App />);

        expect(
            screen.getByRole(
                "heading",
                {
                    name: /Dashboard/,
                }
            )
        ).toBeInTheDocument();

    });


    test("renders Log Today route", () => {

        window.history.pushState(
            {},
            "",
            "/log-today"
        );

        render(<App />);

        expect(
            screen.getByText("Log Today")
        ).toBeInTheDocument();

    });


    test("renders Body Measurements route", () => {

        window.history.pushState(
            {},
            "",
            "/body-measurements"
        );

        render(<App />);

        expect(
            screen.getByText("Body Measurements")
        ).toBeInTheDocument();

    });


    test("renders Workout Metrics route", async () => {

        window.history.pushState(
            {},
            "",
            "/workout-metrics"
        );

        render(<App />);

        expect(
            await screen.findByText("Workouts")
        ).toBeInTheDocument();

    });


    test("renders Sleep Metrics route", async () => {

        window.history.pushState(
            {},
            "",
            "/sleep-metrics"
        );

        render(<App />);

        expect(
            await screen.findByText("Sleep Metrics")
        ).toBeInTheDocument();

    });


    test("renders Nutrition Metrics route", async () => {

        window.history.pushState(
            {},
            "",
            "/nutrition-metrics"
        );

        render(<App />);

        expect(
            await screen.findByText("Nutrition Metrics")
        ).toBeInTheDocument();

    });


    test("renders Health Metrics route", async () => {

        window.history.pushState(
            {},
            "",
            "/health-metrics"
        );

        render(<App />);

        expect(
            await screen.findByText("Health Metrics")
        ).toBeInTheDocument();

    });


    test("renders History route", () => {

        window.history.pushState(
            {},
            "",
            "/history"
        );

        render(<App />);

        expect(
            screen.getByRole(
                "heading",
                {
                    name: /History/,
                }
            )
        ).toBeInTheDocument();

    });


    test("renders Settings route", () => {

        window.history.pushState(
            {},
            "",
            "/settings"
        );

        render(<App />);

        expect(
            screen.getByText("Settings")
        ).toBeInTheDocument();

    });

});