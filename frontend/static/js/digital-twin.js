document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for dashboard navigation
    const dashboardLinks = document.querySelectorAll('.dashboard-link');
    dashboardLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            targetSection.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Simulation functionality
    const simulationButton = document.querySelector('.simulation-button');
    const simulationResults = document.getElementById('simulation-results');

    if (simulationButton) {
        simulationButton.addEventListener('click', async () => {
            const changeType = document.getElementById('change-type').value;
            const changeDescription = document.getElementById('change-description').value;

            if (!changeDescription) {
                alert('Please describe the proposed change');
                return;
            }

            // Show loading state
            simulationResults.innerHTML = `
                <div class="feature">
                    <p>Simulating changes...</p>
                </div>
            `;

            try {
                const response = await fetch('/api/simulate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        changes: [{
                            type: changeType,
                            change: changeDescription,
                            timeline: '4 weeks'
                        }]
                    })
                });

                if (!response.ok) throw new Error('Simulation failed');
                const data = await response.json();

                // Format the results
                const envScoreChange = data.analysis.environmental_impact.score_change.toFixed(1);
                const carbonReduction = data.analysis.environmental_impact.carbon_reduction.toFixed(1);
                const healthScoreChange = data.analysis.health_impact.score_change.toFixed(1);

                simulationResults.innerHTML = `
                    <div class="feature">
                        <h3>Simulation Results</h3>
                        <div class="result-grid">
                            <div class="result-item ${envScoreChange > 0 ? 'positive' : 'negative'}">
                                <h4>Environmental Impact</h4>
                                <p>${envScoreChange > 0 ? '+' : ''}${envScoreChange} points</p>
                            </div>
                            <div class="result-item ${carbonReduction < 0 ? 'positive' : 'negative'}">
                                <h4>Carbon Reduction</h4>
                                <p>${carbonReduction} tons/year</p>
                            </div>
                            <div class="result-item ${healthScoreChange > 0 ? 'positive' : 'negative'}">
                                <h4>Health Impact</h4>
                                <p>${healthScoreChange > 0 ? '+' : ''}${healthScoreChange} points</p>
                            </div>
                        </div>
                        <div class="timeline">
                            <p>Expected Timeline: ${data.analysis.timeline}</p>
                        </div>
                    </div>
                `;
            } catch (error) {
                console.error('Simulation error:', error);
                simulationResults.innerHTML = `
                    <div class="feature error">
                        <p>Error running simulation. Please try again.</p>
                    </div>
                `;
            }
        });
    }
