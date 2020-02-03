#!/bin/bash

workdir=$(cd $(dirname $0); pwd)
cd ${workdir}

helpFunction()
{
   echo ""
   echo -e "\t-f File name containing the connection data such as file.csv"
   echo -e "\t-c Number of connections"
   echo -e "\t-t Number of threads"
   echo -e "\t-d Duration time of testing"
   echo -e "\t-s Server IP"
   exit 1 # Exit script after printing help
}

while getopts "f:c:t:d:s:" opt
do
   case "$opt" in
      f ) f="$OPTARG" ;;
      c ) c="$OPTARG" ;;
      t ) t="$OPTARG" ;;
      d ) d="$OPTARG" ;;
      s ) s="$OPTARG" ;;

   esac
done


if [ -z "$f" ] || [ -z "$c" ] || [ -z "$t" ]|| [ -z "$d" ]|| [ -z "$s" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

# Begin script in case all parameters are correct
echo "File name: $f"
echo "Number of connections: $c"
echo "Number of threads: $t"
echo "Duration time of testing: $d"
echo "Server ip: $s"
        
python pathGenerator.py $f
wrk -c $c -t $t -d $d -s multiplepaths.lua ${s}

