$(document).ready( function () {
    let dt = $('#census_table').DataTable({
        processing: true,
        serverSide: true,
        ordering: false,
        bFilter: false,
        ajax: {
            url: "/load_census",
            dataSrc: "data"
        },
        columns: [
            { data: 'id', visible: false },
            { data: 'age' },
            { data: 'workclass' },
            { data: 'education_level' },
            { data: 'education_num', visible: false },
            { data: 'marital_status' },
            { data: 'occupation' },
            { data: 'relationship' },
            { data: 'race' },
            { data: 'sex' },
            { data: 'capital_gain' },
            { data: 'capital_loss' },
            { data: 'hours_week' },
            { data: 'country' },
            { data: 'over_50k' },
        ]
        
    });

    $.ajax({
        url: '/get_work_hours',
        success: function(data){
            renderWorkChart(data);
        }
    })

    $.ajax({
        url: '/get_pop_distr',
        success: function(data){
            renderPopChart(data);
        }
    })
} );

function renderWorkChart(data){
    Highcharts.chart('workChart', {
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Average Hours Worked by Age'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            title: {
                text: 'Age'
            }
        },
        yAxis: {
            title: {
                text: 'Hours Worked'
            },
            min: 0
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x} y/o: {point.y:.2f} hrs/wk'
        },

        plotOptions: {
            series: {
                marker: {
                    enabled: true,
                    radius: 2.5
                }
            }
        },

        colors: ['#6CF', '#39F', '#06C', '#036', '#000'],

        // Define the data points. All series have a year of 1970/71 in order
        // to be compared on the same x axis. Note that in JavaScript, months start
        // at 0 for January, 1 for February etc.
        series: [
            {
                name: "Immigrant Hours",
                data: data.immigrant_hours
            }, {
                name: "Non-Immigrant Hours",
                data: data.non_immigrant_hours
            }
        ]
    });
}

function renderPopChart(data){
    Highcharts.chart('popChart', {
        chart: {
            type: 'spline',
            zooming:{
                type: 'x'
            }
        },
        title: {
            text: 'Population distribution by age'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            title: {
                text: 'Age'
            },
            type: 'logarithmic',
        },
        yAxis: {
            title: {
                text: 'Population Size'
            },
            min: 0
        },
        tooltip: {
            headerFormat: '<b>{series.name}</b><br>',
            pointFormat: '{point.x} y/o: {point.y:.2f} individuals'
        },

        plotOptions: {
            series: {
                marker: {
                    enabled: true,
                    radius: 2.5
                }
            }
        },

        colors: ['#6CF', '#39F', '#06C', '#036', '#000'],

        // Define the data points. All series have a year of 1970/71 in order
        // to be compared on the same x axis. Note that in JavaScript, months start
        // at 0 for January, 1 for February etc.
        series: [
            {
                name: "Immigrant Population",
                data: data.immigrant_pop
            }, {
                name: "Non-Immigrant Population",
                data: data.non_immigrant_pop
            }
        ]
    });
}
