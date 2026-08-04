// AchievementBanner.tsx

/*
    This component displays a summary of today's achievements.

    For now, the values are hardcoded.
    Later, these will come from the backend API.
*/

function AchievementBanner() {
    return (
        <div>

            {/* Section heading */}
            <h2>🔥 Achievement Banner</h2>

            {/* Motivational message */}
            <p>Great session today!</p>

            {/* Achievement summary */}
            <p>
                620 Calories Burned • Day 24 / 90 • Protein Goal Achieved
            </p>

        </div>
    );
}

// Make this component available to other files.
export default AchievementBanner;