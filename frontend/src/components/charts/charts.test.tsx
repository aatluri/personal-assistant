import {
    fireEvent,
    render,
    screen,
} from "@testing-library/react";

import {
    describe,
    expect,
    test,
    vi,
} from "vitest";

import BarSeries from "./BarSeries";
import Sparkline from "./Sparkline";
import StackedBar from "./StackedBar";


/*
Chart Tests

The Overview's small charts: bars per day, a stacked
bar, and a sparkline.
*/


const describeBar = (index: number) => `Day ${index + 1}`;


describe("BarSeries", () => {

    /*
    Verify that days with no data are drawn as gaps, not
    as zero-height bars, and bars are scaled to the
    largest value.
    */
    test("draws missing days as gaps and scales bars", () => {

        render(
            <BarSeries
                values={[10000, null, 5000]}
                labels={["M", "T", "W"]}
                colorClass="bg-teal-500"
                describeBar={describeBar}
            />
        );

        expect(screen.getAllByTestId("bar-gap")).toHaveLength(1);

        expect(screen.getByRole("img", { name: "Day 1" }))
            .toHaveStyle({ height: "100%" });

        expect(screen.getByRole("img", { name: "Day 3" }))
            .toHaveStyle({ height: "50%" });

        expect(screen.getByText("T")).toBeInTheDocument();

    });


    /*
    Verify that highlighting one bar dims the others.
    */
    test("dims every bar but the highlighted one", () => {

        render(
            <BarSeries
                values={[1, 2, 3]}
                labels={["", "", ""]}
                colorClass="bg-teal-500"
                describeBar={describeBar}
                highlightIndex={2}
            />
        );

        expect(screen.getByRole("img", { name: "Day 1" }).className)
            .toContain("opacity-35");

        expect(screen.getByRole("img", { name: "Day 3" }).className)
            .not.toContain("opacity-35");

    });


    /*
    Verify that with onSelect, bars with data become buttons
    that report their index, and gaps cannot be tapped.
    */
    test("lets bars with data be tapped", () => {

        const onSelect = vi.fn();

        render(
            <BarSeries
                values={[1, null, 3]}
                labels={["", "", ""]}
                colorClass="bg-teal-500"
                describeBar={describeBar}
                onSelect={onSelect}
            />
        );

        expect(screen.getAllByRole("button")).toHaveLength(2);

        fireEvent.click(screen.getByRole("button", { name: "Day 3" }));

        expect(onSelect).toHaveBeenCalledWith(2);

    });

});


describe("StackedBar", () => {

    /*
    Verify that each part's width and legend show its share
    of the total.
    */
    test("splits the bar by share", () => {

        render(
            <StackedBar
                label="Sleep stages"
                parts={[
                    { label: "Deep", value: 1, colorClass: "bg-violet-700" },
                    { label: "Core", value: 3, colorClass: "bg-violet-500" },
                ]}
            />
        );

        expect(
            screen.getByRole("img", { name: "Sleep stages: Deep 25%, Core 75%" })
        ).toBeInTheDocument();

        expect(screen.getByText("Deep 25%")).toBeInTheDocument();
        expect(screen.getByText("Core 75%")).toBeInTheDocument();

    });


    /*
    Verify that an empty total shows 0% rather than failing.
    */
    test("shows 0% when there is nothing to split", () => {

        render(
            <StackedBar
                label="Macros"
                parts={[{ label: "Protein", value: 0, colorClass: "bg-amber-700" }]}
            />
        );

        expect(screen.getByText("Protein 0%")).toBeInTheDocument();

    });

});


describe("Sparkline", () => {

    /*
    Verify that the line has one point per value.
    */
    test("draws a point per value", () => {

        const { container } = render(
            <Sparkline values={[80.2, 79.6, 79.0]} label="Weight trend" />
        );

        expect(screen.getByRole("img", { name: "Weight trend" })).toBeInTheDocument();

        const points = container
            .querySelector("polyline")
            ?.getAttribute("points")
            ?.split(" ");

        expect(points).toHaveLength(3);

    });


    /*
    Verify that nothing is drawn with fewer than two values.
    */
    test("draws nothing with fewer than two values", () => {

        const { container } = render(
            <Sparkline values={[80.2]} label="Weight trend" />
        );

        expect(container).toBeEmptyDOMElement();

    });

});
