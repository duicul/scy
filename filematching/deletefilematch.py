import os,os.path
import time
import traceback
import json
import stat 
def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise



def remove_duplicate(files):
    print(str(len(files)-2)+" matches")
    cnt=0
    for data in files:
        
        match_type=None
        try:
            match_type=data["match"]
        except:
            continue
        file1=data["file1"]
        file2=data["file2"]
        if not os.path.isfile(file1) or not os.path.isfile(file2):
            continue
        size1=""
        size2=""
        if match_type == "name" or match_type=="duration":
            size1=os.path.getsize(file1)
            size2=os.path.getsize(file2)
        elif match_type == "size":
            size1=data["value"]
            size2=data["value"]
        cnt+=1
        print(str(cnt)+"/"+str(len(files)-2))
        print("Match "+match_type)
        print("Choose delete: ")
        print("1 "+str(file1))
        print("size: "+str(size1))
        print("2 "+str(file2))
        print("size: "+str(size2))
        print("3 None")
        print()
        opt=input("Choose option: ")
        if not opt.isdigit():
            print("Option not recognised")
            continue
        if int(opt)==1:
            os.chmod(file1, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
            os.remove(file1)
            print("Deleted "+file1)
        elif int(opt)==2:
            os.chmod(file2, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
            os.remove(file2)
            print("Deleted "+file2)
        print()
        print()
            
if __name__ == "__main__":
    f=open("log_file.txt","r")
    files=json.load(f)
    remove_duplicate(files)