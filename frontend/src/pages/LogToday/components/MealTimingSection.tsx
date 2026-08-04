/*
    This component captures the user's
    meal timings for the day.

    These values will later be used to
    calculate the eating window and
    fasting window.
*/

function MealTimingSection() {
  return (
    <section>

      {/* Section Heading */}
      <h2>Meal Timing</h2>

      {/* First Meal Time */}
      <div>

        <label htmlFor="first-meal-time">
          First Meal Time
        </label>

        <input
          id="first-meal-time"
          name="firstMealTime"
          type="time"
          defaultValue="08:30"
        />

      </div>

      {/* Last Meal Time */}
      <div>

        <label htmlFor="last-meal-time">
          Last Meal Time
        </label>

        <input
          id="last-meal-time"
          name="lastMealTime"
          type="time"
          defaultValue="19:45"
        />

      </div>

    </section>
  );
}

export default MealTimingSection;