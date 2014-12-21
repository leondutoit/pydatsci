
### Handling errors

#### Exception handling

Suppose we have a function, like before, that tests whether a number is even or not.

```python
def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False

is_even(8)
is_even(1.1)
is_even('not a number...')
```

If the function is passed a string as a parameter it cannot perform the logic we intend it to - the function throws an exception: `TypeError: not all arguments converted during string formatting`. Functions often receive inputs from sources that are beyond our control and we need to decide what to do when errors arise from bad input data. Is it alright to simply notify the runner of the program that something failed and then continue? Should the program halt? In python such decisions are made by handling exceptions. How we handle them depends on the case.

Let's consider a simple use case: the program gets a list of data, that can contain integers and strings, and we are interested in whether the integers are even or odd. We need to decide how to respond when getting a string.

```python
input_data = [1, 2, 3, 4, 5, 'hello', 10, '...', 8]

def is_even2(num):
    try:
        if num % 2 == 0:
            return True
        else:
            return False
    except TypeError:
        print "Found non-numerical input, returning None"
        return None

map(is_even2, input_data)
```

In this case we get a list containing `True`, `False` or `None` and a notification that a non-numeric input was found. Instead of the program exiting with an error we specify how we want to handle the specific error and continue accordingly. We will see more of this throughout.

#### Unit testing

In the example python program covered on day 1 we read command line arguments into a list, inserted spaces between words, added an exclamation mark before printing a string to the console. Part of making robust software is writing tests to make sure functions and larger unit of code operate as expected. We can write simple unit tests for the functions in the example program and run them with `nosetests`.

```python
from make_a_sentence import make_annoying_sentence, exclaim

def test_make_annoying_sentence():
    """Test that words are converted to upper case and that spaces are inserted"""
    sample_words = ['hello', 'there']
    sentence = make_annoying_sentence(sample_words)
    correct_sentence = ['HELLO', ' ', 'THERE', ' ']
    assert(sentence == correct_sentence) 

def test_exclaim():
    """Test that an exclamation mark is added to a sentence"""
    with_exclamation = exclaim(['BLA'])
    assert('!' in with_exclamation)
```

We can run this as follows: `cd pydatsci/examples && nosetests`. These are overly simplistic tests and not complete enough, but they illustrate the point well enough.

### Data manipulation with pandas

We will do the work in the `data` directory: `cd pydatsci/data`. You should have the `moviedb` file from day1 in that directory.

```python
import pandas as pd

# Series
s = pd.Series(range(10))
s
s.dtype
s.index
s.values
s.shape

# DataFrame ~ a Series of Series
df = pd.DataFrame({
    'a': ['x' if i % 2 == 0 else 'y' for i in range(10)], 
    'b': [i*i for i in range(10)]})
df
df.dtypes
df.index
df.values
df.shape
df.columns

# slicing and basic manipulation
df['a']
df['a'][0]
type(df['a'][0])
df['a'][df['a'] == 'x']
df['b'][df['a'] == 'x']
df['c'] = df['b']*2
df
```

Read and writing files with pandas is very easy and efficient compared to using plain Python.

```python
movies = pd.read_csv('movies.csv', header = None)
movies.head()

# remove any row with NaN value
cleaned_movies = movies.dropna()
cleaned_movies.to_csv('cleaned_movies.csv', quote = False, index = False, header = False)
```

We can also interact directly with the sqlite movies database that we made previously.

```python
import sqlite3
conn = sqlite3.connect('moviedb')
movie_db = pd.read_sql('select * from movies limit 10', conn)
movie_db.head()
conn.close()
```

DataFrames have a host of methods that makes common tabular data manipulation easy to do.

```python
# DF methods - single column operations
df['b'].cumsum()
df['b'].mean()
df['b'].median()
df['b'].min()
df['b'].max()

# groupby and aggregation - multiple column operations
gdf = df.groupby('a')
gdf
gdf.groups
gdf.sum()
gdf.mean()
gdf.median()
gdf.count()

def f(a):
    """return the cumulative sum only if numbers are even"""
    return reduce(lambda x, y: (x + y) if (x % 2 == 0 and y % 2 == 0) else 0, a)

gdf.aggregate(f)

# merge - multiple DataFrames
df2 = pd.DataFrame({
    'a': ['y' if i % 2 == 0 else 'x' for i in range(10)], 
    'c': [i+i for i in range(10)]})

pd.merge(df, df2, on = 'a')

# pivot tables - changing shape
mdf = pd.DataFrame({
    'sessiontype': ['MOVIE', 'SERIES', 'SERIES', 'MOVIE'],
    'title': ['x-men', 'game of thrones', 'game of thrones', 'iron man'],
    'totalminuteswatched': [10, 4, 40, 90]})

mdf
mdf.pivot_table(values = 'totalminuteswatched', index = ['sessiontype', 'title'], aggfunc = sum)
```

Now we can use pandas to create a set of analysis tools for the movie database. We will answer the following questions:
* How many unique users per period (day, week, month)
* Total minutes watched per period
* Rank content by popularity to display top 10

We need to organise our code into a project that will become the interactive dashboard. Create a directory structure as follows:

```
dashboard/
    |
    - moviedb
    - app.py
    - analysis_tools.py
    - static/
        |
        css/
        |
        js/
    - templates/
        |
        - index.html
```

Suppose you're in the vagrant VM in your home folder, then you can create the structure like this:

```sh
$ mkdir -p dashboard/static/css dashboard/static/js dashboard/templates
$ touch dashboard/app.py dashboard/analysis_tools.py dashboard/templates/index.html
$ cp /vagrant/data/moviedb dashboard
```

