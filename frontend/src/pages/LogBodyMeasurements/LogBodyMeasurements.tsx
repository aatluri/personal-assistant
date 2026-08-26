/*
    LogBodyMeasurements

    Page responsible for viewing and editing
    Body Measurements for a selected date.

    Responsibilities:
    - Load Body Measurements from the backend.
    - Maintain the page state.
    - Pass state to the UI sections.
    - Save changes back to the backend.
*/

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

    Used as the default date when the page
    is first opened.
    */
    const today = new Date().toLocaleDateString("en-CA");

    /*
    Currently selected date.

    Changing this value automatically
    reloads the Body Measurements for
    the selected date.
    */
    const [selectedDate, setSelectedDate] = useState(today);

    /*
    Page state.

    isLoading
        Indicates whether data is currently
        being loaded from the backend.

    isDirty
        Indicates whether the page contains
        unsaved changes.

    saveStatus
        Tracks the current save operation.
    */
    const [isLoading, setIsLoading] = useState(true);
    const [isDirty, setIsDirty] = useState(false);

    const [saveStatus, setSaveStatus] = useState<
        "idle" | "saving" | "saved" | "failed"
    >("saved");

    /*
    Holds the current Body Measurements
    displayed on the page.

    This is the single source of truth
    for all measurement values.
    */
    const [bodyMeasurements, setBodyMeasurements] =
        useState<BodyMeasurements>(
            createEmptyBodyMeasurements()
        );

    /*
    Whenever the selected date changes:

    1. Request the Body Measurements
       from the backend.
    2. Populate the page state.
    3. If no record exists, create an
       empty BodyMeasurements object.
    */
    useEffect(() => {
        /*
            Retrieve the Body Measurements
            for the selected date.
        */
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
        /*
            The [selectedDate] is called the dependency array.
            It tells React to Run this effect whenever selectedDate changes
        */
    }, [selectedDate]);

    /*
    Save the current Body Measurements
    to the backend.

    The Save button invokes this method.
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
    Update the page state whenever the
    user changes a value.

    Also marks the page as having
    unsaved changes.
    */
    function updateBodyMeasurements(
        action: React.SetStateAction<BodyMeasurements>
    ) {

        setIsDirty(true);
        setSaveStatus("idle");
        setBodyMeasurements(action);

    }

    /*
    Display a loading indicator while
    the Body Measurements are being
    retrieved from the backend.
    */
    if (isLoading) {

        return <LoadingSpinner />;

    }

    /*
    Page Layout

    PageContainer
        Provides the standard page layout.

    LogTodayHeader
        Displays the page heading and
        save status.

    DateSection
        Allows the user to choose the
        measurement date.

    CollapsibleCard
        Groups the Body Measurements UI.

    SaveButton
        Saves the current measurements.
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