/*
LogSleepMetrics

Page responsible for viewing and editing
Sleep Metrics for a selected date.

Responsibilities:
- Load Sleep Metrics from the backend.
- Maintain the page state.
- Pass state to the UI section.
- Save changes back to the backend.
*/

import { useEffect, useState } from "react";
import { Moon } from "lucide-react";

import {
    getSleepMetric,
    saveSleepMetric,
} from "../../api/sleepMetrics";

import type { SleepMetrics } from "../../types/SleepMetrics";

import LoadingSpinner from "../../components/LoadingSpinner";
import SaveButton from "../../components/SaveButton";
import PageContainer from "../../components/PageContainer";
import CollapsibleCard from "../../components/CollapsibleCard";

import LogTodayHeader from "../LogToday/components/LogTodayHeader";
import DateSection from "../LogToday/components/DateSection";
import SleepMetricsSection from "./components/SleepMetricsSection";

import { createEmptySleepMetrics } from "../../utils/createEmptySleepMetrics";


function LogSleepMetrics() {

    /*
    Today's date in YYYY-MM-DD format.
    */
    const today = new Date().toLocaleDateString("en-CA");

    /*
    Currently selected date.

    Changing this value automatically
    reloads Sleep Metrics for that date.
    */
    const [selectedDate, setSelectedDate] =
        useState(today);

    /*
    Page state.
    */
    const [isLoading, setIsLoading] =
        useState(true);

    const [isDirty, setIsDirty] =
        useState(false);

    const [saveStatus, setSaveStatus] = useState<
        "idle" | "saving" | "saved" | "failed"
    >("saved");

    const [loadError, setLoadError] = useState(false);

    /*
    Holds the Sleep Metrics currently
    displayed on the page.
    */
    const [sleepMetrics, setSleepMetrics] =
        useState<SleepMetrics>(
            createEmptySleepMetrics()
        );


    /*
    Whenever the selected date changes,
    retrieve Sleep Metrics from the backend.
    */
    useEffect(() => {

        async function loadSleepMetrics() {

            setIsLoading(true);
            setLoadError(false);

            try {

                const existingSleepMetrics =
                    await getSleepMetric(selectedDate);

                if (existingSleepMetrics) {

                    setSleepMetrics(
                        existingSleepMetrics
                    );

                } else {

                    setSleepMetrics(
                        createEmptySleepMetrics()
                    );

                }

                setIsDirty(false);
                setSaveStatus("saved");

            } catch (error) {

                console.error(
                    "Failed to load Sleep Metrics:",
                    error
                );
                setLoadError(true);

            } finally {

                setIsLoading(false);

            }

        }

        loadSleepMetrics();

    }, [selectedDate]);


    /*
    Save the current Sleep Metrics
    to the backend.
    */
    async function handleSaveSleepMetrics() {

        setSaveStatus("saving");

        try {

            await saveSleepMetric(
                selectedDate,
                sleepMetrics,
            );

            setIsDirty(false);
            setSaveStatus("saved");

        } catch (error) {

            console.error(error);
            setSaveStatus("failed");

        }

    }


    /*
    Update the page state whenever
    the user changes a value.
    */
    function updateSleepMetrics(
        action: React.SetStateAction<SleepMetrics>
    ) {

        setIsDirty(true);
        setSaveStatus("idle");
        setSleepMetrics(action);

    }


    /*
    Display a loading indicator while
    Sleep Metrics are being retrieved.
    */
    if (isLoading) {

        return <LoadingSpinner />;

    }


    /*
    Page Layout
    */
    return (

        <PageContainer>

            <div className="space-y-8">

                <LogTodayHeader
                    isDirty={isDirty}
                />

                <DateSection
                    selectedDate={selectedDate}
                    setSelectedDate={setSelectedDate}
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

                <CollapsibleCard
                    title="Sleep Metrics"
                    icon={Moon}
                    iconColor="text-indigo-600"
                >

                    <SleepMetricsSection
                        sleepMetrics={sleepMetrics}
                        setSleepMetrics={updateSleepMetrics}
                    />

                </CollapsibleCard>

                <SaveButton
                    onClick={handleSaveSleepMetrics}
                    isDirty={isDirty}
                    saveStatus={saveStatus}
                />

            </div>

        </PageContainer>

    );

}

export default LogSleepMetrics;