We will create the code in there as we go along. Now  use the `analysis_tools.py` file to create these functions as we go along.

```python
import sqlite3
import pandas as pd
import datetime as dt

conn = sqlite3.connect('moviedb')
movie_db = pd.read_sql('select * from movies', conn)
movie_db.head()
conn.close()

# reindex for groupby purposes
movie_db.index = pd.DatetimeIndex(movie_db.event_date)

# fancy slicing capabilities
movie_db['2013-03-15']

def get_data_from_db(conn):
    data = pd.read_sql('select * from movies', conn)
    data.index = pd.DatetimeIndex(movie_db.event_date)
    return data

def date_resolution(resolution):
    def md(y, m, d):
        return dt.datetime(y, m, d)
    funcs = {
        'daily': lambda x: md(x.year, x.month, x.day).strftime('%Y-%m-%d'),
        'weekly': lambda x: (md(x.year, x.month, x.day) - dt.timedelta(days = x.weekday())).strftime('%Y-%m-%d'),
        'monthly': lambda x: md(x.year, x.month, 1).strftime('%Y-%m-%d')
    }
    return funcs[resolution]

movie_db.groupby(date_resolution('daily'))['totalminuteswatched'].sum()

def metric_by_date(df, resolution, column, agg_func):
    grouped = df.groupby(date_resolution(resolution))[column]
    ans = grouped.apply(agg_func)
    return ans

def unique_users(df, resolution):
    return metric_by_date(df, resolution, 'userid', lambda x: len(x.value_counts()))

def minutes_watched(df, resolution):
    return metric_by_date(df, resolution, 'totalminuteswatched', sum)

# question no. 1
unique_users(movie_db, 'monthly')

# question no. 2
minutes_watched(movie_db, 'daily')

# for unique users and minutes watched there are days with no data
# one those days the value of the metrics should be zero
# to take this into account we can reindex and fill missing values
def add_zeros_for_missing_dates(df, resolution):
    freq_map = {
        'daily': 'D',
        'weekly': 'W-MON',
        'monthly': 'MS'
    }
    freq = freq_map[resolution]
    start = df.index[0]
    end =  df.index[len(df.index) - 1]
    idx = pd.date_range(start, end, freq = freq)
    format_date = lambda x: x.strftime('%Y-%m-%d')
    df = df.reindex(map(format_date, idx.to_pydatetime()), fill_value = 0)
    return df

# then if we need to we can call it like this
weekly_users = unique_users(movie_db, 'weekly')
add_zeros_for_missing_dates(weekly_users, 'weekly')

def rank_titles(df, num):
    toplist = movie_db.groupby('title')['title'].count()
    toplist.sort(ascending = False)
    return toplist[toplist.index != ''][:num]

# question no. 3
rank_title(movie_db, 10)
```

As is clear from the short analysis above, working with dates is hard. We will use these analysis tools later to display data in our interactive dashboard. We can clean up the file by removing all the function calls or just commenting them out so that we're left only with the function definitions - these will be called from the web app eventually.

### A Flask web app

A Hello World Flask app (also visible in `examples/flask_hello_world.py`):

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run(port = 9009, debug = True)
```

We can run this as follows: `$ python flask_hello_world.py` and browse to `localhost:9009` in our browser. The `@app.route("/")` is an annotation - a flask specific construct. In general an annotation modifies the behaviour of the function it annotates. Annotations are built-in language constructs. In this case it simply means that the `hello` function should be called when the browser makes a HTTP request to the app at the root URL `/`. In subsequent web app development we will make more use of custom URLs to control which functions are executed.


#### Talking to the db

Eventually we want to use our analysis tools to get data from the db, do data manipulation and visualise the results from the flask app. To do this we need a way to connect to the database from the web app. Put this into the `app.py` file.

```python
import sqlite3
import pandas as pd
from flask import Flask, g, Response
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

@app.route("/")
def hello():
    db = get_db()
    res = pd.read_sql('select * from movies limit 10', db)
    return Response(res.to_json(), mimetype = 'application/json')

if __name__ == '__main__':
    app.run(port = 9009, debug = True)
```

There are a few new things to notice here: the `get_db` and the `close_connection` functions are new, and there are a couple of details in the `hello` function.

The `get_db` function creates a database connection and stores it on a special flask object that is available during [HTTP](http://code.tutsplus.com/tutorials/http-the-protocol-every-web-developer-must-know-part-1--net-31177) (Hypertext Tranfer Protocol) requests. The functions annotated with the `@route` decorator are called from HTTP requests. This means that the `g` object is available to the `hello` function. `get_db` works in tandem with `close_connection` which is annotated with `@app.teardown_appcontext`: this is called when a request is done. So in the `hello` function, after all the work related to the db is done, the `close_connection` function is called to close the connection to the database.

Inside the `hello` function we use the db connection to read a SQL result set into a pandas DataFrame. The function returns a flask `Response` object. This object maps to a HTTP response which the browser will receive in our case. The HTTP resonse has data (the SQL result set) and it has another attribute called the `mimetype`. The `mimetype` aka [Internet Media Type](http://en.wikipedia.org/wiki/Internet_media_type) is just an identifier which will let the browser know what kind of data it is receiving. We do two things here: we use the pandas `to_json` function to change the data from a DataFrame into JSON (JavaScript Object Notation) and we set the mimetype to `application/json` to let the browser know what kind of data we are returning.

The next step is to include the analysis tools into the web app and to build visualisations on top of those. We will do this in the next session.
