/*
    This component displays the workout section
    of the Log Today page.

    For now, the form fields use default values.
    Later, React state will manage these values.
*/

function WorkoutSection() {
  return (
    <section>
      {/* Section heading */}
      <h2>Workout</h2>

      {/* Workout type field */}
      <div>
        <label htmlFor="workout-type">Workout Type</label>

        <select id="workout-type" name="workoutType" defaultValue="HIIT">
          <option value="HIIT">HIIT</option>
          <option value="Strength">Strength</option>
          <option value="Cardio">Cardio</option>
          <option value="Mobility">Mobility</option>
          <option value="Rest">Rest</option>
        </select>
      </div>

      {/* Workout duration in minutes */}
      <div>
        <label htmlFor="workout-duration">Duration (minutes)</label>

        <input
          id="workout-duration"
          name="workoutDuration"
          type="number"
          min="0"
          defaultValue="58"
        />
      </div>

      {/* Calories burnt during the workout */}
      <div>
        <label htmlFor="workout-calories">Calories Burnt</label>

        <input
          id="workout-calories"
          name="workoutCalories"
          type="number"
          min="0"
          defaultValue="620"
        />
      </div>

      {/* Total workout volume in kilograms */}
      <div>
        <label htmlFor="workout-volume">Volume (kg)</label>

        <input
          id="workout-volume"
          name="workoutVolume"
          type="number"
          min="0"
          defaultValue="5975"
        />
      </div>

      {/* Total number of sets completed */}
      <div>
        <label htmlFor="workout-sets">Sets</label>

        <input
          id="workout-sets"
          name="workoutSets"
          type="number"
          min="0"
          defaultValue="50"
        />
      </div>

      {/* Average heart rate during the workout */}
      <div>
        <label htmlFor="average-heart-rate">
          Average Heart Rate (bpm)
        </label>

        <input
          id="average-heart-rate"
          name="averageHeartRate"
          type="number"
          min="0"
          defaultValue="140"
        />
      </div>

      {/* Multi-line field for entering the workout details */}
      <div>
        <label htmlFor="workout-summary">Workout Summary</label>

        <textarea
          id="workout-summary"
          name="workoutSummary"
          rows={8}
          defaultValue={`   Battle Rope - 5 min
                            Row - 1.25 km
                            Push-ups - 50
                            Kettlebell Swings - 50`}
        />
      </div>
    </section>
  );
}

export default WorkoutSection;