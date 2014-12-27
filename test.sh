#!/bin/bash

echo "Testing your setup"

test_command() {
    if [[ ${1} != 0 ]]
        then
            echo ${2}
        else
            echo ${3}
    fi
}

py_packages=$(ipython -c 'import numpy, pandas, flask, scipy, statsmodels, matplotlib, ggplot')
packages_installed=$?

sqlite_status=$(sqlite3 -version)
sqlite_installed=$?

test_command \
    $packages_installed \
    "python package installation issue" \
    "python package installation all good"

test_command \
    $sqlite_installed \
    "sqlite3 not intalled" \
    "sqlite all good"
