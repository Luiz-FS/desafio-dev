#!/bin/bash

docker-compose -f docker-compose.yml up --build -d db;
python3 -m pip install virtualenv
virtualenv env
source env/bin/activate

services=()

for directory in * ; do
    if [ -d $directory ] ; then
        services+=($directory)
    fi
done

for service in ${services[@]} ; do

    if [ "$service" = "frontend" ] || [ "$service" = "env" ] ; then
        continue
    fi
    echo "=> Testing service $service"
    echo
    cd $service
    sh test_runner/before_install.sh
    sh test_runner/test.sh
    cd ..
    echo
done
