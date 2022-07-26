import sys
import subprocess
import pkg_resources

import speech_recognition as sr #convert speech to text
import datetime #for fetching date and time
import wikipedia
import webbrowser
import requests
import playsound # to play saved mp3 file
from gtts import gTTS # google text to speech
import os # to save/open files
from selenium import webdriver # to control browser operations
import time
import os.path
from os import path
from functions import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
import speech_recognition as sr
from tkinter import *


def button_clicked():
    respond("Ok bye and take care")
    sys.exit()

def callback():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(e1.get())
    forms = driver.find_elements(By.XPATH, '//form')
    j=0
    for form in forms:
        j+=1
        all_inputs = driver.find_elements(By.XPATH, f'//form[{j}]//input')
        i=0
        for input in all_inputs:
            #print(input)
            i+=1
            if input.get_attribute('type') != "hidden" and input.get_attribute('type')!="password":
                text_area = input
                text = talk("")
                if(input.get_attribute('type') == "email" or input.get_attribute('name') == "email"):
                    text = text.replace(' at the rate of ','@')
                    text = text.replace(' at the rate ','@')
                    text=text.replace(" at ","@")
                    text=text.replace(" ","")
                print(text)
                text_area.send_keys(text)


# function takes the voice command from user
def talk(k):
    input=sr.Recognizer()
    with sr.Microphone() as source:

        if(k==""): d=1
        else: d=k
        input.adjust_for_ambient_noise(source,duration=d)

        audio=input.listen(source)
        data=""
        try:
            data=input.recognize_google(audio)
            print("Response is: " + data)

        except sr.UnknownValueError:
            respond("Sorry I did not hear you, Please repeat again.")
            return talk("").lower()
    return data


# function which speaks out
def respond(output):
    num=0
    print(output)
    num += 1
    response=gTTS(text=output, lang='en')
    file = str(num)+".mp3"
    response.save(file)
    playsound.playsound(file, True)
    os.remove(file)


# function to return the extensions for the files
def file_types(type_):
    if type_=='python': return 'py'

    elif type_ in ['c++' ,'cpp','cplusplus','c plus plus','seeplusplus','see plus plus']: return 'cpp'

    elif 'c' in type_: return 'c'

    elif type_ == 'text': return 'txt'

    elif type_ == 'spreadsheet' : return 'xlsx'

    elif type_ == 'writer' : return 'odt'

    elif type_ == 'draw': return 'odg'

    return 0

def list_dir():
    for i in os.listdir():
        print(i,end=", ")



