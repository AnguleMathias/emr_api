#!/bin/bash
function import {
    apt-get update && apt-get install sudo
    filename=$(basename $1)
    sudo -u emr_user psql -d emr_user < $filename
}

import $@