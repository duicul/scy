path=$1
if [ $# -eq 0 ]
then echo "no file"
exit 
fi
#files=$(ls $path)
#echo $files
mkdir $path/converted480p
for file in $path/*
do
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
echo $file
file_name=$(basename "$file")
echo "filename " $file_name
$(ffmpeg -i "$file_name" -s 720x480 -c:a copy "$path/converted480p/$file_name")
done
