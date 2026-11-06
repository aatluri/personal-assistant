import {
    render,
    screen,
    within,
} from "@testing-library/react";

import {
    describe,
    expect,
    test,
} from "vitest";

import type { Highlight } from "../../../types/DashboardSummary";

import Highlights from "./Highlights";


/*
Highlights Tests

The backend writes every part of a highlight; the page
draws goals (with progress) as rings and records (without)
as badges, in the order given.
*/


function goal(overrides: Partial<Highlight> = {}): Highlight {

    return {
        topic: "steps",
        value: "12/31",
        label: "days ≥ 10k steps",
        detail: null,
        progress: 12 / 31,
        goalMet: false,
        text: "Steps goal met 12 of 31 days",
        ...overrides,
    };

}


function record(overrides: Partial<Highlight> = {}): Highlight {

    return {
        topic: "best",
        value: "8h 00m",
        label: "best sleep",
        detail: "May 14",
        progress: null,
        goalMet: false,
        text: "Best sleep May 14 · 8h 00m",
        ...overrides,
    };

}


function ring(name: string) {
    return within(screen.getByRole("list", { name: "Goals" }))
        .getByRole("listitem", { name });
}


describe("Highlights", () => {

    /*
    Verify that goals become rings and records become
    badges, each in order and named by its sentence.
    */
    test("draws goals as rings and records as badges", () => {

        render(
            <Highlights
                highlights={[
                    goal(),
                    record({ topic: "streak", value: "5 days", label: "longest 10k streak", detail: null, text: "Longest 10k streak · 5 days" }),
                    goal({ topic: "sleep", value: "4/12", label: "nights ≥ 7h sleep", progress: 4 / 12, text: "Sleep goal met 4 of 12 nights" }),
                    record(),
                ]}
            />
        );

        const names = (list: string) =>
            within(screen.getByRole("list", { name: list }))
                .getAllByRole("listitem")
                .map((item) => item.getAttribute("aria-label"));

        expect(names("Goals")).toEqual([
            "Steps goal met 12 of 31 days",
            "Sleep goal met 4 of 12 nights",
        ]);

        expect(names("Records")).toEqual([
            "Longest 10k streak · 5 days",
            "Best sleep May 14 · 8h 00m",
        ]);

    });


    /*
    Verify a ring: its percentage, value and caption, and an
    arc as long as the share completed.
    */
    test("fills each ring to its progress", () => {

        render(<Highlights highlights={[goal()]} />);

        const steps = within(ring("Steps goal met 12 of 31 days"));

        expect(steps.getByText("39%")).toBeInTheDocument();
        expect(steps.getByText("12/31")).toBeInTheDocument();
        expect(steps.getByText("days ≥ 10k steps")).toBeInTheDocument();

        const circumference = 2 * Math.PI * 28;

        expect(
            steps.getByTestId("ring-arc").getAttribute("stroke-dasharray")
        ).toBe(`${((12 / 31) * circumference).toFixed(1)} ${circumference.toFixed(1)}`);

    });


    /*
    Verify the colour bands, by the percentage shown in the
    ring: up to 30% red, up to 50% orange, up to 70% amber,
    up to 90% light green, above 90% green.
    */
    test("colours each ring by how complete it is", () => {

        const cases: [number, string, string][] = [
            [0.25, "25%", "red"],
            [0.304, "30%", "red"],
            [0.31, "31%", "orange"],
            [12 / 31, "39%", "orange"],
            [0.5, "50%", "orange"],
            [2 / 3, "67%", "amber"],
            [0.85, "85%", "lime"],
            [0.95, "95%", "green"],
        ];

        render(
            <Highlights
                highlights={cases.map(([progress, percent]) =>
                    goal({ progress, text: `Goal at ${percent}` })
                )}
            />
        );

        for (const [, percent, band] of cases) {
            const item = ring(`Goal at ${percent}`);

            expect(item).toHaveAttribute("data-completion", band);
            expect(within(item).getByText(percent)).toBeInTheDocument();
        }

        expect(
            within(ring("Goal at 39%")).getByTestId("ring-arc").getAttribute("class")
        ).toContain("stroke-orange-500");

    });


    /*
    Verify the ends of the scale: 0% is an empty ring with a
    red "0%", and a fully met goal is green with a tick
    instead of the percentage.
    */
    test("shows an empty ring at 0% and a tick when fully met", () => {

        render(
            <Highlights
                highlights={[
                    goal({ progress: 0, text: "Water goal met 0 of 20 days" }),
                    goal({ progress: 1, goalMet: true, text: "Steps goal met 7 of 7 days" }),
                ]}
            />
        );

        const empty = ring("Water goal met 0 of 20 days");

        expect(within(empty).queryByTestId("ring-arc")).not.toBeInTheDocument();
        expect(within(empty).getByText("0%").className).toContain("text-rose-600");

        const met = ring("Steps goal met 7 of 7 days");

        expect(met).toHaveAttribute("data-completion", "green");
        expect(within(met).getByTestId("goal-met")).toBeInTheDocument();
        expect(within(met).queryByText("100%")).not.toBeInTheDocument();

    });


    /*
    Verify a badge's text: caption, value and detail.
    */
    test("shows each record's caption, value and detail", () => {

        render(<Highlights highlights={[record()]} />);

        expect(
            screen.getByRole("listitem", { name: "Best sleep May 14 · 8h 00m" })
        ).toHaveTextContent("Best sleep · 8h 00m · May 14");

    });


    /*
    Verify that an empty group is left out, and nothing is
    shown without highlights.
    */
    test("leaves out empty groups", () => {

        const { container, rerender } = render(<Highlights highlights={[record()]} />);

        expect(screen.queryByRole("list", { name: "Goals" })).not.toBeInTheDocument();
        expect(screen.getByRole("list", { name: "Records" })).toBeInTheDocument();

        rerender(<Highlights highlights={[goal()]} />);

        expect(screen.getByRole("list", { name: "Goals" })).toBeInTheDocument();
        expect(screen.queryByRole("list", { name: "Records" })).not.toBeInTheDocument();

        rerender(<Highlights highlights={[]} />);

        expect(container).toBeEmptyDOMElement();

    });

});
