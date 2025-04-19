#!/bin/bash
# Lecturer: Nguyen Ho Man Rang
# Department of Computer Science 2006-2018
# Intro AI [192]
# Script for assignment 01

CURR=`pwd`
# Path to the Workspace
ASSHOME=$CURR


# Each SubFolder contains results of a student
RESULT=$ASSHOME/result
if [ ! -d "$RESULT" ]; then
	mkdir "$RESULT"
fi

# Temporary folder that we use to compile and run
DEST="$ASSHOME"/template
SUBMIT="$ASSHOME"/submission

FILE1=search.py
FILE2=searchAgents.py

# *****************************************************************************
				# START PROGRAM
# *****************************************************************************
for STUSUB in $SUBMIT/*
do 
	fname=${STUSUB##*/}
	STURES="$RESULT"/"$fname"
	if [ ! -d "$STURES" ]; then
		mkdir "$STURES"
	fi
	echo $fname
	if [ ! -f "$STUSUB"/"$FILE1" ]; then
		echo $FILE1 " is not found "> "$STURES"/result.txt
		echo "[0, 0, 0, 0, 0, 0, 0, 0]" >> "$STURES"/result.txt
	elif [ ! -f "$STUSUB"/"$FILE2" ]; then
		echo $FILE2 " is not found "> "$STURES"/result.txt
		echo "[0, 0, 0, 0, 0, 0, 0, 0]" >> "$STURES"/result.txt
	else
		# copy the submit file to temporary folder
		cp "$STUSUB"/"$FILE1" "$DEST"
		cp "$STUSUB"/"$FILE2" "$DEST"
		cd "$DEST"
		python3 autograder.py > "$STURES"/result.txt
		rm -rf "$STUSUB"
	fi
	cd "$ASSHOME"
done


