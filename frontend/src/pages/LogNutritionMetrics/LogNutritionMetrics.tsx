/*
LogNutritionMetrics

Page responsible for viewing and editing
Nutrition Metrics for a selected date.

Responsibilities:
- Load Nutrition Metrics from the backend.
- Maintain the page state.
- Pass state to the UI section.
- Save changes back to the backend.
*/

import { useEffect, useState } from "react";
import { Apple } from "lucide-react";

import {
    getNutritionMetric,
    saveNutritionMetric,
} from "../../api/nutritionMetrics";

import type { NutritionMetrics } from "../../types/NutritionMetrics";

import LoadingSpinner from "../../components/LoadingSpinner";
import SaveButton from "../../components/SaveButton";
import PageContainer from "../../components/PageContainer";
import CollapsibleCard from "../../components/CollapsibleCard";

import LogTodayHeader from "../LogToday/components/LogTodayHeader";
import DateSection from "../LogToday/components/DateSection";
import NutritionMetricsSection from "./components/NutritionMetricsSection";

import { createEmptyNutritionMetrics } from "../../utils/createEmptyNutritionMetrics";


function LogNutritionMetrics() {

    /*
    Today's date in YYYY-MM-DD format.
    */
    const today = new Date().toLocaleDateString("en-CA");

    /*
    Currently selected date.

    Changing this value automatically
    reloads Nutrition Metrics for that date.
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

    /*
    Holds the Nutrition Metrics currently
    displayed on the page.
    */
    const [nutritionMetrics, setNutritionMetrics] =
        useState<NutritionMetrics>(
            createEmptyNutritionMetrics()
        );


    /*
    Whenever the selected date changes,
    retrieve Nutrition Metrics from the backend.
    */
    useEffect(() => {

        async function loadNutritionMetrics() {

            setIsLoading(true);

            try {

                const existingNutritionMetrics =
                    await getNutritionMetric(selectedDate);

                if (existingNutritionMetrics) {

                    setNutritionMetrics(
                        existingNutritionMetrics
                    );

                } else {

                    setNutritionMetrics(
                        createEmptyNutritionMetrics()
                    );

                }

                setIsDirty(false);
                setSaveStatus("saved");

            } catch (error) {

                console.error(
                    "Failed to load Nutrition Metrics:",
                    error
                );

            } finally {

                setIsLoading(false);

            }

        }

        loadNutritionMetrics();

    }, [selectedDate]);


    /*
    Save the current Nutrition Metrics
    to the backend.
    */
    async function handleSaveNutritionMetrics() {

        setSaveStatus("saving");

        try {

            await saveNutritionMetric(
                selectedDate,
                nutritionMetrics,
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
    function updateNutritionMetrics(
        action: React.SetStateAction<NutritionMetrics>
    ) {

        setIsDirty(true);
        setSaveStatus("idle");
        setNutritionMetrics(action);

    }


    /*
    Display a loading indicator while
    Nutrition Metrics are being retrieved.
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

                <CollapsibleCard
                    title="Nutrition Metrics"
                    icon={Apple}
                    iconColor="text-green-600"
                >

                    <NutritionMetricsSection
                        nutritionMetrics={nutritionMetrics}
                        setNutritionMetrics={updateNutritionMetrics}
                    />

                </CollapsibleCard>

                <SaveButton
                    onClick={handleSaveNutritionMetrics}
                    isDirty={isDirty}
                    saveStatus={saveStatus}
                />

            </div>

        </PageContainer>

    );

}

export default LogNutritionMetrics;