#Module to monitor the contents of the directory and keep track of files added/deleted/modified
#works for subdirectories as well


import os
import time
#function to just get file details
def get_filedetails(mydict,path):
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.'):
                moddate = os.stat(entry)
                mydict[entry.name]=time.ctime(moddate[8])
                if entry.is_dir()==True:
                    newpath=path+"/"+str(entry.name)
                    with os.scandir(newpath) as it1:
                        for entry1 in it1:
                            if not entry1.name.startswith('.'):
                                moddate = os.stat(entry1)
                                newstr=str(entry.name)+"/"+str(entry1.name)
                                mydict[newstr]=time.ctime(moddate[8])
    return mydict

#Check if file structure has changed, has there been move, adds or deletes
def check_filestructurechange(before,after):
    if set(before) ==set(after):
        print('No change.\n')
        return 0
    elif set(before) > set(after):
    #(len(before.keys()) > len(after.keys())):
        print('Some file deleted.\n')
        return -1
    elif set(before)<set(after):
    #(len(before.keys()) == len(after.keys())):
        print('Some file added .\n')
        return 1

#Checking if any of the files been changed
def check_filetimechange(before,path):
    newafter={}
    newafter=get_filedetails(newafter,path)
    new_dict = { key : 0 if (key in newafter) & (before[key]==newafter[key]) else 1 for key in before   }
    return new_dict

#can run this if I want to continously poll for a particular directory
def poll(current_status,path):
    keepgoing=True
    while(keepgoing):
        new_status={}
        new_status=get_filedetails(new_status,path).copy()
        filechange=check_filestructurechange(current_status,new_status)
        if filechange!=0:
            print("Updating directory structure to represent current status")
            current_status=new_status.copy()
        else:
            timechange=check_filetimechange(current_status,path)
            for key, value in timechange.items():
                    if timechange[key]==1:
                        print("Some files were modified, updating the current status")
                        moddate = os.stat(timechange[key])
                        current_status[key]=time.ctime(moddate[8])
        print("The current directory status is:"+"\n")
        print(current_status)
        vargoing=input("\nEnter y to keep polling: ")
        if vargoing!='y':
            keepgoing=False
        del(new_status)

if __name__ == "__main__":
    path=input("Please enter the path of the directory you want to monitor: ")
    #timesec=int(input("Enter time second interval to monitor in: "))
    current_status={}
    print("The current status is: ")
    current_status=get_filedetails(current_status,path).copy()
    print(current_status)
    print("Will track now!")
    poll(current_status,path)
