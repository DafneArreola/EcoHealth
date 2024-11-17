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