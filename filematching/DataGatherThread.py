'''
Created on Jul 31, 2020

@author: duicul
'''
import threading
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
import traceback

class DataGatherThread (threading.Thread):
    
    def __init__(self, files,measure_duration,thread_no):
        threading.Thread.__init__(self)
        self.files = files # 0-file_name 1-fullpath 2-duration 3-size
        self.measure_duration = measure_duration
        self.thread_no=thread_no
        
    def video_len(self,path,measure_len):
        if not measure_len:
            return False
        try:
            clip = VideoFileClip(path)
        except Exception:
            #print(path)
            #print(str(traceback.format_exc()))
            return False
        if clip is None:
            return False
        len_vid=clip.duration
        #print(len_vid)
        if len_vid is None:
            return False
        clip.reader.close()
        if clip.audio is None:
            return False
        else:
            clip.audio.reader.close_proc()
        return len_vid
    
    
    def gather_data(self,file_range_search,measure_duration):
        #if range_search[len(range_search)-1]>=len(self.file_data):
        #    return
        
        ret_file_data=[]
        for file in file_range_search:
            #print(self.file_data[i][1])
            file[2]=self.video_len(file[1],measure_duration)
            file[3]=os.path.getsize(file[1])
            #print(file)
            ret_file_data.append(file)
        
        self.files=ret_file_data
        #print(self.files)
    
    def run(self):
        print("Starting: "+str(len(self.files))+" files no:"+str(self.thread_no))
        self.gather_data(self.files, self.measure_duration)
        print("Finish: "+" no: "+str(self.thread_no))
if __name__ == '__main__':
    pass