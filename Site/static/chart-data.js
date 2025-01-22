
    // Define the data
    const data = '';

    // Parse the data and count the file extensions
    const lines = data.trim().split('\n');
    const extensionCounts = {};

    lines.forEach(line => {
        const parts = line.split('/');
        const fileName = parts[parts.length - 1];
        const extension = fileName.split('.').pop();
        if (extensionCounts[extension]) {
            extensionCounts[extension]++;
        } else {
            extensionCounts[extension] = 1;
        }
    });

    // Prepare data for Chart.js
    const labels = Object.keys(extensionCounts);
    const counts = Object.values(extensionCounts);

    // Define background colors
    const backgroundColors = [
        'rgba(75, 192, 192, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(199, 199, 199, 0.2)',
        'rgba(83, 102, 255, 0.2)',
        'rgba(255, 100, 64, 0.2)',
        'rgba(75, 200, 192, 0.2)',
        'rgba(255, 90, 86, 0.2)',
    ];

    // Extend or reduce backgroundColors array to match the number of labels
    const bgColors = backgroundColors.slice(0, labels.length);

    // Ensure we have enough colors for all labels
    while (bgColors.length < labels.length) {
        bgColors.push(...backgroundColors);
        bgColors.length = labels.length;
    }

    document.addEventListener("DOMContentLoaded", function() {
        // Create the Chart.js chart
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'File Extension Count',
                    data: counts,
                    backgroundColor: bgColors,
                    borderColor: bgColors.map(color => color.replace('0.2', '1')),
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
    