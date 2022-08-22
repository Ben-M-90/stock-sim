// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.color = '#b6c1d2';
Chart.defaults.font.family = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';



// Area Chart Example
var ctx = document.getElementById("stockDetailArea").getContext('2d');
var fillGradient = ctx.createLinearGradient(0, 0, 0, 175);
fillGradient.addColorStop(0, 'rgba(44,123,229,0.5)');
fillGradient.addColorStop(1, 'rgba(44,123,229,0)');
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
      labels: ["9:00", "10:00", "11:00", "12:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00"],
      datasets: [{
          fill: 'origin',
          label: "Earnings",
          lineTension: 0.3,
          backgroundColor: fillGradient,
          borderColor: "#2c7be5",
          borderWidth: 2,
          pointRadius: 2,
          pointBackgroundColor: "#fff",
          pointBorderColor: "#2c7be5",
          pointHoverRadius: 3,
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "#2c7be5",
          pointHitRadius: 10,
          pointBorderWidth: 1,
          data: [9.42, 3.14, 12.56, 3.14, 15.70, 28.26, 6.28, 18.84, 15.70, 9.42, 15.70, 25.12],
    }],
    },
    options: {
        locale: 'en-US',
        maintainAspectRatio: false,
        layout: {
            padding: {
                left: 10,
                right: 25,
                top: 25,
                bottom: 0
            }
        },
        scales: {
            x: {
                grid: {
                    tickColor: "rgba(255,255,255,0.1)",
                    tickLength: 10,
                    drawBorder: true,
                    borderColor: "rgba(255,255,255,0.1)",
                    color: "rgba(255,255,255,0.1)",
                },
                ticks: {
                    
                }
            },
            y: {
                grid: {
                    display: false,
                },
                ticks: {
                    display: false,
                }
            }
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: "#0b1727",
                bodyColor: "#fff",
                titleMarginBottom: 10,
                titleColor: "#fff",
                titleFont: {
                    size: 14,
                },
                borderColor: "#344050",
                borderWidth: 1,
                xPadding: 7,
                yPadding: 10,
                displayColors: false,
                intersect: false,
                mode: 'index',
                caretPadding: 10,
                callbacks: {
                    label: function (context) {
                        let label = context.dataset.label || '';

                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                        }
                        return label;
                    }
                }
            }
        }
    }

}
);
