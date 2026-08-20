/*
    DateSection

    Displays and updates the date
    for the current Daily Log.
*/

import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Dispatch, SetStateAction } from "react";

interface DateSectionProps {
    selectedDate: string;
    setSelectedDate: Dispatch<SetStateAction<string>>;
}

function DateSection({
    selectedDate,
    setSelectedDate,
}: DateSectionProps) {

    /*
        Convert the selected date into
        a readable format.
    */
    const formattedDate = new Date(selectedDate).toLocaleDateString(
        "en-IN",
        {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric",
        }
    );

    /*
        Move one day backwards.
    */
    function goToPreviousDay() {

        const date = new Date(selectedDate);
        date.setDate(date.getDate() - 1);

        setSelectedDate(
            date.toLocaleDateString("en-CA")
        );

    }

    /*
        Move one day forwards.
    */
    function goToNextDay() {

        const date = new Date(selectedDate);
        date.setDate(date.getDate() + 1);

        setSelectedDate(
            date.toLocaleDateString("en-CA")
        );

    }

    return (

        <section
            className="
                rounded-2xl
                border
                border-slate-200
                bg-white
                p-6
                shadow-sm
            "
        >

            <h2
                className="
                    mb-5
                    text-xl
                    font-semibold
                    tracking-tight
                    text-slate-900
                "
            >
                Date
            </h2>

            <div
                className="
                    flex
                    flex-col
                    gap-4
                    md:flex-row
                    md:items-center
                    md:justify-between
                "
            >

                <div
                    className="
                        flex
                        items-center
                        gap-3
                    "
                >

                    <button
                        type="button"
                        onClick={goToPreviousDay}
                        className="
                            rounded-full
                            p-2
                            transition-colors
                            hover:bg-slate-100
                        "
                    >
                        <ChevronLeft size={22} />
                    </button>

                    <p
                        className="
                            min-w-[240px]
                            text-center
                            text-lg
                            font-medium
                            text-slate-900
                        "
                    >
                        {formattedDate}
                    </p>

                    <button
                        type="button"
                        onClick={goToNextDay}
                        className="
                            rounded-full
                            p-2
                            transition-colors
                            hover:bg-slate-100
                        "
                    >
                        <ChevronRight size={22} />
                    </button>

                </div>

                <input
                    type="date"
                    value={selectedDate}
                    onChange={(event) =>
                        setSelectedDate(event.target.value)
                    }
                    className="
                        h-12
                        rounded-xl
                        border
                        border-slate-300
                        px-4
                        focus:border-blue-600
                        focus:outline-none
                    "
                />

            </div>

        </section>

    );

}

export default DateSection;