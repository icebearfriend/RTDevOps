#!/bin/bash

if [ $# -eq 0 ] 
	then
		echo "Please enter a bucket name and a file in the same directory"
		exit 1
	elif [[ -z "$1" ]]; then
		echo "Please enter a bucket name"
		exit 1
	elif [[ -z "$2" ]]; then
		echo "Please enter a file name"
		exit 1
fi

d=$(date +%m-%d-%y)

cmd="aws s3api put-object --bucket $1 --key $d/$2 --body $2"

echo "Uploading $2 to s3://$1/$d/$2"

$cmd
