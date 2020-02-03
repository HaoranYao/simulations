#!/bin/bash
workdir=$(cd $(dirname $0); pwd)
cd ${workdir}

helpFunction()
{
   echo ""
   echo -e "\t-f File name containing the connection data such as file.csv"
   exit 1 # Exit script after printing help
}

while getopts "f:" opt
do
   case "$opt" in
      f ) f="$OPTARG" ;;
   esac
done

if [ -z "$f" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

python fileGenerator.py $f
#sudo python3 -m http.server 80 
