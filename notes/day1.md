
We will use the vagrant VM as a code execution environment while all files and git repositories will be created on our own machines and accessed from the VM via shared folders.

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
$ git checkout experimental
$ git branch
$ git log
# add commits, cherry pick, add another branch and merge it...
```

#### github

More about github...

If you want, you can [add the local repo to github](https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/) but that is up to you. Here is how you can do it:

```sh
# do it...
```

### Reproducible work

#### Vagrant VM

```sh
$ vagrant --help
# and more
```

### Python programming

Official [website](https://www.python.org/).
Language info, repl etc

#### Data types

#### Data structures

#### Functions

#### Packages

#### An example program

do something simple like read command args mangle it spit it out again

### Relational databases

#### sqlite

[sqlite](http://www.sqlite.org/), in the words of the official website, is a "software library that implements a self-contained, severless, zero-configuration, transactional SQL database engine". This makes it [different](http://www.sqlite.org/different.html) from other widely used SQL (structured query language) databases such as [PostgreSQL](LINKME) and [MySQL](LINKME). We will use it because of its light footprint, availability and portability. What we learn from working with sqlite will easily transfer to other relational databases.

To get started open the interactive prompt:

```sql
-- start an interactive session
$ sqlite3
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
-- cross joins
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
```

We have now seen some of the essential features of SQL and sqlite but the data we manufactured was not very interesting. A more realistic scenario would be one where we have a data file that we want to analyse. We will use the data in the repo located in the `data/WHATDATATOGETHMMMM.csv` file.

```sql
-- import file into db and do the things
```

#### Further reading



