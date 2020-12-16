path=$1
if [ $# -eq 0 ]
then echo "no file"
exit 
fi
#files=$(ls $path)
#echo $files
mkdir $path/convertedhls
files=$path/*
files_no=1
while [ $files_no -gt 0 ]
do 
files_no=0
for file in $files
do
echo $file
# extract config.ini
file_name="${file##*/}"
# get .ini 
file_extension="${file_name##*.}"
# get config 
file_main="${file_name%.*}"
# print it
echo "Full input file : $file"
echo "Filename only : $file_name"
echo "File extension only: $file_extension"
echo "First part of filename only: $file_main"
if [ -f "$file" ]
then 
	echo $file
	file_name=$(basename "$file")
	echo "filename " $file_name
	#-qscale 5
	mkdir "$path/$file_main"
	$(ffmpeg -i "$file_name" -f hls -hls_time 20 "$path/$file_main/$file_main.m3u8")
	mkdir "$path/old"
	mv  "$path/$file_name" "$path/old/$file_name"
	files_no=$(($files_no+1))
fi
done
files=$path/*
done