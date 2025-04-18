#!/bin/bash

script_name="$0"

for file in `ls -p | grep -v / | grep -v ${script_name#*/} | grep -o '\..*$' | sort -uf`
do
	if [ ! -d "${file:1}" ]
	then
		mkdir "${file:1}"
	fi
	shopt -s nocaseglob
	mv *."${file:1}" "${file:1}"
	shopt -u nocaseglob
done
