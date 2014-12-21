
import pandas as pd
import datetime as dt

def get_data_from_db(conn):
    data = pd.read_sql('select * from movies', conn)
    data.index = pd.DatetimeIndex(data.event_date)
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

def metric_by_date(df, resolution, column, agg_func):
    grouped = df.groupby(date_resolution(resolution))[column]
    ans = grouped.apply(agg_func)
    return ans

def unique_users(df, resolution):
    return metric_by_date(df, resolution, 'userid', lambda x: len(x.value_counts()))

def minutes_watched(df, resolution):
    return metric_by_date(df, resolution, 'totalminuteswatched', sum)

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

def rank_titles(df, num):
    toplist = df.groupby('title')['title'].count()
    toplist.sort(ascending = False)
    return toplist[toplist.index != ''][:num]
