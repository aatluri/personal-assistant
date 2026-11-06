/*
OverviewHeader

The Overview page heading, how current the data is, and
the Refresh button.

Responsibilities:
- Display the page title.
- Show "Data through ...", because imports run behind
  real time.
- Let the user reload the data, for edits made directly
  in Google Sheets (saves through the app show without it).
*/

import { CalendarDays, RefreshCw } from "lucide-react";

import { formatDataThrough } from "../../../utils/overviewFormat";


/*
    dataThrough
        The latest date with any data, or null before
        the first load or when there is no data.

    isRefreshing
        True while a refresh is running; the button is
        disabled so it cannot be pressed twice.

    onRefresh
        Called when the Refresh button is pressed.
*/
interface OverviewHeaderProps {
    dataThrough: string | null;
    isRefreshing: boolean;
    onRefresh: () => void;
}

function OverviewHeader({
    dataThrough,
    isRefreshing,
    onRefresh,
}: OverviewHeaderProps) {

    return (

        <div
            className="
                flex
                flex-wrap
                items-start
                justify-between
                gap-3
            "
        >

            <div>

                <h1
                    className="
                        text-3xl
                        font-bold
                        text-slate-900
                    "
                >
                    Overview
                </h1>

                <p
                    className="
                        mt-1
                        flex
                        items-center
                        gap-1
                        text-sm
                        text-slate-500
                    "
                >
                    <CalendarDays size={14} aria-hidden="true" />
                    {formatDataThrough(dataThrough)}
                </p>

            </div>

            <button
                type="button"
                onClick={onRefresh}
                disabled={isRefreshing}
                className="
                    flex
                    items-center
                    gap-2
                    rounded-lg
                    border
                    border-slate-200
                    bg-white
                    px-3
                    py-2
                    text-sm
                    text-slate-700
                    hover:bg-slate-100
                    disabled:opacity-50
                "
            >
                <RefreshCw
                    size={16}
                    aria-hidden="true"
                    className={isRefreshing ? "animate-spin" : ""}
                />
                {isRefreshing ? "Refreshing…" : "Refresh"}
            </button>

        </div>

    );

}

export default OverviewHeader;
