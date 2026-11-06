import {
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

import PeriodControls from "./PeriodControls";


/*
PeriodControls Tests

The page-level behaviour (loading the picked period, Today,
stopping at the first data) is tested in Overview.test.tsx.
These tests cover opening the browser's date picker.
*/


function renderControls(onDateChange = vi.fn()) {

    render(
        <PeriodControls
            period="week"
            label="Nov 2 – 8"
            progress="Week so far · 4 of 7 days"
            selectedDate="2026-11-05"
            today="2026-11-05"
            dataFrom="2022-01-01"
            canGoPrevious={true}
            canGoNext={false}
            isCurrent={true}
            onPeriodChange={vi.fn()}
            onPrevious={vi.fn()}
            onNext={vi.fn()}
            onDateChange={onDateChange}
            onToday={vi.fn()}
        />
    );

    return onDateChange;

}


afterEach(() => {
    vi.restoreAllMocks();
});


describe("PeriodControls", () => {

    /*
    Verify that clicking the period label opens the
    browser's date picker. The test browser has no
    showPicker, so it is provided here.
    */
    test("opens the date picker from the period label", () => {

        const showPicker = vi.fn();

        Object.defineProperty(HTMLInputElement.prototype, "showPicker", {
            configurable: true,
            value: showPicker,
        });

        renderControls();

        fireEvent.click(screen.getByRole("button", { name: /Nov 2 – 8/ }));

        expect(showPicker).toHaveBeenCalledTimes(1);

    });


    /*
    Verify that a picked date is reported, and clearing
    the date changes nothing.
    */
    test("reports a picked date and ignores a cleared one", () => {

        const onDateChange = renderControls();

        const picker = screen.getByLabelText("Choose a date");

        fireEvent.change(picker, { target: { value: "2022-05-15" } });
        expect(onDateChange).toHaveBeenCalledWith("2022-05-15");

        fireEvent.change(picker, { target: { value: "" } });
        expect(onDateChange).toHaveBeenCalledTimes(1);

    });

});
