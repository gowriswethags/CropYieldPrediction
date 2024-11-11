document.addEventListener('DOMContentLoaded', () => {
    fetch('/detailed_analysis')
        .then(response => response.json())
        .then(data => {
            const analysisResult = document.getElementById('analysis-result');
            analysisResult.innerHTML = `
                <p><strong>Average Yield:</strong> ${data.average_yield.toFixed(2)} metric tons per hectare</p>
                <p><strong>Maximum Yield:</strong> ${data.max_yield.toFixed(2)} metric tons per hectare</p>
                <p><strong>Minimum Yield:</strong> ${data.min_yield.toFixed(2)} metric tons per hectare</p>
                <p><strong>Yield by Crop Type:</strong></p>
                <ul>
                    ${Object.entries(data.yield_by_crop_type).map(([crop, yield]) => `<li>${crop}: ${yield.toFixed(2)} metric tons per hectare</li>`).join('')}
                </ul>
            `;
        })
        .catch(error => {
            console.error('Error fetching detailed analysis:', error);
        });

    document.getElementById('back-button').addEventListener('click', () => {
        window.location.href = '/';
    });
});
