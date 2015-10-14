import adb
from easygui import *
import subprocess
import sys
import os
import path_list

B = adb.ADB()

class device():

    
    def __init__(self):
        self.device_name = ""
        self.saved_profile = {}
        self.current_profile ={}
        self.sdcard_list=["/storage/sdcard0"]
        self.sync_folder_list=[]
        self.sync_choice=""
        self.destination_directory = ""
        self.load_profile()

    def load_profile(self):
        import os.path

        if os.path.isfile("E:/super_final/profile.txt"):
            self.saved_profile=eval(open("E:/super_final/profile.txt").read())
            #print self.saved_profile
        else:
            self.saved_profile['device_name']=""

    def set_device (self):
        
        devices_list = B.attached_devices()
        if not devices_list:
            return False
        chosen_device = choicebox(msg="Select a device",title="Devices",choices=devices_list)
        print chosen_device
        print self.saved_profile["device_name"]
        if chosen_device == self.saved_profile['device_name']:
            response = ynbox("The device has a saved profile do you want to use it ?")
            if response:
                self.current_profile = self.saved_profile
                print "profile loaded"
                self.collect_copy_data(self.current_profile)
            else:
                self.device_name = chosen_device
                self.current_profile["device_name"] = self.device_name
                self.set_sdcard_list()
                #call copy function directly
        elif chosen_device is not None:
            self.device_name = chosen_device
            self.current_profile["device_name"] = self.device_name
            self.set_sdcard_list()

    def set_sdcard_list(self):
        dirs = B.folder_list("/storage")
        print type(dirs)
        if "sdcard1" in dirs:
            self.sdcard_list.append("/storage/sdcard1")
        else:
            if  "MicroSD" in dirs:
                print "MicroSD"
                self.sdcard_list.append("/storage/MicroSD")
        self.current_profile["sdcard_list"] = self.sdcard_list
        self.set_sync_folder_list()

    def set_sync_folder_list(self):
        for sdcard in self.sdcard_list:
            print sdcard
            display_list=B.folder_list(sdcard)
            selected_folders = multchoicebox(msg="Select Folders",title="Folders List",choices=tuple(display_list))
        
            try:
                if len(selected_folders) != 0:
                    self.sync_folder_list.extend(selected_folders)
                else:
                    self.set_sync_folder_list()
            except TypeError:
                if ynbox(msg="No folders selected.Are you sure you want to exit ?"):
                    sys.exit()
                else:
                    self.set_sync_folder_list()
                    
        self.current_profile["sync_folder_list"] = self.sync_folder_list
        self.set_destination_directory()
        
    def set_destination_directory(self):
        import json
        destination = diropenbox(msg="select sync folder",title="destination")
        
        destination=destination.replace("\\","/")
        self.destination_directory=destination
        self.current_profile['destination_directory'] = json.dumps(self.destination_directory).strip("\"")
        print destination
        self.set_sync_choice()
        

    def set_sync_choice(self):
        select_choice = ["1 Mobile to PC","2 PC to Mobile"]
        self.sync_choice = choicebox(msg="Select a sync type",title="sync-type",choices=tuple(select_choice))
        print self.sync_choice
        if self.sync_choice is not None:
            self.current_profile['sync_choice'] = self.sync_choice[0]
            #copy function call
            print "copy"
            self.save_profile()
            self.collect_copy_data(self.current_profile)
            
        else:
            if ynbox(msg="No sync type selected. Do you want to exit ?"):
                sys.exit()
            else:
                self.sync_choice()

    def save_profile(self):
        profile_text = open("E:/super_final/profile.txt","w")
        profile_text.write(str(self.current_profile))
        profile_text.close()
        print "profile_saved"

    def collect_copy_data(self,device_profile):

        flag=0
        print "collect_copy_data called"
        destination=device_profile['destination_directory']
        create_dir = ["Documents","Images","Audio","Video","Others"]
        if set(os.listdir(destination)).issuperset(set(create_dir)):
            pass
            
        else:
            flag=1
            print destination
            format_dirs=[]
            for each in create_dir:
                a=os.path.join(destination,each).replace('/','\\')
                format_dirs.append(a)
                os.mkdir(a)
                print "dirs made"
                #os.mkdir(os.path.join(destination,'/',each))
            print "called"
            format_dirs=[ each.replace('\\','/') for each in format_dirs]
            print format_dirs
            print flag
            path_list.file_list(self.sync_folder_list)
            folder_path_to_be_copied=path_list.android_side_dictionary.values()
            for each in folder_path_to_be_copied:
                file_extension=os.path.splitext(each)[-1]
                print file_extension
                
                if file_extension in ['.MP3', '.WMA', '.WAV', '.MP2', '.AAC', '.AC3', '.AU', '.OGG', '.FLAC']:
                    each = '/' + each
                    cmd = "pull %s %s"%(each,format_dirs[2])
                    #print cmd
                    B.call_adb(cmd)
                    #a.pull(each,format_dirs[2])
                elif file_extension in ['.jpg','.png','.JPG','.PNG']:
                    #print "jpg reached"
                    each = '/' + each
                    cmd = "pull %s %s"%(each,format_dirs[1])
                    B.call_adb(cmd)
                    #a.pull(each,format_dirs[1])
                elif file_extension in ['.pdf','.docx','.doc','.xls','.sh','.PDF']:
                    each = '/' + each
                    cmd = "pull %s %s"%(each,format_dirs[0])
                    B.call_adb(cmd)
                    #print "pdf copied"
                    #a.pull(each,format_dirs[0])

        

        
def main():
    new_device = device()
    new_device.set_device()

main()
