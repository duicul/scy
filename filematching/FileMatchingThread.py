'''
Created on Jul 31, 2020

@author: duicul
'''
import threading
import os
import traceback

class FileMatchingThread(threading.Thread):

    def __init__(self,file,file_range):
        threading.Thread.__init__(self)
        self.file=file
        self.file_range=file_range # 0-file_name 1-fullpath 2-duration 3-size
        self.data_log=[]
        
    def run(self):
        
        for file2 in self.file_range:
            
            if(self.file[0]==file2[1]):
                self.data_log.append({"match":"name","value":self.file[1],"file1":self.file,"file2":file2[1]})
                print("Match name "+str(self.file)+" "+str(file2))
            elif(self.file[2]==file2[2] and self.file[2]!=False and file2[2]!=False):
                self.data_log.append({"match":"duration","value":self.file[2],"file1":self.file[1],"file2":file2[1]})
                print("Match duration "+str(self.file[2])+" "+str(self.file)+" "+str(file2))
            elif(self.file[3]==file2[3] and self.file[3]!=False and file2[3]!=False):
                self.data_log.append({"match":"size","value":self.file[3],"file1":self.file[1],"file2":file2[1]})
                print("Match size "+str(self.file[3])+" "+str(self.file)+" "+str(file2))
            
if __name__ == '__main__':
    pass