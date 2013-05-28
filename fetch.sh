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


function compare_the_size(){
    
    if [ ! -f "$1" ]; then
        return 1
    fi

	

  size=$(du -sb $1 | awk '{print $1 }')
  size_remote=$(curl -sI $2 | awk '/Content-Length/ { print $2 }')


  echo "SIZE: $size => REMOTE_SIZE: $size_remote"
  if [ "$size" == "${size_remote%?}" ]; then
	return 0
  fi
  SS=${size_remote%?}
  if [ $size -gt $SS ]; then
	return 0
  fi
  
  	return 1
 
}



while read line
do
    read md5 url filename size <<< $line

    outputfile=`echo $1/$filename`

    # Download file if it doesn't exist
    #if [ ! $(compare_md5 $outputfile $md5) ]; then
    #    curl -L -v  $url -o $outputfile 2>> logfile.txt
    #fi

     echo "Doing $outputfile"

    compare_the_size $outputfile $url
    ret=$?
    if [ $ret == "1" ]; then
	echo "the size is different: downloading:"
        curl -L -v  $url -o $outputfile 2>> logfile.txt
    fi



done










