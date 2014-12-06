
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

Language info, repl etc

#### Data types

#### Data structures

#### Functions

#### Packages


### Relational databases

#### sqlite

```sql
$ sqlite3
# BOOM!
```
