function Start(db) {
    getMatchGoals(db, makeChart);
}

function makeChart(goals) {
    var ctx = document.getElementById('goalsChartTop').getContext('2d');

    orange_goals = [];
    blue_goals = [];

    goals.forEach(g => {
        var datum = {
            x: g['pos_z'],
            y: g['pos_x']
        }
        // ignore 0,0,0 goals
        if (g['pos_x'] != 0 || g['pos_y'] != 0 || g['pos_z'] != 0) {
            if (g['goal_color'] == 'blue') {
                orange_goals.push(datum);
            }
            if (g['goal_color'] == 'orange') {
                blue_goals.push(datum)
            }
        }
    });

    var zscale = 40.3;
    var xscale = 16;
    var goalsChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Orange Goals',
                data: orange_goals,
                backgroundColor: '#ee4400aa',
                pointHoverRadius: 10,
            },
            {
                label: 'Blue Goals',
                data: blue_goals,
                backgroundColor: '#0083d3aa',
                pointHoverRadius: 10,
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: true,
            scales: {
                yAxes: [{
                    ticks: {
                        min: -xscale,
                        max: xscale,
                        display: false
                    },
                    gridLines: {
                        color: "#ffffff",
                        display: false
                    },
                    display: false
                }],
                xAxes: [{
                    ticks: {
                        min: -zscale,
                        max: zscale,
                        display: false
                    },
                    gridLines: {
                        color: "#ffffff",
                        display: false
                    },
                    display: false
                }]
            },
            legend: {
                display: false
            },
            elements: {
                point: {
                    radius: 8,
                }
            },
            // events: [],
            animation: false
        }
    });

    fadeInWhenDone();
}