document.addEventListener('DOMContentLoaded', function() {
    // Handle simulation form submission
    const simulationForm = document.getElementById('simulation-form');
    const simulationResults = document.getElementById('simulation-results');

    if (simulationForm) {
        simulationForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const changeType = document.getElementById('change-type').value;
            const changeDescription = document.getElementById('change-description').value;

            if (!changeDescription) {
                alert('Please describe the proposed change');
                return;
            }

            // Show loading state
            simulationResults.innerHTML = '<div class="feature"><p>Simulating changes...</p></div>';

            try {
                const response = await fetch('/api/simulate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        changes: [{
                            type: changeType,
                            change: changeDescription,
                            timeline: '4 weeks'
                        }]
                    })
                });

                if (!response.ok) throw new Error('Simulation failed');
                const data = await response.json();

                // Format the results
                const envScoreChange = data.analysis.environmental_impact.score_change.toFixed(1);
                const carbonReduction = Math.abs(data.analysis.environmental_impact.carbon_reduction).toFixed(1);
                const healthScoreChange = data.analysis.health_impact.score_change.toFixed(1);

                simulationResults.innerHTML = `
                    <div class="feature result-grid">
                        <div class="result-item ${envScoreChange > 0 ? 'positive' : 'negative'}">
                            <h4>Environmental Impact</h4>
                            <p>${envScoreChange > 0 ? '+' : ''}${envScoreChange} points</p>
                        </div>
                        <div class="result-item positive">
                            <h4>Carbon Reduction</h4>
                            <p>${carbonReduction} tons/year</p>
                        </div>
                        <div class="result-item ${healthScoreChange > 0 ? 'positive' : 'negative'}">
                            <h4>Health Impact</h4>
                            <p>${healthScoreChange > 0 ? '+' : ''}${healthScoreChange} points</p>
                        </div>
                        <div class="timeline">
                            <p>Expected Timeline: ${data.analysis.timeline}</p>
                        </div>
                    </div>
                `;

                // Smooth scroll to results
                simulationResults.scrollIntoView({ behavior: 'smooth' });

            } catch (error) {
                console.error('Simulation error:', error);
                simulationResults.innerHTML = `
                    <div class="feature error">
                        <p>Error running simulation. Please try again.</p>
                    </div>
                `;
            }
        });
    }

    // Add scroll animation for score cards
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.score-card').forEach(card => {
        observer.observe(card);
        card.classList.add('animate-on-scroll');
    });
});

    // Add scroll animation
    const scrollTriggered = document.querySelectorAll('.scroll-triggered');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    scrollTriggered.forEach(element => {
        observer.observe(element);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Handle simulation form submission
    const simulationForm = document.getElementById('simulation-form');
    const simulationResults = document.getElementById('simulation-results');

    if (simulationForm) {
        simulationForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const changeType = document.getElementById('change-type').value;
            const changeDescription = document.getElementById('change-description').value;

            if (!changeDescription) {
                alert('Please describe the proposed change');
                return;
            }

            // Show loading state
            simulationResults.innerHTML = '<div class="feature"><p>Simulating changes...</p></div>';

            try {
                const response = await fetch('/api/simulate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        changes: [{
                            type: changeType,
                            change: changeDescription,
                            timeline: '4 weeks'
                        }]
                    })
                });

                if (!response.ok) throw new Error('Simulation failed');
                const data = await response.json();

                // Format the results
                const envScoreChange = data.analysis.environmental_impact.score_change.toFixed(1);
                const carbonReduction = Math.abs(data.analysis.environmental_impact.carbon_reduction).toFixed(1);
                const healthScoreChange = data.analysis.health_impact.score_change.toFixed(1);

                simulationResults.innerHTML = `
                    <div class="feature result-grid">
                        <div class="result-item ${envScoreChange > 0 ? 'positive' : 'negative'}">
                            <h4>Environmental Impact</h4>
                            <p>${envScoreChange > 0 ? '+' : ''}${envScoreChange} points</p>
                        </div>
                        <div class="result-item positive">
                            <h4>Carbon Reduction</h4>
                            <p>${carbonReduction} tons/year</p>
                        </div>
                        <div class="result-item ${healthScoreChange > 0 ? 'positive' : 'negative'}">
                            <h4>Health Impact</h4>
                            <p>${healthScoreChange > 0 ? '+' : ''}${healthScoreChange} points</p>
                        </div>
                        <div class="timeline">
                            <p>Expected Timeline: ${data.analysis.timeline}</p>
                        </div>
                    </div>
                `;

                // Smooth scroll to results
                simulationResults.scrollIntoView({ behavior: 'smooth' });

            } catch (error) {
                console.error('Simulation error:', error);
                simulationResults.innerHTML = `
                    <div class="feature error">
                        <p>Error running simulation. Please try again.</p>
                    </div>
                `;
            }
        });
    }

    // Add scroll animation for score cards
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.score-card').forEach(card => {
        observer.observe(card);
        card.classList.add('animate-on-scroll');
    });
});

// Add these styles to your CSS
const styles = `
    .result-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }

    .result-item {
        padding: 1rem;
        border-radius: 8px;
        background: #f8f9fa;
        text-align: center;
    }

    .result-item.positive {
        background: #d4edda;
        color: #155724;
    }

    .result-item.negative {
        background: #f8d7da;
        color: #721c24;
    }

    .timeline {
        margin-top: 1rem;
        padding: 1rem;
        background: #e9ecef;
        border-radius: 8px;
        text-align: center;
    }

    .error {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }

    .scroll-triggered {
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.6s ease-out;
    }

    .scroll-triggered.visible {
        opacity: 1;
        transform: translateY(0);
    }
`;