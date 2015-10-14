import adb
from os.path import basename
import subprocess

a=adb.ADB()
android_side_dictionary = {}
windows_side_dictionary = {}
def file_list(folder_list):
    global a,android_side_dictionary
    #folder_list = ['/storage/sdcard0/DCIM/Camera',"/sdcard/bluetooth","/sdcard/images"]
    cmd = "shell sh /sdcard/copy3.sh "
    for each in folder_list:
        cmd = cmd + '\"%s\" '%each
    print cmd
    #to push file
    a.push("E:/practice/LINUX_SHELL_SCRIPT/copy3.sh","/sdcard/")
    print "push exited"
    #subprocess.call("adb shell rm /sdcard/a.txt")
    a.call_adb(cmd)
    text=subprocess.check_output("adb shell cat /sdcard/a.txt",shell = True)
    print "pulled"
    values = [ each.rstrip('\r\r') for each in text.split('\n')]
    keys = [basename(p) for p in values ]
    #print keys
    android_side_dictionary = dict(zip(keys,values))
    #print android_side_dictionary

    #print values
    """
    
    #values = a.split()
    values = [ '/'+ each for each in a.split()]

    #print keys
    android_side_dictionary=dict(zip(keys,values)) 
    #print android_side_dictionary.items()   
    #a.pull("/storage/sdcard0/a.txt","E:/practice/LINUX_SHELL_SCRIPT/")
    """

def get_file_list_from_destination(destination):
    import os
    import sys
    global windows_side_dictionary
    fileList = []
    absolute_path_list = []
    rootdir = destination
    for root, subFolders, files in os.walk(rootdir):
        for file in files:
            fileList.append(file)
            absolute_path_list.append(os.path.abspath(file))
    windows_side_dictionary=dict(zip(fileList,absolute_path_list))



if __name__ == "__main__":
    #file_list(['/storage/sdcard0/WhatsApp/Profile Pictures','/sdcard'])
    get_file_list_from_destination(r"E:\adb downloads")
    print windows_side_dictionary
    
