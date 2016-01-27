#! /bin/bash

/usr/local/bin/convert \
    $1[0] \
    -strip \
    -resize \
    300x400 \
    -compose \
    src \
    -gravity south \
    -extent \
    300x400 \
    png:hi_$1
