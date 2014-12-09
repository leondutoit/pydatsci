
### Manage and share code

We will keep the code we write throughout the workshop in version controlled git repositories on our own machines. You must, therefore, have git installed. Create a workshop folder `$ mkdir ccampus_pydatsci`. Step into that folder `$ cd ccampus_pydatsci`. This is where we will create all our files and directories.

#### git

Let's go through a basic workflow with git in our new workshop directory.

```sh
$ git init 
# let's put some files into the repo
$ touch .gitignore
$ echo "*~" >> .gitignore
$ touch README.md
$ echo "This is my ccampus_pydatsci folder" >> README.md
# what does git say about what we have done so far?
$ git status
# we need to tell git to track our files
$ git add .gitinore
$ git add README.md
$ git status
# and we need to commit our changes
$ git commit -m 'first commit: add gitignore and readme to project'
$ git status
$ git log
```

Next let's look at working with git branches.

```sh
$ git branch
$ git checkout -b exp
$ git branch
$ git log
$ touch onlyinthisbranch.txt && echo "hello there" >> onlyinthisbranch.txt
$ git add onlyinthisbranch.txt
$ git commit -m 'another random file'
$ git log
$ git checkout master 
$ git log
```

If we want the `master` branch to have the new commit from the `exp` branch we can merge the branches.

```sh
# you should be on master now
$ git merge exp master
$ git log
```

git encourages working with branches. In practice people split their development and release work into different branches. At my job, for example, develop new things on `master` and when we are sure that it functions properly, merge all the changes to a `staging` branch. After this code runs in a staging environment we merge the `staging` with the `production` branch. For the workshop though we will only use our `master` branch.

#### github

