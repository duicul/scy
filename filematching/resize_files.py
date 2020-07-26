from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import time
import traceback
import threading
import concurrent.futures
import json
import moviepy.editor as mp
data_log=[]


def parse_dir(paths,out_dir,max_threads,outputfile):
    data_log=[]
    init=time.time()
    # List to store all   
    # directories  
    L = []
    D = []
    # Traversing through Test
    for path in paths:
        for root, dirs, files in os.walk(path):
            print(root)
            L.append((root,files))
            D=D+dirs
    print(paths)
    #print(L)
    #print(D)
    aux_file=[]
    for (root,file_list) in L:
        for file in file_list:
            split_list=file.split(".")
            ext=split_list[len(split_list)-1]
            if ext=="avi" or ext=="mkv" or ext=="mp4" or ext=="wmv" or ext=="mov" or ext=="flv":
                outfile=""
                for i in range(len(split_list)-2):
                    outfile+=(split_list[i]+".")
                outfile+=split_list[len(split_list)-2]
                outfile+="360p."
                outfile+=ext
                aux_file.append([file,root,outfile])
    #print(aux_file)    
    no_files=len(aux_file)
    print("Files: "+str(no_files))
    mess_inp=input("To Continue Press ENTER Key  To Exit Type exit \n")
    if str(mess_inp)=="exit":
        exit()
    print("Processing ... ")
    data_log.append({"file_no":no_files})
    #data_log=data_log+"Files: "+str(no_files)
    total=0
    status_tot=[]
    thread_list=[]
    active_threads=0
    #print(aux_file)
    for i in aux_file:
        print(i[0].split("."))
        print(i)
    print()
    for i in aux_file:
        print(i[0]+" --> "+i[2])
        print(i[1]+"\\"+i[0])
        try:
            clip = mp.VideoFileClip(i[1]+"\\"+i[0])
            clip_resized = clip.resize(height=640,width=360) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
            clip_resized.write_videofile(out_dir+"\\"+i[2],codec='libx264',threads=4,logger='bar',preset="superfast")
            clip.close()
            clip_resized.close()
        except :
            print(traceback.format_exc())
        
        
def compare_dirs(Dir1,Dir2):
        for file1 in Dir1:
            dur1=video_len(file1[1])
            for file2 in Dir2:
                dur2=video_len(file2[1])
                if file1[0] == file2[0]:
                    print("\nMatch name:")
                    print(file1[1])
                    print(file2[1])
                    print()
                elif dur1 == dur2 :
                    print("\nMatch duration: "+str(dur1))
                    print(file1[1])
                    print(file2[1])
                    print()
if __name__ == "__main__":
    data_log=""
    #"E:\ding"
    #"D:\ding\Site"
    parse_dir(["C:\\Users\\duicul\\Downloads\\PornMegaLoad.15.03.06.Ayn.Marie.Making.Dreams.Come.True.XXX.1080p.MP4-KTR[rarbg]"],"C:\\Users\\duicul\\Downloads\\PornMegaLoad.15.03.06.Ayn.Marie.Making.Dreams.Come.True.XXX.1080p.MP4-KTR[rarbg]",20,"log_file.txt")
