document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const dashboardSections = document.querySelectorAll('.dashboard-section');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and sections
            tabButtons.forEach(btn => btn.classList.remove('active'));
            dashboardSections.forEach(section => section.classList.remove('active'));

            // Add active class to clicked button and corresponding section
            button.classList.add('active');
            const tabId = button.dataset.tab;
            document.getElementById(`${tabId}-section`).classList.add('active');
        });
    });

    // Simulation form handling
    const simulationForm = document.querySelector('.simulation-form');
    const simulationResults = document.getElementById('simulation-results');

    if (simulationForm) {
        simulationForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Mock simulation results
            simulationResults.innerHTML = `
                <div class="simulation-result-card">
                    <h4>Simulation Results</h4>
                    <div class="result-item">
                        <span>Environmental Score Change:</span>
                        <span class="positive">+5 points</span>
                    </div>
                    <div class="result-item">
                        <span>Carbon Reduction:</span>
                        <span class="positive">-0.8 tons/year</span>
                    </div>
                    <div class="result-item">
                        <span>Health Score Change:</span>
                        <span class="positive">+3 points</span>
                    </div>
                    <div class="result-item">
                        <span>Timeline:</span>
                        <span>4 weeks</span>
                    </div>
                </div>
            `;
        });
    }
});