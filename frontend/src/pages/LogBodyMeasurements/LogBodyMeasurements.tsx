import { useEffect, useState } from "react";
import { User } from "lucide-react";

import {
    getBodyMeasurement,
    saveBodyMeasurement,
} from "../../api/health";

import type { BodyMeasurements } from "../../types/BodyMeasurements";

import LoadingSpinner from "../../components/LoadingSpinner";
import SaveButton from "../../components/SaveButton";
import PageContainer from "../../components/PageContainer";
import CollapsibleCard from "../../components/CollapsibleCard";

import LogTodayHeader from "../LogToday/components/LogTodayHeader";
import DateSection from "../LogToday/components/DateSection";
import BodyMeasurementsSection from "./components/BodyMeasurementsSection";

import { createEmptyBodyMeasurements } from "../../utils/createEmptyBodyMeasurements";

function LogBodyMeasurements() {

    /*
        Today's date in YYYY-MM-DD format.
    */
    const today = new Date().toLocaleDateString("en-CA");

    /*
        Currently selected date.
    */
    const [selectedDate, setSelectedDate] = useState(today);

    /*
        Page state.
    */
    const [isLoading, setIsLoading] = useState(true);
    const [isDirty, setIsDirty] = useState(false);

    const [saveStatus, setSaveStatus] = useState<
        "idle" | "saving" | "saved" | "failed"
    >("saved");

    /*
        Current body measurements.
    */
    const [bodyMeasurements, setBodyMeasurements] =
        useState<BodyMeasurements>(
            createEmptyBodyMeasurements()
        );

    /*
        Load the measurements whenever the
        selected date changes.
    */
    useEffect(() => {

        async function loadBodyMeasurements() {

            setIsLoading(true);

            try {

                const existingMeasurements =
                    await getBodyMeasurement(selectedDate);

                if (existingMeasurements) {

                    setBodyMeasurements(existingMeasurements);

                } else {

                    setBodyMeasurements(
                        createEmptyBodyMeasurements()
                    );

                }

                setIsDirty(false);
                setSaveStatus("saved");

            } catch (error) {

                console.error(
                    "Failed to load Body Measurements:",
                    error
                );

            } finally {

                setIsLoading(false);

            }

        }

        loadBodyMeasurements();

    }, [selectedDate]);

    /*
        Save Body Measurements.
    */
    async function handleSaveBodyMeasurements() {

        setSaveStatus("saving");

        try {

            await saveBodyMeasurement(
                selectedDate,
                bodyMeasurements,
            );

            setIsDirty(false);
            setSaveStatus("saved");

        } catch (error) {

            console.error(error);
            setSaveStatus("failed");

        }

    }

    /*
        Update state and mark page dirty.
    */
    function updateBodyMeasurements(
        action: React.SetStateAction<BodyMeasurements>
    ) {

        setIsDirty(true);
        setSaveStatus("idle");
        setBodyMeasurements(action);

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
                    title="Body Measurements"
                    icon={User}
                    iconColor="text-violet-600"
                >

                    <BodyMeasurementsSection
                        bodyMeasurements={bodyMeasurements}
                        setBodyMeasurements={updateBodyMeasurements}
                    />

                </CollapsibleCard>

                <SaveButton
                    onClick={handleSaveBodyMeasurements}
                    isDirty={isDirty}
                    saveStatus={saveStatus}
                />

            </div>

        </PageContainer>

    );

}

export default LogBodyMeasurements;