[github](https://github.com/) is a collaboration platform that uses git for source code version control. It is not the same as git. It give you the ability to remotely store your git repository, browse code, comment on code and importantly share this with others on the web. It is very widely used and I highly recommend it.

If you want, you can [add the local repo to github](https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/) but that is up to you.

### Reproducible work

Reproducibility is essential in software development, data science and science in general. If you find a bug in some code and you need help from someone to fix it then they must be able to reproduce the behaviour in order to understand what is wrong. Part of sharing code is sharing the environment in which the code runs. It is normal for programs to have dependencies in order to run and bundling these dependencies and sets of tools in virtual machine images is one way of making reproducibility easier.

#### Vagrant VM

We will use the vagrant VM as a code execution environment while all files and git repositories will be created on our own machines and accessed from the VM via shared folders. Here is a short list of the essential commands we will need:

```sh
$ vagrant --help
$ vagrant status
$ vagrant ssh # log in to the VM
$ vagrant provision # rerun the install
$ vagrant reload # rerun the box build and install
$ vagrant destroy # kill the VM
```

### Python programming

[Python](https://www.python.org/) is a dynamically typed, interpreted language. Dynamically typed languages verify the correctness of data types when the program is run. Interpreted languages are executed by interpreters - programs that read source code and translate it into python bytecode and executed by a virtual machine. The CPU on your machine executes the virtual machine's code. For a more in depth dicussion of this process have a look at [this](http://stackoverflow.com/questions/3299648/python-compilation-interpretation-process) article. 

We will use Python for the workshop since it has grown into a rich ecosystem for data intensive work. To start the python interpreter interactivey simply type `$ ipython`. We will use `ipython` which is an enhanced version of the normal python interactive interpreter.

#### Data types and basic operators

```python
# basic types
type(5)
type(5.5)
type('five')
type(False)
type(True)
type(None)

# assign values to variables
a = 5
b = 5.5
c = 'five'
d = True
e = False
f = None

# basic math
a + a
a + b # here we see the dynamic typing in action
(a + b) / a * 10
a % 2
5 / 2 # watch out for integer division

# logical operators
d == True
e != True
(d and e) == True
(d or e) == True
f is None

# strings
'f' in c
len(c)
c.capitalize()
c.endswith('b')
c.find('i')
c.replace('f', 'l')
c.split('i')
c.startswith('f')
c.upper()
c.upper().lower()

```

#### Data structures

#### Control flow

#### Functions

#### Packages

#### An example program

do something simple like read command args mangle it spit it out again

### Relational databases

#### sqlite

[sqlite](http://www.sqlite.org/), in the words of the official website, is a "software library that implements a self-contained, severless, zero-configuration, transactional SQL database engine". This makes it [different](http://www.sqlite.org/different.html) from other widely used SQL (structured query language) databases such as [PostgreSQL](http://www.postgresql.org/) and [MySQL](http://www.mysql.com/). We will use it because of its light footprint, availability and portability. What we learn from working with sqlite will easily transfer to other relational databases.

To get started open the interactive prompt in the `pydatsci/data` folder:

```sql
-- start an interactive session
-- store the db in a file for reuse later
$ sqlite3 pydatsci_people_db
-- ask for help
sqlite> .help
-- what is currently in the db?
sqlite> .databases
```

Paste all the SQL queries (delimited from each other by `;`) that follow into the sqlite prompt. Let's create a simple table and insert some values into it.

```sql
create table people(
    id integer primary key asc,
    name text,
    surname text,
    birthplace text,
    gender text,
    height real
);

insert into people(name, surname, birthplace, gender, height)
    values('Leon', 'du Toit', 'South Africa', 'male', 1.79);
insert into people(name, surname, birthplace, gender, height)
    values('Line', 'Simentad', 'Norway', 'female', 1.72);
insert into people(name, surname, birthplace, gender, height)
    values('Lars', 'Vegstein', 'Norway', 'male', 1.8);
insert into people(name, surname, birthplace, gender, height)
    values('Monica', 'Larsen', 'Norway', 'female', 1.71);

.schema people
```
We now have a `people` table with data about each person. Next we create an `events` table logging events that belong to people.

```sql
PRAGMA foreign_keys = ON;

create table events(
    id integer primary key asc,
    event_name text,
    event_time timestamp,
    person_id integer,
    foreign key(person_id) references people(id)
);

insert into events(event_name, event_time, person_id)
    values('coffee', '2014-11-06 08:01:10', 1);
insert into events(event_name, event_time, person_id)
    values('climb', '2014-11-07 17:15:01', 1);
insert into events(event_name, event_time, person_id)
    values('yoga', '2014-11-05 18:30:50', 4);
insert into events(event_name, event_time, person_id)
    values('write', '2014-11-07 06:23:10', 2);
insert into events(event_name, event_time, person_id)
    values('coffee', '2014-11-07 06:45:34', 3);
insert into events(event_name, event_time, person_id)
    values('read', '2014-11-07 17:11:11', 3);
insert into events(event_name, event_time, person_id)
    values('read', '2014-11-07 17:10:44', 4);
insert into events(event_name, event_time, person_id)
    values('coffee', '2014-11-07 10:30:03', 2);
```

Now that we have data in two related tables we can do some interesting SQL queries.

```sql
-- wildcard reference to all columns
select * from people;
select * from events;

-- named columns
select name, surname, age from people;
select event_name, event_time from events;

-- limiting printed output
select * from people limit 1;

-- sorting results
select * from people order by name desc;
select * from events order by event_time asc;

-- conditions
select * from people where name = 'Leon';
select * from people where name != 'Leon';
select * from people where name like 'L%';
select * from people where name like 'L%' and height > 1.75;
select * from people where name like 'L%' or height > 1.75;
select * from people where name not like 'L%';

-- aggregations and grouping
select birthplace, count(*) as num_people from people group by birthplace;
select gender, avg(height) as ave_height from people group by gender;
```

So far we have only operated on single tables. We can look at the two tables together using `joins`.

```sql
-- cross join
select * from people cross join events;

-- inner join
select * from people join events on people.id = events.person_id;

-- outer join
-- to make this interesting we need to add another person to the people table
insert into people(name, surname, birthplace, gender, height)
    values('Niel', 'Bekker', 'South Africa', 'male', 1.82);
select * from people left outer join events on people.id = events.person_id;
```

Sometimes you need to compute metrics that will not be readable or possible with a single query. Typically one uses a subquery to produce a first result set and then an outer query to operate on the first set. Here is a simple example:

```sql
-- per person, per date, number of events
select 
    a.name as name,
    date(a.event_time) as et,
    count(*) 
from (select * from people left outer join events on people.id = events.person_id)a
group by 
    name,
    et
order by et;

-- we can close the db now
.exit 
```

We have now seen some of the essential features of SQL and sqlite but the data we manufactured was not very interesting. A more realistic scenario would be one where we have a data file that we want to analyse. We will use the data in the repo located in the `data/movies.csv` file.

```sh
# first we create a new db file
$ sqlite3 moviedb
```

```sql
-- then we load the file into a table
.separator ','
create table movies(
    event_date timestamp,
    userid text, 
    contentid text, 
    device text, 
    market text, 
    totalminuteswatched integer, 
    runningtime integer, 
    viewpercentage real, 
    errorperception real, 
    sessiontype text, 
    title text, 
    seasonnumber integer, 
    episodenumber integer
);
.import movies.csv movies
select * from movies limit 10;
```

Now that we have the csv file in a table we can use SQL to answer some interesting questions.

```sql
-- how many unique users watched something per day?
-- what was the average amount of things they watched?
-- and what was the average daily errorperception?
select
    date(event_date) as day,
    count(distinct userid) as num_users,
    count(contentid) * 1.0 / count(distinct userid) as ave_watched,
    avg(errorperception) as ave_err_percep
from movies
group by day;
```

Our tour of SQL would not be complete withtout a discussion of [indexing](https://www.sqlite.org/lang_createindex.html). SQL is a declarative query language. Unlike imperative languages, like Python, where the programmer tells the machine which operations to perform a declarative language allows the programmer to say what they would like computed for them. It is the task of the system to figure out how to compute that. In sqlite this is the task of the [query planner](https://www.sqlite.org/queryplanner.html). 

When you are working with large tables (several millions of rows) and when you know your data well it makes sense to create indexes. Indexes are essentially sorted lists of the unique values in your column. When an index exists on a column the query planner will, in some circumstances, use the index to find the values you are looking for. This can be much faster than doing the same thing without and index.

Let's create some useful indexes on the movies table.

```sql
-- the names are arbitrary but using idx is a convention
create index userid_idx on movies(userid);
create index event_date_idx on movies(event_date);
.schema movies
```

Since counting unique users and filtering results by date range are two very common operations on a table like this it is likely that there indexes will serve us well.

#### Further reading



