#! /bin/bash

/usr/local/bin/convert \
    $1[0] \
    -alpha \
    off \
    -strip \
    -colorspace \
    gray \
    -normalize \
    -gamma \
    2.2 \
    -quality \
    100 \
    jpg:/tmp/cv.jpg

/usr/local/bin/convert \
    $1[0] \
    -alpha \
    off \
    -strip \
    -crop \
    `/home/cards/sarcards/face.py /tmp/cv.jpg` \
    +repage \
    -colorspace \
    gray \
    -resize \
    70x70 \
    -normalize \
    -gamma \
    2.2 \
    -define \
    jpeg:extent=1024 \
    -quality \
    100 \
    jpg:thumb_$1
