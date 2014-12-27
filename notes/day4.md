
### Presentation vs. exploratory graphics

There are many visualisation tools available - for both python and javascript and more. A helpful conceptual distinction to make when choosing the tool for the job is between presentation and exploratory graphics. The primary purpose of a presentation graphic is to be shown to a user who did not make the graphic themselves in order to help them develop insight about the data. An exploratory graphic is, however, intended to help the person creating it insight into the data. Such graphics are typically part of a series of graphics each intended to give a different insight into one or more aspects of the data.

Considering the different objectives of these types of graphics it is natural that toolsets will develop around satistying the requirements to produce such graphics. Presentation graphics require fine grained control of each element of the graphic while exploratory graphics need to be fast and simple to make. d3 is an example of a system for presentation graphics, while ggplot is an example of a system for exploratory graphics.

### Presentation graphics with d3

[d3](http://d3js.org/) "allows you to bind arbitrary data to a Document Object Model (DOM), and then apply data-driven transformations to the document." What exaclty does this mean? The [DOM](http://www.w3.org/DOM/Overview) "is a platform- and language-neutral interface that will allow programs and scripts to dynamically access and update the content, structure and style of documents. The document can be further processed and the results of that processing can be incorporated back into the presented page." In other words it provides us a way of manipulating the HTML page in the browser from a programming language - and in this case in combination with data.

This model has facilitated the development of incredibly powerful domain specific languages (DSLs) such as d3, where the language is tailored around a set of common tasks. In this case, creating interactive HTML visualisations from data. [Here](http://bl.ocks.org/mbostock) and [here](http://www.jasondavies.com/) are some examples of what is possible.

Before we move into the visualisation a short interactive introduction to d3 is appropriate - let's use the developer console for this (in our existing web app). d3 allows you to manipulate DOM elements in a data driven way. In this session we will do exactly that: manipulate the current HTML page.

```javascript
// removing, creating, modifying html elements
d3.selectAll("svg").remove();
d3.select("body").append("p").text("Hello world");
d3.selectAll("p").attr("class", "helloClass");
d3.selectAll("p").attr("id", "helloId");
d3.select(".helloClass").style("font-size", "20px");
d3.select("#helloId").style("font-size", "10px");
d3.selectAll("p").remove();

// working with svg elements
// a base svg
var svg = d3.select("body").append("svg");
svg.attr("width", 600).attr("height", 500);
// a group element, bordered within the base svg - setting up margins for display
// we also transform the drawing space coordinates
var margin = {top: 50, bottom: 50, left: 50, right: 50};
var width = 600 - margin.left - margin.right;
var height = 500 - margin.top - margin.bottom;
var drawing = svg.append("g").attr("transform", 
    "translate(" + margin.left + "," + margin.top + ")").attr("class", "drawing-svg");
// a simple svg shape
var circle = drawing.append("circle").attr("cx", 60).attr("cy", 60).attr("r", 50);
circle.style("stroke", "blue");
circle.style("fill", "white");
circle.style("stroke-width", "5");
circle.attr("id", "circId");
// mouse-over events
circle.on("mouseover", function() {
        var id = d3.select(this).attr("id");
        d3.selectAll("#" + id).style("fill", "cyan");
    }).on("mouseout", function() {
        var id = d3.select(this).attr("id");
        d3.selectAll("#" + id).style("fill", "white");
    });
d3.selectAll("circle").remove();

// working with data (enter selections)
var data = [10, 1, 12, 14, 11, 30, 36, 10];
var circles = drawing.append("g")
    .attr("class", "circles")
    .attr("id", "circleId")
    .selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", function(i) { return i*7; })
    .attr("cy", 200)
    .attr("r", function(d) { return d; })
    .attr("stroke", "black")
    .attr("fill", "white");
```

We are going to use a new dataset that has already been prepated for visualisation. The data source is the Penn World Tables. Each country's GDP is converted into US Dollar terms (2005 constant prices) using Purchasing Power Parity weighting. The conversion to real terms allows us to see changes in volumes over time, while the conversion to USD using PPP allows for a common unit of expression. We copy the data to the app folder.

```
$ cp /vagrant/examples/dashboard/static/data.json dashboard/static
```

Our d3 heatmap code will be in `static/js/d3_graphs.js`.

```javascript
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
```

We also need to add css to our stylesheet in `static/css/styles.css`:

```css
.title {
    font-weight: bold;
}
.x-axis line {
    fill: none;
    stroke: none;
    stroke-opacity:.8;
    shape-rendering: crispEdges;
}
.x-axis path {
    stroke: white;
    fill: none;
}
.x-axis text {
    font-size: 10px;
}
.labels {
    font-size: 5px;
}
#na {
    fill: white;
}
#zero {
    fill: #6b6ecf;
}
#positive {
    fill: #393b79;
}
#negative {
    fill: #17becf;
}
```

#### Aspects of visualisation

colour
interactivity
design

### Exploratory graphics with ggplot

yhat's [ggplot](http://ggplot.yhathq.com/)
