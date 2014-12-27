
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

