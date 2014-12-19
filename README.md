#### pydatsci

The aim of the course is to expose participants to practical data analysis and visualisation work and equip them with the necessary knowledge and exposure to further develop your data science skills. Split into four parts, the course will walk through essential programming and data tools like version control, collaboration platforms, virtual machines and databases. Thereafter, we cover data manipulation with the python programming language using the pandas library. We will then use what we have learnt about data databases and data analysis to create an interactive web-based dashboard. To finish we will spend time further exploring topics and tools in data visualisation.

#### Outline

Essential programming and data tools
* version control
* collaboration platforms
* virtual machines
* python intro
* sqlite database

Data manipulation and web apps
* using the python pandas library for data manipulation
* Flask web framework

Web based interactive visualisation
* make a small dashboard with Javascript, html and css
* an intro to the d3 Javascript

Visualisation tools for analysis
* presentation graphics vs. exploratory graphics
* python statistical graphics libraries

#### Preparations

Before the workshop I recommend you do the following two things: get the vagrant virtual machine running on your machine, and get to know git if you are not already familiar with it. Follow the instructions below to do so.

#### Get vagrant running

1. Download and install Oracle Virtual Box [here](http://download.virtualbox.org/virtualbox/4.2.0/)
2. Download and install Vagrant for you platform [here](https://www.vagrantup.com/downloads)
3. Install Virtual Box Guest Additions: `$ vagrant plugin install vagrant-vbguest`
4. Download and install [git](http://git-scm.com/downloads) if you do not aleady have it 
5. Checkout this repository: `$ git clone https://github.com/leondutoit/pydatsci.git`
6. Navigate to the repository folder locally: `$ cd pydatsci`
7. Run: `$ vagrant up` - this will take a while...

You can now log in to the VM by doing `$ vagrant ssh`. Once logged in go to the `pydatsci` folder: `$ cd /vagrant`. Once there run the test script `./test.sh`. If this runs without reporting an error you are all set to go.


#### Try git

If you do not know about version control with git then it is a good idea to try it out [here](https://try.github.io/levels/1/challenges/1) to see what it is all about.
