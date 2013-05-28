function check_size ()
{

    if [ ! -f "processed/$1" ]; then
        return 1
    fi
   

   size=$(du -sb processed/$1 | awk '{print $1 }')	
   
  if [ $size -gt 0 ]; then
	return 0
  else
	return 1
  fi 
   

}




while read line
do
    
     filename=$(basename "$line")
    filename=`echo $line | awk '{print $3}'`
    name="${filename%.*}"

    echo $filename
  

    check_size $name
    ret=$?
    if [ $ret == "1" ]; then
        echo "Processing the file: $name"
    gunzip -c archive/$filename | grep "^en " | awk '{ print $2, $3 }' > processed/$name

     else
	echo "Skipping the file $name: already exists"
    fi

done
