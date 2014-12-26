
### Flask, the db and analysis

To use our analysis tools from the web to deliver data to the browser (for visualisation) we extend the `dashboard/app.py` file.

```python
import sqlite3
import pandas as pd
# we add a new imports from flask
from flask import Flask, g, Response, render_template, request
# and we import the analysis tools
from analysis_tools import (get_data_from_db, date_resolution,
    metric_by_date, unique_users, minutes_watched,
    add_zeros_for_missing_dates, rank_titles)
app = Flask(__name__)

DATABASE = 'moviedb'

def connect_to_database():
    conn = sqlite3.connect(DATABASE)
    return conn

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# new code

def json_resp(df, format = "ts"):
    if format == "ts":
        df = pd.DataFrame({
            'date': df.index,
            'values': df.values})
    else:
        df = pd.DataFrame({
            'title': df.index,
            'values': df.values})
    return Response(
        df.to_json(orient = 'records'),
        mimetype = 'application/json')

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/data/<ts_metric>/")
def get_metric(ts_metric):
    res = request.args.get("resolution")
    db = get_db()
    df = get_data_from_db(db)
    if ts_metric == "unique_users":
        df = unique_users(df, res)
    elif ts_metric == "minutes_watched":
        df = minutes_watched(df, res)
    df = add_zeros_for_missing_dates(df, res)
    return json_resp(df)

@app.route("/data/toplist/")
def get_toplist():
    num = int(request.args.get("num"))
    db = get_db()
    df = get_data_from_db(db)
    top = rank_titles(df, num)
    return json_resp(top, format = "rank")

if __name__ == '__main__':
    app.run(port = 9009, debug = True)
```

`json_resp` takes a dataframe and a format specification and constructs an appropriate JSON HTTP response. `hello` now renders an html page. `get_metric` takes a string from the URL combined with a URL parameter to return either unique users or total minutes watched per period. Lastly `get_toplist` uses a URL parameter to display the top `n` popular titles. We can, therefore, get data from the following URLs:

```
/data/unique_users/?resolution=daily
/data/unique_users/?resolution=weekly
/data/unique_users/?resolution=monthly

/data/minutes_watched/?resolution=daily
/data/minutes_watched/?resolution=weekly
/data/minutes_watched/?resolution=monthly

/data/toplist/?num=10
```

We will use these URLs from the JavaScript code to get data for visualisation.

### Javascript

[Javascript](http://en.wikipedia.org/wiki/JavaScript) is a dynamic language used by web browsers to create dynamic web pages. The browser has a JS runtime which executes the code sent to you by the website. We will use the browser's developer tools as an interactive prompt to evaluate the JavaScript in this section. Open the developer console.

```javascript
/* this is a comment
that spans multiple lines */

// this is a single line comment

// basic data types
var num = 9;
typeof(num);
var st = "hello";
typeof(st);
var n = null;
typeof(n);
typeof(true);
typeof(false);
var d = new Date();
typeof(d);

// operators and logic
// stricy comparison (no type conversion)
num === 9; 
num !== 10;
num == 9;
num != 10;
num == "9";
num > 5 && num < 10;
num < 5 || num === 9;
!(num === 9);
((((num * 9) / 10.0) + 10) - 1) % 2;

// data structures, methods, anonymous functions
// arrays
var a = [4, 5, 6, 10];
a[0];
a.map(function(input) { return input*input; });
a.forEach(function(input) { console.log(input); });
a.filter(function(input) {if (input % 2 === 0) return input; });

// object literals
var ob = { k: 100 };
ob;
ob.k;

// arrays of objects - a common pattern
var data = [
    {
        name: "title1",
        value: 100
    }, 
    {
        name: "title2",
        value: 11
    }, 
    {
        name: "title3",
        value: 136
    }
];
data;
data[0].name;
data[0].value;

// use array method to access data in objects
data.forEach(function(d) {
        var announcement = d.name + " received " + d.value + " views.";
        console.log(announcement);
    }
);

// control flow
for (var i = 0; i < a.length; i++) {
    var currentNum = a[i];
    if (currentNum % 2 === 0) {
        console.log(a[i]);    
    } else {
        console.log("uneven number found");
    }
}

var cond = true;
while (cond) {
    console.log("the condition is " + cond);
    cond = false;
}

// functions
var sayHello = function() {
    console.log("Hello");
};
sayHello();

var saySomething = function(thing) {
    var message = "I am saying: " + thing;
    console.log(message);
};
saySomething();

var average = function(nums) {
    var amount = nums.length;
    var total = 0;
    for (var i = 0; i < amount; i++) {
        total += nums[i];
    }
    return total / amount;
};
average([1, 2, 4, 5, 99, 10, 1]);

var doSomethingAndThenAverage = function(nums, todo) {
    var outcome = todo(nums);
    return average(outcome);
};

var onlyEven = function(nums) {
    var evens = nums.filter(function(n) { if (n % 2 === 0) return n; });
    return evens;
};

doSomethingAndThenAverage([99, 88, 6, 3, 1, 3, 2, 46], onlyEven);

// immediately invoked function expressions
// here we can create many new objects which will be destroyed
// when the function expression is done being invoked
// this is useful, for example, if you want to return only one thing
// or make changes to a display without returning anything
// it is a way to keep data private and to group relevant code together
(function() {
    var myObj = {
        metaData: "How many kilometers traveled per day",
        data: [10, 100, 20, 1, 11, 88]
    };
    var kms = myObj.data;
    var totalKms = kms.reduce(function(a, b) { return a + b; });
    console.log(totalKms);
})();

// the object we created are not there anymore
myObj;
kms;
totalKms;
```

We will use the JavaScript concepts and techniques introduced in this section to build an interactive dashboard with our web app.

### JSON

```javascript
ex = JSON.parse("{\"key\": 10}");

```

### A dashboard

#### More flask setup

#### Visualisation with metricsgraphics

visualise the analysis

TODO - make sure JSON format works

http://metricsgraphicsjs.org/


#### d3

lower levels...
