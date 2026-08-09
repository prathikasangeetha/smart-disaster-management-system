/* Chart.js Dashboard Visualizations */

document.addEventListener('DOMContentLoaded', function () {
    const typeChartCtx = document.getElementById('disasterTypeChart');
    const statusChartCtx = document.getElementById('disasterStatusChart');
    const severityChartCtx = document.getElementById('disasterSeverityChart');

    if (!typeChartCtx && !statusChartCtx && !severityChartCtx) {
        return; // Not on dashboard page
    }

    fetch('/api/dashboard-charts')
        .then(response => response.json())
        .then(data => {
            // 1. Disaster by Type (Doughnut Chart)
            if (typeChartCtx) {
                const typeLabels = Object.keys(data.by_type);
                const typeData = Object.values(data.by_type);

                new Chart(typeChartCtx, {
                    type: 'doughnut',
                    data: {
                        labels: typeLabels.length ? typeLabels : ['No Data'],
                        datasets: [{
                            data: typeData.length ? typeData : [1],
                            backgroundColor: [
                                '#0d6efd', '#dc3545', '#ffc107', '#198754',
                                '#0dcaf0', '#6f42c1', '#fd7e14', '#20c997'
                            ],
                            borderWidth: 2,
                            borderColor: '#ffffff'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'bottom' }
                        }
                    }
                });
            }

            // 2. Disaster Status (Pie Chart)
            if (statusChartCtx) {
                const statusLabels = Object.keys(data.by_status);
                const statusData = Object.values(data.by_status);

                new Chart(statusChartCtx, {
                    type: 'pie',
                    data: {
                        labels: statusLabels.length ? statusLabels : ['No Data'],
                        datasets: [{
                            data: statusData.length ? statusData : [1],
                            backgroundColor: ['#ffc107', '#dc3545', '#198754'],
                            borderWidth: 2,
                            borderColor: '#ffffff'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'bottom' }
                        }
                    }
                });
            }

            // 3. Severity Breakdown (Bar Chart)
            if (severityChartCtx) {
                const severityLabels = Object.keys(data.by_severity);
                const severityData = Object.values(data.by_severity);

                new Chart(severityChartCtx, {
                    type: 'bar',
                    data: {
                        labels: severityLabels.length ? severityLabels : ['Low', 'Medium', 'High'],
                        datasets: [{
                            label: 'Incidents Count',
                            data: severityData.length ? severityData : [0, 0, 0],
                            backgroundColor: ['#198754', '#ffc107', '#dc3545'],
                            borderRadius: 8
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: { beginAtZero: true, ticks: { stepSize: 1 } }
                        },
                        plugins: {
                            legend: { display: false }
                        }
                    }
                });
            }
        })
        .catch(err => console.error('Error loading dashboard charts:', err));
});
