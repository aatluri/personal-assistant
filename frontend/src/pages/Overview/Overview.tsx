/*
Overview

The home page: how a day, a week or a month went, at a
glance. Read-only; the backend computes every value
(see docs/dashboard/overview-design.md).

Responsibilities:
- Own the selected period (Day / Week / Month) and date.
- Load the summary whenever either changes.
- Refresh on request, for edits made directly in Google
  Sheets.
- Pass each section the part of the summary it shows.
*/

import { useEffect, useState } from "react";

import { getDashboardSummary } from "../../api/dashboard";

import type { DashboardSummary, Period } from "../../types/DashboardSummary";

import {
    formatPeriodLabel,
    formatPeriodProgress,
    shiftDate,
    toIsoDate,
} from "../../utils/overviewFormat";

import LoadingSpinner from "../../components/LoadingSpinner";
import PageContainer from "../../components/PageContainer";

import HeadlineNumbers from "./components/HeadlineNumbers";
import OverviewHeader from "./components/OverviewHeader";
import PeriodControls from "./components/PeriodControls";


function Overview() {

    /*
    Today's date in YYYY-MM-DD format.
    */
    const today = toIsoDate(new Date());

    const [period, setPeriod] =
        useState<Period>("week");

    /*
    Any date in the selected period. Changing the period
    keeps it, so Day -> Week shows the week of that day.
    */
    const [selectedDate, setSelectedDate] =
        useState(today);

    const [summary, setSummary] =
        useState<DashboardSummary | null>(null);

    const [isLoading, setIsLoading] =
        useState(true);

    const [isRefreshing, setIsRefreshing] =
        useState(false);

    const [loadError, setLoadError] =
        useState(false);


    /*
    Whenever the period or date changes, load its summary.

    If the user clicks again before a response arrives,
    the older response is ignored, so the page never shows
    a period that is no longer selected.
    */
    useEffect(() => {

        let isLatestRequest = true;

        async function loadSummary() {

            setIsLoading(true);
            setLoadError(false);

            try {

                const result = await getDashboardSummary(
                    period,
                    selectedDate
                );

                if (isLatestRequest) {
                    setSummary(result);
                }

            } catch (error) {

                console.error(
                    "Failed to load the Overview:",
                    error
                );

                if (isLatestRequest) {
                    setLoadError(true);
                }

            } finally {

                if (isLatestRequest) {
                    setIsLoading(false);
                }

            }

        }

        loadSummary();

        return () => {
            isLatestRequest = false;
        };

    }, [period, selectedDate]);


    /*
    Reload with refresh, so the backend reads every
    worksheet again instead of using its cache.
    */
    async function handleRefresh() {

        setIsRefreshing(true);
        setLoadError(false);

        try {

            setSummary(
                await getDashboardSummary(period, selectedDate, true)
            );

        } catch (error) {

            console.error(
                "Failed to refresh the Overview:",
                error
            );
            setLoadError(true);

        } finally {

            setIsRefreshing(false);

        }

    }


    /*
    Step one period back or forward. Never past today:
    there is no data after it.
    */
    function handleStep(direction: -1 | 1) {

        const shifted = shiftDate(selectedDate, period, direction);

        setSelectedDate(shifted > today ? today : shifted);

    }


    /*
    Display a loading indicator until the first summary
    arrives. Later loads keep the current summary on
    screen, dimmed, until the new one replaces it.
    */
    if (summary === null && isLoading) {

        return <LoadingSpinner />;

    }


    /*
    The current period has no "next": its end is today
    or later.
    */
    const canGoNext =
        !isLoading && summary !== null && summary.end < today;


    /*
    Page Layout
    */
    return (

        <PageContainer>

            <div className="space-y-6">

                <OverviewHeader
                    dataThrough={summary?.dataThrough ?? null}
                    isRefreshing={isRefreshing}
                    onRefresh={handleRefresh}
                />

                <PeriodControls
                    period={period}
                    label={summary ? formatPeriodLabel(summary) : ""}
                    progress={summary ? formatPeriodProgress(summary) : ""}
                    canGoNext={canGoNext}
                    onPeriodChange={setPeriod}
                    onPrevious={() => handleStep(-1)}
                    onNext={() => handleStep(1)}
                />

                {loadError && (
                    <div
                        className="
                            rounded-xl
                            border
                            border-red-200
                            bg-red-50
                            px-4
                            py-3
                            text-sm
                            text-red-700
                        "
                    >
                        Unable to load data. Please check your connection and try again.
                    </div>
                )}

                {summary && (
                    <div
                        aria-busy={isLoading}
                        className={isLoading ? "opacity-60" : ""}
                    >
                        <HeadlineNumbers summary={summary} />
                    </div>
                )}

            </div>

        </PageContainer>

    );

}

export default Overview;
