
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


### Relational databases

#### sqlite

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

create table events2(
    id integer primary key asc,
    event_name text,
    event_time timestamp,
    person_id integer,
    foreign key(person_id) references people(id)
);

insert into events2(event_name, event_time, person_id)
    values('coffee', '2014-11-06 08:01:10', 1);
insert into events2(event_name, event_time, person_id)
    values('climb', '2014-11-07 17:15:01', 1);
insert into events2(event_name, event_time, person_id)
    values('yoga', '2014-11-05 18:30:50', 4);
insert into events2(event_name, event_time, person_id)
    values('write', '2014-11-07 06:23:10', 2);
insert into events2(event_name, event_time, person_id)
    values('coffee', '2014-11-07 06:45:34', 3);
insert into events2(event_name, event_time, person_id)
    values('read', '2014-11-07 17:11:11', 3);
insert into events2(event_name, event_time, person_id)
    values('read', '2014-11-07 17:10:44', 4);
insert into events2(event_name, event_time, person_id)
    values('coffee', '2014-11-07 10:30:03', 2);
```

Now that we have data in two related tables we can do some interesting SQL queries.

```sql
select * from people;
select * from events;
-- and more intersting ones please
```

We have now seen some of the essential features of SQL and sqlite but the data we manufactured was not very interesting. A more realistic scenario would be one where we have a data file that we want to analyse. 

```sql
-- import file into db and do the things
```

