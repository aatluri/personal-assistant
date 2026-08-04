/*
    Displays today's key metrics.

    These values are currently hardcoded.
    Later they will come from the backend.
*/

function Scoreboard() {
    return (
        <div>

            <h2>Today's Scoreboard</h2>

            <p>Weight: 80.3 kg</p>
            <p>Protein: 110 / 130 g</p>
            <p>Water: 2.7 / 3.0 L</p>

            <p>Sleep: 7h 42m</p>
            <p>Steps: 10,542</p>
            <p>Calories: 620 / 2450</p>

        </div>
    );
}

export default Scoreboard;