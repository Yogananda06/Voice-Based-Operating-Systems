import os
import sys
import subprocess
import pkg_resources
import time

if __name__=='__main__':

    required = {'selenium','webdriver-manager','speechrecognition','pyaudio','wikipedia','requests','playsound','gtts'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    temp_path = '/home/'+os.getlogin()+'/Desktop/os_miniproj'
    for res in missing:
        os.system("pip3 install "+res+"\npip3 install --upgrade "+res)

    command = "idle -r "+temp_path+"/sdf.py"
    os.system(command)