if __name__=='__main__':

    window1=Tk()
    window1.title('VOICE CONTROL')
    window1.geometry("400x300+10+10")

    user = os.getlogin()

    respond("Hi "+user)
    flag=0
    while(1):

        lbl=Label(window1, text="Click any of the button below", fg='Black', font=("Times", "16", "bold italic"))
        lbl.place(x=60, y=50)
        btn1 = Button(window1, text='Speak',command=lambda:[window1.destroy()])
        btn1.place(x=150, y=100)
        btn3 = Button(window1, text='Exit',command=lambda:[window1.destroy(),button_clicked()])
        btn3.place(x=150, y=150)
        window1.mainloop()
        while(1):
            if flag<2:
                respond("How can I help you?")
                text=talk("").lower()

            else:
                respond("Sorry, I can't get you. Please type your command")
                text=input("Please type your command: ")
                text=text.lower()
                flag=0

            if text==0:
                continue

            # stop/exit/bye   ->To exit the controller
            if "stop" in str(text) or "exit" in str(text) or "bye" in str(text):
                respond("Ok bye and take care")
                break

            # create directory/folder  <NAME>
            # create python/C/C++/text file <NAME>
            elif "create" in text :
                text = text.replace('create ','')
                if("directory" in text):
                    name=text.replace( 'directory ',"")
                    if not create_folder(name,os.getcwd()):
                        respond("name not recognised! and folder not created.")
                    print(list_dir())

                elif("folder" in text):
                    name=text.replace( 'folder ',"")
                    if not create_folder(name,os.getcwd()):
                        respond("name not recognised! and folder not created.")
                    print(list_dir())

                elif("file" in text):
                    name=text.replace( 'file ',"")
                    types = name.split()
                    exten = file_types(types[0])
                    if exten:
                        name = types[1]
                        if not create_file(name,exten,os.getcwd()):
                            respond(f"{name} file not created")
                        print(name, list_dir())

                else:
                    respond('Please tell the command correctly')



            # youtube <QUERY>
            elif 'youtube' in text:
                query = text.replace("youtube","")
                if query!="":
                    respond("Opening in youtube")
                    query=query.replace(" ","")
                    webbrowser.open("http://www.youtube.com/results?search_query="+str(query))
                    time.sleep(3)
                else:
                    respond("Please say something to search in youtube")


            # show folder/folders/
            # show path
            elif "show" in text:
                if "show folder" in text:
                    print(list_dir())
                elif "show path" in text:
                    print(os.getcwd())
                else:
                    respond('Please tell the command correctly')


            # wikipedia <QUERY>
            elif 'wikipedia' in text:
                respond('Searching Wikipedia')
                text =text.replace("wikipedia", "")
                results = wikipedia.summary(text, sentences=3)
                respond("According to Wikipedia")
                print(results)
                respond(results)
                time.sleep(3)


            # time
            elif 'time' in text:
                strTime=datetime.datetime.now().strftime("%H:%M:%S")
                respond(f"the time is {strTime}")


            # open folder/directory <NAME>
            # open application <NAME>
            # open google
            # open python/C/C++/text file <NAME>
            elif 'open' in text:
                text=text.replace("open ","")
                if 'folder' in text:
                    name=text.replace("folder ","")
                    if not open_folder(os.path.join(os.getcwd(),name)):
                        respond('Folder is not opened')

                if 'directory' in text:
                    name=text.replace("directory ","")
                    if not open_folder(os.path.join(os.getcwd(),name)):
                        respond('Folder is not opened')

                elif 'application' in text:
                    name = text.replace('application ','')
                    if "writer" in name: name = "office writer"
                    elif "spreadsheet" in name: name  = "office calc"
                    elif "draw" in name :name = "office draw"
                    if not open_application(name):
                        respond(f"{name} not opened")


                elif 'file' in text:

                    temp =''
                    text=text.replace("file ","")
                    types=text.split()
                    exten=file_types(types[0])
                    if exten == 'odt':
                        temp=os.path.join(os.getcwd(),types[1]+'.'+exten)
                        if not os.path.exists(temp):
                            temp=os.path.join(os.getcwd(),types[1]+'.docx')
                    if exten==0: respond("File type must be python, c, c plus plus, odt, docx, xlsx or text only!")
                    else:
                        types[1]=types[1]+"."+exten
                    if not open_file(os.path.join(os.get_cwd(),types[1])):
                        respond('File not opened')


                elif 'google' in text:
                   if not web_search(''):
                       respond('Google not opened')
                   else:
                       respond("Google is open")
                   time.sleep(3)

                else:
                    respond('Please tell the command correctly')
                    
            elif 'application' in text:
                    name = text.replace('application ','')
                    if "writer" in name: name = "office writer"
                    elif "spreadsheet" in name: name  = "office calc"
                    elif "draw" in name :name = "office draw"
                    if not open_application(name):
                        respond(f"{name} not opened")


            # rename python/C/C++/text file <SOURCE> to <DESTINATION>
            # rename <SOURCE> to <DESTINATION>   -> for folders/directories
            elif 'rename' in text:
                text=text.replace("rename ","").replace("to","")
                if 'file' in text:
                    text = text.replace('file ','')
                    types = text.split()
                    if len(types) ==3:
                        exten = file_types(types[0])
                        if exten:
                            types[1]=types[1]+'.'+exten
                            types[2]=types[2]+'.'+exten
                            flag=rename_dir_file(os.path.join(os.getcwd(),types[1]),os.path.join(os.getcwd(),types[2]))
                            if flag==-1:
                                respond('Not renamed because source file doesnt exits')
                            elif flag==0:
                                respond(f'{types[2]} already exists')


                else:
                    ind=text.split()
                    file1=ind[0]
                    file2=ind[1]
                    k=rename_dir_file(os.path.join(os.getcwd(),file1),os.path.join(os.getcwd(),file2))
                    if k==0: respond("Rename failed")
                    elif k==-1: respond("Folder doesn't exists")
                    else: respond("Rename successful")



            #edit python/C/C++/text file <NAME>
            # content .....
            elif 'edit' in text:
                text = text.replace('edit ','')
                if 'file ' in text:
                    name=text.replace( 'file ',"")
                    types = name.split()
                    exten = file_types(types[0])
                    if exten:
                        name = types[1]
                        name=name+'.'+exten
                        if not fill_file(os.path.join(os.getcwd(),name)):
                            respond(f"{name} file not opened")

                else:
                    respond('Please tell the command correctly')


            # run python/C/C++/ file <NAME>
            elif 'run' in text:
                text=text.replace("run ","")
                if 'file ' in text:
                    text=text.replace("file ","")
                    types = text.split()
                    exten = file_types(types[0])
                    if exten:
                        if not run_file(os.path.join(os.getcwd(),types[1]+'.'+exten)):
                            respond('File Not executed')
                    print(text)

                else:
                    respond('Please tell the command correctly')


            # search <QUERY>/NULL
            elif 'search'  in text:
                if "search " in text:
                    text = text.replace("search ", "")
                else:
                    text = text.replace("search",'')
                web_search(text)
                time.sleep(5)



            # delete folder/directory <NAME>
            # delete python/C/C++/text file <NAME>
            elif 'delete' in text:
                text = text.replace('delete ','')
                if 'folder' in text:
                    name = text.replace('folder ','')
                    if not delete_folder(name,os.getcwd()):
                        respond(f'{name} folder not deleted')
                    print(list_dir())

                elif 'directory' in text:
                    name = text.replace('directory ','')
                    if not delete_folder(name,os.getcwd()):
                        respond(f'{name} folder not deleted')
                    print(list_dir())

                elif 'file' in text:
                    name=text.replace( 'file ',"")
                    types = name.split()
                    exten = file_types(types[0])
                    if exten:
                        name = types[1]
                        if not delete_file(name+'.'+exten,os.getcwd()):
                            respond(f"{name} file not created")
                        print(name)
                    print(list_dir())

                else:
                    respond('Please tell the command correctly')



            # change directory/folder <NAME>
            elif 'change' in text:
                text = text.replace('change ','')
                if 'folder' in text:
                    name  =text.replace('folder ','')
                    if not change_dir(os.getcwd(),name):
                        respond('Folder not changed')
                elif 'directory' in text:
                    name = text.replace('directory ','')
                    if not change_dir(os.getcwd(),name):
                        respond('Folder not changed')

                else:
                    respond('Please tell the command correctly')



            # back
            elif 'back' in text:
                if not go_back(os.getcwd()):
                    respond('directory not changed')



            # shutdown in <TIME(in minutes)> seconds/minutes/hours
            elif 'shutdown' in text:
                t=1
                text = text.replace('shutdown in ','')
                text = text.replace('shutdown','')
                if 'in' in text:
                    time_ = text.split()
                    if time_[1] == 'seconds':
                        t=int(time_[0])/60
                    if time_[1] == 'minutes':
                        t = int(time_[0])
                    if time_[1] == 'hours':
                        t= int(time_[0])*60

                respond('Are you sure do you want to shutdown')
                response = talk("").lower()
                if 'yeah' or 'yes' in response:
                    if not shutdown(t,''):
                        respond("shut down failed")

            # restart
            elif 'restart' in text:
                restart()


            # close all
            elif 'close all' in text:
                stop_all()

            #form filling
            elif 'form' in text:
                root = Tk()
                root.geometry("500x350")

                Label(root, text="Enter the URL of the form:").place(x=20,y=20)

                e1 = Entry(root,width=50)

                e1.place(x=20,y=70)

                button1 = Button(root, text="Submit",command=callback).place(x=20,y=90)
                button = Button(root, text="Exit",command=root.destroy).place(x=20,y=120)
                root.mainloop()

            else:
               respond("Application not available")
               flag+=1
            window2=Tk()
            window2.title('VOICE CONTROL')
            window2.geometry("400x300+10+10")
            lbl=Label(window2, text="Click any of the button below", fg='Black', font=("Times", "16", "bold italic"))
            lbl.place(x=60, y=50)
            btn2 = Button(window2, text='speak',command=lambda:[window2.destroy()])#
            btn2.place(x=150, y=100)
            btn4 = Button(window2, text='exit',command=lambda:[window2.destroy(),button_clicked()])#
            btn4.place(x=150, y=150)
            window2.mainloop()
