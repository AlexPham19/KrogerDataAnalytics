window.renderBasketChart = (labels, liftData, confidenceData, supportData) => {

    console.log("Rendering chart...");

    const canvas = document.getElementById('basketChart');

    if (!canvas) {
        console.error("Canvas not found!");
        return;
    }

    const ctx = canvas.getContext('2d');

    if (window.basketChartInstance) {
        window.basketChartInstance.destroy();
    }

    window.basketChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Lift',
                    data: liftData
                },
                {
                    label: 'Confidence',
                    data: confidenceData
                },
                {
                    label: 'Support',
                    data: supportData
                }
            ]
        },
        options: {
            responsive: true,
            indexAxis: 'y'
        }
    });
    console.log("basketChart.js loaded");
};