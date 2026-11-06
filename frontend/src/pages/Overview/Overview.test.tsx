import {
    cleanup,
    fireEvent,
    render,
    screen,
    waitFor,
} from "@testing-library/react";

import {
    afterEach,
    beforeEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";

import Overview from "./Overview";

import * as dashboardApi from "../../api/dashboard";

import type { DashboardSummary, Period } from "../../types/DashboardSummary";

import {
    makeDashboardSummary,
    makePeriodSummary,
} from "../../test/dashboardSummary";


/*
Mock the Dashboard API.

No real backend requests are made during these tests.
*/
vi.mock("../../api/dashboard", () => ({
    getDashboardSummary: vi.fn(),
}));


/*
Summaries the mocked API returns, by period, for the
current period (containing today, Thu Nov 5, 2026).
*/
const CURRENT: Record<Period, DashboardSummary> = {
    week: makeDashboardSummary(),
    day: makeDashboardSummary({
        period: "day",
        start: "2026-11-05",
        end: "2026-11-05",
        daysInPeriod: 1,
        daysElapsed: 1,
    }),
    month: makeDashboardSummary({
        period: "month",
        start: "2026-11-01",
        end: "2026-11-30",
        daysInPeriod: 30,
        daysElapsed: 5,
    }),
};

/*
The previous week, which is complete.
*/
const LAST_WEEK = makeDashboardSummary({
    date: "2026-10-29",
    start: "2026-10-26",
    end: "2026-11-01",
    daysElapsed: 7,
    isCurrent: false,
});


beforeEach(() => {

    vi.clearAllMocks();

    /*
    Fix "today" to Thursday, November 5, 2026. Only the
    date is faked, so the testing library's timers still
    run normally.
    */
    vi.useFakeTimers({ toFake: ["Date"] });
    vi.setSystemTime(new Date(2026, 10, 5, 12, 0));

    vi.mocked(dashboardApi.getDashboardSummary).mockImplementation(
        async (period, date) =>
            period === "week" && date === "2026-10-29"
                ? LAST_WEEK
                : CURRENT[period]
    );

});


afterEach(() => {
    vi.useRealTimers();
    cleanup();
});


describe("Overview", () => {

    /*
    Verify that the page opens on the current week and
    shows the heading, how current the data is, and the
    period.
    */
    test("loads this week on open", async () => {

        render(<Overview />);

        expect(
            await screen.findByRole("heading", { level: 1, name: "Overview" })
        ).toBeInTheDocument();

        expect(dashboardApi.getDashboardSummary).toHaveBeenCalledWith(
            "week",
            "2026-11-05"
        );

        expect(screen.getByText("Data through Thu, Nov 5")).toBeInTheDocument();
        expect(screen.getByRole("heading", { name: "Nov 2 – 8" })).toBeInTheDocument();
        expect(screen.getByText("Week so far · 4 of 7 days")).toBeInTheDocument();

        expect(
            screen.getByRole("button", { name: "Week" })
        ).toHaveAttribute("aria-pressed", "true");

    });


    /*
    Verify the four headline numbers and how each
    compares with last week.
    */
    test("shows the headline numbers with their changes", async () => {

        render(<Overview />);

        expect(await screen.findByText("9,210")).toBeInTheDocument();
        expect(screen.getByText("↑ 6% vs last week")).toBeInTheDocument();

        expect(screen.getByText("7h 11m")).toBeInTheDocument();
        expect(screen.getByText("↑ 22m vs last week")).toBeInTheDocument();

        expect(screen.getByText("53")).toBeInTheDocument();
        expect(screen.getByText("↓ 2 vs last week")).toBeInTheDocument();

        expect(screen.getByText("4")).toBeInTheDocument();
        expect(screen.getByText("210 min · 2,310 kcal")).toBeInTheDocument();

    });


    /*
    Verify that missing values are shown as a dash, with
    no change, never as zero.
    */
    test("shows a dash for missing values", async () => {

        vi.mocked(dashboardApi.getDashboardSummary).mockResolvedValue(
            makeDashboardSummary({
                current: makePeriodSummary(),
            })
        );

        render(<Overview />);

        expect(await screen.findAllByText("–")).toHaveLength(3);
        expect(screen.queryByText(/vs last week/)).not.toBeInTheDocument();

    });


    /*
    Verify that choosing Day loads the selected day.
    */
    test("switches to Day", async () => {

        render(<Overview />);

        fireEvent.click(await screen.findByRole("button", { name: "Day" }));

        expect(
            await screen.findByRole("heading", { name: "Thu, Nov 5" })
        ).toBeInTheDocument();

        expect(dashboardApi.getDashboardSummary).toHaveBeenLastCalledWith(
            "day",
            "2026-11-05"
        );

        expect(screen.getByText("Today so far")).toBeInTheDocument();

    });


    /*
    Verify that Next is disabled for the current period,
    and that Previous loads the previous week, after
    which Next is available again.
    */
    test("steps back a week, and not past today", async () => {

        render(<Overview />);

        const next = await screen.findByRole("button", { name: "Next period" });

        expect(next).toBeDisabled();

        fireEvent.click(screen.getByRole("button", { name: "Previous period" }));

        expect(
            await screen.findByRole("heading", { name: "Oct 26 – Nov 1" })
        ).toBeInTheDocument();

        expect(dashboardApi.getDashboardSummary).toHaveBeenLastCalledWith(
            "week",
            "2026-10-29"
        );

        await waitFor(() => expect(next).toBeEnabled());

        fireEvent.click(next);

        expect(
            await screen.findByRole("heading", { name: "Nov 2 – 8" })
        ).toBeInTheDocument();

        expect(dashboardApi.getDashboardSummary).toHaveBeenLastCalledWith(
            "week",
            "2026-11-05"
        );

    });


    /*
    Verify that Refresh reloads the same period with
    refresh, so the backend reads the Sheet again.
    */
    test("refreshes the current period", async () => {

        render(<Overview />);

        fireEvent.click(await screen.findByRole("button", { name: "Refresh" }));

        await waitFor(() =>
            expect(dashboardApi.getDashboardSummary).toHaveBeenLastCalledWith(
                "week",
                "2026-11-05",
                true
            )
        );

        expect(
            await screen.findByRole("button", { name: "Refresh" })
        ).toBeEnabled();

    });


    /*
    Verify that an error message is shown when the
    summary cannot be loaded.
    */
    test("shows an error when loading fails", async () => {

        const consoleError = vi
            .spyOn(console, "error")
            .mockImplementation(() => {});

        vi.mocked(dashboardApi.getDashboardSummary).mockRejectedValue(
            new Error("Network error")
        );

        render(<Overview />);

        expect(
            await screen.findByText(
                "Unable to load data. Please check your connection and try again."
            )
        ).toBeInTheDocument();

        consoleError.mockRestore();

    });

});
