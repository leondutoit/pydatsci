
We will use the vagrant VM as a code execution environment while all files and git repositories will be created on our own machines and accessed from the VM via shared folders.

### Manage and share code

We will keep the code we write throughout the workshop in version controlled git repositories on our own machines. You must, therefore, have git installed. Create a workshop folder `$ mkdir ccampus_pydatsci`. Step into that folder `$ cd ccampus_pydatsci`. This is where we will create all our files and directories.

#### git

Let's go through a basic workflow with git in our new workshop directory.

```sh
$ git init
$ git branch
$ touch .gitignore
$ echo "*~" >> .gitignore
$ touch README.md
$ echo "This is my ccampus_pydatsci folder" >> README.md
$ git status
$ git add .gitinore
$ git add README.md
$ git status
$ git commit -m 'first commit: add gitignore and reamde to project'
$ git status
$ git log
```

#### github

If you want, you can [add the local repo to github](https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/) but that is up to you. Here is how you can do it:

```sh
# do it...
```

More about github...

### Reproducible work

#### Vagrant VM

```sh
$ vagrant --help
# and more
```

### Python programming

#### Data types

#### Data structures

#### Functions


### Relational databases

#### sqlite

```sql
$ sqlite3
# BOOM!
```
