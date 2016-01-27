#! /bin/bash

/usr/local/bin/convert \
    $1[0] \
    -alpha \
    off \
    -strip \
    -resize \
    70x70 \
    -quality \
    80 \
    jpg:thumb_$1
