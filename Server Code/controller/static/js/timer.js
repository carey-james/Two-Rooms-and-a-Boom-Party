// Function to fetch the current timer data from the server
function fetchCurrentTimer() {
    fetch('/api/current/')
        .then(response => response.json())
        .then(data => {
            if (data.remaining_seconds !== undefined) {
                const minutes = Math.floor(data.remaining_seconds / 60);
                const seconds = data.remaining_seconds % 60;
                const remainingTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

                // Update the timer display on the page
                document.getElementById('timer-display').innerHTML =
                    `<p>Time Remaining: ${remainingTime}</p>`;
            } else {
                document.getElementById('timer-display').innerHTML =
                    `<p>No active timer found.</p>`;
            }
        })
        .catch(error => {
            console.error('Error fetching timer:', error);
            document.getElementById('timer-display').innerHTML =
                `<p>Error loading timer.</p>`;
        });
}

// Fetch the current timer every second
setInterval(fetchCurrentTimer, 1000);

// Initial fetch when the page loads
fetchCurrentTimer();