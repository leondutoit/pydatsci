
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
var data = [10, 9, 12, 14, 11, 30, 36, 10];
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
$ cp examples/dashboard/static/data.json cc_dashboard/static
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

#### Colour

Good visualisation systems provide helper functions and sensilbe defaults for choosing colours. d3 provides access to the colour designs and specifications develpoed by Cynthia Brewer in the form of an internal object [mapping](https://github.com/mbostock/d3/tree/master/lib/colorbrewer). Her [website](http://colorbrewer2.org/) is a great guide to choosing colour schemes that work well. In d3 you can choose from colour [palletes](https://github.com/mbostock/d3/wiki/Ordinal-Scales#categorical-colors) for ordinal scales or using colour space [functions](https://github.com/mbostock/d3/wiki/Colors).

Another important point is to avoid red-green colour combinations - about 6% of the male population is colourblind. If you use such combinations you risk losing the communicative power of your visualisation.

For more detailed and an excellent discussion of colour choice in statistical graphics read [Escaping RGBland](http://statmath.wu.ac.at/~zeileis/papers/Zeileis+Hornik+Murrell-2009.pdf).

### Exploratory graphics with ggplot

For exploratory graphics we will use [ggplot](http://ggplot.yhathq.com/) - a port of the [R](http://www.r-project.org/) language's [ggplot2](http://ggplot2.org/) and an implementation of the [Grammar of Graphics](http://www.amazon.com/The-Grammar-Graphics-Statistics-Computing/dp/0387245448). The central idea underpinning the Grammar of Graphics is that the user creates a statistical graphic by specifying what they want to see - they describe the graphic with a grammar and the system uses the rules of the grammar to figure out how the description should be translated into data transformations and visualisations. Instead of, therefore, saying in detail what to draw (as we did with d3) we will use higher level concepts to describe what we want to see.

#### ggplot

We should be in the `dashboard` directory - we will use the `moviedb` data in combination with `analysis_tools.py`.

```python
import sqlite3
import pandas as pd
from ggplot import *
from analysis_tools import *

conn = sqlite3.connect("moviedb")
# remove some numeric rows with null values - implifies visualisation code
query = "select * from movies where viewpercentage != ''"
mvdata = pd.read_sql(query, conn)
mvdata.index = pd.DatetimeIndex(mvdata.event_date)
conn.close()

def as_df(series):
    return pd.DataFrame({
        "date": series.index.to_datetime(),
        "values": series.values})

users = as_df(unique_users(mvdata, "daily"))
mins = as_df(minutes_watched(mvdata, "weekly"))

# we add geometries as layers to base objects based on data
ggplot(aes(x = "date", y = "values"), data = users) + geom_line()
ggplot(aes(x = "date", y = "values"), data = mins) + geom_point() + stat_smooth()

# a common task is to compare a metric to a benchmark
ggplot(aes(x = "date", y = "values"), data = users) + \
    geom_line() + geom_hline(yintercept = [10], colour = "red")

# the dispertion of session length
ggplot(aes(x = "totalminuteswatched"), data = mvdata) + geom_histogram()

# session length dispertion by session type (movies/series)
ggplot(aes(x = "totalminuteswatched", fill = "sessiontype"), data = mvdata) + \
    geom_density(alpha = 0.25)

# role of device in session length along with type
ggplot(aes(x = "totalminuteswatched", fill = "sessiontype"), data = mvdata) + \
    geom_density(alpha = 0.25) + facet_wrap("device")

# which device lends itself more to finishing a session
ggplot(aes(x = "viewpercentage"), data = mvdata) + geom_histogram() + \
    facet_wrap("device")

# remove crazy viewpercentage > 100%
mvclean = mvdata[mvdata.viewpercentage < 100]

ggplot(aes(x = "viewpercentage"), data = mvclean) + \
    geom_histogram() + facet_wrap("device")

# perhaps a relation between content duration and finishing a session
ggplot(aes(x = "runningtime", y = "viewpercentage"), data = mvclean) + geom_point()

# let's remove very short sessions - call them sample peeks
# we also use a technique called jittering to make the points more visible
ggplot(
    aes(x = "runningtime", y = "viewpercentage"),
    data = mvclean[mvclean.viewpercentage > 20]) + \
        geom_point() + geom_jitter() + stat_smooth(colour = "blue")

# polish this last graph a bit
ggplot(
    aes(x = "runningtime", y = "viewpercentage"),
    data = mvclean[mvclean.viewpercentage > 20]) + \
        geom_point() + geom_jitter() + stat_smooth(colour = "blue") + \
        ggtitle("Relation between running time and view percentage") + \
        ylab("% of content viewed") + xlab("Content running time")
```

ggplot provides plotting facilities at a much higher level than d3. It also makes many decisions for you - which is a good thing if they are made well and if the constraints imposed by them match your use case. If your use case is exploratory graphics, to learn about your data with a rapid succession of statistical graphics then it is a very good fit. It will also suffice for many presentation purposes, even if they will not be very fancy.

For some the Grammar of Graphics approach does not work - perhaps the syntax is too terse or perhaps you are already familiar with another approach that works for you. That is obviously fine :) Another python visualisation library focused on data analysis and exploration that is well worth a look is [seaborn](http://stanford.edu/~mwaskom/software/seaborn/index.html). It is also a safe bet to be conversant with more than one graphical library since you will invariably run into limitations as your needs to visualise your data grow.

Other interesting projects are [bokeh](http://bokeh.pydata.org/) and [vincent](https://vincent.readthedocs.org/en/latest/quickstart.html). Both focus on creating visualisations for the web from python.
