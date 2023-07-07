Chart.defaults.global.defaultFontSize = 18;
Chart.defaults.global.defaultFontFamily = 'Tanha';

const ri_prog = $("#rial_progress");

const visit = new Chart(ri_prog, {
    type: "line",
    data: {
        labels: [
            "شنبه",
            "یک‌شنبه",
            "دوشنبه",
            "سه‌شنبه",
            "چهارشنبه",
            "پنج‌شنبه",
            "جمعه",
        ],

        datasets: [
            {
                data: [15000, 14700, 16500, 15600, 14700, 15000, 14000],
                backgroundColor: "",
                borderColor: "#17a2b8",
                pointBackgroundColor: "#17a2b8",
            },
            {
                data: [14000, 15700, 13500, 14600, 16700, 15200, 12500],
                backgroundColor: "",
                borderColor: "#ffc107",
                pointBackgroundColor: "#ffc107",
            },
        ],
    },
    options: {
        scales: {
            yAxes: [
                {
                    display: true,
                },
            ],
            xAxes: [
                {
                    display: true,
                },
            ],
        },
        legend: {
            display: false,
        },
        layout: {
            padding: {
                left: 5,
                right: 5,
                top: 5,
                bottom: 5,
            },
        },
    },
});

// ----------------------------------------

var tem_prog = $("#temporal_progress");
var myChart = new Chart(tem_prog, {
    type: 'bar',
    data: {
        labels: [
            "فروردین",
            "اردیبهشت",
            "خرداد",
            "تیر",
            "مرداد",
            "شهریور",
        ],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 8, 5, 14, 7],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [
                {
                    display: true,
                },
            ],
            xAxes: [
                {
                    display: true,
                },
            ],
        },
        legend: {
            display: false,
        },
        layout: {
            padding: {
                left: 5,
                right: 5,
                top: 5,
                bottom: 5,
            },
        },
    },
});
