(function(){

    var margin = {top: 70, bottom: 30, left: 100, right: 50},
        width = 900 - margin.left - margin.right,
        height = 450 - margin.top - margin.bottom;

    var svg = d3.select("body").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .attr("class", "base-svg");

    var parseDate = d3.time.format("%Y").parse;
    var xScale = d3.time.scale().range([0, width]);
    var yScale = d3.scale.ordinal().rangeRoundBands([0, height], 1, 0);

    var graphSvg = svg.append("g")
                .attr("transform",
                        "translate(" + margin.left + "," + margin.top + ")")
                .attr("class", "bar-svg");

    var x = graphSvg.append("g")
            .attr("class", "x-axis");

    var dataUrl = "static/data.json";

    d3.json(dataUrl, function(data) {

        data.daterange.forEach(function(d) {
            d = parseDate(d);
        });

        xScale.domain(d3.extent(data.daterange, function(d) { return parseDate(d); }));
        yScale.domain(data.data.map(function(d) { return d.id; }));

        d3.select(".base-svg").append("text")
            .attr("x", margin.left)
            .attr("y", (margin.top)/2)
            .attr("text-anchor", "start")
            .text("Real per person GDP growth in the world (PPP): 1960 to 2011")
            .attr("class", "title");

        var labels = graphSvg.append("g").attr("class", "labels")
                        .selectAll("text")
                        .data(data.data)
                        .enter()
                        .append("text")
                        .attr("x", "0")
                        .attr("y", function(d) { return yScale(d.id); })
                        .text(function(d) { return d.id; })
                        .attr("text-anchor", "end")
                        .attr("dx", "-.32em")
                        .attr("dy", "1.2em")
                        .attr("id", function(d) { return d.id; });

        data.data.forEach(function(activity) {

            individualEconomy = activity[activity.id];

            graphSvg.append("g")
                .attr("class", function(d) { return activity.id; })
                .selectAll("rect")
                .data(individualEconomy)
                .enter()
                .append("rect")
                .attr("x", function(d,i) { return xScale(parseDate(data.daterange[i])); })
                .attr("y", function() { return yScale(activity.id)})
                .attr("fill", "white")
                .attr("width", width/individualEconomy.length)
                .attr("height", height/individualEconomy.length)
                .attr("class", function() { return activity.id; })
                .attr("id", function(d) {
                    if (d < 0) {
                        return "negative";
                    } else if (d === 0) {
                        return "zero";
                    } else if (d > 0) {
                        return "positive";
                    }
                });
        });

        var xAxis = d3.svg.axis().scale(xScale)
                .orient("top")
                .tickSize((-height))
                .ticks(numTicks);

        x.call(xAxis);

        var numTicks = data.daterange.length;
        var grid = xScale.ticks(numTicks);

        graphSvg.append("g").attr("class", "grid")
            .selectAll("line")
            .data(grid, function(d) { return d; })
            .enter().append("line")
                .attr("y1", 0)
                .attr("y2", height + margin.bottom)
                .attr("x1", function(d) { return xScale(d); })
                .attr("x2", function(d) { return xScale(d); })
                .attr("stroke", "white");

        labels.on("mouseover", function() {
            var country = d3.select(this).attr("id");
            d3.selectAll("#" + country).style("font-size", "12px");
            d3.selectAll("." + country).attr("stroke", "white");
        }).on("mouseout", function() {
            var country = d3.select(this).attr("id");
            d3.selectAll("#" + country).style("font-size", "5px");
            d3.selectAll("." + country).attr("stroke", "none");
        });

    });

})();
