// movie stats

var uniqueUsersDaily = function () {
    // a simple graph
    var url = "/data/unique_users/?resolution=daily";
    d3.json(url, function(data) {
        data = MG.convert.date(data, "date");
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

// we assume we want to display one graph at a time
// for a given URL with a specific metric name and resolution

var graphSpecs = {
    unique_users: {
        title: "Unique users",
        description: "The unique number of users per period"
    },
    minutes_watched: {
        title: "Total minutes watched",
        description: "The total minutes streamed (movies and series) per period"
    }
};

$.urlParam = function(name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results === null) {
       return null;
    } else {
       return results[1] || 0;
    }
};

var buildUrl = function() {
    var metric = $.urlParam("metric");
    var resolution = $.urlParam("resolution");
    var url = "".concat("/data/", metric, "/?resolution=", resolution);
    return url;
}

var createGraph = function(url, spec) {
    d3.json(url, function(data) {
        data = MG.convert.date(data, "date");
        MG.data_graphic({
            title: spec.title,
            description: spec.description,
            data: data,
            width: 650,
            height: 400,
            target: "#metricsGraphs",
            x_accessor: "date",
            y_accessor: "values"
        });
    });
};

var renderGraphs = function() {
    var url = buildUrl();
    var metric = $.urlParam("metric");
    createGraph(url, graphSpecs[metric]);
};

renderGraphs();
