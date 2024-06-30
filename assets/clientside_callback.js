if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.clientside = {
    update_graph: function(fromMonth, toMonth, data) {
        // Filter data based on selected months
        var filteredData = data.filter(function(row) {
            return row.Month >= fromMonth && row.Month <= toMonth;
        });

        // Group by HourOfDay and sum the 'Value'
        var hourlySumData = {};
        filteredData.forEach(function(row) {
            if (!(row.HourOfDay in hourlySumData)) {
                hourlySumData[row.HourOfDay] = 0;
            }
            hourlySumData[row.HourOfDay] += row.Value;
        });

        var xValues = Object.keys(hourlySumData);
        var yValues = Object.values(hourlySumData);

        var monthDict = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        };

        return {
            data: [{
                x: xValues,
                y: yValues,
                type: 'bar',
                name: 'Hourly Sum'
            }],
            layout: {
                title: 'Sum of Value Over Hour of the Day (' + monthDict[fromMonth] + ' to ' + monthDict[toMonth] + ')',
                xaxis: {title: 'Hour of the Day'},
                yaxis: {title: 'Sum of Value'}
            }
        };
    }
};