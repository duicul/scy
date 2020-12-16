'''
Created on Jul 31, 2020

@author: duicul
'''
import os 
import traceback
from moviepy.video.io.VideoFileClip import VideoFileClip
#import concurrent.futures
import time 
import json

from DataGatherThread import DataGatherThread
from FileMatchingThread import FileMatchingThread

class FileData:
    
    def __init__(self,paths,no_threads,outputfile):
        self.paths=paths
        self.file_data=[] # 0-file_name 1-fullpath 2-duration 3-size
        self.no_threads=no_threads
        self.outputfile=outputfile
        
    def parse_dir(self):
        L = []
        D = []
        for path in self.paths:
            for root, dirs, files in os.walk(path):
                print(root)
                L.append((root,files))
                D=D+dirs
        for (root,file_list) in L:
            for file in file_list:
                self.file_data.append([file,root+"\\"+file,False,False])
        return L    
    
    def join_threads_gather(self,thread_list):
        file_data=[]
        for thread in thread_list:
            while thread.is_alive():
                pass
            #print(thread.files)
            file_data+=thread.files
            thread.join()
            
        return file_data
    
    def join_threads_match(self,thread_list):
        file_data=[]
        for thread in thread_list:
            while thread.is_alive():
                pass
            #print(thread.files)
            file_data+=thread.data_log
            thread.join()
            
        return file_data
    
    def split_file_matching(self):
        thread_list=[]
        data_log=[]
        print("Starting file matching")
        
        for file_i in range(len(self.file_data)):
                curr_range=self.file_data[file_i+1:len(self.file_data)]
                           
                fmt=FileMatchingThread(self.file_data[file_i],curr_range)
                fmt.start()
                thread_list.append(fmt)
                
                if(len(thread_list)>=self.no_threads):
                    data_log+=self.join_threads_match(thread_list)
                    thread_list=[]
        
        return  data_log            
    
    def split_gather_data(self):
        thread_list=[]
        data_log=[]
        
        print("Files: "+str(len(self.file_data)))
        
        data_log.append({"file_no":len(self.file_data)})
        
        split_items_no=len(self.file_data)/self.no_threads
        
        for i in range(self.no_threads):
            right_head=split_items_no*(i+1) if split_items_no/self.no_threads*(i+1) < len(self.file_data) else len(self.file_data)
            curr_range=self.file_data[int(split_items_no*i):int(right_head)]
            print(str(int(split_items_no*i))+" -> "+str(int(right_head)))
            #print(curr_range)
            
            dgt=DataGatherThread(curr_range,True,i)
            dgt.start()
            thread_list.append(dgt)
            #with concurrent.futures.ThreadPoolExecutor(no_threads) as executor:
            #    thread_list.append(executor.submit(self.gather_data,curr_range,True))
        
        self.file_data=self.join_threads_gather(thread_list)
        #for file in self.file_data:
        #    print(str(file))
        #self.gather_data(list(range(100)),True)            
    
    def main(self):
        self.parse_dir()
        self.split_gather_data()
        data_log=self.split_file_matching()
        print(data_log)
        f = open(self.outputfile, "w")
        json.dump(data_log,f)
        
if __name__ == "__main__":
    fd=FileData(["E:\ding\Site\WhippedAss"],20,"match.log")
    fd.main()
    #for i in range(100):
    #    print(fd.file_data[i])
