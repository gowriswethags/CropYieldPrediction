const ctx = document.getElementById('myChart');

let myChart;
let jsonData

fetch('../static/crop_type.json')


    .then(function (response) {
        if (response.ok == true) {
            return response.json();
        }
    })

    .then(function (data) {

        jsonData = data;
        createChart(data, 'bar');
    });

function setChartType(chartType) {
    myChart.destroy();

    createChart(jsonData, chartType)
}

function createChart(data, type) {

    myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: data.map(row => row.crop_type),
            datasets: [{
                label: 'Average yield based on the crop type',
                data: data.map(row => row.yield),
                borderWidth: 2,
                borderRadius:20,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        
                        callback: function (value) {
                            return value.toFixed(2); 
                        }
                    }
                }
            },
            maintainAspectRatio: false
        }
    });
}