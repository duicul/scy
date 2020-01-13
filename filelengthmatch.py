from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import time
import traceback
import threading

data_log=""

def video_len(path):
    #print()
    #print(path)
    return False
    init=time.time()
    try:
        clip = VideoFileClip(path)
    except Exception:
        return False
    if clip is None:
        return False
    len_vid=clip.duration
    if len_vid is None:
        return False
    clip.reader.close()
    if clip.audio is None:
        return False
    else:
        clip.audio.reader.close_proc()

    #print(time.time()-init)
    #print()
    return len_vid

def match(file1,aux_file,ind1,dur1,size1,total):
    no_files=len(aux_file)
    for ind2 in range(ind1+1,no_files):
            perc=ind2/no_files
            #if ind1==0:
            #    status=[]
            #    for i in range(9):
            #        status.append(False)
            #    for ia in range(len(status)):
            #        if not status[ia]:
            #            if (ia+1)*0.1<perc:
            #                print("First pass:"+str(ia)+" "+str(perc*100)+"% "+str(status[ia]))
            #                status[ia]=True
            #                print(status)
            file2=aux_file[ind2][1]
            if(file1!=file2):
                try:
                    if len(aux_file[ind2])<= 2:
                        dur2=video_len(file2)
                        aux_file[ind2].append(dur2)
                        total=total+1
                    else:
                        dur2=aux_file[ind2][2]
                    if len(aux_file[ind2])<= 3:
                        size2=os.path.getsize(file2)
                        aux_file[ind2].append(size2)
                    else:
                        size2=aux_file[ind2][3]
                    if dur1 == dur2 and dur1!=False and dur2!=False :
                        data_log=data_log+("\nMatch duration: "+str(dur1)+" "+file1+" "+file2)
                        print("\nMatch duration: "+str(dur1))
                        print(file1)
                        print(file2)
                        print()
                    if aux_file[ind1][0] == aux_file[ind2][0]:
                        data_log=data_log+("\nMatch name: "+file1+" "+file2)
                        print("\nMatch name: "+aux_file[ind1][1])
                        print(file1)
                        print(file2)
                        print()
                    if size1 == size2:
                        data_log=data_log+("\nMatch size: "+str(size1)+" "+file1+" "+file2)
                        print("\nMatch size: "+str(size1)+" "+file1+" "+file2)
                        print(file1)
                        print(file2)
                        print()
                except Exception:
                    print(file1+" "+str(dur1))
                    print(file2+" "+str(dur2))
                    data_log=data_log+("\n"+traceback.format_exc())
                    print(traceback.format_exc())

def join_threads(thread_list):
    for thread in thread_list:
        thread.join()
    

def parse_dir(paths):
    data_log=""
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
            aux_file.append([file,root+"\\"+file])
    #print(aux_file)    
    no_files=len(aux_file)
    print("Files: "+str(no_files))
    data_log=data_log+"Files: "+str(no_files)
    total=0
    status_tot=[]
    thread_list=[]
    active_threads=0
    for i in range(9):
        status_tot.append(False)
    for ind1 in range(no_files):
        if ind1 == 1:
            print("Finished first pass")
            data_log=data_log+"\nFinished first pass\n"
        perc_tot=ind1/no_files
        #for i in range(len(status_tot)):
        #    if not status_tot[i]:
        #        if (i+1)*0.1<perc_tot:
        #            print("Total passes: "+str(perc_tot*100)+"%")
        #            status_tot[i]=True
        file1=aux_file[ind1][1]
        dur1=0
        size1=0
        if len(aux_file[ind1])<= 2:
            dur1=video_len(file1)
            aux_file[ind1].append(dur1)
            total=total+1
        else:
            dur1=aux_file[ind1][2]
        if len(aux_file[ind1])<= 3:
            size1=os.path.getsize(file1)
            aux_file[ind1].append(size1)
        else:
            size1=aux_file[ind1][3]
        t1 = threading.Thread(target=match, args=(file1,aux_file,ind1,dur1,size1,total)) 
        t1.start()
        thread_list.append(t1)
        active_threads+=1
        if active_threads >= 6 :
            join_threads(thread_list)
            active_thread=0
            thread_list=[]
        #match(file2,aux_file,ind1)
                    
    #print(L)
    #print(D)
    for t in thread_list:
        t.join()
    print(path)
    data_log=data_log+"\nOperations: "+str(total)
    data_log=data_log+"\n"+str(time.time()-init)
    print("Operations: "+str(total))
    print(time.time()-init)
    f = open("log_file.txt", "w")
    f.write(data_log)
    f.close()
    return L

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
        
parse_dir(["D:\ding\Site","D:\ding\Star"])
