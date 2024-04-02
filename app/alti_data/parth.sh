#!/bin/bash

if [ -f ./list.txt ]; then
    rm ./list.txt
fi

touch list.txt

ls ./unzip > list.txt
echo "Files identified"

if [ -d ./firstlayer ]; then
    rm ./firstlayer/* -R
    rmdir firstlayer
fi
if [ -d ./secondlayer ]; then
    rm ./secondlayer/* -R
    rmdir secondlayer
fi
if [ -d ./thirdlayer ]; then
    rm ./thirdlayer/* -R
    rmdir thirdlayer
fi

mkdir firstlayer
mkdir firstlayer/hd
mkdir firstlayer/ld

mkdir secondlayer
mkdir secondlayer/hd
mkdir secondlayer/ld
mkdir secondlayer/hd3
mkdir secondlayer/ld3
mkdir secondlayer/trans
mkdir secondlayer/trans2

mkdir thirdlayer
mkdir thirdlayer/hd
mkdir thirdlayer/ld
mkdir thirdlayer/hd3
mkdir thirdlayer/ld3
mkdir thirdlayer/trans
mkdir thirdlayer/trans2

echo "Architecture done"


echo "Parthing first layer 1/2..."
python3 parth1.py 
echo "Parthing first layer 2/2..."
python3 parth2.py

touch ./secondlayer/list.txt
ls ./firstlayer/hd/ > ./secondlayer/list.txt

mv ./firstlayer/hd/* ./secondlayer/hd
mv ./firstlayer/ld/* ./secondlayer/ld
cp add.py ./secondlayer/add.py
cp add2.py ./secondlayer/add2.py

cd secondlayer

echo "Parthing second layer 1/2..."
python3 add.py	
echo "Parthing second layer 2/2..."
python3 add2.py

cd ..

touch ./thirdlayer/list.txt
ls ./secondlayer/hd3/ > ./thirdlayer/list.txt

mv ./secondlayer/hd/* ./thirdlayer/hd
mv ./secondlayer/ld/* ./thirdlayer/ld
mv ./secondlayer/hd3/* ./thirdlayer/hd
mv ./secondlayer/ld3/* ./thirdlayer/ld
cp ad.py ./thirdlayer/ad.py
cp ad2.py ./thirdlayer/ad2.py

cd thirdlayer
echo "Parthing third layer 1/2..."
python3 ad.py  
echo "Parthing third layer 2/2..."
python3 ad2.py


# Output:
# 'File exists.' if the file is present
# 'File does not exist.' if the file is not present






#files="$@";

#text="ABCDEFG.m4a";

#echo ${text:(0):(-4)};
#echo $text

#mkdir mp3 2> /dev/null

#for t in ${files[@]}; do
#	echo ${t:(0):(-4)}
#	ffmpeg -i $t "./mp3/"${t:(0):(-4)}".mp3" 2> /dev/null
#	echo "done"
#done

#mv *.mp3 ./mp3/ 2> /dev/null
#rename -v 'y/_/ /' ./mp3/* > /dev/null
#echo "all done"
