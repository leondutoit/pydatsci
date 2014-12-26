// movie stats

var uniqueUsersDaily = function () {
    // a simple graph
    var url = "/data/unique_users/?resolution=daily";
    d3.json(url, function(data) {
        data = MG.convert.date(data, "date");
        console.log(data);
        MG.data_graphic({
            title: "Daily unique users",
            description: "#Users that watched a movie or series per day",
            data: data,
            width: 650,
            height: 400,
            target: "#metricsGraphs",
            x_accessor: "date",
            y_accessor: "values"
        });
    });
};

var drawGraphs = function() {
    uniqueUsersDaily();
}

drawGraphs();
