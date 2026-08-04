/*
    This component displays the body-related
    measurements for the current day.

    At the moment, it contains only weight.
    More measurements may be added in future.
*/

function BodySection() {
  return (
    <section>

      {/* Section Heading */}
      <h2>Body</h2>

      {/* Weight Field */}
      <div>

        {/* Label for the weight input */}
        <label htmlFor="weight">
          Weight (kg)
        </label>

        {/* Numeric input for today's weight */}
        <input
          id="weight"
          name="weight"
          type="number"
          step="0.1"
          min="0"
          defaultValue="80.3"
        />

      </div>

    </section>
  );
}

export default BodySection;