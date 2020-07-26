path=$1
if [ $# -eq 0 ]
then echo "no file"
exit 
fi
#files=$(ls $path)
#echo $files
mkdir $path/converted480p
files=$path/*
files_no=1
while [ $files_no -gt 0 ]
do 
files_no=0
for file in $files
do
echo $file
# extract config.ini
#file_name="${file##*/}"
# get .ini 
#file_extension="${file_name##*.}"
# get config 
#file="${file_name%.*}"
# print it
#echo "Full input file : $file"
#echo "Filename only : $file_name"
#echo "File extension only: $file_extension"
#echo "First part of filename only: $file"
if [ -f "$file" ]
then 
	echo $file
	file_name=$(basename "$file")
	echo "filename " $file_name
	$(ffmpeg -i "$file_name" -s 840x480 -c:a copy "$path/converted480p/$file_name")
	mkdir "$path/old"
	mv  "$path/$file_name" "$path/old/$file_name"
	files_no=$(($files_no+1))
fi
done
files=$path/*
done
