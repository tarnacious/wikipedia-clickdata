#!/bin/bash

# params: file, md5
function compare_md5() {
    if [ ! -f "$1" ]; then
        return
    fi
    calculated_md5=$(md5sum "$1" | cut -c1-32)
    if [ "$2" == "$calculated_md5" ]; then
        echo "valid"
    fi
}

while read line
do
    read md5 url filename size <<< $line

    outputfile=`echo $1/$filename`

    # Download file if it doesn't exist
    if [ ! $(compare_md5 $outputfile $md5) ]; then
        curl -L -v  $url -o $outputfile 2>> logfile.txt
    fi


    if [ $(compare_md5 $outputfile $md5) ]; then
        echo "Complete $outputfile"
    else
        echo "Error $outputfile"
    fi
done



