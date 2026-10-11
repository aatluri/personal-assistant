/*
LogHealthMetrics

Page responsible for viewing and editing
Health Metrics for a selected date.

Responsibilities:
- Load Health Metrics from the backend.
- Maintain the page state.
- Pass state to the UI section.
- Save changes back to the backend.
*/

import { useEffect, useState } from "react";
import { HeartPulse } from "lucide-react";

import {
    getHealthMetric,
    saveHealthMetric,
} from "../../api/healthMetrics";

import type { HealthMetrics } from "../../types/HealthMetrics";

import LoadingSpinner from "../../components/LoadingSpinner";
import SaveButton from "../../components/SaveButton";
import PageContainer from "../../components/PageContainer";
import CollapsibleCard from "../../components/CollapsibleCard";

import LogTodayHeader from "../LogToday/components/LogTodayHeader";
import DateSection from "../LogToday/components/DateSection";
import HealthMetricsSection from "./components/HealthMetricsSection";

import { createEmptyHealthMetrics } from "../../utils/createEmptyHealthMetrics";


function LogHealthMetrics() {

    const today = new Date().toLocaleDateString("en-CA");

    const [selectedDate, setSelectedDate] = useState(today);

    const [isLoading, setIsLoading] = useState(true);

    const [isDirty, setIsDirty] = useState(false);

    const [saveStatus, setSaveStatus] = useState<
        "idle" | "saving" | "saved" | "failed"
    >("saved");


    const [healthMetrics, setHealthMetrics] =
        useState<HealthMetrics>(
            createEmptyHealthMetrics()
        );


    /*
    Reload Health Metrics whenever the selected
    date changes.
    */
    useEffect(() => {

        async function loadHealthMetrics() {

            setIsLoading(true);

            try {

                const existingHealthMetrics =
                    await getHealthMetric(selectedDate);

                if (existingHealthMetrics) {

                    setHealthMetrics(existingHealthMetrics);

                } else {

                    setHealthMetrics(
                        createEmptyHealthMetrics()
                    );

                }

                setIsDirty(false);
                setSaveStatus("saved");

            } catch (error) {

                console.error(
                    "Failed to load Health Metrics:",
                    error
                );

            } finally {

                setIsLoading(false);

            }

        }

        loadHealthMetrics();

    }, [selectedDate]);


    /*
    Save the current Health Metrics record.
    */
    async function handleSaveHealthMetrics() {

        setSaveStatus("saving");

        try {

            await saveHealthMetric(
                selectedDate,
                healthMetrics,
            );

            setIsDirty(false);
            setSaveStatus("saved");

        } catch (error) {

            console.error(error);

            setSaveStatus("failed");

        }

    }


    /*
    Wrapper around setHealthMetrics.

    Any change to the Health Metrics state marks
    the page as having unsaved changes.
    */
    function updateHealthMetrics(
        action: React.SetStateAction<HealthMetrics>
    ) {

        setIsDirty(true);
        setSaveStatus("idle");

        setHealthMetrics(action);

    }


    if (isLoading) {
        return <LoadingSpinner />;
    }


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
                    title="Health Metrics"
                    icon={HeartPulse}
                    iconColor="text-red-600"
                >

                    <HealthMetricsSection
                        healthMetrics={healthMetrics}
                        setHealthMetrics={updateHealthMetrics}
                    />

                </CollapsibleCard>

                <SaveButton
                    onClick={handleSaveHealthMetrics}
                    isDirty={isDirty}
                    saveStatus={saveStatus}
                />

            </div>

        </PageContainer>

    );

}

export default LogHealthMetrics;