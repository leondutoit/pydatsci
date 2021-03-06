### pydatsci

The aim of the course is to expose participants to practical data analysis and visualisation work and equip them with the necessary knowledge and exposure to further develop your data science skills. Split into four parts, the course will walk through essential programming and data tools like version control, collaboration platforms, virtual machines and databases. Thereafter, we cover data manipulation with the python programming language using the pandas library. We will then use what we have learnt about data databases and data analysis to create an interactive web-based dashboard. To finish we will spend time further exploring topics and tools in data visualisation.

### Outline

Essential programming and data tools
* version control
* collaboration platforms
* python intro
* sqlite database

Data manipulation and web apps
* using the python pandas library for data manipulation
* Flask web framework

Web based interactive visualisation
* make a dashboard with Python, Javascript, html and css
* an intro to the d3 Javascript

Visualisation tools for analysis
* presentation graphics vs. exploratory graphics
* python statistical graphics libraries

### Expected programming experience and preparation

I will assume that you will have either done this or that you understand the material:
* [python](http://www.codecademy.com/tracks/python)
* [javascript](http://www.codecademy.com/tracks/javascript)

If you do not know about version control with git then it is a good idea to try it out [here](https://try.github.io/levels/1/challenges/1).

### Get the VM running

To run all the course material you can use Virtual Box to run an Ubuntu machine (with a GUI) that has everything already installed.

1. Download and install Oracle Virtual Box [here](http://download.virtualbox.org/virtualbox/4.2.0/)
2. Get the VM zip file: downloadable [here](https://dl.dropboxusercontent.com/u/104325750/pydatsci_vm.zip) warning: large zip file ~2GB, unzip it
3. Start the VM: in Vbox go to Machine -> Add -> ...path_to_folder.../pydatsci_vm/pydatsci_vm.box
4. Run the test script in the terminal (to open press `alt + ctl + t`): `$ ./test.sh`

Alternatively you can have a look at the `installs.sh` file and make sure you have everything running on your machine.

Note: for vbox [display](http://askubuntu.com/questions/452108/cannot-change-screen-size-from-640x480-after-14-04-installation-on-virtualbox-os) improvements.

### LICENSE

[AGPL](http://www.gnu.org/licenses/agpl-3.0.en.html). 2015. Copyright, Leon du Toit.
