#!/bin/bash
extension=".mkv"
for file in ./*;
do 
  basename=`basename $file ${extension}`
  echo "converting $basename";
  ffmpeg -i $file -codec copy ./output/${basename}${extension};
  echo "done";
done
