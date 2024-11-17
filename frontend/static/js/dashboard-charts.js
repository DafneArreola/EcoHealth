document.addEventListener('DOMContentLoaded', function() {
    // Get the data from the template
    const rawData = document.getElementById('twin-state-data');
    if (!rawData) {
        console.error('Twin state data element not found');
        return;
    }   

    let twinState;
    try {
        twinState = JSON.parse(rawData.textContent);
    } catch (e) {
        console.error('Failed to parse twin state data:', e);
        return;
    }

    // Common chart options
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    font: {
                        size: 12
                    }
                }
            }
        }
    };

    // 1. Radar Chart
    try {
        const radarCtx = document.getElementById('radarChart').getContext('2d');
        new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: ['Transportation', 'Diet', 'Consumption', 'Exercise', 'Sleep', 'Wellness'],
                datasets: [{
                    label: 'Current Scores',
                    data: [
                        twinState.environmental.transportation.score,
                        twinState.environmental.diet.score,
                        twinState.environmental.consumption.score,
                        twinState.health.exercise.score,
                        twinState.health.sleep.score,
                        twinState.health.wellness.score
                    ],
                    backgroundColor: 'rgba(76, 175, 80, 0.2)',
                    borderColor: 'rgba(76, 175, 80, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(76, 175, 80, 1)',
                    pointRadius: 4
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            display: false, // Hide scale numbers
                            stepSize: 20
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        angleLines: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        pointLabels: {
                            font: {
                                size: 12
                            }
                        }
                    }
                }
            }
        });
    } catch (e) {
        console.error('Failed to create radar chart:', e);
    }

    // 2. Environmental Chart
    try {
        const envCtx = document.getElementById('environmentalChart').getContext('2d');
        new Chart(envCtx, {
            type: 'bar',
            data: {
                labels: ['Transportation', 'Diet', 'Consumption'],
                datasets: [{
                    label: 'Environmental Scores',
                    data: [
                        twinState.environmental.transportation.score,
                        twinState.environmental.diet.score,
                        twinState.environmental.consumption.score
                    ],
                    backgroundColor: 'rgba(76, 175, 80, 0.6)',
                    borderColor: 'rgba(76, 175, 80, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    ...commonOptions.plugins,
                    title: {
                        display: true,
                        text: 'Environmental Impact Breakdown',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                }
            }
        });
    } catch (e) {
        console.error('Failed to create environmental chart:', e);
    }

    // 3. Health Chart
    try {
        const healthCtx = document.getElementById('healthChart').getContext('2d');
        new Chart(healthCtx, {
            type: 'bar',
            data: {
                labels: ['Exercise', 'Sleep', 'Wellness'],
                datasets: [{
                    label: 'Health Scores',
                    data: [
                        twinState.health.exercise.score,
                        twinState.health.sleep.score,
                        twinState.health.wellness.score
                    ],
                    backgroundColor: 'rgba(33, 150, 243, 0.6)',
                    borderColor: 'rgba(33, 150, 243, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    ...commonOptions.plugins,
                    title: {
                        display: true,
                        text: 'Health Metrics Breakdown',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    }
                }
            }
        });
    } catch (e) {
        console.error('Failed to create health chart:', e);
    }

    // Add resize handler for responsiveness
    window.addEventListener('resize', function() {
        Chart.instances.forEach(chart => {
            chart.resize();
        });
    });
});

class WellnessAnalyzer {
    constructor() {
        this.video = document.getElementById('webcam');
        this.canvas = document.getElementById('webcam-canvas');
        this.startButton = document.getElementById('start-camera');
        this.captureButton = document.getElementById('capture-image');
        this.resultsContainer = document.getElementById('analysis-content');
        this.loadingSpinner = document.getElementById('loading-analysis');
        this.stream = null;

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.startButton.addEventListener('click', () => this.toggleCamera());
        this.captureButton.addEventListener('click', () => this.captureAndAnalyze());
    }

    async toggleCamera() {
        if (this.stream) {
            this.stopCamera();
        } else {
            await this.startCamera();
        }
    }

    async startCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                }
            });
            this.video.srcObject = this.stream;
            this.startButton.textContent = '⏹ Stop Camera';
            this.captureButton.disabled = false;
        } catch (error) {
            console.error('Error accessing camera:', error);
            alert('Unable to access camera. Please ensure you have granted camera permissions.');
        }
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
            this.video.srcObject = null;
            this.startButton.textContent = '📹 Start Camera';
            this.captureButton.disabled = true;
        }
    }

    async captureAndAnalyze() {
        if (!this.stream) return;

        // Setup canvas and capture image
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        const context = this.canvas.getContext('2d');
        context.drawImage(this.video, 0, 0);

        // Convert to base64
        const imageData = this.canvas.toDataURL('image/jpeg');

        // Show loading state
        this.loadingSpinner.style.display = 'flex';
        this.resultsContainer.innerHTML = '';

        try {
            // Send to backend for analysis
            const response = await fetch('/api/analyze-wellness', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageData })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.displayResults(data.analysis);
            } else {
                throw new Error(data.message || 'Analysis failed');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.resultsContainer.innerHTML = `
                <div class="error-message">
                    Analysis failed. Please try again.
                    <br>
                    Error: ${error.message}
                </div>
            `;
        } finally {
            this.loadingSpinner.style.display = 'none';
        }
    }

    displayResults(analysis) {
        // Parse the analysis text and create structured HTML
        const insights = this.parseAnalysis(analysis);
        
        const resultsHTML = insights.map(insight => `
            <div class="wellness-insight">
                <h4>${insight.title}</h4>
                <p>${insight.observation}</p>
                <div class="wellness-tip">
                    <strong>Recommendation:</strong> ${insight.recommendation}
                </div>
            </div>
        `).join('');

        this.resultsContainer.innerHTML = resultsHTML;
    }

    parseAnalysis(analysisText) {
        // Simple parsing of GPT's response - you might need to adjust based on your actual response format
        const insights = [];
        const sections = analysisText.split('\n\n');

        sections.forEach(section => {
            if (section.trim()) {
                const lines = section.split('\n');
                insights.push({
                    title: lines[0].replace(':', '').trim(),
                    observation: lines[1]?.trim() || '',
                    recommendation: lines[2]?.replace('Recommendation:', '').trim() || ''
                });
            }
        });

        return insights;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new WellnessAnalyzer();
});